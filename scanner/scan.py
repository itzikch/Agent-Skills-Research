#!/usr/bin/env python3
"""Explainable static scanner for OpenClaw-style agentic skills.

The scanner is intentionally dependency-free.  It is a research prototype, not a
malware verdict service: results are triage signals and must be reviewed.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".txt", ".py", ".js", ".mjs", ".cjs", ".sh", ".json", ".yaml", ".yml", ".toml"}
IGNORED_NAMES = {"license", "license.txt", "notice", "notice.txt"}
MAX_FILE_BYTES = 1_000_000


@dataclass(frozen=True)
class Rule:
    rule_id: str
    category: str
    score: int
    pattern: str
    reason: str
    since: int = 1


@dataclass
class Finding:
    rule_id: str
    category: str
    score: int
    file: str
    line: int
    evidence: str
    reason: str
    layer: str = "literal"


RULES = [
    Rule("INJ001", "instruction-hijack", 4, r"(?i)ignore\s+(?:all\s+)?(?:(?:previous|prior)(?:\s+(?:system|developer))?|system|developer)\s+instructions", "Attempts to override higher-priority instructions."),
    Rule("INJ002", "concealment", 4, r"(?i)(?:do\s+not|don['’]t|never)\s+(?:tell|show|mention|inform|alert)\s+(?:the\s+)?user", "Tells the agent to conceal behavior from the user."),
    Rule("SEC001", "secret-access", 5, r"(?i)(?:~/|\$HOME/|/home/[^/]+/|/Users/[^/]+/)?(?:\.ssh/(?:id_rsa|id_ed25519|config)|\.aws/credentials|\.config/gcloud|\.kube/config|\.env\b|wallet\.dat|Login Data)", "References a high-value credential or private-data path."),
    Rule("SEC002", "secret-access", 4, r"(?i)\b(?:AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|PRIVATE_KEY|SEED_PHRASE)\b", "References a credential-bearing environment variable or value."),
    Rule("NET001", "network-egress", 4, r"(?i)\b(?:curl|wget)\b[^\n]{0,160}(?:https?://|--data|-d\s|--upload-file)", "Uses a command-line client for outbound transfer."),
    Rule("NET002", "network-egress", 4, r"(?i)(?:requests\.(?:post|put)|fetch\s*\(|axios\.(?:post|put)|https?\.request|webhook|upload\s+to|POST\s+https?://)", "Performs or directs an outbound data transfer."),
    Rule("PER001", "persistence", 4, r"(?i)(?:\.openclaw|\.claude|\.codex)/(?:skills|config|settings)|workspace/skills", "Targets an agent skill or configuration location."),
    Rule("PER002", "persistence", 3, r"(?i)\b(?:copy|cp|mv|write|append|install|replace|modify)\b[^\n]{0,100}(?:SKILL\.md|config\.json|settings\.json|skills?/)", "Writes to skill/configuration material."),
    Rule("EXE001", "dynamic-execution", 4, r"(?i)(?:\beval\s*\(|\bexec\s*\(|base64\s+(?:--decode|-d)|b64decode\s*\([^\n]{0,80}\)\s*(?:\)|\.decode)[^\n]{0,80}(?:exec|eval))", "Decodes or dynamically executes data."),
    Rule("DES001", "destructive", 7, r"(?i)\brm\s+-[a-z]*r[a-z]*f\b|\b(?:mkfs|shred)\b", "Contains a destructive filesystem command."),
    Rule("CTL001", "approval-bypass", 4, r"(?i)(?:bypass|skip|disable|avoid)\s+(?:the\s+)?(?:approval|permission|confirmation|sandbox|security)", "Directs the agent to bypass a safety boundary."),
]

BASE64_RE = re.compile(r"(?<![A-Za-z0-9+/])([A-Za-z0-9+/]{48,}={0,2})(?![A-Za-z0-9+/])")


def skill_roots(target: Path) -> list[Path]:
    if target.is_file():
        if target.name != "SKILL.md":
            raise ValueError("a file input must be named SKILL.md")
        return [target.parent]
    if not target.is_dir():
        raise ValueError(f"input does not exist: {target}")
    if (target / "SKILL.md").is_file():
        return [target]
    return sorted({p.parent for p in target.rglob("SKILL.md")})


def parse_name(skill_file: Path) -> str:
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    head = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else text[:1000]
    match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", head)
    return match.group(1).strip() if match else skill_file.parent.name


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            continue
        if not path.is_file() or path.name.lower() in IGNORED_NAMES:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > MAX_FILE_BYTES:
            continue
        yield path


def scan_text(text: str, relpath: str, ruleset: int, layer: str = "literal") -> list[Finding]:
    findings: list[Finding] = []
    for rule in RULES:
        if rule.since > ruleset:
            continue
        for match in re.finditer(rule.pattern, text):
            line = text.count("\n", 0, match.start()) + 1
            evidence = " ".join(match.group(0).split())[:180]
            findings.append(Finding(rule.rule_id, rule.category, rule.score, relpath, line, evidence, rule.reason, layer))
    return findings


def decoded_layers(text: str) -> Iterable[str]:
    """Yield printable base64-decoded strings (added in ruleset v2)."""
    for match in BASE64_RE.finditer(text):
        token = match.group(1)
        try:
            decoded = base64.b64decode(token, validate=True).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            continue
        printable = sum(ch.isprintable() or ch in "\r\n\t" for ch in decoded)
        if decoded and printable / len(decoded) >= 0.9:
            yield decoded


def dedupe_and_cap(findings: list[Finding]) -> list[Finding]:
    """One contribution per rule/layer prevents repeated prose inflating a verdict."""
    chosen: dict[tuple[str, str], Finding] = {}
    for finding in findings:
        chosen.setdefault((finding.rule_id, finding.layer), finding)
    return list(chosen.values())


def evaluate(root: Path, ruleset: int) -> dict:
    raw: list[Finding] = []
    scanned_files = 0
    for path in iter_text_files(root):
        scanned_files += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(root))
        raw.extend(scan_text(text, rel, ruleset))
        if ruleset >= 2:
            for index, decoded in enumerate(decoded_layers(text), 1):
                raw.extend(scan_text(decoded, rel, ruleset, f"base64-decoded-{index}"))

    findings = dedupe_and_cap(raw)
    categories = {f.category for f in findings}
    score = sum(f.score for f in findings)

    # Cross-signal combinations express intent better than isolated tool use.
    bonuses: list[str] = []
    if {"secret-access", "network-egress"} <= categories:
        score += 4
        bonuses.append("credential/private-data access is combined with network egress")
    if {"persistence", "concealment"} <= categories:
        score += 3
        bonuses.append("agent persistence is combined with concealment")
    if ruleset >= 2 and any(f.layer.startswith("base64-decoded") for f in findings):
        score += 3
        bonuses.append("v2 decoded an embedded payload before applying the normal rules")

    verdict = "Malicious" if score >= 10 else "Suspicious" if score >= 5 else "Benign"
    reasons = [f"{f.rule_id}: {f.reason}" for f in findings]
    reasons.extend(f"CORRELATION: {bonus}." for bonus in bonuses)
    if not reasons:
        reasons = ["No configured high-risk pattern or risk correlation was found."]

    try:
        display_path = str(root.relative_to(Path.cwd()))
    except ValueError:
        display_path = str(root)
    return {
        "skill": parse_name(root / "SKILL.md"),
        "path": display_path,
        "ruleset": f"v{ruleset}",
        "verdict": verdict,
        "score": score,
        "files_scanned": scanned_files,
        "reasoning": reasons,
        "findings": [asdict(f) for f in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="SKILL.md or directory containing one or more skills")
    parser.add_argument("--ruleset", choices=("v1", "v2"), default="v2", help="historical ruleset (default: v2)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        roots = skill_roots(args.target.resolve())
    except ValueError as exc:
        parser.error(str(exc))
    if not roots:
        parser.error("no SKILL.md files found")

    results = [evaluate(root, int(args.ruleset[1:])) for root in roots]
    if args.format == "json":
        json.dump(results, sys.stdout, indent=2)
        print()
    else:
        for result in results:
            print(f"{result['skill']}: {result['verdict']} (score={result['score']}, {result['ruleset']})")
            for reason in result["reasoning"]:
                print(f"  - {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
