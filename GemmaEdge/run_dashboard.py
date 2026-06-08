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

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    cfg = load_frontend_config()

    # FIX: Use .get() to prevent KeyError crashes if 'frontend' or 'headless' is missing
    frontend_cfg = cfg.get('frontend', {})

    port = str(frontend_cfg.get('port', 8501))

    # If 'headless' is not specified, default to 'false' so the browser opens automatically
    is_headless = frontend_cfg.get('headless', False)
    headless = "true" if is_headless else "false"

    print("\n" + "=" * 55)
    print(" 😼 GemmaEdge Dashboard — Sovereign Launcher Active")
    print(f" 📡 Local URL: http://localhost:{port}")
    print("=" * 55 + "\n")

    # Launch the Streamlit subprocess and catch the shutdown gracefully
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "frontend/dashboard.py",  # Assumes a 'frontend' directory exists with 'dashboard.py' inside
            "--server.port", port,
            "--server.headless", headless
        ])
    except KeyboardInterrupt:
        print("\n[SYSTEM]: Dashboard closed by user (Ctrl+C). Sovereign Launcher deactivated. 😼")
        sys.exit(0)
