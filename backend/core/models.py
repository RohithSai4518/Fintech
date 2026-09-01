"""
Fintech Core Domain Models
Defines immutable data classes and validation schemas for banking, ledger, trading, and fraud entities.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any


class AccountType(str, Enum):
    ASSET = "ASSET"               # Cash, Customer Deposits, Receivables
    LIABILITY = "LIABILITY"       # Customer Balances (from bank view), Payables
    EQUITY = "EQUITY"             # Bank Capital, Retained Earnings
    REVENUE = "REVENUE"           # Processing Fees, Interest Income, FX Spread
    EXPENSE = "EXPENSE"           # Operational Costs, Chargeback Losses, Interest Expense


class AccountSubtype(str, Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    INVESTMENT = "INVESTMENT"
    ESCROW = "ESCROW"
    CLEARING = "CLEARING"
    FEE_COLLECTION = "FEE_COLLECTION"
    VAULT = "VAULT"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"
    CAD = "CAD"
    AUD = "AUD"


class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    SETTLED = "SETTLED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    FLAGGED = "FLAGGED"
    REVERSED = "REVERSED"


class EntryDirection(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class PaymentMethod(str, Enum):
    INTERNAL = "INTERNAL"
    ACH = "ACH"
    WIRE = "WIRE"
    CARD = "CARD"
    FX = "FX"


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(str, Enum):
    OPEN = "OPEN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Account:
    id: str
    account_number: str
    name: str
    account_type: AccountType
    account_subtype: AccountSubtype
    currency: Currency
    balance: float = 0.0
    available_balance: float = 0.0
    hold_balance: float = 0.0
    credit_limit: float = 0.0
    interest_rate: float = 0.0  # Annual Percentage Yield (APY)
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    owner_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class JournalEntryLine:
    account_id: str
    direction: EntryDirection
    amount: float
    currency: Currency
    memo: str = ""

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError(f"Journal entry amount must be positive, got {self.amount}")
        self.amount = round(float(self.amount), 4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "direction": self.direction.value if isinstance(self.direction, Enum) else self.direction,
            "amount": self.amount,
            "currency": self.currency.value if isinstance(self.currency, Enum) else self.currency,
            "memo": self.memo
        }


@dataclass
class JournalEntry:
    id: str
    reference_id: str
    timestamp: str
    description: str
    lines: List[JournalEntryLine]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate_balance(self) -> bool:
        """
        Enforce the Fundamental Accounting Equation:
        Sum of Debits MUST equal Sum of Credits for each currency.
        """
        currency_totals: Dict[str, Dict[str, float]] = {}

        for line in self.lines:
            curr = line.currency.value if isinstance(line.currency, Enum) else line.currency
            if curr not in currency_totals:
                currency_totals[curr] = {"DEBIT": 0.0, "CREDIT": 0.0}
            
            direction_str = line.direction.value if isinstance(line.direction, Enum) else line.direction
            currency_totals[curr][direction_str] += line.amount

        for curr, totals in currency_totals.items():
            debit_sum = round(totals["DEBIT"], 4)
            credit_sum = round(totals["CREDIT"], 4)
            if abs(debit_sum - credit_sum) > 0.0001:
                raise ValueError(
                    f"Double-entry imbalance for {curr}: Debits={debit_sum} != Credits={credit_sum}"
                )
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "reference_id": self.reference_id,
            "timestamp": self.timestamp,
            "description": self.description,
            "lines": [line.to_dict() for line in self.lines],
            "metadata": self.metadata
        }


@dataclass
class Transaction:
    id: str
    source_account_id: Optional[str]
    destination_account_id: Optional[str]
    amount: float
    fee: float
    currency: Currency
    payment_method: PaymentMethod
    status: TransactionStatus
    idempotency_key: str
    description: str
    risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    settled_at: Optional[str] = None
    failure_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_account_id": self.source_account_id,
            "destination_account_id": self.destination_account_id,
            "amount": self.amount,
            "fee": self.fee,
            "currency": self.currency.value if isinstance(self.currency, Enum) else self.currency,
            "payment_method": self.payment_method.value if isinstance(self.payment_method, Enum) else self.payment_method,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "idempotency_key": self.idempotency_key,
            "description": self.description,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value if isinstance(self.risk_level, Enum) else self.risk_level,
            "created_at": self.created_at,
            "settled_at": self.settled_at,
            "failure_reason": self.failure_reason,
            "metadata": self.metadata
        }


@dataclass
class Order:
    id: str
    account_id: str
    symbol: str               # e.g., "EUR/USD", "AAPL", "BTC/USD"
    side: OrderSide
    order_type: OrderType
    quantity: float
    filled_quantity: float
    price: Optional[float]
    average_fill_price: float
    status: OrderStatus
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "symbol": self.symbol,
            "side": self.side.value if isinstance(self.side, Enum) else self.side,
            "order_type": self.order_type.value if isinstance(self.order_type, Enum) else self.order_type,
            "quantity": self.quantity,
            "filled_quantity": self.filled_quantity,
            "price": self.price,
            "average_fill_price": self.average_fill_price,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class FraudRule:
    id: str
    name: str
    rule_type: str            # e.g. "VELOCITY", "AMOUNT_THRESHOLD", "GEO_ANOMALY", "BLACK_LIST"
    threshold: float
    action: str               # "FLAG", "BLOCK", "REVIEW"
    is_active: bool = True
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditLog:
    id: str
    entity_type: str
    entity_id: str
    action: str
    actor_id: str
    timestamp: str
    details: Dict[str, Any]
    checksum: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
