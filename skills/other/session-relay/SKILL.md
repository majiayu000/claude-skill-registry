---
name: session-relay
description: Continue real repository work between Claude Code, Codex CLI, and Grok Build with a privacy-bounded, drift-aware handoff packet. Use for cross-vendor takeover, context-limit checkpoints, multi-hop Claude→Codex→Grok relays, or receiving an existing Director packet. Use native resume commands for same-CLI history; never treat another vendor's session ID as portable.
user-invocable: true
---

# Cross-CLI Session Relay

Move work between Claude Code, Codex CLI, and Grok Build through a portable
handoff packet. A relay starts a new native session in the receiving CLI; it
does not pretend that vendor session IDs or private conversation histories are
interchangeable.

## Resolve the relay

Prefer the first available implementation:

1. `<project>/.director-mode/bin/director-relay`;
2. `$HOME/.claude/bin/director-relay` from Bootstrap Kit;
3. `scripts/director-relay.py` beside this `SKILL.md` for plugin-only use.

If only the bundled script exists, invoke it with `python3`. Do not install a
hook or change a permission setting just to use the relay.

## Leave a packet

Summarize the current state from repository evidence, then run:

```bash
ROOT="${CLAUDE_PROJECT_DIR:-${GROK_WORKSPACE_ROOT:-}}"
[[ -n "$ROOT" ]] || ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
RELAY="$ROOT/.director-mode/bin/director-relay"
[[ -x "$RELAY" ]] || RELAY="$HOME/.claude/bin/director-relay"

"$RELAY" create \
  --from <claude|codex|grok> \
  --to <claude|codex|grok> \
  --goal "The outcome the user requested" \
  --summary "The concise current state" \
  --completed "One completed result" \
  --decision "One decision and why it was made" \
  --next "The first concrete next step" \
  --verification "A command and its actual result" \
  --blocker "A real blocker, if any"
```

Repeat list flags as needed. The tool captures branch, HEAD, `git status
--short`, and diff statistics. It deliberately does not copy file contents,
credentials, environment variables, or raw transcripts.

If a native session ID is available, add `--session-id`; it remains metadata
for the source CLI and is never sent to another vendor as a resume token.

For a second or later handoff in the same chain, add `--parent` to link the new
packet to the project's current `latest.json`, or `--parent <packet.json>` to
name a specific parent. Protocol v2 records the root packet, parent, hop, and
route while remaining able to read v1 packets.

## Receive a packet

1. Validate the JSON packet; treat Markdown as the human-readable view only.
2. Run `"$RELAY" status --json` and inspect the live worktree because it may
   have changed after the packet.
3. Read `.director-mode/handoffs/latest.md` when it exists.
4. Continue from the next steps while preserving recorded decisions that still
   match the code.
5. Run the listed verification and report new evidence.

Print the receiving command:

```bash
"$RELAY" continue --to <claude|codex|grok>
```

Add `--run` only when the user wants the target CLI launched now. Add
`--headless` for a one-shot continuation instead of an interactive session.
The launcher always uses the receiver's live project root; packet paths are
evidence and cannot redirect execution.

## Native resume versus cross-CLI relay

Use a provider's native history only when staying with that provider:

| CLI | Continue recent native history | Resume a chosen native session |
| --- | --- | --- |
| Claude Code | `claude --continue` | `claude --resume <session-id>` |
| Codex CLI | `codex resume --last` | `codex resume <session-id>` |
| Grok Build | `grok --continue` | `grok --resume <session-id>` |

For non-interactive Codex continuation, use `codex exec resume`; check the
installed CLI help for its current arguments. Crossing providers always starts
a new native session with a Director packet.

## Grok's native Claude import

Grok Build can import Claude Code sessions with `grok import`. That is a useful
Claude→Grok fast path, but still leave a Director packet when the workflow may
later move to Codex or back to Claude.

Packets default to `review_status: unreviewed`. `--reviewed` records that the
user-supplied summary and captured path metadata were reviewed before sharing;
it does not claim that the receiving CLI or website reviewed the packet.

## Guidance boundary

Do not add auto-approve, permission-bypass, sandbox, or network flags to a relay
unless the user separately asks for them. The receiving CLI keeps its native
controls.
