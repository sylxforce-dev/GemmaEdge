import torch
import sys
import os


def check_sovereign_status():
    print("=== GEMMAEDGE SYSTEM CHECK ===")

    # 1. Python & Venv Check
    is_venv = sys.prefix != sys.base_prefix
    print(f"[SYSTEM] Python Version: {sys.version.split()[0]}")
    print(f"[SYSTEM] Virtual Environment Active: {'YES' if is_venv else 'NO (CRITICAL ERROR)'}")

    # 2. CUDA Check (The Engine)
    cuda_available = torch.cuda.is_available()
    print(f"[HARDWARE] CUDA Available: {'YES' if cuda_available else 'NO (CPU ONLY - SLOW)'}")

    if cuda_available:
        print(f"[HARDWARE] GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"[HARDWARE] CUDA Version (Torch): {torch.version.cuda}")
        print(f"[HARDWARE] Current VRAM Usage: {torch.cuda.memory_allocated(0) / 1024 ** 2:.2f} MB")
    else:
        print("[WARNING] System is running on CPU. Check your '--index-url' in requirements.txt!")

    # 3. Path Anchor Check
    print(f"[PATH] Current Directory: {os.getcwd()}")

    print("===============================")


if __name__ == "__main__":
    check_sovereign_status()