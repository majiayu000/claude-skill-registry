---
name: plugin-ideation
description: 'Adaptive brainstorming for plugin concepts and improvements when exploring
  ideas, not implementing. Autonomous triggers: "I want to make...", "Explore improvements
  to...", "brainstorm", "ideate", "new'
---

---
name: plugin-ideation
description: Adaptive brainstorming for plugin concepts and improvements when exploring ideas, not implementing. Autonomous triggers: "I want to make...", "Explore improvements to...", "brainstorm", "ideate", "new plugin idea", "what if I added". NOT for implementing existing improvement proposals (use plugin-improve skill).
allowed-tools:
  - Read
  - Write
  - Bash
preconditions:
  - None (entry point)
---

# plugin-ideation Skill

**Purpose:** Interactive brainstorming and creative vision capture for new plugins and improvements to existing plugins.

This skill uses mode-based workflow loading to optimize context window usage. After detecting which mode applies (New Plugin vs Improvement), the appropriate workflow reference is loaded on-demand.

## Mode Detection

<critical_sequence>
<sequence_name>mode_detection</sequence_name>
<enforcement>must_complete_before_proceeding</enforcement>

<step number="1" required="true">
**Check if plugin exists:**

```bash
grep "^### $PLUGIN_NAME$" PLUGINS.md
```

**Route based on result:**
- If found → Load Improvement Mode workflow
- If not found → Load New Plugin Mode workflow
</step>
</critical_sequence>

---

## Workflow References

After mode detection completes, load the appropriate workflow:

### New Plugin Mode

**When to use:** Plugin does not exist in PLUGINS.md (new plugin ideation)

**Workflow:** See [new-plugin-workflow.md](references/new-plugin-workflow.md)

**Overview:** 8-phase workflow from free-form collection through creative brief creation
- Phase 1: Free-form collection
- Phase 2: Gap analysis (4-tier priority system)
- Phase 3: Question batch generation (adaptive 4-question batches)
- Phase 4: Decision gate (finalize or iterate)
- Phase 5: Plugin name validation
- Phase 6: Document creation (creative-brief.md + PLUGINS.md)
- Phase 7: Session handoff (.continue-here.md)
- Phase 8: Decision menu with parallel workflow option

**Key features:**
- Adaptive questioning based on tier-based gap analysis
- Context accumulation across question batches
- Parallel workflow path (Phase 8.1) for faster iteration
- Continuous iteration support until user says "finalize"

### Improvement Mode

**When to use:** Plugin exists in PLUGINS.md (improvement brainstorming)

**Workflow:** See [improvement-workflow.md](references/improvement-workflow.md)

**Overview:** 7-phase workflow from vagueness detection through improvement proposal creation
- Phase 0: Vagueness detection (brainstorm vs implement routing)
- Phase 1: Free-form collection
- Phase 2: Gap analysis (3-tier priority system)
- Phase 3: Question batch generation
- Phase 4: Decision gate (finalize or iterate)
- Phase 5: Document creation (improvement proposal)
- Phase 6: Session handoff (.continue-here.md)
- Phase 7: Decision menu

**Key features:**
- Vagueness detection to route between ideation and implementation
- 3-tier gap analysis specific to improvements
- Version impact tracking (PATCH/MINOR/MAJOR)
- Backward compatibility consideration

---

## Mode-Based Loading Instructions

1. **Complete mode detection first** (check PLUGINS.md)
2. **Load appropriate workflow reference:**
   - New Plugin: Read [references/new-plugin-workflow.md](references/new-plugin-workflow.md)
   - Improvement: Read [references/improvement-workflow.md](references/improvement-workflow.md)
3. **Execute loaded workflow** following all phase instructions
4. **Follow checkpoint protocol** at decision gates

This structure reduces initial context load by ~50% (from 8k to 4k tokens) while preserving full functionality through on-demand reference loading.
