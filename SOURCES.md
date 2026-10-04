# Sources

Accessed 2026-10-04 unless noted otherwise.

1. [OpenClaw: Skills](https://docs.openclaw.ai/tools/skills) — skill format,
   discovery, loading precedence, environment injection, and installation paths.
2. [OpenClaw: Creating skills](https://docs.openclaw.ai/tools/creating-skills) —
   minimal `SKILL.md` anatomy and local authoring workflow.
3. [OWASP Agentic Skills Top 10](https://owasp.org/projects/agentic-skills-top-10)
   and its [project site](https://owasp.github.io/www-project-agentic-skills-top-10/)
   — threat taxonomy and recommendations for sandboxing, provenance, scanning,
   and structured audit logging. Version shown by OWASP: 1.0-2026.
4. [Anthropic public skills repository](https://github.com/anthropics/skills) at
   commit [`8a1541c`](https://github.com/anthropics/skills/tree/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4)
   — all ten benign baseline skills. Per-skill license files are retained.
5. Python 3.10 standard-library documentation for
   [`base64`](https://docs.python.org/3.10/library/base64.html),
   [`re`](https://docs.python.org/3.10/library/re.html), and
   [`subprocess`](https://docs.python.org/3.10/library/subprocess.html) — APIs used
   by the scanner and contained replay harness.
6. [Google Antigravity: Agent Skills](https://antigravity.google/docs/skills?app=antigravity-ide)
   — `.agents/skills/<skill-folder>/SKILL.md` workspace location, progressive
   disclosure, and activation behavior.
7. [OpenClaw: Ollama provider](https://docs.openclaw.ai/providers/ollama) and
   [Ollama setup](https://docs.openclaw.ai/providers/ollama/setup) — native local
   API configuration, model discovery, tool capability, and context requirements.

Claims in the report labeled “observed” come from the checked-in test/evaluation
outputs, not from these sources. Threat examples are synthetic and are not claimed
to be samples recovered from a real campaign.
