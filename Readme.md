# AlgoSensei: Your Personal AI Coding Tutor

[![Vercel Deployment](https://img.shields.io/badge/Frontend-Deployed%20on%20Vercel-black?style=for-the-badge&logo=vercel)](https://algosensei-frontend.vercel.app/)
[![Render Deployment](https://img.shields.io/badge/Backend-Deployed%20on%20Render-46E3B7?style=for-the-badge&logo=render)](https://algosenseibackend.onrender.com/)

**AlgoSensei** is a web application designed to be the personal mentor every developer wishes they had. Instead of just giving you the answer, it uses the Socratic method to guide you toward the optimal solution for your coding problems, fostering deep understanding over rote memorization.

### [➡️ Visit the Live Application ⬅️](https://algosensei-frontend.vercel.app/)



---

## 🌟 Features

*   **Socratic Dialogue**: The AI tutor asks guiding questions that force you to think critically about your own code, leading to "aha!" moments.
*   **Complexity-Aware Guidance**: The AI identifies performance bottlenecks (e.g., time/space complexity) and prompts you to consider more efficient algorithms and data structures.
*   **Personalized Feedback**: The conversation adapts to your specific code and thought process, providing a tailored learning experience.
*   **Multi-Language Support**: Get help with Python, JavaScript, Java, and C++.
*   **Sleek, Responsive UI**: A beautiful and intuitive interface with both light and dark modes, built with Tailwind CSS.

---

## ⚙️ How It Works: The Technical Workflow

AlgoSensei is built on a modern web stack, separating the frontend and backend for scalability and maintainability.

1.  **User Input (Frontend)**: The user visits the `index.html` page, enters a problem description, their code solution, and selects the language.
2.  **Session Start (Frontend → Backend)**:
    *   Upon clicking "Coach Me!", the input data is saved to `localStorage`.
    *   The user is redirected to `coach.html`.
    *   The `coach.html` JavaScript makes a `POST` request to the `/api/start_session` endpoint on the FastAPI backend.
3.  **Initial Analysis (Backend)**:
    *   The FastAPI backend receives the initial problem, code, and language.
    *   It uses a specialized LangChain prompt (`socratic_start_prompt`) to instruct the Google Gemini model to analyze the user's code and formulate the *first* Socratic question.
    *   The backend returns this first question to the frontend.
4.  **Interactive Chat (Frontend ↔ Backend Loop)**:
    *   The user sees the AI's first question and types a response.
    *   When the user sends a message, the frontend makes a `POST` request to the `/api/chat` endpoint. This request includes the original problem/code context *and* the entire chat history.
    *   The backend uses a second LangChain prompt (`socratic_continue_prompt`) which instructs the Gemini model to continue the conversation based on the history.
    *   The AI generates the next logical question, which is sent back to the frontend and displayed to the user.
    *   This loop continues, creating a dynamic and interactive tutoring session.

---

## 🚀 Tech Stack

| Component      | Technology                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| **Frontend**   | `HTML5`, `Tailwind CSS`, `Vanilla JavaScript`                                                          |
| **Backend**    | `Python 3`, `FastAPI`, `Uvicorn`                                                                       |
| **AI Logic**   | `Google Gemini Pro`, `LangChain`                                                                       |
| **Deployment** | **Frontend:** Vercel, **Backend:** Render                 |

---

## 🛠️ Local Development Setup

Want to run AlgoSensei on your own machine? Follow these steps.

### Prerequisites

*   Git
*   Python 3.10+
*   A code editor like VS Code

### 1. Clone the Repository

```bash
git clone https://github.com/Diwakar-18/AlgoSENSEI.git
cd AlgoSENSEI
```

### 2. Backend Setup

The backend server runs on FastAPI and powers the AI logic.

```bash
# Navigate to the backend directory
cd Backend

# Create and activate a virtual environment
# On Windows
python -m venv venv
.\venv\Scripts\activate
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Create an environment file for your API key
# Create a new file named 'python.env' in the 'Backend' directory
# and add your Google API key to it:
echo "GOOGLE_API_KEY='your_google_api_key_here'" > python.env

# Run the backend server
uvicorn main:app --reload
```

Your backend is now running at `http://127.0.0.1:8000`.

### 3. Frontend Setup

The frontend is a set of static HTML/CSS/JS files. The easiest way to serve them is with the "Live Server" extension in VS Code.

1.  Open the `AlgoSENSEI` project folder in VS Code.
2.  Install the Live Server extension.
3.  Right-click on `index.html` and select "Open with Live Server".

Your browser will open to `http://127.0.0.1:5500` (or a similar port), and you can start using the application. The frontend code is already configured to automatically connect to your local backend when running on `127.0.0.1`.

---

## 🌐 Deployment

The application is deployed as two separate services:

1.  **Backend (Render)**:
    *   **Service Type**: Web Service
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    *   **Environment Variables**: The `GOOGLE_API_KEY` is set as a secret environment variable in the Render dashboard.

2.  **Frontend (Vercel)**:
    *   The project is imported into Vercel from the GitHub repository.
    *   Vercel automatically detects it as a static site (Framework Preset: "Other").
    *   No build command is needed. Vercel serves the static files from the root of the repository.
    *   The `coach.html` file contains logic to switch the `BACKEND_URL` to the live Render URL when it's not running on localhost.

---

## 👨‍💻 About the Founder

> "As a B.Tech student preparing for SDE roles myself, I constantly felt the gap between just solving a problem and truly understanding its core principles. I built AlgoSensei to be the bridge—a tool that doesn't just validate your code, but elevates your thinking."
>
> — Diwakar

---

*This project was built with ❤️ for coders.*
