"""
debug.py — Debug Service
api/routes/debug.py

Full visibility into what API is doing.
Toggle off with DEBUG_MODE = False in debug_config.py.
"""

from fastapi import APIRouter, HTTPException
from api.debug_config import DEBUG_MODE
from api.state import selector
from telemetry.gpu_monitor import get_telemetry_data
import pynvml

router = APIRouter(prefix="/debug", tags=["debug"])


def _check_debug():
    if not DEBUG_MODE:
        raise HTTPException(status_code=403, detail="Debug mode is disabled.")


@router.get("/router")
def debug_router(prompt: str):
    _check_debug()

    previous_model = selector.current_model
    inp = prompt.lower()

    matched_model = "misha-maincore"
    matched_trigger = None

    for model, triggers in selector.matrix.items():
        for trigger in triggers:
            if trigger in inp:
                matched_model = model
                matched_trigger = trigger
                break
        if matched_trigger:
            break

    return {
        "prompt": prompt,
        "routed_to": matched_model,
        "previous_model": previous_model,
        "swap_required": matched_model != previous_model,
        "trigger_matched": matched_trigger if matched_trigger else "none — default maincore",
        "debug_mode": DEBUG_MODE
    }


@router.get("/telemetry")
def debug_telemetry():
    _check_debug()

    data = get_telemetry_data()

    try:
        pynvml.nvmlInit()
        nvml_status = "ok"
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
    except Exception as e:
        nvml_status = f"error: {e}"
        gpu_name = "unknown"

    return {
        "vram_used_gb": data["vram_used"],
        "vram_total_gb": data["vram_total"],
        "vram_free_gb": round(data["vram_total"] - data["vram_used"], 2),
        "gpu_temp_c": data["gpu_temp"],
        "gpu_load_pct": data["gpu_load"], # LISATUD: Reaalne koormus
        "cpu_load_pct": data["cpu_load"],
        "ram_used_gb": data["ram_used"],
        "gpu_name": gpu_name,
        "pynvml_status": nvml_status,
        "debug_mode": DEBUG_MODE
    }


@router.get("/status")
def debug_status():
    _check_debug()

    data = get_telemetry_data()

    return {
        "active_module": selector.current_model,
        "matrix_loaded": len(selector.matrix) > 0,
        "matrix_modules": list(selector.matrix.keys()),
        "matrix_trigger_counts": {
            model: len(triggers)
            for model, triggers in selector.matrix.items()
        },
        "telemetry": {
            "vram_used_gb": data["vram_used"],
            "vram_total_gb": data["vram_total"],
            "gpu_temp_c": data["gpu_temp"],
            "gpu_load": data["gpu_load"], # LISATUD: Reaalne koormus
            "cpu_load_pct": data["cpu_load"],
            "ram_used_gb": data["ram_used"],
        },
        "debug_mode": DEBUG_MODE
    }


@router.get("/toggle")
def debug_toggle():
    return {
        "debug_mode": DEBUG_MODE,
        "message": "To toggle debug mode, change DEBUG_MODE in api/debug_config.py"
    }