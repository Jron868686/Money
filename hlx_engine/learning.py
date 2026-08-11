from dataclasses import dataclass


@dataclass
class StrategyVersion:
    version: int
    min_profit: float
    min_return_rate: float
    sample_size: int = 0
    net_pnl: float = 0.0
    wins: int = 0


class BoundedLearner:
    """Adjusts thresholds only inside configured bounds; no unconstrained self-modification."""

    def __init__(self) -> None:
        self.current = StrategyVersion(1, 1.0, 0.001)

    def observe(self, net_pnl: float) -> None:
        self.current.sample_size += 1
        self.current.net_pnl += net_pnl
        self.current.wins += int(net_pnl > 0)

    def propose(self) -> StrategyVersion:
        if self.current.sample_size < 50:
            return self.current
        win_rate = self.current.wins / self.current.sample_size
        # Conservative bounded adaptation based on observed paper performance.
        new_min = min(10.0, max(0.50, self.current.min_profit * (1.05 if win_rate < 0.55 else 0.98)))
        new_rate = min(0.01, max(0.0005, self.current.min_return_rate * (1.05 if win_rate < 0.55 else 0.98)))
        return StrategyVersion(self.current.version + 1, new_min, new_rate)
