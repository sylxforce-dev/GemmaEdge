import os
import json
import yaml
import ollama
from sentence_transformers import SentenceTransformer, util


class MishaSelector:
    def __init__(self):
        """
        Darth Misha - Sovereign Hybrid Router v1.4
        Logic driven by external config.yaml.
        """
        # 1. Load configuration from the YAML matrix
        self.config = self._load_config()

        # --- OFFLINE ENFORCEMENT ---
        if self.config.get('engine', {}).get('offline_mode', True):
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            os.environ['HF_DATASETS_OFFLINE'] = '1'

        # FIX: Start clean with None for accurate status endpoint telemetry tracking
        self.current_model = None

        # 2. Establish dynamic paths relative to the project root
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.matrix_path = os.path.join(base_path, self.config['router']['matrix_path'])
        self.matrix = self._load_matrix_from_json()

        # --- CONFIGURATION PARAMETERS ---
        self.THRESHOLD = self.config['router']['threshold']
        self.MAX_WEIGHT = self.config['router']['max_weight']
        self.MEAN_WEIGHT = self.config['router']['mean_weight']

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
        target = self.config['personalities']['main_core']
        highest_hybrid_score = 0.0
        query_vec = self.vector_engine.encode(user_input, convert_to_tensor=True)

        for model, keyword_vecs in self.encoded_matrix.items():
            # YOUR ORIGINAL MATH: Cosine similarity calculation
            scores = util.cos_sim(query_vec, keyword_vecs)
            current_max = scores.max().item()
            current_mean = scores.mean().item()

            # YOUR ORIGINAL MATH: Hybrid scoring logic based on YAML weights
            hybrid_score = (current_max * self.MAX_WEIGHT) + (current_mean * self.MEAN_WEIGHT)

            if hybrid_score > highest_hybrid_score:
                highest_hybrid_score = hybrid_score
                
                # Dynamic mapping to config names
                clean_key = model.replace("misha-", "")
                target = self.config['personalities'].get(clean_key, self.config['personalities']['main_core'])

        # LOGGING: Detailed telemetry of scores and selection before threshold validation
        print(f"[ROUTER]: Match: {target.upper()} | Score: {highest_hybrid_score:.4f} (Threshold: {self.THRESHOLD})")

        # THRESHOLD VALIDATION: Fallback to MAINCORE if similarity is insufficient
        if highest_hybrid_score < self.THRESHOLD:
            if target != self.config['personalities']['main_core']:
                print(f"[ROUTER]: Score below threshold. Falling back to MAINCORE.")
            target = self.config['personalities']['main_core']

        return self._handle_cold_swap(target)

    def _handle_cold_swap(self, target):
        """Executes model swap and applies hardware 'keep_alive' rules for VRAM management."""
        if target != self.current_model:
            # Only trigger memory purge routine if a model is actively initialized
            if self.current_model:
                print(f"[ROUTER]: Swapping VRAM: {self.current_model.upper()} -> {target.upper()}")
                try:
                    # Apply keep_alive constraint (0 = immediate VRAM flush)
                    ollama.chat(
                        model=self.current_model,
                        messages=[],
                        keep_alive=self.config['hardware']['keep_alive']
                    )
                except Exception as e:
                    print(f"⚠️ [VRAM FLUSH ERROR]: Failed to purge {self.current_model}: {e}")
            else:
                print(f"[ROUTER]: Cold boot trace. Initializing active runtime to: {target.upper()}")
            
            self.current_model = target
            
        return target
