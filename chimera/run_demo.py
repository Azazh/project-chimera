from chimera.registry import SkillRegistry
from chimera.gateway import OpenClawGateway

if __name__ == "__main__":
    registry = SkillRegistry()
    gateway = OpenClawGateway(registry=registry)

    manifest = {
        "skill_required": "wallet_manager",
        "priority": "HIGH",
        "timeout_ms": 15000,
        "idempotency_key": "pay-20260207-demo",
        "trace_id": "trace-demo",
        "policy_version": "finance.v1"
    }
    input_payload = {"action": "payment", "amount": 25, "currency": "USDC", "to_address": "0x1234567890abcdef1234567890abcdef12345678"}

    route = gateway.resolve_route(task_manifest=manifest, input=input_payload)
    print("Demo route:", route)
