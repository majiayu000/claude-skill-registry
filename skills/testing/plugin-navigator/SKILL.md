---
name: plugin-navigator
description: Navigate between Jekyll plugins and their tests. Use when working on _plugins/ or _tests/, finding untested code, or reviewing test coverage.
---

# Plugin Navigator

Tools for navigating between plugins (`_plugins/src/`) and tests (`_tests/src/`).

## Scripts

Run from project root:

```bash
# Find test(s) for a plugin
.claude/skills/plugin-navigator/scripts/test-for-plugin _plugins/src/infrastructure/url_utils.rb

# Find plugin for a test
.claude/skills/plugin-navigator/scripts/plugin-for-test _tests/src/infrastructure/test_url_utils.rb

# Coverage summary
.claude/skills/plugin-navigator/scripts/coverage-stats

# List untested plugins
.claude/skills/plugin-navigator/scripts/coverage-stats --list-missing
.claude/skills/plugin-navigator/scripts/coverage-stats --list-missing --by-domain

# List orphan tests (no matching plugin)
.claude/skills/plugin-navigator/scripts/orphan-tests
```

## Naming Convention

- Plugin: `_plugins/src/{path}/{name}.rb`
- Test: `_tests/src/{path}/test_{name}.rb` or `_tests/src/{path}/test_{name}_*.rb`

Matching is precise: `test_user.rb` and `test_user_integration.rb` match `user.rb`, but `test_user_profile.rb` does NOT match `user.rb` (it matches `user_profile.rb`).

## Architecture

Four domains under `_plugins/src/`:

| Domain | Purpose |
|--------|---------|
| `infrastructure/` | Low-level utilities (logging, URL, text processing, link cache) |
| `content/` | Domain logic (books, posts, authors, series, short stories) |
| `seo/` | JSON-LD generators, front matter validation |
| `ui/` | Generic components (cards, ratings, citations) |

## Test Review Checklist

When reviewing test comprehensiveness:

1. **Public API coverage** - Are all public methods tested?
2. **Edge cases** - nil inputs, empty collections, missing data
3. **Error paths** - Invalid input, missing dependencies
4. **Boundary conditions** - First/last items, single vs multiple
5. **Integration** - Does it work with real Jekyll site data?

## Known Quirks

- Some tests in `lists/` test renderers in `lists/renderers/` (shows as "orphan" but isn't)
- `test_helper.rb` is excluded from orphan detection
