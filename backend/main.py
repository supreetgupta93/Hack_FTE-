import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import enrich_company


app = FastAPI(
    title="Prospect Research Agent"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path("company_profiles.json")


class EnrichRequest(BaseModel):
    website_name: str
    url: str


def load_results():

    if not DATA_FILE.exists():

        with open(
            DATA_FILE,
            "w"
        ) as f:

            json.dump([], f)

    try:

        with open(
            DATA_FILE,
            "r"
        ) as f:

            return json.load(f)

    except:

        return []


def save_result(data):

    results = load_results()

    results.append(data)

    with open(
        DATA_FILE,
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )


@app.get("/")
def home():

    return {
        "message":
        "Prospect Research Agent API Running"
    }


@app.post("/enrich")
def enrich(request: EnrichRequest):

    try:

        result = enrich_company(
            request.url
        )

        result["website_name"] = (
            request.website_name
        )

        save_result(result)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/results")
def get_results():

    return load_results()