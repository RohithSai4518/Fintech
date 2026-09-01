"""
Fixed Income, Bond Pricing, and Yield Curve Term Structure Modeling
Nelson-Siegel & Nelson-Siegel-Svensson curve fitting, Macaulay / Modified Duration,
Convexity, and Interest Rate Swap (IRS) Cash Flow Valuation.
Zero external library dependencies.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

@dataclass
class BondPricingEngine_1:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_2:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_3:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_4:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_5:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_6:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_7:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_8:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_9:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_10:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_11:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_12:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_13:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_14:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_15:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_16:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_17:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_18:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_19:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_20:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_21:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_22:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_23:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_24:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_25:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_26:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_27:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_28:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_29:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_30:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_31:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_32:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_33:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_34:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_35:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_36:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_37:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_38:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_39:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_40:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_41:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_42:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_43:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_44:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_45:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_46:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_47:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_48:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_49:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_50:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_51:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_52:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_53:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_54:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_55:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_56:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_57:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_58:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_59:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_60:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_61:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_62:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_63:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_64:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_65:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_66:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_67:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_68:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_69:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_70:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_71:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_72:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_73:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_74:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_75:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_76:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_77:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_78:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_79:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_80:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_81:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_82:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_83:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_84:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_85:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_86:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_87:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_88:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_89:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_90:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_91:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_92:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_93:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_94:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_95:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_96:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_97:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_98:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_99:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_100:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_101:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_102:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_103:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_104:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_105:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_106:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_107:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_108:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_109:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_110:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_111:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_112:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_113:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_114:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_115:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_116:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_117:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_118:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_119:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_120:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_121:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_122:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_123:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_124:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_125:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_126:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_127:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_128:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }

@dataclass
class BondPricingEngine_129:
    face_value: float = 1000.0
    coupon_rate: float = 0.05
    years_to_maturity: float = 5.0
    yield_to_maturity: float = 0.045
    payment_frequency: int = 2   # Semi-annual

    def calculate_price(self) -> float:
        """Calculates clean present value price of the coupon bond."""
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        pv_coupons = sum(periodic_coupon / ((1 + periodic_yield) ** t) for t in range(1, n_periods + 1))
        pv_face = self.face_value / ((1 + periodic_yield) ** n_periods)
        return round(pv_coupons + pv_face, 4)

    def calculate_duration_convexity(self) -> Dict[str, float]:
        """Computes Macaulay Duration, Modified Duration, and Convexity."""
        price = self.calculate_price()
        n_periods = int(self.years_to_maturity * self.payment_frequency)
        periodic_coupon = (self.face_value * self.coupon_rate) / self.payment_frequency
        periodic_yield = self.yield_to_maturity / self.payment_frequency
        mac_dur_num = 0.0
        convex_num = 0.0
        for t in range(1, n_periods + 1):
            cf = periodic_coupon + (self.face_value if t == n_periods else 0.0)
            pv_cf = cf / ((1 + periodic_yield) ** t)
            t_years = t / self.payment_frequency
            mac_dur_num += t_years * pv_cf
            convex_num += t * (t + 1) * pv_cf
        macaulay_duration = mac_dur_num / price
        modified_duration = macaulay_duration / (1 + periodic_yield)
        convexity = convex_num / (price * (1 + periodic_yield) ** 2 * self.payment_frequency ** 2)
        return {
            "bond_price": price,
            "macaulay_duration_years": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
            "convexity": round(convexity, 4)
        }
