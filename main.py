import csv
import io
import re
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CSV API", version="1.0.0")


# ── DTOs ──────────────────────────────────────────────────────────────────────

class CsvRequest(BaseModel):
    googleDriveUrl: str


class CsvJsonResponse(BaseModel):
    success: bool
    totalRecords: int
    records: list[dict[str, Any]]


# ── Service ───────────────────────────────────────────────────────────────────

def extract_file_id(drive_url: str) -> str:
    """Extract the file ID from a Google Drive share URL."""
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", drive_url)
    if not match:
        raise ValueError("Invalid Google Drive URL")
    return match.group(1)


def download_csv(drive_url: str) -> str:
    """Download CSV content from a Google Drive share URL."""
    file_id = extract_file_id(drive_url)
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    with httpx.Client(follow_redirects=True, timeout=30) as client:
        response = client.get(download_url)
        response.raise_for_status()
        return response.text


def parse_csv(csv_content: str) -> list[dict[str, str]]:
    """Parse CSV string into a list of dicts (header row becomes keys)."""
    reader = csv.DictReader(io.StringIO(csv_content))
    return [dict(row) for row in reader]


# ── Controller ────────────────────────────────────────────────────────────────

@app.post("/api/csv/content", response_model=CsvJsonResponse)
def get_content(request: CsvRequest) -> CsvJsonResponse:
    """Download a CSV from Google Drive and return its rows as JSON."""
    try:
        content = download_csv(request.googleDriveUrl)
        records = parse_csv(content)
        return CsvJsonResponse(
            success=True,
            totalRecords=len(records),
            records=records,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch CSV: {exc}") from exc
