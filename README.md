# OpenTrack

**Provider-neutral horse-racing data models.** A standalone project in the
[OpenBook Data Standards](https://github.com/openbook-data-standards) organization.

OpenTrack separates the racing data contract from the systems that collect,
translate, price or act on that data. Provider-specific adapters and consumer
applications can remain private; they do not belong in this repository.

**Status:** experimental draft · Python package `0.0.1` · Python 3.11+ · standard
library only at runtime. This is not a published interoperability standard or a
claim of conformance to OpenBook.

## Focus

The project covers horse racing, with **Standardbred / harness racing**—trotting
and pacing—as its first validation focus. The initial implementation provides
race snapshots, runners, grouped markets and selections.

The models do not establish that any particular provider offers harness racing.
Discipline stays unknown when source evidence does not establish it. Driver,
start-method, handicap and full harness-market semantics still need validation
against representative source fixtures; see [issue #1](https://github.com/openbook-data-standards/opentrack/issues/1).

## What is implemented

| Model | Purpose |
| --- | --- |
| `Runner` | Source runner identity, name, number, draw, withdrawal time and available connection/form details |
| `Selection` | Native outcome identity/status, quoted value, optional fixed decimal odds, stake limits and source parameters |
| `Market` | Source market and group identity, adapter-supplied classification, optional paid places, sequence and selections |
| `RaceSnapshot` | Source race identity, meeting/country, available times, source status, optional discipline, runners, markets and warnings |

These are immutable Python dataclasses. `RaceSnapshot.to_dict()` produces a
plain dictionary for serialization. They are not JSON Schemas, source-payload
validators or an identity-resolution service.

### Data principles

- Preserve source identifiers and statuses; a native identifier is not a
  cross-provider canonical identity.
- Keep decimal quote and stake values as strings rather than binary floats.
- Preserve market groups and terms instead of merging superficially similar
  products.
- Keep the source's quoted value separate from usable fixed decimal odds.
  Starting-price and unknown products must not be treated as guaranteed
  fixed-odds quotes.
- Leave missing times, currency assumptions and discipline unresolved rather
  than guessing. Stake limits without a verified currency are not comparable
  monetary limits.
- Record observation time separately from source scheduling and cutoff times.

## Install and use

From a checkout of this repository:

```sh
python3 -m pip install .
```

A synthetic example, with no provider connection:

```python
from opentrack import Runner, hypothetical_return

runner = Runner(
    source_id="example-runner-1",
    name="Example Horse",
    number=1,
    draw=3,
    withdrawn_at=None,
    trainer=None,
    rider=None,
    form=None,
    age=None,
)

print(runner.name)
print(hypothetical_return("10", "3.5"))
```

The return illustration produces `35.00` units. It is decimal arithmetic only:
no order is submitted, and deductions, dead heats, fees and currency conversion
are not included. It is not a bet-acceptance or payout guarantee.

The [model definitions](src/opentrack/__init__.py) and
[synthetic contract cases](tests/test_opentrack.py) describe the current API.

## Architecture and project boundary

```text
Provider data
    -> provider-specific adapter, maintained separately
    -> OpenTrack models
    -> research, display or other consumer application
```

This repository contains the provider-neutral models and synthetic examples.
It does **not** contain provider clients, credentials, proprietary mappings,
feed payloads, the consumer demo, account handling or bet execution.

OpenTrack has its own repository and lifecycle within the OpenBook Data
Standards organization; it is not a directory inside the public OpenBook
specification repository and does not create a separate GitHub organization.
[OpenBook](https://github.com/openbook-data-standards/openbook) remains the sibling
sportsbook/event-data standard. OpenTrack does not modify its specification or
vocabularies, or substitute draft model fields for approved OpenBook contracts.

## Development and verification

Source lives in `src/opentrack/`; synthetic tests live in `tests/`.
[GitHub Actions](https://github.com/openbook-data-standards/opentrack/actions)
runs lint and model tests on pushes and pull requests. This project's workflow
keeps test execution in CI rather than running tests locally.

Static lint, when Ruff is installed:

```sh
ruff check src tests
```

Provider adapters and integration-specific verification belong in their own
projects. No real provider account or API key is needed for OpenTrack CI.

## License

No license has been declared yet. Public repository visibility alone does not
grant an open-source license; a licensing decision is still pending.
