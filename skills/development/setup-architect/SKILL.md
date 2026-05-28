---
name: setup-architect
description: Sets up and installs the AI Software Architect framework in a NEW project for the FIRST time. Use when the user requests "Setup .architecture", "Setup ai-software-architect", "Initialize architecture framework", "Install software architect", or similar setup/installation phrases. Do NOT use for checking status (use architecture-status), creating documents (use create-adr or reviews), or when framework is already set up.
allowed-tools: Read,Write,Edit,Glob,Grep,Bash
---

# Setup AI Software Architect Framework

Sets up and customizes the AI Software Architect framework for a project.

## Overview

This skill performs a complete framework installation:
1. Verifies prerequisites (framework cloned, project root confirmed)
2. Analyzes project (languages, frameworks, structure, patterns)
3. Installs framework files and directory structure
4. Customizes team members and principles for detected tech stack
5. Performs initial system analysis
6. Reports customizations and findings

**Detailed procedures**: [references/installation-procedures.md](references/installation-procedures.md)
**Customization guide**: [references/customization-guide.md](references/customization-guide.md)

## High-Level Workflow

### 1. Verify Prerequisites

Check requirements before installation:
- `.architecture/.architecture/` directory exists (cloned framework)
- Currently in project root directory

**If missing**: Guide user to clone framework first.

### 2. Analyze Project

Identify project characteristics:
- **Languages**: JavaScript/TypeScript, Python, Ruby, Java, Go, Rust
- **Frameworks**: React, Vue, Django, Rails, Spring, etc.
- **Infrastructure**: Testing setup, CI/CD, package managers
- **Structure**: Directory layout, architectural patterns

Use `Glob` and `Grep` to detect technologies, `Read` to examine configs.

### 3. Install Framework

Execute installation steps (see [references/installation-procedures.md](references/installation-procedures.md)):
- Copy framework files to `.architecture/`
- Remove clone directory
- Create directory structure (decisions/adrs, reviews, recalibration, etc.)
- Initialize configuration from templates
- Set up agent documentation (ADR-006 progressive disclosure)

**Critical**: Follow safety procedures when removing `.git/` directory.

### 4. Customize Architecture Team

Add technology-specific members to `.architecture/members.yml`:
- **JavaScript/TypeScript**: JavaScript Expert, framework specialists (React/Vue/Angular)
- **Python**: Python Expert, framework specialists (Django/Flask/FastAPI)
- **Ruby**: Ruby Expert, Rails Architect
- **Java**: Java Expert, Spring Boot Specialist
- **Go**: Go Expert, Microservices Architect
- **Rust**: Rust Expert, Systems Programmer

Use template from [assets/member-template.yml](assets/member-template.yml).

**Keep core members**: Systems Architect, Domain Expert, Security, Performance, Maintainability, AI Engineer, Pragmatic Enforcer.

**Customization details**: [references/customization-guide.md § Customize Team Members](references/customization-guide.md#customize-architecture-team-members)

### 5. Customize Architectural Principles

Add framework-specific principles to `.architecture/principles.md`:
- **React**: Component composition, hooks, unidirectional data flow
- **Rails**: Convention over configuration, DRY, RESTful design
- **Django**: Explicit over implicit, reusable apps, use built-ins

**Principle examples**: [references/customization-guide.md § Customize Principles](references/customization-guide.md#customize-architectural-principles)

### 6. Update CLAUDE.md Integration

If `CLAUDE.md` exists in project root, append framework usage section:
- Available commands
- Where to find documentation
- How to invoke skills

**Template**: [references/customization-guide.md § Update CLAUDE.md](references/customization-guide.md#update-claudemd-integration)

### 7. Cleanup

Remove framework development files:
- Framework documentation (README.md, USAGE*.md, INSTALL.md)
- Template `.git/` directory (with **critical safety checks**)

**⚠️  IMPORTANT**: Follow all safeguards in [references/installation-procedures.md § Cleanup](references/installation-procedures.md#cleanup-procedures).

### 8. Create Initial System Analysis

Generate comprehensive initial analysis document:
- Each member analyzes system from their perspective
- System overview (stack, structure, patterns)
- Strengths identified
- Concerns raised (with impact levels)
- Recommendations prioritized (Critical/Important/Nice-to-Have)
- Collaborative synthesis of findings

Save to `.architecture/reviews/initial-system-analysis.md`.

**Template**: [assets/initial-analysis-template.md](assets/initial-analysis-template.md)

### 9. Report to User

Provide setup summary:

```
AI Software Architect Framework Setup Complete

Customizations:
- Added [N] technology specialists: [list]
- Customized principles for: [frameworks]
- Configuration: Pragmatic mode [enabled/disabled]

Initial Analysis Highlights:
- Overall assessment: [assessment]
- Top strength: [strength]
- Top concern: [concern]
- Critical recommendation: [recommendation]

Location: .architecture/reviews/initial-system-analysis.md

Next Steps:
- Review initial analysis findings
- "List architecture members" to see customized team
- "Create ADR for [first decision]" to start documenting
- "What's our architecture status?" to verify setup
```

## Error Handling

**Framework not cloned**:
```
The framework must be cloned first. Please run:

git clone https://github.com/codenamev/ai-software-architect .architecture/.architecture

Then run setup again.
```

**Already set up**:
```
Framework appears to be already set up.

To verify: "What's our architecture status?"
To reconfigure: Manually edit .architecture/members.yml and .architecture/principles.md
```

**Unclear project structure**:
```
Could not clearly identify project type. Please describe:
- Primary programming language(s)
- Framework(s) used
- Project purpose

I'll customize the framework accordingly.
```

## Related Skills

**After Setup**:
- `list-members` - View customized team
- `architecture-status` - Verify setup completion
- `create-adr` - Document first decision

**Initial Work**:
- Review `initial-system-analysis.md` findings
- `specialist-review` - Deep-dive on specific concerns
- `create-adr` - Document existing key decisions

**Workflow Example**:
Setup → Review initial analysis → Create ADRs → Status check → Regular reviews

## Notes

- Customize based on **actual** project, not every possible option
- Be specific about **why** each customization was made
- Initial analysis should be thorough but focused on actionable findings
- Safety checks during cleanup are **non-negotiable**

## Documentation

- **Installation details**: [references/installation-procedures.md](references/installation-procedures.md)
- **Customization guide**: [references/customization-guide.md](references/customization-guide.md)
- **Initial analysis template**: [assets/initial-analysis-template.md](assets/initial-analysis-template.md)
- **Member template**: [assets/member-template.yml](assets/member-template.yml)
- **Common patterns**: [../_patterns.md](../_patterns.md)
