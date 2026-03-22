---
name: version-checker
version: 1.8.0
description: Intelligent auto-update checker with impact analysis and automated execution
author: SDLC Agêntico Team
created: 2026-01-22
updated: 2026-01-22
status: active
type: system
invocation: automatic
---

# Version Checker Skill

## Metadata

- **Skill ID**: version-checker
- **Version**: 1.8.0
- **Phase**: 0 (Pre-workflow)
- **Agent**: orchestrator
- **Invocation**: Automatic (triggered on `/sdlc-start`)
- **Model**: sonnet (efficient for routine checks)

## Purpose

Automatically checks for SDLC Agêntico framework updates, analyzes impact, and manages user approval before executing updates.

## Dependencies

### System Requirements
- Python 3.11+
- gh CLI (GitHub authentication required)
- git

### Python Packages
- PyYAML (already in project)
- Standard library: subprocess, json, pathlib, datetime

### Internal Dependencies
- `.claude/lib/python/sdlc_logging.py` (structured logging)
- `.claude/VERSION` (current version file)

## Scripts

| Script | Purpose | Invocation |
|--------|---------|------------|
| `check_updates.py` | Main entry point | Orchestrator, manual |
| `version_comparator.py` | Version comparison | Internal |
| `release_fetcher.py` | GitHub API | Internal |
| `impact_analyzer.py` | Changelog parsing | Internal |
| `dismissal_tracker.py` | State management | Internal |
| `update_executor.py` | Git operations | Internal (on user approval) |

## Integration Points

### Orchestrator Agent

The orchestrator agent invokes this skill **before** starting any workflow:

```python
# In orchestrator logic
update_info = check_for_updates()

if update_info["update_available"] and not update_info.get("dismissed"):
    # Present to user via AskUserQuestion
    response = AskUserQuestion([
        {
            "question": "Update available. What would you like to do?",
            "options": [
                {"label": "Update now", "description": "..."},
                {"label": "Show changelog", "description": "..."},
                {"label": "Skip this version", "description": "..."},
                {"label": "Remind me later", "description": "..."}
            ]
        }
    ])

    if response == "Update now":
        execute_update(update_info["latest"])
```

### Hooks

No pre/post hooks required (invoked directly by orchestrator).

## State Files

| File | Location | Format | Retention |
|------|----------|--------|-----------|
| Release cache | `~/.claude/simple-memory/latest_release.json` | JSON | 1 hour TTL |
| Dismissals | `~/.claude/simple-memory/dismissed_updates.json` | JSON | Until new release |

## Configuration

No configuration file required. Behavior is hardcoded:
- Cache TTL: 1 hour
- Timeout: 10 seconds (GitHub API), 5 minutes (git operations)
- Rollback: Always attempted on failure

## Logging

**Skill Label**: `version-checker`
**Phase Label**: `0`

Key log events:
- `update_check_started`
- `version_comparison_completed`
- `github_api_call` (with timing)
- `update_execution_started`
- `rollback_triggered`

## Error Handling

All errors are non-blocking:
- GitHub unreachable → Log warning, return "no update"
- Invalid VERSION → Log error, use fallback
- Update fails → Automatic rollback

**Never blocks workflow execution.**

## Testing

Tests: 88 total across 6 modules
Coverage: 90%+ average

Run tests:
```bash
pytest .claude/skills/version-checker/tests/ -v
```

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Version check (cached) | < 100ms | Using cached release |
| Version check (fresh) | 1-2s | GitHub API call |
| Update execution | 10-30s | Depends on repo size |

## Security

- Uses `gh` CLI (authenticated, respects permissions)
- No secrets stored by skill
- Git operations run with user permissions
- Rollback available on all failures

## Limitations

- Requires GitHub releases (won't detect unreleased commits)
- Depends on `gh` CLI authentication
- No support for pre-release versions (alpha/beta)
- Changelog parsing is heuristic (may miss some markers)

## Future Enhancements

- [ ] Support for pre-release channels (beta, alpha)
- [ ] Scheduled update checks (weekly)
- [ ] Rollback command (`/sdlc-rollback v1.7.0`)
- [ ] Dependency update detection (Python packages, Node modules)
- [ ] Telemetry (track update adoption rates)

## Changelog

### v1.8.0 (2026-01-22)
- Initial implementation
- Semantic version comparison
- GitHub release fetching with caching
- Impact analysis (breaking changes, migrations, dependencies, security)
- Dismissal tracking
- Automated update execution with rollback
- Comprehensive test suite (88 tests, 90%+ coverage)
- Structured logging integration
