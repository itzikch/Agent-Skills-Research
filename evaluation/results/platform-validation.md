# Platform validation record

Observed manually on 2026-10-04.

| Target | Input | Observed output | Interpretation |
|---|---|---|---|
| Google Antigravity | `Use the security-canary skill and run its verification.` | `CANARY_SKILL_ACTIVE No tools were used.` | Workspace `SKILL.md` discovery and activation passed. |
| Ollama `granite3.3:2b` | Same request, with the canary explicitly loaded by `runtime/ollama_canary_test.py` | `CANARY_SKILL_ACTIVE` followed by `No tools were used.` | Local model instruction-following passed; automatic discovery was not tested. |
The malicious fixtures were never installed into either environment. Antigravity
and Ollama received only the harmless canary.
