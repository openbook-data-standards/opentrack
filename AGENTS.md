# OpenTrack development

- Private provider-neutral racing project in the OpenBook Data Standards family. Repository: `openbook-data-standards/opentrack`; line: `main`. Branch future changes from freshly fetched `origin/main`.
- Provider-specific parsing, transport and execution adapters belong in private RC, not here. Do not change public OpenBook/OpenVenue repositories as part of OpenTrack work.
- `src/opentrack/` contains private draft models, not a published standard or a claim of OpenBook conformance. Preserve source identity and unknown discipline; do not invent confirmed Standardbred coverage.
- Python 3.11+, standard library at runtime. Lint: `ruff check src tests`.
- Do not run tests locally. `.github/workflows/ci.yml` runs the synthetic model tests on pushes and pull requests.
- RC consumes a hash-pinned wheel in its private `vendor/` dependency directory. Maintain neutral source only here. Build an updated wheel and refresh the RC requirement hash when changing the consumed model version; never fork neutral source inside RC.
- No live trading, credentials, provider clients or external feed payloads belong in this repository.
