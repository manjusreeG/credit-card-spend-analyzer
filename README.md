# CardLens — Credit Card Spend Analyzer

CardLens is a full-stack financial analytics application that helps users upload credit card PDF statements, extract transactions, categorize expenses, and visualize spending patterns through an interactive dashboard.

The project is designed as a professional, scalable application with future support for both web and mobile clients.

## Project Goals

The main goal of CardLens is to make credit card statements easier to understand by converting raw PDF statements into structured financial insights.

Users should be able to:

* Upload credit card statement PDFs
* Extract transaction data from statements
* Automatically categorize transactions
* Review and manually update categories
* View spending summaries by category, merchant, and month
* Understand financial habits through dashboards and charts

## Why This Project

Credit card statements are often difficult to analyze manually. CardLens solves this by combining PDF processing, transaction normalization, categorization logic, and visual analytics into one application.

This project also demonstrates practical full-stack engineering skills, including:

* Frontend architecture
* API design
* File upload handling
* Data modeling
* Rule-based classification
* Dashboard development
* Monorepo structure
* Future mobile app readiness

## Tech Stack

### Web Application

* Next.js
* React
* TypeScript
* Tailwind CSS
* shadcn/ui
* Recharts

### Backend

* Next.js API routes for the initial MVP
* REST-style API design for future mobile compatibility

### Database

* PostgreSQL
* Prisma ORM

### PDF Processing

Planned parser service:

* Python
* FastAPI
* pdfplumber

### Shared Logic

The project is structured to keep business logic reusable across clients:

* Transaction types
* Category types
* Classification rules
* Validation schemas
* Utility functions

## Planned Architecture

```text
PDF Statement Upload
        ↓
Upload API
        ↓
PDF Parser Service
        ↓
Transaction Normalization
        ↓
Category Classification
        ↓
Database
        ↓
Dashboard & Insights
```

## Monorepo Structure

```text
credit-card-spend-analyzer/
  apps/
    web/              # Next.js web application
    mobile/           # Future Expo mobile application
  packages/
    shared/           # Shared types, categories, validation, classifier logic
    api-client/       # Future shared API client
  services/
    parser/           # Future Python/FastAPI PDF parser service
  docs/
    ARCHITECTURE.md   # Architecture notes
    API.md            # API documentation
  README.md
  ROADMAP.md
```

## Core Features

### Current / MVP Features

* PDF statement upload UI
* Spending dashboard layout
* Transactions page
* Default spending categories
* Rule-based transaction classification
* Manual category correction flow
* Category-wise spending summary

### Planned Features

* Real PDF transaction extraction
* PostgreSQL persistence
* Merchant-based category learning
* Dashboard charts
* Monthly spending trends
* Top merchant analysis
* CSV export
* AI fallback for uncategorized transactions
* Mobile app using Expo React Native

## Categorization Strategy

CardLens uses a layered categorization approach.

```text
User-defined merchant rule
        ↓
Saved merchant category
        ↓
Keyword-based category rule
        ↓
AI fallback
        ↓
Uncategorized
```

The first version uses rule-based classification for predictable and explainable results. Later versions will add AI-assisted categorization for transactions that cannot be classified confidently.

Example:

```ts
const categoryRules = {
  Groceries: ["lidl", "carrefour", "aldi", "biedronka"],
  Dining: ["restaurant", "mcdonald", "ubereats", "deliveroo"],
  Transport: ["uber", "bolt", "ztm", "sncf"],
  Shopping: ["amazon", "zara", "temu", "allegro"],
};
```

## Data Model

Planned core entities:

```text
User
Statement
Transaction
Category
MerchantRule
CategoryRule
```

Example transaction structure:

```ts
type Transaction = {
  id: string;
  statementId: string;
  date: string;
  description: string;
  merchant: string;
  amount: number;
  currency: string;
  category: string;
  confidence: number;
};
```

## API Design

The application is designed API-first so that both the web app and future mobile app can use the same backend.

Planned endpoints:

```text
POST   /api/statements/upload
GET    /api/statements
GET    /api/transactions
PATCH  /api/transactions/:id/category
GET    /api/dashboard/summary
GET    /api/categories
```

## Mobile App Readiness

CardLens is planned as a web-first product with future mobile support.

To make mobile development easier later:

* Business logic is kept outside the web app
* Shared types and category logic live in `packages/shared`
* Backend functionality is exposed through API routes
* UI components remain platform-specific
* Web uses shadcn/ui
* Mobile will use Expo React Native components

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/credit-card-spend-analyzer.git
cd credit-card-spend-analyzer
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

The web app will be available at:

```text
http://localhost:3000
```

## Development Workflow

This project follows a feature-branch workflow.

```bash
git checkout -b feat/pdf-upload
```

After making changes:

```bash
git add .
git commit -m "feat: implement pdf upload form"
git push -u origin feat/pdf-upload
```

Then open a pull request into `main`.

## Roadmap

The full roadmap is available in:

```text
ROADMAP.md
```

High-level phases:

* Project foundation
* Web application shell
* Rule-based categorization MVP
* Dashboard and insights
* Database integration
* PDF parser service
* AI categorization
* Mobile app support
* Production readiness

## Project Status

This project is currently in active development.

Current focus:

* Setting up the monorepo structure
* Building the web application shell
* Creating shared categorization logic
* Preparing the project for future backend and mobile support

## Future Improvements

* Authentication
* Secure file storage
* Multi-bank PDF support
* Multi-currency support
* Budget alerts
* Recurring subscription detection
* AI-powered spending insights
* Monthly financial reports
* Mobile app for iOS and Android

## Author

Built by Manjusree Gopinath as a professional full-stack portfolio project.
