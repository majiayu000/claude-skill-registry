---
name: runtime-hal
description: Runtime HAL for multi-runtime agent orchestration. Detects active AI assistant (Claude Code, Codex, Gemini, Cursor) and exposes uniform interface for startup injection, GUPP enforcement, and communication selection.
---

# Runtime HAL

Hardware Abstraction Layer for AI coding assistant runtimes. The HAL detects which runtime environment is active and provides a uniform interface so that every other skill in the Gastown chipset can operate identically regardless of runtime. This mirrors Gastown's `internal/runtime/runtime.go` provider abstraction, where the Go binary auto-detects its host environment and adapts its hook, nudge, and session strategies accordingly.

In the chipset hardware metaphor, the Runtime HAL is the **BIOS/UEFI firmware layer**. Real firmware probes hardware on boot, detects what peripherals exist, and presents a uniform interface to the operating system. The HAL does the same: it probes the runtime on activation, detects what capabilities exist (hooks, session IDs, context forking), and presents a uniform interface to the chipset's skills and agents.

## Activation Triggers

This skill activates when the task involves:

- Determining which AI coding assistant runtime is active
- Selecting a startup injection strategy for an agent
- Choosing a GUPP enforcement mechanism (hooks vs polling vs preamble)
- Configuring stall detection thresholds or nudge intervals
- Adapting behavior based on runtime capabilities (hooks, context fork, session ID)
- Debugging why an agent is not receiving hooks or nudges

## HAL Interface

The HAL exposes a uniform interface that other skills consume. No skill outside the HAL should inspect environment variables, probe the filesystem for runtime indicators, or check the process tree directly.

```typescript
interface RuntimeHAL {
  // Detection
  detectProvider(): RuntimeProvider;

  // Startup
  getStartupStrategy(): StartupStrategy;
  getStartupCommands(role: AgentRole): string[];

  // Communication capabilities
  supportsHooks(): boolean;
  supportsNudge(): boolean;
  getSessionId(): string | null;

  // GUPP enforcement
  getGUPPStrategy(): GUPPStrategy;
  getStallThreshold(): number;   // seconds before declaring an agent stalled
  getNudgeInterval(): number;    // seconds between nudge pings
}
```

### Types

```typescript
type RuntimeProvider = 'claude' | 'codex' | 'gemini' | 'cursor' | 'unknown';
type StartupStrategy = 'hook_injection' | 'startup_fallback' | 'polling';
type GUPPStrategy = 'hook_injection' | 'prompt_preamble' | 'polling';
```

These types are also declared in the shared Gastown type system at `src/chipset/gastown/types.ts`. The HAL consumes `AgentRole` from the same module when generating startup commands.

## Provider Detection

Detection runs once at activation time and caches the result. The detection cascade follows Gastown's `runtime.go` pattern, which tries the most specific signal first and falls through to progressively weaker indicators.

### Detection Cascade

**Step 1: Explicit override via GT_RUNTIME environment variable**

If `GT_RUNTIME` is set, use its value directly. This allows operators to force a specific provider during testing, CI, or when running inside a container where other signals are absent.

```
GT_RUNTIME=claude  -> RuntimeProvider = 'claude'
GT_RUNTIME=codex   -> RuntimeProvider = 'codex'
GT_RUNTIME=gemini  -> RuntimeProvider = 'gemini'
GT_RUNTIME=cursor  -> RuntimeProvider = 'cursor'
```

Any unrecognized value maps to `'unknown'`.

**Step 2: Check CLAUDE_SESSION_ID environment variable**

Claude Code sets `CLAUDE_SESSION_ID` for every active session. If this variable is present and non-empty, the runtime is Claude Code.

```
CLAUDE_SESSION_ID exists && non-empty -> RuntimeProvider = 'claude'
```

**Step 3: Check for .claude/settings.json in workspace**

If the workspace root contains `.claude/settings.json`, this strongly indicates a Claude Code environment. This catches cases where the session ID variable is not yet propagated (e.g., hook execution before session fully initializes).

```
.claude/settings.json exists -> RuntimeProvider = 'claude'
```

**Step 4: Check process tree for known runtime binaries**

Inspect the process tree for known executable names:

| Binary | Provider |
|--------|----------|
| `claude` | `claude` |
| `codex` | `codex` |
| `gemini` | `gemini` |
| `cursor` | `cursor` |

This step is the least reliable (binary names can change across versions) and serves as a last-resort heuristic before falling back.

**Step 5: Fall back to 'unknown'**

If no signal matches, the provider is `'unknown'`. The HAL selects the `polling` strategy for both startup and GUPP. This ensures graceful degradation: no crash, no hang, no error. The chipset operates in a reduced-capability mode where hooks are unavailable but work items still flow through periodic filesystem polling.

### Detection Summary

```
GT_RUNTIME set?
  yes -> use GT_RUNTIME value
  no  -> CLAUDE_SESSION_ID set?
           yes -> 'claude'
           no  -> .claude/settings.json exists?
                    yes -> 'claude'
                    no  -> process tree matches known binary?
                             yes -> matched provider
                             no  -> 'unknown'
```

## Provider Capabilities Matrix

| Capability | Claude Code | Codex | Gemini | Cursor | Unknown |
|---|---|---|---|---|---|
| Session hooks | Yes | No | No | Partial | No |
| Context fork | Yes | No | No | Yes | No |
| Session ID env var | CLAUDE_SESSION_ID | GT_SESSION_ID | GT_SESSION_ID | None | None |
| Startup injection | SessionStart hook | gt prime fallback | gt prime fallback | Command palette | Polling |
| GUPP strategy | hook_injection | startup_fallback | polling | prompt_preamble | polling |
| Stall threshold | 120s | 180s | 300s | 120s | 300s |
| Nudge interval | 30s | 60s | 120s | 30s | 120s |
| Nudge support | Yes (filesystem) | Yes (filesystem) | Yes (filesystem) | Limited | Yes (filesystem) |

## Startup Strategies

The HAL selects a startup strategy based on the detected provider. Startup strategy determines how an agent receives its initial context (role, work item, GUPP rules) when it is spawned.

### hook_injection (Claude Code)

Claude Code supports `.claude/settings.json` hooks that fire on session events. The mayor writes a `SessionStart` hook entry that injects the agent's role, assigned bead, and GUPP rules into the session context before the agent's first prompt. This is the highest-fidelity strategy: the agent starts with full context and never needs to poll for its assignment.

```
Mayor writes hook -> Agent starts -> SessionStart fires -> Context injected
```

### startup_fallback (Codex)

Codex does not support hooks. Instead, the mayor writes the agent's assignment to a known filesystem path, then starts the agent with a `gt prime` command that reads the assignment file on startup. The agent receives its context through command-line injection rather than hook callbacks.

```
Mayor writes assignment file -> gt prime starts agent -> Agent reads file -> Context loaded
```

### polling (Gemini, Unknown)

For runtimes without hooks or startup injection, the agent starts with a generic context and immediately enters a polling loop, checking `state/hooks/{agentId}.json` at the configured nudge interval until it finds an assignment. This is the slowest strategy but requires zero runtime-specific integration.

```
Agent starts generic -> Polls hook file -> Finds assignment -> Context loaded
```

## GUPP Strategies

GUPP (Guided Unsupervised Parallel Processing) enforcement varies by runtime capability. The HAL selects the most reliable GUPP mechanism available.

### hook_injection (Claude Code)

GUPP rules are injected via hooks into the agent's session context. The agent operates under GUPP constraints enforced by the runtime itself. Stall detection works through hook callbacks: if the agent's `lastActivity` timestamp in the hook state exceeds the stall threshold, the witness raises an alert.

### startup_fallback (Codex)

GUPP rules are baked into the agent's startup context via the `gt prime` command. The agent cannot modify its own GUPP constraints after startup. Stall detection relies on filesystem observation: the witness watches for changes in `state/hooks/{agentId}.json` and triggers if the file's modification time exceeds the threshold.

### prompt_preamble (Cursor)

GUPP rules are prepended to the agent's prompt context via the command palette integration. This is less reliable than hook injection because the agent can potentially ignore preamble instructions. Stall detection works identically to the startup_fallback case.

### polling (Gemini, Unknown)

GUPP rules are written to the hook state file. The agent polls for both work assignments and GUPP constraint updates. This is the most robust fallback: it requires no runtime-specific integration, but introduces latency equal to the nudge interval. Stall detection is inherent in the polling mechanism: if the agent stops polling (no reads on the hook file), it is stalled.

## Error Handling

### Unknown Provider Behavior

When the provider is `'unknown'`, the HAL guarantees:

1. **No crash** -- all interface methods return valid defaults
2. **No hang** -- polling uses bounded intervals, never blocks indefinitely
3. **No error thrown** -- `detectProvider()` always returns a valid RuntimeProvider
4. **Reduced capability** -- hooks unavailable, startup uses polling, GUPP uses polling
5. **Operational** -- work items still flow; agents still execute; merges still happen

This is the fundamental contract: the chipset degrades gracefully, never catastrophically.

### Detection Failure Recovery

If detection throws an exception (corrupted settings file, permission denied on process tree), the HAL catches the error, logs a warning, and returns `'unknown'`. No detection failure propagates to calling skills.

### Session ID Absence

If `getSessionId()` returns `null`, the calling skill must not assume hooks are unavailable. Some runtimes set the session ID asynchronously. The HAL uses the full detection cascade (not just session ID) to determine capabilities.

## Integration with Other Gastown Skills

| Skill | How It Uses the HAL |
|-------|-------------------|
| `mayor-coordinator` | Calls `getStartupStrategy()` and `getStartupCommands()` when spawning polecats |
| `polecat-worker` | Calls `getGUPPStrategy()` to know how GUPP rules are enforced |
| `witness-observer` | Calls `getStallThreshold()` and `getNudgeInterval()` for monitoring timers |
| `nudge-sync` | Calls `supportsNudge()` to decide whether to send filesystem nudges |
| `hook-persistence` | Calls `supportsHooks()` to decide whether to write hook state files |
| `beads-state` | Uses `getSessionId()` to tag work items with the active session |

No skill outside the HAL should perform its own runtime detection. If a skill needs to know the runtime, it calls `detectProvider()`. If it needs to know whether hooks work, it calls `supportsHooks()`. The HAL is the single source of truth for runtime capabilities.

## Boundary: What the HAL Does NOT Do

The HAL NEVER:

- **Executes work** -- it detects the runtime and exposes capabilities; it does not perform orchestration
- **Writes hook state files** -- that is the responsibility of `hook-persistence` and `beads-state`
- **Sends messages** -- that is the responsibility of `mail-async` and `nudge-sync`
- **Monitors agents** -- that is the responsibility of `witness-observer`
- **Makes dispatch decisions** -- that is the responsibility of `mayor-coordinator`

The HAL is a detection and capability layer. It answers "what can this runtime do?" but never "what should we do?"

## Configuration Override

Operators can override HAL defaults via environment variables:

| Variable | Purpose | Example |
|----------|---------|---------|
| `GT_RUNTIME` | Force a specific provider | `GT_RUNTIME=codex` |
| `GT_STALL_THRESHOLD` | Override stall detection (seconds) | `GT_STALL_THRESHOLD=240` |
| `GT_NUDGE_INTERVAL` | Override nudge interval (seconds) | `GT_NUDGE_INTERVAL=45` |
| `GT_GUPP_STRATEGY` | Force a GUPP strategy | `GT_GUPP_STRATEGY=polling` |

Overrides take precedence over provider defaults but not over structural impossibilities (e.g., forcing `hook_injection` on Codex will not make hooks appear).

## References

- `references/gastown-origin.md` -- How this skill maps to Gastown's internal/runtime/runtime.go
- `providers/claude-code.md` -- Claude Code provider details and hook integration
- `providers/codex.md` -- Codex provider details and startup fallback
- `providers/fallback.md` -- Generic fallback provider for unknown runtimes
