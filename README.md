# Deal Machine Test - Message Analysis Platform

## Overview
This project is a full-stack message analysis platform built with FastAPI, PostgreSQL, and a modern HTML/JS frontend. It demonstrates advanced backend and frontend integration, database management, and AI-powered text analysis. The app is designed as a skill test for a Software Analyst position, showcasing best practices in API design, containerization, and user experience.

## Features
- **FastAPI Backend**: Robust REST API for message CRUD, search, and analytics.
- **PostgreSQL Database**: Reliable storage for all messages and metadata.
- **AI-Powered Analysis**: Automatic extraction of keywords, intention, and feeling from messages using both static rules and an AI agent.
- **Advanced Filtering**: Search messages by username, keywords, feeling, intention, and date range.
- **Distinct Endpoints**: Retrieve all unique usernames, keywords, feelings, and intentions for dynamic filtering.
- **Modern Frontend**: Responsive HTML/JS interface with live filtering and beautiful message cards.
- **Containerized**: One-command startup with Docker Compose, including Adminer for DB inspection.

## Architecture
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Jinja2, Uvicorn
- **Database**: PostgreSQL (with Adminer for easy DB management)
- **Frontend**: HTML, CSS (Tailwind), JavaScript (fetch API)
- **AI Agent**: Pluggable logic for message analysis (see `filters.py` and `analyze_agent.py`)

## Quick Start
### Prerequisites
- Docker & Docker Compose installed

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd deal_machine-test
```

### 2. Start all services (API, DB, Adminer) with one command
```sh
docker compose up --build
```
- The API will be available at [http://localhost:8000](http://localhost:8000)
- The frontend is served at the root URL.
- Adminer (DB UI) is at [http://localhost:8080](http://localhost:8080)
  - System: PostgreSQL
  - Server: db
  - Username: example
  - Password: example
  - Database: postgres

### 3. Using the App
- Open [http://localhost:8000](http://localhost:8000) in your browser.
- Add messages, search, and filter using the intuitive UI.
- All analysis is automatic—try different texts to see keyword, intention, and feeling extraction.

### 4. API Endpoints
- `POST /add_message/` — Add a new message (auto-analyzed)
- `GET /list_messages/` — List/search messages (filter by username, keywords, feeling, intention, date)
- `GET /distinct_usernames/` — List all unique usernames
- `GET /distinct_keywords/` — List all unique keywords
- `GET /distinct_feelings/` — List all unique feelings
- `GET /distinct_intentions/` — List all unique intentions
- `POST /from_telegram/` — Ingest and analyze Telegram-style messages

### 5. Customization
- **Message Analysis**: Edit `filters.py` and `analyze_agent.py` to change how keywords, intentions, and feelings are extracted.
- **Database Models**: See `db_manager.py` for SQLAlchemy models.
- **Frontend**: Edit `templates/index.html` and `static/script.js` for UI changes.

## Project Structure
```
.
├── api.py                # FastAPI app and endpoints
├── db_manager.py         # DB models and session management
├── filters.py            # Message analysis logic
├── analyze_agent.py      # AI agent for advanced analysis
├── requirements.txt      # Python dependencies
├── Dockerfile            # API container build
├── compose.yaml          # Docker Compose config
├── start.sh              # Entrypoint: create tables, then start API
├── static/
│   └── script.js         # Frontend JS
├── templates/
│   └── index.html        # Frontend HTML
└── ...
```

## Why This Project Stands Out
- **Production-Ready Patterns**: Clean separation of concerns, robust error handling, and scalable architecture.
- **DevOps Friendly**: Fully containerized, easy to deploy, and works out-of-the-box.
- **User Experience**: Modern, responsive UI with real-time filtering and feedback.
- **Extensible**: Easily add new analysis logic, endpoints, or UI features.

## Author & Contact
Felipe Costa

---

**Ready to deliver value as a Software Analyst!**

---

*Feel free to reach out for any questions or improvements.*
