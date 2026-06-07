# ⚡ GemmaEdge: Local AI Reasoning Runtime (No Cloud, Full Control) 😼

[![Version](https://shields.io)]()
[![Hardware](https://shields.io)]()
[![Sovereignty](https://shields.io)]()

**A modular, fully local AI reasoning system optimized for consumer hardware (GTX 1050 Ti class).**

GemmaEdge is a lightweight, sovereignty-focused AI orchestration engine that enables multi-domain reasoning on constrained hardware without cloud dependency, API costs, or external data leakage.

> **“Advanced AI is not defined by scale, but by how intelligently it adapts to constraints. The constraint is not the story. The engineering born from it is.”**

---

## ⚡ The Gemma 4 Good Hackathon Writeup (May 18, 2026)

### What I Built
I developed **GemmaEdge**, a sovereign local AI orchestration system powered by **Gemma 4**. Built solo in 15 days, the system is engineered as a 6-module specialist reasoning engine that runs entirely on consumer-grade legacy hardware—specifically an NVIDIA GTX 1050 Ti (4GB VRAM) from 2016. By treating extreme hardware limitations as a core design requirement, I built a professional reasoning environment that requires zero cloud dependency, no API subscriptions, and ensures absolute data sovereignty.

---

## 🏗️ Core Architecture (V1 Ecosystem)

GemmaEdge separates reasoning into specialized execution roles to reduce context contamination and maximize efficiency under strict memory constraints. The system runs fully optimized for the **Gemma 4 E2B** model running locally under strict 4GB constraints:

Use code with caution.┌────────────────────────┐│   USER PROMPT (CPU)    │└───────────┬────────────┘│[ misha_selector.py ] <── Offline MiniLM-L6-v2│┌──────────────┴──────────────┐▼ (Hybrid Score > Threshold)  ▼ (Fallback)┌─────────────────┐           ┌──────────────────┐│ SPECIALIST MOD  │           │ MISHA-MAINCORE   │└────────┬────────┘           └────────┬─────────┘│                             │└──────────────┬──────────────┘▼[ ollama chat swap ](keep_alive=0 -> Hard Purge VRAM)▼┌──────────────────┐│   GTX GPU VRAM   │└──────────────────┘
### The Specialist Squad (`Modelfiles`)
*   **`Misha_MainCore` (Gemma 4 E2B)** — The default general reasoning and static routing layer.
*   **`Misha_Social` (Gemma 4 E2B)** — Manages contextual, human-like interaction and high-speed smalltalk utilizing full **128K context window symmetry**. Warm but sharp, like a Maine Coon in tactical armor.
*   **`Misha_Reasoning` (Gemma 4 E2B)** — Transparent logic engine enforcing visible, step-by-step reasoning chains with deterministic precision (`temperature 0.3`).
*   **`Misha_Auditor` (Gemma 4 E2B)** — Specialized in career, CV, and contract analysis, shifting skills from task-based into systemic architecture.
*   **`Misha_Oracle` (Gemma 4 E2B)** — Asset strategist. Handles probability, logic mathematics, failstacks (BDO/Genshin pity), and blocks impulsive FOMO decisions via `FOMO_REQUIRES_INTERNAL_SEAL™`.
*   **`Misha_Sovereign` (Gemma 4 E2B)** — Maintains system identity, digital autonomy guidelines, and meta-level stability.

---

## ⚙️ Key Technical Innovations

### 1. MishaSelector: CPU-Based Semantic Routing (Zero VRAM Cost)
To protect precious VRAM, `misha_selector.py` isolates the semantic routing logic entirely on the **CPU** using a lightweight, offline `SentenceTransformer('all-MiniLM-L6-v2')`.
- **Hybrid Scoring Matrix:** It calculates similarity using a unique matrix combining `MAX_WEIGHT` and `MEAN_WEIGHT` to capture both precise keyword matches and overall contextual intent.
- **Hardware Isolation:** Zero GPU overhead. 100% of VRAM remains allocated to the executing Gemma 4 E2B model.

### 2. Cold-Swap Memory Logic (`keep_alive=0`)
Instead of forcing multiple models to sit concurrently in VRAM (causing Instant Out-Of-Memory crashes), GemmaEdge uses an aggressive **asynchronous single-prompt memory swap**:
- Only one model is loaded at a time.
- When a new domain is detected by the router, a hard flush is triggered by sending an empty request with `keep_alive: 0`.
- The previous model is instantly purged from VRAM in milliseconds, allowing the next specialized **Gemma 4 E2B** file to load fresh into bare metal without memory fragmentation.

### 3. Real-Time Telemetry Bridge
The engine implements low-latency hardware monitoring via `pynvml` using direct `nvml.dll` mapping. This ensures deterministic runtime monitoring (GPU Temp, VRAM ceiling, load) directly on Windows-native deployments.

---

## 🛠️ Deployment & Execution Environment

The entire core system is engineered to run out-of-the-box using **Ollama** as the backend engine. This provides an immediate, zero-friction setup to rotate specialized, lightweight `Modelfiles` seamlessly on consumer hardware. You can swap any GGUF model, tune the routing matrix via `personality_matrix.json`, and lock hardware limits in one master `config.yaml`.

### 💡 Advanced Note for Legacy Bare-Metal Compilation
While the main pipeline relies on Ollama for fast deployment, advanced developers who want to bypass the standard environment and compile/run directly via raw CUDA backends on legacy hardware will face severe Visual Studio/STL compatibility restrictions. 

For those environments, a **Special Pascal CUDA Windows Compile Guide** is included in the repository documentation to bridge the MSBuild gaps specifically for the GTX 1050 Ti architecture.

---

## 🌍 Value & Global Impact: Digital Equity

Most AI systems today require heavy cloud APIs, corporate subscriptions, or high-end enterprise hardware. **GemmaEdge proves that advanced local AI orchestration runs on legacy hardware available globally for under $100.**

It serves as critical architecture for:
- 🛰️ **Disaster Response & Remote Areas:** Total operation where internet connectivity is destroyed or non-existent.
- 🔐 **Absolute Data Sovereignty:** Processing sensitive financial, career, or architectural data with 100% privacy — no bytes ever leave the machine.
- 🎓 **Democratizing AI Development:** Giving students and indie builders a clear, structural path to build advanced, multi-agent networks without a cloud budget.

---

## 🧠 Roadmap & Future Architecture
- **V2 Evolution:** Transitioning system parameters to scale seamlessly on upgraded consumer GPUs (RTX 5060 Ti class) with context compression.
- **V4 Horizon:** Integration of a local `FAISS` Vector index running on a dedicated RAM-Extension Bus for persistent context preservation.

---
*Every module, every file, and every path is hardcoded with the signature of the 
