import os
import uvicorn
import yaml

def load_sovereign_config():
    """Reads the master configuration matrix."""
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ [CRITICAL ERROR]: {config_path} not found in root!")
        exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    cfg = load_sovereign_config()

    # Otseteed sektsioonidele puhtamaks lugemiseks
    api_cfg = cfg['api']
    log_cfg = cfg['logging']

    host = api_cfg['host']
    port = api_cfg['port']
    reload_mode = api_cfg['reload']
    log_level = log_cfg['log_level']
    
    # Uvicorn ei luba reload=True puhul mitut workerit. Sunnime reegli peale.
    workers = 1 if reload_mode else api_cfg['workers']

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
        log_level=log_level.lower(),
        access_log=True
    )
