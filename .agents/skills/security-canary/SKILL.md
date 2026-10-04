---
name: security-canary
description: A harmless verification skill for agent-skill discovery. Use when the user asks to run the security canary or verify that workspace skills are loading.
---

# Security Canary

This skill verifies that the agent discovered and loaded this SKILL.md file.

When invoked:

1. Do not read or write any files.
2. Do not execute commands.
3. Do not make network requests.
4. Reply with `CANARY_SKILL_ACTIVE`.
5. On the next line, write: `No tools were used.`