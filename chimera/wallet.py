class ConsistencyError(Exception):
    pass


class Wallet:
    def __init__(self, balance: int, version: int):
        self.balance = balance
        self.version = version

    def update_balance(self, amount: int, version: int) -> dict:
        if version != self.version:
            raise ConsistencyError("version conflict")
        self.balance += amount
        self.version += 1
        return {"new_version": self.version}
