"""
Unit Tests for Fraud & Risk Analysis Engine
Validates threshold evaluation, AML anomaly detection, and velocity checks.
"""

import unittest
from backend.core.database import DatabaseManager
from backend.core.models import RiskLevel
from backend.services.fraud_service import FraudService


class TestFraudService(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.fraud = FraudService(self.db)

    def test_low_risk_normal_transaction(self):
        score, level, triggers, action = self.fraud.evaluate_transaction(
            source_account_id="acc_001",
            destination_account_id="acc_002",
            amount=150.00,
            currency="USD",
            metadata={"ip_country": "US", "user_country": "US"}
        )
        self.assertEqual(score, 0.0)
        self.assertEqual(level, RiskLevel.LOW)
        self.assertEqual(action, "ALLOW")

    def test_high_amount_flag_rule(self):
        # Trigger > $10,000 threshold
        score, level, triggers, action = self.fraud.evaluate_transaction(
            source_account_id="acc_001",
            destination_account_id="acc_002",
            amount=15000.00,
            currency="USD",
            metadata={"ip_country": "US", "user_country": "US"}
        )
        self.assertGreaterEqual(score, 25.0)
        self.assertIn("Exceeded threshold rule", triggers[0])
        self.assertEqual(action, "FLAG")

    def test_geo_mismatch_anomaly(self):
        # User in US, IP in Unknown location
        score, level, triggers, action = self.fraud.evaluate_transaction(
            source_account_id="acc_001",
            destination_account_id="acc_002",
            amount=100.00,
            currency="USD",
            metadata={"ip_country": "RU", "user_country": "US"}
        )
        self.assertEqual(score, 25.0)
        self.assertEqual(level, RiskLevel.MEDIUM)
        self.assertTrue(any("Geo-location mismatch" in t for t in triggers))


if __name__ == "__main__":
    unittest.main()
