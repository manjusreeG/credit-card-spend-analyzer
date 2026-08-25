
import re

import pandas as pd


def normalize_description(description: object) -> str:
    if pd.isna(description):
        return ""

    normalized = str(description).upper().strip()
    normalized = re.sub(r"[^A-Z0-9\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()

def normalize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    normalized_df = df.copy()

    normalized_df = normalized_df.rename(
        columns={
            "Date": "transaction_date",
            "Transaction Details": "description",
            "Amount" : "amount",
            "Debit/Credit": "transaction_type",
        }
    )

    required_columns = {
        "transaction_date",
        "description",
        "amount",
        "transaction_type",
    }

    missing_columns = (
        required_columns - set(normalized_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing required transaction columns: "
            f"{sorted(missing_columns)}"
        )

    normalized_df["transaction_date"] = pd.to_datetime(
        normalized_df["transaction_date"],
        format="%d %b '%y",
        errors="coerce"
    )

    normalized_df["description"] = (
        normalized_df["description"]
        .astype(str)
        .str.strip()
    )


    normalized_df["normalized_description"] = (
        normalized_df["description"]
        .apply(normalize_description)
    )

    normalized_df["amount"] = (
        normalized_df["amount"]
        .astype(str)
        .str.replace(r"[^\d,.\-]", "", regex=True)
        .str.replace(",","", regex=False)
        .str.strip()
    )

    normalized_df["amount"] = pd.to_numeric(
        normalized_df["amount"],
        errors="coerce"
    )

    return normalized_df