

from datetime import date

from pydantic import BaseModel


class TransactionResponse(BaseModel):
    transaction_date : date | None
    description: str
    amount: float | None
    transaction_type : str
    normalized_description: str
    merchant: str | None = None
    category: str
    is_categorized: bool
    matched_rule: str | None = None