---
name: claim-investigation
description: Systematically investigate social media claims and viral content. Use when fact-checking complex claims, when decomposing multi-part assertions, or when investigating narratives that mix facts with interpretation.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Claim Investigation: Systematic Fact-Checking Skill

You help systematically investigate claims from social media and other sources, separating verifiable facts from narrative interpretation and identifying what can and cannot be confirmed.

## Core Principle

Complex claims typically combine verifiable facts with unverifiable interpretations. Effective investigation decomposes claims into atomic components, verifies each independently, and clearly distinguishes between confirmed facts and narrative framing.

## Phase 1: Claim Decomposition

### 1.1 Extract Atomic Claims
Break the statement into individual verifiable claims. Each should be:
- A single factual assertion
- Independently verifiable
- Free of narrative interpretation

**Example Decomposition**:
Original: "The House Leader refusing to seat the newly-elected AZ-07 special election winner because she'd vote to release the Epstein files"

Atomic claims:
1. There is a House Leader (entity exists)
2. There was an AZ-07 special election (event occurred)
3. Someone won that election (result exists)
4. The winner has not been seated (current state)
5. A refusal action occurred (specific action claim)
6. Causal relationship with Epstein files (causation claim)

### 1.2 Classify Each Component

| Type | Description | Verifiability |
|------|-------------|---------------|
| ENTITY | Person, organization, place | Usually verifiable |
| EVENT | Something that allegedly happened | Often verifiable |
| STATE | Current condition or status | Usually verifiable |
| PROCESS | Official procedure or mechanism | Verifiable |
| CAUSATION | Claimed reason or motivation | Rarely verifiable |
| NARRATIVE | Interpretive framing | Not directly verifiable |

### 1.3 Identify Missing Information
Note what's conspicuously absent:
- Unnamed entities ("the winner" instead of a name)
- Unspecified dates
- Missing procedural context
- Absent opposing perspectives

## Phase 2: Entity Resolution

### 2.1 Resolve Vague References
Convert vague references to specific, searchable terms:
- "House Leader" → Current House Speaker/Majority Leader name
- "newly-elected winner" → Candidate names from election results
- "Epstein files" → Specific documents/investigations

### 2.2 Establish Timeline
For each event:
- When did it allegedly occur?
- What is normal timeline for this type of event?
- Are there procedural deadlines involved?

### 2.3 Identify Key Actors
- Primary actors (those taking alleged actions)
- Secondary actors (those affected)
- Official bodies with relevant authority
- Potential sources of verification

## Phase 3: Systematic Verification

### 3.1 Verify Foundational Facts First
Start with most basic, verifiable claims:
1. Did the event occur?
2. Do the entities exist?
3. Are basic facts correct?

**Search Strategy**:
- Official sources first (.gov, electoral bodies)
- Cross-reference multiple news sources
- Look for primary documents

### 3.2 Investigate Procedural Context
For any claimed action/inaction:
1. What is normal procedure?
2. What are requirements?
3. What is typical timeline?
4. What are legitimate reasons for delays?

### 3.3 Examine Causation Claims
For any "because" or causal claim:

**Direct Evidence**:
- Quoted statements from alleged actor
- Official statements or press releases
- Video/audio of relevant statements

**Indirect Evidence**:
- Other explanations for observed facts
- Standard reasons for similar situations
- Procedural explanations

**Context**:
- Previous positions by involved parties
- Historical precedents
- Timeline compatibility

## Phase 4: Source Evaluation

### 4.1 Source Priority Order
1. Official government records/databases
2. Direct statements from involved parties
3. Court documents or legal filings
4. Contemporary news reports (multiple outlets)
5. Analysis or opinion pieces (noted as such)

### 4.2 Credibility Markers
For each source, note:
- Type (official, news, advocacy, social media)
- Date relative to events
- Whether claims are attributed
- Presence of supporting documentation
- Corrections or updates issued

### 4.3 Bias Indicators
Document without dismissing:
- Source's typical political alignment
- Stakeholder relationships
- Pattern of coverage
- Language choices (neutral vs charged)

## Phase 5: Narrative Pattern Recognition

### 5.1 Identify Narrative Constructions
Patterns indicating narrative rather than fact:
- Causal chains without evidence ("X because Y because Z")
- Mind-reading claims ("thinks that," "wants to")
- Selective fact inclusion
- Temporal conflation (mixing time periods)
- False dichotomies

### 5.2 Find Counter-Narratives
For each narrative:
- What facts support it?
- What facts complicate it?
- What alternative narratives explain same facts?
- What facts are excluded?

### 5.3 Missing Context
What would change interpretation:
- Standard procedures being followed
- Similar historical cases
- Full quotes vs partial quotes
- Events immediately before/after

## Phase 6: Synthesis and Reporting

### 6.1 Report Structure

```
VERIFIED FACTS:
- [Fact] (Source: [citation])

DISPUTED/UNCLEAR:
- [Claim]:
  - Supporting: [source]
  - Contradicting: [source]
  - Unable to verify: [what's missing]

CONTEXT NEEDED:
- [Procedural context]
- [Historical precedent]
- [Timeline considerations]

NARRATIVE ELEMENTS:
- [Claim]
  - Facts that support: [list]
  - Facts that complicate: [list]
  - Alternative explanations: [list]
```

### 6.2 Confidence Levels

| Level | Meaning |
|-------|---------|
| **Certain** | Multiple primary sources confirm |
| **Probable** | Multiple credible sources align, no contradictions |
| **Possible** | Some evidence supports, gaps remain |
| **Unclear** | Contradictory evidence or insufficient info |
| **False** | Contradicted by authoritative sources |

## Phase 7: Meta-Analysis

### 7.1 Information Gaps
Document what couldn't be determined:
- Information that should exist but wasn't found
- Questions that remain unanswered
- Time constraints on verification

### 7.2 Manipulation Indicators
Patterns suggesting intentional misrepresentation:
- Key facts consistently omitted
- Misquoted or out-of-context statements
- Conflation of different events/people
- Old events presented as new

### 7.3 Further Investigation
If initial investigation reveals deeper issues:
- What additional tools/access would help?
- What questions should be asked of officials?
- What documents should be requested?

## Search Query Construction

- Start broad, then narrow
- Use multiple phrasings for same concept
- Include date ranges when relevant
- Search for both supporting and contradicting evidence
- Use exact phrases for quotes, broad terms for concepts

## Output Principles

1. Lead with verified facts
2. Clearly separate facts from analysis
3. Include all relevant context
4. Present multiple valid interpretations where applicable
5. Never assert causation without evidence
6. Acknowledge investigation limitations

## Output Persistence

### Output Discovery
1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found, ask user: "Where should I save investigation reports?"
4. Suggest: `research/investigations/` or `explorations/research/`

### Primary Output
- **Decomposed claims** - Atomic components with classifications
- **Verification results** - Confidence levels per component
- **Context documentation** - Procedural and historical context
- **Synthesis report** - Using standard report structure

### File Naming
Pattern: `{topic}-investigation-{date}.md`

## Verification (Oracle)

### What This Skill Can Verify
- **Decomposition complete** - All atomic claims identified? (High confidence)
- **Entity resolution** - Vague references resolved? (High confidence)
- **Source evaluation** - Credibility markers documented? (High confidence)

### What Requires Human Judgment
- **Source reliability** - Contextual trust assessment
- **Narrative interpretation** - Which framing is most accurate?
- **Manipulation detection** - Intent behind information gaps

### Oracle Limitations
- Cannot assess motivations behind claims
- Cannot predict how information will evolve

## Feedback Loop

### Session Persistence
- **Output location:** See `context/output-config.md`
- **What to save:** Decomposition, verification, context, synthesis
- **Naming pattern:** `{topic}-investigation-{date}.md`

### Cross-Session Learning
- Check for prior investigations on related topics
- Build on previous source evaluations
- Failed verifications inform methodology

## Design Constraints

### This Skill Assumes
- A specific claim to investigate (not general research)
- Verifiable components exist within the claim
- Sources are accessible for verification

### This Skill Does Not Handle
- **General research** - Route to: research
- **AI output verification** - Route to: fact-check
- **Media pattern analysis** - Route to: media-meta-analysis

### Degradation Signals
- Single-source verification (confirmation rush)
- Accepting causation without evidence
- Dismissing entire claims for single errors

## Reasoning Requirements

### Standard Reasoning
- Single claim decomposition
- Basic entity resolution
- Simple source evaluation

### Extended Reasoning (ultrathink)
- **Multi-claim investigation** - [Why: claims interact and context builds]
- **Narrative analysis** - [Why: detecting manipulation patterns]
- **Deep source tracing** - [Why: finding original sources through citation chains]

**Trigger phrases:** "full investigation", "trace all sources", "analyze the narrative"

## Execution Strategy

### Sequential (Default)
- Decomposition before verification
- Foundational facts before causation claims
- Individual components before synthesis

### Parallelizable
- Verifying independent atomic claims
- Researching multiple sources simultaneously

### Subagent Candidates
| Task | Agent Type | When to Spawn |
|------|------------|---------------|
| Source research | general-purpose | When tracing claim origins |
| Timeline construction | general-purpose | When mapping event sequences |

## Context Management

### Approximate Token Footprint
- **Skill base:** ~3.5k tokens (phases + templates)
- **With examples:** ~4.5k tokens
- **With full output structure:** ~5k tokens

### Context Optimization
- Focus on current investigation phase
- Report structure is reference, not in-context
- Examples optional

### When Context Gets Tight
- Prioritize: Current phase, active claims
- Defer: Full template structure, all phases
- Drop: Meta-analysis section, search examples

## Anti-Patterns

### 1. Confirmation Rush
**Pattern:** Finding one source that matches the claim and declaring it verified.
**Why it fails:** Single-source verification misses errors, biases, and coordinated misinformation where multiple outlets repeat the same false claim without independent verification.
**Fix:** Require at least 2-3 independent sources. Trace claims back to primary sources. Check if "multiple sources" are actually just repeating the same original source.

### 2. Causation Collapse
**Pattern:** Accepting "X happened because Y" claims when only "X happened" and "Y exists" are verified.
**Why it fails:** Correlation proves co-occurrence, not causation. Human pattern-matching fills in causal links that may not exist. Political narratives especially exploit this gap.
**Fix:** Demand direct evidence for causation (stated intent, documented decisions). When causation can't be verified, report it as "alleged motivation" or "claimed reason."

### 3. Premature Debunking
**Pattern:** Finding one fact wrong and dismissing the entire claim without investigating other components.
**Why it fails:** Complex claims often mix true and false elements. Dismissing everything because one part is wrong misses real issues embedded in the narrative.
**Fix:** Decompose fully, verify each component independently. Report accuracy per-component: "Claims A and C are verified; claim B is false; claim D is unverifiable."

### 4. Authority Fallacy
**Pattern:** Accepting official sources uncritically because they're "authoritative."
**Why it fails:** Official sources can be wrong, incomplete, outdated, or deliberately misleading. Authority reduces probability of error but doesn't eliminate it.
**Fix:** Cross-reference official sources with other evidence. Note when official sources have incentives to misrepresent. Distinguish between "official position" and "verified fact."

### 5. Narrative Anchoring
**Pattern:** Starting with a hypothesis about what's "really happening" and investigating to prove it.
**Why it fails:** Confirmation bias shapes what evidence you seek and how you interpret it. You'll find "evidence" for any narrative if you look hard enough.
**Fix:** Start with the specific claims made. Investigate each on its own terms. Actively seek disconfirming evidence. Document alternative explanations that fit the same facts.

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| research | Initial source discovery and query expansion |
| media-meta-analysis | Understanding of source biases and media patterns |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| fact-check | Verified facts for post-generation checking |
| sensitivity-check | Context for evaluating representation claims |

### Complementary
| Skill | Relationship |
|-------|--------------|
| research | Use research for broad information gathering, claim-investigation for specific claim verification |
| fact-check | Use claim-investigation for external claims, fact-check for AI-generated content verification |
