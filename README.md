# Agentic Skills Security Research Exercise

This repository is a reproducible, safety-contained study of malicious agentic
skills. It contains ten public benign skills, three synthetic malicious fixtures,
an explainable static scanner, and a runtime event correlator.

**Safety:** never install or publish anything under `skills/malicious/`. The
fixtures contain malicious *instructions* as research data, but no working
exfiltration or persistence payload. `runtime/run_lab.py` only replays declared
events into a temporary directory; it does not read real secrets, execute decoded
content, or open network sockets.

The full method, definition, results, failed attempt, and limitations are in
[REPORT.md](REPORT.md). Sources are inventoried in [SOURCES.md](SOURCES.md).

## Repository layout

```text
skills/benign/       10 public baseline skills plus provenance and licenses
skills/malicious/    3 synthetic, non-deployable abuse fixtures
scanner/scan.py      static scanner; v1 and improved v2 rulesets
scanner/runtime_detector.py
runtime/run_lab.py   contained telemetry replay (not a real agent runtime)
evaluation/          reproducible evaluator and checked-in outputs
tests/               acceptance tests
```

## Requirements

- Python 3.10 or newer
- No third-party Python packages
- OpenClaw and Ollama are **not** required to reproduce the scanner results

The study targets the OpenClaw `SKILL.md` directory model. The benign public
samples use the same frontmatter-plus-Markdown skill shape.

## Reproduce

From this repository root:

```bash
python3 -m unittest discover -s tests -v
python3 evaluation/evaluate.py
```

The second command replaces the files in `evaluation/results/` and asserts:

- all 10 benign skills have verdict `Benign` under v2;
- v1 catches 2/3 malicious fixtures and misses the encoded fixture;
- v2 catches 3/3 malicious fixtures;
- runtime correlation catches all 3 contained replays.

Scan one skill or a directory containing many skills:

```bash
python3 scanner/scan.py skills/benign/academy-guide
python3 scanner/scan.py skills/malicious --ruleset v2
python3 scanner/scan.py skills/malicious --ruleset v1 --format json
```

Replay and inspect runtime telemetry independently:

```bash
python3 runtime/run_lab.py skills/malicious --output /tmp/skill-events.jsonl
python3 scanner/runtime_detector.py /tmp/skill-events.jsonl
```

## Expected summary

| Corpus | Ruleset/detector | Expected |
|---|---|---|
| 10 benign | static v2 | 10 Benign |
| 3 malicious | static v1 | 2 Malicious, 1 Benign (documented miss) |
| 3 malicious | static v2 | 3 Malicious |
| 3 malicious replays | runtime | 3 Malicious |

## Scope warning

This is a compact research prototype, not a production malware scanner. A
`Benign` result means “no configured correlation crossed the threshold,” not
“safe.” Use provenance verification, permission review, isolation, and runtime
policy in addition to scanning.
