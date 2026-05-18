"""
run_api.py — GemmaEdge API Launcher (Sovereign Edition)
Root level, beside boot.py

Usage: python run_api.py
This version is fully anchored to config.yaml.
"""

import uvicorn
import yaml
import os


def load_sovereign_config():
    """Reads the master configuration matrix."""
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ [CRITICAL ERROR]: {config_path} not found in root!")
        exit(1)

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    # Load settings from your YAML control panel
    cfg = load_sovereign_config()

    # Extract API and Logging parameters
    host = cfg['api']['host']
    port = cfg['api']['port']
    reload_mode = cfg['api']['reload']
    workers = cfg['api']['workers']
    log_level = cfg['logging']['log_level']

    # 🧠 Set dev runtime flags for internal logic
    os.environ["GEMMAEDGE_MODE"] = "dev" if reload_mode else "prod"

    print("\n" + "=" * 55)
    print(" 🔥 GemmaEdge API — Sovereign Launcher Active")
    print(f" 📡 Target: http://{host}:{port}")
    print(f" ⚡ Reload: {'ENABLED' if reload_mode else 'DISABLED'}")
    print(f" 🏗️  Engine: MiniLM (F-Drive Local)")
    print("=" * 55 + "\n")

    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=reload_mode,
        workers=workers,
        log_level=log_level,
        access_log=True
    )