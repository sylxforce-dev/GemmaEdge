import os
import psutil
import pynvml

# Point pynvml to correct dll location on Windows
os.add_dll_directory("C:\\Windows\\System32")

_nvml_initialized = False


def _init_nvml():
    global _nvml_initialized
    if not _nvml_initialized:
        try:
            pynvml.nvmlInit()
            _nvml_initialized = True
        except Exception as e:
            print(f"[TELEMETRY ERROR]: pynvml init failed: {e}")


def get_gpu_name() -> str:
    _init_nvml()
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        return pynvml.nvmlDeviceGetName(handle)
    except Exception:
        return "Unknown GPU"


def get_telemetry_data() -> dict:
    """
    Returns current GPU/CPU/RAM snapshot.
    Called by engine_starter, router, and API directly.
    """
    _init_nvml()
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

        # LISA: Reaalne GPU koormus (0-100%)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        gpu_load = util.gpu

        vram_used = mem.used / 1e9
        vram_total = mem.total / 1e9
    except Exception:
        vram_used = 0.0
        vram_total = 4.0
        temp = 0
        gpu_load = 0  # Fallback väärtus

    try:
        cpu_load = psutil.cpu_percent(interval=None)
        ram_used = psutil.virtual_memory().used / 1e9
    except Exception:
        cpu_load = 0
        ram_used = 0.0

    return {
        'vram_used': vram_used,
        'vram_total': vram_total,
        'gpu_temp': temp,
        'gpu_load': gpu_load,  # Nüüd on see siin olemas
        'cpu_load': cpu_load,
        'ram_used': ram_used
    }