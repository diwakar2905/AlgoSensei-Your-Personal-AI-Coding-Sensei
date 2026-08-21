# Project Interview Preparation

## 1. 30-Second Explanation
AlgoSensei is a browser-based AI interview-preparation app with a FastAPI backend. It has three main modes: Socratic coding mentor, structured code review, and mock technical interview. The frontend is static HTML/JavaScript with Tailwind CSS, while the backend sends prompts to Google Gemini through LangChain and returns JSON or text responses. Analytics are stored locally in the browser using `localStorage`, not in a database.

## 2. 60-Second Explanation
AlgoSensei is designed to help users practice coding interviews more actively than a normal code generator. Instead of giving direct solutions, the mentor mode asks guided questions, the review mode analyzes pasted code for complexity, bugs, and edge cases, and the interview mode simulates a multi-round technical interview with scoring and follow-ups. The frontend is entirely static and communicates with FastAPI endpoints using `fetch`. The backend is organized into routers, schemas, prompt builders, and a Gemini service layer. There is no database, authentication system, or persistent server-side user profile; learning analytics are tracked locally in the browser.

## 3. 2-Minute Technical Explanation
The project is a split frontend-backend application. On the frontend, HTML pages such as `index.html`, `coach.html`, `code-review.html`, `interview.html`, and `dashboard.html` provide different workflows. `assets/app.js` centralizes browser-side utilities like theme switching, mobile menu logic, and `localStorage` analytics helpers.

The backend is a FastAPI app in `Backend/main.py`. It loads environment variables from `Backend/python.env`, enables CORS, and mounts three routers: mentor, code review, and interview. Each router accepts Pydantic-validated request bodies, builds a LangChain prompt, and calls Google Gemini via `ChatGoogleGenerativeAI`. Responses are either plain text or structured JSON; JSON responses are parsed defensively with fallback values if parsing fails.

The architecture is lightweight and stateless on the server side. The only persistent state is browser analytics in `localStorage`, which powers the dashboard. There is no database, authentication, or queueing layer in the repository.

## 4. Problem Statement
The project solves the problem of passive interview prep. Instead of just showing answers, it tries to train the user’s reasoning through guided questioning, code review feedback, and mock interview practice. The intended outcome is to help users build interview readiness, not just solve one problem at a time.

## 5. Features
- Socratic coding mentor
- Code review assistant
- Mock technical interview flow
- Round-based interview scoring
- Local learning analytics dashboard
- Theme toggle
- Mobile navigation
- Browser-only state passing between pages using `localStorage`

## 6. Tech Stack
- HTML5
- Tailwind CSS via CDN
- Vanilla JavaScript
- FastAPI
- Pydantic
- Uvicorn
- python-dotenv
- LangChain
- langchain-google-genai
- Google Gemini models
- Vercel frontend deployment, Render backend deployment per README

## 7. Architecture
### Verified structure
- `Backend/main.py` creates the FastAPI app
- `Backend/app/routers/` contains API endpoints
- `Backend/app/prompts/` contains prompt templates
- `Backend/app/models/` contains Pydantic schemas
- `Backend/app/services/gemini_service.py` handles Gemini calls and parsing
- `assets/app.js` handles frontend utilities and analytics

### Actual request flow
- Mentor: browser → `POST /api/start_session` or `POST /api/chat` → router → prompt template → Gemini service → Gemini model → response
- Code review: browser → `POST /api/code_review` → router → prompt template → Gemini service → JSON parse → response
- Interview: browser → `POST /api/interview/start` / `turn` / `finalize` → router → prompt template → Gemini service → JSON parse → response

## 8. Complete Data Flow
### Mentor mode
User types problem and code in `index.html`
→ click `Coach Me!`
→ data saved to `localStorage`
→ page redirects to `coach.html`
→ `coach.html` reads problem/code/language from `localStorage`
→ frontend sends request to backend mentor endpoint
→ backend prompt asks Gemini for a Socratic question
→ response rendered in chat UI.

### Code review mode
User pastes code in `code-review.html`
→ frontend sends JSON to `/api/code_review`
→ backend builds review prompt
→ Gemini returns structured analysis
→ backend parses JSON and returns response
→ frontend displays complexity, bugs, edge cases, optimization suggestions.

### Interview mode
User selects domain/difficulty in `interview.html`
→ frontend calls `/api/interview/start`
→ backend generates opening question
→ user answers
→ frontend calls `/api/interview/turn`
→ backend generates evaluation and follow-up
→ after interview ends, frontend calls `/api/interview/finalize`
→ backend returns final scorecard.

### Dashboard flow
`dashboard.html`
→ reads `localStorage`
→ computes readiness score and topic stats in browser only
→ renders analytics.

## 9. Backend Deep Dive
### Framework and routing
- FastAPI is used for the HTTP API.
- `APIRouter` separates mentor, code review, and interview features.
- The root endpoint `/` is a simple health-check style response.

### HTTP methods and endpoints
Verified endpoints:
- `GET /`
- `POST /api/start_session`
- `POST /api/chat`
- `POST /api/code_review`
- `POST /api/interview/start`
- `POST /api/interview/turn`
- `POST /api/interview/finalize`

### Validation
- Request validation is handled by Pydantic models.
- No custom validation logic beyond model structure and a few model validators for output normalization.

### Error handling
- Mentor and interview text endpoints use `try/except` around model calls and provide fallback text/JSON behavior.
- Code review uses a fallback dictionary if JSON parsing fails.
- There is no broader centralized exception handler.

### Authentication/authorization
- None implemented.
- INTERVIEWER MAY ASK: Why is there no authentication? You should answer that the app is a public/demo-style learning tool and the repository does not implement user identity or access control.

### Middleware
- CORS middleware is present.
- IMPORTANT: `allow_origins=["*"]` and `allow_credentials=False` are used in code. The README claims a specific Vercel origin is accepted, but that is not what the code currently enforces.

### Async/concurrency
- Route handlers are declared `async`, but the Gemini call path is effectively synchronous because `chain.invoke(...)` is used.
- So async syntax exists, but true non-blocking LLM I/O is not verified.
- INTERVIEWER MAY ASK: If handlers are async, why does the app still block? You should know that `invoke()` is synchronous.

### Dependency injection
- No explicit FastAPI dependency injection is used.

### Logging
- Minimal logging only: fallback loop prints model failures to stdout.
- No structured logging framework is present.

### Rate limiting / caching / pagination / versioning
- Not implemented.
- INTERVIEWER MAY ASK: How would you protect the API from abuse? Mention rate limiting, auth, quotas, and maybe caching of repeated requests as production additions.

## 10. Database Deep Dive
### Actual database status
- No database is implemented in the repository.
- No tables, schemas, migrations, ORM models, or queries exist in code.
- The README mentions “analytics” but those analytics are stored in browser `localStorage`, not in a server database.

### Relationships, PKs, FKs, constraints, indexes
- NOT DETERMINABLE FROM REPOSITORY because no database exists in the codebase.

### Important interview point
- INTERVIEWER MAY ASK: Why no database? Your answer should be that the current product intentionally keeps analytics local and server state stateless.
- If asked how to persist user history centrally, say you would add a DB and user auth layer, but that is not implemented.

## 11. API Documentation
### Verified request/response shape
#### `POST /api/start_session`
Input: `problem`, `code`, `language`, `topic`
Output: `{ "from": "ai", "text": "..." }`

#### `POST /api/chat`
Input: `history`, `problem`, `code`, `language`, `topic`
Output: `{ "from": "ai", "text": "..." }`

#### `POST /api/code_review`
Input: `code`, `language`, `focus_area`
Output fields:
- `from`
- `code_quality_analysis`
- `time_complexity`
- `space_complexity`
- `potential_bugs`
- `edge_cases`
- `optimization_suggestions`
- `interview_feedback`

#### `POST /api/interview/start`
Input: `domain`, `difficulty`
Output fields:
- `from`
- `question`
- `score`
- `round_number`

#### `POST /api/interview/turn`
Input: `domain`, `difficulty`, `latest_answer`, `history`, `round_number`
Output fields:
- `from`
- `evaluation`
- `follow_up`
- `score`
- `round_number`
- `should_end`

#### `POST /api/interview/finalize`
Input: `domain`, `difficulty`, `history`
Output fields:
- `from`
- `overall_score`
- `verdict`
- `strengths`
- `weaknesses`
- `next_steps`

### Status codes
- FastAPI default 200 on success.
- No explicit custom status codes are set.
- Validation errors will produce FastAPI’s standard 422 responses.

## 12. Security
### What is actually implemented
- `.gitignore` is present and README says the env file is untracked.
- Environment variables are loaded from `Backend/python.env` locally.
- CORS middleware exists.
- No secrets are committed in the inspected code.

### What is missing
- No authentication.
- No authorization.
- No CSRF protection.
- No rate limiting.
- No input sanitization beyond Pydantic structure.
- No secure session management.
- No server-side user identity.
- No file upload handling.

### Important correction
- README claims restricted CORS for the Vercel client, but code currently allows any origin.
- That is a meaningful mismatch you should be ready to defend honestly.

### Interviewer may ask
- Why is `allow_origins=["*"]` acceptable?
- Why no auth?
- How do you protect API keys?
- Could a user inject malicious code into prompts?
- Could stored browser content be abused?

## 13. Performance
### Actual performance-sensitive areas
- Gemini model calls are the main latency source.
- Fallback model pipeline may try multiple models sequentially.
- The dashboard computations are lightweight and browser-side.
- There is no database bottleneck because there is no database.

### Potential bottlenecks
- Blocking model invocations in `run_text_prompt`
- Multiple fallback attempts if a model fails
- No caching of repeated prompts
- No request queue or background jobs

### Not implemented
- No indexing
- No query optimization
- No batching
- No connection pooling
- No caching layer
- No async LLM client usage verified

## 14. Scalability
### Current scale characteristics
- Stateless backend architecture is easy to scale horizontally in principle.
- Browser-local analytics avoid server storage cost.
- But the system is constrained by external LLM API limits and latency.

### If traffic increases
- Add request rate limiting
- Add auth and per-user quotas
- Add server-side persistence if analytics/history must roam across devices
- Add caching for repeated prompt/result combinations if valid
- Consider queue-based processing for long-running LLM calls
- Use async-compatible downstream calls

### What happens if the database goes down?
- Not applicable because no database exists.

### What happens if external API fails?
- Mentor has fallback text.
- Code review returns fallback fields.
- Interview returns fallback JSON-like defaults.

## 15. Important Files and Functions
### `Backend/main.py`
- `app = FastAPI(...)`
- CORS middleware setup
- router registration
- `/` health endpoint

### `Backend/app/routers/mentor.py`
- `start_session`
- `chat_session`
- `_fallback_response`

### `Backend/app/routers/code_review.py`
- `code_review`

### `Backend/app/routers/interview.py`
- `interview_start`
- `interview_turn`
- `interview_finalize`

### `Backend/app/services/gemini_service.py`
- `format_history`
- `strip_markdown_fences`
- `safe_json_parse`
- `get_llm_for_model`
- `get_model_pipeline`
- `run_text_prompt`
- `run_json_prompt`

### `Backend/app/models/schemas.py`
- request/response Pydantic models
- validators that normalize list/string output

### `Backend/app/prompts/*.py`
- prompt templates

### `assets/app.js`
- `readAnalytics`
- `saveAnalytics`
- `recordQuestionSolved`
- `recordCodeReview`
- `recordInterviewCompleted`
- `calculateReadinessScore`
- `getDashboardModel`
- `initThemeToggle`
- `initMobileMenu`

## 16. Important Code Logic
1. `index.html` stores problem/code/language into `localStorage` before redirecting.
2. `coach.html` reads that state and sends it to backend endpoints.
3. `gemini_service.py` tries a primary model plus fallback Gemini models.
4. `run_json_prompt` strips code fences and parses JSON; on parse failure it returns fallback data.
5. `InterviewFinalResponse` and `CodeReviewResponse` normalize LLM output into expected shapes.
6. `dashboard.html` computes readiness purely in the browser.
7. `recordInterviewCompleted()` weights interview practice more heavily than mentor/code review.

## 17. Technology Why/Why Not
### FastAPI
- Why used: quick REST API development, Pydantic integration, clean router structure.
- Where used: backend entrypoint and all API routes.
- How it works here: request bodies are validated into models, responses are serialized from Pydantic models.
- Alternative: Flask or Django REST Framework.
- Why this choice makes sense: simple, lightweight, good for demo-style APIs.
- Potential limitation: no built-in production app structure, auth, or ORM.

### Pydantic
- Why used: schema validation and response shaping.
- Where used: `schemas.py`.
- Alternative: manual dict handling.
- Limitation: only validates structure, not full business correctness.

### LangChain + Google Gemini
- Why used: prompt orchestration and LLM integration.
- Where used: service layer and prompt templates.
- Alternative: direct Gemini API calls without LangChain.
- Limitation: added abstraction can obscure control flow and error handling.

### Tailwind CDN
- Why used: fast UI styling without build tooling.
- Where used: all HTML pages.
- Alternative: custom CSS or a component framework.
- Limitation: no build-time optimization, some repetition in markup.

### localStorage
- Why used: zero-backend analytics and simple state persistence.
- Where used: `assets/app.js`, `index.html`, `coach.html`, `dashboard.html`.
- Alternative: database-backed user profiles.
- Limitation: browser-specific, easy to clear, not shared across devices.

## 18. Technical Trade-offs
- Simplicity vs persistence: localStorage keeps the project easy to run but limits portability and durability.
- Fast prototyping vs production robustness: direct prompt-to-response flow is simple but lacks observability, retries, and guardrails.
- Flexible LLM output vs strict correctness: JSON parsing with fallbacks helps, but the model can still output malformed responses.
- Stateless backend vs user history: server scalability improves, but long-term user tracking is weak.

## 19. Common Interview Questions
- Why FastAPI?
- Why no database?
- How do the pages communicate?
- How does the backend talk to Gemini?
- How do you handle failed model calls?
- How do you ensure the output format is valid JSON?
- Why use localStorage for analytics?
- What happens if the LLM returns invalid JSON?
- How would you secure this in production?
- How would you scale this?

## 20. Deep Cross Questions
- If the backend is stateless, where is user progress stored?
- If `async` is used, why are the calls still blocking?
- If the README says restricted CORS, why does code allow `*`?
- If the app says it uses LangChain, what parts actually depend on it?
- If analytics are “measurable,” where are they persisted?
- What happens if the browser clears localStorage?
- Why not use server-side sessions?

## 21. TCS-Style Questions
- Explain your project end to end.
- Why did you use FastAPI instead of Flask?
- What is REST?
- What status codes would you return for validation failure?
- What is the difference between authentication and authorization?
- How does localStorage differ from cookies?
- What is CORS?
- What is Big-O complexity?
- Explain ACID, even though this repo does not use a DB.
- How would you deploy this to production?
- What is the role of environment variables?
- What is the difference between sync and async?
- Why are prompts important in LLM apps?

## 22. Resume Claims to Defend
### Claim: Built an AI coding mentor with Socratic guidance
- Evidence in repository: `Backend/app/prompts/mentor.py`, `index.html`, `coach.html`, README
- Confidence: High
- Interviewer may ask: How is it Socratic and not direct-answer generation?
- What I must know: The prompt explicitly tells the model not to give direct answers.

### Claim: Built automated code review
- Evidence in repository: `Backend/app/prompts/code_review.py`, `code-review.html`, router and schema files
- Confidence: High
- Interviewer may ask: What fields are returned and how are they parsed?
- What I must know: The review endpoint returns structured analysis fields.

### Claim: Built a mock interview engine
- Evidence in repository: `Backend/app/prompts/interview.py`, `interview.html`, router and schema files
- Confidence: High
- Interviewer may ask: How do scoring and follow-ups work?
- What I must know: The interview flow is question → answer → evaluation → final score.

### Claim: Used FastAPI backend
- Evidence: `Backend/main.py`, `requirements.txt`
- Confidence: High
- Interviewer may ask: Which endpoints are exposed?
- What I must know: The verified routes listed above.

### Claim: Used LangChain and Gemini
- Evidence: `gemini_service.py`, prompts, README, requirements
- Confidence: High
- Interviewer may ask: Where exactly is LangChain used?
- What I must know: Prompt templates are composed into chains with `ChatGoogleGenerativeAI` and `StrOutputParser`.

### Claim: Implemented local learning analytics
- Evidence: `assets/app.js`, `dashboard.html`
- Confidence: High
- Interviewer may ask: Is this server-side analytics?
- What I must know: It is browser localStorage-based only.

### Claim: Deployed frontend on Vercel and backend on Render
- Evidence: README and backend URL in `assets/app.js`
- Confidence: Medium
- Interviewer may ask: Is deployment config in the repo?
- What I must know: It is documented, but explicit deployment manifests were not verified in code.

### Claims that should NOT be overstated
- “Secure REST requests” — not fully supported by code
- “Restricted CORS” — not supported by the actual middleware config
- “Database-backed analytics” — false; analytics are localStorage-only
- “Authentication system” — not present
- “Production-grade observability” — not present

## 23. Weak Areas
1. No database.
2. No authentication/authorization.
3. No production logging or monitoring.
4. No rate limiting.
5. No tests verified.
6. No CI/CD files verified.
7. No Dockerfile verified.
8. No explicit deployment manifests verified.
9. LLM calls are synchronous inside async routes.
10. Browser localStorage can be cleared and is device-specific.

## 24. What I Need to Study
- FastAPI async vs sync behavior
- Pydantic validation and model validators
- REST status codes and error handling
- CORS and browser security basics
- Authentication vs authorization
- localStorage vs cookies vs server sessions
- LLM output parsing and prompt reliability
- Basic scalability patterns for API services
- Production logging and monitoring
- When to use a database

## 25. 50 Most Important Questions
| # | Question | Difficulty | Why interviewer may ask it | What I should answer | Repository evidence | Likely follow-up question |
|---|---|---|---|---|---|---|
| 1 | What problem does AlgoSensei solve? | Basic | To test product understanding | It helps users practice interviews through guided mentoring, code review, and mock interviews | README, pages, prompts | Why not just use ChatGPT directly? |
| 2 | What are the main user flows? | Basic | To test architecture understanding | Mentor, code review, mock interview, dashboard | HTML pages, routers | How does data move between them? |
| 3 | Why did you choose FastAPI? | Basic | To test stack choice | Lightweight API framework with Pydantic integration and easy routing | `Backend/main.py`, requirements | Why not Flask or Django? |
| 4 | What endpoints are implemented? | Basic | To verify code familiarity | `/`, `/api/start_session`, `/api/chat`, `/api/code_review`, `/api/interview/start`, `/api/interview/turn`, `/api/interview/finalize` | routers, README | Which one is synchronous? |
| 5 | What does `localStorage` do in this project? | Basic | To check frontend state management | Stores problem, code, language, theme, and analytics locally in browser | `index.html`, `coach.html`, `assets/app.js` | What happens if the user clears it? |
| 6 | How does the mentor mode work? | Intermediate | To test request flow knowledge | Frontend saves context and backend asks Gemini for a Socratic question | `index.html`, `coach.html`, mentor router, prompt | What makes it Socratic? |
| 7 | How does code review work? | Intermediate | To test structured output handling | Frontend sends code, backend prompts Gemini, parses JSON, and returns review fields | `code-review.html`, code review router, schemas | What if Gemini returns invalid JSON? |
| 8 | How does interview scoring work? | Intermediate | To test stateful conversation design | Scores and round number are returned by the backend and stored in frontend state | interview router and schemas | Where is scoring logic implemented? |
| 9 | Is there a database? | Basic | To test honesty and architecture | No, analytics are browser-local only | `assets/app.js`, dashboard | Why did you avoid a DB? |
| 10 | What is the request lifecycle for code review? | Intermediate | To test end-to-end flow | UI → fetch → router → prompt → Gemini → JSON parse → render | `code-review.html`, router, service | What if the call fails? |
| 11 | How do you handle API failures? | Intermediate | To test resilience | Mentor and interview have fallback responses; code review has fallback JSON data | routers, service | Are retries implemented? |
| 12 | Why use Pydantic models? | Intermediate | To test backend hygiene | To validate request bodies and normalize output shapes | `schemas.py` | What validation is custom? |
| 13 | How do you ensure Gemini output is parseable? | Intermediate | To test LLM robustness | Strip markdown fences, parse JSON, and fall back if parsing fails | `gemini_service.py` | Is that enough for production? |
| 14 | What does `ChatPromptTemplate` do here? | Intermediate | To test prompt flow understanding | It formats prompt variables into a chain that feeds the LLM | prompt files, service | Why not use plain strings? |
| 15 | Why did you store analytics client-side? | Intermediate | To test product trade-offs | Simplicity, no auth friction, no backend database costs | README, `assets/app.js` | What are the drawbacks? |
| 16 | Is the backend really stateless? | Intermediate | To test correctness | Mostly yes; the server keeps no per-user state, but the frontend carries context and history | routers, frontend | What about interview history? |
| 17 | What security controls are implemented? | Intermediate | To test production thinking | CORS and environment variable loading; otherwise minimal | `Backend/main.py`, README | Why is `*` CORS used? |
| 18 | Why is `allow_origins=["*"]` risky? | Deep Technical | To challenge security understanding | It allows any origin to call the API; that is permissive and not production-tight | `Backend/main.py` | How would you restrict it properly? |
| 19 | Does the app use authentication? | Basic | To test feature honesty | No | codebase overall | How would you add it? |
| 20 | Does the app use authorization? | Basic | To test feature honesty | No | codebase overall | How would roles work? |
| 21 | Is the FastAPI route handler truly async? | Deep Technical | To test runtime understanding | The function is async, but the Gemini invocation is synchronous | `routers/*.py`, `gemini_service.py` | What would you change? |
| 22 | What happens if Gemini fails? | Intermediate | To test fault tolerance | The app tries fallback models or returns fallback text/JSON | `gemini_service.py`, routers | Does it retry forever? |
| 23 | Why multiple Gemini models? | Deep Technical | To test resilience reasoning | To try a primary model and fallback to others if one fails | `gemini_service.py` | Could this affect consistency? |
| 24 | What is the purpose of `safe_json_parse`? | Deep Technical | To test output handling | It strips fences and parses model JSON safely with fallback | `gemini_service.py` | What if the model returns malformed arrays? |
| 25 | How is history formatted for the LLM? | Intermediate | To test context handling | It converts role and first text part into readable lines | `gemini_service.py` | What is lost in this transformation? |
| 26 | Why are there separate prompt files? | Intermediate | To test modularity | Each mode has its own prompt contract and behavior | `Backend/app/prompts/` | What changes when adding another mode? |
| 27 | How does the dashboard compute readiness score? | Intermediate | To test frontend logic | It uses counts, topic coverage, and average review/interview scores | `assets/app.js` | Why these weights? |
| 28 | Is readiness score a real ML score? | Deep Technical | To test honesty | No, it is a heuristic computed in JavaScript | `assets/app.js` | Could it be gamed? |
| 29 | What technologies are used on the frontend? | Basic | To verify stack awareness | HTML, Tailwind via CDN, vanilla JS | HTML files | Why no React? |
| 30 | Why not use a database for analytics? | Intermediate | To test trade-offs | Simpler demo, local persistence, no backend storage needed | README and JS | What if the user uses another browser? |
| 31 | What happens if browser storage is cleared? | Intermediate | To test understanding of limitations | Analytics and saved context are lost | `assets/app.js`, `index.html`, `coach.html` | How would you persist it? |
| 32 | How does the frontend communicate with backend? | Basic | To test integration knowledge | Using `fetch` with JSON bodies | `code-review.html`, `interview.html` | What headers are sent? |
| 33 | Are there any database queries? | Basic | To test DB honesty | No | codebase overall | Then what persists server-side? |
| 34 | What output shape does the code review endpoint return? | Intermediate | To test API contract awareness | Structured analysis fields plus `from` | schema and router | How do you handle invalid fields? |
| 35 | Why do response models use alias `from`? | Deep Technical | To test Pydantic knowledge | To expose `from` in JSON while mapping to a valid Python attribute name | `schemas.py` | Why set `populate_by_name=True`? |
| 36 | What is the role of `model_validator`? | Deep Technical | To test Pydantic v2 skills | It normalizes list/string output into a consistent format | `schemas.py` | Why normalize at model level instead of service level? |
| 37 | What does `recordInterviewCompleted` do? | Intermediate | To test frontend analytics logic | Stores completion data, score, and boosts topic practice weights | `assets/app.js` | Why is interview weighted more? |
| 38 | What is the biggest bottleneck in the app? | Deep Technical | To test performance reasoning | External LLM latency and model failures | backend service | How would you reduce it? |
| 39 | How would you scale this to 10x users? | Backend/SDE | To test systems thinking | Keep backend stateless, add auth, rate limiting, caching, and queueing | architecture | What about LLM cost? |
| 40 | How would you handle 100x traffic? | Backend/SDE | To test scaling depth | Introduce async downstream calls, load balancing, request quotas, and caching | architecture | Which endpoint is most expensive? |
| 41 | What happens if the external API rate-limits you? | Deep Technical | To test resilience | Fallback models are attempted, but there is no full quota management | `gemini_service.py` | What if all models are rate-limited? |
| 42 | Why is the app called “backend” if UI is static? | Intermediate | To test system boundary understanding | Backend handles all AI logic; frontend is static presentation and client state | project structure | Why not use SSR? |
| 43 | How do you prevent malicious prompt content? | Deep Technical | To test security thinking | You don’t fully; there is no strong prompt-injection defense in repo | prompts and flow | What would you add? |
| 44 | Is there logging? | Basic | To test observability honesty | Only a simple print on model failure | service | Why is structured logging better? |
| 45 | Are tests present? | Basic | To test maturity | No tests were verified in the repository | repo structure | What should be tested first? |
| 46 | Are Docker files present? | Basic | To test deployment readiness | Not verified in the repository | repo structure | How would you containerize it? |
| 47 | How is CORS configured and why? | Intermediate | To test browser security knowledge | Middleware allows all origins in code; intended to permit frontend access | `Backend/main.py` | Why is the README different? |
| 48 | What would you change if rebuilding it? | Backend/SDE | To test reflection | Add auth, DB, better observability, async LLM client, and stronger validation | whole repo | What would you prioritize first? |
| 49 | What concepts should you study before mentioning this project? | Basic | To probe readiness | FastAPI, HTTP, auth, CORS, localStorage, async, Pydantic, LLM prompting | whole repo | Which one is weakest for you? |
| 50 | What is one claim from the README you cannot fully defend? | Trap | To test honesty | The README says restricted CORS and certain future roadmap items, but code does not fully verify them | README vs code mismatch | Can you show evidence in code? |

## 26. Final honest summary
This project is strongest as a lightweight AI workflow demo with clear frontend pages and a modular FastAPI backend. It is weak as a production backend system because it lacks database persistence, authentication, authorization, real observability, rate limiting, tests, and deployment infrastructure in the inspected code. The most defensible interview story is: static frontend + FastAPI + prompt-engineered Gemini workflows + browser-local analytics.
