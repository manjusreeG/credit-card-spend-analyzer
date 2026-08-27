

from dataclasses import dataclass
from typing import Iterable

from sqlalchemy.orm import Session

import pandas as pd

from app.core.merchant_rules import MERCHANT_RULES
from app.core.categories import DEFAULT_CATEGORY
from app.repositories.merchant_mapping_repository import find_mapping


@dataclass
class CategorizationResult:
    merchant: str | None
    category: str
    is_categorized: bool
    matched_rule: str | None = None
    mapping_source: str | None = None


class TransactionCategorizer:
    """
    Assigns a merchant and category to a normalized transaction description.

    Categorization priority:
    1. User-saved merchant/category mappings
    2. Predefined merchant rules
    3. Uncategorized fallback
    """

    def __init__(
        self,
        merchant_rules: Iterable[dict] | None = None,
    ) -> None:
        self.merchant_rules = list(merchant_rules or MERCHANT_RULES)

    def categorize(
        self,
        normalized_description: str,
        db: Session,
    ) -> CategorizationResult:
        description = normalized_description.upper().strip()

        # 1. User-saved database mapping
        saved_mapping = find_mapping(
            db,
            description,
        )

        if saved_mapping:
            return CategorizationResult(
                merchant=saved_mapping.merchant,
                category=saved_mapping.category,
                is_categorized=True,
                matched_rule=saved_mapping.match_text,
                mapping_source="user",
            )
            
        rule_result = self._match_merchant_rule(description)

        if rule_result:
            return rule_result
        
        return CategorizationResult(
            merchant=None,
            category=DEFAULT_CATEGORY,
            is_categorized=False,
            mapping_source=None,
        )
    
    def _match_merchant_rule(
        self,
        description: str
    ) -> CategorizationResult | None:
        """
        Match predefined application-level merchant rules.

        Expected merchant rule structure:

        {
            "keywords": ["AMAZON PAY", "AMAZON SELLER"],
            "merchant": "Amazon",
            "category": "Shopping"
        }
        """

        for rule in self.merchant_rules:
            match_text = rule.get("match_text", [])

            for keyword in match_text:
                normalize_keyword = keyword.upper().strip()

                if normalize_keyword in description:
                    return CategorizationResult(
                        merchant=rule["merchant"],
                        category=rule["category"],
                        is_categorized=True,
                        matched_rule=normalize_keyword,
                        mapping_source="rule",
                    )
        return None

    def categorize_transactions(
        self,
        df: pd.DataFrame,
        db: Session,
    ) -> pd.DataFrame:
        """
        Categorize all transactions in a normalized DataFrame.

        The DataFrame must contain a 'normalized_description' column.
        """

        if "normalized_description" not in df.columns:
            raise ValueError(
                "The DataFrame must contain a "
                "'normalized_description' column."
            )

        categorized_df = df.copy()

        results = categorized_df["normalized_description"].apply(
            lambda description: self.categorize(
                normalized_description=str(description),
                db=db,
            )
        )

        categorized_df["merchant"] = results.apply(
            lambda result: result.merchant
        )
        categorized_df["category"] = results.apply(
            lambda result: result.category
        )
        categorized_df["is_categorized"] = results.apply(
            lambda result: result.is_categorized
        )
        categorized_df["matched_rule"] = results.apply(
            lambda result: result.matched_rule
        )
        categorized_df["mapping_source"] = results.apply(
            lambda result: result.mapping_source
        )

        return categorized_df