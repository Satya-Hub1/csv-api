# CSV API — Python (FastAPI)

Python port of the original Java Spring Boot CSV API.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/csv/content` | Download a CSV from Google Drive and return rows as JSON |

### Request body

```json
{ "googleDriveUrl": "https://drive.google.com/file/d/<FILE_ID>/view" }
```

### Response

```json
{
  "success": true,
  "totalRecords": 3,
  "records": [
    { "col1": "val1", "col2": "val2" },
    ...
  ]
}
```

## Running locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The server starts on **http://localhost:8000**.  
Interactive docs: **http://localhost:8000/docs**

## Example curl

```bash
curl -X POST http://localhost:8000/api/csv/content \
  -H "Content-Type: application/json" \
  -d '{"googleDriveUrl": "https://drive.google.com/file/d/YOUR_FILE_ID/view"}'
```
