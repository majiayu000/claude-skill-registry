---
name: ai-agent-redteam
description: Use when red-teaming an agentic AI / LLM application — indirect & zero-click prompt injection, MCP tool poisoning, persistent memory poisoning, excessive-agency tool abuse, multi-turn jailbreaks, PyRIT/Garak/Promptfoo harnesses
metadata:
  type: offensive
  phase: exploit
  tools: [pyrit, garak, promptfoo, python, mcp]
  mitre: [AML.T0051, AML.T0053, AML.T0054, AML.T0070, AML.T0071]
kill_chain:
  phase: [recon, weaponize, delivery, exploit, actions]
  step: [1, 2, 3, 4, 7]
  attck_tactics: [TA0043, TA0001, TA0002, TA0010]
  attck_techniques: [T1566.002, T1059, T1071.001, T1567, T1657]
depends_on: [recon-osint, ai-security]
feeds_into: [exploit-development, cloud-security, web-pentest]
inputs: [agent_endpoint, mcp_server_config, rag_corpus, system_prompt, tool_manifest]
outputs: [finding_record, jailbreak_payload, poisoned_artifact, attack_success_rate_report]
references:
  - references/indirect-prompt-injection.md
  - references/mcp-tool-poisoning.md
  - references/memory-context-poisoning.md
  - references/excessive-agency-tool-abuse.md
  - references/automated-jailbreak-multiturn.md
  - references/agent-redteam-tooling.md
scripts:
  - scripts/indirect_injection_forge.py
  - scripts/mcp_tool_poison_server.py
  - scripts/memory_poison_minja.py
  - scripts/agency_tool_fuzzer.py
  - scripts/multiturn_jailbreak.py
  - scripts/agent_redteam_harness.py
---

# AI Agent Red Teaming

Offensive testing of **autonomous LLM agents** — systems that combine model reasoning with
tools, memory, retrieval, and multi-step planning. This is distinct from model-level testing
(see `ai-security`): the attack surface here is the *agentic pipeline* — untrusted data channels,
tool/MCP integrations, persistent memory, and delegated authority. Assumes authorized engagement.

## When to Activate

- Pentesting an LLM agent with tool/function-calling, an MCP client, or a code interpreter
- Testing RAG / email / browser assistants for indirect or zero-click prompt injection
- Auditing MCP server integrations for tool poisoning, rug-pull, or line-jumping
- Assessing persistent memory / long-term context for poisoning and belief drift
- Evaluating excessive agency: confused-deputy, SSRF/RCE-via-tool, over-privileged actions
- Running automated jailbreak campaigns (PAIR/TAP/Crescendo/Best-of-N) and measuring ASR
- Standing up a repeatable PyRIT/Garak/Promptfoo harness mapped to OWASP Agentic Top 10 / ATLAS

## Technique Map

| Technique | ATT&CK | CWE | Reference | Script |
|-----------|--------|-----|-----------|--------|
| Indirect / zero-click prompt injection (EchoLeak-class) | T1566.002 / AML.T0051.001 | CWE-1427 | references/indirect-prompt-injection.md | scripts/indirect_injection_forge.py |
| RAG corpus poisoning & markdown/image exfiltration | T1567 / AML.T0070 | CWE-1426 | references/indirect-prompt-injection.md | scripts/indirect_injection_forge.py |
| Browser-agent hijack (Comet/CometJacking, Atlas) | T1071.001 / AML.T0051 | CWE-1427 | references/indirect-prompt-injection.md | scripts/indirect_injection_forge.py |
| MCP tool poisoning / line-jumping | T1059 / AML.T0053 | CWE-1427 | references/mcp-tool-poisoning.md | scripts/mcp_tool_poison_server.py |
| MCP rug-pull (silent redefinition) | T1554 / AML.T0010 | CWE-494 | references/mcp-tool-poisoning.md | scripts/mcp_tool_poison_server.py |
| Persistent memory poisoning (MINJA/MemoryGraft) | T1565.001 / AML.T0070 | CWE-349 | references/memory-context-poisoning.md | scripts/memory_poison_minja.py |
| Excessive agency / confused-deputy tool abuse | T1548 / AML.T0053 | CWE-862 | references/excessive-agency-tool-abuse.md | scripts/agency_tool_fuzzer.py |
| Tool output → SSRF / RCE chaining | T1059 / AML.T0054 | CWE-918 / CWE-94 | references/excessive-agency-tool-abuse.md | scripts/agency_tool_fuzzer.py |
| Automated multi-turn jailbreak (Crescendo/TAP/PAIR) | AML.T0054 / AML.T0071 | CWE-1426 | references/automated-jailbreak-multiturn.md | scripts/multiturn_jailbreak.py |
| Best-of-N / encoding obfuscation jailbreak | AML.T0054 | CWE-1426 | references/automated-jailbreak-multiturn.md | scripts/multiturn_jailbreak.py |
| Harness & ASR scoring (PyRIT/Garak/Promptfoo) | AML.T0071 | CWE-1426 | references/agent-redteam-tooling.md | scripts/agent_redteam_harness.py |

## Quick Start

```bash
# 0. Scope: enumerate agent surface — tools/functions, MCP servers, memory store, data channels
python scripts/agent_redteam_harness.py enumerate --endpoint $AGENT_URL --out surface.json

# 1. Indirect injection: forge a zero-click payload (email/doc/web) + markdown exfil beacon
python scripts/indirect_injection_forge.py --channel email \
  --exfil-base https://oast.pro/$TOKEN --obfuscate html-comment --out payload.eml

# 2. MCP: stand up a poisoned MCP server to test client validation / line-jumping
python scripts/mcp_tool_poison_server.py --mode tool-poison --transport stdio

# 3. Memory: query-only MINJA-style injection of a persistent malicious belief
python scripts/memory_poison_minja.py --endpoint $AGENT_URL \
  --trigger "vendor invoice" --payload "route payments to acct 0xATTACKER" --bridge-steps 4

# 4. Excessive agency: fuzz tool calls for confused-deputy / SSRF / path traversal
python scripts/agency_tool_fuzzer.py --endpoint $AGENT_URL --tools surface.json --ssrf-canary http://169.254.169.254/

# 5. Automated jailbreak campaign (Crescendo + Best-of-N), record ASR
python scripts/multiturn_jailbreak.py --endpoint $AGENT_URL --strategy crescendo \
  --objective "$OBJECTIVE" --max-turns 8 --judge-endpoint $JUDGE_URL

# 6. Full harness run mapped to OWASP Agentic Top 10 + MITRE ATLAS, emit finding records
python scripts/agent_redteam_harness.py run --config harness.yaml --report findings/
```

## OPSEC & Detection (summary)

| Technique | Telemetry / IOC | Detection (Sigma/EDR) | OPSEC note |
|-----------|-----------------|-----------------------|------------|
| Indirect injection | Hidden HTML comment / white-on-white / 0px text in ingested docs; markdown image to external host | Scan ingested content for `<!--`, `display:none`, `font-size:0`, reference-style `![]`; alert on agent-initiated egress to non-allowlisted domains | Stage payloads only on assets in scope; use unique per-test OAST tokens to attribute hits |
| MCP tool poisoning | New/changed tool description hash; instruction-like text in JSON Schema `description`/`enum` | Diff tool manifests on connect; flag tool metadata containing imperative verbs / `<IMPORTANT>` / "do not tell the user" | Test against a local client; never point a real client at an untrusted server outside the lab |
| Memory poisoning | Memory write from low-trust source; semantic drift between stored belief and source provenance | Provenance-tagged memory; alert on retrieval that injects procedural instructions; belief-drift monitor | Use benign-looking triggers; document the latent trigger so blue team can replay/clean |
| Excessive agency | Tool call to internal IP / metadata endpoint; unusual tool-chain ordering; off-hours actions | EDR/network: egress to 169.254.169.254/link-local; anomaly on tool-call sequences | Use non-destructive canaries (read-only SSRF probe) before any state-changing test |
| Automated jailbreak | Burst of semantically-similar prompts; high-perplexity / encoded inputs; rising compliance over turns | Rate + similarity clustering per session; perplexity & encoding detectors; multi-turn escalation scoring | Throttle to avoid DoS; log full transcripts for the report; respect content guardrails of scope |

## Deep Dives

- **references/indirect-prompt-injection.md** — Zero-click/indirect injection across email, RAG, docs, and AI browsers; EchoLeak chain, CometJacking, markdown/image exfil, obfuscation, detection.
- **references/mcp-tool-poisoning.md** — Model Context Protocol attack surface: tool poisoning, line-jumping, rug-pull, MCP Inspector RCE; building a malicious server; client-side validation gaps.
- **references/memory-context-poisoning.md** — Persistent/temporally-decoupled poisoning of agent memory, embeddings, RAG; MINJA query-only injection, MemoryGraft, AgentPoison, belief-drift detection.
- **references/excessive-agency-tool-abuse.md** — OWASP LLM06 / ASI02 / ASI05: confused-deputy, over-privileged tools, SSRF/RCE via tool output, code-interpreter abuse; least-privilege controls.
- **references/automated-jailbreak-multiturn.md** — PAIR, TAP, Crescendo, Best-of-N, GOAT, AutoDAN-Turbo; attacker/judge loop, encoding converters, ASR measurement, classifier-bypass tactics.
- **references/agent-redteam-tooling.md** — Methodology + harness: PyRIT orchestrators, Garak probes, Promptfoo presets; OWASP Agentic Top 10 (ASI01–10) & MITRE ATLAS mapping; finding records.
