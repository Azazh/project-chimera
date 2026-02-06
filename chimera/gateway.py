from .errors import SchemaViolation, DispatchError


class OpenClawGateway:
    def __init__(self, registry):
        self.registry = registry
        self._min_timeout_ms = 100

    def resolve_route(self, task_manifest: dict, input: dict) -> dict:
        skill = task_manifest.get("skill_required")
        idempotency_key = task_manifest.get("idempotency_key")
        timeout_ms = task_manifest.get("timeout_ms")

        if not idempotency_key or not isinstance(idempotency_key, str):
            raise SchemaViolation("idempotency_key is required")
        if not isinstance(timeout_ms, int) or timeout_ms < self._min_timeout_ms:
            raise SchemaViolation("timeout_ms below minimum")
        if not skill or not self.registry.is_known(skill):
            raise DispatchError("unknown skill")

        queue = self.registry.get_queue(skill)
        return {"queue": queue}
