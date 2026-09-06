"""
Example usage of Iterative Self-Rewarding Prompt Synthesizer Skill.
"""

from client import SelfRewardingJudge


def main():
    print("=== Iterative Self-Rewarding Prompt Synthesizer Demonstration ===")
    judge = SelfRewardingJudge()

    prompt = "Explain how Raft consensus handles network partitions."
    response = (
        "In Raft, when a network partition occurs, the cluster splits into two or more subsets. "
        "The partition containing a strict majority (quorum) continues to accept and commit log entries. "
        "The minority partition cannot elect a leader or commit entries. "
        "Upon partition recovery, the higher term leader reconciles the minority's stale state."
    )

    eval_result = judge.score_response(prompt, response)
    print("Aggregate Score:", eval_result["aggregate_score"], "/ 5.0")
    print("Normalized Score:", eval_result["normalized_score"])
    print("Acceptable Quality:", eval_result["is_acceptable"])
    print("Dimension Breakdown:")
    for dim, score in eval_result["dimension_scores"].items():
        print(f"  {dim:<18}: {score} / 5.0")

    # Synthesize hard contrastive prompt mutations for self-play training
    print("\n--- Contrastive Prompt Mutations ---")
    for defect in ["ambiguity", "adversarial_constraint", "missing_info"]:
        mut = judge.synthesize_contrastive_variation(prompt, defect)
        print(f"[{defect.upper()}]: {mut['mutated_prompt']}")


if __name__ == "__main__":
    main()
