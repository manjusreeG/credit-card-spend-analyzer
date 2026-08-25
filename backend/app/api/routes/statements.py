from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)
import pandas as pd

from app.services.statement_parser import (
    StatementParserError,
    parse_statement,
)
from app.services.transaction_categorizer import (
    TransactionCategorizer,
)
from app.services.transaction_normaliser import (
    normalize_transactions
)
from app.schemas.statement import StatementUploadResponse

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.merchant_mapping_repository import (
    get_all_mappings,
)

router = APIRouter(
    prefix="/statements",
    tags=["Statements"],
)

categorizer = TransactionCategorizer()



@router.post(
    "/upload",
    response_model=StatementUploadResponse,
)

def statement_upload(
    file : UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    try:
        df_final, header_row_index = parse_statement(
            file=file,
            filename=file.filename,
        )
      
        print("After parsing:", df_final.columns.tolist())

        df_final = normalize_transactions(df_final)

        print("After normalization:", df_final.columns.tolist())

        saved_mapping_records = get_all_mappings(db)
        saved_mappings = [
            {
                "match_text": mapping.match_text,
                "merchant": mapping.merchant,
                "category": mapping.category,
            }
            for mapping in saved_mapping_records
        ]

        df_final = categorizer.categorize_transactions(
            df=df_final,
            saved_mappings=saved_mappings,
        )
  
    except StatementParserError as exc:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(exc),
        ) from exc
    
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
    
    print(df_final)

    response_df = df_final.copy()

    response_df["transaction_date"] = (
        response_df["transaction_date"]
        .dt.strftime("%Y-%m-%d")
    )

    raw_transactions = response_df.to_dict(
        orient="records"
    )

    transactions = [
        {
            key: None if pd.isna(value) else value
            for key, value in transaction.items()
        }
        for transaction in raw_transactions
    ]

    return {
    "filename": file.filename,
    "message": "Statement uploaded successfully",
    "content_type": file.content_type,
    "header_row": header_row_index + 1,
    "rows": len(df_final),
    "columns": len(df_final.columns),
    "column_names": df_final.columns.tolist(),
    "preview": transactions[:5],
    "transactions": transactions,
}