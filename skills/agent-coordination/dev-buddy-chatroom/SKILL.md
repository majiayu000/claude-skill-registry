---
name: dev-buddy-chatroom
description: PK Stage — multi-AI competitive debate with iterative consensus. Sends a topic to all configured AI participants simultaneously, synthesizes the best approach, then iterates until consensus or max rounds.
user-invocable: true
allowed-tools: Read, Bash, Task, TaskOutput, AskUserQuestion, Glob, Grep
---

# PK Stage — Multi-AI Competitive Debate

Fan out a topic to ALL configured AIs + Claude simultaneously, synthesize the best approach, iterate until consensus.

**Usage:** `/dev-buddy-chatroom <topic or question>`

**Config:** `~/.vcp/dev-buddy-chatroom.json` — use `/dev-buddy-config` web portal or edit manually.

**Plan mode:** This skill can run in plan mode. Participants are instructed to only read and analyze (not modify files), but this is prompt-level enforcement only — see Known Limitation #1. Use it to gather multi-AI perspectives before finalizing a plan.

---

## Step 1: Parse & Load Config

Extract the user's topic from the arguments after the skill trigger.

Load and validate the chatroom config:

```bash
bun -e "
import { loadChatroomConfig } from '${CLAUDE_PLUGIN_ROOT}/scripts/chatroom-config.ts';
import { readPresets } from '${CLAUDE_PLUGIN_ROOT}/scripts/preset-utils.ts';
import { validateChatroomConfig } from '${CLAUDE_PLUGIN_ROOT}/scripts/chatroom-config.ts';
const config = loadChatroomConfig();
const presets = readPresets();
const err = validateChatroomConfig(config, presets);
if (err) { console.error('CONFIG ERROR: ' + err); process.exit(1); }
console.log(JSON.stringify({
  participants: config.participants.map((p, i) => ({
    index: i,
    system_prompt: p.system_prompt || '',
    preset: p.preset,
    model: p.model,
    type: presets.presets[p.preset]?.type || 'unknown',
    timeout_ms: presets.presets[p.preset]?.timeout_ms
  })),
  max_rounds: config.max_rounds
}));
"
```

If config error or no participants: report error to user and stop.

**Resolve session variables:**

1. Resolve tmpdir:
   ```bash
   bun -e "console.log(require('os').tmpdir())"
   ```
   Store result as `{TMPDIR}`.

2. Compute project hash:
   ```bash
   bun -e "const c=require('crypto');console.log(c.createHash('sha256').update(process.env.CLAUDE_PROJECT_DIR||process.cwd()).digest('hex').slice(0,8))"
   ```
   Store result as `{PROJHASH}`.

3. Generate random suffix:
   ```bash
   bun -e "console.log(require('crypto').randomBytes(2).toString('hex'))"
   ```
   Store result as `{RAND}`.

4. Generate session ID: `{PROJHASH}-{Date.now()}-{RAND}` → store as `{SESSION_ID}`

5. Assign each participant a zero-based index: `p0`, `p1`, `p2`, ...

6. Ensure output directory exists:
   ```bash
   mkdir -p "{TMPDIR}/.vcp/oneshot"
   ```

7. **No startup cleanup** — stale files from other sessions are harmless.

**Display session info to user:**
- Number of participants, their presets/models
- Max rounds configured
- Session ID (for debugging)

---

## Step 2: Opening Round (Fan-Out)

**PARALLEL OK — dispatch all participants + generate Claude's position in a single message.**

### 2a. Generate heredoc delimiter

Generate a unique delimiter to prevent heredoc injection:
```bash
bun -e "console.log('VCPTASK_' + require('crypto').randomBytes(4).toString('hex'))"
```
Store result as `{DELIM}` (e.g., `VCPTASK_a3f7b2c1`).

### 2a-bis. Resolve participant system prompts

For each participant that has a non-empty `system_prompt` field, resolve the content:

```bash
bun -e "
import { getSystemPrompt } from '${CLAUDE_PLUGIN_ROOT}/scripts/system-prompts.ts';
const prompt = getSystemPrompt('{SYSTEM_PROMPT}', '${CLAUDE_PLUGIN_ROOT}/system-prompts/built-in');
console.log(prompt ? prompt.content : '');
"
```

Store the resolved content for each participant. If the result is empty or the command fails, skip — the participant uses default behavior (no system prompt prepended).

### 2b. Dispatch ALL participants in parallel

For each participant at index `{i}`:

**Output ID:** `cr-{SESSION_ID}-p{i}-r1`

**Opening prompt template:**

If the participant has resolved `system_prompt` content (from Step 2a-bis), prepend it before the debate prompt:
```
{system_prompt_content}
---
You are a participant in a COMPETITIVE multi-AI debate. {participant_count} other AI systems will also respond. Your goal is to present the STRONGEST position and be prepared to defend it.

TOPIC:
{user_topic}

RESPOND WITH THESE SECTIONS:

**POSITION:** Your core recommendation in 2-3 sentences. Be specific — no fence-sitting.

**ARGUMENTS:** 3-5 key arguments supporting your position, each as a bullet point with concrete evidence or reasoning.

**ANTICIPATED OBJECTIONS:** 2-3 counter-arguments you expect and your preemptive rebuttals.

**BOTTOM LINE:** One sentence — why your approach wins over alternatives.

IMPORTANT: ONLY read and analyze. Do NOT modify any files. Do NOT use Write, Edit, or Bash tools to change anything.
```

If the participant has no `system_prompt` (empty or unresolved), use the prompt without the prefix:
```
You are a participant in a COMPETITIVE multi-AI debate. {participant_count} other AI systems will also respond. Your goal is to present the STRONGEST position and be prepared to defend it.

TOPIC:
{user_topic}

RESPOND WITH THESE SECTIONS:

**POSITION:** Your core recommendation in 2-3 sentences. Be specific — no fence-sitting.

**ARGUMENTS:** 3-5 key arguments supporting your position, each as a bullet point with concrete evidence or reasoning.

**ANTICIPATED OBJECTIONS:** 2-3 counter-arguments you expect and your preemptive rebuttals.

**BOTTOM LINE:** One sentence — why your approach wins over alternatives.

IMPORTANT: ONLY read and analyze. Do NOT modify any files. Do NOT use Write, Edit, or Bash tools to change anything.
```

Route by participant type:

- **Subscription:** `Task(subagent_type: "general-purpose", model: {model}, prompt: {prompt})`

- **API:** `Bash(run_in_background: true)` →
  ```bash
  bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" \
    --type api --output-id cr-{SESSION_ID}-p{i}-r1 \
    --preset "{PRESET}" --model "{MODEL}" \
    --cwd "${CLAUDE_PROJECT_DIR}" --task-stdin <<'{DELIM}'
  {prompt_text}
  {DELIM}
  ```

- **CLI:** `Bash(run_in_background: true)` →
  ```bash
  bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" \
    --type cli --output-id cr-{SESSION_ID}-p{i}-r1 \
    --preset "{PRESET}" --model "{MODEL}" \
    --cwd "${CLAUDE_PROJECT_DIR}" --task-stdin <<'{DELIM}'
  {prompt_text}
  {DELIM}
  ```

### 2c. Claude generates its own opening position

While background tasks run, generate your own analysis of the topic inline. This is Claude's opening position in the debate.

---

## Step 3: Collect Responses (SEQUENTIAL)

**CRITICAL:** Poll background tasks ONE AT A TIME. Do NOT issue multiple TaskOutput calls in the same message — this causes sibling cascade failures.

**Subscription participants:** Result was returned directly from the Task call in Step 2. Already collected.

**API/CLI participants:** For each, sequentially:

1. Derive timeout: `min(timeout_ms + 120000, 600000)` where `timeout_ms` is the preset's configured timeout (default 300000 for API, 1200000 for CLI).

2. Poll for completion:
   ```
   TaskOutput(task_id: "{id}", block: true, timeout: {computed_timeout})
   ```

3. If TaskOutput returns but task is still running, repeat:
   ```
   TaskOutput(task_id: "{id}", block: true, timeout: 600000)
   ```
   Keep repeating until the task completes.

4. Read the output file:
   ```
   Read("{TMPDIR}/.vcp/oneshot/cr-{SESSION_ID}-p{i}-r{round}.json")
   ```
   Parse the JSON. Extract the `result` field for successful responses. Note `error` field for failures.

5. **CLI output normalization:** Strip ANSI escape sequences (`/\x1b\[[0-9;]*[a-zA-Z]/g` pattern). The useful content may be mixed with banners or progress output.

**Error handling:**
- If a participant times out or errors: note the failure, continue with remaining participants.
- **Quorum rule:** Need at least 1 external response + Claude's own to proceed. If ALL external participants fail, report the error to the user and stop.

---

## Step 4: Recap, Synthesize & Check Consensus

Read ALL collected responses (Claude's own + all external participants).

### 4a. Update participant ledger

**Maintain a running ledger of each participant's state across rounds.** After each round, record for each participant:
- Round N position summary (Core Position + Key Arguments, extracted from their response)
- Round N verdict (AGREE/DISAGREE/PARTIAL — for rounds 2+, or "OPENING" for round 1)
- Round N concessions (what they gave up from previous rounds, if any)

**Also track disagreement resolution events** (feeds Step 6 "Points Resolved During Debate"):
- After each round's conflict matrix (Step 4b), compare with the previous round's conflicts
- Record any disagreement that existed in Round N-1 but no longer appears in Round N
- Format: `"{topic}: resolved in Round {N} — {participant} conceded to {participant}"`

For participants that **failed or timed out** this round:
- Record status as "NO RESPONSE (timeout/error)" in the ledger
- Carry forward their last known position from the previous round
- Note them as absent in the recap (do NOT fabricate a position)

This ledger feeds Steps 4b, 5, and 6. It is Claude's internal state — not sent to participants.

### 4b. Present per-participant recap to user (EVERY round)

**This is shown to the user inline. NOT sent to participants.**

```
## Round {N} — Participant Positions

### Claude
**Core Position:** {2-3 sentence summary}
**Key Arguments:**
- {argument 1}
- {argument 2}

### {preset}/{model} (p0)
**Core Position:** {2-3 sentence summary}
**Key Arguments:**
- {argument 1}
- {argument 2}

### {preset}/{model} (p1) — NO RESPONSE (timeout)
*Carried forward from Round {N-1}: {previous position}*

{...repeat for all participants...}

---

### Conflict Matrix

| Point of Contention | Who Agrees | Who Disagrees |
|---------------------|-----------|---------------|
| {topic 1} | {list} | {list} |
| {topic 2} | {list} | {list} |

**Key Disagreements:**
1. {who} vs {who}: {1-sentence clash summary}
{...list ALL disagreements, not capped...}

**Areas of Universal Agreement:**
- {points all agree on}
```

### 4c. Generate/update moderator synthesis

**Claude MUST generate an updated synthesis every round.** This synthesis:
- Identifies the strongest argument on each side of each key disagreement
- Proposes a combined approach that resolves the top conflicts
- Notes which participant's reasoning was most persuasive on each point
- Explicitly states what remains unresolved

Present the synthesis to the user after the recap.

### 4d. Consensus check (rounds 2+ only, skip for Round 1)

For rounds 2+, apply CLI output normalization (strip ANSI) and parse each response for verdict keywords:
- Search for consensus keywords **anywhere** in each response (not just the first line):
  - `AGREE` — participant accepts the synthesis
  - `DISAGREE: <reason>` — participant rejects with specific reason
  - `PARTIAL: <accepted> / <contested>` — partial agreement
- If no keyword found, interpret overall sentiment to classify as agree/disagree/partial
- Also evaluate: are participants actually engaging with each other's arguments, or just restating?

### 4e. Decision

**Consensus is evaluated only among ACTIVE participants** (those who responded this round). ABSENT participants (timed out / errored) are excluded from the consensus count but noted in the final output.

- **Round 1:** Always proceed to **Step 5** (participants haven't seen each other yet)
- **Rounds 2+ — all ACTIVE participants agree:** Go to **Step 6**
- **Rounds 2+ — max_rounds reached:** Go to **Step 6** (report final state)
- **Rounds 2+ — any ACTIVE participant disagrees, rounds remaining:** Refine synthesis, go to **Step 5**

---

## Step 5: Subsequent Rounds — Adversarial Rebuttal

Generate a new heredoc delimiter (same method as Step 2a).

**Adversarial debate prompt template:**

If the participant has resolved `system_prompt` content (from Step 2a-bis), prepend it before the debate prompt:
```
{system_prompt_content}
---
MULTI-AI DEBATE — Round {N}

ORIGINAL TOPIC:
{user_topic}

YOUR PREVIOUS POSITION (Round {N-1}):
{this_participant_position_and_arguments_from_ledger}

---

OTHER PARTICIPANTS' POSITIONS (Round {N-1}):

**NOTE: Showing the most divergent positions. {total_participant_count} total participants.**

**Claude:**
Position: {summary}
Arguments:
- {arg 1}
- {arg 2}

**{preset}/{model} (p{i}):**
Position: {summary}
Arguments:
- {arg 1}
- {arg 2}

{...show up to 4 most divergent participants, not all...}

**Participants aligned with synthesis (not shown in detail):**
- {list any participants who AGREED last round}

---

CURRENT SYNTHESIS (from debate moderator):
{claude_synthesis}

UNRESOLVED DISAGREEMENTS:
1. {participant_A} vs {participant_B}: {clash description} — {1-sentence summary of each side}
2. {participant_C} vs {participant_D}: {clash description} — {1-sentence summary of each side}
{...ALL disagreements, each with participant names and both sides summarized so you can rebut even if the participant's full position is not shown above...}

---

YOUR TASK — respond with ALL sections:

1. **CRITIQUES** — For each disagreement above where you have a view, identify the weakest argument from the opposing side. Name the participant, reference their specific claim, explain why it fails.

2. **DEFENSE** — Address the strongest critique of YOUR position from last round. Concede valid points or explain why they don't apply.

3. **UPDATED POSITION** — Restate your position with any concessions or refinements. If unchanged, explain why others failed to persuade you.

4. **VERDICT:** — One of:
   - AGREE — you accept the current synthesis
   - DISAGREE: <specific objection and what must change>
   - PARTIAL: <what you accept> / <what you contest>

IMPORTANT: ONLY read and analyze. Do NOT modify any files.
```

If the participant has no `system_prompt` (empty or unresolved), use the prompt without the `{system_prompt_content}` prefix (same content starting from "MULTI-AI DEBATE — Round {N}").

**Scaling rules (participant positions only — disagreements are NOT capped):**
- With 1-4 participants: show all positions in detail
- With 5-10 participants: show the 3-4 most divergent positions in detail, list AGREE'd participants by name only
- All disagreements are shown — no cap on disagreement count

**Claude's own round N response:** While background tasks run, Claude also produces its own response following the same 4-section structure (CRITIQUES, DEFENSE, UPDATED POSITION, VERDICT) inline.

Dispatch to all participants using the same pattern as Step 2b (parallel fan-out with `run_in_background: true`).

Output ID for round N: `cr-{SESSION_ID}-p{i}-rN`

Collect responses using the same sequential pattern as Step 3.

Return to **Step 4** with the new responses.

---

## Step 6: Present Results & Cleanup

### Present final results to user:

Use the participant ledger built in Step 4a to generate position evolution.

**If consensus reached:**
```
## Consensus Reached (Round {N}/{max_rounds})

### Final Synthesis
{final_synthesis}

### Position Evolution
**Claude:**
- Round 1: {original position from ledger}
- Final: {final position from ledger}
- Key Concessions: {from ledger, or "None — held firm"}

**{preset}/{model} (p0):**
- Round 1: {original position from ledger}
- Final: {final position from ledger}
- Key Concessions: {from ledger}

**{preset}/{model} (p2) — ABSENT (timed out Round 3)**
- Round 1: {position}
- Last known: Round 2 — {position}

{...all participants from ledger...}

### Consensus Votes
- Claude: AGREE
- {preset}/{model} (p0): AGREE
- {preset}/{model} (p2): ABSENT
```

**If max rounds exhausted without full consensus:**
```
## Debate Complete — No Full Consensus (Round {max_rounds}/{max_rounds})

### Best Synthesis
{final_synthesis}

### Position Evolution
{same format as above, include Final Verdict per participant from ledger}

### Remaining Disagreements
- {participant}: {their specific objection from last DISAGREE/PARTIAL verdict}

### Points Resolved During Debate
- {topic}: resolved in Round {N} — {participant} conceded to {participant} (from ledger disagreement-resolution events)

### Areas of Universal Agreement
- {what everyone agreed on}
```

### Cleanup

Remove THIS session's output files only:
```bash
rm -f "{TMPDIR}/.vcp/oneshot/cr-{SESSION_ID}-"*
```

---

## Known Limitations

1. **Participant repo mutation:** Both API participants (via api-task-runner's Write/Edit/Bash tools) and CLI participants (via their native shell access, e.g., Codex `--full-auto`) retain the ability to modify the repo despite the prompt instruction to only read and analyze. This is prompt-level enforcement only. A structural read-only mode is a follow-up feature.

2. **CLI output noise:** CLI tools may emit banners, ANSI sequences, progress output, or debug text alongside the actual response. The SKILL strips ANSI and searches for consensus keywords anywhere in the response, but noisy output may still confuse synthesis.

3. **Web portal:** Configuration is available via `/dev-buddy-config` web portal (Chatroom tab) or manual editing of `~/.vcp/dev-buddy-chatroom.json`.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No participants configured | Report error, suggest editing `~/.vcp/dev-buddy-chatroom.json` |
| Config validation fails | Report the specific error |
| All external participants fail | Report error to user (quorum not met) |
| Single participant fails | Note failure, continue with remaining (if quorum met) |
| Max rounds exhausted | Present best synthesis with disagreements noted |

---

## Anti-Patterns

- Do NOT issue multiple TaskOutput calls in the same message — cascade failure
- Do NOT use a fixed heredoc delimiter like `TASK_EOF` — generates a random one per dispatch
- Do NOT cleanup files from OTHER sessions — only clean `cr-{SESSION_ID}-*`
- Do NOT skip Claude's own position — Claude is always a participant
- Do NOT fall back to foreground Bash for background tasks — always use `run_in_background: true` + TaskOutput polling
- Do NOT use the default TaskOutput timeout (30s) — always compute from preset's `timeout_ms`
