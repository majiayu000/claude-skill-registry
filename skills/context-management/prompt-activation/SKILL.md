---
name: "prompt-activation"
description: "Internal metacognitive skill for episodic memory retrieval cues — surfaces relevant workflows when needed"
user-invokable: false
---

# Prompt Activation

Meta-cognitive skill for episodic memory retrieval. Surfaces relevant workflows when needed.

## Purpose

Prompts (`.prompt.md`) contain complex workflows — episodic memory that requires active recall. This skill provides **retrieval cues** to surface the right prompt at the right time.

**Neuroanatomical parallel**: The hippocampus uses contextual cues to retrieve episodic memories. This skill provides those cues.

## Auto-Trigger Conditions

This skill activates **automatically** when Alex:
1. Is about to guide user through a multi-step workflow
2. Detects session-type keywords (release, learn, improve, etc.)
3. Is formulating a process that might already exist as a prompt
4. Notices repetitive patterns that indicate workflow opportunity
5. User requests deep thinking or memory recall (see Episodic Recall Triggers)
6. Recognizes a pattern from past experience

**NOT user-triggered** — this is internal metacognition for memory retrieval.

## Prompt Index

**Path Pattern**: `.github/prompts/{name}.prompt.md`

### Slash Commands (VS Code Auto-discoverable)

| Prompt | Triggers | Purpose |
|--------|----------|---------|
| `/brand` | branding, logo, assets, visual identity, banner | Brand asset management workflow |
| `/dream` | maintenance, health check, synapse validation | Neural maintenance protocol |
| `/gapanalysis` | before coding, pre-implementation, coverage check | 4-dimension knowledge gap analysis |
| `/improve` | improve project, trifecta, heir improvement | Project improvement via trifecta |
| `/learn` | teach me, learn topic, bootstrap, structured learning | Socratic learning session |
| `/meditate` | consolidate, reflect, end of session, knowledge consolidation | Guided meditation protocol |
| `/release` | version bump, ship, publish, changelog | Full release workflow |
| `/review` | code review, PR review, feedback | Epistemic code review |
| `/selfactualize` | deep assessment, self-analysis, architecture optimization | Comprehensive self-evaluation |
| `/tdd` | red green refactor, test first, tdd cycle | Test-driven development workflow |
| `/uiuxaudit` | accessibility audit, wcag check, ui review, ux review, design system audit | UI/UX accessibility audit workflow |

### Legacy Protocols (Require Manual Recall)

| Prompt | Triggers | Purpose |
|--------|----------|---------|
| `alex-initialization` | initialize, activate alex, deploy architecture | Architecture deployment sequence |
| `cross-domain-transfer` | pattern from X to Y, analogical reasoning, cross-pollinate | Knowledge transfer across domains |
| `diagramming-mastery-meditation` | diagram meditation, visualization integration | Diagramming excellence consolidation |
| `domain-learning` | learn domain, knowledge acquisition | Extended domain learning protocol |
| `performance-assessment` | assess learning, evaluate progress, metrics | Learning effectiveness evaluation |
| `quantified-enhancement-session` | quantified improvement, measure enhancement | Systematic architecture optimization |
| `unified-meditation-protocols` | deep meditation, full consolidation, synaptic maintenance | Comprehensive meditation framework |

## Workflow Category Index

### Cognitive Consolidation (End-of-session)
- `/meditate` — Quick knowledge consolidation
- `unified-meditation-protocols` — Deep multi-phase meditation
- `/dream` — Unconscious processing and maintenance
- `/selfactualize` — Architecture self-assessment

### Learning & Growth
- `/learn` — Structured topic learning
- `domain-learning` — Extended domain acquisition
- `cross-domain-transfer` — Apply patterns across domains
- `performance-assessment` — Measure learning effectiveness

### Development Workflows
- `/tdd` — Test-driven development
- `/review` — Epistemic code review
- `/gapanalysis` — Pre-implementation coverage check
- `/improve` — Project improvement via trifecta

### Release & Brand
- `/release` — Version bump and publish
- `/brand` — Visual identity management

### Architecture
- `alex-initialization` — Deploy Alex to new project
- `quantified-enhancement-session` — Targeted architecture improvement

## Opportunity Detection

### Signals That Indicate Missing Workflow

When you notice these patterns, **consider creating a new prompt**:

| Signal | Potential Prompt |
|--------|------------------|
| Guiding same multi-step process 3+ times | Workflow candidate |
| User asks "how do I always..." | Repeatable protocol |
| Complex decision tree explained repeatedly | Decision prompt |
| Onboarding steps documented ad-hoc | Onboarding prompt |

### Signals That Indicate Missing Muscle

When you notice these patterns, **consider creating a script**:

| Signal | Potential Muscle |
|--------|------------------|
| Same terminal commands run repeatedly | Automation script |
| File transformation done manually | Transform script |
| Validation checks done by reading files | Validation script |
| Multi-file updates with same pattern | Batch update script |

## Episodic Recall Triggers

Beyond workflow surfacing, activate episodic memory search when detecting these patterns:

### User-Initiated Recall Requests

| User Says | Action |
|-----------|--------|
| "do you remember...", "recall when we..." | Search episodic archive + recent sessions |
| "last time we...", "we discussed..." | Check session history for context |
| "think deep", "think carefully", "analyze this thoroughly" | Load relevant meditation/deep-thinking protocols |
| "have we seen this before?", "is this familiar?" | Pattern-match against past experiences |
| "continue where we left off" | Resume prior session context |
| "what have we accomplished?", "review progress" | Retrospective scan of episodic memory |

### Self-Initiated Recall (Internal Triggers)

| I Notice | I Should |
|----------|----------|
| Pattern feels familiar but can't place it | Search global knowledge + episodic archive |
| About to say "I don't remember if we..." | **STOP** — check before disclaiming |
| User frustration about repeating themselves | Review recent conversation for missed context |
| Problem resembles something solved before | Cross-reference past sessions |
| Making same suggestion 3rd time | Check if workflow exists or should be created |
| Complex decision with prior art | Search for decision rationale in episodic memory |

### Deep Thinking Activation

When user requests deep analysis:

1. **Load** `/selfactualize` or `unified-meditation-protocols` if architectural
2. **Load** `/gapanalysis` if pre-implementation thinking
3. **Load** `cross-domain-transfer` if pattern recognition needed
4. **Load** `performance-assessment` if evaluating progress
5. **Consult** skill-activation for domain-specific deep skills

### Memory Confidence Protocol

When uncertain about past interactions:

```
"I believe we discussed X..." → Admit uncertainty, offer to search
"We definitely did Y..." → Only if verifiable in current context
"I don't have memory of..." → Be honest about session boundaries
```

## Self-Correction Protocol

Before suggesting a multi-step manual process:

1. **STOP** — Check this prompt index
2. **MATCH** — Does a prompt already cover this workflow?
3. **LOAD** — If yes, load the prompt and follow it
4. **FLAG** — If no and this is the 3rd time, flag as candidate

## Integration with Skill Selection Optimization

During SSO Phase 1b (Context Survey), also scan this index for:
- Matching session-type prompts
- Workflow prompts that reduce cognitive load
- Consolidation prompts for session end

---

*Episodic memory requires retrieval cues. This skill provides them.*
