import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from router.misha_functions import call_misha_stream
from api.state import selector
from telemetry.gpu_monitor import get_telemetry_data
from telemetry.runtime_monitor import start_runtime_monitor, stop_runtime_monitor
from api.models.schemas import PromptRequest

router = APIRouter()

@router.post("/generate")
def generate(request: PromptRequest):
    def event_stream():
        # 1. Mooduli tuvastamine ja isiksuse valik
        active_model = selector.select_personality(request.prompt)

        print(f"[API ROUTER]: Prompt received → '{request.prompt}'")
        print(f"[API ROUTER]: Routed to → {active_model}")

        # Teavitame frontendi valitud moodulist kohe alguses
        yield f"data: {json.dumps({'type': 'module', 'model': active_model})}\n\n"

        # 2. Seire käivitamine ja striimi algus
        start_time = start_runtime_monitor()
        stream = call_misha_stream(request.prompt, active_model)

        if stream:
            for chunk in stream:
                # Eeldame, et chunk järgib standardset sõnumistruktuuri
                token = chunk.get("message", {}).get("content", "")
                if token:
                    # Saadame märgi (token) otse JS-Ghostile
                    yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

        # 3. Sessiooni lõpetamine ja telemeetria koondamine
        inference_time = stop_runtime_monitor(start_time)
        data = get_telemetry_data()

        # Logime tulemuse serveri konsooli - LISATUD: LOAD
        print(f"[API DONE]: {active_model} | {inference_time:.2f}s | LOAD: {data['gpu_load']}% | VRAM: {round(data['vram_used'], 2)}GB")

        # Saadame lõplikud andmed (Final Handshake) - LISATUD: gpu_load
        yield f"data: {json.dumps({
            'type': 'done',
            'model': active_model,
            'inference_time': round(inference_time, 2),
            'vram_used': round(data['vram_used'], 2),
            'vram_total': round(data['vram_total'], 2),
            'gpu_temp': data['gpu_temp'],
            'gpu_load': data['gpu_load'],
            'cpu_load': round(data['cpu_load'], 2),
            'ram_used': round(data['ram_used'], 2)
        })}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")