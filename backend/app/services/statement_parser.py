from pathlib import Path
from typing import BinaryIO

import pandas as pd

from app.core.constants import (
    COLUMN_ALIASES,
    ALLOWED_EXTENSIONS,
    REQUIRED_COLUMNS
)

class StatementParserError(Exception):
    """Raised when a statement cannot be parsed."""

def validate_file_extension(filename:str) -> str:
    file_extension = Path(filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        supported_extensions = {', '.join(ALLOWED_EXTENSIONS)}

        raise StatementParserError(
            f"Invalid file extension. "
            f"Only {supported_extensions} are supported."
        )
    
    return file_extension

def read_statement_file(
    file: BinaryIO,
    file_extension: str,
) -> pd.DataFrame :
    try:
        # Read without assuming where the header is.
        if file_extension in {".xlsx", ".xls"}:
            return pd.read_excel(file.file, header=None)
        
        if file_extension == ".csv":
            return pd.read_csv(file.file, header=None)
        
    except (
        ValueError, 
        TypeError, 
        pd.errors.ParserError,
    ) as exc:
        raise StatementParserError(
            "Unable to read statement file.",
            "Please check the file format."
        ) from exc
    
    raise StatementParserError("Unsupported file type. ")


def find_header_row(df: pd.DataFrame) -> int | None:
    for index, row in df.iterrows():
        row_values = {
            str(value).strip()
            for value in row.dropna().tolist()
        }

        has_date = "Date" in row_values
        has_transaction_details = (
            "Transaction Details" in row_values
        )
        if has_date and has_transaction_details:
            return index

    return None

def create_transaction_dataframe(
    raw_df: pd.DataFrame,
    header_row_index: int,
) -> pd.DataFrame:
    df = raw_df.iloc[header_row_index + 1:].copy()
    df.columns = raw_df.iloc[header_row_index].tolist()

    # Remove columns whose header is empty.
    df = df.loc[:, df.columns.notna()]

    # clean column names.
    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    # Convert bank-specific column names to CardLens names.
    df = df.rename(columns=COLUMN_ALIASES)
    
    return df

def validate_required_columns(
    df: pd.DataFrame
) -> None:
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise StatementParserError(
            "Required transaction columns were not found. "
            f"Missing : {sorted(missing_columns)}. "
            f"Detected: {df.columns.tolist()}."
        )

def remove_statement_footer(
    df: pd.DataFrame
) -> pd.DataFrame:
    # Find the statement-ending marker.
    end_row_mask = df.astype(str).apply(
        lambda column: column.str.contains( 
            r"\*\*\s* End of Statement\s*\*\*",
            case=False,
            na=False,
            regex=True,
        )
    ).any(axis=1)

    if not end_row_mask.any():
        return df
    
    end_row_position = (
        end_row_mask.to_numpy().argmax()
    )
    
    return df.iloc[:end_row_position]

def select_transaction_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    selected_columns = [
        "Date",
        "Transaction Details",
        "Amount",
    ]

    # Keep Debit/Credit when the statement provides it.
    if "Debit/Credit" in df.columns:
        selected_columns.append("Debit/Credit")

    return df[selected_columns].copy()

def parse_statement(
    file: BinaryIO,
    filename: str,
) -> tuple[pd.DataFrame, int]:
    file_extension = validate_file_extension(
        filename
    )

    raw_df = read_statement_file(
        file=file,
        file_extension=file_extension,
    )

    header_row_index = find_header_row(raw_df)

    if header_row_index is None:
        raise StatementParserError(
            "Transaction table header could not be found."
        )
    
    transaction_df = create_transaction_dataframe(
        raw_df=raw_df,
        header_row_index=header_row_index,
    )

    validate_required_columns(transaction_df)

    transaction_df = remove_statement_footer(
        transaction_df
    )

    transaction_df = select_transaction_columns(
        transaction_df
    )

    transaction_df = (
        transaction_df
        .dropna(how="all")
        .reset_index(drop=True)    
    )

    return transaction_df, header_row_index
