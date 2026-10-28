from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True, slots=True)
class Runner:
    source_id: str
    name: str
    number: int | None
    draw: int | None
    withdrawn_at: str | None
    trainer: str | None
    rider: str | None
    form: str | None
    age: int | None


@dataclass(frozen=True, slots=True)
class Selection:
    source_id: str
    runner_id: str | None
    source_status: str | None
    quoted_value: str | None
    decimal_odds: str | None
    minimum_stake: str | None
    maximum_stake: str | None
    source_url: str | None
    parameters: str | None


@dataclass(frozen=True, slots=True)
class Market:
    source_id: str
    source_group: str
    kind: str
    places: int | None
    sequence: str | None
    selections: tuple[Selection, ...]


@dataclass(frozen=True, slots=True)
class RaceSnapshot:
    source: str
    source_id: str
    name: str
    meeting: str | None
    country: str | None
    scheduled_at: str | None
    cutoff_at: str | None
    observed_at: str
    source_status: str | None
    discipline: str | None
    runners: tuple[Runner, ...]
    markets: tuple[Market, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def hypothetical_return(stake: str, decimal_odds: str) -> str:
    try:
        amount, odds = Decimal(stake), Decimal(decimal_odds)
    except InvalidOperation:
        raise ValueError("Stake and odds must be decimal numbers") from None
    if not amount.is_finite() or not odds.is_finite() or amount <= 0 or odds <= 1:
        raise ValueError("Stake must be positive and decimal odds greater than one")
    if amount > 1000000 or odds > 1000000:
        raise ValueError("Hypothetical calculation exceeds demo bounds")
    return format(amount * odds, ".2f")
