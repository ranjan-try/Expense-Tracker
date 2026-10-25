# Expense Tracker API

A personal finance backend where users can track transactions,
organize them by category, and set budgets.
Built to learn backend engineering with FastAPI.

## Tech Stack
- Python, FastAPI
- SQLAlchemy + SQLite
- Pydantic

## Features
- [x] User creation
- [ ] Categories
- [ ] Transactions
- [ ] Budgets & summaries
- [ ] Authentication
- [ ] Tests

## Getting Started
1. Clone the repo
2. Create and activate a virtual environment
3. `pip install -r requirements.txt`
4. Create a `.env` file (see `.env.example`)
5. Run: `fastapi dev app/main.py`
6. Open http://127.0.0.1:8000/docs

## Project Structure
app/
  main.py, database.py, models.py, schemas.py

## Roadmap
1. Finish the categories endpoints (create, list, update, delete)
2. Build transactions, which are the core of the app
3. Add budgets and monthly summaries
4. Replace the placeholder password with real authentication
5. Write tests for everything above
6. Maybe a minimal frontend at the very end, if I still feel like it