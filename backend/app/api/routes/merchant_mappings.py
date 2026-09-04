from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.merchant_mapping_repository import (
    create_mapping,
    delete_mapping,
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


@router.delete(
    "/{mapping.id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def remove_merchant_mapping(
    mapping_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_mapping(
        db=db,
        mapping_id=mapping_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant Mapping not found",
        )