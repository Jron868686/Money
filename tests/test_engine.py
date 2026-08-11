from hlx_engine.core import Opportunity, trade_is_profitable
from hlx_engine.market import Level, OrderBook, executable_buy_cost, executable_sell_proceeds
from hlx_engine.risk import RiskLimits, RiskState, allow_trade


def test_fees_can_turn_gross_edge_into_loss():
    op = Opportunity("BTC", 100, 101, 1, 0.01, 0.01)
    assert op.gross_pnl == 1
    assert op.estimated_net_pnl < 0
    assert not trade_is_profitable(op, 0, 0)


def test_orderbook_depth_is_used():
    book = OrderBook("A", "BTC", (Level(99, 2),), (Level(100, 1), Level(101, 2)), 1)
    assert executable_buy_cost(book, 2) == 201
    assert executable_sell_proceeds(book, 1) == 99


def test_risk_blocks_stale_quotes():
    ok, reason = allow_trade(10, 5000, RiskLimits(), RiskState())
    assert not ok
    assert reason == "stale_quote"
