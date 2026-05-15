from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Merchant, Transaction
from app.schemas import TransactionIn, TransactionOut, MerchantOut
from app.scoring import scoring_rules, compute_tier

router = APIRouter()


@router.post("/transactions", response_model=TransactionOut)
def create_transaction(txn: TransactionIn, db: Session = Depends(get_db)):
    # Check if merchant exists, create if not
    merchant = db.query(Merchant).filter(Merchant.merchant_id == txn.merchant_id).first()
    if not merchant:
        merchant = Merchant(
            merchant_id=txn.merchant_id,
            base_score=100.0,
            score=100.0,
            risk="low_risk"
        )
        db.add(merchant)
        db.commit()
        db.refresh(merchant)

    # Save the transaction
    db_txn = Transaction(
        txn_id=txn.txn_id,
        customer_id=txn.customer_id,
        merchant_id=txn.merchant_id,
        amount=txn.amount,
        hour=txn.hour,
        day=txn.day,
        status="APPROVED",
        reason=None
    )
    db.add(db_txn)
    db.commit()

    # Get all transactions for this merchant
    all_txns = db.query(Transaction).filter(
        Transaction.merchant_id == txn.merchant_id
    ).all()

    # Convert to list of dicts for scoring
    txn_dicts = [
        {
            "customer_id": t.customer_id,
            "merchant_id": t.merchant_id,
            "amount": t.amount,
            "hour": t.hour
        }
        for t in all_txns
    ]

    # Recalculate merchant score
    new_score = scoring_rules(merchant.base_score, txn_dicts)
    merchant.score = new_score
    merchant.risk = compute_tier(new_score)
    db.commit()

    # Return the transaction
    return TransactionOut(
        txn_id=db_txn.txn_id,
        customer_id=db_txn.customer_id,
        merchant_id=db_txn.merchant_id,
        amount=db_txn.amount,
        status=db_txn.status,
        reason=db_txn.reason
    )


@router.get("/merchants/{merchant_id}", response_model=MerchantOut)
def get_merchant(merchant_id: str, db: Session = Depends(get_db)):
    merchant = db.query(Merchant).filter(Merchant.merchant_id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant


@router.get("/merchants/{merchant_id}/transactions")
def get_merchant_transactions(merchant_id: str, db: Session = Depends(get_db)):
    txns = db.query(Transaction).filter(
        Transaction.merchant_id == merchant_id
    ).all()
    return txns