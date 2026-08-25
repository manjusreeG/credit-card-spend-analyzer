

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from app.core.merchant_rules import MERCHANT_RULES
from app.core.categories import DEFAULT_CATEGORY


@dataclass
class CategorizationResult:
    merchant: str | None
    category: str
    is_categorized: bool
    matched_rule: str | None = None


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
        saved_mappings: Iterable[dict] | None = None,
    ) -> CategorizationResult:
        description = normalized_description.upper().strip()

        saved_mapping_result = self._match_saved_mapping(
            description=description,
            saved_mappings=saved_mappings or [],
        )

        if saved_mapping_result:
            return saved_mapping_result
        
        rule_result = self._match_merchant_rule(description)

        if rule_result:
            return rule_result
        
        return CategorizationResult(
            merchant=None,
            category=DEFAULT_CATEGORY,
            is_categorized=False
        )
    
    def _match_saved_mapping(
        self,
        description: str,
        saved_mappings: Iterable[dict],
    ) -> CategorizationResult | None:
        """
        Match rules previously selected and saved by the user.

        Expected mapping structure:

        {
            "match_text": "AMAZON PAY INDIA",
            "merchant": "Amazon",
            "category": "Shopping"
        }
        """

        for mapping in saved_mappings:
            match_text = str(mapping.get("match_text", "")).upper().strip()

            if match_text and match_text in description:
                return CategorizationResult(
                    merchant=mapping["merchant"],
                    category=mapping["category"],
                    is_categorized=True,
                    matched_rule=match_text,
                )
            
        return None
        
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
            keywords = rule.get("keywords", [])

            for keyword in keywords:
                normalize_keyword = keyword.upper().strip()

                if normalize_keyword in description:
                    return CategorizationResult(
                        merchant=rule["merchant"],
                        category=rule["category"],
                        is_categorized=True,
                        matched_rule=normalize_keyword,
                    )
        return None

    def categorize_transactions(
        self,
        df: pd.DataFrame,
        saved_mappings: Iterable[dict] | None = None,
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
                saved_mappings=saved_mappings,
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

        return categorized_df