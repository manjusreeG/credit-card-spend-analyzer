export type MockTransaction = {
  id: string;
  date: string;
  merchant: string;
  description: string;
  amount: number;
  currency: string;
  category: string;
};

export const mockTransactions: MockTransaction[] = [
  {
    id: "txn_001",
    date: "2026-06-01",
    merchant: "Lidl",
    description: "LIDL WARSZAWA",
    amount: 42.75,
    currency: "EUR",
    category: "Groceries",
  },
  {
    id: "txn_002",
    date: "2026-06-02",
    merchant: "Uber",
    description: "UBER TRIP",
    amount: 14.2,
    currency: "EUR",
    category: "Transport",
  },
  {
    id: "txn_003",
    date: "2026-06-04",
    merchant: "Netflix",
    description: "NETFLIX SUBSCRIPTION",
    amount: 15.99,
    currency: "EUR",
    category: "Subscriptions",
  },
  {
    id: "txn_004",
    date: "2026-06-06",
    merchant: "Zara",
    description: "ZARA ONLINE",
    amount: 89.9,
    currency: "EUR",
    category: "Shopping",
  },
  {
    id: "txn_005",
    date: "2026-06-08",
    merchant: "Ryanair",
    description: "RYANAIR FLIGHT BOOKING",
    amount: 126.4,
    currency: "EUR",
    category: "Travel",
  },
  {
    id: "txn_006",
    date: "2026-06-10",
    merchant: "McDonald's",
    description: "MCDONALDS RESTAURANT",
    amount: 11.5,
    currency: "EUR",
    category: "Dining",
  },
];