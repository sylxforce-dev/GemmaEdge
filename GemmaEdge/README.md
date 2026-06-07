# GEMMAEDGE V1.4 — SOVEREIGN SETUP & TROUBLESHOOTING GUIDE

**Project:** GemmaEdge (Local AI Reasoning Engine)  
**Hardware Target:** NVIDIA GPU Only (GTX 1050 Ti 4GB Optimized via Ollama)  
**Environment Target:** Windows Native Architecture Only (Requires Win DLL Paths)  
**Base Logic:** Reasoning over Reflex™

---

### PRE-REQUISITES (Install Ollama First)

GemmaEdge relies on Ollama to host and serve the partitioned model variants locally.

1. Download and install **Ollama for Windows** from the official site: [ollama.com](https://ollama.com)
2. Run the installer and ensure Ollama is running in your Windows system tray.
3. Open a fresh command prompt (`cmd`) and verify the installation:
   ```cmd
   ollama --version
   ```

---

### 0. ENVIRONMENT SETUP (The Isolated Base)

To prevent library conflicts and "Dependency Drift," ALWAYS use a Virtual Environment (venv).

#### Create Environment
```cmd
python -m venv .venv
```

#### Activate Environment
* **Windows:** `.venv\Scripts\activate`
* **Linux/Mac:** `source .venv/bin/activate`

#### Project Requirements File
Create a `requirements.txt` file in your project root with the following standard packages:

```text
# requirements.txt
torch==2.3.1
sentence-transformers==3.0.1
streamlit==1.35.0
fastapi==0.111.0
uvicorn==0.30.1
pyyaml==6.0.1
pydantic==2.7.2
```

#### Install Dependencies
```cmd
pip install -r requirements.txt
```

---

### 1. DIAGNOSTIC TOOLS (The Safety Net)

Before starting the engine, use the `guide_scripts/` to verify your environment alignment. This prevents setup configuration errors.

#### Step A: Verify Core Support
* Run `python guide_scripts/check_system.py`
* Checks `.venv` activation status and validates Python dependencies.

#### Step B: Locate DLL Path
* Run `python guide_scripts/find_nvml_auto.py`
* Locates `nvml.dll` dynamically for GPU telemetries.
* **Expected:** `Found nvml.dll at C:\Windows\System32\nvml.dll`

#### Step C: Test Telemetry Bridge
* Run `python guide_scripts/test_nvml_link.py`
* Confirms Python-to-GPU link for monitoring memory states during swaps.
* **Expected:** `GPU Telemetry Active | VRAM: X.XX GB | Temp: XX C`

---

### 🛑 2. CONFIGURATION BARRIER (UPDATE config.yaml)

⚠️ **CRITICAL STEP:** Do not execute any further terminal commands or compilation scripts until you complete this step. The engine cannot automatically detect where your files are stored. You MUST define your local paths first.

Open the `config.yaml` file in your project root using any text editor and update the following configuration rules:

```yaml
router:
  threshold: 0.30
  max_weight: 0.95
  mean_weight: 0.05
  matrix_path: "router/personality_matrix.json"

personalities:
  main_core: "misha-maincore"
  sovereign: "misha-sovereign"
  reasoning: "misha-reasoning"
  auditor: "misha-auditor"
  social: "misha-social"
  oracle: "misha-oracle"

engine:
  model_path: "C:\\Users\\YourUsername\\.cache\(\huggingface\hub\models--\)sentence-transformers--all-MiniLM-L6-v2\\snapshots\\1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
  device: "cpu"
  offline_mode: true

hardware:
  keep_alive: 0 # Cold-Swap value

api:
  host: "127.0.0.1"
  port: 8000

frontend:
  port: 8501
```
Save the `config.yaml` file and proceed below.

---

### 3. STARTUP SEQUENCE (Strict Hierarchy)

The system must be started in this specific order.

#### STEP 1: DOWNLOAD THE BASE MODEL (one time only)
GemmaEdge runs on Gemma 4 2B in GGUF format (Q4_K_M quantization). Download the model file from HuggingFace:
* **Model:** `gemma-4-E2B-it-Q4_K_M.gguf`
* **Source:** `unsloth/gemma-4-E2B-it-GGUF`
* **Destination:** Place the file inside your project's `engineModels` folder.

⚠️ **NOTE:** You can swap any compatible GGUF model here. Update the filename in each Modelfile if you use a different model: `FROM "./your-model-name.gguf"`. This is the framework's model-agnostic design — use what fits your hardware.

#### STEP 2: COMPILE THE MODELFILES (one time only)
Each specialist module is compiled from its Modelfile.

##### 💡 HOW TO NAVIGATE IN WINDOWS CMD
Navigate to your project's `engineModels` folder in CMD. If your project is on a different drive, change the drive letter first:
```cmd
X:
cd your-project-folder\engineModels
```
*(Replace `X:` with your actual drive letter and `your-project-folder` with your actual path.)*

##### 🚀 QUICK COMPILE LIST (Copy & Paste)
Once inside the `engineModels` folder, paste this block to compile all 6 modules:
```cmd
ollama create misha-maincore   -f Misha_MainCore.Modelfile
ollama create misha-auditor    -f Misha_Auditor.Modelfile
ollama create misha-oracle     -f Misha_Oracle.Modelfile
ollama create misha-social     -f Misha_Social.Modelfile
ollama create misha-reasoning  -f Misha_Reasoning.Modelfile
ollama create misha-sovereign  -f Misha_Sovereign.Modelfile
```

Verify all 6 are compiled:
```cmd
ollama list
```
* **Expected:** All 6 `misha-*` models appear in the list.

#### STEP 3: BOOT THE SYSTEM
Open 3 separate terminals and run each command in its own terminal, in this order:

* **Terminal 1 — Backend API**
  ```cmd
  python run_api.py
  ```
* **Terminal 2 — Frontend Dashboard**
  ```cmd
  streamlit run run_dashboard.py
  ```
* **Network Targets:**
  * Dashboard: http://127.0.0.1:8501
  * API Endpoint: http://127.0.0.1:8000

---

### SWAP YOUR OWN MODEL
GemmaEdge is model-agnostic. To use a different GGUF model:
1. Place your GGUF file in your project's `engineModels` folder.
2. Edit each Modelfile — change the FROM line:
   ```dockerfile
   FROM "./your-model-name.gguf"
   ```
3. Navigate to the `engineModels` folder in CMD:
   ```cmd
   X:
   cd your-project-folder\engineModels
   ```
4. Recompile all 6 modules:
   ```cmd
   ollama create misha-maincore   -f Misha_MainCore.Modelfile
   ollama create misha-auditor    -f Misha_Auditor.Modelfile
   ollama create misha-oracle     -f Misha_Oracle.Modelfile
   ollama create misha-social     -f Misha_Social.Modelfile
   ollama create misha-reasoning  -f Misha_Reasoning.Modelfile
   ```
5. Boot normally — follow STEP 3 above.

The routing, cold-swap, and telemetry all work the same regardless of which model you use.

---

### TUNE THE ROUTER
All routing sensitivity is controlled in `config.yaml`:
```yaml
router:
  threshold: 0.40      # <- lower = more aggressive routing
  max_weight: 0.95
  mean_weight: 0.05
```
* All routing keywords are in: `router/personality_matrix.json`
* Edit the JSON to add your own routing triggers per module. No code changes required.

---

> "The constraint is the point. Structure is the cure."  
> — *Misha Sovereign*
