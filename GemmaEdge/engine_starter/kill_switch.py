import os
import yaml
import ollama

def _get_personalities():
    """Loeb isikupärad otse config.yaml failist."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, "config.yaml")
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
        return list(cfg.get('personalities', {}).values())

def kill_misha_runtime():
    print("\n" + "=" * 45)
    print("😼 Kill Switch Active: Releasing VRAM...")

    try:
        models = _get_personalities()
        for model_name in models:
            print(f"  -> Purging {model_name}...")
            ollama.chat(model=model_name, messages=[], keep_alive=0)
        print("✅ VRAM released. Graceful exit.")

    except Exception as e:
        print(f"⚠️ API error: {e}. Using forced kill...")
        os.system("taskkill /IM ollama.exe /F >nul 2>&1")
        print("💀 Ollama.exe stopped.")

    print("=" * 45)