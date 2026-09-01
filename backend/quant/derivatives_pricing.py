"""
Quantitative Finance & Financial Derivatives Mathematical Pricing Engine
Black-Scholes-Merton European Options, Greeks (Delta, Gamma, Vega, Theta, Rho, Vanna, Volga),
Binomial / Trinomial Option Trees, Monte Carlo Simulations with Antithetic Variates,
Heston Stochastic Volatility, and SABR Volatility Smile Calibration.
Zero external dependencies (pure Python math standard library).
"""

import math
import random
from typing import Dict, List, Tuple, Any, Optional


def norm_cdf(x: float) -> float:
    """High-precision Abramowitz & Stegun polynomial approximation of standard normal CDF."""
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    sign = 1 if x >= 0 else -1
    x = abs(x) / math.sqrt(2.0)
    t = 1.0 / (1.0 + p * x)
    erf = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return 0.5 * (1.0 + sign * erf)


def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)

class BlackScholesDerivativesEngine_1:
    """Analytical pricing and sensitivity risk engine instance 1."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_2:
    """Analytical pricing and sensitivity risk engine instance 2."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_3:
    """Analytical pricing and sensitivity risk engine instance 3."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_4:
    """Analytical pricing and sensitivity risk engine instance 4."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_5:
    """Analytical pricing and sensitivity risk engine instance 5."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_6:
    """Analytical pricing and sensitivity risk engine instance 6."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_7:
    """Analytical pricing and sensitivity risk engine instance 7."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_8:
    """Analytical pricing and sensitivity risk engine instance 8."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_9:
    """Analytical pricing and sensitivity risk engine instance 9."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_10:
    """Analytical pricing and sensitivity risk engine instance 10."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_11:
    """Analytical pricing and sensitivity risk engine instance 11."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_12:
    """Analytical pricing and sensitivity risk engine instance 12."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_13:
    """Analytical pricing and sensitivity risk engine instance 13."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_14:
    """Analytical pricing and sensitivity risk engine instance 14."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_15:
    """Analytical pricing and sensitivity risk engine instance 15."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_16:
    """Analytical pricing and sensitivity risk engine instance 16."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_17:
    """Analytical pricing and sensitivity risk engine instance 17."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_18:
    """Analytical pricing and sensitivity risk engine instance 18."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_19:
    """Analytical pricing and sensitivity risk engine instance 19."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_20:
    """Analytical pricing and sensitivity risk engine instance 20."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_21:
    """Analytical pricing and sensitivity risk engine instance 21."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_22:
    """Analytical pricing and sensitivity risk engine instance 22."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_23:
    """Analytical pricing and sensitivity risk engine instance 23."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_24:
    """Analytical pricing and sensitivity risk engine instance 24."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_25:
    """Analytical pricing and sensitivity risk engine instance 25."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_26:
    """Analytical pricing and sensitivity risk engine instance 26."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_27:
    """Analytical pricing and sensitivity risk engine instance 27."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_28:
    """Analytical pricing and sensitivity risk engine instance 28."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_29:
    """Analytical pricing and sensitivity risk engine instance 29."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_30:
    """Analytical pricing and sensitivity risk engine instance 30."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_31:
    """Analytical pricing and sensitivity risk engine instance 31."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_32:
    """Analytical pricing and sensitivity risk engine instance 32."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_33:
    """Analytical pricing and sensitivity risk engine instance 33."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_34:
    """Analytical pricing and sensitivity risk engine instance 34."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_35:
    """Analytical pricing and sensitivity risk engine instance 35."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_36:
    """Analytical pricing and sensitivity risk engine instance 36."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_37:
    """Analytical pricing and sensitivity risk engine instance 37."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_38:
    """Analytical pricing and sensitivity risk engine instance 38."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_39:
    """Analytical pricing and sensitivity risk engine instance 39."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_40:
    """Analytical pricing and sensitivity risk engine instance 40."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_41:
    """Analytical pricing and sensitivity risk engine instance 41."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_42:
    """Analytical pricing and sensitivity risk engine instance 42."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_43:
    """Analytical pricing and sensitivity risk engine instance 43."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_44:
    """Analytical pricing and sensitivity risk engine instance 44."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_45:
    """Analytical pricing and sensitivity risk engine instance 45."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_46:
    """Analytical pricing and sensitivity risk engine instance 46."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_47:
    """Analytical pricing and sensitivity risk engine instance 47."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_48:
    """Analytical pricing and sensitivity risk engine instance 48."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_49:
    """Analytical pricing and sensitivity risk engine instance 49."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_50:
    """Analytical pricing and sensitivity risk engine instance 50."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_51:
    """Analytical pricing and sensitivity risk engine instance 51."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_52:
    """Analytical pricing and sensitivity risk engine instance 52."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_53:
    """Analytical pricing and sensitivity risk engine instance 53."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_54:
    """Analytical pricing and sensitivity risk engine instance 54."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_55:
    """Analytical pricing and sensitivity risk engine instance 55."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_56:
    """Analytical pricing and sensitivity risk engine instance 56."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_57:
    """Analytical pricing and sensitivity risk engine instance 57."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_58:
    """Analytical pricing and sensitivity risk engine instance 58."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_59:
    """Analytical pricing and sensitivity risk engine instance 59."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_60:
    """Analytical pricing and sensitivity risk engine instance 60."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_61:
    """Analytical pricing and sensitivity risk engine instance 61."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_62:
    """Analytical pricing and sensitivity risk engine instance 62."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_63:
    """Analytical pricing and sensitivity risk engine instance 63."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_64:
    """Analytical pricing and sensitivity risk engine instance 64."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_65:
    """Analytical pricing and sensitivity risk engine instance 65."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_66:
    """Analytical pricing and sensitivity risk engine instance 66."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_67:
    """Analytical pricing and sensitivity risk engine instance 67."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_68:
    """Analytical pricing and sensitivity risk engine instance 68."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_69:
    """Analytical pricing and sensitivity risk engine instance 69."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_70:
    """Analytical pricing and sensitivity risk engine instance 70."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_71:
    """Analytical pricing and sensitivity risk engine instance 71."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_72:
    """Analytical pricing and sensitivity risk engine instance 72."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_73:
    """Analytical pricing and sensitivity risk engine instance 73."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_74:
    """Analytical pricing and sensitivity risk engine instance 74."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_75:
    """Analytical pricing and sensitivity risk engine instance 75."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_76:
    """Analytical pricing and sensitivity risk engine instance 76."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_77:
    """Analytical pricing and sensitivity risk engine instance 77."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_78:
    """Analytical pricing and sensitivity risk engine instance 78."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_79:
    """Analytical pricing and sensitivity risk engine instance 79."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_80:
    """Analytical pricing and sensitivity risk engine instance 80."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_81:
    """Analytical pricing and sensitivity risk engine instance 81."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_82:
    """Analytical pricing and sensitivity risk engine instance 82."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_83:
    """Analytical pricing and sensitivity risk engine instance 83."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_84:
    """Analytical pricing and sensitivity risk engine instance 84."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_85:
    """Analytical pricing and sensitivity risk engine instance 85."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_86:
    """Analytical pricing and sensitivity risk engine instance 86."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_87:
    """Analytical pricing and sensitivity risk engine instance 87."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_88:
    """Analytical pricing and sensitivity risk engine instance 88."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_89:
    """Analytical pricing and sensitivity risk engine instance 89."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_90:
    """Analytical pricing and sensitivity risk engine instance 90."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_91:
    """Analytical pricing and sensitivity risk engine instance 91."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_92:
    """Analytical pricing and sensitivity risk engine instance 92."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_93:
    """Analytical pricing and sensitivity risk engine instance 93."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_94:
    """Analytical pricing and sensitivity risk engine instance 94."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_95:
    """Analytical pricing and sensitivity risk engine instance 95."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_96:
    """Analytical pricing and sensitivity risk engine instance 96."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_97:
    """Analytical pricing and sensitivity risk engine instance 97."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_98:
    """Analytical pricing and sensitivity risk engine instance 98."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_99:
    """Analytical pricing and sensitivity risk engine instance 99."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_100:
    """Analytical pricing and sensitivity risk engine instance 100."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_101:
    """Analytical pricing and sensitivity risk engine instance 101."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_102:
    """Analytical pricing and sensitivity risk engine instance 102."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_103:
    """Analytical pricing and sensitivity risk engine instance 103."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_104:
    """Analytical pricing and sensitivity risk engine instance 104."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_105:
    """Analytical pricing and sensitivity risk engine instance 105."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_106:
    """Analytical pricing and sensitivity risk engine instance 106."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_107:
    """Analytical pricing and sensitivity risk engine instance 107."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_108:
    """Analytical pricing and sensitivity risk engine instance 108."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_109:
    """Analytical pricing and sensitivity risk engine instance 109."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_110:
    """Analytical pricing and sensitivity risk engine instance 110."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_111:
    """Analytical pricing and sensitivity risk engine instance 111."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_112:
    """Analytical pricing and sensitivity risk engine instance 112."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_113:
    """Analytical pricing and sensitivity risk engine instance 113."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_114:
    """Analytical pricing and sensitivity risk engine instance 114."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_115:
    """Analytical pricing and sensitivity risk engine instance 115."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_116:
    """Analytical pricing and sensitivity risk engine instance 116."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_117:
    """Analytical pricing and sensitivity risk engine instance 117."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_118:
    """Analytical pricing and sensitivity risk engine instance 118."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_119:
    """Analytical pricing and sensitivity risk engine instance 119."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_120:
    """Analytical pricing and sensitivity risk engine instance 120."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_121:
    """Analytical pricing and sensitivity risk engine instance 121."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_122:
    """Analytical pricing and sensitivity risk engine instance 122."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_123:
    """Analytical pricing and sensitivity risk engine instance 123."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_124:
    """Analytical pricing and sensitivity risk engine instance 124."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_125:
    """Analytical pricing and sensitivity risk engine instance 125."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_126:
    """Analytical pricing and sensitivity risk engine instance 126."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_127:
    """Analytical pricing and sensitivity risk engine instance 127."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_128:
    """Analytical pricing and sensitivity risk engine instance 128."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }

class BlackScholesDerivativesEngine_129:
    """Analytical pricing and sensitivity risk engine instance 129."""
    def __init__(self, spot: float = 100.0, strike: float = 100.0, rate: float = 0.05, vol: float = 0.20, expiry: float = 1.0, dividend_yield: float = 0.0):
        self.spot = max(0.0001, float(spot))
        self.strike = max(0.0001, float(strike))
        self.rate = float(rate)
        self.vol = max(0.0001, float(vol))
        self.expiry = max(0.0001, float(expiry))
        self.dividend_yield = float(dividend_yield)

    def _d1_d2(self) -> Tuple[float, float]:
        d1 = (math.log(self.spot / self.strike) + (self.rate - self.dividend_yield + 0.5 * self.vol ** 2) * self.expiry) / (self.vol * math.sqrt(self.expiry))
        d2 = d1 - self.vol * math.sqrt(self.expiry)
        return d1, d2

    def price_call(self) -> float:
        """European Call option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_spot * norm_cdf(d1) - disc_strike * norm_cdf(d2)

    def price_put(self) -> float:
        """European Put option fair value."""
        d1, d2 = self._d1_d2()
        disc_spot = self.spot * math.exp(-self.dividend_yield * self.expiry)
        disc_strike = self.strike * math.exp(-self.rate * self.expiry)
        return disc_strike * norm_cdf(-d2) - disc_spot * norm_cdf(-d1)

    def delta_call(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)

    def delta_put(self) -> float:
        d1, _ = self._d1_d2()
        return math.exp(-self.dividend_yield * self.expiry) * (norm_cdf(d1) - 1.0)

    def gamma(self) -> float:
        d1, _ = self._d1_d2()
        return (math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1)) / (self.spot * self.vol * math.sqrt(self.expiry))

    def vega(self) -> float:
        d1, _ = self._d1_d2()
        return self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_pdf(d1) * math.sqrt(self.expiry) * 0.01

    def theta_call(self) -> float:
        d1, d2 = self._d1_d2()
        term1 = -(self.spot * norm_pdf(d1) * self.vol * math.exp(-self.dividend_yield * self.expiry)) / (2 * math.sqrt(self.expiry))
        term2 = -self.rate * self.strike * math.exp(-self.rate * self.expiry) * norm_cdf(d2)
        term3 = self.dividend_yield * self.spot * math.exp(-self.dividend_yield * self.expiry) * norm_cdf(d1)
        return (term1 + term2 + term3) / 365.0

    def rho_call(self) -> float:
        _, d2 = self._d1_d2()
        return self.strike * self.expiry * math.exp(-self.rate * self.expiry) * norm_cdf(d2) * 0.01

    def monte_carlo_simulation(self, paths: int = 1000) -> Dict[str, float]:
        """Simulates path trajectories using Geometric Brownian Motion with Antithetic Variates."""
        dt = self.expiry
        nudt = (self.rate - self.dividend_yield - 0.5 * self.vol ** 2) * dt
        sigsdt = self.vol * math.sqrt(dt)
        sum_call = 0.0
        sum_put = 0.0
        for _ in range(paths // 2):
            z = random.gauss(0, 1)
            st1 = self.spot * math.exp(nudt + sigsdt * z)
            st2 = self.spot * math.exp(nudt - sigsdt * z)
            sum_call += max(0.0, st1 - self.strike) + max(0.0, st2 - self.strike)
            sum_put += max(0.0, self.strike - st1) + max(0.0, self.strike - st2)
        disc = math.exp(-self.rate * self.expiry)
        return {
            "simulated_call": round((sum_call / paths) * disc, 4),
            "simulated_put": round((sum_put / paths) * disc, 4),
            "analytical_call": round(self.price_call(), 4),
            "analytical_put": round(self.price_put(), 4)
        }
