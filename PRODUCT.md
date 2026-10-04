# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The primary user is the repository author presenting an agentic-skills security
exercise during a technical interview. The secondary user is the interviewer, who
needs to understand the threat model, experimental process, evidence, and limits
quickly without reading the entire repository first.

## Product Purpose

The product is a self-contained interview dashboard that explains and demonstrates
the repository's static scanning, scanner improvement, contained runtime detection,
and platform-validation results. Success means a presenter can walk through the
work accurately and an interviewer can distinguish observed evidence from claims
and simulations.

## Positioning

The dashboard connects each conclusion to its evidence: the exact skill technique,
rule-score composition, v1 failure, v2 change, runtime correlation, and platform
validation boundary. It is a presentation layer over reproducible repository facts,
not a replacement for the report or a generic security dashboard.

## Operating Context

The dashboard is opened directly from the Git repository during an interview. It
must work offline as one HTML file without a build step, server, package install,
or external font/script dependency. The Markdown report remains the formal written
deliverable.

## Capabilities and Constraints

- Present the ten-benign and three-malicious static results.
- Compare literal-only v1 with decoded-layer v2.
- Explain the three malicious techniques and score breakdowns.
- Visualize the contained runtime event correlations.
- Separate Antigravity discovery, Ollama instruction following, and blocked
  OpenClaw installation.
- Include scanner limitations, telemetry gaps, and an interview talk track.
- Use only repository-backed facts; do not invent benchmarks or production claims.
- Keep malicious fixtures inert and never install or execute them.

## Evidence on Hand

- `REPORT.md`, `README.md`, and `SOURCES.md`.
- `evaluation/results/*.json` and `evaluation/results/platform-validation.md`.
- Scanner and runtime source code.
- Ten pinned public benign skills and three synthetic malicious fixtures.
- Observed Antigravity canary activation and Ollama canary response.
- No validated OpenClaw execution because IBM corporate policy blocked installation.

## Product Principles

1. Evidence before assertion.
2. Distinguish static content, simulated telemetry, and real platform observations.
3. Make the failed v1 experiment as visible as the successful v2 result.
4. Preserve safety boundaries and avoid implying that a Benign verdict proves safety.
5. Support a concise interview story while keeping detailed reasoning one interaction away.

## Accessibility & Inclusion

Use semantic HTML, keyboard-operable navigation, visible focus, reduced-motion
support, sufficient contrast, responsive layouts, and explanations that do not
depend on color alone.
