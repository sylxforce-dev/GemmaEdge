"""
styles.py — Dashboard CSS
frontend/styles.py
"""

DASHBOARD_CSS = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    html, body, [class*="css"] {
        font-family: 'Courier New', monospace;
        background-color: #0D0D0D;
        color: #E0E0E0;
    }

    .status-bar {
        background: #1A1A1A;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 13px;
        color: #888;
        margin-bottom: 16px;
        letter-spacing: 0.5px;
    }

    .module-box {
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 12px;
        text-align: center;
    }

    .module-name {
        font-size: 22px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }

    .module-desc {
        font-size: 11px;
        color: #AAA;
        letter-spacing: 0.5px;
    }

    .swap-log {
        background: #1A1A1A;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 12px;
        font-size: 11px;
        color: #666;
        height: 180px;
        overflow-y: auto;
    }

    .swap-entry {
        padding: 4px 0;
        border-bottom: 1px solid #222;
        color: #888;
    }

    .op-message {
        background: #1A1A1A;
        border-left: 3px solid #444;
        border-radius: 4px;
        padding: 10px 14px;
        margin: 8px 0;
        font-size: 13px;
        color: #888;
    }

    .misha-message {
        border-radius: 4px;
        padding: 10px 14px;
        margin: 8px 0;
        font-size: 13px;
        line-height: 1.6;
    }

    .inference-time {
        font-size: 10px;
        color: #555;
        margin-top: 4px;
        text-align: right;
    }

    .telemetry-bar {
        background: #1A1A1A;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 12px;
        color: #666;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }

    .stTextInput input {
        background: #1A1A1A !important;
        border: 1px solid #333 !important;
        color: #E0E0E0 !important;
        border-radius: 6px !important;
        font-family: 'Courier New', monospace !important;
    }

    .stButton button {
        background: #222 !important;
        border: 1px solid #444 !important;
        color: #E0E0E0 !important;
        border-radius: 6px !important;
        font-family: 'Courier New', monospace !important;
        width: 100% !important;
    }

    .stButton button:hover {
        border-color: #888 !important;
        color: #FFF !important;
    }
</style>
"""