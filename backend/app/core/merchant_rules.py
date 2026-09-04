MERCHANT_RULES = [
    {
        "match_text": ["AMAZON PAY", "AMAZONIN", "AMAZON.IN"],
        "merchant": "Amazon",
        "category": "Shopping",
    },
    {
        "match_text": ["SWIGGY"],
        "merchant": "Swiggy",
        "category": "Dining",
    },
    {
        "match_text": ["ZOMATO"],
        "merchant": "Zomato",
        "category": "Dining",
    },
    {
        "match_text": ["UBER"],
        "merchant": "Uber",
        "category": "Transport",
    },
    {
        "match_text": ["NETFLIX"],
        "merchant": "Netflix",
        "category": "Subscriptions",
    },
]

def find_merchant_rule(normalized_description: str)-> dict | None:
    description = normalized_description.upper().strip()

    for rule in MERCHANT_RULES:
        if rule["match_text"] in description:
            return rule

    return None