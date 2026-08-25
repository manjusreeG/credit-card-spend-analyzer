from pydantic import BaseModel, ConfigDict

class MerchantMappingCreate(BaseModel):
    match_text: str
    merchant: str
    category: str

class MerchantMappingResponse(BaseModel):
    id: int
    match_text: str
    merchant: str
    category: str

    model_config = ConfigDict(
        from_attributes=True
    )