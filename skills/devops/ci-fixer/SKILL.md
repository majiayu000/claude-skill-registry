---
name: ci-fixer
description: Automated CI/CD pipeline fixer - watches CI, fixes errors locally, commits, and loops until green. Use when CI is failing and you want to automatically fix and verify changes.
argument-hint: "[--auto] [--max-attempts=N]"
color: yellow
---

<objective>
Autonomously fix CI/CD pipeline failures by:
1. Watching CI runs in real-time
2. Analyzing failures (GitHub Actions, Vercel, Netlify, etc.)
3. Fixing errors and verifying locally (tests, linter - NO skipping, NO hacks)
4. Committing fixes and looping until pipeline is green
5. Cleaning up artifacts when done
</objective>

<quick_start>
**Basic usage (watch and fix CI):**

```bash
/ci-fixer
```

**Auto mode (no confirmations):**

```bash
/ci-fixer --auto
```

**With max attempts limit:**

```bash
/ci-fixer --max-attempts=3
```

The skill will:

1. Detect your current branch's CI run
2. Watch for failures
3. Fix errors locally (tests, lint, build)
4. Commit and push
5. Loop until green ✅

**CRITICAL**: Zero tolerance for hacks - fixes must be proper, no `@ts-ignore`, `eslint-disable`, or test skipping.
</quick_start>

<parameters>
| Flag | Description |
|------|-------------|
| `-a, --auto` | Auto mode - skip confirmations, auto-proceed |
| `-m N, --max-attempts=N` | Maximum fix attempts before asking for help (default: 5) |
</parameters>

<state_variables>
**Persist throughout all steps:**

| Variable            | Type    | Description                                       |
| ------------------- | ------- | ------------------------------------------------- |
| `{auto_mode}`       | boolean | Skip confirmations                                |
| `{max_attempts}`    | integer | Max fix attempts (default: 5)                     |
| `{current_attempt}` | integer | Current attempt number                            |
| `{run_id}`          | string  | Current GitHub Actions run ID                     |
| `{branch}`          | string  | Current git branch                                |
| `{last_commit_sha}` | string  | SHA of commit being watched                       |
| `{artifacts_dir}`   | string  | Path to artifacts: `.claude/data/ci-{run_id}/`    |
| `{error_source}`    | string  | Source of error (github-actions, vercel, netlify) |
| `{error_logs}`      | string  | Captured error logs                               |
| `{fixes_applied}`   | list    | List of fixes applied this session                |
| `{local_verified}`  | boolean | Whether local tests/lint passed                   |

</state_variables>

<entry_point>
Load `steps/step-00-init.md`
</entry_point>

<step_files>
| Step | File | Description |
|------|------|-------------|
| 0 | `step-00-init.md` | Parse flags, detect branch, setup state |
| 1 | `step-01-watch-ci.md` | Find CI run, monitor status |
| 2 | `step-02-analyze-errors.md` | Fetch logs/artifacts, analyze errors |
| 3 | `step-03-fix-locally.md` | Fix errors, verify locally |
| 4 | `step-04-commit-push.md` | Commit and push, loop back |
| 5 | `step-05-cleanup.md` | Cleanup artifacts, show summary |
</step_files>

<workflow_diagram>

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Init   │───►│  Watch   │───►│ Analyze  │───►│   Fix    │───►│  Commit  │
│ Step 0   │    │   CI     │    │  Errors  │    │ Locally  │    │  & Push  │
└──────────┘    └────┬─────┘    └──────────┘    └──────────┘    └────┬─────┘
                     │                                               │
                     │         ┌─────────────────────────────────────┘
                     │         │ (loop until green or max attempts)
                     │◄────────┘
                     │
                ┌────┴────┐    ┌──────────┐
                │ SUCCESS │───►│ Cleanup  │
                │ or STOP │    │ Step 5   │
                └─────────┘    └──────────┘
```

</workflow_diagram>

<artifacts_storage>
Artifacts are stored in `.claude/data/ci-{run_id}/`:

```
.claude/data/ci-{run_id}/
├── github/
│   ├── failed-logs.txt      # Failed job logs
│   └── artifacts/           # Downloaded artifacts
├── vercel/
│   ├── deployment.json      # Deployment info
│   └── logs.txt             # Build/runtime logs
├── netlify/
│   └── build-logs.txt       # Build logs
└── summary.md               # Error analysis summary
```

</artifacts_storage>

<core_principles>
<zero_tolerance_policy>
**ZERO TOLERANCE FOR HACKS**

If you can't fix it properly, ASK FOR HELP. Never bypass or hack.

1. **NEVER skip tests** - All tests must pass locally before committing
2. **NEVER hack around issues** - Fix the root cause, don't disable checks
3. **NEVER use bypass flags** - No `--no-verify`, `--skip`, `@ts-ignore`, `eslint-disable`
4. **NEVER disable rules** - Don't add to `.eslintignore`, don't lower strictness
5. **Verify locally first** - Always run tests/lint locally before pushing
6. **Minimal changes** - Only fix what's broken, don't refactor unrelated code
7. **Clear commits** - Each fix should have a descriptive commit message
8. **Clean up** - Delete artifacts when workflow completes

**Forbidden hacks include:** `@ts-ignore`, `eslint-disable`, `.skip`, `as any`, `--no-verify`, `--legacy-peer-deps`, commenting out tests, changing assertions to match wrong output, adding files to ignore lists.
</zero_tolerance_policy>
</core_principles>

<success_criteria>

- CI pipeline status successfully monitored
- Errors analyzed and root cause identified
- Fixes applied locally and verified (all tests/lint passing)
- Changes committed with clear messages
- CI pipeline green ✅ after fixes
- Artifacts cleaned up
- No hacks or bypasses used
- Maximum attempts limit respected
  </success_criteria>

<references>
- [CLI Commands](references/cli-commands.md) - GitHub, Vercel, Netlify CLI reference
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
</references>
