# AlgoSensei

AlgoSensei is an AI-powered coding mentor featuring Socratic tutoring, automated code review, mock technical interviews, and personalized learning analytics built with FastAPI, LangChain, and Google Gemini.

The product now reads more like an AI engineering SaaS: a mentor mode for guided problem solving, a code review mode for structured feedback, a mock interview mode for live practice, and a private dashboard for browser-local analytics.

## Product Scope

- Socratic coding mentor for problem solving and interview prep
- Code Review mode with structured feedback on quality, bugs, complexity, edge cases, and optimization
- Mock Interview mode for DSA, DBMS, OOP, OS, and System Design practice
- Learning analytics stored in localStorage with no authentication
- Multi-page frontend deployed on Vercel and backend API deployed on Render

## Backend Architecture

The backend is organized into a resume-ready FastAPI layout:

- `Backend/app/core/` for environment and configuration helpers
- `Backend/app/models/` for request and response schemas
- `Backend/app/prompts/` for mode-specific prompt templates
- `Backend/app/services/` for Gemini and LangChain execution helpers
- `Backend/app/routers/` for API endpoints grouped by feature

This keeps the application modular without changing the deployment model. Render can still start the app with `uvicorn main:app`.

## Frontend Pages

- `index.html` for the main mentor experience and feature cards
- `coach.html` for the original Socratic tutoring chat
- `code-review.html` for the new code review workflow
- `interview.html` for the mock interview workflow
- `dashboard.html` for local learning analytics and readiness scoring
- `about.html`, `features.html`, and `contact.html` for supporting product and marketing pages

Each page includes the same top-level mode switcher so users can jump between Mentor, Code Review, Mock Interview, and Dashboard without leaving the product context.

## API Endpoints

- `POST /api/start_session` starts the Socratic mentor flow
- `POST /api/chat` continues the mentor conversation
- `POST /api/code_review` returns structured code review feedback
- `POST /api/interview/start` creates the opening interview question
- `POST /api/interview/turn` evaluates an answer and asks a follow-up
- `POST /api/interview/finalize` generates the final interview score

## Local Development

### Backend

```bash
cd Backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Set `GOOGLE_API_KEY` in `Backend/python.env` for local development.

### Frontend

Serve the repository root with Live Server or any static file server, then open `index.html`.

## Deployment Notes

- Keep the frontend as a static site on Vercel
- Keep the backend on Render with the existing FastAPI start command
- Add `GOOGLE_API_KEY` as a Render environment variable
- Update the frontend backend URL only if the Render deployment URL changes
- No authentication, payments, Redis, Docker, or Kubernetes are required for this project
- Analytics stay in localStorage, so each browser profile keeps its own practice history with no database dependency.

## What Changed

- Added Code Review mode
- Added Mock Interview mode
- Added local learning analytics
- Refactored backend into routers, services, prompts, and models
- Improved homepage positioning to look more like an AI SaaS product
- Updated the supporting marketing pages and shared navigation to match the new product positioning
