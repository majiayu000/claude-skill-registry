---
name: Mega Skills Batch Creator
description: Create 10-20 powerful project-specific skills in one session for Leavn iOS app based on common workflows, debugging needs, and development patterns
allowed-tools: Write, Read, Glob
---

# Mega Skills Batch Creator

## Instructions

Create comprehensive skill library for Leavn project:

1. **Analyze project patterns** from:
   - CLAUDE.md (development commands, architecture)
   - Makefile (build commands)
   - Common debugging workflows
   - Frequent tasks from session history

2. **Create skills for**:
   - **Build/Debug**: Error fixing, build optimization, clean builds
   - **Testing**: Feature verification, UI testing, integration tests
   - **Migration**: @Observable, SwiftData, TCA removal
   - **Architecture**: DI setup, service creation, entity creation
   - **Quality**: Localization, accessibility, performance
   - **Workflow**: Commits, documentation, audits

3. **Skill naming convention**:
   - Action-oriented: "swift-binding-fixer" not "bindings"
   - Domain-specific: "leavn-commit-machine" not "git-commit"
   - Clear purpose: What it does + when to use

4. **Each skill must have**:
   - Specific description (when Claude should invoke)
   - Step-by-step instructions
   - Code examples
   - Leavn-specific patterns
   - "Use this skill when" trigger examples

5. **Batch create 20 skills**:
   - 5 build/debug skills
   - 5 migration/architecture skills
   - 5 testing/verification skills
   - 5 workflow/productivity skills

Use this skill when: Setting up new project, need debugging tools, want automation
