---
name: context-continuity
description: High-fidelity context transfer protocol for moving conversations between AI agents. Preserves decision tempo, open loops, and critical context with graceful degradation. Use when the user says "transfer," "handoff," "continue this in another chat," or needs to work around context window limits. Produces structured artifacts (Minimal ~200 words, Full ~1000 words). DO NOT trigger on simple "summarize our conversation" requests—only when transfer intent is explicit.
---

# Context Continuity Protocol v2

Enable high-fidelity context transfer between AI agents with graceful degradation and zero external dependencies.

## Core Concept

When conversations need to transfer between AI agents (different chats, different systems, context window resets), context is typically lost or degraded through naive copy-paste. This protocol creates structured artifacts that:

- **Preserve decision tempo** - Avoid rehashing resolved questions
- **Maintain forward momentum** - Surface open loops and next actions
- **Gracefully degrade** - Critical information survives truncation
- **Separate fact from interpretation** - What happened vs. why it matters
- **Support both human and machine parsing** - Scannable and structured

## When to Use This Skill

Use this skill when:
- User explicitly says "transfer this conversation," "continue this elsewhere," "handoff," "create a transfer artifact"
- Context window is filling and user needs to start fresh with preserved state
- User wants to switch between Claude instances while maintaining continuity
- User asks to "summarize for transfer" (explicit transfer intent)

DO NOT use for general conversation summaries without transfer intent.

## Workflow: Automatic Mode Selection

I automatically choose the appropriate mode based on conversation complexity:

**Minimal Mode (~200 words)** - Used when:
- Conversation < 30 messages OR straightforward single objective
- Few decision points (1-2)
- Quick task handoff

**Full Mode (~1000 words)** - Used when:
- Conversation ≥ 30 messages OR multiple decisions identified
- Complex strategic work, long-running project
- User says "comprehensive," "detailed," or "full handoff"

**User can override:** Say "minimal transfer" or "quick handoff" to force Minimal mode regardless of complexity

---

## Minimal Mode (Fast Path)

Generate immediately without reading reference files:

```markdown
═══════════════════════════════════════════════════════════════════
CONTEXT TRANSFER — MINIMAL MODE
═══════════════════════════════════════════════════════════════════

**TRANSFER**: [One sentence: what we're accomplishing]

**STATUS**: [✓ resolved | ⧗ in-progress | ⚠ blocked | ↻ iterating]

**DECIDED**: [Key decision + rationale | If multiple, bullet list with "because..."]
  - Alternatives rejected: [What we explicitly didn't do]

**NEXT**: [Immediate next action when conversation resumes]

**BLOCKED**: [If anything is preventing progress]

**CONTEXT**: [1-2 para critical background—constraints, values at stake, key insights]

**HUMAN PREFS**: [Communication style: direct/exploratory | technical/narrative]

═══════════════════════════════════════════════════════════════════
Generated: [ISO timestamp] | Session: [ID if available]
```

**After generating, ask:**
"Before you transfer—are there any sections that need further detail or refinement?"

---

## Full Mode (Comprehensive Path)

For complex transfers, generate the complete 8-section artifact.

### Step 1: Analyze the Conversation

Extract these elements **directly** (no file reads needed for standard cases):

**§ Immediate Orientation**
- Mission: [One clear sentence: what + why it matters]
- Status: [Current state + progress + momentum]
- Next Action: [What should happen when conversation resumes]

**§ Decision Log**
| Decision | Rationale | Alternatives Rejected | Tradeoff Accepted | Type |
|----------|-----------|----------------------|-------------------|------|
| [What] | [Why] | [What we didn't do] | [Cost we're paying] | [explicit\|implicit\|emergent] |

- Decision Type:
  - **explicit** = deliberate choice with clear rationale
  - **implicit** = we started doing X without formal decision
  - **emergent** = pattern that evolved over conversation
- Decision principles applied: [OODA, Wardley, Cynefin, etc. if used]

**§ Open Loops**
- Unresolved questions: [What needs answering]
- Blockers: [What's preventing progress + why]
- Pending inputs: [Waiting for human/data/time]
- Hypotheses to test: [Assumptions needing validation]

**§ Critical Context**
- Key insights [tag with evolution stage]:
  - [G] = Genesis (novel discovery, first-time insight)
  - [C] = Custom (emerging pattern, still validating)
  - [P] = Product (established approach, proven)
  - [K] = Commodity (common knowledge, standard practice)
- Constraints: [Technical | Resource | Political/Org | Ethical]
- Uncertainty map: [Known unknowns | Model weaknesses | Risk factors]
- Values at stake: [What matters beyond task completion]

**§ Artifacts & Outputs**
- Created: [Files/code/analyses with 1-line summary + key finding]
- Referenced: [External resources + why they matter]
- Tools used: [How leveraged + results]

**§ Human Context**
- Communication preferences: [Style | Depth | Archetypes engaged]
- Assumed knowledge: [Domain expertise | Shared frameworks]
- Session dynamics: [Trust level | Collaboration mode | Sensitivities]

**§ Conversation History** (optional, use `<details>` tag)
- Act I: Problem Formation [messages 1-X]
- Act II: Exploration & Development [messages X-Y]
- Act III: Current State [messages Y-now]
- Notable moments: [Load-bearing jokes/metaphors/exchanges]

**§ Transfer Metadata**
- Provenance: [Source agent]
- Context window pressure: [○ spacious | ◐ moderate | ● constrained]
- Completeness: [Visual bar + % + what's missing if <100%]
- Verification: [✓ human reviewed | ⚠ unverified | ⧗ partial]
- Handoff notes: [Special instructions | Warnings | Suggested first questions]

### Step 2: Structure Using Template

View the full template if you need detailed structure reference:
```bash
view /home/claude/context-continuity/references/artifact-template.md
```

**But for most cases, the extraction checklist above is sufficient.**

### Step 3: Present with Engagement Prompt

After generating the artifact:

1. Present it in full
2. Add: "§ TRANSFER READY—Review for accuracy before sharing."
3. **Then ask**: "Before you transfer, are there any sections that need further detail or refinement?"

This forces human review and catches errors early.

### Step 4: Optional Receiver Guidance

If the human wants guidance for the receiving agent:
```bash
view /home/claude/context-continuity/references/receiver-prompt.md
```

This is an optional prepend with instructions for processing the artifact.

## Design Principles

**Dual-mode operation**: Minimal mode for speed (80% of cases), Full mode for complexity (20% of cases).

**Antifragile**: Critical information at top. Truncation doesn't break core functionality.

**Dual interface**: Human-scannable (they verify) + machine-parseable (structured sections).

**Tempo preservation**: Decision log with type taxonomy prevents circular rehashing.

**Fact-meaning separation**: Artifacts = what exists. Critical Context = why it matters.

**Evolution awareness**: [G/C/P/K] tags help receiving agent understand information maturity:
- [G] = Genesis (novel, first-time discovery)
- [C] = Custom (emerging, still being validated)
- [P] = Product (established, proven approach)
- [K] = Commodity (common knowledge)

**Forced engagement**: Ask if any sections need refinement—prevents blind paste.

## Usage Examples

**Example 1: Quick transfer (Minimal mode - auto-selected)**
```
User: "I need to continue this in another chat. Transfer the context."

Agent: [Analyzes: 12 messages, single objective, straightforward → Minimal mode]
       [Generates minimal mode artifact immediately—no file reads]
       [Presents artifact]
       "§ TRANSFER READY—Before you transfer, are there any sections that need
       further detail or refinement?"
```

**Example 2: Complex project transfer (Full mode - auto-selected)**
```
User: "Create a comprehensive handoff for this AI transformation project."

Agent: [Analyzes: 45 messages, multiple decisions, strategic work → Full mode]
       [Generates 8-section artifact with decision log, open loops, critical context]
       [Presents artifact]
       "§ TRANSFER READY—Before you transfer, are there any sections that need
       further detail or refinement?"

User: "Yes, expand the Critical Context around measurement challenges."

Agent: [Expands § Critical Context with more detail on metrics selection debate]
```

**Example 3: Context window pressure (Full mode - auto-selected)**
```
User: "We're at 180k tokens. Compress for a fresh start."

Agent: [Analyzes: 180K tokens, long conversation → Full mode]
       [Generates Full mode artifact]
       [Notes in § Transfer Metadata: "Context window pressure: ● constrained"]
       [Keeps § Conversation History concise]
```

## Best Practices

### For Generating Agents

**Do:**
- Auto-select mode based on conversation complexity (user can override)
- Be specific about decisions—include Type (explicit | implicit | emergent)
- Flag uncertainties explicitly in Uncertainty Map
- Mark evolution stage for key insights ([G/C/P/K])
- Include enough detail for receiving agent to avoid stupid mistakes
- Note human communication preferences and sensitivities
- **Always ask** if any sections need further detail or refinement after presenting artifact

**Don't:**
- Generalize or use vague language ("made progress" → specify what was completed)
- Omit the rationale behind decisions
- Assume receiving agent has conversational context
- Fabricate post-hoc rationale for emergent decisions (mark them as "emergent" instead)
- Let human paste without reviewing—force engagement with quality verification question

**Decision Type Guide:**
- **Explicit**: "We decided to use OODA loops because..." (deliberate choice)
- **Implicit**: "Started using OODA loops for orientation framing" (no formal decision, just did it)
- **Emergent**: "OODA loops emerged as our primary framework through repeated use" (pattern that evolved)

### For Receiving Agents

When you receive a context transfer artifact:

1. **Scan § Immediate Orientation first** - Get bearings quickly
2. **Read § Decision Log before proposing** - Don't rehash resolved debates
3. **Check § Open Loops** - Know what needs attention
4. **Review § Critical Context** - Understand constraints and values at stake
5. **Acknowledge with handshake** - Confirm understanding before continuing

**Handshake Protocol (CRITICAL):**
After reading the artifact, respond with:

"I've reviewed the transfer. Quick confirmation:
- Mission: [Echo back mission in your own words]
- Status: [Echo back current state]
- Next: [Echo back immediate next action]

Ready to [next action]. What's your priority?"

This catches misinterpretation early and gives human confidence you understood the context.

**Natural integration examples:**
- Bad: "I can see from the context transfer artifact that..."
- Good: "Picking up where we left off—you're building the measurement framework..."

### For Humans

**Before pasting to new agent:**
- Answer the "which section to expand" question (don't skip it)
- Scan for accuracy and completeness
- Redact any sensitive information
- Verify § NEXT ACTION matches your intent
- Consider if receiver needs the optional prepend from receiver-prompt.md

**When starting with new agent:**
- Paste artifact first, then state your immediate need
- Wait for handshake confirmation (mission/status/next echo-back)
- If agent seems confused, point them to specific sections
- Don't expect perfect continuity—some context loss is unavoidable, but handshake catches major gaps

## Failure Modes and Mitigations

**Problem:** Receiving agent treats artifact as gospel instead of hypothesis
**Mitigation:** § Transfer Metadata includes uncertainty indicators and handoff notes

**Problem:** Human doesn't know what's critical to preserve
**Mitigation:** Generator prompt asks for evolution tags and uncertainty maps

**Problem:** Truncation cuts off critical context
**Mitigation:** Antifragile structure puts critical info at top; each section is self-contained

**Problem:** Load-bearing jokes or metaphors lost
**Mitigation:** § Conversation History explicitly calls out notable moments

**Problem:** Over-reliance on artifact instead of re-orientation
**Mitigation:** Artifact is starting hypothesis, not replacement for human context-setting

## Advanced Usage

### Iterative Transfers

For long-running projects requiring multiple transfers:
1. Previous artifacts can be referenced in § Conversation History
2. Evolution tags track how understanding matured across agents
3. Decision log accumulates decisions across transfer boundaries

### Cross-System Transfers

The protocol is system-agnostic:
- No special formatting beyond markdown
- No assumptions about tool access
- Works between Claude instances, other LLMs, or human-to-human handoffs

### Custom Adaptations

The template can be adapted:
- Add domain-specific sections (e.g., § Code Context for dev projects)
- Reorder sections if different prioritization makes sense
- Use minimal mode for constrained environments
- Adjust detail level based on trust/familiarity with receiving agent

## References

All reference materials are in the `references/` directory:

- **generator-prompt.md** - Prompt to give generating agent for creating artifacts
- **artifact-template.md** - Complete template structure and design principles
- **receiver-prompt.md** - Optional prepend for receiving agent guidance
- **examples.md** - Real-world transfer scenarios showing both modes in action

Load these as needed during the workflow.
