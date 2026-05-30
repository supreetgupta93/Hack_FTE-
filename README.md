# Prospect Research Agent

A production-ready hackathon project that enriches company profiles via a FastAPI backend and Streamlit frontend.

## Overview

- Backend: `FastAPI`
- Frontend: `Streamlit`
- Storage: `company_profiles.json`
- Deployment: `Render`
- AI Integration: `Gemini API` via environment variable

## Project Structure

```
backend/
  main.py
  scraper.py
  company_profiles.json
frontend/
  app.py
requirements.txt
render.yaml
README.md
```

## Local Setup

1. Create a Python virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set required environment variables:

   - `GEMINI_API_KEY` for backend AI integration
   - `API_BASE_URL` for the frontend (default: `http://localhost:8000`)

   Example Windows PowerShell:

   ```powershell
   $env:GEMINI_API_KEY = "your_api_key_here"
   $env:API_BASE_URL = "http://localhost:8000"
   ```

4. Run the backend from the project root:

   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

5. In a separate terminal, run the frontend from the project root:

   ```bash
   streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
   ```

6. Open Streamlit in your browser:

   ```text
   http://localhost:8501
   ```

## Render Deployment

1. Push the repository to a Git provider connected to Render.
2. Create two Render web services, one for the backend and one for the frontend.
3. In each service, set the environment variables:

   - Backend: `GEMINI_API_KEY`
   - Frontend: `API_BASE_URL` set to the deployed backend URL

4. Use these start commands:

   - Backend: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Frontend: `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0`

5. Ensure the frontend service points to the live backend URL in `API_BASE_URL`.

6. Verify the backend service is running before using the frontend.

## API Endpoints

- `POST /enrich`
  - Request body: `{ "website_name": "OpenAI", "url": "https://openai.com" }`
  - Response: enriched company profile JSON

- `GET /results`
  - Response: list of stored company profiles

## Notes

- `backend/scraper.py` contains the `enrich_company(url: str) -> dict` entrypoint.
- Do not rewrite the function signature in `scraper.py` if you already have an existing implementation.
- The backend safely creates `company_profiles.json` if it does not exist.
