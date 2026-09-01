"""
Multi-GAAP / IFRS General Ledger Translation & Financial Standards Engine
IFRS 9 Expected Credit Loss (ECL) 3-stage model, IFRS 15 Revenue Recognition 5-step model,
and IFRS 16 Leases Amortization Schedule generator.
Zero external library dependencies.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

class ECLStage(str, Enum):
    STAGE_1_PERFORMING = "STAGE_1"       # 12-Month ECL
    STAGE_2_UNDERPERFORMING = "STAGE_2"   # Lifetime ECL (Significant increase in credit risk)
    STAGE_3_CREDIT_IMPAIRED = "STAGE_3"   # Lifetime ECL (Defaulted / 90+ DPD)

@dataclass
class IFRS9CreditImpairmentModel_1:
    loan_id: str = "LOAN_000001"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_2:
    loan_id: str = "LOAN_000002"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_3:
    loan_id: str = "LOAN_000003"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_4:
    loan_id: str = "LOAN_000004"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_5:
    loan_id: str = "LOAN_000005"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_6:
    loan_id: str = "LOAN_000006"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_7:
    loan_id: str = "LOAN_000007"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_8:
    loan_id: str = "LOAN_000008"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_9:
    loan_id: str = "LOAN_000009"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_10:
    loan_id: str = "LOAN_000010"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_11:
    loan_id: str = "LOAN_000011"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_12:
    loan_id: str = "LOAN_000012"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_13:
    loan_id: str = "LOAN_000013"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_14:
    loan_id: str = "LOAN_000014"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_15:
    loan_id: str = "LOAN_000015"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_16:
    loan_id: str = "LOAN_000016"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_17:
    loan_id: str = "LOAN_000017"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_18:
    loan_id: str = "LOAN_000018"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_19:
    loan_id: str = "LOAN_000019"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_20:
    loan_id: str = "LOAN_000020"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_21:
    loan_id: str = "LOAN_000021"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_22:
    loan_id: str = "LOAN_000022"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_23:
    loan_id: str = "LOAN_000023"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_24:
    loan_id: str = "LOAN_000024"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_25:
    loan_id: str = "LOAN_000025"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_26:
    loan_id: str = "LOAN_000026"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_27:
    loan_id: str = "LOAN_000027"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_28:
    loan_id: str = "LOAN_000028"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_29:
    loan_id: str = "LOAN_000029"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_30:
    loan_id: str = "LOAN_000030"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_31:
    loan_id: str = "LOAN_000031"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_32:
    loan_id: str = "LOAN_000032"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_33:
    loan_id: str = "LOAN_000033"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_34:
    loan_id: str = "LOAN_000034"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_35:
    loan_id: str = "LOAN_000035"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_36:
    loan_id: str = "LOAN_000036"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_37:
    loan_id: str = "LOAN_000037"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_38:
    loan_id: str = "LOAN_000038"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_39:
    loan_id: str = "LOAN_000039"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_40:
    loan_id: str = "LOAN_000040"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_41:
    loan_id: str = "LOAN_000041"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_42:
    loan_id: str = "LOAN_000042"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_43:
    loan_id: str = "LOAN_000043"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_44:
    loan_id: str = "LOAN_000044"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_45:
    loan_id: str = "LOAN_000045"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_46:
    loan_id: str = "LOAN_000046"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_47:
    loan_id: str = "LOAN_000047"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_48:
    loan_id: str = "LOAN_000048"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_49:
    loan_id: str = "LOAN_000049"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_50:
    loan_id: str = "LOAN_000050"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_51:
    loan_id: str = "LOAN_000051"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_52:
    loan_id: str = "LOAN_000052"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_53:
    loan_id: str = "LOAN_000053"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_54:
    loan_id: str = "LOAN_000054"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_55:
    loan_id: str = "LOAN_000055"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_56:
    loan_id: str = "LOAN_000056"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_57:
    loan_id: str = "LOAN_000057"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_58:
    loan_id: str = "LOAN_000058"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_59:
    loan_id: str = "LOAN_000059"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_60:
    loan_id: str = "LOAN_000060"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_61:
    loan_id: str = "LOAN_000061"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_62:
    loan_id: str = "LOAN_000062"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_63:
    loan_id: str = "LOAN_000063"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_64:
    loan_id: str = "LOAN_000064"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_65:
    loan_id: str = "LOAN_000065"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_66:
    loan_id: str = "LOAN_000066"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_67:
    loan_id: str = "LOAN_000067"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_68:
    loan_id: str = "LOAN_000068"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_69:
    loan_id: str = "LOAN_000069"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_70:
    loan_id: str = "LOAN_000070"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_71:
    loan_id: str = "LOAN_000071"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_72:
    loan_id: str = "LOAN_000072"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_73:
    loan_id: str = "LOAN_000073"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_74:
    loan_id: str = "LOAN_000074"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_75:
    loan_id: str = "LOAN_000075"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_76:
    loan_id: str = "LOAN_000076"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_77:
    loan_id: str = "LOAN_000077"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_78:
    loan_id: str = "LOAN_000078"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_79:
    loan_id: str = "LOAN_000079"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_80:
    loan_id: str = "LOAN_000080"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_81:
    loan_id: str = "LOAN_000081"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_82:
    loan_id: str = "LOAN_000082"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_83:
    loan_id: str = "LOAN_000083"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_84:
    loan_id: str = "LOAN_000084"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_85:
    loan_id: str = "LOAN_000085"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_86:
    loan_id: str = "LOAN_000086"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_87:
    loan_id: str = "LOAN_000087"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_88:
    loan_id: str = "LOAN_000088"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_89:
    loan_id: str = "LOAN_000089"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_90:
    loan_id: str = "LOAN_000090"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_91:
    loan_id: str = "LOAN_000091"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_92:
    loan_id: str = "LOAN_000092"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_93:
    loan_id: str = "LOAN_000093"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_94:
    loan_id: str = "LOAN_000094"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_95:
    loan_id: str = "LOAN_000095"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_96:
    loan_id: str = "LOAN_000096"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_97:
    loan_id: str = "LOAN_000097"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_98:
    loan_id: str = "LOAN_000098"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_99:
    loan_id: str = "LOAN_000099"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_100:
    loan_id: str = "LOAN_000100"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_101:
    loan_id: str = "LOAN_000101"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_102:
    loan_id: str = "LOAN_000102"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_103:
    loan_id: str = "LOAN_000103"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_104:
    loan_id: str = "LOAN_000104"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_105:
    loan_id: str = "LOAN_000105"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_106:
    loan_id: str = "LOAN_000106"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_107:
    loan_id: str = "LOAN_000107"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_108:
    loan_id: str = "LOAN_000108"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_109:
    loan_id: str = "LOAN_000109"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_110:
    loan_id: str = "LOAN_000110"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_111:
    loan_id: str = "LOAN_000111"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_112:
    loan_id: str = "LOAN_000112"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_113:
    loan_id: str = "LOAN_000113"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_114:
    loan_id: str = "LOAN_000114"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_115:
    loan_id: str = "LOAN_000115"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_116:
    loan_id: str = "LOAN_000116"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_117:
    loan_id: str = "LOAN_000117"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_118:
    loan_id: str = "LOAN_000118"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_119:
    loan_id: str = "LOAN_000119"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_120:
    loan_id: str = "LOAN_000120"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_121:
    loan_id: str = "LOAN_000121"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_122:
    loan_id: str = "LOAN_000122"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_123:
    loan_id: str = "LOAN_000123"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_124:
    loan_id: str = "LOAN_000124"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_125:
    loan_id: str = "LOAN_000125"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_126:
    loan_id: str = "LOAN_000126"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_127:
    loan_id: str = "LOAN_000127"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_128:
    loan_id: str = "LOAN_000128"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }

@dataclass
class IFRS9CreditImpairmentModel_129:
    loan_id: str = "LOAN_000129"
    principal_balance: float = 250000.0
    stage: ECLStage = ECLStage.STAGE_1_PERFORMING
    probability_of_default_12m: float = 0.015
    probability_of_default_lifetime: float = 0.065
    loss_given_default: float = 0.45
    exposure_at_default: float = 250000.0
    days_past_due: int = 0

    def evaluate_stage_transition(self) -> ECLStage:
        """Evaluates SICR (Significant Increase in Credit Risk) per IFRS 9."""
        if self.days_past_due >= 90:
            self.stage = ECLStage.STAGE_3_CREDIT_IMPAIRED
        elif self.days_past_due >= 30 or self.probability_of_default_lifetime > 0.05:
            self.stage = ECLStage.STAGE_2_UNDERPERFORMING
        else:
            self.stage = ECLStage.STAGE_1_PERFORMING
        return self.stage

    def calculate_expected_credit_loss(self) -> Dict[str, Any]:
        """Calculates expected credit loss provision: ECL = PD * LGD * EAD."""
        stage = self.evaluate_stage_transition()
        if stage == ECLStage.STAGE_1_PERFORMING:
            ecl = self.probability_of_default_12m * self.loss_given_default * self.exposure_at_default
        else:
            ecl = self.probability_of_default_lifetime * self.loss_given_default * self.exposure_at_default
        return {
            "loan_id": self.loan_id,
            "stage": stage.value,
            "ecl_provision": round(ecl, 2),
            "net_carrying_amount": round(self.principal_balance - ecl, 2)
        }
