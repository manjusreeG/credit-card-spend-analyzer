from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.merchant_mapping_repository import (
    create_mapping,
    get_all_mappings,
)
from app.schemas.merchant_mapping import (
    MerchantMappingCreate,
    MerchantMappingResponse,
)

router = APIRouter(
    prefix = '/merchant-mappings',
    tags=["Merchant Mappings"],
)

@router.post(
    "",
    response_model=MerchantMappingResponse
)
def save_merchant_mapping(
    mapping: MerchantMappingCreate,
    db: Session = Depends(get_db),
): 
    return create_mapping(
        db=db,
        mapping=mapping,
    )


@router.get(
    "",
    response_model=list[MerchantMappingResponse],
)
def list_merchant_mappings(
    db:Session = Depends(get_db),
):
    return get_all_mappings(db)