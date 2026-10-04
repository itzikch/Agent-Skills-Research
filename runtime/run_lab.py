#!/usr/bin/env python3
"""Safely replay declared malicious-skill behavior as telemetry only.

This harness never interprets shell commands, reads real secrets, or opens sockets.
It validates a small event schema, rewrites paths into the lab directory, and emits
JSONL so runtime correlation can be tested without executing the abusive action.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path


ALLOWED_EVENTS = {"file_read", "file_write", "network_connect", "process_spawn", "decoder_invocation"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scenarios = sorted(args.skills.rglob("scenario.json"))
    if not scenarios:
        parser.error("no scenario.json files found")

    rows = []
    with tempfile.TemporaryDirectory(prefix="agent-skill-lab-") as lab:
        lab_root = Path(lab)
        for scenario_index, scenario_path in enumerate(scenarios):
            scenario = json.loads(scenario_path.read_text())
            session = f"{scenario_path.parent.name}-session"
            for offset, declared in enumerate(scenario["events"]):
                if declared.get("event") not in ALLOWED_EVENTS:
                    raise ValueError(f"unsupported event in {scenario_path}: {declared}")
                event = dict(declared)
                event["session"] = session
                event["skill"] = scenario_path.parent.name
                event["relative_ms"] = scenario_index * 1000 + offset * 10
                if "path" in event:
                    event["original_path"] = event["path"]
                    # Keep evidence deterministic while retaining a real isolated
                    # directory for the duration of the replay.
                    _contained_path = lab_root / event["path"].lstrip("~/")
                    event["path"] = "sandbox://" + str(_contained_path.relative_to(lab_root))
                if event["event"] == "network_connect":
                    event["blocked"] = True
                    event["note"] = "telemetry replay only; no socket was opened"
                rows.append(event)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    print(f"wrote {len(rows)} contained telemetry events to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
