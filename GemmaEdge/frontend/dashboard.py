"""
dashboard.py — GemmaEdge Streamlit Dashboard (JS-Ghost Edition)
frontend/dashboard.py
"""

import streamlit as st
from frontend.styles import DASHBOARD_CSS
from frontend.helpers import init_session_state, fetch_status, send_prompt
from frontend.components import (
    render_status_bar,
    render_swap_log,
    render_chat,
    render_telemetry_bar,
    #render_architecture_map
)

# ─── PAGE CONFIG ──────────────────────────────────────────

st.set_page_config(
    page_title="GemmaEdge",
    page_icon="😼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── INIT ─────────────────────────────────────────────────

st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
init_session_state()

if "initial_sync" not in st.session_state:
    fetch_status()
    st.session_state.initial_sync = True

# ─── TOP STATUS BAR ───────────────────────────────────────

render_status_bar()

# ─── MAIN LAYOUT ──────────────────────────────────────────

left, right = st.columns([1, 2])

# ─── LEFT PANEL ───────────────────────────────────────────

with left:
    module_placeholder = st.empty()
    render_swap_log()

# ─── RIGHT PANEL ──────────────────────────────────────────

with right:
    render_chat()

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── REFACTOR: text_input replaced with text_area for extended prompt capacity ───
    user_input = st.text_area(
        "Prompt",
        placeholder="Enter your prompt here... (Shift+Enter to send)",
        label_visibility="collapsed",
        height=200,  # Optimized height for multi-line analysis and comparison
        key="input"
    )

    col1, col2 = st.columns([5, 1])
    with col1:
        # Maintaining layout structure
        pass
    with col2:
        send = st.button("SEND 😼", use_container_width=True)

    if send and user_input.strip():
        send_prompt(user_input.strip(), module_placeholder)

# ─── TELEMETRY BAR (The Ghost) ────────────────────────────
render_telemetry_bar()

# ─── ARCHITECTURE ANCHOR ──────────────────────────────────
# Rendered at the base level, following GPU/RAM metrics
#render_architecture_map()