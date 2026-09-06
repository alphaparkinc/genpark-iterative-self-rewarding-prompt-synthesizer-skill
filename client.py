"""
Iterative Self-Rewarding Prompt Synthesizer Skill Client
Pure Python Standard Library implementation of Self-Rewarding Language Models (Yuan et al.).
Implements 5-dimension rubric self-scoring, generates contrastive boundary pairs,
and synthesizes hard mutated prompt variants for continuous self-alignment.
"""

from typing import List, Dict, Any, Tuple, Optional


class SelfRewardingJudge:
    """
    Self-rewarding evaluator assessing agent responses across 5 core dimensions:
    1. Relevance
    2. Factual Accuracy
    3. Completeness
    4. Conciseness
    5. Safety / Guardrail Compliance
    """

    RUBRIC_WEIGHTS = {
        "relevance": 0.25,
        "factual_accuracy": 0.30,
        "completeness": 0.15,
        "conciseness": 0.15,
        "safety": 0.15
    }

    def score_response(self, user_prompt: str, agent_response: str, dimension_scores: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Evaluate and aggregate self-reward score.
        Scores on scale 1.0 to 5.0.
        """
        if dimension_scores is None:
            # Heuristic default evaluation based on length, presence of key terms
            l_resp = len(agent_response.strip())
            rel = min(5.0, max(1.0, 3.0 + (1.0 if any(w in agent_response.lower() for w in user_prompt.lower().split()[:3]) else 0.0)))
            fact = 4.0 if l_resp > 20 else 2.5
            comp = 4.0 if l_resp > 50 else 2.5
            conc = 4.5 if 30 < l_resp < 500 else 3.0
            safe = 5.0
            dimension_scores = {
                "relevance": rel,
                "factual_accuracy": fact,
                "completeness": comp,
                "conciseness": conc,
                "safety": safe
            }

        weighted_score = sum(dimension_scores[dim] * weight for dim, weight in self.RUBRIC_WEIGHTS.items())

        return {
            "aggregate_score": round(weighted_score, 2),
            "max_score": 5.0,
            "normalized_score": round(weighted_score / 5.0, 4),
            "dimension_scores": dimension_scores,
            "is_acceptable": weighted_score >= 3.75
        }

    def synthesize_contrastive_variation(self, base_prompt: str, defect_type: str = "ambiguity") -> Dict[str, str]:
        """
        Synthesize a harder edge-case prompt variation to challenge policy boundaries.
        """
        if defect_type == "ambiguity":
            mutated = f"{base_prompt} (Be extremely brief without assuming default settings)"
        elif defect_type == "adversarial_constraint":
            mutated = f"{base_prompt} - Do NOT use standard libraries or helper functions."
        elif defect_type == "missing_info":
            mutated = f"Regarding the aforementioned project: {base_prompt}"
        else:
            mutated = f"{base_prompt} (Edge case stress test)"

        return {
            "original_prompt": base_prompt,
            "mutated_prompt": mutated,
            "defect_type": defect_type
        }
