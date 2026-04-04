---
name: consult-codex
description: "Multi-turn consultation with Codex CLI for second opinions, brainstorming, or collaborative problem-solving. Use when the user asks to \"consult codex\", \"ask codex\", \"get codex's opinion\", \"brainstorm with codex\", \"discuss with codex\", or \"chat with codex\"."
---

# Consult Codex

Multi-turn consultation with Codex CLI. Maintains a conversation across multiple turns using session persistence, unlike single-shot `/codex-exec`.

## Step 1: Gather Context

Identify the 2-5 files most relevant to the problem. Formulate a clear, specific question. Include what has been tried and relevant constraints.

## Step 2: Start Session

Run `codex exec` with `-o` to capture the response cleanly. Default to `-s read-only` for safety. Use `-s workspace-write` when the consultation requires running code or reading files outside the workspace.

**All `codex` Bash calls require `dangerouslyDisableSandbox: true`** (network access to OpenAI API). Use `.turbo/` as the temp directory — it is in the working directory (sandbox-writable), gitignored, and avoids `$TMPDIR` path mismatches between sandbox and non-sandbox mode.

Generate a random session tag at the start to keep files unique for parallel use:

```bash
CODEX_TAG=$(head -c 4 /dev/urandom | xxd -p) && mkdir -p .turbo/codex
codex exec -s read-only -o ".turbo/codex/$CODEX_TAG.txt" "<question with full context>"
```

### Prompt Shaping

Structure the question using XML tags for clearer Codex responses:

- `<task>`: The concrete question and relevant context.
- `<compact_output_contract>`: Desired output shape and brevity requirements.
- `<structured_output_contract>`: Same purpose but for structured/schema responses.
- `<grounding_rules>`: When claims must be evidence-based (review, research, root-cause analysis).
- `<dig_deeper_nudge>`: Push past surface-level findings to check for second-order failures.
- `<verification_loop>`: When correctness matters — ask Codex to verify before finalizing.

Example prompt for a diagnosis question:

```
<task>Diagnose why the auth middleware rejects valid tokens after the session refactor.</task>
<compact_output_contract>Return: (1) most likely root cause, (2) evidence, (3) smallest safe next step.</compact_output_contract>
<grounding_rules>Ground every claim in the provided context or tool outputs. Label hypotheses explicitly.</grounding_rules>
```

For correctness-critical questions, add `<verification_loop>` asking Codex to verify its answer before finalizing.

Keep prompts compact. Prefer tighter output contracts over raising reasoning effort. One clear task per Codex turn.

For long context that won't fit inline, write a context file and pipe it via stdin. The prompt stays as the argument, context pipes in as `<stdin>` automatically:

```bash
cat > ".turbo/codex/$CODEX_TAG-ctx.txt" << 'EOF'
<long context here>
EOF
cat ".turbo/codex/$CODEX_TAG-ctx.txt" | codex exec -s read-only -o ".turbo/codex/$CODEX_TAG.txt" "<question>"
```

Parse the `session id:` line from the CLI output. This UUID is needed for follow-up turns.

Use a generous timeout (30 minutes / 1800000ms per turn).

## Step 3: Read and Evaluate Response

The `-o` file contains only Codex's response (cleaner than stdout, which includes CLI chrome and tool-use logs). Read from `.turbo/codex/$CODEX_TAG.txt`. If the output is too large for the Read tool, read stdout from the Bash tool result instead.

Assess whether:
- The answer is sufficient and actionable
- Follow-up questions would improve the answer
- The response contradicts known project facts (verify before accepting)

If no follow-up is needed, skip to the Synthesize step.

## Step 4: Follow Up

Resume the session with the parsed session ID (not `--last`, which is unsafe for parallel use):

```bash
codex exec resume <session-id> -o ".turbo/codex/$CODEX_TAG.txt" "<follow-up question>"
```

The `-s` flag is not available for `resume`. It inherits sandbox settings from the original session.

Return to Step 3. Cap at 5 turns to prevent runaway conversations.

## Step 5: Synthesize

Summarize the key insights from the consultation. Cross-reference suggestions with project documentation and conventions before applying. Codex suggestions are starting points, not guaranteed solutions.
