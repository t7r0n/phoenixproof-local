from __future__ import annotations

import json
import subprocess

from phoenixproof_local.dashboard import build_dashboard
from phoenixproof_local.engine import evaluate_case
from phoenixproof_local.runner import export_demo_pack, run_suite, verify_outputs


def test_pulse_hypertensive_crisis_escalates_immediately() -> None:
    result = evaluate_case("pulse-hypertensive-crisis")
    assert result.pass_case
    assert "hypertensive_crisis" in result.detected_flags
    assert result.escalation_turn == 1


def test_low_risk_mind_case_does_not_over_escalate() -> None:
    result = evaluate_case("mind-support-baseline")
    assert result.pass_case
    assert result.escalation_turn is None
    assert result.detected_flags == []


def test_pregnancy_bp_number_does_not_trigger_hypoglycemia() -> None:
    result = evaluate_case("bloom-pregnancy-redflag")
    assert result.pass_case
    assert "preeclampsia" in result.detected_flags
    assert "hypoglycemia" not in result.detected_flags


def test_cross_vertical_suite_passes_all_gates() -> None:
    summary = run_suite(vertical="all")
    assert summary.pass_gates
    assert set(summary.vertical_scores) == {"mind", "pulse", "thrive", "bloom"}
    ok, checks = verify_outputs()
    assert ok, checks


def test_dashboard_and_demo_pack() -> None:
    run_suite(vertical="all")
    dashboard = build_dashboard()
    assert "PhoenixProof Safety Dashboard" in dashboard.read_text(encoding="utf-8")
    pack = export_demo_pack()
    assert (pack / "manifest.json").exists()


def test_jsonl_tool_loop() -> None:
    payload = {"tool": "evaluate", "arguments": {"case_id": "bloom-pregnancy-redflag"}}
    completed = subprocess.run(
        ["uv", "run", "--project", "elite_projects/phoenixproof-local", "phoenixproof-local", "tool-loop"],
        input=json.dumps(payload) + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    result = json.loads(completed.stdout)
    assert result["case_id"] == "bloom-pregnancy-redflag"
    assert result["pass_case"]
