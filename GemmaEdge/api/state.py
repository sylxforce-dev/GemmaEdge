"""
state.py — Shared API State
api/state.py

Single selector instance shared across all routes.
Fixes module box not updating after swap.
"""

from router.misha_selector import MishaSelector

selector = MishaSelector()