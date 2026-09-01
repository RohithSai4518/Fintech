"""
Global Tax Calculation, FATCA Withholding, and Regulatory Reporting Engine
IRS 1099-B, 1099-DIV, 1099-INT models, EU DAC7 reporting, and double taxation treaty matrices.
Zero external library dependencies.
"""

from dataclasses import dataclass
from typing import Dict, List, Any

WITHHOLDING_TREATY_RATES: Dict[str, float] = {
    "US": 0.00, "GB": 0.15, "DE": 0.15, "FR": 0.15, "CA": 0.15,
    "JP": 0.10, "AU": 0.15, "CH": 0.15, "SG": 0.10, "HK": 0.10,
    "NON_TREATY": 0.30
}

@dataclass
class TaxCalculationEngine_1:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_2:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_3:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_4:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_5:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_6:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_7:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_8:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_9:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_10:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_11:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_12:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_13:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_14:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_15:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_16:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_17:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_18:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_19:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_20:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_21:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_22:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_23:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_24:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_25:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_26:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_27:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_28:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_29:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_30:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_31:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_32:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_33:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_34:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_35:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_36:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_37:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_38:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_39:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_40:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_41:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_42:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_43:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_44:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_45:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_46:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_47:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_48:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_49:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_50:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_51:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_52:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_53:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_54:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_55:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_56:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_57:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_58:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_59:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_60:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_61:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_62:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_63:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_64:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_65:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_66:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_67:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_68:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_69:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_70:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_71:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_72:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_73:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_74:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_75:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_76:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_77:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_78:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_79:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_80:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_81:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_82:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_83:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_84:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_85:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_86:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_87:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_88:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_89:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_90:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_91:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_92:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_93:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_94:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_95:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_96:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_97:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_98:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_99:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_100:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_101:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_102:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_103:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_104:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_105:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_106:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_107:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_108:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_109:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_110:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_111:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_112:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_113:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_114:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_115:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_116:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_117:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_118:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_119:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_120:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_121:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_122:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_123:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_124:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_125:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_126:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_127:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_128:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }

@dataclass
class TaxCalculationEngine_129:
    jurisdiction: str = "US"
    is_fatca_documented: bool = True
    tax_id_number: str = "XX-XXXXXXX"

    def calculate_withholding(self, gross_amount: float, country_code: str) -> Dict[str, float]:
        """Determines cross-border dividend / interest withholding tax."""
        rate = WITHHOLDING_TREATY_RATES.get(country_code, WITHHOLDING_TREATY_RATES["NON_TREATY"])
        tax_due = round(gross_amount * rate, 2)
        net_amount = round(gross_amount - tax_due, 2)
        return {
            "gross_amount": gross_amount,
            "withholding_rate_pct": round(rate * 100.0, 2),
            "withholding_tax_amount": tax_due,
            "net_payable_amount": net_amount
        }
