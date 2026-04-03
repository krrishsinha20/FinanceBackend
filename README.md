---
title: FinanceBackend
emoji: 💰
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---
# Finance Data Processing and Access Control Backend

A backend system for managing financial records with role-based access control. Built with FastAPI and SQLite.

---

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** SQLite via SQLAlchemy ORM
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** bcrypt via passlib
- **API Docs:** Swagger UI (auto-generated)

---

## Project Structure
```
finance-backend/
│
├── main.py                  → FastAPI app entry point
├── database.py              → SQLite connection and session
├── requirements.txt         → Dependencies
├── finance.db               → Auto-generated SQLite database
│
├── models/
│   ├── user.py              → User table
│   └── record.py            → Financial Record table
│
├── schemas/
│   ├── user.py              → User request/response schemas
│   └── record.py            → Record request/response schemas
│
├── routes/
│   ├── auth.py              → /auth endpoints
│   ├── users.py             → /users endpoints
│   ├── records.py           → /records endpoints
│   └── dashboard.py         → /dashboard endpoints
│
├── services/
│   ├── auth_service.py      → Auth business logic
│   ├── user_service.py      → User business logic
│   ├── record_service.py    → Record business logic
│   └── dashboard_service.py → Summary and analytics logic
│
└── core/
    ├── dependencies.py      → JWT auth and role checker
    └── security.py          → Password hashing and JWT utils
```

---

## Deployed API

- **Base URL:** `https://your-deployed-url.com`
- **Swagger UI:** `https://your-deployed-url.com/docs`

> Replace the above links once deployed.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/finance-backend.git
cd finance-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

### 6. Open Swagger UI
```
http://localhost:8000/docs
```

> Note: The SQLite database (finance.db) is created automatically on first run. No manual database setup required.

---

## How to Test

### Step 1 — Register users
Use `POST /auth/register` to create users with different roles:
```json
{ "name": "Admin User", "email": "admin@zorvyn.com", "password": "admin123", "role": "admin" }
{ "name": "Analyst User", "email": "analyst@zorvyn.com", "password": "analyst123", "role": "analyst" }
{ "name": "Viewer User", "email": "viewer@zorvyn.com", "password": "viewer123", "role": "viewer" }
```

### Step 2 — Login
Use `POST /auth/login` or click **Authorize** on Swagger UI and enter credentials directly.

### Step 3 — Add transactions (Admin only)
Use `POST /records/` to add income and expense entries.

### Step 4 — Test role restrictions
Switch between users in Authorize and verify access control behavior.

---

## Roles and Permissions

| Feature | Viewer | Analyst | Admin |
|---------|--------|---------|-------|
| View records | Yes | Yes | Yes |
| View summary | Yes | Yes | Yes |
| View recent activity | Yes | Yes | Yes |
| View category wise breakdown | No | Yes | Yes |
| View monthly trends | No | Yes | Yes |
| Create/Edit/Delete records | No | No | Yes |
| Manage users | No | No | Yes |

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/auth/register` | Register new user | Public |
| POST | `/auth/login` | Login and get JWT token | Public |

### Users
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/users/` | Get all users | Admin |
| GET | `/users/me` | Get current user info | All |
| GET | `/users/{id}` | Get user by ID | Admin |
| PUT | `/users/{id}` | Update user role or status | Admin |
| DELETE | `/users/{id}` | Deactivate user | Admin |

### Financial Records
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/records/` | Create new transaction | Admin |
| GET | `/records/` | Get all transactions with filters | All |
| GET | `/records/{id}` | Get single transaction | All |
| PUT | `/records/{id}` | Update transaction | Admin |
| DELETE | `/records/{id}` | Soft delete transaction | Admin |

### Dashboard
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/dashboard/summary` | Total income, expense, net balance | All |
| GET | `/dashboard/category-wise` | Category wise breakdown | Analyst + Admin |
| GET | `/dashboard/monthly-trends` | Monthly income and expense trends | Analyst + Admin |
| GET | `/dashboard/recent-activity` | Last 10 transactions | All |

---

## Filtering Records

`GET /records/` supports query parameters:
```
/records/?type=income
/records/?type=expense
/records/?category=salaries
/records/?start_date=2026-01-01T00:00:00&end_date=2026-04-01T00:00:00
```

---

## Assumptions Made

- Roles are limited to three types: `viewer`, `analyst`, `admin`
- Only admins can create, update, or delete financial records
- Soft delete is used for both users and records — data is never permanently removed
- JWT tokens expire after 24 hours
- Password must be 72 characters or less (bcrypt limitation)
- SQLite is used for simplicity as this is an assessment project

---

## Tradeoffs Considered

- **SQLite over PostgreSQL** — easier setup for evaluators, no external DB server needed
- **Passlib + bcrypt** — industry standard password hashing, minor version compatibility resolved by pinning bcrypt==4.0.1
- **Soft delete** — records and users are never permanently deleted, maintains data integrity
- **JWT over sessions** — stateless authentication, better suited for API based systems

---

## Author

**Krrish Sinha**
Backend Developer Intern Assignment
Zorvyn FinTech Pvt. Ltd.