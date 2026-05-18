import time
import threading
import httpx
from telemetry.gpu_monitor import get_telemetry_data

boot_complete = False


def _telemetry_loop(start_time: float):
    """Background thread — prints live telemetry every 0.5s during boot."""
    while not boot_complete:
        try:
            elapsed = time.time() - start_time

            r = httpx.get("http://localhost:11434/api/ps", timeout=2)
            models_loaded = r.json().get("models", [])
            ollama_vram = sum(m.get("size_vram", 0) for m in models_loaded) / 1e9

            data = get_telemetry_data()

            # LISATUD: GPU LOAD näidik telemeetria ritta
            print(
                f"\r⏱ {elapsed:.1f}s | "
                f"GPU VRAM: {data['vram_used']:.2f}GB | "
                f"GPU LOAD: {data['gpu_load']}% | "
                f"Ollama VRAM: {ollama_vram:.2f}GB | "
                f"TEMP: {data['gpu_temp']}°C | "
                f"CPU: {data['cpu_load']}% | "
                f"RAM: {data['ram_used']:.2f}GB",
                end="", flush=True
            )
        except Exception:
            pass
        time.sleep(0.5)


def start_boot_telemetry() -> tuple:
    global boot_complete
    boot_complete = False
    start_time = time.time()
    thread = threading.Thread(target=_telemetry_loop, args=(start_time,), daemon=True)
    thread.start()
    return thread, start_time


def stop_boot_telemetry(start_time: float):
    global boot_complete
    boot_complete = True
    time.sleep(0.6)
    boot_time = time.time() - start_time
    print(f"\n\n✅ Engine HOT in {boot_time:.1f}s")
    return boot_time


def print_telemetry_snapshot():
    """Gate 2 — clean snapshot after boot completes."""
    print("=" * 55)
    print("GATE 2 — Telemetry Snapshot")

    data = get_telemetry_data()

    try:
        r = httpx.get("http://localhost:11434/api/ps", timeout=2)
        models = r.json().get("models", [])
        for m in models:
            print(f"  Model  : {m.get('name', 'unknown')}")
            print(f"  VRAM   : {m.get('size_vram', 0) / 1e9:.2f} GB")
    except Exception:
        print("  Ollama API unreachable — using system VRAM only")

    # LISATUD: GPU LOAD ka lõpp-snapshot'i
    print(f"  GPU    : {data['vram_used']:.2f} GB used | LOAD: {data['gpu_load']}% | {data['gpu_temp']}°C")
    print(f"  CPU    : {data['cpu_load']}%")
    print(f"  RAM    : {data['ram_used']:.2f} GB")
    print("=" * 55)