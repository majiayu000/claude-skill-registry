---
name: external-consensus
description: Synthesize consensus implementation plan from multi-agent debate reports using external AI review
allowed-tools:
  - Bash(.claude/skills/external-consensus/scripts/external-consensus.sh:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(wc:*)
  - Bash(grep:*)
---

# External Consensus Skill

This skill invokes an external AI reviewer (Codex or Claude Opus) to synthesize a balanced, consensus implementation plan from the combined multi-agent debate report.

## CLI Tool Usage

**IMPORTANT**: These CLI tools take long to run, give it 30 minutes of wall time to complete!

This skill uses external CLI tools for consensus review. The implementation pattern follows best practices for security, reasoning quality, and external research capabilities.

### Codex CLI (Preferred)

The skill uses `codex exec` with advanced features:

```bash
# Create temporary files for input/output
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
INPUT_FILE=".tmp/external-review-input-$TIMESTAMP.md"
OUTPUT_FILE=".tmp/external-review-output-$TIMESTAMP.txt"

# Write prompt to input file
echo "$FULL_PROMPT" > "$INPUT_FILE"

# Invoke Codex with advanced features (prompt read from stdin via -)
codex exec \
    -m gpt-5.2-codex \
    -s read-only \
    --enable web_search_request \
    -c model_reasoning_effort=xhigh \
    -o "$OUTPUT_FILE" \
    - < "$INPUT_FILE"

# Read output
CONSENSUS_PLAN=$(cat "$OUTPUT_FILE")
```

**Configuration details:**
- **Model**: `gpt-5.2-codex` - Latest Codex model with enhanced reasoning
- **Sandbox**: `read-only` - Security restriction (no file writes)
- **Web Search**: `--enable web_search_request` - External research capability for fact-checking and SOTA patterns
- **Reasoning Effort**: `model_reasoning_effort=xhigh` - Maximum reasoning depth for thorough analysis

**Benefits:**
- Web search allows fact-checking technical decisions and researching best practices
- High reasoning effort produces more thorough trade-off analysis
- Read-only sandbox ensures security
- File-based I/O handles large debate reports reliably

### Claude Code CLI (Fallback)

When Codex is unavailable, the skill falls back to Claude Code with Opus:

```bash
# Create temporary files
INPUT_FILE=".tmp/external-review-input-$TIMESTAMP.md"
OUTPUT_FILE=".tmp/external-review-output-$TIMESTAMP.txt"

# Write prompt to input file
echo "$FULL_PROMPT" > "$INPUT_FILE"

# Invoke Claude Code with Opus model and read-only tools
claude -p \
    --model opus \
    --tools "Read,Grep,Glob,WebSearch,WebFetch" \
    --permission-mode bypassPermissions \
    < "$INPUT_FILE" > "$OUTPUT_FILE"

# Read output
CONSENSUS_PLAN=$(cat "$OUTPUT_FILE")
```

**Configuration details:**
- **Model**: `opus` - Claude Opus 4.5 with highest reasoning capability
- **Tools**: Limited to read-only tools (Read, Grep, Glob, WebSearch, WebFetch)
- **Permission Mode**: `bypassPermissions` - Skip permission prompts for automated execution
- **File I/O**: Input via stdin, output via stdout redirection

**Benefits:**
- Same research capabilities (WebSearch, WebFetch) as Codex
- High reasoning quality from Opus model
- Read-only tools ensure security
- Seamless fallback when Codex unavailable

## Skill Philosophy

After three agents debate a feature from different perspectives, an **external, neutral reviewer** synthesizes the final plan:

- **External = Unbiased**: Not influenced by any single perspective
- **Consensus = Balanced**: Incorporates best ideas from all agents
- **Actionable = Clear**: Produces ready-to-implement plan with specific steps

The external reviewer acts as a "tie-breaker" and "integrator" - resolving conflicts between agents and combining their insights into a coherent whole.

## Skill Overview

When invoked, this skill:

1. **Loads combined debate report**: Three-agent perspectives from debate-based-planning skill
2. **Prepares external review prompt**: Uses template with debate context
3. **Invokes external reviewer**: Calls Codex (preferred) or Claude Opus (fallback)
4. **Parses consensus plan**: Extracts structured implementation plan from response
5. **Returns final plan**: Ready for user approval and GitHub issue creation

## Inputs

This skill requires exactly 3 agent report file paths:
- **Report 1**: Path to first agent report (e.g., `.tmp/issue-42-bold-proposal.md`)
- **Report 2**: Path to second agent report (e.g., `.tmp/issue-42-critique.md`)
- **Report 3**: Path to third agent report (e.g., `.tmp/issue-42-reducer.md`)

The script automatically:
- Extracts feature name from any of the three reports (case-insensitive, supports multiple formats):
  - Headers: `# Feature: Example` or `## Title: Example`
  - Bold labels: `**Feature**: Example` or `**Title**: Example`
  - Plain labels: `Feature: Example` or `Title: Example`
  - Scans reports in priority order (report 1 → 2 → 3) until match found
  - Falls back to "Unknown Feature" if no match in any report
- Extracts issue number from first report filename (if it follows `issue-{N}-*` pattern)
- Combines all 3 reports into a single debate report file

## Outputs

- **Combined debate report**: `.tmp/issue-{N}-debate.md` (if first report has issue number) or `.tmp/debate-report-{timestamp}.md` (fallback) with all 3 reports combined
- **Consensus plan file**: `.tmp/issue-{N}-consensus.md` (if debate report has issue number) or `.tmp/consensus-plan-{timestamp}.md` (fallback) with final implementation plan
- **Plan summary**: Key decisions and LOC estimate

## Implementation Workflow

**Design Principle**: Minimize human intervention by avoiding environment variable management. The script should be invoked directly and handle all operations autonomously, outputting results to stdout for the user to review.

### Step 1: Invoke External Consensus Script

Direct invocation with 3 report paths - the script handles everything and outputs summary:

```bash
# Standard invocation: pass 3 report file paths
.claude/skills/external-consensus/scripts/external-consensus.sh \
    .tmp/issue-42-bold-proposal.md \
    .tmp/issue-42-critique.md \
    .tmp/issue-42-reducer.md
```

**Script automatically:**
1. Validates all 3 report files exist
2. Extracts issue number from first report filename (if it follows `issue-{N}-*` pattern)
3. Extracts feature name from any of the three reports (case-insensitive, multiple formats):
   - Accepts headers (`# Feature:`), bold labels (`**Feature**:`), or plain labels (`Feature:`)
   - Scans in priority order: report 1 → 2 → 3 until first match found
   - Falls back to "Unknown Feature" if no label found in any report
4. Combines all 3 reports into a single debate report file (`.tmp/issue-{N}-debate.md` or `.tmp/debate-report-{timestamp}.md`)
5. Loads and processes prompt template with variable substitution
6. Checks if Codex is available (prefers Codex with xhigh reasoning)
7. Falls back to Claude Opus if Codex unavailable
8. Invokes external AI with appropriate configuration:
   - **Codex**: `gpt-5.2-codex`, read-only sandbox, web search enabled, xhigh reasoning (30 min)
   - **Claude**: Opus model, read-only tools, bypassPermissions (30 min)
9. Saves consensus plan to `.tmp/issue-{N}-consensus.md` or `.tmp/consensus-plan-{timestamp}.md`
10. Validates output and extracts summary information
11. Outputs consensus file path on stdout (last line)
12. Displays summary information on stderr for user review

**Required inputs:**
- Path to first agent report (required)
- Path to second agent report (required)
- Path to third agent report (required)

**No environment variables needed** - just invoke the script and review the output

**Expected output format:**
```markdown
# Implementation Plan: {Feature Name}

## Consensus Summary

[Summary of balanced approach...]

## Codebase Analysis

**File changes:**

| File | Level | Purpose |
|------|-------|---------|
| `path/to/file` | major/medium/minor/remove | Description |

## Implementation Steps

[Detailed steps with LOC estimates...]

## Test Strategy

[Test approach and cases...]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Risks and Mitigations

[Risk table...]
```

**Modification levels:**
- **minor**: <10 LOC, cosmetic changes
- **medium**: 10-50 LOC, no interface changes
- **major**: >50 LOC, interface changes, or new files
- **remove**: File deletion

**Script output on stdout (last line):**
```
.tmp/issue-42-consensus.md
```

**Script output on stderr (summary for review):**
```
Using external AI reviewer for consensus synthesis...

Configuration:
- Input: .tmp/issue-42-external-review-input.md (1012 lines)
- Output: .tmp/issue-42-external-review-output.txt
- Model: gpt-5.2-codex (Codex CLI)
- Sandbox: read-only
- Web search: enabled
- Reasoning effort: xhigh

[Codex execution details...]

External consensus review complete!

Consensus Plan Summary:
- Feature: Review-Standard Simplification with Scoring
- Total LOC: ~350-420 (Medium)
- Implementation Steps: 3
- Risks Identified: 4

Key Decisions:
- Accepted from Bold Proposal: Keep explicit evidence requirements
- Addressed from Critique: Preserve Phase 3 specialized checks
- Applied from Reducer: Single-file architecture, compress prose

Consensus plan saved to: .tmp/issue-42-consensus.md
```

The script performs validation and summary extraction internally - no additional steps needed.

## Error Handling

The `external-consensus.sh` script handles most error scenarios internally. Here are the main error cases:

### Report Files Not Found

The script validates that all 3 report files exist. If any file is missing, it exits with:

```
Error: Report file not found: {file_path}
```

**Solution**: Ensure all 3 agent reports were generated successfully by the multi-agent debate workflow.

### Codex CLI Unavailable (Auto-fallback to Claude)

The script automatically detects if Codex is available and falls back to Claude Opus:

```
Codex not available. Using Claude Opus as fallback...
```

This is seamless and maintains the same research capabilities (WebSearch, WebFetch) and read-only security.

### External Reviewer Failure

If the external AI (Codex or Claude) fails, the script exits with a non-zero code:

```
Error: External review failed with exit code {code}
```

**Possible causes:**
- API rate limit reached
- Network connection issue
- Invalid API credentials
- Web search timeout (Codex only)
- Reasoning effort timeout (xhigh setting)

**Solution**: Check API credentials, network connection, or retry with different settings.

### Invalid or Incomplete Output

If the consensus plan is missing required sections, Step 2 validation will detect it:

```
Warning: Consensus plan may be incomplete. Missing sections: {list}
The plan is available at: {file_path}
```

**Solution**: Review the plan manually, adjust the prompt template if needed, or retry the external consensus review.

## Usage Examples

### Example 1: Successful Consensus with Codex

**Input:**
```bash
.claude/skills/external-consensus/scripts/external-consensus.sh \
    .tmp/issue-42-bold-proposal.md \
    .tmp/issue-42-critique.md \
    .tmp/issue-42-reducer.md
```

**Execution:**
```
Combined debate report saved to: .tmp/issue-42-debate.md

Using Codex (gpt-5.2-codex) for external consensus review...

[Codex executes with advanced features:]
- Model: gpt-5.2-codex
- Sandbox: read-only
- Web search: enabled (researching JWT best practices)
- Reasoning effort: xhigh
- Input: .tmp/issue-42-external-review-input.md
- Output: .tmp/issue-42-external-review-output.txt
```

**Output:**
```
External consensus review complete!

Consensus Plan Summary:
- Feature: JWT Authentication
- Total LOC: ~280 (Medium)
- Components: 4
- Critical risks: 1

Key Decisions:
- From Bold Proposal: Accepted JWT with refresh tokens
- From Critique: Addressed token storage security concern (httpOnly cookies)
- From Reducer: Removed OAuth2 complexity, kept simple JWT

Research Applied:
- Verified OWASP JWT security guidelines (via web search)
- Confirmed refresh token rotation best practices
- Fact-checked token expiration standards

Consensus plan saved to: .tmp/issue-42-consensus.md

Next step: Review plan and create GitHub issue with open-issue skill.
```

### Example 2: Web Search Usage

**Scenario:** Feature requires external research for SOTA patterns.

**Input:**
```bash
.claude/skills/external-consensus/scripts/external-consensus.sh \
    .tmp/issue-15-bold-proposal.md \
    .tmp/issue-15-critique.md \
    .tmp/issue-15-reducer.md
```

(First report contains: **Feature**: Real-time Collaboration with CRDT)

**Codex behavior:**
```
Combined debate report saved to: .tmp/issue-15-debate.md

Using Codex (gpt-5.2-codex) for external consensus review...

[Web search queries executed:]
- "CRDT implementation best practices 2025"
- "Yjs vs Automerge performance comparison"
- "Operational transformation vs CRDT trade-offs"

[External research findings incorporated into consensus:]
- Yjs recommended for browser-based collaboration (proven, actively maintained)
- WebSocket vs WebRTC trade-off analysis
- Conflict resolution strategies from recent papers
```

**Output includes fact-checked decisions based on web research.**

### Example 3: Claude Fallback with Research

**Scenario:** Codex unavailable, Claude Code (always available) provides same research capabilities.

**Output:**
```
Codex not available. Using Claude Opus as fallback...

[Claude Opus executes with:]
- Model: opus
- Tools: Read, Grep, Glob, WebSearch, WebFetch (read-only)
- Permission mode: bypassPermissions
- Input: .tmp/issue-42-external-review-input.md (via stdin)
- Output: .tmp/issue-42-external-review-output.txt (via stdout)

External consensus review complete!
[Summary as Example 1...]

Note: Used Claude Opus (Codex unavailable)
Research capability: WebSearch and WebFetch used for fact-checking
```
