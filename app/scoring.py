from collections import defaultdict

"""
Rule 1: For each transaction where amount > 100, multiply score by 1.5
Rule 2: Track customer+merchant pairs — on the 3rd+ transaction for same customer to same merchant, add 10 to score each time
Rule 3: Track customer+merchant+hour — on the 3rd+ transaction in same hour, add 5 if hour is 12–17, subtract 5 if hour is 9–11 or 18–21
"""
def scoring_rules(base_score, transactions) -> float:
    # Fraud logic scoring 

    # Repeat Transactions
    repeat_txns = defaultdict(int)
    # Track cusomter, merchant, and hour
    customer_merchant_hour = defaultdict(int)

    for t in transactions:
        # Transaction amount
        if t["amount"] > 100:
            base_score *= 1.5


        key1 = (t["merchant_id"], t["customer_id"])

        repeat_txns[key1] += 1

        if repeat_txns[key1] >= 3:
            base_score += 10

        # Merchant and Customer in same hour 
        key2 = (t["merchant_id"], t["customer_id"], t["hour"])

        customer_merchant_hour[key2] += 1

        if customer_merchant_hour[key2] >= 3:
            if 12 <= t["hour"] <= 17:
                base_score += 5
            elif 9 <= t["hour"] <= 11 or 18 <= t["hour"] <= 21:
                base_score -= 5

        return base_score

        




def compute_tier(score) -> str:
    if score < 100:
        return "low_risk"
    elif 100 <= score < 250:
        return "medium_risk"
    else:
        return "high_risk"