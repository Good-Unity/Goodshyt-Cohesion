from fastapi import FastAPI
from .models import AssignmentRequest
from .service import CohesionService

app = FastAPI(title="GoodShyt Cohesion", version="0.1.0")
service = CohesionService()

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "goodshyt-cohesion"}

@app.post("/assign")
def assign(payload: AssignmentRequest) -> dict[str, object]:
    return {"assignments": [item.model_dump() for item in service.assign(payload)]}
