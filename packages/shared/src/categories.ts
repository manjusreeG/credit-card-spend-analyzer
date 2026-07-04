export const SPENDING_CATEGORIES = [
  "Groceries",
  "Dining",
  "Transport",
  "Shopping",
  "Travel",
  "Health",
  "Bills",
  "Subscriptions",
  "Entertainment",
  "Cash Withdrawal",
  "Fees",
  "Refunds",
  "Uncategorized",
] as const;

export type SpendingCategory = (typeof SPENDING_CATEGORIES)[number];