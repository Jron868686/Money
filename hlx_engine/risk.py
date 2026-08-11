from dataclasses import dataclass
from time import time


@dataclass
class RiskLimits:
    max_trade_notional: float = 1000.0
    daily_loss_limit: float = 50.0
    max_concurrent_trades: int = 2
    max_drawdown: float = 100.0
    max_quote_age_ms: int = 1500


@dataclass
class RiskState:
    daily_pnl: float = 0.0
    drawdown: float = 0.0
    active_trades: int = 0
    kill_switch: bool = False


def allow_trade(notional: float, quote_age_ms: int, limits: RiskLimits, state: RiskState) -> tuple[bool, str]:
    if state.kill_switch:
        return False, "kill_switch"
    if notional > limits.max_trade_notional:
        return False, "trade_notional_limit"
    if quote_age_ms > limits.max_quote_age_ms:
        return False, "stale_quote"
    if state.active_trades >= limits.max_concurrent_trades:
        return False, "concurrency_limit"
    if state.daily_pnl <= -abs(limits.daily_loss_limit):
        return False, "daily_loss_limit"
    if state.drawdown >= limits.max_drawdown:
        return False, "drawdown_limit"
    return True, "approved"
