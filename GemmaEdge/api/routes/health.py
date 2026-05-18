"""
health.py — Health Check
api/routes/health.py
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "online",
        "engine": "GemmaEdge",
        "version": "1.0"
    }