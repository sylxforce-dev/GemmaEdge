"""
misha_selector.py — Sovereign Hybrid Router v1.4 (Score-Logging Enabled)
router/misha_selector.py
"""

import os
import json
import ollama
import torch
import yaml
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
        if self.config['engine']['offline_mode']:
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            os.environ['HF_DATASETS_OFFLINE'] = '1'

        self.current_model = "misha-maincore"

        # 2. Establish dynamic paths relative to the project root
        base_path = os.path.dirname(os.path.dirname(__file__))
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
                device=self.config['engine']['device']
            )
        except Exception as e:
            print(f"⚠️ [ROUTER ERROR]: Configured model path failed: {e}")
            self.vector_engine = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

        self.encoded_matrix = self._pre_encode_matrix()
        print("[ROUTER]: System Ready. Sovereign Orchestration Active. 😼\n")

    def _load_config(self):
        """Loads config.yaml from the project root directory."""
        base_path = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(base_path, "config.yaml")
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ [CONFIG ERROR]: Cannot load config.yaml: {e}")
            return {
                'router': {'threshold': 0.40, 'max_weight': 0.95, 'mean_weight': 0.05,
                           'matrix_path': 'router/personality_matrix.json'},
                'engine': {'model_path': 'all-MiniLM-L6-v2', 'device': 'cpu', 'offline_mode': True},
                'hardware': {'keep_alive': 0}
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
            if model == "misha-maincore": continue
            if triggers:
                encoded[model] = self.vector_engine.encode(triggers, convert_to_tensor=True)
        return encoded

    def select_personality(self, user_input):
        """Calculates hybrid similarity score and logs the decision-making process."""
        target = "misha-maincore"
        highest_hybrid_score = 0.0
        query_vec = self.vector_engine.encode(user_input, convert_to_tensor=True)

        for model, keyword_vecs in self.encoded_matrix.items():
            # Cosine similarity calculation
            scores = util.cos_sim(query_vec, keyword_vecs)
            current_max = scores.max().item()
            current_mean = scores.mean().item()

            # Hybrid scoring logic based on YAML weights
            hybrid_score = (current_max * self.MAX_WEIGHT) + (current_mean * self.MEAN_WEIGHT)

            if hybrid_score > highest_hybrid_score:
                highest_hybrid_score = hybrid_score
                target = model

        # LOGGING: Detailed telemetry of scores and selection before threshold validation
        print(f"[ROUTER]: Match: {target.upper()} | Score: {highest_hybrid_score:.4f} (Threshold: {self.THRESHOLD})")

        # THRESHOLD VALIDATION: Fallback to MAINCORE if similarity is insufficient
        if highest_hybrid_score < self.THRESHOLD:
            if target != "misha-maincore":
                print(f"[ROUTER]: Score below threshold. Falling back to MAINCORE.")
            target = "misha-maincore"

        return self._handle_cold_swap(target)

    def _handle_cold_swap(self, target):
        """Executes model swap and applies hardware 'keep_alive' rules for VRAM management."""
        if target != self.current_model:
            try:
                # Apply keep_alive constraint (0 = immediate VRAM flush)
                ollama.chat(
                    model=self.current_model,
                    messages=[],
                    keep_alive=self.config['hardware']['keep_alive']
                )
            except:
                pass
            self.current_model = target
        return target