---
name: farm-inspect
description: Run full code inspection with all audit agents in parallel. Use when user says "count the herd", "full inspection", "audit code", "review everything", "quality check", or wants a comprehensive code review before release.
allowed-tools: Bash(*), Task, Read, Edit, Glob, Grep
---

# Farm Inspect Skill

Full code inspection using all audit agents. Runs quality gates but does NOT push.

## When to Use
- Before releases
- After major changes
- Quality gate checks
- Comprehensive code review

## Workflow

### Step 1: Run Audit Agents (Parallel)
Launch these agents in parallel using the Task tool:

1. **code-quality** - Code review + smell detection
   - Updates `_AUDIT/CODE_QUALITY.md`

2. **security-auditor** - OWASP Top 10 scanning
   - Updates `_AUDIT/SECURITY.md`

3. **performance-auditor** - Performance anti-patterns
   - Updates `_AUDIT/PERFORMANCE.md`

4. **accessibility-auditor** - WCAG 2.1 compliance
   - Updates `_AUDIT/ACCESSIBILITY.md`

5. **code-cleaner** - Dead code + comment detection
   - Reports what would be cleaned (dry run)

### Step 1b: Knip Analysis (if enabled)
If knip is installed in the project, run dead code detection:

\`\`\`bash
npx knip --reporter compact
\`\`\`

Include findings:
- Unused files
- Unused dependencies
- Unused exports

### Step 1c: Knip Auto-Fix Prompt (if enabled)
If knip found issues, ask user:
"Would you like to run \`knip --fix --allow-remove-files\` to automatically fix issues?"

If confirmed, run:
\`\`\`bash
npx knip --fix --allow-remove-files
\`\`\`

**Warning:** This modifies/deletes files. Review changes with \`git diff\` after running.

### Step 2: Dry Run Quality Gates
Run these commands but do NOT commit or push:

1. **Lint**: Run the configured lint command
2. **Test**: Run the configured test command
3. **Build**: Run the configured build command

### Step 3: Generate Summary Report
Consolidate all findings:
- Critical issues (must fix)
- High priority issues
- Medium priority issues
- Low priority suggestions

## Output Format
```
## Full Inspection Complete

### Code Quality
Score: X/10
Issues: X critical, X high, X medium

### Security
Score: X/10
Vulnerabilities: X found

### Performance
Score: X/10
Anti-patterns: X found

### Accessibility
Score: X/10
WCAG issues: X found

### Dead Code (Knip)
- Unused files: X
- Unused deps: X
- Unused exports: X

### Quality Gates
- Lint: ✓/✗
- Tests: ✓/✗
- Build: ✓/✗

### Next Steps
[List of recommended actions]
```

## Important
This skill does NOT push changes. Use `/push` when ready to commit and push.
