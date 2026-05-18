from fastapi import APIRouter
from api.state import selector
from telemetry.gpu_monitor import get_telemetry_data

router = APIRouter()


# =========================
# 🧠 SHARED TELEMETRY CORE
# =========================
def base_telemetry():
    data = get_telemetry_data()

    return {
        "vram_used": round(data["vram_used"], 2),
        "vram_total": round(data["vram_total"], 1),
        "gpu_temp": data["gpu_temp"],
        "gpu_load": data["gpu_load"],  # LISATUD: Reaalne koormus (0-100%)
        "cpu_load": round(data["cpu_load"], 1),
        "ram_used": round(data["ram_used"], 2),
    }


# =========================
# 🟢 FULL STATUS ENDPOINT
# =========================
@router.get("/status")
def status():
    payload = base_telemetry()

    payload.update({
        "active_module": selector.current_model
    })

    return payload


# =========================
# ⚡ LIGHTWEIGHT PING ENDPOINT
# =========================
@router.get("/ping")
def ping():
    return base_telemetry()