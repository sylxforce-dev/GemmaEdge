from fastapi import APIRouter
from api.state import selector
from telemetry.gpu_monitor import get_telemetry_data

router = APIRouter()


# =====================================================================
# --- SHARED TELEMETRY CORE (Low-Level NVML & NumPy Data Fetch) ---
# =====================================================================
def base_telemetry():
    """Retrieves low-level hardware performance stats from the GPU layer."""
    data = get_telemetry_data()

    return {
        "vram_used": round(data["vram_used"], 2),
        "vram_total": round(data["vram_total"], 1),
        "gpu_temp": data["gpu_temp"],
        "gpu_load": data["gpu_load"],  # Real-time GPU execution load (0-100%)
        "cpu_load": round(data["cpu_load"], 1),
        "ram_used": round(data["ram_used"], 2),
    }


# =====================================================================
# --- 🟢 FULL STATUS ENDPOINT (Diagnostics & Active Active State) ---
# =====================================================================
@router.get("/status")
def status():
    """Returns comprehensive telemetry mapped with the active model runtime."""
    payload = base_telemetry()

    # FIX: Dynamic check prevents AttributeError. 
    # Reads the active model state from the v1.4 selector matrix.
    active = selector.current_model if selector.current_model else "misha-maincore (Cold Boot)"

    payload.update({
        "active_module": active
    })

    return payload


# =====================================================================
# --- ⚡ LIGHTWEIGHT PING ENDPOINT ---
# =====================================================================
@router.get("/ping")
def ping():
    """Lightweight endpoint to verify API connection state."""
    return base_telemetry()
