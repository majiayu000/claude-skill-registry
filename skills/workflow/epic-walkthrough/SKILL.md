# Epic Walkthrough Skill

Generate comprehensive walkthrough documentation and trigger self-improvement for epic workflows.

## Purpose

Create walkthrough.md documenting the epic journey and trigger workflow audit/healing for continuous improvement.

## When to Invoke

- During `/epic` Step 8 (Finalization phase)
- After deployment completes successfully
- Via `/finalize` command

## Template Reference

Use the template at `.spec-flow/templates/epic/walkthrough.md` as the base structure.

**Template variables** (replace with actual values):
- `{{EPIC_TITLE}}`, `{{EPIC_NUMBER}}`, `{{EPIC_SLUG}}`
- `{{START_DATE}}`, `{{END_DATE}}`, `{{DURATION_DAYS}}`, `{{DURATION_HOURS}}`
- `{{SPRINT_COUNT}}`, `{{TASKS_COMPLETED}}`
- `{{EXPECTED_VELOCITY}}`, `{{ACTUAL_VELOCITY}}`
- Phase durations, sprint details, quality gate results
- File change statistics, deployment information

**Data sources**:
- `state.yaml` - Phase timestamps, sprint status
- `epic-spec.md` - Business value, constraints
- `sprint-plan.md` - Sprint dependencies, estimates
- `optimization-report.md` - Quality gate results
- `git log` - Commit history, file statistics

## Walkthrough Structure

```xml
<walkthrough>
  <overview>
    <epic_goal>...</epic_goal>
    <business_value>...</business_value>
    <duration>Start: 2025-11-19, End: 2025-11-25 (6 days)</duration>
    <velocity>Expected: 3x, Actual: 4.2x</velocity>
  </overview>

  <phases_completed>
    <phase name="research">
      <duration>2 hours</duration>
      <key_findings>OAuth 2.1 recommended, JWT tokens for sessions</key_findings>
      <artifacts>research.md, API contracts locked</artifacts>
    </phase>
    <phase name="planning">
      <duration>1.5 hours</duration>
      <key_decisions>PostgreSQL for sessions, httpOnly cookies</key_decisions>
      <artifacts>plan.md, sprint-plan.md</artifacts>
    </phase>
    <phase name="implementation">
      <duration>16 hours</duration>
      <sprints_completed>S01 (8h), S02 (12h), S03 (6h)</sprints_completed>
      <artifacts>Implementation in sprints/S01, S02, S03</artifacts>
    </phase>
    <phase name="optimization">
      <duration>2 hours</duration>
      <quality_gates>All passed (tests, security, performance, accessibility)</quality_gates>
      <artifacts>optimization-report.xml</artifacts>
    </phase>
  </phases_completed>

  <validation>
    <quality_gates>
      <gate name="tests" status="passed">98% coverage, 142/142 passing</gate>
      <gate name="security" status="passed">0 critical, 2 medium (triaged)</gate>
      <gate name="performance" status="passed">API p95: 87ms (target: <200ms)</gate>
      <gate name="accessibility" status="passed">WCAG 2.1 AA compliant</gate>
    </quality_gates>
    <deployment>
      <staging>Deployed v1.5.0-rc.1, validated 2025-11-24</staging>
      <production>Promoted to v1.5.0, deployed 2025-11-25</production>
    </deployment>
  </validation>

  <key_files_modified>
    <category name="backend">
      <file path="src/auth/middleware.ts">JWT validation middleware</file>
      <file path="src/auth/service.ts">OAuth 2.1 integration</file>
    </category>
    <category name="frontend">
      <file path="components/LoginForm.tsx">OAuth login flow</file>
      <file path="hooks/useAuth.ts">Auth state management</file>
    </category>
    <category name="infrastructure">
      <file path="migrations/20251119_sessions.sql">Session table</file>
      <file path="contracts/api/auth-v1.yaml">Auth API contract</file>
    </category>
  </key_files_modified>

  <next_steps>
    <future_enhancement priority="high">Add MFA support</future_enhancement>
    <future_enhancement priority="medium">Social login</future_enhancement>
    <technical_debt>Token refresh uses polling (should use refresh tokens)</technical_debt>
    <monitoring>Watch auth_failures_total metric</monitoring>
  </next_steps>

  <summary>
    <what_worked>
      - Parallel sprint execution saved 8 hours
      - API contract locking prevented integration bugs
      - Meta-prompting research identified OAuth 2.1 early
    </what_worked>
    <what_struggled>
      - Sprint S02 took 12h vs 8h estimated
      - Cookie SameSite policy required research
    </what_struggled>
    <lessons_learned>
      - Lock contracts before parallel work
      - Research phase crucial for architectural decisions
      - Parallel execution 4.2x faster than sequential
    </lessons_learned>
    <velocity_impact>
      Expected: 3x faster
      Actual: 4.2x faster
      Reason: S02/S03 ran 60% parallel
    </velocity_impact>
  </summary>
</walkthrough>
```

## Self-Improvement Actions

**1. Run post-mortem audit:**

```bash
/audit-workflow
```

**2. Pattern detection (after 2-3 epics):**

- Analyze completed epics for recurring patterns
- Detect code generation opportunities
- Suggest custom skills for detected patterns
- Generate project-specific commands/hooks

**3. Self-healing:**

```bash
/heal-workflow
```

- Apply approved workflow improvements
- Update skills based on learnings

**4. Update documentation:**

- CHANGELOG.md
- README.md
- Project CLAUDE.md (add epic summary)

**5. Archive epic artifacts:**

- Move prompts to completed/
- Mark epic complete in state.yaml

## Outputs

- `walkthrough.md` - Comprehensive epic summary
- `workflow-improvements.xml` - Self-improvement suggestions
- Updated project documentation

## State Updates

After finalization:

```yaml
phases:
  finalization:
    status: completed
    completed_at: { ISO_TIMESTAMP }

epic:
  status: completed
  completed_at: { ISO_TIMESTAMP }
  velocity_actual: 4.2
```

## Velocity Tracking

**Metrics captured:**

- Expected vs actual sprint durations
- Parallel execution efficiency
- Quality gate pass rates
- Deployment success rate

**Used for:**

- Future epic estimation
- Workflow optimization
- Pattern detection for self-improvement
