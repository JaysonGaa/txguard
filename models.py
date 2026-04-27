from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id: Mapped[str] = mapped_column(primary_key=True)
    base_score: Mapped[float]
    score: Mapped[float]
    risk: Mapped[str]

    def __repr__(self) -> str:
        return f"<User(merchant_id={self.merchant_id}, base_score{self.base_score}, score={self.score}, risk={self.risk})"
    
class Transaction(Base):
    __tablename__ = "transactions"

    txn_id: Mapped[str] = mapped_column(primary_key=True)
    customer_id: Mapped[str]
    merchant_id: Mapped[str] = mapped_column(ForeignKey("merchants.merchant_id"))
    amount: Mapped[float]
    status: Mapped[str]
    reason: Mapped[str | None]
    date: Mapped[str]
    hour: Mapped[str]

    def __repr__(self) -> str:
        return (
            f"<Txn(txn_id={self.txn_id}, customer_id={self.customer_id}, "
            f"merchant_id={self.merchant_id}, amount={self.amount}, "
            f"status={self.status}, date={self.date}, hour={self.hour})>"
        )