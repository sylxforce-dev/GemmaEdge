"""
gates.py — Sovereign Master Controller v1.4
GemmaEdge | Single Source of Truth: config.yaml
"""

import os
import sys
import yaml
import ollama

# Resolve internal module paths for cross-package imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from telemetry.boot_telemetry import start_boot_telemetry, stop_boot_telemetry, print_telemetry_snapshot
from engine_starter.kill_switch import kill_misha_runtime
from router.misha_selector import MishaSelector
from telemetry.gpu_monitor import get_telemetry_data
from router.misha_functions import call_misha_stream


def _load_config():
    """Reads master config.yaml from project root."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


cfg = _load_config()
selector = MishaSelector()


def run_boot_sequence():
    """Master boot sequence. Direct YAML-to-Engine orchestration."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  😼 LocalForge Boot Sequence — GemmaEdge")
    print(f"  Sovereign System | {cfg['hardware']['gpu_vram_limit']} GB VRAM Limit\n")
    print("=" * 55)
    print("GATE 1 — Engine Ignition | Locking MainCore...\n")

    _, start_time = start_boot_telemetry()

    # --- DIRECT IGNITION ---
    try:
        # Võtame nime otse YAML-ist, ilma misha_engine.py vahenduseta
        main_model = cfg['personalities']['main_core']

        ollama.chat(
            model=main_model,
            messages=[{'role': 'user', 'content': 'System check. Confirm logic status.'}],
            keep_alive=-1  # Permanent lock
        )
        print(f"✅ {main_model.upper()} HOT and locked.")
    except Exception as e:
        stop_boot_telemetry(start_time)
        print(f"❌ Ignition failed: {e}")
        return

    stop_boot_telemetry(start_time)
    print("✅ GATE 1 PASS")
    print_telemetry_snapshot()

    print(f"MISHA IS LIVE — Reasoning over Reflex active ({cfg['router']['threshold']}).")
    print("=" * 55)

    _input_loop()


def _input_loop():
    while True:
        try:
            inp = input("\n[OP]: ").strip()
            if not inp: continue

            if inp.lower() in ['exit', 'quit', 'lõpeta']:
                kill_misha_runtime()
                sys.exit(0)

            active_model = selector.select_personality(inp)
            print("MISHA: ", end="", flush=True)

            stream = call_misha_stream(inp, active_model)
            if stream:
                for chunk in stream:
                    print(chunk['message']['content'], end='', flush=True)

            status = get_telemetry_data()
            print(
                f"\n\n[{active_model.upper()} | LOAD: {status['gpu_load']}% | {status['vram_used']:.2f} GB | {status['gpu_temp']}°C]")

        except KeyboardInterrupt:
            kill_misha_runtime()
            sys.exit(0)


if __name__ == "__main__":
    run_boot_sequence()