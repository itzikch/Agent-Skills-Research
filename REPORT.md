# Agentic Skills Security: Static and Runtime Detection

Test date: 2026-10-04  
Target model: OpenClaw-style file-backed skills  
Scanner implementation: dependency-free Python 3.10+

## 1. Definition and security boundary

### What is an agentic skill?

For this exercise, an **agentic skill** is a versionable bundle that extends an
AI agent's behavior by supplying model-readable instructions and, optionally,
scripts, references, assets, metadata, and tool requirements. It is agentic when
the bundle can affect how the model selects tools or carries out a multi-step
task—not merely when it contains executable code.

This definition follows OpenClaw's documented model: a skill is a directory with
a YAML-frontmatter `SKILL.md` whose Markdown teaches the agent when and how to use
tools. OpenClaw also supports scripts/resources and several discovery roots. Its
workspace skills have higher precedence than bundled skills. Those details matter:
natural language is part of the executable control plane, and a write to a
higher-precedence skill directory can alter future agent behavior.

### What makes one malicious?

A skill is **malicious** when its intended or reasonably foreseeable behavior
covertly violates the user's authorization, confidentiality, integrity, or
availability, or weakens the controls that protect those properties. The key is
the mismatch between represented purpose and effective behavior. Examples include
secret collection unrelated to the task, concealed egress, installing a shadow
skill for persistence, disabling approvals, and decoding instructions to evade
review.

Risky capability alone is not enough. A deployment skill may legitimately use
networking; a test skill may spawn a process; a document skill may read user
files. The scanner therefore looks for **correlated intent**—for example,
sensitive access plus egress—rather than declaring every shell command malicious.

Three classifications are used:

- **Benign (score 0–4):** no strong configured correlation. This is not proof of safety.
- **Suspicious (score 5–9):** meaningful risk indicators need human review.
- **Malicious (score 10+):** multiple high-risk signals or a severe operation establish a strong abuse pattern.

This framing maps most directly to OWASP AST01 (Malicious Skills), while the
shadowing case also touches AST02 (Supply Chain Compromise), AST03
(Over-Privileged Skills), AST08 (Poor Scanning), and AST09 (No Governance).

## 2. Environment and corpus

I selected OpenClaw because its public documentation clearly specifies the skill
format, search roots, precedence, environment injection, and local/Ollama path.
The scanner does not require a model: it analyzes the bundle before installation.

### Benign baseline

The ten benign skills were copied from Anthropic's public `anthropics/skills`
repository at pinned commit `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`:

1. `academy-guide`
2. `algorithmic-art`
3. `brand-guidelines`
4. `discernment-nudge`
5. `frontend-design`
6. `internal-comms`
7. `pdf`
8. `slack-gif-creator`
9. `theme-factory`
10. `webapp-testing`

They are public examples rather than hand-written easy negatives. Some contain
real scripts and tool-oriented instructions, which makes them a useful
false-positive baseline. Exact provenance, licenses, and corpus digests are in
`skills/benign/PROVENANCE.md`. The PDF skill's upstream license is
source-available rather than open source; its terms are preserved in place.

### Malicious corpus and safety design

The three malicious skills are synthetic because this exercise is about detection,
not distributing live malware. Each includes an explicit warning and a declarative
`scenario.json`. Destinations use the reserved `.invalid` TLD. There is no code
that reads credentials, modifies OpenClaw, or contacts a server.

| Fixture | Technique | General pattern |
|---|---|---|
| `01-credential-exfiltration` | Prompt-level secret theft and concealed exfiltration | instruction override + sensitive path + outbound POST + concealment |
| `02-shadow-skill-persistence` | Higher-precedence skill shadowing and config persistence | agent-control-path write + config change + concealed process |
| `03-obfuscated-payload` | Base64 concealment of dangerous natural-language instructions | opaque decode + decoded sensitive read + decoded outbound POST |

These differ at the control layer: direct task abuse, durable modification of the
agent's future behavior, and scanner evasion through representation.

## 3. Static scanner design

`scanner/scan.py` accepts either one `SKILL.md` or a directory. For every discovered
skill it:

1. Recursively inventories bounded-size text files while refusing to follow symlinks.
2. Parses the skill name without executing YAML tags or importing the bundle.
3. Applies explainable regex rules for instruction hijacking, concealment, sensitive
   paths and environment variables, network egress, agent-control-path writes,
   dynamic execution, destructive commands, and approval bypass.
4. Caps repeated matches to one contribution per rule/layer so repeated prose does
   not inflate a verdict.
5. Adds correlation bonuses for private-data access plus egress, or persistence
   plus concealment.
6. Emits verdict, score, rule IDs, file, line, evidence, and reasoning as text or JSON.

The rules are general: no rule contains a fixture name, fixture path, exact encoded
string, or corpus-specific allowlist. An isolated `fetch()` or `eval()` is scored
but does not cross the suspicious threshold. That is why legitimate creative and
frontend samples can remain Benign even when they contain a risky primitive.

### Scanner limits by construction

Static matching sees declared text and scripts but not model interpretation,
runtime arguments, remote content fetched later, environment-specific permissions,
or a dependency that changes after review. Regex is particularly weak against
paraphrase, fragmented instructions, novel codecs, encryption, steganography,
generated code, and logic split across multiple skills.

## 4. What failed, and the v2 change

The first implementation, retained as `--ruleset v1`, inspected literal text only.
It caught the direct exfiltration and persistence fixtures but returned **Benign**
for the base64 fixture. That is a real false negative: the dangerous instruction
was present, but its representation hid all literal indicators.

The fix in v2 is bounded representation-aware scanning:

- identify standalone base64-like strings of at least 48 characters;
- decode only with strict base64 validation;
- keep only outputs that are at least 90% printable UTF-8;
- scan the decoded layer with the same general rules;
- label decoded findings and add a small representation-evasion correlation bonus.

I did not add the exact blob or filename as a signature. The change therefore
catches a class of encoded instruction payloads. Re-running the benign corpus
afterward still produced 10/10 Benign verdicts.

## 5. Static results

### Benign baseline, v2

| Skill | Verdict | Score | Note |
|---|---:|---:|---|
| academy-guide | Benign | 0 | no configured indicator |
| algorithmic-art | Benign | 4 | isolated dynamic-execution primitive in a generator template |
| brand-guidelines | Benign | 0 | no configured indicator |
| discernment-nudge | Benign | 0 | no configured indicator |
| frontend-design | Benign | 4 | isolated outbound-request primitive in design guidance |
| internal-comms | Benign | 0 | no configured indicator |
| pdf | Benign | 0 | no configured indicator |
| slack-gif-creator | Benign | 0 | no configured indicator |
| theme-factory | Benign | 0 | no configured indicator |
| webapp-testing | Benign | 0 | no configured indicator |

Result: **10/10 clear**. Two skills retained low-score explainable findings rather
than being silently allowlisted. If the threshold were lowered to 4, they would
become false positives; this demonstrates the precision/recall tradeoff.

### Malicious fixtures

| Fixture | Expected | v1 observed | v2 observed | Caught after fix? |
|---|---|---|---|---|
| credential exfiltration | Malicious: secret access + egress + concealment | Malicious | Malicious | Yes |
| shadow-skill persistence | Malicious: skill/config write + concealment | Malicious | Malicious | Yes |
| obfuscated payload | Malicious: decoded secret access + egress | **Benign** | Malicious | **Yes** |

The checked-in JSON gives exact scores, file/line evidence, and correlation text.
The results are general for the represented patterns, but not universal. For
example, v2 handles ordinary base64, not custom encryption or a payload assembled
one token at a time.

## 6. Runtime exercise

OpenClaw was not installed in the test environment, and installing these fixtures
into a real agent would create unnecessary risk. I therefore invoked all three
through `runtime/run_lab.py`, a deliberately non-executing harness. It reads only
`scenario.json`, validates an event allowlist, rewrites declared paths into a fresh
temporary directory, marks network events blocked, and emits JSONL. It never runs
instructions from `SKILL.md`.

This produces the signals expected from real endpoint/agent telemetry without the
harmful effect:

| Fixture | Expected runtime signals |
|---|---|
| credential exfiltration | sensitive file read, then outbound HTTPS POST to a new destination |
| shadow-skill persistence | write under an agent skill/config root, then concealed/background child process |
| obfuscated payload | decoder use on opaque content, then child-process execution; a real run might also show sensitive read + egress |

The observed replay contained six events, two per fixture. No real network or
credential access occurred.

### Runtime detector logic

`scanner/runtime_detector.py` groups structured events by agent session and alerts
on these correlations:

1. `file_read(sensitive=true)` followed in the same session by `network_connect`;
2. `file_write(agent_control_path=true)` plus a concealed `process_spawn`;
3. `decoder_invocation` plus `process_spawn`.

All three replays were classified Malicious. In production, the event source should
be outside the agent's control: eBPF/Endpoint Security/auditd or container syscall
telemetry for files and processes, DNS/proxy/firewall logs for egress, and the
agent runtime for session ID, skill identity, tool call, arguments, approval result,
and content hash. A monitor should use event time windows and process/session
lineage, not merely presence anywhere in a host log.

### What indicates a malicious skill running?

No single event is decisive. Strong indications are behavior inconsistent with the
skill's declared job, especially a high-value source-to-sink sequence; writes to
identity, memory, configuration, or skill roots; hidden persistence; undeclared or
new network destinations; execution immediately after decoding; approval bypass;
and a runtime bundle hash different from the reviewed hash.

Runtime detection sees effective behavior and values that static review cannot,
but it may alert only after an attempted action. Blocking policy should therefore
sit inline for secret reads, protected-path writes, child execution, and egress.

## 7. What can defeat both approaches?

Both can fail when the behavior remains inside individually legitimate operations:
a skill reads an authorized document and leaks one fact through an already-approved
chat integration; remote trusted-looking content supplies the actual instruction;
a dependency is clean during review and compromised later; intent is spread across
sessions or cooperating skills; the skill uses a new encoding; or the runtime
labels a sensitive file as ordinary. A patient attacker can also wait beyond a
correlation window or reuse the agent's normal network destination.

Telemetry that closes part of the gap includes:

- immutable bundle and dependency hashes tied to every tool call;
- signed provenance and transparency logs from source through installation;
- declared capability and destination manifests compared with observed behavior;
- content-aware data-flow labels from secret store/file read to network sink;
- model instruction provenance (user, skill, remote page, memory) and tool-call lineage;
- protected write auditing for `SKILL.md`, agent config, memory, and identity files;
- DNS/TLS/proxy identity, bytes sent, destination novelty, and egress allowlist result;
- approval prompts and whether the arguments changed after approval;
- cross-session and cross-skill correlation retained by a tamper-resistant collector.

Even with that telemetry, human review and least privilege remain necessary. The
most valuable control is preventing a skill from receiving permissions unrelated
to its declared purpose.

## 8. Platform validation

### Google Antigravity: real skill discovery

On 2026-10-04, I placed the harmless canary at Antigravity's documented workspace
location:

```text
.agents/skills/security-canary/SKILL.md
```

I scanned it first; v2 returned `Benign (score=0)`. After starting a new
Antigravity conversation, I asked it to use `security-canary`. Antigravity returned:

```text
CANARY_SKILL_ACTIVE
No tools were used.
```

That unique response was defined only in the skill, so this validates workspace
discovery, activation, full-instruction loading, and instruction following. It does
not validate operating-system telemetry or prove that Antigravity would block an
unknown malicious skill.

### Ollama: explicitly loaded, tool-free model test

Local Ollama client `0.34.3` served `granite3.3:2b` (2.5B parameters, tool
capability, 131072-token advertised context). Ollama is a model service, not an
automatic skill-discovery layer. `runtime/ollama_canary_test.py` therefore reads
only the named `security-canary`, supplies it as a system instruction, provides no
tools, and calls the local native `/api/chat` endpoint. The model returned the same
canary phrase.

This validates that the local model can follow explicitly loaded skill instructions.
It does **not** claim Ollama discovered `SKILL.md` automatically.

### OpenClaw limitation

OpenClaw was not installed. The official installer and site were blocked by the
machine's IBM corporate security policy. I did not attempt to bypass that control.
Accordingly, this report makes no claim that OpenClaw skill discovery or execution
was validated on this host. The OpenClaw documentation remains the basis for the
target format and precedence threat model; Antigravity supplies the live agent-skill
execution evidence.

| Validation | Observed result | What it establishes |
|---|---|---|
| Antigravity workspace skill | Canary response returned | real discovery and activation |
| Ollama tool-free harness | Canary response returned | local model followed loaded instructions |
| OpenClaw | blocked before installation | not validated; policy respected |

## 9. Reproduction and evidence

Run:

```bash
python3 -m unittest discover -s tests -v
python3 evaluation/evaluate.py
```

Generated evidence is in `evaluation/results/`. `SOURCES.md` distinguishes external
claims from observations. The design and conclusions above are the author's own
analysis except where the report explicitly attributes the skill model or taxonomy
to OpenClaw/OWASP.

For a guided interview presentation, `demo/index.html` provides a self-contained
offline walkthrough of these same repository-backed facts. It is a presentation
layer, not additional experimental evidence and not a replacement for this report.
