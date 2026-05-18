# Security Review

## Scope

Local CLI, deterministic synthetic care fixtures, rule-based clinician simulator, safety judges, DuckDB run store, static dashboard, JSONL tool loop, and demo-pack export.

## Assessment

The application is offline and synthetic-only. It does not contact model APIs, clinical systems, medical devices, external identity systems, or shell commands at runtime.

## Controls

- Fixtures are parsed through Pydantic models.
- Scenario verticals, red flags, and safety criteria are closed local enumerations.
- The verifier checks escalation timing, contraindication avoidance, and judge coverage.
- DuckDB writes use parameterized inserts.
- Dashboard rendering uses Jinja autoescaping.
- Runtime state, outputs, caches, and virtual environments are ignored by git.

## Focused Scan Status

Completed for the public release.

## Results

- Static release hygiene scan: clean for non-public context, personal account strings, cloud credential markers, and common secret prefixes.
- Runtime surface scan: no network clients, dynamic code execution, unsafe deserialization, or shell execution in application code.
- Test-only process launch is limited to the CLI JSONL loop regression test.
- Validation suite: `ruff`, `pytest`, `phoenixproof-local verify`, `phoenixproof-local benchmark --iterations 100`, and dashboard HTML checks passed.

## Residual Risk

This is a deterministic local benchmark over synthetic cases. It is not a medical device, clinical decision system, or replacement for expert safety review. Real deployments should add external clinical governance, broader adversarial fixtures, and reviewer sign-off.
