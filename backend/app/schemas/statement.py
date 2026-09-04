
from pydantic import BaseModel

from app.schemas.transaction import TransactionResponse


class StatementUploadResponse(BaseModel):
    filename : str 
    message : str
    content_type: str | None
    header_row : int
    rows: int
    columns: int
    column_names: list[str]
    preview: list[TransactionResponse]
    transactions : list[TransactionResponse]
