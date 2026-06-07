# ⚡ GemmaEdge: Local AI Reasoning Runtime (No Cloud, Full Control) 😼

**A modular, fully local AI reasoning system optimized for consumer hardware (GTX 1050 Ti class).**

GemmaEdge is a lightweight, sovereignty-focused AI orchestration engine that enables multi-domain reasoning on constrained hardware without cloud dependency, API costs, or external data leakage.

> **“Advanced AI is not defined by scale, but by how intelligently it adapts to constraints.”**

---

## 🚀 Overview

GemmaEdge is a CPU-aware, VRAM-constrained multi-agent inference system designed for running local LLM workflows on low-end consumer GPUs.

It focuses on:
- Modular reasoning specialization
- CPU-based routing (no GPU overhead)
- Dynamic VRAM model swapping
- Fully offline execution

---

## 🏗️ Architecture (V1)


┌────────────────────────┐
│ USER PROMPT (CPU) │
└───────────┬────────────┘
│
▼
misha_selector.py
(MiniLM-L6-v2 CPU router)
│
semantic routing layer
┌─────┴─────┐
▼ ▼
SPECIALIST MAIN CORE
MODULES MODEL
│ │
└─────┬─────┘
▼
VRAM SINGLE MODEL SWAP
(keep_alive=0 purge)
▼
GPU EXECUTION


---

## ⚙️ Core Modules

- MainCore — general reasoning + orchestration
- Social — conversational adaptation layer
- Reasoning — deterministic logic engine
- Auditor — validation, CV, contract analysis
- Oracle — strategy + probability modeling
- Sovereign — system stability + identity layer

---

## 🧠 Key Technical Features

### CPU Semantic Router
- SentenceTransformer MiniLM-L6-v2
- Fully CPU execution
- Zero VRAM overhead
- Lightweight intent classification

---

### VRAM Cold Swap System
- One model in GPU memory at a time
- Hard purge before loading next model
- Prevents OOM and fragmentation
- Stable 4GB VRAM operation

---

### Telemetry Layer
- pynvml GPU monitoring
- VRAM + temperature tracking
- Real-time system metrics

---

## 🛠️ Deployment

Backend:
- Ollama runtime

Requirements:
- Windows / Linux
- NVIDIA GPU (4GB VRAM minimum tested)
- Python 3.10+

Config files:
- config.yaml
- personality_matrix.json

---

## 🌍 Design Principles

- Sovereignty over dependency
- Local-first execution
- Constraint-driven optimization
- Deterministic system behavior

---

## 🎯 Use Cases

- Offline AI systems
- Privacy-sensitive workloads
- Education / research environments
- Low-cost AI experimentation
- Edge computing setups

---

## 🧠 Status

Active development (V1 stable)

Planned improvements:
- Routing optimization
- Multi-instance execution
- Context compression layer
- Latency improvements

---

## 🔥 Summary

GemmaEdge is a local-first AI reasoning system designed to run advanced multi-agent workflows on constrained consumer hardware without cloud dependency.

It proves that architecture > brute force compute when constraints are tight.
