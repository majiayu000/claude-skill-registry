---
name: analyzing-meetings
description: |
  MUST BE USED when analyzing meeting transcripts or notes.
  Classifies input type, attributes speakers, and verifies names against colleagues.json.
  Works with routing-initiatives and summarizing-meetings skills for complete workflow.
---

# Analyzing Meetings Skill

## Purpose

Analyze meeting input to prepare it for routing and summarization:
1. **Classify input type** (transcript vs notes vs hybrid)
2. **Attribute speakers** with confidence levels
3. **Verify names** against `Reference/colleagues.json`

For product-specific context, see `CLAUDE.local.md`.

---

## Persona

**Role**: Programme Manager / Chief of Staff with exceptional attention to detail

**Experience**: 10+ years supporting senior leadership, skilled at distilling complex discussions into actionable content.

**Mindset**:
- Completeness over speed - never analyze based on partial reading
- Action-oriented - every analysis should enable follow-up
- Diplomatically accurate - captures substance without editorializing

---

## Input Classification

### Step 1: Detect Input Type

| Input Type | Characteristics | Processing Approach |
|------------|-----------------|---------------------|
| **Raw Transcript** | Speaker labels, timestamps, disfluencies, "um/uh" | Clean, segment by speaker turns |
| **Meeting Notes** | Bullet points, headers, structured sections | Parse structure, extract by section |
| **Hybrid** | Mix of verbatim quotes and summarized points | Apply both parsers, merge results |

### Detection Heuristics

**Raw Transcript indicators**:
- Speaker labels: `[John]:`, `Speaker 1:`, `John Smith:`
- Timestamps: `[00:15:32]`, `(15:32)`
- Filler words: "um", "uh", "like", "you know"
- Incomplete sentences, interruptions marked with `--`

**Meeting Notes indicators**:
- Markdown headers: `#`, `##`, `###`
- Bullet points: `-`, `*`, `•`
- Action item markers: `[ ]`, `TODO:`, `Action:`
- Structured sections: "Attendees:", "Decisions:", "Next Steps:"

---

## Speaker Attribution Protocol

### Input Assessment

| Label Type | Examples | Attribution Approach |
|------------|----------|---------------------|
| **Explicit labels** | `[John]:`, `Speaker 1:` | Use directly |
| **Partial labels** | `J:`, timestamps only | Infer with medium confidence |
| **No labels** | Continuous text | Apply inference heuristics |

### Attribution Heuristics

**Positional Inference**:
- First speaker often sets agenda (likely meeting owner)
- Responses to questions indicate different speaker
- "I'll do X" vs "Can you do X" indicates speaker switch

**Contextual Clues**:
| Clue Type | Example | Inference |
|-----------|---------|-----------|
| **Role statement** | "As the PM..." | Speaker is a PM |
| **Self-reference** | "My team will handle..." | Speaker has a team |
| **Domain expertise** | Deep technical details | Likely engineer/specialist |
| **First-person ownership** | "I've been working on..." | Speaker owns that work |

**Conversation Flow**:
- Question → Answer = speaker change
- Agreement ("Yes, and...") = new speaker
- Topic shift = possible new speaker

### Confidence Levels

| Level | Score | Criteria | Action |
|-------|-------|----------|--------|
| **High** | 0.8+ | Explicit name, clear role statement | Attribute directly |
| **Medium** | 0.5-0.8 | Strong contextual clues | Attribute with [Inferred] tag |
| **Low** | < 0.5 | Ambiguous clues | Ask user |

### Output Formats

**High confidence:**
```markdown
**[Name]**: "We should prioritize the API work for Q2"
```

**Medium confidence:**
```markdown
**[Inferred: Engineering Lead]**: "The technical debt is blocking new features"
- *Attribution basis*: Speaker discussed technical architecture
```

**Low confidence:**
```
I couldn't determine who said this:
**Quote**: "We need to push back the launch date"
Who made this statement?
a) [Name 1]  b) [Name 2]  c) Someone else  d) Unknown
```

### Critical Attribution Requirements

**MUST attribute (ask if uncertain):**
- Action item owners ("I'll handle X")
- Decision makers ("We've decided to...")
- Blockers/concerns raised ("I'm worried about...")
- Commitments made ("My team can deliver by...")

---

## Name Verification Protocol

### Purpose

Transcription services often misspell names. Use `Reference/colleagues.json` to verify.

### When to Verify

Check a name against colleagues.json when:
- Name spelling looks phonetically plausible but unusual
- Name doesn't match any known colleague exactly
- Name appears in action item owner context

### Verification Process

```
1. Extract all names mentioned
2. For each name:
   a. Check exact match in colleagues.json → Use as-is
   b. If no exact match:
      - Check commonAliases
      - Search for phonetically similar names
   c. If match found with high confidence → Auto-correct
   d. If uncertain → Flag for user verification
```

### Correction Format

- **Auto-corrected**: Just use the correct name
- **Uncertain**: Note original: "[Corrected from: original transcription]"

For detailed name lookup protocols, see `.claude/reference/name-verification.md`.

---

## Example Input

```
[00:15:32] Speaker 1: So I think we should move forward with the React migration.
[00:15:45] Speaker 2: I agree, but we need to consider the timeline. My team is already stretched.
[00:16:02] Speaker 1: Can you give me a realistic estimate?
```

## Example Output

```markdown
## Input Classification
**Type**: Raw Transcript
**Speaker Labels**: Partial (numbered speakers, timestamps)
**Duration**: ~1 minute segment

## Speaker Attribution
- **Speaker 1** [Inferred: PM/Lead]: Sets agenda, asks for estimates
- **Speaker 2** [Inferred: Engineering Lead]: References "my team", timeline concerns

## Names Verified
- No names mentioned directly in this segment
- "Speaker 2" likely engineering based on team reference

## Ready for Routing
- 1 potential decision: React migration
- 1 action item: Timeline estimate needed
- Attribution: Ask user to confirm speaker identities
```

---

## Quality Gates

- [ ] Complete content read (beginning to end)
- [ ] Input type correctly classified
- [ ] Speaker label presence assessed
- [ ] Names verified against colleagues.json
- [ ] Attribution confidence levels assigned
- [ ] Action item owners identified or flagged

---

## Success Criteria

1. Input type correctly identified
2. Speakers attributed with appropriate confidence
3. Names verified and corrected if needed
4. Ready for routing-initiatives skill
