from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel


Vertical = Literal["mind", "pulse", "thrive", "bloom"]


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


class Vital(BaseModel):
    turn: int
    systolic: int | None = None
    diastolic: int | None = None
    glucose: int | None = None
    weight_delta_kg: float | None = None


class Turn(BaseModel):
    turn: int
    member: str


class Case(BaseModel):
    id: str
    vertical: Vertical
    profile: dict[str, str | int]
    vitals: list[Vital]
    turns: list[Turn]
    red_flags: list[str]
    must_escalate_by_turn: int | None
    unsafe_terms: list[str]


class FixtureSet(BaseModel):
    cases: list[Case]


class SimulatedTurn(BaseModel):
    turn: int
    member: str
    phoenix: str
    escalated: bool
    detected_flags: list[str]


class CaseResult(BaseModel):
    case_id: str
    vertical: Vertical
    simulated_turns: list[SimulatedTurn]
    expected_flags: list[str]
    detected_flags: list[str]
    escalation_turn: int | None
    required_escalation_turn: int | None
    unsafe_terms_found: list[str]
    safety_score: float
    pass_case: bool
    failure_reasons: list[str]
    latency_ms: float


class SuiteSummary(BaseModel):
    run_id: str
    case_count: int
    pass_rate: float
    escalation_slo_rate: float
    unsafe_term_rate: float
    vertical_scores: dict[str, float]
    p95_latency_ms: float
    pass_gates: bool

