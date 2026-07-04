import type { SpendingCategory } from "./categories";
import { CATEGORY_RULES } from "./category-rules";

export type ClassificationResult = {
  category: SpendingCategory;
  confidence: number;
  matchedKeyword?: string;
};

export function classifyTransaction(description: string): ClassificationResult {
  const normalizedDescription = description.toLowerCase();

  for (const rule of CATEGORY_RULES) {
    const matchedKeyword = rule.keywords.find((keyword) =>
      normalizedDescription.includes(keyword.toLowerCase())
    );

    if (matchedKeyword) {
      return {
        category: rule.category,
        confidence: 0.9,
        matchedKeyword,
      };
    }
  }

  return {
    category: "Uncategorized",
    confidence: 0,
  };
}