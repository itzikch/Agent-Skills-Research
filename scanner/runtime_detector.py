#!/usr/bin/env python3
"""Correlate JSONL runtime events emitted by the contained lab harness."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def detect(events: list[dict]) -> dict:
    by_session: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        by_session[event.get("session", "unknown")].append(event)

    alerts = []
    for session, session_events in by_session.items():
        session_events.sort(key=lambda event: event.get("relative_ms", 0))

        def sequence(first, second, window_ms: int = 30_000) -> bool:
            for left in session_events:
                if not first(left):
                    continue
                for right in session_events:
                    delta = right.get("relative_ms", 0) - left.get("relative_ms", 0)
                    if 0 <= delta <= window_ms and second(right):
                        return True
            return False

        read_then_egress = sequence(
            lambda e: e.get("event") == "file_read" and e.get("sensitive"),
            lambda e: e.get("event") == "network_connect",
        )
        write_then_hidden_spawn = sequence(
            lambda e: e.get("event") == "file_write" and e.get("agent_control_path"),
            lambda e: e.get("event") == "process_spawn" and e.get("concealed"),
        )
        decode_then_spawn = sequence(
            lambda e: e.get("event") == "decoder_invocation",
            lambda e: e.get("event") == "process_spawn",
        )

        reasons = []
        if read_then_egress:
            reasons.append("sensitive file read followed by an outbound connection attempt")
        if write_then_hidden_spawn:
            reasons.append("agent control-path write correlated with a concealed child process")
        if decode_then_spawn:
            reasons.append("content decoding correlated with child-process execution")
        alerts.append({"session": session, "verdict": "Malicious" if reasons else "Benign", "reasons": reasons or ["no configured runtime correlation matched"]})
    return {"sessions": alerts, "event_count": len(events)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.events.read_text().splitlines() if line.strip()]
    print(json.dumps(detect(rows), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
