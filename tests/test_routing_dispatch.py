import pytest

# Placeholder imports for future implementation.
from chimera.gateway import OpenClawGateway
from chimera.registry import SkillRegistry
from chimera.errors import SchemaViolation, DispatchError

# These tests are "ready to fail" and set goal posts for deterministic routing.

@pytest.fixture
def registry():
    # The registry will be backed by contracts in `skills/`.
    return SkillRegistry()

@pytest.fixture
def gateway(registry):
    return OpenClawGateway(registry=registry)


def test_deterministic_dispatch_to_correct_skill(gateway, registry):
    """
    Ensure that a Task Manifest with `skill_required = wallet_manager` is dispatched
    to the wallet_manager queue based on capability-discovery, not prompt guessing.

    Critical for governance: routing must be deterministic to avoid ghost updates
    and logic loops.
    """
    manifest = {
        "skill_required": "wallet_manager",
        "priority": "HIGH",
        "timeout_ms": 15000,
        "idempotency_key": "pay-20260205-abc123",
        "trace_id": "trace-xyz",
        "policy_version": "finance.v1"
    }

    input_payload = {"action": "payment", "amount": 25, "currency": "USDC", "to_address": "0x1234567890abcdef1234567890abcdef12345678"}

    # Expect: gateway chooses the wallet_manager worker queue.
    route = gateway.resolve_route(task_manifest=manifest, input=input_payload)
    assert route["queue"] == "wallet_manager"


def test_unknown_skill_rejected(gateway):
    """
    Unknown skills must be rejected instead of being misrouted.
    This prevents silent failures and maintains strong capability-discovery guarantees.
    """
    manifest = {
        "skill_required": "unknown_capability",
        "priority": "NORMAL",
        "timeout_ms": 10000,
        "idempotency_key": "idemp-xyz",
        "trace_id": "trace-abc",
        "policy_version": "policy.v1"
    }

    with pytest.raises(DispatchError):
        gateway.resolve_route(task_manifest=manifest, input={})


def test_manifest_schema_violation(gateway):
    """
    Missing idempotency_key or invalid timeout_ms must raise SchemaViolation.
    This enforces contract-first discipline for multi-agent orchestration.
    """
    invalid_manifest = {
        "skill_required": "trend_hunter",
        "priority": "NORMAL",
        # "idempotency_key": missing
        "timeout_ms": 50,  # below minimum
        "trace_id": "trace-abc",
        "policy_version": "policy.v1"
    }

    with pytest.raises(SchemaViolation):
        gateway.resolve_route(task_manifest=invalid_manifest, input={"query": "BTC"})
