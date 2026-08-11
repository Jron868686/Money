# HLX Arbitrage Engine

Fee-aware Python arbitrage research and execution platform.

## Safety first

The engine defaults to paper trading. It does not guarantee profit and must not enter a trade unless estimated net profit clears configurable thresholds after fees, slippage, gas/network costs, spread, latency risk, and a safety reserve.

## Core components

- Multi-venue market data and order-book monitoring
- Cross-venue and triangular arbitrage opportunity detection
- Executable-fill and depth-aware cost modeling
- Net-profit gate and configurable minimum edge
- Paper trading and backtesting
- Risk limits, circuit breakers, stale-quote protection, and kill switch
- Performance attribution and execution analytics
- Bounded, versioned self-improvement based on out-of-sample results
- Pluggable live venue adapters
- Dashboard/API layer

Live trading should remain disabled until venue credentials, permissions, risk limits, and independent testing have been reviewed.
