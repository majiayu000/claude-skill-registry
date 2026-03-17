---
name: essay-pipeline
version: 1.0
description: >
  Use when collaboratively writing a science blog essay through interactive
  thesis development, essay structuring, argument development, and paragraph
  writing with tiered fact-checking and voice matching.
handoff:
  accepts_from:
    - "*"
  provides_to:
    - essay-fact-checker
    - essay-voice-matcher
  schema_version: "3.0"
  schema_type: universal
categories:
  - writing
  - research
  - content-creation
prerequisites:
  - Style profile (style-profile.md) at configured path
  - Sample essays in configured directory (recommended, not required)
  - WebSearch tool available (for fact-checking)
  - Topic idea or rough thesis from user
estimated_duration: 2-8 hours (depending on essay length and user pace)
success_criteria:
  - User completes all 4 stages from topic idea to finished essay
  - Every stage involves interactive dialogue with user approval
  - Stage-appropriate pushback applied at configured level
  - Final essay matches user voice (voice-matcher confirms)
  - All factual claims verified with source URLs
  - Session state preserved across pauses and resumes
---

# Essay Pipeline

Announce: "I'm using the essay-pipeline skill for interactive essay writing."

## Architecture Overview

This pipeline uses an orchestrator-as-conductor pattern. You (the orchestrator) run all four interactive stages in your main thread, maintaining direct conversation with the user. Only non-interactive specialists are delegated as sub-agents.

```
User
  |
  v
essay-pipeline orchestrator (YOU -- main thread)
  |
  |-- Stage 1: Thesis Development (interactive, in your thread)
  |     Reference: references/stage-1-thesis-development.md
  |
  |-- Stage 2: Essay Structuring (interactive, in your thread)
  |     Reference: references/stage-2-essay-structuring.md
  |
  |-- Stage 3: Argument Development (interactive, per-section, in your thread)
  |     Reference: references/stage-3-argument-development.md
  |     Support: essay-fact-checker (via Task tool)
  |
  |-- Stage 4: Paragraph Writing (interactive, per-paragraph, in your thread)
  |     Reference: references/stage-4-paragraph-writing.md
  |     Support: essay-fact-checker (via Task tool)
  |     Support: essay-voice-matcher (via Task tool)
  |
  v
Final Essay Output
```

**Why this architecture**: Claude Code sub-agents cannot use AskUserQuestion. Since every stage requires interactive dialogue, the orchestrator must run all stages directly. Sub-agents are used only for non-interactive work (fact verification and voice evaluation).

## State Anchoring Protocol

Start every response with a state anchor:

```
[Stage N/4 - {stage_name}] {status}
```

Examples:
- `[Stage 1/4 - Thesis Development] Developing thesis through Socratic dialogue`
- `[Stage 2/4 - Essay Structuring] Negotiating section structure`
- `[Stage 3/4 - Argument Development - Section 2 of 5] Developing argument map`
- `[Stage 4/4 - Paragraph Writing - Section 1, Paragraph 3] Drafting paragraph`

**Re-anchor after:**
- Navigation commands ("go back to...", "show full state")
- Stage transitions
- Resume from pause
- Any context-switching action

## Tool Selection Table

| Situation | Tool | Reason |
|-----------|------|--------|
| Load stage reference file | Read tool | Load behavioral instructions from references/ |
| Load style profile | Read tool | Load user's voice characteristics |
| Load session state | Read tool | Resume from pause or check progress |
| Load stage outputs (thesis, outline, argument maps) | Read tool | Context for current stage |
| Invoke fact-checker | Task tool | Non-interactive; returns structured verification results |
| Invoke voice-matcher | Task tool | Non-interactive; returns voice assessment |
| User interaction (all stages) | AskUserQuestion | ALL dialogue, approvals, pushback, navigation |
| Write session state | Bash tool | Atomic write protocol (tmp + rename) |
| Write stage outputs (thesis, outline, maps, draft) | Write tool | Save approved content to session files |
| Check prerequisites | Bash tool | File existence checks for style profile and samples |
| Check for existing sessions | Bash tool | Scan /tmp/essay-pipeline-*/ directories |
| Search style profile or samples | Grep tool | Find patterns in profile or sample essays |
| List sample essays | Glob tool | Enumerate available sample essay files |

**Self-check rule**: Before performing any action, ask: "Am I about to verify a fact or evaluate voice consistency?" If YES, delegate to the appropriate sub-agent via Task tool. NEVER verify facts or evaluate voice consistency yourself.

## Delegation Mandate

### Orchestrator-Owned (YOU do these)
- Session management: Create, save, restore, pause, resume sessions
- Stage transitions: Evaluate exit criteria, present summaries, get user approval
- User dialogue: ALL interactive conversation via AskUserQuestion
- Quality gate evaluation: Check exit criteria checklists
- Context assembly: Load relevant files for each stage
- Stage execution: Follow stage reference file instructions
- Final essay assembly: Combine approved paragraphs into final document
- State anchoring: Maintain stage/section/paragraph tracking in every response

### Delegated to essay-fact-checker (via Task tool)
- ALL factual claim verification (Tier 1)
- ALL proactive research enrichment (Tier 2)
- Tier 3 escalation identification
- Source URL verification
- Contradictory source reporting

### Delegated to essay-voice-matcher (via Task tool)
- ALL voice consistency evaluation
- Style profile analysis
- Sample essay consultation
- Profile-sample conflict detection
- Cumulative voice tracking

**Never do sub-agent work yourself.** If you find yourself about to look up a fact or evaluate whether text matches the user's voice, stop and delegate.

## Pre-Flight Validation

Before starting the pipeline, check prerequisites:

### 1. Style Profile Check

Use Bash tool to check for the style profile:
```bash
test -f "{configured_path}/style-profile.md" && echo "FOUND" || echo "NOT_FOUND"
```

**If found**: Read the profile and keep it in context throughout the session.

**If not found**: Offer three paths via AskUserQuestion:
- **(a) Quick 5-question profile**: Ask the 5 express profile questions (from `references/style-profile-template.md`), synthesize a minimal profile, save it, and proceed.
- **(b) Proceed without (degraded mode)**: Voice matching will be limited. The voice-matcher will work from sample essays only, or skip voice matching entirely if no samples either.
- **(c) Exit to create full profile**: Provide the template path and exit. User fills out the full template and returns.

### 2. Sample Essays Check

Use Bash/Glob to check for sample essays:
```bash
ls "{configured_path}/samples/"*.md 2>/dev/null | head -5
```

**If found**: Note the number of available samples. The voice-matcher will consult them.
**If not found**: Warn the user. Voice matching will rely solely on the style profile.

### 3. WebSearch Availability

Note that WebSearch is available through the essay-fact-checker sub-agent. If fact-checker invocation fails, fall back to user-provided sources only.

## Session Initialization

### Check for Existing Sessions

Scan for existing sessions:
```bash
ls -d /tmp/essay-pipeline-*/ 2>/dev/null
```

**If sessions found**: Present them to the user with status summaries. Ask whether to resume an existing session or start new.

**If no sessions found**: Proceed to create a new session.

### Create New Session

1. Generate session directory:
   ```bash
   mkdir -p /tmp/essay-pipeline-$(date +%Y%m%d-%H%M%S)
   ```

2. Initialize session state (see `references/session-state-schema.md` for full schema)

3. Offer pushback level selection via AskUserQuestion:
   ```
   Before we begin, how much intellectual pushback would you like?

   - Full (default): I'll challenge your ideas vigorously to strengthen them.
     3 rounds of pushback in thesis development, 2 in argument development.
   - Light: I'll raise concerns once and accept your response.
     1 round per point.
   - Minimal: I'll offer observations but won't challenge.
     No pushback rounds.

   You can change this at any time during the session.
   ```

4. Save initial state using atomic write protocol.

5. Begin Stage 1.

## Pipeline Workflow

For each stage, follow this process:

### Stage Entry
1. Read the stage reference file: `references/stage-N-{name}.md`
2. Anchor state: `[Stage N/4 - {name}] Beginning stage`
3. Follow the stage's behavioral instructions

### Stage Execution
4. Conduct interactive dialogue with user per the stage's process
5. Apply stage-appropriate pushback per the configured pushback level
6. Delegate to sub-agents as needed (fact-checker in Stage 3/4, voice-matcher in Stage 4)
7. Save incremental progress to session files

### Stage Exit
8. Evaluate exit criteria (from the stage reference file)
9. Present stage completion summary to the user
10. Get user approval at quality gate via AskUserQuestion
11. Save stage outputs to session directory
12. Update session state (atomic write)
13. Ask user to confirm readiness to proceed to next stage

### Stage Transition
14. Drop the previous stage's reference file from active consideration
15. Keep stage OUTPUT files (thesis, outline, argument maps) as context
16. Load the next stage's reference file
17. Begin the next stage's process

## Stage-Specific Execution Notes

### Stage 1: Thesis Development
- Load: `references/stage-1-thesis-development.md`
- Follow its Socratic dialogue process
- Express path available for pre-formed theses
- Quality Gate G1: Thesis is clear, defensible, and approved

### Stage 2: Essay Structuring
- Load: `references/stage-2-essay-structuring.md`
- Read Stage 1 output for thesis and claim type
- Negotiate structure, length, audience
- Quality Gate G2: Outline is complete and approved

### Stage 3: Argument Development (Per-Section Loop)
- Load: `references/stage-3-argument-development.md`
- Loop through each section in the outline:
  ```
  for each section in outline:
    Develop argument map for this section
    Batch-invoke fact-checker for all claims in this section
    Handle fact-checker results with user
    Get user approval for section argument map
    Save argument map to session directory
    Update session state
  ```
- After all sections: Present bird's-eye review of all argument maps
- Quality Gate G3-Final: All argument maps cohere and are approved
- Optional: User can request paragraph writing for completed sections (controlled forward-jumping)

### Stage 4: Paragraph Writing (Per-Paragraph Loop)
- Load: `references/stage-4-paragraph-writing.md`
- Loop through each section, then each paragraph:
  ```
  for each section:
    for each paragraph in section:
      Draft paragraph following argument map + style profile
      Self-audit for argument map compliance
      Present to user for approval
      Save approved paragraph
    Invoke voice-matcher on complete section
    Present section for bird's-eye review
  ```
- After all sections: Final voice check, final fact-check sweep, resolve deferred verifications
- Quality Gate G5: Full essay approved

## Quality Gates

| Gate | Location | Criteria | Failure Action |
|------|----------|----------|----------------|
| G1 | End of Stage 1 | Thesis is clear, defensible, claim type identified, user approved | Loop Stage 1 |
| G2 | End of Stage 2 | Outline complete, length agreed, sections purposeful, user approved | Loop Stage 2 |
| G3 (per section) | End of each Stage 3 iteration | Claims evidenced, counterarguments addressed, sources verified, user approved | Loop current section |
| G3-Final | After all Stage 3 sections | All argument maps cohere, bird's-eye approval | Revisit specific sections |
| G4 (per paragraph) | End of each Stage 4 iteration | Voice matches, facts verified, user approved | Revise paragraph |
| G4-Section | After all paragraphs in a section | Section reads well, voice consistent | Revise specific paragraphs |
| G5 | End of Stage 4 | Full essay reviewed, voice consistent, all facts verified, all deferred claims resolved, user gives final approval | Revise specific sections/paragraphs |

## User Navigation

At any point, the user can issue navigation commands. Detect these in user responses and handle accordingly:

| Command | Action |
|---------|--------|
| "Show full state" / "Where am I?" | Display current stage, section, paragraph; completed work summary; pending work |
| "Show essay so far" | Read and display all approved paragraphs from stage-4-draft.md |
| "Go back to thesis" / "Go back to Stage 1" | Assess impact, archive downstream if needed, return to Stage 1 |
| "Go back to outline" / "Go back to Stage 2" | Assess impact, archive downstream if needed, return to Stage 2 |
| "Go back to section N arguments" | Return to Stage 3 for section N |
| "Pause" / "Save and exit" | Save state, display resume instructions |
| "Resume" | Load state, present summary, continue |
| "Change pushback level" | Update pushback_level in session state |

### Stage Revisit Cascade

When the user goes back to an earlier stage:

1. **Assess change impact** (see `references/session-state-schema.md`):
   - Minor: Flag downstream for review
   - Moderate: Archive affected downstream artifacts
   - Major: Archive ALL downstream artifacts, warn user
2. **Present impact to user**: "Going back to [stage] will [impact description]. Your current work will be [preserved/archived/flagged]. Continue?"
3. **If user confirms**: Update session state, version old artifacts, begin the earlier stage
4. **Never silently discard work**

## Error Handling Protocol

| Failure | Detection | Action |
|---------|-----------|--------|
| Fact-checker sub-agent fails | Task tool returns error | Retry once. If fails again: mark claims as DEFERRED; inform user; proceed |
| Voice-matcher sub-agent fails | Task tool returns error | Skip voice check; note in metadata; inform user; proceed |
| WebSearch unavailable | Fact-checker reports service failure | Graceful degradation: user-provided sources only; inform user |
| Session state corrupt | YAML parse fails on Read | Level 1: Recover from .bak. Level 2: Reconstruct from artifacts. Level 3: Ask user |
| Style profile missing | Pre-flight check finds no file | Offer 3 paths: quick profile, degraded mode, exit to create |
| Style profile malformed | Read returns unparseable content | Warn user; offer to proceed with best-effort interpretation or exit to fix |
| Literature-researcher unavailable | Pre-flight check or runtime | Inform user; Tier 3 escalation unavailable; expanded Tier 2 search as substitute |
| Stage reference file missing | Read tool returns error | FATAL: Cannot proceed. Report error and stop. This indicates a broken installation. |

### Graceful Degradation Hierarchy

When components fail, degrade gracefully rather than stopping:

```
Full capability (all components working)
  |
  v (fact-checker fails)
Degraded: User-provided sources only; claims marked DEFERRED
  |
  v (voice-matcher also fails)
Degraded: No voice checking; user self-evaluates voice
  |
  v (session state corrupt)
Recovery mode: Reconstruct from artifacts
  |
  v (artifacts also lost)
Manual recovery: Ask user where to resume
```

## Timeout Configuration

| Component | Timeout | Exceeded Action |
|-----------|---------|-----------------|
| Fact-checker (per invocation) | 3 minutes | Return "verification timeout"; mark claims as DEFERRED |
| Voice-matcher (per invocation) | 3 minutes | Skip voice check; note in metadata |
| Session inactivity | 24 hours | Auto-pause; session eligible for resume |
| Session abandonment | 7 days | Warn on next access; offer cleanup or resume |

When invoking sub-agents via Task tool, include timeout guidance in the task prompt.

## Fact-Checker Invocation Protocol

### During Stage 3 (Argument Development)
- **When**: After developing the argument map for a section
- **What**: Batch all factual claims in the section into one invocation
- **How**: Prepare claim list per the fact-checker's input format; invoke via Task tool
- **Result handling**: Present results to user; update argument map with verification status and sources

### During Stage 4 (Paragraph Writing)
- **When**: When a draft paragraph introduces NEW claims not already verified in Stage 3
- **What**: Only new claims (do NOT re-verify claims already in argument maps)
- **How**: Same as Stage 3

### Final Sweep
- **When**: After all paragraphs are approved, before Quality Gate G5
- **What**: All claims in the complete essay (one batch invocation)
- **Purpose**: Catch any claims modified during user edits, verify deferred claims

### Deferred Verification Queue
- Track unverified claims in session state under `deferred_verifications`
- Resolve ALL deferred claims before Quality Gate G5
- Resolution: Retry verification, user provides source, revise claim, or remove claim

### Task Tool Invocation Format

```
Task: essay-fact-checker

Verify the following claims from Section [N] of a science blog essay about [topic].

[YAML claim batch]

Return results as YAML with verification status, source URLs, and notes for each claim.
Timeout: Complete within 3 minutes.
```

## Voice-Matcher Invocation Protocol

### Invocation Schedule
- **After each section is complete**: Section-level voice consistency check
- **After full essay is complete**: Essay-level voice consistency check
- **On user request**: Any time the user asks about voice

### Calibration (First Invocation)
On the first voice-matcher result:
1. Present the assessment to the user
2. Ask: "How accurate is this voice assessment? Rate 1-5, where 5 is very accurate."
3. Save the user's rating in session state under `voice_calibration`
4. Include calibration data in all subsequent voice-matcher invocations

### Score Thresholds
| Score | Action |
|-------|--------|
| 5/5 | Proceed; inform user of strong match |
| 4/5 | Proceed; mention specific observations |
| 3/5 | Present assessment to user; ask if they want revisions |
| 2/5 | Flag for revision; present specific suggestions |
| 1/5 | Pause and suggest style profile review |

### Task Tool Invocation Format

```
Task: essay-voice-matcher

Evaluate the following text for voice consistency against the user's style profile.

Text to evaluate:
[text]

Style profile path: [path]
Sample essays path: [path]
Context: Stage [N], Section [N], [content type]
Previous assessments: [YAML list of prior assessments]
Calibration: [calibration data if available]
Voice reference mode: [profile | sample | hybrid]

Return assessment as YAML with score (1-5), observations, and suggestions.
Timeout: Complete within 3 minutes.
```

## User Override Protocol

When the fact-checker's findings conflict with the user's claim:

1. **Present evidence**: "The fact-checker found [result]. Your claim states [claim]. Source: [URL]"
2. **Offer options via AskUserQuestion**:
   - Revise the claim to match verified evidence
   - Rephrase (keep the spirit, adjust specifics)
   - Keep with override (log the disagreement)
   - Provide your own source
3. **Log all overrides** in `fact-check-log.md`
4. **Surface at final review**: At Quality Gate G5, present all overrides for one final confirmation

## Argument Map Compliance (Stage 4)

Before presenting each paragraph draft in Stage 4:

1. **Self-audit**: Which argument map points does this paragraph cover?
2. **Tag content**: Mark each sentence as MAPPED (covers an argument map point) or NOT IN MAP
3. **Flag deviations**: If NOT IN MAP content exists, explicitly notify the user:
   - "This paragraph includes content not in your argument map: [description]."
   - Options: (a) Keep and add to map retroactively, (b) Remove, (c) Go back to Stage 3

## Context Window Management

For long essays (5,000+ words), context window pressure is a concern. Follow these rules:

| Content | When Loaded | When Dropped | Budget |
|---------|-------------|-------------|--------|
| Style profile | Session start | Never (kept throughout) | ~500 words |
| Current stage reference file | Stage entry | Stage exit | ~300 words |
| Thesis statement | Stage 1 completion | Never | ~50 words |
| Essay outline | Stage 2 completion | Never | ~300 words |
| Current section argument map | Stage 3/4 per section | Moving to next section | ~200-400 words |
| Previous sections argument maps | Summarized after completion | After summary | ~50 words each |
| Current section approved paragraphs | Stage 4 per section | Moving to next section | Variable |
| Previous sections full text | Written to file | Immediately | 0 (file-based) |

**Key rule**: Rely on FILES for historical content, not conversation memory. After each section is complete in Stage 4, write the full section text to `stage-4-draft.md` and drop it from active context. When needed for continuity, read only the last paragraph of the previous section.

## Session State Resilience

### Atomic Writes
All session state updates use the atomic write protocol:
1. Write to `.tmp` file
2. Copy current state to `.bak`
3. Rename `.tmp` to primary

### Incremental Saves
Save progress at granular checkpoints:
- After each completed argument point (Stage 3)
- After each approved paragraph (Stage 4)
- After each stage transition
- After any user navigation command

### Recovery
On session load, attempt: Primary state -> Backup state -> Artifact reconstruction (see `references/session-state-schema.md`)

## Pipeline Completion

When all stages are complete and Quality Gate G5 is passed:

1. **Final voice check**: Invoke voice-matcher on full essay
2. **Final fact-check sweep**: Invoke fact-checker on all claims in complete essay
3. **Resolve deferred verifications**: All must be resolved
4. **Present completion summary**:
   ```
   Pipeline Complete!

   Word count: [N] words
   Sections: [N]
   Sources verified: [N] claims with [M] unique sources
   Voice consistency: [score]/5
   User overrides: [N] (see fact-check-log.md)
   Deferred claims resolved: [N] of [N]
   Time spent: [duration]
   ```
5. **Write final essay** to `{session_dir}/final-essay.md`
6. **Offer export**: "Would you like me to write the essay to a specific file path?"
7. **Archive session**: Mark session as "completed" in state

## Quick Reference: Stage Summary

| Stage | Reference File | Pushback Type | Delegates To | Quality Gate |
|-------|---------------|---------------|-------------|-------------|
| 1. Thesis Development | stage-1-thesis-development.md | Logical rigor | None | G1 |
| 2. Essay Structuring | stage-2-essay-structuring.md | Audience awareness | None | G2 |
| 3. Argument Development | stage-3-argument-development.md | Devil's advocacy | essay-fact-checker | G3, G3-Final |
| 4. Paragraph Writing | stage-4-paragraph-writing.md | Minimal | essay-fact-checker, essay-voice-matcher | G4, G4-Section, G5 |
