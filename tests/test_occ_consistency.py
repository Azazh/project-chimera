import pytest
from unittest.mock import Mock, patch

# Placeholder imports for your future OCC implementation.
from chimera.wallet import Wallet, ConsistencyError

def test_occ_race_condition():
    """
    Simulate two agents attempting to update the same wallet balance with the same version number.
    This test is critical: OCC prevents double-spending and ensures data integrity in distributed agent systems.
    """
    # Mock wallet with versioning
    wallet = Wallet(balance=100, version=1)

    # Agent 1 prepares update
    agent1_update = {"amount": -50, "version": 1}
    # Agent 2 prepares update (same version)
    agent2_update = {"amount": -30, "version": 1}

    # Agent 1 succeeds
    result1 = wallet.update_balance(**agent1_update)
    assert result1["new_version"] == 2
    assert wallet.balance == 50

    # Agent 2 should fail due to version conflict
    with pytest.raises(ConsistencyError):
        wallet.update_balance(**agent2_update)
