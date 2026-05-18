"""
runtime_monitor.py — Live Inference Telemetry
telemetry/runtime_monitor.py

Runs in background thread during model inference.
Prints telemetry snapshot every 10 seconds.
Used by speaking2.py now, API layer later.
"""

import time
import threading
from telemetry.gpu_monitor import get_telemetry_data

_monitor_active = False
_monitor_thread = None


def _monitor_loop(start_time: float):
    """Prints telemetry every 10s during inference."""
    while _monitor_active:
        time.sleep(10)
        if not _monitor_active:
            break
        elapsed = time.time() - start_time
        data = get_telemetry_data()

        # LISATUD: GPU LOAD, et näha reaalset koormust genereerimise ajal
        print(
            f"\n[LIVE | {elapsed:.1f}s | "
            f"GPU LOAD: {data['gpu_load']}% | "
            f"VRAM: {data['vram_used']:.2f}/{data['vram_total']:.1f}GB | "
            f"TEMP: {data['gpu_temp']}°C | "
            f"CPU: {data['cpu_load']}% | "
            f"RAM: {data['ram_used']:.2f}GB]"
        )


def start_runtime_monitor() -> float:
    """Starts inference telemetry thread. Returns start time."""
    global _monitor_active, _monitor_thread
    _monitor_active = True
    start_time = time.time()
    _monitor_thread = threading.Thread(
        target=_monitor_loop,
        args=(start_time,),
        daemon=True
    )
    _monitor_thread.start()
    return start_time


def stop_runtime_monitor(start_time: float) -> float:
    """Stops inference telemetry thread. Returns total inference time."""
    global _monitor_active
    _monitor_active = False
    return time.time() - start_time