import os
import json
import yaml
import ollama
from sentence_transformers import SentenceTransformer, util


class MishaSelector:
    def __init__(self):
        """
        Darth Misha - Sovereign Hybrid Router v1.4
        Logic driven by external config.yaml with full asynchronous safety boundaries.
        """
        # 1. Load configuration from the YAML matrix
        self.config = self._load_config()

        # --- OFFLINE ENFORCEMENT ---
        if self.config.get('engine', {}).get('offline_mode', True):
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            os.environ['HF_DATASETS_OFFLINE'] = '1'

        # FIX: Start clean with None so the status endpoint tracks state accurately
        self.current_model = None

        # 2. Establish dynamic paths relative to the project root
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.matrix_path = os.path.join(self.base_path, self.config['router']['matrix_path'])
        self.matrix = self._load_matrix_from_json()

        # --- CONFIGURATION PARAMETERS ---
        self.THRESHOLD = self.config['router']['threshold']
        self.MAX_WEIGHT = self.config['router']['max_weight']
        self.MEAN_WEIGHT = self.config['router']['mean_weight']
        self.keep_alive = self.config['hardware']['keep_alive']

        print(f"\n[ROUTER]: Initializing Sovereign Engine (Threshold: {self.THRESHOLD})...")

        # 3. Initialize vector engine from the defined local path
        model_local_path = self.config['engine']['model_path']

        try:
            self.vector_engine = SentenceTransformer(
                model_local_path,
                device=self.config['engine'].get('device', 'cpu')
            )
        except Exception as e:
            print(f"⚠️ [ROUTER ERROR]: Configured model path failed: {e}")
            self.vector_engine = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

        self.encoded_matrix = self._pre_encode_matrix()
        print("[ROUTER]: System Ready. Sovereign Orchestration Active. 😼\n")

    def _load_config(self):
        """Loads config.yaml from the project root directory using strict paths."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_path, "config.yaml")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ [CONFIG ERROR]: Cannot load config.yaml: {e}")
            return {
                'router': {'threshold': 0.30, 'max_weight': 0.95, 'mean_weight': 0.05,
                           'matrix_path': 'router/personality_matrix.json'},
                'engine': {'model_path': 'all-MiniLM-L6-v2', 'device': 'cpu', 'offline_mode': True},
                'hardware': {'keep_alive': 0},
                'personalities': {'main_core': 'misha-maincore'}
            }

    def _load_matrix_from_json(self):
        """Retrieves personality matrix from the specified JSON source."""
        try:
            with open(self.matrix_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [ROUTER ERROR]: Matrix file not found at {self.matrix_path}")
            return {}

    def _pre_encode_matrix(self):
        """Encodes matrix keywords into vector tensors for similarity comparison."""
        encoded = {}
        for model, triggers in self.matrix.items():
            if model == "misha-maincore": 
                continue
            if triggers:
                encoded[model] = self.vector_engine.encode(triggers, convert_to_tensor=True)
        return encoded

    def select_personality(self, user_input):
        """Calculates hybrid similarity score and logs the decision-making process."""
        query_vec = self.vector_engine.encode(user_input, convert_to_tensor=True)
        scores = {}

        # OPTIMIZATION FIX: Run cos_sim exactly ONCE per module to prevent double compute waste
        for model, keyword_vecs in self.encoded_matrix.items():
            sim_tensor = util.cos_sim(query_vec, keyword_vecs)
            current_max = sim_tensor.max().item() * self.MAX_WEIGHT
            current_mean = sim_tensor.mean().item() * self.MEAN_WEIGHT
            scores[model] = current_max + current_mean

        # Find the highest hybrid scoring specialist
        best_match = max(scores, key=scores.get)
        score = scores[best_match]

        # LOGGING: Detailed telemetry of scores and selection before threshold validation
        print(f"[ROUTER]: Match: {best_match.upper()} | Score: {score:.4f} (Threshold: {self.THRESHOLD})")

        # THRESHOLD VALIDATION: Fallback to MAINCORE if similarity is insufficient
        if score >= self.THRESHOLD:
            clean_key = best_match.replace("misha-", "")
            target = self.config['personalities'].get(clean_key, self.config['personalities']['main_core'])
        else:
            print(f"[ROUTER]: Score below threshold. Falling back to default core.")
            target = self.config['personalities']['main_core']

        return self._handle_cold_swap(target)

    def _handle_cold_swap(self, target):
        """Executes model swap and applies hardware 'keep_alive' rules for VRAM management."""
        if target != self.current_model:
            # Only attempt memory flush if a model is actively loaded (skips cold boot step)
            if self.current_model:
                print(f"[ROUTER]: Swapping VRAM: {self.current_model.upper()} -> {target.upper()}")
                try:
                    # Apply keep_alive constraint (0 = immediate VRAM flush)
                    ollama.chat(
                        model=self.current_model,
                        messages=[],
                        keep_alive=self.keep_alive
                    )
                except Exception as e:
                    print(f"⚠️ [VRAM FLUSH ERROR]: Failed to purge {self.current_model}: {e}")
            else:
                print(f"[ROUTER]: Cold boot trace. Initializing runtime to: {target.upper()}")
            
            self.current_model = target
            
        return target
