"""
MCP Server for Iterative Self-Rewarding Prompt Synthesizer Skill.
"""

import json
import sys
from client import SelfRewardingJudge

JUDGE = SelfRewardingJudge()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "score_response",
                    "description": "Self-score agent response on 5-dimension rubric",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_prompt": {"type": "string"},
                            "agent_response": {"type": "string"},
                            "dimension_scores": {"type": "object"}
                        },
                        "required": ["user_prompt", "agent_response"]
                    }
                },
                {
                    "name": "synthesize_contrastive_variation",
                    "description": "Synthesize hard prompt variation for iterative training",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "base_prompt": {"type": "string"},
                            "defect_type": {"type": "string", "default": "ambiguity"}
                        },
                        "required": ["base_prompt"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "score_response":
            res = JUDGE.score_response(
                args["user_prompt"],
                args["agent_response"],
                args.get("dimension_scores")
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        elif tool_name == "synthesize_contrastive_variation":
            res = JUDGE.synthesize_contrastive_variation(
                args["base_prompt"],
                args.get("defect_type", "ambiguity")
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
