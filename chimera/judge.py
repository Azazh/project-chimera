class JudgeAgent:
    def evaluate_post(self, post: dict) -> dict:
        content = (post.get("content") or "").lower()
        persona = post.get("persona") or ""
        risk_flags = post.get("risk_flags") or []

        if "[system" in content or "prompt injection" in content:
            return {
                "status": "REJECTED",
                "reason": "prompt injection detected",
                "score": 0.0,
            }

        enthusiastic_markers = ["excited", "🚀", "thrilled", "so happy"]
        is_enthusiastic = any(m in content for m in enthusiastic_markers)

        if persona == "enthusiastic" and not risk_flags and is_enthusiastic:
            return {
                "status": "APPROVED",
                "score": 0.95,
            }

        if persona == "enthusiastic" and not is_enthusiastic:
            return {
                "status": "REMEDIATION",
                "score": 0.5,
                "remediation_delta": {
                    "feedback": "tone should be enthusiastic",
                },
            }

        return {
            "status": "REVIEW",
            "score": 0.5,
        }
