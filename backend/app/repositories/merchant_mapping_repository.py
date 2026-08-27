from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models.merchant_mapping import MerchantMapping
from app.schemas.merchant_mapping import MerchantMappingCreate


def get_all_mappings(db: Session,) ->list[MerchantMapping]:

    statement = select(MerchantMapping)

    return list(
        db.scalars(statement).all()
    )

def get_mapping_by_match_text(
    db:Session,
    match_text: str,
)  -> MerchantMapping | None:

    statement = select(MerchantMapping).where(
        MerchantMapping.match_text
        == match_text.upper().strip()
    )

    return db.scalars(statement)

def create_mapping(
    db: Session,
    mapping: MerchantMappingCreate,
) -> MerchantMapping: 

    db_mapping = MerchantMapping(
        match_text = mapping.match_text.upper().strip(),
        merchant = mapping.merchant.strip(),
        category = mapping.category.strip(),
    )

    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)

    return db_mapping

def find_mapping(
        db:Session, 
        normalized_description: str
    ) -> MerchantMapping | None:

    description = normalized_description.upper().strip()

    statement = select(MerchantMapping)
    mappings = db.scalars(statement).all()

    print("DESCRIPTION:", repr(description))

    for mapping in mappings:
        print(
            "DB MAPPING:",
            repr(mapping.match_text),
            "MATCH:",
            mapping.match_text.upper().strip() in description,
        )

    match_mappings = [
        mapping
        for mapping in mappings
        if mapping.match_text
        and mapping.match_text.upper().strip() in description
    ]

    if not match_mappings:
        return None

    

    return max(
        match_mappings,
        key=lambda mapping: len(mapping.match_text),
    )

def delete_mapping(
    db: Session,
    mapping_id: int
)-> bool:
    mapping = db.get(
        MerchantMapping,
        mapping_id,
    )

    if mapping is None:
        return False

    db.delete(mapping)
    db.commit()

    return True