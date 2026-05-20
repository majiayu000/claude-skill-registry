---
name: update-people
description: Update People doc based on code attribution, reflection learnings, and role changes.
---

# Update People

Extract people-related insights from card reflections, code analysis, and team observations to update the People document. Keeps team structure, roles, and capability tracking aligned with reality.

## Operating Mode

**READ + WRITE (PEOPLE DOC ONLY)**

**Allowed:**
- Read card reflection stage docs
- Analyze code ownership patterns (git blame, commit history)
- Update people doc (`docs/business-os/people/people.user.md` and `.agent.md`)
- Commit people doc updates with agent identity

**Not allowed:**
- Modifying cards, ideas, or business plans
- Creating new people entries without Pete approval
- Changing role assignments (Pete does this)

## Inputs

**Required:**
- Update source: `reflection` (from card), `code-analysis` (git attribution), or `manual` (Pete-provided)

**Optional:**
- Card ID: If updating from specific card reflection
- Person name: If updating specific person's entry

## People Doc Structure

People doc located at: `docs/business-os/people/people.user.md` and `people.agent.md`

### Sections

1. **Roles** (Who does what)
   - Person name
   - Primary role (Developer, Designer, Product, Operations, etc.)
   - Business affiliations
   - Ownership areas

2. **Responsibilities** (Detailed duties)
   - Current projects/cards owned
   - Domain expertise areas
   - Ongoing maintenance duties

3. **Capabilities** (Current skills)
   - Technical skills (languages, frameworks, tools)
   - Domain knowledge (payments, auth, SEO, etc.)
   - Process skills (planning, fact-finding, reflection)

4. **Gaps** (Identified needs)
   - Skill gaps blocking work
   - Knowledge gaps discovered during execution
   - Resource needs (time, tools, training)

5. **Availability** (Capacity tracking)
   - Current workload (cards in progress)
   - Upcoming availability
   - Leave/vacation plans

## Workflow

### 1. Identify Update Source

**From Card Reflection:**
```typescript
const reader = createRepoReader(repoRoot);
const reflectDoc = await reader.getStageDoc(cardId, "reflect");

// Extract from reflect.agent.md:
// - New skills learned
// - Knowledge gaps discovered
// - Responsibility changes
// - Ownership updates
```

**From Code Analysis:**
```bash
# Analyze code ownership patterns
git log --format="%an" --since="30 days ago" -- apps/brikette/ | sort | uniq -c | sort -nr

# Identify primary contributors by module
git blame apps/brikette/src/components/guides/ | awk '{print $2}' | sort | uniq -c
```

**From Manual Input:**
```typescript
// Pete provides:
// - Role change
// - New team member
// - Skill gap identified
// - Responsibility transfer
```

### 2. Extract People-Related Changes

**New Capabilities:**
- Skills learned during card execution
- Domain knowledge gained
- Tools/technologies mastered

Example from reflection:
```markdown
## Learnings: Technical

Pete learned:
- Next.js 15 App Router patterns (server components, route handlers)
- Zod schema validation with react-hook-form
- simple-git library for git automation
```

**Skill Gaps:**
- Blockers caused by missing knowledge
- Areas where external help needed
- Training needs identified

Example from reflection:
```markdown
## Gaps Identified

- GDPR compliance knowledge (required legal review)
- Platform auth internals (spike needed to understand integration)
- Performance profiling tools (baseline measurements took longer than expected)
```

**Responsibility Changes:**
- New ownership areas
- Cards transferred
- Domain expertise shifts

Example from code analysis:
```bash
Pete: 127 commits in apps/business-os/ (primary owner)
Pete: 45 commits in docs/business-os/ (documentation)
```

**Availability Updates:**
- Workload changes (cards completed/added)
- Vacation plans
- Capacity constraints

### 3. Read Current People Doc

```typescript
const peoplePath = "docs/business-os/people/people.user.md";
const currentPeople = matter(await fs.readFile(peoplePath, "utf-8"));
```

### 4. Draft People Doc Updates

**Roles Section:**
```markdown
## Roles

### Pete

**Primary Role:** Full-Stack Developer, Product Owner

**Business Affiliations:**
- BRIK (Brikette): Primary owner
- SKYL (Skyline): Contributing developer
- PLAT (Platform): Core infrastructure

**Ownership Areas:**
- Business OS (apps/business-os) - primary
- Brikette guides system (apps/brikette/src/components/guides) - primary
- Platform core (packages/platform-core) - contributing
```

**Responsibilities Section:**
```markdown
## Responsibilities

### Pete

**Current Projects:**
- Business OS Phase 0 MVP (PLAT-OPP-0001) - In progress
  - Cards: BOS-01 through BOS-32
  - Status: 14/32 complete (as of 2026-01-28)

**Domain Expertise:**
- Next.js / React architecture
- TypeScript type system design
- Git workflow automation
- Business process modeling

**Ongoing Maintenance:**
- Brikette guides system (bug fixes, content updates)
- Platform auth (minor updates)
- Design system (token updates)
```

**Capabilities Section:**
```markdown
## Capabilities

### Pete

**Technical Skills:**
- **Languages:** TypeScript, JavaScript, SQL, Bash
- **Frameworks:** Next.js 15, React 19, Prisma
- **Tools:** Git, simple-git, Zod, react-hook-form
- **Testing:** Jest, Cypress, React Testing Library

**Domain Knowledge:**
- Next.js App Router patterns (learned: 2026-01-28)
- Git automation with simple-git (learned: 2026-01-28)
- Business OS kanban workflows (learned: 2026-01-27)
- Dual-audience documentation (learned: 2026-01-26)

**Process Skills:**
- Fact-finding (evidence-based discovery)
- Planning (confidence-gated task breakdown)
- Reflection (learnings extraction)
```

**Gaps Section:**
```markdown
## Gaps

### Pete

**Knowledge Gaps (Updated 2026-01-28):**
- GDPR compliance for user data (blocked BRIK-ENG-0001)
  - Impact: Legal review required, 1-2 week delay
  - Mitigation: Engage legal team early in fact-finding

- Platform auth internals (discovered during fact-finding)
  - Impact: Integration spike needed, added 2 days to timeline
  - Mitigation: Study platform-core/src/auth/ before planning

- Performance profiling tools (discovered during BRIK-ENG-0005)
  - Impact: Baseline measurements took longer than expected
  - Mitigation: Learn Lighthouse CI, RUM setup

**Resource Gaps:**
- Time: Current workload at 100% (5 active cards)
- Recommendation: Defer new P3+ cards until current work completes
```

**Availability Section:**
```markdown
## Availability

### Pete

**Current Workload (2026-01-28):**
- In Progress: 3 cards (BOS-15, BOS-16, BOS-17)
- Planned: 2 cards (BOS-19, BOS-20)
- Capacity: At limit (100%)

**Upcoming Availability:**
- Next 2 weeks: Fully committed to Business OS Phase 0
- After Phase 0: Available for new BRIK features

**Leave Plans:**
- None scheduled
```

### 5. Merge Updates into People Doc

**Rules:**
- **Roles:** Update only if role formally changes (rare)
- **Responsibilities:** Update current projects list
- **Capabilities:** Add newly learned skills, update domain knowledge
- **Gaps:** Add new gaps, archive resolved gaps
- **Availability:** Update workload and capacity regularly

**Dual-audience mirroring:**
- `.user.md`: Narrative, human-readable format
- `.agent.md`: Structured, with evidence links and code ownership stats

### 6. Commit Changes

```typescript
const writer = createRepoWriter(repoRoot);

await writer.updateFile(
  "docs/business-os/people/people.user.md",
  updatedUserContent,
  CommitIdentities.agent
);

await writer.updateFile(
  "docs/business-os/people/people.agent.md",
  updatedAgentContent,
  CommitIdentities.agent
);
```

Commit message:
```
Update people doc: Pete's capabilities and gaps (from BRIK-ENG-0001)

- Capabilities: Added Next.js App Router, simple-git automation
- Gaps: GDPR compliance, platform auth internals, perf profiling
- Availability: At capacity (3 in progress, 2 planned)

Source: Card BRIK-ENG-0001 reflection
```

## Evidence Requirements

Every people doc update must include:

- **Source:** Card ID, code analysis period, or manual observation
- **Evidence type:** repo-diff (code ownership), reflection (learnings), measurement (workload)
- **Date:** When change occurred or evidence gathered

## Integration with Other Skills

- **After `/work-idea`:** Update responsibilities (new card ownership)
- **After reflection:** Update capabilities (skills learned) and gaps (discovered needs)
- **After `/scan-repo`:** Update availability (workload changes from scan)
- **After `/ideas-go-faster`:** Sweep reads profiles and flags capacity gaps — use this skill to act on sweep recommendations for profile bootstrapping or updates
- **Monthly review:** Run code analysis to update ownership and contributions

## Example Session

```
User: /update-people --card BRIK-ENG-0001

Agent:
Updating people doc from card BRIK-ENG-0001 reflection...

[Reading reflection stage doc]
Card: BRIK-ENG-0001 (User Authentication)
Owner: Pete
Lane: Reflected
Completed: 2026-01-28

[Extracting people-related changes]
✓ Capabilities learned:
  - Next.js App Router patterns (server components)
  - Zod + react-hook-form integration
  - simple-git library usage

✓ Gaps discovered:
  - GDPR compliance (legal review needed)
  - Platform auth internals (spike required)
  - Performance profiling tools

✓ Workload:
  - Card completed: BRIK-ENG-0001
  - Current in progress: 2 cards (BOS-15, BOS-16)

[Reading current people doc]
File: docs/business-os/people/people.user.md
Last updated: 2026-01-20

[Drafting updates for Pete's entry]
Capabilities section:
  + Next.js App Router patterns (2026-01-28)
  + Git automation with simple-git (2026-01-28)

Gaps section:
  + GDPR compliance knowledge (blocked BRIK-ENG-0001)
  + Platform auth internals (spike needed)
  + Performance profiling tools

Availability section:
  ~ Current workload: 3 → 2 cards in progress (completed BRIK-ENG-0001)

[Merging into people.user.md and people.agent.md]
✓ Capabilities updated (2 new skills)
✓ Gaps added (3 new)
✓ Availability updated

[Committing changes]
✓ Commit: Update people doc (Pete's capabilities + gaps)
✓ Agent identity used

Done! People doc updated. Pete can review diff:
  git show HEAD -- docs/business-os/people/people.user.md
```

## Code Analysis Examples

**Ownership by module:**
```bash
# Who owns apps/business-os/?
git log --format="%an" --since="30 days ago" -- apps/business-os/ | sort | uniq -c
# Output: 127 Pete

# Who owns apps/brikette/src/components/guides/?
git log --format="%an" --since="90 days ago" -- apps/brikette/src/components/guides/ | sort | uniq -c
# Output: 45 Pete, 12 Other-Contributor
```

**Contribution patterns:**
```bash
# Pete's recent focus areas (top 5 directories by commit count)
git log --author="Pete" --since="30 days ago" --format="" --name-only | grep "/" | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -5
# Output:
# 127 apps/business-os/src
#  45 docs/business-os
#  23 apps/brikette/src/components/guides
#  15 packages/platform-core/src
#  12 docs/plans
```

## Frequency Recommendations

- **After card reflection:** Update capabilities and gaps (every completed card)
- **Monthly code analysis:** Update ownership and contribution patterns
- **Role changes:** Immediate update (ad-hoc, Pete-triggered)
- **Quarterly review:** Comprehensive audit of all people entries

## Error Handling

- **People doc not found:** Create from template (ask Pete first)
- **Person not in doc:** Ask Pete before adding new person
- **Conflicting updates:** Pete resolves manually (e.g., simultaneous cards)
- **No meaningful updates:** Skip commit, report "no changes"

## Phase 0 Constraints

- Pete-only in Phase 0 (single person, simple updates)
- Agent identity for all people doc commits
- Pete reviews all people changes
- Manual trigger only (no automated updates)

## Success Metrics

- Update frequency: Within 1 week of card completion
- Capability tracking: ≥80% of new skills captured from reflections
- Gap visibility: All blockers documented in gaps section
- Accuracy: People doc reflects current team state (validated monthly)
