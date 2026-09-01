"""
Fintech Fraud & Risk Management Service
Evaluates financial transactions against rule engines, velocity models, and anomaly heuristics.
Zero external library dependencies.
"""

import uuid
import json
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

from backend.core.models import FraudRule, RiskLevel, Transaction
from backend.core.database import DatabaseManager


class FraudService:
    """Real-time rule evaluation and heuristic risk scoring engine for financial operations."""

    def __init__(self, db: DatabaseManager):
        self.db = db
        self._init_default_rules()

    def _init_default_rules(self) -> None:
        """Seeds standard banking risk rules if not present."""
        rules = [
            ("rule_large_tx", "High Amount Anomaly Threshold", "AMOUNT_THRESHOLD", 10000.0, "FLAG", "Flag single transactions exceeding $10,000 for AML scrutiny"),
            ("rule_extreme_tx", "Extreme Critical Transfer Threshold", "AMOUNT_THRESHOLD", 50000.0, "BLOCK", "Block transactions exceeding $50,000 without prior authorization"),
            ("rule_velocity_rapid", "Rapid Fire Velocity Check (5 min)", "VELOCITY_COUNT", 5.0, "FLAG", "Flag when more than 5 transfers occur in a 5-minute window"),
            ("rule_velocity_burst", "High Burst Velocity Check (1 min)", "VELOCITY_COUNT", 3.0, "REVIEW", "Require review when more than 3 transfers occur in 1 minute"),
            ("rule_round_sum_aml", "Structuring / Smurfing Anomaly", "STRUCTURING", 9900.0, "FLAG", "Flag amounts just below reporting thresholds ($9,500 - $9,999)")
        ]
        for r_id, name, r_type, thresh, act, desc in rules:
            existing = self.db.query_one("SELECT id FROM fraud_rules WHERE id = ?;", (r_id,))
            if not existing:
                self.db.execute(
                    """
                    INSERT INTO fraud_rules (id, name, rule_type, threshold, action, is_active, description)
                    VALUES (?, ?, ?, ?, ?, 1, ?);
                    """,
                    (r_id, name, r_type, thresh, act, desc)
                )

    def evaluate_transaction(
        self,
        source_account_id: Optional[str],
        destination_account_id: Optional[str],
        amount: float,
        currency: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, RiskLevel, List[str], str]:
        """
        Calculates aggregate risk score (0.0 to 100.0) and assigns an actionable risk level.
        Returns: (risk_score, risk_level, triggered_rule_messages, recommended_action)
        """
        score = 0.0
        triggers: List[str] = []
        highest_action = "ALLOW"

        meta = metadata or {}
        ip_country = meta.get("ip_country", "US")
        user_country = meta.get("user_country", "US")

        # 1. Evaluate Geographic Anomaly
        if ip_country != user_country:
            score += 25.0
            triggers.append(f"Geo-location mismatch: IP origin ({ip_country}) differs from registered home ({user_country})")

        # 2. Evaluate Dynamic DB Rules
        rules = self.list_rules()
        for r in rules:
            if not r.is_active:
                continue

            if r.rule_type == "AMOUNT_THRESHOLD":
                if amount >= r.threshold:
                    if r.action == "BLOCK":
                        score += 50.0
                        highest_action = "BLOCK"
                    else:
                        score += 30.0
                        if highest_action != "BLOCK":
                            highest_action = "FLAG"
                    triggers.append(f"Exceeded threshold rule '{r.name}': ${amount:,.2f} >= ${r.threshold:,.2f}")

            elif r.rule_type == "STRUCTURING":
                # Detect smurfing / intentional structuring just below $10k
                if 9500.0 <= amount <= 9999.99:
                    score += 40.0
                    triggers.append(f"Potential AML structuring pattern detected: amount is ${amount:,.2f}")
                    if highest_action not in ["BLOCK", "REVIEW"]:
                        highest_action = "FLAG"

        # 3. Evaluate Velocity Heuristics (Recent transactions in last 5 minutes)
        if source_account_id:
            five_mins_ago = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
            recent_count_row = self.db.query_one(
                """
                SELECT COUNT(*) as count, SUM(amount) as total_vol
                FROM transactions
                WHERE source_account_id = ? AND created_at >= ?;
                """,
                (source_account_id, five_mins_ago)
            )
            count = recent_count_row["count"] if recent_count_row else 0
            if count >= 5:
                score += 35.0
                triggers.append(f"High transaction frequency: {count} transactions initiated in the past 5 minutes")
                if highest_action != "BLOCK":
                    highest_action = "FLAG"
            elif count >= 3:
                score += 15.0
                triggers.append(f"Moderate transaction velocity: {count} transfers in past 5 minutes")

        # 4. Normalize Score & Determine Risk Level
        score = min(100.0, round(score, 1))

        if score >= 75.0 or highest_action == "BLOCK":
            level = RiskLevel.CRITICAL
            recommended_action = "BLOCK"
        elif score >= 50.0:
            level = RiskLevel.HIGH
            recommended_action = "REVIEW"
        elif score >= 25.0:
            level = RiskLevel.MEDIUM
            recommended_action = "FLAG"
        else:
            level = RiskLevel.LOW
            recommended_action = "ALLOW"

        return score, level, triggers, recommended_action

    def list_rules(self) -> List[FraudRule]:
        """Returns all configured risk rules."""
        rows = self.db.query_all("SELECT * FROM fraud_rules ORDER BY threshold ASC;")
        return [
            FraudRule(
                id=r["id"],
                name=r["name"],
                rule_type=r["rule_type"],
                threshold=r["threshold"],
                action=r["action"],
                is_active=bool(r["is_active"]),
                description=r["description"] or ""
            ) for r in rows
        ]

    def create_rule(self, name: str, rule_type: str, threshold: float, action: str, description: str = "") -> FraudRule:
        """Creates a custom fraud detection rule."""
        rule_id = f"rule_{uuid.uuid4().hex[:8]}"
        self.db.execute(
            """
            INSERT INTO fraud_rules (id, name, rule_type, threshold, action, is_active, description)
            VALUES (?, ?, ?, ?, ?, 1, ?);
            """,
            (rule_id, name, rule_type, threshold, action, description)
        )
        return FraudRule(rule_id, name, rule_type, threshold, action, True, description)

    def toggle_rule(self, rule_id: str, is_active: bool) -> None:
        """Enables or disables a fraud rule."""
        self.db.execute(
            "UPDATE fraud_rules SET is_active = ? WHERE id = ?;",
            (1 if is_active else 0, rule_id)
        )
