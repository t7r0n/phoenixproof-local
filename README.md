# Phoenixproof Local

Phoenixproof Local is an offline, synthetic safety benchmark for multi-turn AI care conversations across several care verticals.

It extends a role-play style evaluation with biosignal-conditioned fixtures, deterministic safety judges, escalation timing checks, and a local dashboard. It does not call clinical systems, model APIs, device APIs, or external services.

## Quick Start

```bash
uv sync
uv run phoenixproof-local init-demo
uv run phoenixproof-local run --vertical all
uv run phoenixproof-local verify
uv run phoenixproof-local dashboard
```

Run one case:

```bash
uv run phoenixproof-local evaluate pulse-hypertensive-crisis
```

## What It Measures

- Red-flag detection across `mind`, `pulse`, `thrive`, and `bloom`.
- Time-to-escalation SLOs for biosignal and symptom-triggered scenarios.
- Unsafe reassurance, contraindication, and missed-referral failures.
- Local leaderboard-style scores by vertical and scenario.

## Outputs

- `outputs/results.json`
- `outputs/summary.json`
- `outputs/leaderboard.json`
- `outputs/dashboard.html`
- `outputs/demo_pack/`

