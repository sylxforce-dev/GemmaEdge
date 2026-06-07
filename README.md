# ⚡ GemmaEdge: Local AI Reasoning Runtime (No Cloud, Full Control) 😼

**A modular, fully local AI reasoning system optimized for consumer hardware (GTX 1050 Ti class).**

GemmaEdge is a sovereignty-focused AI orchestration engine that runs multi-domain reasoning locally without cloud dependency, API costs, or external data leakage.

> **“Advanced AI is not defined by scale, but by how intelligently it adapts to constraints.”**

---

## 🚀 Overview

GemmaEdge is a local-first AI reasoning architecture designed to run multi-agent inference systems on constrained consumer hardware. The system is built around a custom semantic execution controller (**MishaSelector**) that manages routing, model selection, and VRAM lifecycle in real time.

---

## 🧠 Core Innovation: MishaSelector (Sovereign Inference Controller)

`MishaSelector` is not a classifier. It is a runtime-level inference orchestration engine responsible for semantic routing, model selection, VRAM lifecycle control, and execution stability under strict hardware constraints.

### ⚙️ Routing Pipeline
Use code with caution.USER INPUT│▼CPU EMBEDDING ENGINE (MiniLM-L6-v2)│▼PRE-ENCODED SEMANTIC MATRIX│▼HYBRID SCORING ENGINE (Max Similarity + Mean Distribution Weighting)│▼MODEL SELECTION DECISION│▼OLLAMA EXECUTION LAYER│▼VRAM COLD SWAP SYSTEM (keep_alive=0)
### 🔥 Key Technical Features
*   **Hybrid Semantic Scoring System:** Uses maximum cosine similarity and mean distribution signal for robust routing under ambiguity.
*   **Precomputed Semantic Decision Space:** Embeddings are precomputed at startup, turning routing into a static inference graph with deterministic latency.
*   **VRAM Cold Swap Controller:** Only one model exists in GPU memory at a time. The previous model is forcibly purged via `keep_alive=0`, preventing fragmentation and OOM issues.
*   **Deterministic Fallback Layer:** If confidence score is below the configured threshold, the system automatically falls back to MainCore to ensure stable, uninterrupted execution.

---

## 🏗️ System Architecture

┌────────────────────────┐│   USER PROMPT (CPU)    │└───────────┬────────────┘│[ misha_selector.py ] <── Offline MiniLM-L6-v2│┌──────────────┴──────────────┐▼ (Hybrid Score > Threshold)  ▼ (Fallback)┌─────────────────┐           ┌──────────────────┐│ SPECIALIST MOD  │           │ MISHA-MAINCORE   │└────────┬────────┘           └────────┬─────────┘│                             │└──────────────┬──────────────┘▼[ ollama chat swap ](keep_alive=0 -> Hard Purge VRAM)▼┌──────────────────┐│   GTX GPU VRAM   │└──────────────────┘
### 🧩 Specialist Modules (`Modelfiles`)
*   **`Misha_MainCore` (Gemma 4 E2B)** — General reasoning and core system orchestration fallback.
*   **`Misha_Social` (Gemma 4 E2B)** — Conversational adaptation layer and high-speed contextual smalltalk.
*   **`Misha_Reasoning` (Gemma 4 E2B)** — Transparent, deterministic logic execution with step-by-step reasoning chains.
*   **`Misha_Auditor` (Gemma 4 E2B)** — Structural validation, analysis, and strategic career/CV reframing.
*   **`Misha_Oracle` (Gemma 4 E2B)** — Asset strategist. Handles probability, logic mathematics, and game system RNG mechanics.
*   **`Misha_Sovereign` (Gemma 4 E2B)** — System governance, digital autonomy enforcement, and meta-level stability.

---

## ⚙️ Deployment

*   **Backend:** Ollama
*   **OS:** Windows / Linux
*   **GPU:** NVIDIA 4GB VRAM minimum tested
*   **Runtime:** Python 3.10+
*   **Config Structure:** `config.yaml`, `personality_matrix.json`, modular model files

### 💡 Advanced Note for Legacy Bare-Metal Compilation
While the main pipeline relies on Ollama for fast deployment, advanced developers who want to bypass the standard environment and compile/run directly via raw CUDA backends on legacy hardware will face severe Visual Studio/STL compatibility restrictions. A **Special Pascal CUDA Windows Compile Guide** is included in the repository documentation to bridge the MSBuild gaps specifically for the GTX 1050 Ti architecture.

---

## 🌍 Design Principles

*   **Sovereignty over dependency.**
*   **Architecture over brute force scaling.**
*   **Deterministic execution over randomness.**
*   **Local-first AI computation.**

---

## 🎯 Use Cases

*   🛰️ **Offline AI Systems:** Remote locations, air-gapped environments, or disaster zones.
*   🔐 **Privacy-Sensitive Workloads:** Secure local data processing with zero external API data leakage.
*   🔌 **Edge Computing:** Deployments on localized consumer hardware without a cloud connection.
*   🎓 **Democratizing AI Development:** Giving students and researchers a ready structural guide to build advanced multi-agent networks without a cloud budget.

---

## 🧠 Status

Active development (V1 system stable on legacy consumer hardware).

---

## 🔥 Summary

GemmaEdge is a local-first AI reasoning architecture built around a custom semantic execution controller (MishaSelector). It replaces traditional routing with a hybrid scoring inference engine that actively controls model selection, VRAM lifecycle, execution stability and semantic decision boundaries, enabling advanced multi-agent AI systems to run reliably on constrained consumer hardware without cloud dependency.

---
*Every module, every file, and every path is hardcoded with the signature of the 
