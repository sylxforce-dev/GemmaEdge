"""
main.py — GemmaEdge API Entry Point (Sovereign Edition)
api/main.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yaml
import os

from api.routes import health, status, generate, debug
from api.state import selector
from telemetry.gpu_monitor import get_telemetry_data

# --- LOAD CONFIG FOR ACCURATE LOGGING ---
def load_api_config():
    base_path = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(base_path, "config.yaml"), "r") as f:
        return yaml.safe_load(f)

cfg = load_api_config()

app = FastAPI(
    title="GemmaEdge API",
    version="1.4"
)

# ---------------------------------------------------
# CORS (Sovereign Open Mode)
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
app.include_router(health.router)
app.include_router(status.router)
app.include_router(generate.router)
app.include_router(debug.router)

# ---------------------------------------------------
# STARTUP TRACE
# ---------------------------------------------------
@app.on_event("startup")
async def startup_trace():
    # Kasutame YAML seadistust, et otsustada, kas näidata logi
    if not cfg['logging']['debug_enabled']:
        return

    data = get_telemetry_data()

    print("\n" + "=" * 55)
    print(" 😼 GemmaEdge API — Sovereign Local Runtime")
    print("=" * 55)

    # Sync dynamic logs with active settings
    print(f" API ENDPOINT: http://{cfg['api']['host']}:{cfg['api']['port']}")
    print(f" REASONING MODE: {cfg['router']['threshold']} Threshold")

    print("-" * 55)
    print(f" Active Module : {selector.current_model}")
    print(f" VRAM Usage    : {data['vram_used']:.2f} GB / {cfg['hardware']['gpu_vram_limit']} GB")
    print(f" GPU Temp      : {data['gpu_temp']}°C")
    print("-" * 55)

    print(" REGISTERED ROUTES:")
    print("   GET  /status  |  POST /generate  |  GET /health")
    print("=" * 55 + "\n")