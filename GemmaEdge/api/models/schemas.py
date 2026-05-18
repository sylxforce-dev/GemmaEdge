"""
schemas.py — Pydantic Request/Response Models
api/models/schemas.py
"""

from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str


class StatusResponse(BaseModel):
    active_module: str
    vram_used: float
    vram_total: float
    gpu_temp: int
    cpu_load: float
    ram_used: float