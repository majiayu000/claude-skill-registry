---
name: topic-brainstormer
description: "Generate blog topic ideas: problem mining, gap analysis, expansion."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
command: /brainstorm
routing:
  triggers:
    - "brainstorm topics"
    - "content ideas"
    - "blog topic ideas"
    - "what to write about"
  category: content-creation
  pairs_with:
    - content-calendar
    - series-planner
    - research-pipeline
---

# Topic Brainstormer

## Overview

This skill generates blog post topic ideas that align with a content identity built around solving frustrating technical problems. It operates through three sequential phases (ASSESS → DECIDE → GENERATE) with **hard quality gates**: every topic must pass a three-question content quality filter before presentation. The output is always a prioritized list with impact/vex/resolution scores, never an unfiltered pile of ideas.

Core principle: **Assess-Decide-Generate with Domain Intelligence**. Gather signals from existing content and problem sources, filter candidates ruthlessly, then score and prioritize the survivors.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| filtering topics against blog identity: the three-question test | `content-filter.md` | Loads detailed guidance from `content-filter.md`. |
| scoring topics on impact, vex level, resolution | `priority-scoring.md` | Loads detailed guidance from `priority-scoring.md`. |
| mining topics: problems, gaps, technology expansion | `topic-sources.md` | Loads detailed guidance from `topic-sources.md`. |

## Instructions

### Phase 1: ASSESS

**Goal**: Gather context about existing content and available topic sources.

**Step 1: Scan existing content**

Read all posts in the content directory. Document:

```markdown
## Content Landscape
Posts found: [N]
Content clusters: [list main themes]
Technologies covered: [list]
Last post date: [date]
```

**Step 2: Identify available sources**

Determine which topic sources have material to mine:
- Problem Mining: Recent debugging sessions, errors, config struggles
- Gap Analysis: Cross-references in existing posts that lead nowhere
- Tech Expansion: Adjacent technologies not yet covered

**Step 3: Note cross-references**

Extract all "see also", "related", and cross-reference mentions from existing posts. Flag any that point to content that does not exist.

**Gate**: Content landscape documented, at least 2 sources identified with material. Proceed only when gate passes.

---

### Phase 2: DECIDE

**Goal**: Generate topic candidates and filter them through the content quality test.

**Quality Filter Rule**: This is non-negotiable. Every candidate must answer YES to all three questions. Unfiltered lists waste user time; apply rigor here.

**Step 1: Mine candidates from identified sources**

Generate 5-10 raw topic candidates from at least 2 sources. For each candidate, capture:
- Source (problem mining, gap analysis, or tech expansion)
- Raw topic area
- Initial vex signal (what frustration exists)

**Step 2: Apply content quality filter to every candidate**

Each topic must answer YES to all three questions:

1. **Was there genuine frustration?** Real time lost, multiple failed attempts, unclear docs, or unexpected behavior that blocked progress.
2. **Is there a satisfying resolution?** Clear fix exists, understanding gained, prevention strategy available, or "a-ha moment" to share.
3. **Would this help others?** Problem is reproducible, not too environment-specific, solution is actionable, frustration is relatable.

**Why this matters**: Topics that fail any question produce weak posts. "How to Set Up Hugo" lacks genuine frustration (official docs already cover installation). "Rewriting a Python CLI in Go Cut Startup Time by 10x" has concrete vex (400ms startup delay) and concrete joy (40ms result).

**Step 3: Reject failing candidates**

Remove any topic that fails the filter. Document why each rejection failed:

| Rejected Topic | Failed Question | Reason |
|----------------|-----------------|--------|
| [topic] | [1, 2, or 3] | [why] |

**Failure Mode Warning — Do Not Generate Tutorial-Only Topics**: "How to Set Up X" with vex listed as "learning a new tool" is not genuine frustration. Find the specific friction point. "Hugo Local Build Works But Cloudflare Deploy Fails" has real vex (version mismatch between local and CI).

**Failure Mode Warning — Do Not Accept Opinion Without Experience**: "Why Go Is Better Than Python for CLI Tools" is debate, not experience. This lacks a specific problem solved, no measurable outcome. Ground in measurement instead.

**Gate**: At least 3 candidates pass the content quality filter. If fewer than 3 pass, return to Step 1 with different sources. Proceed only when gate passes.

---

### Phase 3: GENERATE

**Goal**: Score, prioritize, and present the filtered topic list.

**Step 1: Score each passing topic**

Apply the priority matrix to every candidate:

```
Impact (1-5):     How many people face this problem?
Vex Level (1-5):  How frustrating is the problem?
Resolution (1-5): How satisfying is the solution?

Priority Score = Impact x Vex Level x Resolution

  60-125: HIGH PRIORITY    - Write this soon
  30-59:  MEDIUM PRIORITY  - Good candidate with right angle
  15-29:  LOW PRIORITY     - Needs more vex or broader impact
  1-14:   SKIP             - Not enough value for readers
```

**Why scoring matters**: Unscored lists require user re-evaluation. Always include the priority matrix for every topic.

**Step 2: Write specific titles**

Replace vague category titles with failure-mode titles:
- Bad: "Kubernetes Networking Issues"
- Good: "Pod-to-Pod Traffic Works But Service Discovery Fails"

**Failure Mode Warning — Do Not Use Vague Topic Titles**: "Kubernetes Networking Issues" is too broad to act on. Which issues? What specifically failed? Use failure-mode titles instead: "CoreDNS Returns NXDOMAIN for Internal Services" signals real vex and specificity.

**Step 3: Present prioritized output**

```markdown
## Topic Brainstorm Results

### Source: [problem mining / gap analysis / tech expansion]

### HIGH PRIORITY (Strong vex potential)

1. "[Specific Topic Title]"
   The Vex: [What frustration this addresses]
   The Joy: [What satisfying resolution looks like]
   Fits existing: [Which content cluster this joins]
   Estimated: [word count range]
   Score: Impact(N) x Vex(N) x Resolution(N) = [total]

### MEDIUM PRIORITY (Good but needs angle)

2. "[Specific Topic Title]"
   The Vex: [frustration]
   The Joy: [resolution]
   Angle needed: [What narrative hook would strengthen this]
   Score: Impact(N) x Vex(N) x Resolution(N) = [total]

### GAP FILL (Based on existing content)

3. "[Specific Topic Title]"
   Referenced in: [which post mentions this]
   Missing: [what content would fill the gap]
   Score: Impact(N) x Vex(N) x Resolution(N) = [total]

### Recommendations
- Top pick: [Topic N] - [one sentence why]
- Quick win: [Topic N] - [one sentence why]
- Deep dive: [Topic N] - [one sentence why]
```

**Step 4: Handle score ties**

When scores are equal, prefer topics that:
1. Fill an existing content gap
2. Complement recent posts
3. Use technologies already covered (lower research overhead)
4. Have clearer narrative structure

**Gate**: All topics scored, prioritized, and presented with recommendations. Output is complete.

---

## Examples

### Example 1: Problem Mining Session
User says: "I spent all day debugging a Hugo build issue, brainstorm some topics"
Actions:
1. Scan existing posts for Hugo coverage (ASSESS)
2. Mine the debugging session for vex signals, filter through content quality test (DECIDE)
3. Score and present topics with the build issue as high-priority candidate (GENERATE)
Result: Prioritized topic list with the fresh debugging experience as top pick

### Example 2: Content Gap Analysis
User says: "What should I write about next?"
Actions:
1. Read all existing posts, extract cross-references and themes (ASSESS)
2. Identify referenced-but-missing content, filter through content quality test (DECIDE)
3. Score gap-fill topics alongside any problem-mined candidates (GENERATE)
Result: Prioritized list mixing gap fills with fresh topic candidates

---

## Error Handling

### Error: "No Existing Posts to Analyze"
Cause: Content directory is empty or does not exist yet
Solution:
1. Focus entirely on problem mining instead of gap analysis
2. Ask user about recent debugging sessions or technical struggles
3. Check repository CLAUDE.md or project docs for tech stack hints
4. Generate topics from technology interests alone

### Error: "All Candidates Fail content quality Filter"
Cause: Sources lack genuine frustration signals or resolutions
Solution:
1. Ask probing questions: "What broke recently?" or "What took hours to fix?"
2. Reframe tutorial candidates: "What surprised you?" or "What mistake does everyone make?"
3. Shift to a different source (e.g., from gap analysis to problem mining)
4. If no vex exists, acknowledge honestly -- not every session yields topics

### Error: "Topic Too Broad to Score"
Cause: Candidate is a category ("Kubernetes networking") rather than a specific problem
Solution:
1. Break into multiple specific failure modes
2. Ask: "What specific moment was most frustrating?"
3. Use failure-mode title pattern: "[Thing A] works but [Thing B] fails"

### Error: "Resolution Unclear or Missing"
Cause: User has an ongoing issue without a resolution, or the fix is a workaround with no understanding
Solution:
1. Ask: "Did you solve it? How?"
2. If unresolved, defer the topic until resolution is found
3. If workaround-only, assess whether "understanding why the workaround works" provides enough joy
4. Consider documenting the investigation so far as a "part 1" topic (requires series planning)

---

## References

This skill uses these patterns:
- **Content Quality Filter**: Three-question test (frustration + resolution + helpfulness) is the gate
- **Priority Scoring**: Always use the Impact × Vex × Resolution matrix
- **Failure-Mode Titles**: Specific problem descriptors, never vague categories
- **Problem Mining Signals**: Debugging sessions, Stack Overflow searches, error messages, config struggles
- **Gap Analysis**: "See also" missing posts, prerequisites assumed, incomplete series, follow-up questions
- **Technology Expansion**: Same tool/different feature, same category/different tool, integration opportunities
