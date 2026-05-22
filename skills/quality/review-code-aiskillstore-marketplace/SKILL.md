---
name: review-code
description: Provides a structured workflow for planning and executing code reviews like a senior engineer. Use when asked to review code, PRs, or plan a code review task.
---

# Code Review Skill

## Workflow
1. **Understand**: Read context (ticket, PR description) and identifiy scope.
2. **Execute**: Use the checklist in [references/checklist.md](references/checklist.md).
   - Core areas: Quality, Security, Performance, Maintainability.
3. **Tools**: Run project-specific linting and testing commands (e.g., `just lint`, `npm test`, `pytest`); use static analysis if available.
4. **Document**: Provide constructive feedback with rationale and suggestions.
5. **Follow Up**: Track and verify fixes.

## References
- `checklist.md`: Detailed review criteria.