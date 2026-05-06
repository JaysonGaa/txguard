from app.database import engine, Base, SessionLocal
from app.models import Merchant, Transaction

# Create tables
Base.metadata.create_all(engine)

# Test data
merch_test = Merchant(
    merchant_id="Walmart",
    base_score=100.0,
    score=150.0,
    risk="Medium Risk"
)

txn_test = Transaction(
    txn_id="T1",
    customer_id="Customer1",
    merchant_id="Walmart",
    amount=500.75,
    status="APPROVED",
    reason=None, 
    date= "12/04/25",
    hour= 3,
)

# Insert and query
with SessionLocal() as session:
        
    session.query(Transaction).delete()
    session.query(Merchant).delete()
    session.commit()
    
    session.add(merch_test)
    session.add(txn_test)
    session.commit()

    merchants = session.query(Merchant).all()
    transactions = session.query(Transaction).all()

    print("MERCHANTS:", merchants)
    print("TRANSACTIONS:", transactions)