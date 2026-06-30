# Roadmap

CardLens is a credit card spend analysis application that helps users upload PDF statements, extract transactions, categorize spending, and understand financial patterns through dashboards.

## Phase 1 — Project Foundation

- [x] Initialize Next.js application
- [x] Setup TypeScript, Tailwind CSS, and ESLint
- [x] Setup shadcn/ui components
- [x] Restructure project as a monorepo
- [x] Create shared package for categories and transaction logic
- [ ] Add basic landing, upload, dashboard, and transactions pages

## Phase 2 — Transaction Categorization MVP

- [x] Define transaction and category types
- [x] Add default spending categories
- [ ] Build rule-based transaction classifier
- [ ] Add mock transaction data
- [ ] Display categorized transactions in a table
- [ ] Allow users to manually update categories

## Phase 3 — Dashboard & Insights

- [ ] Show total monthly spending
- [ ] Show spending by category
- [ ] Show top merchants
- [ ] Add charts for category breakdown
- [ ] Add monthly spending trend
- [ ] Add filters by month, category, and merchant

## Phase 4 — Database Integration

- [ ] Setup PostgreSQL
- [ ] Setup Prisma ORM
- [ ] Create database models for statements, transactions, categories, and merchant rules
- [ ] Persist uploaded statement metadata
- [ ] Persist categorized transactions
- [ ] Save user-corrected merchant rules

## Phase 5 — PDF Statement Processing

- [ ] Build upload API endpoint
- [ ] Add PDF file validation
- [ ] Create Python/FastAPI parser service
- [ ] Extract transaction rows from PDF statements
- [ ] Normalize transaction dates, descriptions, amounts, and currencies
- [ ] Handle different bank statement formats

## Phase 6 — AI Enhancement

- [ ] Add AI fallback for uncategorized transactions
- [ ] Add confidence score for category predictions
- [ ] Review low-confidence transactions manually
- [ ] Improve category suggestions using user corrections

## Phase 7 — Mobile App Readiness

- [ ] Keep business logic inside shared packages
- [ ] Expose API endpoints usable by both web and mobile clients
- [ ] Create Expo mobile app
- [ ] Reuse shared transaction types and categorization logic
- [ ] Add mobile upload and dashboard screens

## Phase 8 — Production Readiness

- [ ] Add authentication
- [ ] Add secure file handling
- [ ] Add error logging
- [ ] Add loading and empty states
- [ ] Add tests for classifier logic
- [ ] Add README screenshots
- [ ] Deploy web app
- [ ] Document architecture decisions

## Future Ideas

- Multi-currency support
- Budget alerts
- Subscription detection
- CSV export
- Monthly financial reports
- Bank-specific PDF templates
- Receipt upload support