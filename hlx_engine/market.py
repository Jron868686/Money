from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Level:
    price: float
    quantity: float


@dataclass(frozen=True)
class OrderBook:
    venue: str
    symbol: str
    bids: tuple[Level, ...]
    asks: tuple[Level, ...]
    timestamp_ms: int


def executable_buy_cost(book: OrderBook, quantity: float) -> float | None:
    remaining, cost = quantity, 0.0
    for level in book.asks:
        take = min(remaining, level.quantity)
        cost += take * level.price
        remaining -= take
        if remaining <= 0:
            return cost
    return None


def executable_sell_proceeds(book: OrderBook, quantity: float) -> float | None:
    remaining, proceeds = quantity, 0.0
    for level in book.bids:
        take = min(remaining, level.quantity)
        proceeds += take * level.price
        remaining -= take
        if remaining <= 0:
            return proceeds
    return None


def best_cross_venue(books: Iterable[OrderBook], quantity: float) -> tuple[OrderBook, OrderBook] | None:
    books = list(books)
    candidates = []
    for buy in books:
        cost = executable_buy_cost(buy, quantity)
        if cost is None:
            continue
        for sell in books:
            if sell.venue == buy.venue:
                continue
            proceeds = executable_sell_proceeds(sell, quantity)
            if proceeds is not None:
                candidates.append((proceeds - cost, buy, sell))
    if not candidates:
        return None
    _, buy, sell = max(candidates, key=lambda item: item[0])
    return buy, sell
