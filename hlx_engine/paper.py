from dataclasses import dataclass


@dataclass
class PaperTrade:
    symbol: str
    quantity: float
    entry_cost: float
    exit_proceeds: float
    fees: float

    @property
    def net_pnl(self) -> float:
        return self.exit_proceeds - self.entry_cost - self.fees


class PaperBroker:
    def __init__(self) -> None:
        self.trades: list[PaperTrade] = []

    def execute(self, symbol: str, quantity: float, entry_cost: float, exit_proceeds: float, fees: float) -> PaperTrade:
        trade = PaperTrade(symbol, quantity, entry_cost, exit_proceeds, fees)
        self.trades.append(trade)
        return trade
