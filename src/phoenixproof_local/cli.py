from __future__ import annotations

import json
import sys

import typer
from rich.console import Console
from rich.table import Table

from phoenixproof_local.dashboard import build_dashboard
from phoenixproof_local.engine import evaluate_case
from phoenixproof_local.runner import benchmark, export_demo_pack, init_demo, run_suite, verify_outputs


app = typer.Typer(help="Offline cross-vertical AI care safety benchmark.")
console = Console()


@app.command("init-demo")
def init_demo_command(force: bool = typer.Option(False, "--force")) -> None:
    init_demo(force=force)
    console.print("[green]Initialized synthetic safety benchmark store.[/green]")


@app.command("evaluate")
def evaluate_command(case_id: str) -> None:
    result = evaluate_case(case_id)
    console.print_json(result.model_dump_json(indent=2))
    if not result.pass_case:
        raise typer.Exit(1)


@app.command("run")
def run_command(vertical: str = typer.Option("all", "--vertical"), iterations: int = typer.Option(1, "--iterations", min=1)) -> None:
    summary = run_suite(vertical=vertical, iterations=iterations)
    console.print_json(summary.model_dump_json(indent=2))
    if not summary.pass_gates:
        raise typer.Exit(1)


@app.command("verify")
def verify_command() -> None:
    ok, checks = verify_outputs()
    table = Table(title="Verification")
    table.add_column("Gate")
    table.add_column("Status")
    for gate, status in checks.items():
        table.add_row(gate, "PASS" if status else "FAIL")
    console.print(table)
    if not ok:
        raise typer.Exit(1)


@app.command("dashboard")
def dashboard_command() -> None:
    path = build_dashboard()
    console.print(f"[green]Dashboard written:[/green] {path}")


@app.command("benchmark")
def benchmark_command(iterations: int = typer.Option(100, "--iterations", min=1)) -> None:
    summary = benchmark(iterations=iterations)
    table = Table(title="Benchmark")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("cases", str(summary.case_count))
    table.add_row("pass rate", f"{summary.pass_rate:.0%}")
    table.add_row("escalation SLO", f"{summary.escalation_slo_rate:.0%}")
    table.add_row("unsafe term rate", f"{summary.unsafe_term_rate:.0%}")
    table.add_row("p95 latency", f"{summary.p95_latency_ms} ms")
    table.add_row("pass gates", str(summary.pass_gates))
    console.print(table)
    if not summary.pass_gates:
        raise typer.Exit(1)


@app.command("export-demo-pack")
def export_demo_pack_command() -> None:
    path = export_demo_pack()
    console.print(f"[green]Demo pack exported:[/green] {path}")


@app.command("tool-loop")
def tool_loop_command() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        payload = json.loads(line)
        tool = str(payload["tool"])
        args = dict(payload.get("arguments", {}))
        if tool == "evaluate":
            print(evaluate_case(str(args["case_id"])).model_dump_json())
        else:
            raise typer.BadParameter(f"unknown tool: {tool}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()

