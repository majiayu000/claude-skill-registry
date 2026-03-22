---
name: code-review
description: Review code written during a run, auto-fix no-brainer issues, and suggest improvements requiring confirmation. Invoked after tests pass.
version: 1.0.0
---

<objective>
Review code written during a run, auto-fix no-brainer issues, and suggest improvements requiring confirmation.
</objective>

<triggers>
  - Invoked by run-execute after tests pass (Step 6b)
  - Receives: files_created, files_modified, run_id, intent context
</triggers>

<degrees_of_freedom>

- **AUTO-FIX**: LOW — Only mechanical, non-semantic changes
- **SUGGESTIONS**: MEDIUM — Present options, let user decide
</degrees_of_freedom>

<llm critical="true">
  <mandate>REVIEW all files created/modified in current run</mandate>
  <mandate>AUTO-FIX only mechanical, non-semantic issues</mandate>
  <mandate>ALWAYS CONFIRM security, architecture, and behavioral changes</mandate>
  <mandate>RESPECT project coding standards from .specs-fire/standards/</mandate>
  <mandate>NEVER break working code — if tests passed, be conservative</mandate>
  <mandate>RE-RUN tests after auto-fixes — revert if tests fail</mandate>
</llm>

<input_context>
  The skill receives from run-execute:

  ```yaml
  files_created:
    - path: src/auth/login.ts
      purpose: Login endpoint handler
    - path: src/auth/login.test.ts
      purpose: Unit tests for login

  files_modified:
    - path: src/routes/index.ts
      changes: Added login route

  run_id: run-fabriqa-2026-001
  intent_id: user-auth
  ```

</input_context>

<references_index>
  <reference name="review-categories" path="references/review-categories.md" load_when="analyzing code"/>
  <reference name="auto-fix-rules" path="references/auto-fix-rules.md" load_when="classifying findings"/>
</references_index>

<flow>
  <step n="1" title="Gather Context">
    <action>Receive files_created and files_modified from parent workflow</action>
    <action>Load project standards:</action>
    <substep>.specs-fire/standards/coding-standards.md</substep>
    <substep>.specs-fire/standards/testing-standards.md</substep>

    <action>Detect project tooling:</action>
    <substep>Check for .eslintrc, eslint.config.js (JavaScript/TypeScript)</substep>
    <substep>Check for .prettierrc (formatting)</substep>
    <substep>Check for golangci.yml (Go)</substep>
    <substep>Check for pyproject.toml, ruff.toml (Python)</substep>

    <action>Read each file to be reviewed</action>

    <output>Reviewing {file_count} files...</output>
  </step>

  <step n="2" title="Run Project Linters (if available)">
    <check if="eslint config exists">
      <action>Run: npm run lint --fix 2>&1 || npx eslint --fix {files}</action>
      <action>Parse output for remaining issues</action>
    </check>

    <check if="golangci config exists">
      <action>Run: golangci-lint run --fix {files}</action>
      <action>Parse output for remaining issues</action>
    </check>

    <check if="ruff/pyproject config exists">
      <action>Run: ruff check --fix {files}</action>
      <action>Parse output for remaining issues</action>
    </check>

    <check if="no linter configured">
      <action>Use built-in review rules from references/review-categories.md</action>
    </check>
  </step>

  <step n="3" title="Analyze Code">
    <action>For each file, check against review categories:</action>
    <substep>Code Quality — unused imports, console statements, formatting</substep>
    <substep>Security — hardcoded secrets, injection vulnerabilities, missing validation</substep>
    <substep>Architecture — code placement, coupling, error handling</substep>
    <substep>Testing — coverage gaps, edge cases, brittle patterns</substep>

    <action>Classify each finding using references/auto-fix-rules.md:</action>
    <substep>AUTO-FIX: Mechanical, non-semantic, reversible, tests won't break</substep>
    <substep>CONFIRM: Behavioral change, security implication, judgment required</substep>

    <action>Group findings by category and severity</action>
  </step>

  <step n="4" title="Apply Auto-Fixes">
    <check if="auto-fix issues found">
      <action>Apply all AUTO-FIX changes</action>
      <action>Track each change made (file, line, before, after)</action>

      <critical>Re-run tests to verify no breakage</critical>
      <action>Run project test command</action>

      <check if="tests fail after auto-fix">
        <output>Auto-fix caused test failure. Reverting...</output>
        <action>Revert all auto-fix changes</action>
        <action>Move failed fixes to CONFIRM category</action>
      </check>

      <check if="tests pass">
        <output>Auto-fixed {count} issues. Tests still passing.</output>
      </check>
    </check>
  </step>

  <step n="5" title="Generate Review Report">
    <action>Create review report using template: templates/review-report.md.hbs</action>
    <action>Write to: .specs-fire/runs/{run-id}/review-report.md</action>
    <action>Include: auto-fixed issues, pending suggestions, skipped items</action>
  </step>

  <step n="6" title="Present Suggestions">
    <check if="no suggestions requiring confirmation">
      <output>
        ## Code Review Complete

        Auto-fixed {auto_count} issues. No additional suggestions.

        Review report: .specs-fire/runs/{run-id}/review-report.md
      </output>
      <return>success</return>
    </check>

    <check if="suggestions exist">
      <template_output section="suggestions">
        ## Code Review Complete

        **Auto-fixed ({auto_count} issues)**:
        {for each auto_fixed}
        - {description} ({file}:{line})
        {/for}

        **Suggestions requiring approval ({suggest_count} issues)**:

        {for each suggestion with index}
        {index}. **[{category}]** {title}
           - File: {file}:{line}
           - Suggestion: {description}
           - Risk: {risk_level}
        {/for}

        ---
        Apply suggestions?
        [a] Apply all suggestions
        {for each suggestion with index}
        [{index}] Apply #{index} only ({category})
        {/for}
        [s] Skip all suggestions
        [r] Review each individually
      </template_output>

      <checkpoint>Wait for user response</checkpoint>
    </check>
  </step>

  <step n="7" title="Process User Choice">
    <check if="response == a">
      <action>Apply all suggestions</action>
      <action>Re-run tests</action>
      <action>Update review-report.md with applied status</action>
    </check>

    <check if="response == s">
      <action>Skip all suggestions</action>
      <action>Update review-report.md with skipped status</action>
    </check>

    <check if="response == r">
      <iterate over="suggestions" as="suggestion">
        <template_output section="individual_suggestion">
          **[{suggestion.category}]** {suggestion.title}

          File: {suggestion.file}:{suggestion.line}

          Current code:
          ```
          {suggestion.current_code}
          ```

          Suggested change:
          ```
          {suggestion.suggested_code}
          ```

          Rationale: {suggestion.rationale}

          Apply this change? [y/n]
        </template_output>
        <checkpoint>Wait for response</checkpoint>
        <check if="response == y">
          <action>Apply this suggestion</action>
        </check>
      </iterate>
      <action>Re-run tests if any changes applied</action>
    </check>

    <check if="response is number">
      <action>Apply only the numbered suggestion</action>
      <action>Re-run tests</action>
      <action>Update review-report.md</action>
    </check>
  </step>

  <step n="8" title="Return to Parent">
    <action>Return summary to run-execute workflow:</action>
    <return_value>
      {
        "success": true,
        "auto_fixed_count": {count},
        "suggestions_applied": {count},
        "suggestions_skipped": {count},
        "tests_passing": true,
        "report_path": ".specs-fire/runs/{run-id}/review-report.md"
      }
    </return_value>
  </step>
</flow>

<output_artifact>
  Creates `.specs-fire/runs/{run-id}/review-report.md` with:

- Summary table (auto-fixed, suggested, skipped by category)
- Detailed list of auto-fixed issues with diffs
- Applied suggestions with approval timestamps
- Skipped suggestions with reasons
</output_artifact>

<success_criteria>
  <criterion>All files created/modified in run reviewed</criterion>
  <criterion>Auto-fixes applied without breaking tests</criterion>
  <criterion>Suggestions presented for user approval</criterion>
  <criterion>review-report.md created in run folder</criterion>
  <criterion>Return status to parent workflow</criterion>
</success_criteria>
