# Phoenixproof Local

Phoenixproof Local is an offline, synthetic safety benchmark for multi-turn AI care conversations across several care verticals.

It extends a role-play style evaluation with biosignal-conditioned fixtures, deterministic safety judges, escalation timing checks, and a local dashboard. It does not call clinical systems, model APIs, device APIs, or external services.

## Engineering target

Offline cross-vertical safety benchmark for AI care conversations.

## How it works

- Models the `phoenixproof-local` workflow with deterministic fixtures and seeded failure cases.
- Turns the core claim in `Phoenixproof Local` into explicit gates that can fail a local run.
- Stores enough `Phoenixproof Local` evidence for a reviewer to inspect the decision path.
- Keeps `phoenixproof-local` offline, reproducible, and independent of hosted services.

## Run the system

```bash
uv sync
uv run phoenixproof-local init-demo
uv run phoenixproof-local run --vertical all
uv run phoenixproof-local verify
uv run phoenixproof-local dashboard
```

```bash
uv run phoenixproof-local evaluate pulse-hypertensive-crisis
```

## Evidence to inspect

- `outputs/results.json`
- `outputs/summary.json`
- `outputs/leaderboard.json`
- `outputs/dashboard.html`
- `outputs/demo_pack/`

## Validation

```bash
uv run ruff check .
uv run pytest -q
uv run phoenixproof-local verify
```

## Data boundary

The `phoenixproof-local` public surface is source, tests, lockfile, and docs. It does not need credentials, browser state, customer records, or hosted services.
