---
name: skills
command: /skills
aliases: ["/commands", "/help-skills"]
description: List available skills and their activation methods
tier: focused
model: haiku
---

# Skills Listing Skill

## Usage

```
/skills              - Show all available skills by category
/skills <category>   - Show skills in a specific category
/skills search <term> - Search for skills by name or description
```

## Categories

- **session** - Session management (/resume, /close-phase, /rollback)
- **traceability** - Requirement traceability (/trace)
- **ideation** - Phases 1-2: Ideation and Discovery
- **validation** - Phases 3-4: PRD Validation and Audit
- **tasks** - Phase 5: Task Decomposition
- **spec** - Phase 6: Specification Generation
- **implementation** - Phase 7: TDD Implementation
- **review** - Phase 8: Code Review
- **testing** - Phases 9-10: Integration and E2E Testing
- **deployment** - Phases 11-12: Deployment and Monitoring
- **pipeline** - Pipeline orchestration and monitoring
- **agents** - Agent management and curation

## Behavior

When `/skills` is invoked:

1. **List mode** (no args):
   ```
   ╔═══════════════════════════════════════════════════════════════════════╗
   ║  AVAILABLE SKILLS                                                     ║
   ╠═══════════════════════════════════════════════════════════════════════╣
   ║                                                                        ║
   ║  SLASH COMMANDS (Direct Invocation)                                   ║
   ║  ├── /resume     Resume previous session                              ║
   ║  ├── /close-phase  Seal phase with context externalization            ║
   ║  ├── /rollback   Restore to previous phase                            ║
   ║  ├── /trace      Manage requirement traceability                      ║
   ║  └── /skills     This listing                                         ║
   ║                                                                        ║
   ║  PHASE SKILLS (Auto-Activated)                                        ║
   ║  ├── Phase 1-2: ideation, discovery, web-researcher                   ║
   ║  ├── Phase 3-4: prd-validator, prd-audit                              ║
   ║  ├── Phase 5:   task-decomposer, task-review-gate                     ║
   ║  ├── Phase 6:   spec-gen                                              ║
   ║  ├── Phase 7:   tdd-implementer, mock-detector                        ║
   ║  ├── Phase 8:   code-review-gate                                      ║
   ║  ├── Phase 9-10: integration-validator, e2e-validator                 ║
   ║  └── Phase 11-12: deployment-orchestrator, deployment-rollback        ║
   ║                                                                        ║
   ║  BACKGROUND SKILLS                                                    ║
   ║  └── plan-guardian  Drift detection (runs alongside other agents)     ║
   ║                                                                        ║
   ╠═══════════════════════════════════════════════════════════════════════╣
   ║  Run `/skills <category>` for details. Full catalog: docs/SKILL-CATALOG.md
   ╚═══════════════════════════════════════════════════════════════════════╝
   ```

2. **Category mode** (`/skills session`):
   ```
   ╔═══════════════════════════════════════════════════════════════════════╗
   ║  SESSION MANAGEMENT SKILLS                                            ║
   ╠═══════════════════════════════════════════════════════════════════════╣
   ║                                                                        ║
   ║  /resume [--details] [--rollback]                                     ║
   ║    Aliases: /continue, /status, /where                                ║
   ║    Resume previous session, show current pipeline state               ║
   ║                                                                        ║
   ║  /close-phase                                                         ║
   ║    Aliases: /checkpoint                                               ║
   ║    Seal current phase with complete context externalization           ║
   ║    Creates rollback checkpoint, confirms safe to close terminal       ║
   ║                                                                        ║
   ║  /rollback [<phase>]                                                  ║
   ║    Restore project to previous phase checkpoint                       ║
   ║    Archives (doesn't delete) work from later phases                   ║
   ║                                                                        ║
   ╚═══════════════════════════════════════════════════════════════════════╝
   ```

3. **Search mode** (`/skills search deploy`):
   ```
   ╔═══════════════════════════════════════════════════════════════════════╗
   ║  SEARCH RESULTS: "deploy"                                             ║
   ╠═══════════════════════════════════════════════════════════════════════╣
   ║                                                                        ║
   ║  deployment-orchestrator (Phase 11)                                   ║
   ║    Orchestrates deployment to production                              ║
   ║    Activation: DEPLOYMENT_ORCHESTRATOR_V1                             ║
   ║                                                                        ║
   ║  deployment-rollback (Phase 12)                                       ║
   ║    Rollback production deployment if issues detected                  ║
   ║    Activation: DEPLOYMENT_ROLLBACK_V1                                 ║
   ║                                                                        ║
   ║  infrastructure-validator (Phase 11)                                  ║
   ║    Validates infrastructure readiness before deployment               ║
   ║    Activation: INFRASTRUCTURE_VALIDATOR_V1                            ║
   ║                                                                        ║
   ╚═══════════════════════════════════════════════════════════════════════╝
   ```

## Implementation

1. **Scan skills directory**:
   ```
   Glob: skills/**/*.md, skills/*.SKILL.md
   ```

2. **Extract frontmatter metadata**:
   - name, command, aliases, description
   - activation_code, phase, category

3. **Group by category** based on phase or explicit category

4. **Present formatted output** based on mode (list/category/search)

## Related Files

| File | Purpose |
|------|---------|
| `docs/SKILL-CATALOG.md` | Full skill documentation |
| `skills/*/SKILL.md` | Individual skill definitions |
| `docs/GETTING-STARTED.md` | User onboarding with skill overview |
