import os
import glob
import platform
import string


def get_drive_letters():
    """Detects all available drive letters (A-Z)."""
    drives = []
    for letter in string.ascii_uppercase:
        if os.path.exists(f"{letter}:\\"):
            drives.append(f"{letter}:\\")
    return drives


def find_nvml_pro_scanner():
    print("=" * 70)
    print("GEMMAEDGE — ADVANCED NVML DIAGNOSTIC & STABILITY ANALYZER")
    print("=" * 70)

    if platform.system() != "Windows":
        print("[-] This system is optimized for Windows environments.")
        return

    drives = get_drive_letters()

    # Strategic search patterns
    sub_paths = [
        "Windows\\System32",
        "Program Files\\NVIDIA Corporation\\NVSMI",
        "Windows\\System32\\DriverStore\\FileRepository\\nv_dispi*",
        "Program Files\\NVIDIA Corporation"
    ]

    found_locations = []

    for drive in drives:
        for sub in sub_paths:
            full_search_path = os.path.join(drive, sub)
            search_pattern = os.path.join(full_search_path, "nvml.dll")

            try:
                # Recursive search to ensure deep capture
                for match in glob.glob(search_pattern, recursive=True):
                    directory = os.path.dirname(match)
                    if directory not in found_locations:
                        found_locations.append(directory)
            except (PermissionError, OSError):
                continue

    if not found_locations:
        print("\n❌ CRITICAL: nvml.dll NOT FOUND. Verify NVIDIA drivers.")
        return

    print(f"✅ SCAN COMPLETE: {len(found_locations)} locations identified.\n")
    print("DETAILED SYSTEM REPORT:")
    print("-" * 70)

    recommended_path = None

    # Logic for ranking paths
    for i, path in enumerate(found_locations, 1):
        status = "[SCAN]"
        note = ""

        if "System32" in path and "DriverStore" not in path:
            status = "[STABLE]"
            note = "<- RECOMMENDED: Best for long-term stability. Permanent path."
            recommended_path = path
        elif "DriverStore" in path:
            status = "[RAW]"
            note = "<- Active driver package. Most up-to-date, but path changes on update."
            if not recommended_path:  # Fallback if System32 is missing
                recommended_path = path
        elif "NVSMI" in path:
            status = "[LEGACY]"
            note = "<- Legacy management path."

        print(f"{i}. {status} Path: {path}")
        if note:
            print(f"   INFO: {note}")

    # Final actionable output
    print("-" * 70)
    print("ACTIONABLE INTEGRATION:")
    print("Add this logic to your 'gpu_monitor.py' to fix DLL loading:")
    print("-" * 70)

    if recommended_path:
        print(f"import os")
        print(f"os.add_dll_directory(r\"{recommended_path}\")")
    else:
        print("# No stable path identified. Check manual locations above.")

    print("=" * 70)


if __name__ == "__main__":
    find_nvml_pro_scanner()