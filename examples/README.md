# OpenTrack examples

| File | Shows |
| --- | --- |
| `harness_trot_snapshot.json` | A synthetic Standardbred trotting race: three runners (one withdrawn), win and place markets, and the unvalidated semantics listed in `warnings`. |

Everything is synthetic — `synthetic-harness` is not a real source and no
provider offers this data. The file is shaped exactly like
`RaceSnapshot.to_dict()` output, so it round-trips through the models.

## Load it

```sh
PYTHONPATH=src python3 - <<'PY'
import json
from opentrack import RaceSnapshot, Runner, Market, Selection

data = json.loads(open('examples/harness_trot_snapshot.json').read())
snap = RaceSnapshot(
    **{k: (tuple(Runner(**r) for r in data["runners"]) if k == "runners"
           else tuple(Market(**{**m, "selections":
               tuple(Selection(**s) for s in m["selections"])})
               for m in data["markets"]) if k == "markets"
           else tuple(data["warnings"]) if k == "warnings"
           else data[k])
       for k in data}
)
# JSON-equal round trip (dataclass tuples serialize as arrays)
assert json.loads(json.dumps(snap.to_dict())) == data
print(snap.name, "|", len(snap.runners), "runners,", len(snap.markets), "markets")
PY
```

## What this dataset validates — and what it can't

The point of a representative harness corpus is to expose which Standardbred
semantics the current neutral model can carry and which it cannot. This file
exercises:

- `discipline` as a free string (`trot`) — pacing and mixed-gait cards are
  **not** distinguished today.
- A withdrawn runner keeping `source_id`, `withdrawn_at` and a `removed`
  selection rather than disappearing.
- The driver problem: the model has `rider`, and this file puts the driver
  there — one plausible adapter choice, recorded in `warnings`, **not** a
  settled contract.
- Missing data: `draw: null` post-scratch, `form: null`, `quoted_value: null`
  on the removed selection — unknown is preserved, never zero.
- `minimum_stake`/`maximum_stake` left null where units aren't verified.

Still unmodeled (and therefore still unverifiable from data): start method
(gate / walk-up / volt), gait beyond the `discipline` string, driver as a
first-class field, fractional/starting-price quote kinds, and track length or
surface. A real corpus run against these files is the evidence needed before
any of those become fields.
