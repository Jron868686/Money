from fastapi import FastAPI
from pydantic import BaseModel, Field

from .core import Opportunity, trade_is_profitable

app = FastAPI(title="HLX Arbitrage Engine", version="0.1.0")


class OpportunityRequest(BaseModel):
    symbol: str
    buy_price: float = Field(gt=0)
    sell_price: float = Field(gt=0)
    quantity: float = Field(gt=0)
    buy_fee_rate: float = Field(ge=0)
    sell_fee_rate: float = Field(ge=0)
    slippage_rate: float = Field(ge=0)
    network_cost: float = Field(ge=0)
    latency_reserve: float = Field(ge=0)
    safety_reserve: float = Field(ge=0)
    min_profit: float = 0.0
    min_return_rate: float = 0.0


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": "paper", "live_trading": False}


@app.post("/v1/opportunity/evaluate")
def evaluate(request: OpportunityRequest) -> dict:
    opportunity = Opportunity(**request.model_dump(exclude={"min_profit", "min_return_rate"}))
    return {
        "symbol": opportunity.symbol,
        "gross_pnl": opportunity.gross_pnl,
        "trading_fees": opportunity.trading_fees,
        "slippage_cost": opportunity.slippage_cost,
        "network_cost": opportunity.network_cost,
        "latency_reserve": opportunity.latency_reserve,
        "safety_reserve": opportunity.safety_reserve,
        "estimated_net_pnl": opportunity.estimated_net_pnl,
        "execute": trade_is_profitable(opportunity, request.min_profit, request.min_return_rate),
    }
