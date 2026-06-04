#!/usr/bin/env python3
"""Local health checks for AI agent operator tooling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import socket
import sys
from dataclasses import asdict, dataclass


DEFAULT_COMMANDS = ["codex", "claude", "n8n", "node", "python3", "gh"]
DEFAULT_PORTS = [3000, 3417, 5678]


@dataclass
class CheckResult:
    kind: str
    target: str
    ok: bool
    detail: str


def check_command(command: str) -> CheckResult:
    path = shutil.which(command)
    if path:
        return CheckResult("command", command, True, f"found at {path}")
    return CheckResult("command", command, False, "not found in PATH")


def check_port(host: str, port: int, timeout: float) -> CheckResult:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
        except OSError as exc:
            return CheckResult("port", f"{host}:{port}", False, exc.__class__.__name__)
    return CheckResult("port", f"{host}:{port}", True, "reachable")


def load_profile(path: str | None) -> dict[str, object]:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("profile must be a JSON object")
    return data


def run_doctor(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    profile_commands = profile.get("commands", DEFAULT_COMMANDS)
    profile_ports = profile.get("ports", DEFAULT_PORTS)
    profile_host = str(profile.get("host", args.host))

    commands = args.command or list(profile_commands)
    ports = args.port or ([] if args.no_default_ports else list(profile_ports))

    results: list[CheckResult] = []
    results.extend(check_command(command) for command in commands)
    results.extend(check_port(profile_host, int(port), args.timeout) for port in ports)
    display_results = [result for result in results if not result.ok] if args.only_failures else results

    if args.json:
        print(json.dumps([asdict(result) for result in display_results], indent=2))
    else:
        for result in display_results:
            marker = "ok" if result.ok else "warn"
            print(f"[{marker}] {result.kind} {result.target}: {result.detail}")

    return 0 if all(result.ok for result in results) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agentops-healthkit")
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    doctor = subparsers.add_parser("doctor", help="Run local operator health checks")
    doctor.add_argument("--json", action="store_true", help="Print JSON output")
    doctor.add_argument("--host", default="127.0.0.1", help="Host for port checks")
    doctor.add_argument("--timeout", type=float, default=0.5, help="Port timeout in seconds")
    doctor.add_argument("--command", action="append", help="Command to check")
    doctor.add_argument("--port", type=int, action="append", help="TCP port to check")
    doctor.add_argument("--profile", help="JSON profile with commands, ports, and host")
    doctor.add_argument("--no-default-ports", action="store_true", help="Skip default port checks")
    doctor.add_argument("--only-failures", action="store_true", help="Only print failed checks")
    doctor.set_defaults(func=run_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
