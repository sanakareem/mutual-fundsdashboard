# Mutual Fund Dashboard

A full-stack web application for tracking and analyzing mutual fund investments.

## Features

- Dashboard with investment performance metrics
- Portfolio composition analysis
- Mutual fund overlap analysis
- Sector and stock allocation visualization
- Interactive charts for portfolio performance

## Tech Stack

### Frontend
- **Framework**: Next.js
- **Styling**: TailwindCSS
- **State Management**: React Query & Context API
- **Charts**: Recharts

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with Supabase
- **Authentication**: JWT Tokens

### Deployment
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: Supabase

## Project Structure

```
mutual-fund-dashboard/
├── frontend/                  # Next.js frontend
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── contexts/          # React contexts for state management
│   │   ├── hooks/             # Custom React hooks
│   │   ├── lib/               # Utility functions and API clients
│   │   ├── pages/             # Next.js pages
│   │   └── styles/            # Global styles
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── core/              # Core functionality
│   │   ├── db/                # Database models and migrations
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic
│   ├── tests/                 # Backend tests
│   └── main.py                # FastAPI entry point
└── docker-compose.yml         # Docker configuration for local development
```

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- PostgreSQL or Supabase account

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Create a `.env.local` file with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file with:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/mutual_fund_dashboard
   SECRET_KEY=your-secret-key
   ```

3. Run the