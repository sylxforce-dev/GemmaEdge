"""
run_dashboard.py — GemmaEdge Dashboard Launcher (Sovereign Edition)
Root level, beside boot.py and run_api.py
"""
import subprocess
import sys
import yaml
import os


def load_frontend_config():
    """Reads the master configuration matrix."""
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ [CRITICAL ERROR]: {config_path} not found!")
        exit(1)

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    cfg = load_frontend_config()

    # Extract settings from YAML
    port = str(cfg['frontend']['port'])
    headless = "true" if cfg['frontend']['headless'] else "false"

    print("\n" + "=" * 55)
    print(" 😼 GemmaEdge Dashboard — Sovereign Launcher Active")
    print(f" 📡 Local URL: http://localhost:{port}")
    print("=" * 55 + "\n")

    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "frontend/dashboard.py",
        "--server.port", port,
        "--server.headless", headless
    ])