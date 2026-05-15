from pydantic import BaseModel
from typing import Optional


class TransactionIn(BaseModel):
    txn_id:      str
    customer_id: str
    merchant_id: str
    amount:      float
    hour:        int
    day:         int


class TransactionOut(BaseModel):
    txn_id:      str
    customer_id: str
    merchant_id: str
    amount:      float
    status:      str
    reason:      Optional[str]

    class Config:
        from_attributes = True


class MerchantOut(BaseModel):
    merchant_id: str
    base_score:  float
    score:       float
    risk:        str

    class Config:
        from_attributes = True