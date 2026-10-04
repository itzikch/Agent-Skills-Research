#!/usr/bin/env python3
"""Regenerate all checked-in evaluation artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "evaluation" / "results"


def run_json(*args: str) -> object:
    proc = subprocess.run([sys.executable, *args], cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(proc.stdout)


def write_json(name: str, value: object) -> None:
    (RESULTS / name).write_text(json.dumps(value, indent=2) + "\n")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    scan = str(ROOT / "scanner" / "scan.py")
    benign_v2 = run_json(scan, "skills/benign", "--ruleset", "v2", "--format", "json")
    malicious_v1 = run_json(scan, "skills/malicious", "--ruleset", "v1", "--format", "json")
    malicious_v2 = run_json(scan, "skills/malicious", "--ruleset", "v2", "--format", "json")
    canary_v2 = run_json(scan, ".agents/skills/security-canary", "--ruleset", "v2", "--format", "json")
    write_json("benign-v2.json", benign_v2)
    write_json("malicious-v1.json", malicious_v1)
    write_json("malicious-v2.json", malicious_v2)
    write_json("canary-v2.json", canary_v2)

    events = RESULTS / "runtime-events.jsonl"
    subprocess.run(
        [sys.executable, str(ROOT / "runtime" / "run_lab.py"), "skills/malicious", "--output", str(events)],
        cwd=ROOT,
        check=True,
    )
    runtime = run_json(str(ROOT / "scanner" / "runtime_detector.py"), str(events))
    write_json("runtime-detection.json", runtime)

    assert len(benign_v2) == 10 and all(row["verdict"] == "Benign" for row in benign_v2)
    assert len(malicious_v2) == 3 and all(row["verdict"] == "Malicious" for row in malicious_v2)
    assert len(canary_v2) == 1 and canary_v2[0]["verdict"] == "Benign"
    assert sum(row["verdict"] == "Malicious" for row in malicious_v1) == 2
    assert all(row["verdict"] == "Malicious" for row in runtime["sessions"])
    print("evaluation regenerated; acceptance checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
