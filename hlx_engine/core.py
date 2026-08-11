from dataclasses import dataclass


@dataclass(frozen=True)
class Opportunity:
    symbol: str
    buy_price: float
    sell_price: float
    quantity: float
    buy_fee_rate: float
    sell_fee_rate: float
    slippage_rate: float = 0.0
    network_cost: float = 0.0
    latency_reserve: float = 0.0
    safety_reserve: float = 0.0

    @property
    def gross_pnl(self) -> float:
        return max(0.0, (self.sell_price - self.buy_price) * self.quantity)

    @property
    def trading_fees(self) -> float:
        return (self.buy_price * self.quantity * self.buy_fee_rate) + (
            self.sell_price * self.quantity * self.sell_fee_rate
        )

    @property
    def slippage_cost(self) -> float:
        notional = max(self.buy_price, self.sell_price) * self.quantity
        return notional * self.slippage_rate

    @property
    def estimated_net_pnl(self) -> float:
        return self.gross_pnl - self.trading_fees - self.slippage_cost - self.network_cost - self.latency_reserve - self.safety_reserve


def trade_is_profitable(opportunity: Opportunity, min_profit: float = 0.0, min_return_rate: float = 0.0) -> bool:
    """Hard gate: no execution unless estimated net P&L clears both thresholds."""
    if opportunity.estimated_net_pnl < min_profit:
        return False
    invested = opportunity.buy_price * opportunity.quantity
    if invested <= 0:
        return False
    return opportunity.estimated_net_pnl / invested >= min_return_rate
