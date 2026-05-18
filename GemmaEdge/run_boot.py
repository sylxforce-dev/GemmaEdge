"""
boot.py — LocalForge Master Entry Point
GemmaEdge | Run from project root: python boot.py
"""
import sys
import os

# Lisame juurkausta pathi, et importid töötaksid igal pool
sys.path.append(os.path.dirname(__file__))

from engine_starter.gates import run_boot_sequence

if __name__ == "__main__":
    run_boot_sequence()