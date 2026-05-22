---
document_name: "agent-creation.skill.md"
location: ".claude/skills/agent-creation.skill.md"
codebook_id: "CB-SKILL-AGENTCREATE-001"
version: "1.0.0"
date_created: "2026-01-03"
date_last_edited: "2026-01-03"
document_type: "skill"
purpose: "Procedural guide for creating new agents from templates when project complexity requires delegation"
category: "skills"
subcategory: "orchestration"
skill_metadata:
  category: "orchestration"
  complexity: "intermediate"
  estimated_time: "15-30 minutes"
  prerequisites:
    - "Head Cook role"
    - "Project complexity assessment"
related_docs:
  - "agentdocs/_agent-index.md"
  - "agentdocs/templates/"
maintainers:
  - "head-cook"
status: "active"
tags:
  - "skill"
  - "agents"
  - "orchestration"
  - "delegation"
ai_parser_instructions: |
  This skill is for creating new agents.
  Only Head Cook should use this skill.
  Section markers: === SECTION ===
  Procedure markers: <!-- PROCEDURE:name:START/END -->
---

# Agent Creation Skill

[!FIXED!]
## Purpose

This skill provides procedures for creating new agents when project complexity requires delegation. Agents should be created on-demand, not preemptively.

**When to use:**
- Task complexity exceeds single-agent capacity
- Specialized expertise is needed
- Parallel work would be beneficial
- Recurring tasks would benefit from dedicated agent

**When NOT to use:**
- Simple tasks Head Cook can handle
- One-off tasks
- Early project phases (keep simple)
[!FIXED!]

---

=== PREREQUISITES ===
<!-- AI:PREREQUISITES:START -->

Before using this skill:

- [ ] You are Head Cook (only Head Cook creates agents)
- [ ] Assessed that complexity warrants new agent
- [ ] Identified appropriate template
- [ ] Buildlog is current

<!-- AI:PREREQUISITES:END -->

---

=== PROCEDURE: ASSESS NEED ===
<!-- PROCEDURE:assess-need:START -->

### Questions to Ask

1. **Is this task recurring?**
   - One-off → Handle directly
   - Recurring → Consider agent

2. **Does this require specialized expertise?**
   - Coding focus → Code Chef
   - Review focus → Review Chef
   - Documentation focus → Doc Chef
   - General → Handle directly

3. **Would parallel work help?**
   - Sequential is fine → Handle directly
   - Parallel beneficial → Consider agent

4. **Is current workload sustainable?**
   - Manageable → Handle directly
   - Overwhelming → Create agent(s)

### Decision Matrix

| Recurring | Specialized | Parallel | Overwhelming | Action |
|-----------|-------------|----------|--------------|--------|
| No | No | No | No | Handle directly |
| Yes | Any | Any | Any | Create agent |
| Any | Yes | Any | Any | Create agent |
| Any | Any | Yes | Any | Create agent |
| Any | Any | Any | Yes | Create agent(s) |

<!-- PROCEDURE:assess-need:END -->

---

=== PROCEDURE: SELECT TEMPLATE ===
<!-- PROCEDURE:select-template:START -->

### Available Templates

| Template | Use For |
|----------|---------|
| `agent.template.md` | Custom/new agent types |
| `code-chef.template.md` | Dedicated coding agent |
| `review-chef.template.md` | Code review specialist |
| `doc-chef.template.md` | Documentation specialist |

### Template Selection

1. **For coding tasks**
   - Use `code-chef.template.md`
   - Customize for specific tech stack

2. **For review tasks**
   - Use `review-chef.template.md`
   - Customize review criteria

3. **For documentation tasks**
   - Use `doc-chef.template.md`
   - Customize for project docs

4. **For other specialized tasks**
   - Use `agent.template.md`
   - Define role from scratch

<!-- PROCEDURE:select-template:END -->

---

=== PROCEDURE: CREATE AGENT ===
<!-- PROCEDURE:create-agent:START -->

### Step 1: Copy Template

```bash
# Copy appropriate template
cp agentdocs/templates/code-chef.template.md agentdocs/code-chef.agent.md
```

### Step 2: Customize Preamble

Update YAML preamble:

```yaml
---
document_name: "code-chef.agent.md"
location: "agentdocs/code-chef.agent.md"
codebook_id: "CB-AGENT-CODE-001"  # Assign unique ID
date_created: "YYYY-MM-DD"         # Today's date
date_last_edited: "YYYY-MM-DD"     # Today's date
# ... rest of preamble
---
```

### Step 3: Customize Content

Replace all `<< placeholder >>` values:

1. **Responsibilities**
   - Customize for project needs
   - Add project-specific duties
   - Remove irrelevant items

2. **Capabilities**
   - Map to available skills
   - Add project-specific skills
   - Specify proficiency levels

3. **Boundaries**
   - Define what agent DOES
   - Define what agent DOES NOT
   - Specify escalation paths

4. **Handoff Protocols**
   - Define inputs from Head Cook
   - Define outputs to Head Cook
   - Define interactions with other agents

### Step 4: Register Agent

Update `agentdocs/_agent-index.md`:

```markdown
=== REGISTERED AGENTS ===

| Codebook ID | Agent Name | File | Role | Status |
|-------------|------------|------|------|--------|
| CB-AGENT-HEAD-001 | Head Cook | head-cook.agent.md | Orchestrator | active |
| CB-AGENT-CODE-001 | Code Chef | code-chef.agent.md | Coding | active |  <!-- NEW -->
```

### Step 5: Log Creation

Add buildlog entry:

```markdown
| HH:MM | #micro-decision | Created Code Chef agent for dedicated coding tasks | CB-AGENT-CODE-001 |
```

### Step 6: Verify

- [ ] Agent file has complete preamble
- [ ] All placeholders replaced
- [ ] Codebook ID is unique
- [ ] Registered in index
- [ ] Referenced skills exist
- [ ] Handoff protocols are clear

<!-- PROCEDURE:create-agent:END -->

---

=== PROCEDURE: RETIRE AGENT ===
<!-- PROCEDURE:retire-agent:START -->

When an agent is no longer needed:

### Step 1: Assess

- Is agent still being used?
- Would other agents cover this role?
- Is project complexity decreasing?

### Step 2: Mark Deprecated

Update agent's preamble:

```yaml
status: "deprecated"
```

### Step 3: Update Index

In `_agent-index.md`, change status:

```markdown
| CB-AGENT-XXX-001 | Agent Name | file.md | Role | deprecated |
```

### Step 4: Archive (Optional)

Move to `agentdocs/archive/` if keeping for reference.

### Step 5: Log

```markdown
| HH:MM | #micro-decision | Retired Agent Name - no longer needed | CB-AGENT-XXX-001 |
```

<!-- PROCEDURE:retire-agent:END -->

---

=== CODEBOOK ID ASSIGNMENT ===
<!-- AI:CODEBOOK-ID:START -->

### Format

```
CB-AGENT-{NAME}-{SEQUENCE}

Examples:
- CB-AGENT-HEAD-001    : Head Cook
- CB-AGENT-CODE-001    : Code Chef
- CB-AGENT-REVIEW-001  : Review Chef
- CB-AGENT-DOC-001     : Doc Chef
- CB-AGENT-TEST-001    : Test Chef
- CB-AGENT-CUSTOM-001  : Custom agent
```

### Rules

1. Use descriptive NAME (CODE, REVIEW, DOC, etc.)
2. Start SEQUENCE at 001
3. Never reuse a retired agent's ID
4. Document in both agent file and index

<!-- AI:CODEBOOK-ID:END -->

---

=== COMMON ISSUES ===
<!-- AI:ISSUES:START -->

### Too Many Agents
**Issue:** Created agents prematurely, now overwhelming
**Fix:** Retire unused agents; consolidate similar roles

### Missing Skills
**Issue:** Agent references skills that don't exist
**Fix:** Create required skills first, or adjust agent capabilities

### Unclear Boundaries
**Issue:** Agents stepping on each other's responsibilities
**Fix:** Review and clarify boundaries; update both agents

### Orphaned Agents
**Issue:** Agent exists but is never used
**Fix:** Either integrate into workflow or retire

<!-- AI:ISSUES:END -->

---

=== RELATED DOCUMENTS ===
<!-- AI:RELATED:START -->

| Document | Codebook ID | Relationship |
|----------|-------------|--------------|
| _agent-index.md | CB-AGENT-INDEX | Registration |
| head-cook.agent.md | CB-AGENT-HEAD-001 | Only user of this skill |
| templates/*.md | - | Source templates |

<!-- AI:RELATED:END -->
