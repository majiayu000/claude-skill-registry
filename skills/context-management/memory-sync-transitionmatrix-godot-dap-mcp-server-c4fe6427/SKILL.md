---
name: memory-sync
description: Guided workflow for maintaining strategic redundancy between Serena memories and project documentation. Use after significant code changes, phase completions, or when new architectural patterns are discovered.
---

# Memory Sync: Maintaining Strategic Redundancy

## Overview

This skill helps maintain the "strategic redundancy" pattern between Serena memories (optimized for code navigation) and documentation (optimized for human comprehension). Use this skill after significant changes to ensure both remain accurate and useful.

**Key Principle**: Memories are concise, token-efficient summaries for immediate context; docs are comprehensive references for deep understanding.

---

# Process

## 🔍 Phase 1: Assess What Changed

### 1.1 Review Recent Changes

First, understand what has changed since the last sync:

```bash
# Check recent commits
git log --oneline -10

# Check uncommitted changes
git status
git diff

# Check what files were modified
git diff --name-only HEAD~5..HEAD
```

### 1.2 Identify Change Categories

Categorize the changes:

**Architecture Changes** → Affect `project_overview.md`, `codebase_structure.md`, `critical_implementation_patterns.md`
- New layers or components added
- Protocol flow changes
- Session management patterns
- Critical implementation patterns discovered

**Convention Changes** → Affect `code_style_and_conventions.md`
- New naming patterns
- Error message format changes
- Commit message conventions
- Code organization rules

**Workflow Changes** → Affect `suggested_commands.md`, `task_completion_checklist.md`
- New build commands
- Testing procedure updates
- Dependency management changes
- New development tools

**Status Changes** → Affect `project_overview.md`
- Phase completions
- Milestone achievements
- New features complete

**Technology Changes** → Affect `tech_stack.md`
- New dependencies
- Version upgrades
- Platform support changes

---

## 📝 Phase 2: Update Memories

For each affected memory, follow this process:

### 2.1 Read Current Memory

```bash
# Use Serena to read the memory
read_memory(memory_file_name="<memory_name>")
```

### 2.2 Compare with Current Code

Use Serena's symbolic tools to verify accuracy:

```bash
# Example: Check if codebase_structure matches reality
list_dir(relative_path="internal", recursive=true)
get_symbols_overview(relative_path="internal/dap/client.go")

# Example: Verify critical patterns still apply
find_symbol(name_path="Client/waitForResponse", include_body=true)
```

### 2.3 Update Memory (Token-Efficient)

**Guidelines for memory updates:**
- Keep concise (1-2 pages max)
- Focus on "what you need to know NOW"
- Use bullet points and code snippets
- Remove outdated information
- Add new critical patterns

```bash
# Update the memory
write_memory(
  memory_name="<memory_name>",
  content="<updated_content>"
)
```

### 2.4 Memory-Specific Update Patterns

**project_overview.md**:
- Update implementation status
- Add new architectural insights
- Update phase completion status
- Revise key capabilities if changed

**critical_implementation_patterns.md**:
- Add newly discovered patterns
- Update code examples if APIs changed
- Mark deprecated patterns
- Highlight gotchas from recent debugging

**code_style_and_conventions.md**:
- Add new naming conventions
- Update error message examples
- Revise file organization rules
- Add new commit types if introduced

**suggested_commands.md**:
- Add new build/test commands
- Update command sequences
- Add new dependency management steps
- Revise platform-specific commands

**codebase_structure.md**:
- Update directory tree if structure changed
- Revise layer descriptions
- Update file counts and key files
- Add new packages or modules

**tech_stack.md**:
- Update dependency versions
- Add new dependencies
- Update build system changes
- Revise platform support

**task_completion_checklist.md**:
- Add new quality checks
- Update test commands
- Revise documentation requirements
- Add new special considerations

---

## 📚 Phase 3: Flag Documentation Updates

After updating memories, identify which docs need comprehensive updates:

### 3.1 Check Documentation Impact

**For architecture changes:**
- [ ] `docs/ARCHITECTURE.md` - Update design patterns
- [ ] `docs/IMPLEMENTATION_GUIDE.md` - Update component specs
- [ ] `docs/reference/GODOT_SOURCE_ANALYSIS.md` - Add findings

**For convention changes:**
- [ ] `docs/reference/CONVENTIONS.md` - Update coding standards
- [ ] `CLAUDE.md` - Update quick reference

**For workflow changes:**
- [ ] `docs/TESTING.md` - Update test procedures
- [ ] `docs/DEPLOYMENT.md` - Update build/deploy steps
- [ ] `CLAUDE.md` - Update development commands

**For status changes:**
- [ ] `docs/PLAN.md` - Update phase status and timeline
- [ ] `README.md` - Update project status

### 3.2 Update Documentation

For each flagged document:

1. **Read the current doc**
2. **Identify sections that need updates**
3. **Update with comprehensive details** (unlike memories, docs should be thorough)
4. **Add examples and rationale** (explain WHY, not just WHAT)
5. **Maintain existing structure and formatting**

**Key Difference from Memories:**
- Docs explain the reasoning and trade-offs
- Docs provide extensive examples
- Docs are stable references, not quick summaries

---

## ✅ Phase 4: Verify Sync Completeness

### 4.1 Cross-Check Critical Information

Verify that critical information appears in both places (with appropriate detail level):

**Pattern**: Check that each critical pattern exists in:
- Memory (concise, code snippet)
- Doc (comprehensive, with rationale)

Example checks:

```bash
# Check event filtering pattern
grep -r "event filtering" .serena/memories/
grep -r "event filtering" docs/

# Check timeout protection pattern
grep -r "timeout" .serena/memories/
grep -r "timeout" docs/
```

### 4.2 Validate Memory Size

Ensure memories remain token-efficient:

```bash
# Check memory sizes (should be under ~2000 tokens each)
wc -w .serena/memories/*.md

# If any memory is too large, condense it
```

### 4.3 Document the Sync

Add a note about what was synced:

```bash
# In git commit message
git commit -m "docs: sync memories with Phase X completion

Updated memories:
- project_overview.md (phase status)
- critical_implementation_patterns.md (new timeout pattern)

Updated docs:
- ARCHITECTURE.md (event filtering section)
- PLAN.md (Phase X marked complete)"
```

---

## 🎯 Quick Reference: Update Triggers

**Must sync immediately:**
- ✅ Phase completion
- ✅ New critical pattern discovered (e.g., event filtering, timeout requirement)
- ✅ Architecture layer added/removed
- ✅ Major refactoring (5+ files changed)

**Should sync soon:**
- New tool naming convention
- Error message pattern change
- New development command
- Directory structure change

**No sync needed:**
- Bug fixes in existing code
- Test additions without new patterns
- Minor documentation typos
- Comment improvements

---

## 📋 Checklist Template

Use this checklist each time you run memory-sync:

```
Memory Sync Checklist - [Date]

Changes Assessed:
- [ ] Reviewed git log for recent changes
- [ ] Identified change categories
- [ ] Determined affected memories and docs

Memories Updated:
- [ ] project_overview.md (if status/architecture changed)
- [ ] critical_implementation_patterns.md (if new patterns)
- [ ] code_style_and_conventions.md (if conventions changed)
- [ ] suggested_commands.md (if workflow changed)
- [ ] codebase_structure.md (if structure changed)
- [ ] tech_stack.md (if dependencies changed)
- [ ] task_completion_checklist.md (if process changed)

Documentation Flagged:
- [ ] ARCHITECTURE.md (architecture changes)
- [ ] CONVENTIONS.md (convention changes)
- [ ] TESTING.md (test procedure changes)
- [ ] PLAN.md (status updates)
- [ ] CLAUDE.md (quick reference updates)
- [ ] Other: _______________

Verification:
- [ ] Cross-checked critical patterns exist in both places
- [ ] Verified memory sizes remain token-efficient
- [ ] Documented sync in git commit message

Notes:
[Add any observations or decisions made during sync]
```

---

## 💡 Tips for Effective Memory Sync

**Keep Memories Lean:**
- If a memory grows beyond 2 pages, split it or condense
- Remove outdated information immediately
- Focus on "what changed recently" not "complete history"

**Use Code Examples Wisely:**
- Memories: Small, focused snippets (5-10 lines)
- Docs: Complete, annotated examples (20+ lines)

**Maintain Single Source of Truth:**
- Docs are authoritative for "how things should work"
- Memories reflect "how things actually work now"
- When they diverge, it signals needed doc updates

**Leverage Serena Tools:**
- Use symbolic search to verify code matches memories
- Use `find_referencing_symbols` to check pattern usage
- Use `search_for_pattern` to find all instances

**Version Control Your Memories:**
- Commit memory changes with descriptive messages
- Review memory diffs before committing
- Document why memories were updated
