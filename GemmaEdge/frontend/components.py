"""
components.py — Reusable UI Components (Sovereign JS-Ghost Edition)
frontend/components.py
"""

import streamlit.components.v1 as components
import streamlit as st
import os
from frontend.helpers import get_module_color, get_module_desc


def render_status_bar():
    """Kuvab süsteemi üldise staatuse ja API ühenduse [cite: 2026-02-14]."""
    api_status = "🟢 Online" if st.session_state.get("api_online") else "🔴 Offline"
    st.markdown(f"""
    <div class="status-bar">
        😼 GemmaEdge &nbsp;|&nbsp; Engine: Ready &nbsp;|&nbsp; API: {api_status}
    </div>
    """, unsafe_allow_html=True)


def render_module_box():
    """Kuvab hetkel aktiivse Misha mooduli ja selle funktsiooni [cite: 2026-02-14]."""
    module = st.session_state.active_module
    color = get_module_color(module)
    desc = get_module_desc(module)
    st.markdown(f"""
    <div class="module-box" style="background:{color}22; border: 1px solid {color};">
        <div class="module-name" style="color:{color};">{module.upper().replace("-", " ")}</div>
        <div class="module-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def render_swap_log():
    """Logib kõik moodulite vahetused (Cold-Swaps) reaalajas [cite: 2026-02-14]."""
    st.markdown("**Swap Log**")
    swap_html = '<div class="swap-log">'

    if st.session_state.swap_log:
        for entry in st.session_state.swap_log:
            from_color = get_module_color(entry["from"])
            to_color = get_module_color(entry["to"])
            swap_html += f'''
            <div class="swap-entry">
                {entry["time"]} &nbsp;
                <span style="color:{from_color}">{entry["from"].replace("misha-", "")}</span>
                →
                <span style="color:{to_color}">{entry["to"].replace("misha-", "")}</span>
            </div>'''
    else:
        swap_html += '<div style="color:#444; padding:8px;">No swaps yet</div>'

    swap_html += '</div>'
    st.markdown(swap_html, unsafe_allow_html=True)


def render_chat():
    """Kuvab vestluse ajaloo koos inferentsi aja ja mudeli märgistusega [cite: 2026-02-14]."""
    for msg in st.session_state.messages:
        if msg["role"] == "op":
            st.markdown(
                f'<div class="op-message">[OP]: {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            color = get_module_color(msg.get("model", "misha-maincore"))
            st.markdown(
                f'<div class="misha-message" style="background:{color}22; border-left: 3px solid {color};">'
                f'MISHA: {msg["content"]}</div>'
                f'<div class="inference-time">{msg.get("model", "").upper()} | {msg.get("inference_time", 0):.2f}s</div>',
                unsafe_allow_html=True
            )


def render_telemetry_bar():
    """
    JS-Ghosti ankurpunkt reaalajas GPU telemeetria jaoks [cite: 2026-02-14].
    """
    js_path = os.path.join(os.path.dirname(__file__), "static", "telemetry.js")
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            # See on see muutuja, mida scripti sees kasutame
            telemetry_script = f.read()
    except FileNotFoundError:
        telemetry_script = "console.error('JS-GHOST: telemetry.js NOT FOUND');"

    components.html(
        f"""
        <style>
            html, body {{ 
                margin: 0; 
                padding: 0; 
                background: transparent !important; 
                overflow: hidden; 
            }}
            #telemetry-display {{
                background: rgba(13, 13, 13, 0.95);
                color: #39FF14;
                padding: 10px 20px;
                font-family: monospace;
                border-radius: 6px;
                border: 1px solid #444;
                display: flex;
                justify-content: space-around;
                align-items: center;
                min-height: 45px;
                position: relative;
                z-index: 9999;
            }}
        </style>
        <div id="telemetry-display">
            <span style="color:#555;">LINKING SOVEREIGN SCRIPT...</span>
        </div>
        <script>
            try {{
                {telemetry_script}
            }} catch (e) {{
                console.error("JS-GHOST CRASH:", e);
            }}
        </script>
        """,
        height=85,
        scrolling=False,
    )