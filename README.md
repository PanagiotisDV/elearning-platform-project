# E-Learning Platform

A full-stack e-learning application built with FastAPI and React, designed for course publishing, student enrollment, lesson tracking, and quiz evaluation. The platform supports multiple user roles, including students, instructors, and admins, with role-based access control and a protected instructor dashboard.

## Overview

This project allows:

- Students to browse published courses and request enrollment
- Instructors to create and manage their own courses and lessons
- Admins to oversee system content and access
- Learners to track their progress through lessons and quizzes
- Instructors to publish courses and manage student enrollment flow

## Tech Stack

- Frontend: React + Vite + React Router + React Query
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Authentication: JWT with refresh tokens
- Styling: Tailwind CSS
- Validation: Pydantic schemas
- Database migrations: Alembic

## Project Structure

```text
E-LEARNING-PLATFORM/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── README.md
│   ├── alembic.ini
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
├── README.md
├── package.json
└── .gitignore
```

## Authentication and Roles

The application uses JWT-based authentication with the following roles:

- `student`
- `instructor`
- `admin`

Role checks are enforced in the backend and mirrored in the frontend route guards to ensure that each user sees only the relevant screens and actions.

## Backend Setup

### Prerequisites

- Python 3.12+
- PostgreSQL database
- `uv` package manager (recommended)

### Environment variables

Create a `.env` file in the `backend` folder with values like:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/e_learning
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
ENVIRONMENT=development
```

### Install dependencies

```bash
cd backend
uv venv
.venv\Scripts\activate
uv sync
```

### Run backend

```bash
cd backend
uvicorn app.main:app --reload
```

The API is then available at:

- http://localhost:8000
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Frontend Setup

### Prerequisites

- Node.js 18+
- npm

### Install dependencies

```bash
cd frontend
npm install
```

### Run frontend

```bash
cd frontend
npm run dev
```

The frontend runs by default at:

- http://localhost:5173

## Validation

The project was validated with the following checks:

```bash
cd frontend
npm run build
```

```bash
cd backend
python -m compileall app
```

These checks confirm that the app is compiling successfully and the project is in a working state.

## Main Features

### Student experience

- Browse published courses
- View course details
- Request enrollment
- Track course progress
- Complete lessons and quizzes

### Instructor experience

- Create and edit courses
- Publish/unpublish courses
- Manage lessons and quiz content
- Access only the courses they own
- Visit dedicated instructor pages for management flows

### Security and route protection

Protected routes are wrapped with role-aware guards. In addition, the course list endpoint includes a `my_courses` filter so instructors only receive the courses they own.

## API Structure

The backend exposes a REST API under `/api` with modules for:

- authentication
- courses
- lessons
- enrollments
- progress
- quizzes

## Notes

This repository is a full-stack academic e-learning platform focused on practical backend/frontend integration, user roles, protected routes, and course workflow management.

## License

This project is intended for educational and academic use.

