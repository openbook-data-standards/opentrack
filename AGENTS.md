# OpenTrack development

- Public, standalone provider-neutral racing project in the OpenBook Data Standards organization. Repository: `openbook-data-standards/opentrack`; line: `main`. It is not a separate GitHub organization. Branch future changes from freshly fetched `origin/main`.
- Provider-specific parsing, transport and execution adapters belong in separately maintained implementations, which may be private, not here. Do not change public OpenBook/OpenVenue repositories as part of OpenTrack work.
- `src/opentrack/` contains experimental draft models, not a published standard or a claim of OpenBook conformance. Preserve source identity and unknown discipline; do not invent confirmed Standardbred coverage.
- Python 3.11+, standard library at runtime. Lint: `ruff check src tests`.
- Do not run tests locally. `.github/workflows/ci.yml` runs the synthetic model tests on pushes and pull requests.
- Consumers may depend on hash-pinned wheels. Maintain neutral source only here; when changing a consumed model version, coordinate dependency-version/hash updates with consumers rather than forking neutral source into adapters.
- No live trading, credentials, provider clients or external feed payloads belong in this repository.
