"""
Basel III & IV Capital Adequacy, Risk-Weighted Assets (RWA), and Liquidity Framework
Standardized Credit Risk, Market Risk FRTB, Operational Risk SMA, LCR, and NSFR calculations.
Zero external library dependencies.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

class AssetClass(str, Enum):
    SOVEREIGN_AAA = "SOVEREIGN_AAA"
    SOVEREIGN_BBB = "SOVEREIGN_BBB"
    BANK_TIER1 = "BANK_TIER1"
    CORPORATE_INVESTMENT_GRADE = "CORPORATE_IG"
    CORPORATE_HIGH_YIELD = "CORPORATE_HY"
    RESIDENTIAL_MORTGAGE = "RESIDENTIAL_MORTGAGE"
    COMMERCIAL_REAL_ESTATE = "COMMERCIAL_REAL_ESTATE"
    RETAIL_REVOLVING = "RETAIL_REVOLVING"
    EQUITY_EXCHANGE_TRADED = "EQUITY_EXCHANGE_TRADED"
    EQUITY_UNLISTED = "EQUITY_UNLISTED"

RISK_WEIGHT_MAPPINGS: Dict[AssetClass, float] = {
    AssetClass.SOVEREIGN_AAA: 0.00,
    AssetClass.SOVEREIGN_BBB: 0.50,
    AssetClass.BANK_TIER1: 0.20,
    AssetClass.CORPORATE_INVESTMENT_GRADE: 0.75,
    AssetClass.CORPORATE_HIGH_YIELD: 1.50,
    AssetClass.RESIDENTIAL_MORTGAGE: 0.35,
    AssetClass.COMMERCIAL_REAL_ESTATE: 1.00,
    AssetClass.RETAIL_REVOLVING: 0.75,
    AssetClass.EQUITY_EXCHANGE_TRADED: 2.50,
    AssetClass.EQUITY_UNLISTED: 4.00,
}

@dataclass
class BaselCapitalCalculator_1:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_2:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_3:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_4:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_5:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_6:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_7:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_8:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_9:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_10:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_11:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_12:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_13:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_14:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_15:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_16:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_17:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_18:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_19:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_20:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_21:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_22:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_23:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_24:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_25:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_26:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_27:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_28:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_29:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_30:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_31:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_32:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_33:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_34:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_35:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_36:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_37:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_38:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_39:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_40:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_41:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_42:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_43:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_44:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_45:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_46:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_47:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_48:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_49:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_50:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_51:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_52:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_53:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_54:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_55:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_56:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_57:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_58:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_59:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_60:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_61:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_62:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_63:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_64:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_65:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_66:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_67:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_68:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_69:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_70:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_71:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_72:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_73:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_74:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_75:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_76:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_77:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_78:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_79:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_80:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_81:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_82:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_83:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_84:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_85:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_86:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_87:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_88:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_89:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_90:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_91:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_92:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_93:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_94:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_95:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_96:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_97:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_98:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_99:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_100:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_101:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_102:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_103:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_104:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_105:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_106:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_107:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_108:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_109:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_110:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_111:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_112:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_113:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_114:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_115:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_116:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_117:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_118:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_119:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_120:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_121:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_122:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_123:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_124:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_125:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_126:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_127:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_128:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }

@dataclass
class BaselCapitalCalculator_129:
    common_equity_tier1: float = 50000000.0
    additional_tier1: float = 10000000.0
    tier2_capital: float = 15000000.0
    exposures: List[Dict[str, Any]] = field(default_factory=list)
    operational_gross_income_yr1: float = 12000000.0
    operational_gross_income_yr2: float = 14000000.0
    operational_gross_income_yr3: float = 16000000.0

    def calculate_credit_rwa(self) -> float:
        """Computes Standardized Approach Credit Risk-Weighted Assets."""
        total_rwa = 0.0
        if not self.exposures:
            # Sample baseline portfolio
            total_rwa += 100000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.CORPORATE_INVESTMENT_GRADE]
            total_rwa += 50000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.RESIDENTIAL_MORTGAGE]
            total_rwa += 20000000.0 * RISK_WEIGHT_MAPPINGS[AssetClass.SOVEREIGN_AAA]
        else:
            for exp in self.exposures:
                nominal = float(exp.get("nominal", 0.0))
                asset_type = exp.get("asset_class", AssetClass.CORPORATE_INVESTMENT_GRADE)
                weight = RISK_WEIGHT_MAPPINGS.get(asset_type, 1.0)
                total_rwa += nominal * weight
        return round(total_rwa, 2)

    def calculate_operational_rwa_sma(self) -> float:
        """Calculates Operational Risk RWA via Standardized Measurement Approach (SMA)."""
        avg_bi = (self.operational_gross_income_yr1 + self.operational_gross_income_yr2 + self.operational_gross_income_yr3) / 3.0
        # Business Indicator Component (12% for bucket 1 <= 1B EUR)
        bic = avg_bi * 0.12
        # Operational Risk Capital * 12.5 = Operational RWA
        return round(bic * 12.5, 2)

    def calculate_capital_ratios(self) -> Dict[str, Any]:
        """Verifies Basel III minimum capital thresholds (CET1 >= 4.5%, Tier 1 >= 6.0%, Total >= 8.0%)."""
        credit_rwa = self.calculate_credit_rwa()
        op_rwa = self.calculate_operational_rwa_sma()
        total_rwa = credit_rwa + op_rwa
        total_tier1 = self.common_equity_tier1 + self.additional_tier1
        total_capital = total_tier1 + self.tier2_capital
        cet1_ratio = (self.common_equity_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        t1_ratio = (total_tier1 / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        total_capital_ratio = (total_capital / total_rwa) * 100.0 if total_rwa > 0 else 0.0
        return {
            "credit_rwa": credit_rwa,
            "operational_rwa": op_rwa,
            "total_rwa": total_rwa,
            "cet1_ratio_pct": round(cet1_ratio, 2),
            "tier1_ratio_pct": round(t1_ratio, 2),
            "total_capital_ratio_pct": round(total_capital_ratio, 2),
            "is_compliant": cet1_ratio >= 4.5 and t1_ratio >= 6.0 and total_capital_ratio >= 8.0
        }
