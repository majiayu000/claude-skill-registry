---
name: kimi-supervisor
description: "Token-efficient multi-agent orchestration. Claude spawns Kimi for research + MiniMax for review. 85-93% token savings on exploration tasks."
---

# Kimi Supervisor - Token-Efficient Multi-Agent Orchestration

**Provider:** Kimi K2.5 (Moonshot AI)
**Purpose:** Claude orchestrates Kimi (research) + MiniMax (review) for verified exploration with massive token savings
**Cost Savings:** 85-93% on exploration vs direct Claude work

---

## When to Use This Skill

Use Kimi Supervisor when:
- Task requires spawning 2+ exploration/research agents
- Need to synthesize information from multiple sources
- Complex research across multiple domains
- Batch operations (file reading, image analysis, web searches)

**Don't use when:**
- Single straightforward query
- Code writing (Claude handles this directly)
- Architectural decisions (Claude maintains control)

---

## How It Works

```
Traditional Approach:
  Claude → [Agent1, Agent2, Agent3] → Claude reads all outputs (~10k tokens)

Kimi Supervisor Approach:
  Claude → Kimi K2.5 → [Agent1, Agent2, Agent3] → Kimi synthesizes → MiniMax reviews → Claude reads summary (~1-2k tokens)
```

**Token Efficiency:**
- Kimi exploration: ~$0.30/M tokens
- MiniMax review: ~$0.20/M tokens
- Claude Sonnet: ~$15/M tokens (input)
- **Savings: ~50-100x on synthesis work**

---

## Architecture Pattern (Claude Orchestrates)

**CRITICAL:** Only Claude can spawn subagents. Kimi cannot spawn its own agents.

```
┌─ Claude (Main Agent - Orchestrator) ──────────────────┐
│ 1. Receives task requiring exploration                │
│ 2. Constructs Kimi prompt with supervisor template    │
│ 3. Spawns Kimi K2.5 via Task tool                     │
│                                                        │
│    ┌─ Kimi K2.5 (Research Agent) ──────────────┐      │
│    │ • Uses native Glob/Grep/Read tools        │      │
│    │ • Explores codebase, reads files          │      │
│    │ • Synthesizes findings                    │      │
│    │ • Shows work (quotes, paths, assumptions) │      │
│    │ • Returns compressed summary              │      │
│    └───────────────────────────────────────────┘      │
│                                                        │
│ 4. Claude spawns MiniMax for review                   │
│                                                        │
│    ┌─ MiniMax (Review Agent) ─────────────────┐       │
│    │ • Receives Kimi's synthesis              │       │
│    │ • Checks for hallucinations              │       │
│    │ • Validates quotes and file paths        │       │
│    │ • Returns approval/concerns              │       │
│    └──────────────────────────────────────────┘       │
│                                                        │
│ 5. Claude receives both outputs                       │
│ 6. Claude makes decisions based on verified data      │
└────────────────────────────────────────────────────────┘
```

**Token Efficiency:**
- Kimi exploration: ~$0.30/M tokens
- MiniMax review: ~$0.20/M tokens
- Claude Sonnet: ~$15/M tokens (input)
- Claude receives compressed summary (~1-2k tokens vs 10k+ raw)
- **Savings: 85-93% on exploration phases**

---

## Why This Works (Token Economics)

**Claude orchestrates, cheaper models execute:**
- Claude makes architectural decisions (what it's best at)
- Kimi does deep research (256K context, $0.30/M tokens)
- MiniMax provides review (fast, cheap, $0.20/M tokens)
- Claude receives compressed summaries (1-2k tokens vs 10k+ raw)

**Kimi K2.5 Research Capabilities:**
- 256K token context (can read many files)
- Built-in vision (can analyze images)
- Native Glob/Grep/Read tools (fast file exploration)
- Strong synthesis abilities (compresses findings well)

**MiniMax Review Strengths:**
- Fast turnaround (low latency)
- Good at spotting hallucinations (different model = different blind spots)
- Cheap enough to always use ($0.20/M tokens)
- Cross-model verification (not self-review)

---

## Usage Instructions

### For Claude (Main Agent)

This skill loads a step-by-step workflow for you to manually orchestrate Kimi + MiniMax.

**Step-by-Step Workflow:**

1. **Identify exploration task** - Recognize when you need to research codebase

2. **Spawn Kimi with supervisor prompt:**

   ⚠️ **IMPORTANT:** Kimi requires environment variable setup via `scripts/start-kimi.ps1`.
   You CANNOT use `model="kimi"` as a Task parameter - it will fail with InputValidationError.

   **Correct approach:** The Kimi Supervisor workflow requires launching Kimi in a separate terminal:
   ```powershell
   # In separate terminal/session
   .\scripts\start-kimi.ps1
   ```

   Then delegate work to that Kimi session (not via Task tool model parameter).

3. **Receive Kimi's synthesis** - Contains quotes, file paths, assumptions, confidence scores

4. **Spawn MiniMax for review:**
   ```
   Task(
     subagent_type="general-purpose",
     model="minimax",
     prompt="Review the following Kimi synthesis for hallucinations, errors, and missing context:\n\n[Kimi's output]",
     description="MiniMax reviews Kimi findings"
   )
   ```

5. **Receive MiniMax's verification** - APPROVED / NEEDS_REVISION / concerns

6. **Make decisions** - You now have verified, compressed findings to act on

---

## Anti-Hallucination Protocol

### Show Work Requirements

Kimi MUST include in every response:

1. **Direct Quotes:**
   ```markdown
   > "Exact text from file.py:42"
   ```
   - Shows actual code/content found
   - Reduces paraphrasing errors

2. **File Paths with Line Numbers:**
   ```
   Found in src/utils.py:156-172
   ```
   - Verifiable locations
   - Claude can spot-check if suspicious

3. **Assumptions List:**
   ```markdown
   ## Assumptions Made
   - Assumed X based on Y
   - Inferred Z from pattern in files A, B, C
   ```
   - Makes inferences explicit
   - Easier to catch logical leaps

4. **New Files Created:**
   ```markdown
   ## Files Created
   - /path/to/new/file.py (42 lines)
   - /path/to/config.json (12 lines)
   ```
   - Claude knows what to verify
   - No silent file creation

5. **Confidence Scores:**
   ```markdown
   Confidence: High (95%) - verified in 3 files
   Confidence: Medium (70%) - inferred from naming patterns
   Confidence: Low (40%) - no direct evidence found
   ```

### MiniMax Review Checklist

MiniMax verifies:
- [ ] All code quotes are exact (not paraphrased)
- [ ] File paths are complete and valid
- [ ] Line numbers match actual file content
- [ ] Assumptions are explicitly stated
- [ ] No logical leaps without evidence
- [ ] New files are documented
- [ ] Confidence scores are justified

**If MiniMax flags issues:**
- Kimi revises output
- Second review pass
- Maximum 2 revision rounds (prevents infinite loops)

---

## Token Optimization Patterns

### 1. AgentDiet Pattern
- Remove redundant/expired info from trajectories
- **40-60% token savings**

### 2. Observation Masking
- Sliding window for older observations
- **50% cost reduction** vs raw agent

### 3. Parallel Execution
- K2.5 swarm reduces critical-path latency 3-4.5x
- Same tokens, faster completion

### 4. Escape Hatch
- If Kimi can't verify information:
  ```
  [UNVERIFIED]: Claim about X - no source found
  Confidence: Low (30%) - proceed with caution
  ```

---

## Example Usage

### Task: Find Dialogue Presentation Patterns in Quest Files

**Step 1: Claude spawns Kimi with supervisor prompt**

⚠️ **NOTE:** This example is conceptual. In practice, Kimi must be launched via `.\scripts\start-kimi.ps1` in a separate session, NOT via Task tool `model` parameter.

**Conceptual workflow (requires separate Kimi session):**
```markdown
Kimi Prompt Template:
---
You are Kimi K2.5 researching dialogue patterns for Claude.

Task: Find all dialogue presentation patterns in quest files

Deliverable Format:
- Files containing dialogue
- Common patterns (RichTextLabel, dialogue boxes, etc.)
- Direct code quotes with line numbers
- File paths with line numbers

CRITICAL - Show Your Work:
1. Include EXACT code quotes (not paraphrased)
2. File paths with line numbers (path/file.gd:42-56)
3. List all assumptions explicitly
4. Confidence scores with justification

Minimum Confidence: 80%
---
```

**Actual implementation requires:**
1. Launch Kimi in separate terminal: `.\scripts\start-kimi.ps1`
2. Provide prompt to Kimi session manually or via automation
3. Kimi returns synthesis
4. Claude spawns MiniMax to review (via Task tool with `model="minimax"`)
5. Claude receives both outputs and decides

**Step 2: Kimi returns synthesis**

```markdown
## Dialogue Patterns Found

### Pattern 1: RichTextLabel with BBCode
> "dialogue_label.text = \"[wave amp=50]\" + npc_text"
Source: game/quests/quest_1.gd:42

**Locations:**
- game/quests/quest_1.gd:42
- game/quests/quest_2.gd:67
- game/ui/dialogue_box.gd:28

**Confidence:** High (90%) - verified in 3 files

### Assumptions Made
- Assumed dialogue_label is RichTextLabel (based on BBCode usage)
- Inferred [wave] is animation effect (not verified in docs)

### Confidence: Overall 85%
```

**Step 3: Claude spawns MiniMax for review**

✅ **This step works correctly** - MiniMax can be spawned via Task tool:

```python
Task(
  subagent_type="general-purpose",
  model="minimax",  # ✅ Valid - MiniMax supports model parameter
  prompt="""Review the following Kimi synthesis for hallucinations and errors:

[Kimi's output above]

Verify:
- Code quotes are exact (not paraphrased)
- File paths are complete with line numbers
- Assumptions are stated explicitly
- No logical leaps without evidence

Return: APPROVED / NEEDS_REVISION with specific concerns
""",
  description="MiniMax reviews Kimi findings"
)
```

**Step 4: MiniMax returns verification**

```markdown
### MiniMax Review

✅ Code quotes appear exact (BBCode syntax present)
✅ File paths include line numbers
✅ Assumptions are explicitly stated
⚠️  Recommend Claude verify game/quests/quest_1.gd:42 line number

**Status:** APPROVED (spot-check recommended)
**Flagged for verification:** quest_1.gd:42
```

**Step 5: Claude makes decisions**

Claude now has:
- Compressed findings (2k tokens vs 10k+ if Claude explored directly)
- Cross-model verification (MiniMax reviewed)
- Specific items to spot-check if needed
- High confidence to proceed with implementation

---

## API Configuration

**Kimi K2.5 Setup:**
```powershell
# Use existing launcher
.\scripts\start-kimi.ps1

# Or configure environment
$env:ANTHROPIC_BASE_URL = "https://api.moonshot.cn/anthropic/"
$env:ANTHROPIC_API_KEY = "sk-kimi-YOUR_KEY"
$env:ANTHROPIC_MODEL = "kimi-k2.5-thinking"
```

**MiniMax Setup:**
```powershell
# Use existing launcher
.\scripts\start-claude-minimax.ps1

# Or configure environment
$env:ANTHROPIC_BASE_URL = "https://api.minimax.io/anthropic"
$env:ANTHROPIC_API_KEY = "sk-cp-YOUR_KEY"
$env:ANTHROPIC_MODEL = "minimax:m2.1"
```

---

## Limitations & Caveats

**Don't use Kimi Supervisor for:**
- ❌ Code writing (Claude is better)
- ❌ Architectural decisions (Claude maintains control)
- ❌ Single-file reads (too much overhead)
- ❌ Simple queries (no coordination needed)

**When Kimi may struggle:**
- Complex code synthesis (not trained for code generation)
- Subtle semantic understanding (Claude is better)
- Domain-specific reasoning requiring deep context

**Fallback strategy:**
- If Kimi confidence < threshold: escalate to Claude
- If MiniMax rejects 2x: escalate to Claude
- If task takes >5 min: report progress and continue

---

## Success Metrics

**Track these to measure effectiveness:**
- Token reduction: Target 70-90% savings on exploration tasks
- Accuracy: MiniMax approval rate should be >80%
- Speed: Parallel execution should be 3-4x faster
- Claude iterations: Fewer fixes needed post-handoff

**Quality indicators:**
- All code quotes are exact
- File paths are verifiable
- Assumptions are explicit
- Confidence scores are accurate

---

## Integration with Existing Skills

**Complements:**
- `/skill delegation` - Kimi supervisor is one delegation pattern
- `/review` - MiniMax review mirrors the /review workflow
- `/longplan` - Use Kimi for research phases in long plans
- `/ralph` - Kimi can coordinate ralph subagents

**Replaces:**
- Manual spawning of 3+ Explore agents in parallel
- Direct Claude reading of multiple agent outputs
- Self-review (now cross-model MiniMax review)

---

## Next Steps

After using this skill:
1. **Verify Kimi's work** (spot-check high-value claims)
2. **Make architectural decisions** (Claude's role)
3. **Write implementation** (Claude writes code)
4. **Consider updating token budget** (you saved tokens!)

**Future enhancements:**
- Auto-select Kimi vs GLM based on task type
- Track token savings per session
- Build confidence score history
- Create Kimi swarm templates for common patterns

---

**Updated:** 2026-01-29
**Model:** Kimi K2.5 (kimi-k2.5-thinking)
**Review Protocol:** MiniMax M2.1
**Cost:** ~$0.30-0.50/M tokens (vs $15/M for Claude)
