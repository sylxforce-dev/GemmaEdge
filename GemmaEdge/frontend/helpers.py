"""
helpers.py — State, Colors, API calls (Optimized for JS-Ghost)
frontend/helpers.py
"""

import time
import json
import requests
import streamlit as st

API_URL = "http://localhost:8000"

MODULE_COLORS = {
    "misha-maincore":  "#4A90D9",
    "misha-auditor":   "#27AE60",
    "misha-oracle":    "#8E44AD",
    "misha-social":    "#E67E22",
    "misha-reasoning": "#E74C3C",
    "misha-sovereign": "#F0C040",
}

MODULE_DESCRIPTIONS = {
    "misha-maincore":  "Sovereign reasoning — default intelligence layer",
    "misha-auditor":   "Career infiltration — CV, contracts, LinkedIn",
    "misha-oracle":    "Asset strategy — probability, RNG, gacha math",
    "misha-social":    "Aura guard — vibe, casual, human interface",
    "misha-reasoning": "Full reasoning chain — transparent logic visible",
    "misha-sovereign": "Presentation layer — identity, architecture, purpose",
}

def get_module_color(module: str) -> str:
    return MODULE_COLORS.get(module, "#444")

def get_module_desc(module: str) -> str:
    return MODULE_DESCRIPTIONS.get(module, "")

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "swap_log" not in st.session_state:
        st.session_state.swap_log = []
    if "active_module" not in st.session_state:
        st.session_state.active_module = "misha-maincore"
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "telemetry" not in st.session_state:
        st.session_state.telemetry = {
            "vram_used": 0.0,
            "vram_total": 4.3,
            "gpu_temp": 0,
            "gpu_load": 0,    # LISATUD: GPU load algväärtus
            "cpu_load": 0.0,
            "ram_used": 0.0,
        }
    if "api_online" not in st.session_state:
        st.session_state.api_online = False

def fetch_status():
    """
    Sünkroniseerib üldist olekut.
    JS-Ghost tegeleb reaalajas näidikutega, see funktsioon on vaid süsteemi 'ankurdamiseks'.
    """
    try:
        r = requests.get(f"{API_URL}/status", timeout=1)
        if r.status_code == 200:
            data = r.json()
            st.session_state.telemetry = data
            st.session_state.active_module = data["active_module"]
            st.session_state.api_online = True
    except Exception:
        st.session_state.api_online = False

def log_swap(from_module: str, to_module: str):
    if from_module != to_module:
        timestamp = time.strftime("%H:%M:%S")
        st.session_state.swap_log.insert(0, {
            "time": timestamp,
            "from": from_module,
            "to": to_module
        })
        if len(st.session_state.swap_log) > 10:
            st.session_state.swap_log.pop()

def send_prompt(prompt: str, module_placeholder=None):
    previous_module = st.session_state.active_module
    st.session_state.is_generating = True
    st.session_state.messages.append({"role": "op", "content": prompt})

    full_response = ""
    active_model = previous_module
    inference_time = 0.0

    def _render_module(module):
        if module_placeholder:
            color = get_module_color(module)
            desc = get_module_desc(module)
            module_placeholder.markdown(f"""
            <div class="module-box" style="background:{color}22; border: 1px solid {color};">
                <div class="module-name" style="color:{color};">{module.upper().replace("-", " ")}</div>
                <div class="module-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    _render_module(previous_module)

    try:
        # Stream=True hoiab Pythoni lõime kinni, aga JS-Ghost jookseb brauseris edasi
        with requests.post(f"{API_URL}/generate", json={"prompt": prompt}, stream=True, timeout=300) as r:
            response_placeholder = st.empty()

            for line in r.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        payload = json.loads(decoded[6:])

                        if payload["type"] == "module":
                            active_model = payload["model"]
                            log_swap(previous_module, active_model)
                            st.session_state.active_module = active_model
                            _render_module(active_model)

                        elif payload["type"] == "token":
                            full_response += payload["content"]
                            color = get_module_color(active_model)
                            response_placeholder.markdown(
                                f'<div class="misha-message" style="background:{color}22; border-left: 3px solid {color};">{full_response}▌</div>',
                                unsafe_allow_html=True
                            )

                        elif payload["type"] == "done":
                            inference_time = payload["inference_time"]
                            # Commit final state to session post-response (gpu_load integrated)
                            st.session_state.telemetry = payload
                            response_placeholder.empty()

    except Exception as e:
        full_response = f"[API ERROR]: {e}"

    st.session_state.messages.append({
        "role": "misha",
        "content": full_response,
        "model": active_model,
        "inference_time": inference_time
    })

    st.session_state.is_generating = False
    st.rerun()