import type { SpendingCategory } from "./categories";

export type CategoryRule = {
  category: SpendingCategory;
  keywords: string[];
};

export const CATEGORY_RULES: CategoryRule[] = [
  {
    category: "Groceries",
    keywords: ["lidl", "carrefour", "auchan", "aldi", "biedronka", "zabka"],
  },
  {
    category: "Dining",
    keywords: ["restaurant", "mcdonald", "kfc", "burger", "ubereats", "deliveroo"],
  },
  {
    category: "Transport",
    keywords: ["uber", "bolt", "ztm", "metro", "sncf", "ratp", "shell", "orlen"],
  },
  {
    category: "Shopping",
    keywords: ["amazon", "zara", "hm", "temu", "allegro"],
  },
  {
    category: "Subscriptions",
    keywords: ["netflix", "spotify", "apple", "google", "openai"],
  },
  {
    category: "Health",
    keywords: ["pharmacy", "pharmacie", "apteka", "doctolib"],
  },
  {
    category: "Travel",
    keywords: ["booking", "airbnb", "hotel", "ryanair", "wizz", "airlines"],
  },
];