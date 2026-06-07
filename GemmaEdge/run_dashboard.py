import os
import subprocess
import sys
import yaml


def load_frontend_config():
    """Reads the master configuration matrix."""
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ [CRITICAL ERROR]: {config_path} not found!")
        exit(1)

    # Määrame utf-8 kodeeringu, et Windowsi terminalid ei viskaks emoji tõttu vigu
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    cfg = load_frontend_config()

    # Otsetee frontend sektsioonile
    front_cfg = cfg['frontend']

    # Extract settings from YAML
    port = str(front_cfg['port'])
    headless = "true" if front_cfg['headless'] else "false"

    print("\n" + "=" * 55)
    print(" 😼 GemmaEdge Dashboard — Sovereign Launcher Active")
    print(f" 📡 Local URL: http://localhost:{port}")
    print("=" * 55 + "\n")

    # Käivitame Streamliti põhiprotsessi
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "frontend/dashboard.py",
        "--server.port", port,
        "--server.headless", headless
    ])
