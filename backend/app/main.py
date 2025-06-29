from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ← relative import (works because main.py and crud_router.py share the same folder)
from app.crud_router import router as crud_router
from app.vt_router    import router as vt_router
from app.threat_intel.router import router as threat_intel_router
from dotenv       import load_dotenv

load_dotenv()      # pulls VT_API_KEY from .env

app = FastAPI(
    title="OpenThreat Fusion API – student edition",
    description="Demonstrates OWASP-aligned validation and VirusTotal enrichment",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Add health check endpoint for tests
@app.get("/")
def health_check():
    return {"status": "ok"}

# SECURITY NOTE: Authentication deliberately omitted in student/demo edition.
# TODO: Implement JWT authentication with role-based access before any production use.

# Include routers
app.include_router(crud_router)
app.include_router(vt_router)
app.include_router(threat_intel_router)
