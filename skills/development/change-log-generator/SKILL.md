---
name: change-log-generator
description: Automatically generates change logs from git commits, patches, and pull requests. Use when preparing software releases, creating version summaries, or maintaining CHANGELOG.md files. Analyzes commit messages (including conventional commits), diff/patch files, and PR data to produce categorized Markdown change logs organized by type (Features, Bug Fixes, Breaking Changes, etc.). Ideal for release notes, version updates, and automated changelog maintenance.
---

# Change Log Generator

Automatically generate comprehensive change logs from git history and code changes.

## Core Capabilities

This skill helps create change logs by:

1. **Analyzing git commits** - Parse commit messages for changes
2. **Processing conventional commits** - Extract structured information from standardized commits
3. **Examining diffs/patches** - Understand code changes from git diff output
4. **Categorizing changes** - Automatically group by type (features, fixes, docs, etc.)
5. **Formatting output** - Generate Markdown change logs following best practices

## Change Log Generation Workflow

### Step 1: Gather Change Information

Collect commits and changes for the release period.

**Determine Release Range:**

```bash
# Changes since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Changes between two tags
git log v1.2.0..v1.3.0 --oneline

# Changes in last N commits
git log -n 50 --oneline

# Changes since specific date
git log --since="2024-01-01" --oneline

# Changes in current branch vs main
git log main..HEAD --oneline
```

**Get Detailed Commit Information:**

```bash
# Full commit messages
git log v1.2.0..HEAD --format="%H|%an|%ad|%s|%b" --date=short

# With file changes
git log v1.2.0..HEAD --name-status

# With diff stats
git log v1.2.0..HEAD --stat
```

**Get Pull Request Information:**

```bash
# Using GitHub CLI
gh pr list --state merged --base main --limit 50

# Get PR details
gh pr view 123 --json title,body,labels,mergedAt
```

### Step 2: Parse Commit Messages

Extract meaningful information from commits.

**Conventional Commit Format:**

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Common Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system or external dependency changes
- `ci`: CI configuration changes
- `chore`: Other changes that don't modify src or test files

**Examples:**

```
feat(auth): add OAuth2 authentication

Implements OAuth2 authentication flow using Google provider.
Users can now sign in with their Google accounts.

Closes #45
```

```
fix(api): prevent race condition in user creation

Race condition occurred when multiple requests tried to create
the same user simultaneously. Added database constraint and
retry logic.

Fixes #123
```

```
docs: update installation instructions

Added troubleshooting section for Windows users.
```

```
BREAKING CHANGE: remove deprecated API endpoints

The /api/v1/users endpoint has been removed. Use /api/v2/users instead.
```

**Parse Commit Messages:**

```python
import re

def parse_conventional_commit(message):
    """Parse conventional commit message."""
    # Pattern: type(scope): description
    pattern = r'^(\w+)(\(([^)]+)\))?:\s*(.+)$'
    match = re.match(pattern, message)

    if match:
        return {
            'type': match.group(1),
            'scope': match.group(3),
            'description': match.group(4),
            'breaking': 'BREAKING CHANGE' in message
        }
    else:
        return {
            'type': 'other',
            'scope': None,
            'description': message,
            'breaking': 'BREAKING CHANGE' in message
        }

# Example
commit = "feat(auth): add OAuth2 authentication"
parsed = parse_conventional_commit(commit)
# Returns: {'type': 'feat', 'scope': 'auth', 'description': 'add OAuth2 authentication', 'breaking': False}
```

See `references/conventional_commits.md` for detailed parsing rules.

### Step 3: Categorize Changes

Group commits by change type.

**Category Mapping:**

```python
CATEGORIES = {
    'feat': {
        'title': 'Features',
        'emoji': '✨',
        'description': 'New features and capabilities'
    },
    'fix': {
        'title': 'Bug Fixes',
        'emoji': '🐛',
        'description': 'Bug fixes and corrections'
    },
    'perf': {
        'title': 'Performance',
        'emoji': '⚡',
        'description': 'Performance improvements'
    },
    'refactor': {
        'title': 'Refactoring',
        'emoji': '♻️',
        'description': 'Code refactoring'
    },
    'docs': {
        'title': 'Documentation',
        'emoji': '📚',
        'description': 'Documentation updates'
    },
    'test': {
        'title': 'Testing',
        'emoji': '✅',
        'description': 'Test additions and updates'
    },
    'build': {
        'title': 'Build System',
        'emoji': '🏗️',
        'description': 'Build and dependency changes'
    },
    'ci': {
        'title': 'CI/CD',
        'emoji': '👷',
        'description': 'CI/CD changes'
    },
    'style': {
        'title': 'Code Style',
        'emoji': '💄',
        'description': 'Code style and formatting'
    },
    'chore': {
        'title': 'Chores',
        'emoji': '🔧',
        'description': 'Maintenance and chores'
    }
}

def categorize_commits(commits):
    """Categorize commits by type."""
    categorized = {}

    for commit in commits:
        parsed = parse_conventional_commit(commit['message'])
        commit_type = parsed['type']

        if commit_type not in categorized:
            categorized[commit_type] = []

        categorized[commit_type].append({
            'description': parsed['description'],
            'scope': parsed['scope'],
            'sha': commit['sha'][:7],
            'author': commit['author'],
            'breaking': parsed['breaking']
        })

    return categorized
```

**Prioritize Categories:**

Order of importance:
1. Breaking Changes (always first)
2. Features
3. Bug Fixes
4. Performance
5. Security
6. Deprecations
7. Other categories

### Step 4: Format Change Log

Generate Markdown output following conventions.

**Basic Template:**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New feature A
- New feature B

### Changed
- Updated component X
- Improved performance of Y

### Deprecated
- Old API endpoint will be removed in v2.0

### Removed
- Deprecated feature Z

### Fixed
- Bug in authentication flow
- Memory leak in processor

### Security
- Fixed XSS vulnerability in input validation
```

**Generate Changelog Entry:**

```python
def generate_changelog_entry(version, date, categorized_commits):
    """Generate changelog entry for a version."""
    lines = []

    # Header
    lines.append(f"## [{version}] - {date}\n")

    # Breaking Changes (if any)
    breaking_changes = []
    for category, commits in categorized_commits.items():
        for commit in commits:
            if commit.get('breaking'):
                breaking_changes.append(commit)

    if breaking_changes:
        lines.append("### ⚠️ BREAKING CHANGES\n")
        for change in breaking_changes:
            scope_str = f"**{change['scope']}**: " if change['scope'] else ""
            lines.append(f"- {scope_str}{change['description']} ({change['sha']})")
        lines.append("")

    # Regular categories
    category_order = ['feat', 'fix', 'perf', 'refactor', 'docs', 'test', 'build', 'ci', 'style', 'chore']

    for cat_type in category_order:
        if cat_type in categorized_commits:
            category_info = CATEGORIES.get(cat_type, {'title': cat_type.title()})
            lines.append(f"### {category_info['title']}\n")

            for commit in categorized_commits[cat_type]:
                if commit.get('breaking'):
                    continue  # Already listed in breaking changes

                scope_str = f"**{commit['scope']}**: " if commit['scope'] else ""
                lines.append(f"- {scope_str}{commit['description']} ([`{commit['sha']}`](link/to/commit/{commit['sha']}))")

            lines.append("")

    return "\n".join(lines)
```

**Example Output:**

```markdown
## [1.3.0] - 2024-02-15

### ⚠️ BREAKING CHANGES

- **api**: remove deprecated /v1/users endpoint (a1b2c3d)

### Features

- **auth**: add OAuth2 authentication support ([`d4e5f6g`](link))
- **dashboard**: add real-time metrics visualization ([`h7i8j9k`](link))
- **api**: implement rate limiting for API endpoints ([`l0m1n2o`](link))

### Bug Fixes

- **auth**: prevent race condition in user creation ([`p3q4r5s`](link))
- **ui**: fix button alignment on mobile devices ([`t6u7v8w`](link))
- **api**: handle null values in request validation ([`x9y0z1a`](link))

### Performance

- **database**: optimize user query with indexes ([`b2c3d4e`](link))
- **api**: implement caching for frequently accessed data ([`f5g6h7i`](link))

### Documentation

- update installation instructions ([`j8k9l0m`](link))
- add troubleshooting guide ([`n1o2p3q`](link))
```

### Step 5: Handle Special Cases

Address non-conventional commits and edge cases.

**Non-Conventional Commits:**

```python
def categorize_non_conventional(message):
    """Categorize commits that don't follow conventional format."""
    message_lower = message.lower()

    # Keyword-based categorization
    if any(word in message_lower for word in ['add', 'implement', 'create']):
        return 'feat'
    elif any(word in message_lower for word in ['fix', 'resolve', 'correct', 'patch']):
        return 'fix'
    elif any(word in message_lower for word in ['update', 'improve', 'enhance']):
        return 'refactor'
    elif any(word in message_lower for word in ['doc', 'readme', 'comment']):
        return 'docs'
    elif any(word in message_lower for word in ['test', 'spec']):
        return 'test'
    else:
        return 'other'
```

**Merge Commits:**

```bash
# Exclude merge commits
git log --no-merges v1.2.0..HEAD

# Or include merge commits with special handling
git log --first-parent v1.2.0..HEAD
```

**Pull Request Integration:**

```python
def extract_pr_info(commit_message):
    """Extract PR number from commit message."""
    # Pattern: (#123) or Merge pull request #123
    import re
    match = re.search(r'#(\d+)', commit_message)
    if match:
        return match.group(1)
    return None

def enhance_with_pr_data(commit, pr_number):
    """Enhance commit with PR metadata."""
    # Use gh CLI or GitHub API
    import subprocess
    import json

    result = subprocess.run(
        ['gh', 'pr', 'view', pr_number, '--json', 'title,labels,author'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        pr_data = json.loads(result.stdout)
        commit['pr_title'] = pr_data.get('title')
        commit['pr_labels'] = pr_data.get('labels', [])
        commit['pr_author'] = pr_data.get('author', {}).get('login')

    return commit
```

### Step 6: Add Metadata and Links

Enrich changelog with helpful information.

**Add Comparison Links:**

```markdown
## [1.3.0] - 2024-02-15

[Full Changelog](https://github.com/user/repo/compare/v1.2.0...v1.3.0)

### Features
...
```

**Add Contributors:**

```bash
# Get unique contributors
git log v1.2.0..v1.3.0 --format="%an <%ae>" | sort | uniq
```

```markdown
## [1.3.0] - 2024-02-15

**Contributors:** @alice, @bob, @charlie

### Features
...
```

**Add Issue References:**

```python
def extract_issue_refs(message):
    """Extract issue references from commit message."""
    import re
    # Patterns: #123, Closes #123, Fixes #123
    patterns = [
        r'#(\d+)',
        r'[Cc]loses?\s+#(\d+)',
        r'[Ff]ixes?\s+#(\d+)',
        r'[Rr]esolves?\s+#(\d+)'
    ]

    issues = set()
    for pattern in patterns:
        matches = re.findall(pattern, message)
        issues.update(matches)

    return list(issues)

# Format in changelog
# - Fix authentication bug (closes #123, #124)
```

### Step 7: Validate and Publish

Review and finalize the changelog.

**Validation Checklist:**

- [ ] All significant changes included
- [ ] Breaking changes clearly marked
- [ ] Changes categorized correctly
- [ ] Links working (commits, PRs, issues)
- [ ] Version number follows semantic versioning
- [ ] Date is correct
- [ ] Contributors acknowledged
- [ ] No duplicate entries
- [ ] Formatting consistent

**Update CHANGELOG.md:**

```bash
# Prepend new entry to existing CHANGELOG.md
cat new_entry.md CHANGELOG.md > temp.md
mv temp.md CHANGELOG.md

# Commit the changelog
git add CHANGELOG.md
git commit -m "docs: update changelog for v1.3.0"
```

**Create GitHub Release:**

```bash
# Using gh CLI
gh release create v1.3.0 \
  --title "Version 1.3.0" \
  --notes-file new_entry.md

# Or manually via GitHub web interface
```

## Quick Templates

### Minimal Template

```markdown
## [1.3.0] - 2024-02-15

### Added
- OAuth2 authentication
- Real-time metrics

### Fixed
- Race condition in user creation
- Mobile UI alignment

### Changed
- Optimized database queries
- Updated dependencies
```

### Standard Template

```markdown
## [1.3.0] - 2024-02-15

[Full Changelog](https://github.com/user/repo/compare/v1.2.0...v1.3.0)

### ⚠️ BREAKING CHANGES

- **api**: Removed deprecated /v1/users endpoint. Migrate to /v2/users ([#145](link))

### Features

- **auth**: Add OAuth2 authentication support ([#142](link)) @alice
- **dashboard**: Real-time metrics visualization ([#143](link)) @bob

### Bug Fixes

- **auth**: Prevent race condition in user creation ([#144](link)) @alice
- **ui**: Fix button alignment on mobile ([#146](link)) @charlie

### Performance

- **database**: Optimize user queries with indexes ([#147](link))

**Contributors:** @alice, @bob, @charlie
```

### Comprehensive Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### In Progress
- Feature X under development
- Performance improvements being tested

## [1.3.0] - 2024-02-15

[Full Changelog](https://github.com/user/repo/compare/v1.2.0...v1.3.0) | [Release Notes](link)

> **Highlights:** This release adds OAuth2 authentication and significantly improves performance.

### ⚠️ BREAKING CHANGES

- **api**: Removed deprecated /v1/users endpoint
  - **Migration Guide:** Replace `/v1/users` with `/v2/users` in your API calls
  - **Impact:** Applications using the old endpoint will receive 404 errors
  - See [Migration Guide](link) for details

### ✨ Features

- **auth**: Add OAuth2 authentication support ([`a1b2c3d`](link)) ([#142](link))
  - Supports Google and GitHub providers
  - Automatic account creation on first login
  - Thanks to @alice for implementation
- **dashboard**: Real-time metrics visualization ([`d4e5f6g`](link)) ([#143](link))
  - Live update every 5 seconds
  - Customizable dashboard widgets
- **api**: Implement rate limiting ([`h7i8j9k`](link)) ([#148](link))
  - 100 requests per minute per IP
  - Configurable via environment variables

### 🐛 Bug Fixes

- **auth**: Prevent race condition in user creation ([`l0m1n2o`](link)) ([#144](link))
  - Fixed duplicate user creation
  - Added database constraint
- **ui**: Fix button alignment on mobile devices ([`p3q4r5s`](link)) ([#146](link))
- **api**: Handle null values in validation ([`t6u7v8w`](link)) ([#149](link))

### ⚡ Performance

- **database**: Optimize user queries with indexes ([`x9y0z1a`](link)) ([#147](link))
  - 70% faster user lookups
  - Reduced database load
- **api**: Implement response caching ([`b2c3d4e`](link)) ([#150](link))
  - 50% reduction in API response time

### 📚 Documentation

- Update installation instructions ([`f5g6h7i`](link))
- Add troubleshooting guide ([`j8k9l0m`](link))
- Improve API documentation ([`n1o2p3q`](link))

### 🏗️ Build System

- Update dependencies to latest versions ([`r4s5t6u`](link))
- Add Docker support for development ([`v7w8x9y`](link))

### 🧪 Testing

- Add integration tests for auth flow ([`z0a1b2c`](link))
- Improve test coverage to 85% ([`d3e4f5g`](link))

### 👷 CI/CD

- Add automated deployment to staging ([`h6i7j8k`](link))
- Implement security scanning in CI ([`l9m0n1o`](link))

**New Contributors:**
- @alice made their first contribution in #142
- @bob improved the dashboard in #143

**Full Contributor List:** @alice, @bob, @charlie, @david

**Download:** [v1.3.0 Release](link)

---

## [1.2.0] - 2024-01-15

[Previous release notes...]
```

## Automation Scripts

### Generate Changelog Script

```bash
#!/bin/bash
# generate_changelog.sh - Generate changelog between two tags

FROM_TAG=${1:-$(git describe --tags --abbrev=0 HEAD^)}
TO_TAG=${2:-HEAD}
VERSION=${3:-"Unreleased"}
DATE=$(date +%Y-%m-%d)

echo "# Changelog Entry for $VERSION"
echo ""
echo "## [$VERSION] - $DATE"
echo ""

# Get commits
git log $FROM_TAG..$TO_TAG --format="%s" --no-merges | while read commit; do
    # Parse conventional commit
    if [[ $commit =~ ^([a-z]+)(\(([^)]+)\))?:\ (.+)$ ]]; then
        type="${BASH_REMATCH[1]}"
        scope="${BASH_REMATCH[3]}"
        desc="${BASH_REMATCH[4]}"

        case $type in
            feat)
                echo "### Features" >> /tmp/feat.txt
                echo "- $desc" >> /tmp/feat.txt
                ;;
            fix)
                echo "### Bug Fixes" >> /tmp/fix.txt
                echo "- $desc" >> /tmp/fix.txt
                ;;
            docs)
                echo "### Documentation" >> /tmp/docs.txt
                echo "- $desc" >> /tmp/docs.txt
                ;;
        esac
    fi
done

# Output in order
for file in /tmp/{feat,fix,docs}.txt; do
    if [ -f "$file" ]; then
        cat "$file" | sort | uniq
        echo ""
        rm "$file"
    fi
done
```

See `references/automation_examples.md` for more complete scripts.

## Best Practices

1. **Use conventional commits** - Makes categorization automatic
2. **Include issue/PR references** - Provides context and traceability
3. **Highlight breaking changes** - Critical for users upgrading
4. **Keep entries concise** - One line per change, link to details
5. **Use present tense** - "Add feature" not "Added feature"
6. **Group by category** - Easier to scan and understand
7. **Add migration guides** - For breaking changes
8. **Link to commits/PRs** - Enables deeper investigation
9. **Acknowledge contributors** - Recognize team efforts
10. **Update regularly** - Don't wait until release day

## Resources

- **`references/conventional_commits.md`** - Detailed guide to conventional commit format and parsing rules
- **`references/keep_a_changelog.md`** - Keep a Changelog format specification and examples
- **`references/automation_examples.md`** - Complete scripts for automating changelog generation

## Quick Reference

| Task | Command |
|------|---------|
| Commits since last tag | `git log $(git describe --tags --abbrev=0)..HEAD` |
| Commits between tags | `git log v1.2.0..v1.3.0` |
| No merge commits | `git log --no-merges` |
| With file changes | `git log --name-status` |
| Contributors | `git log --format="%an" \| sort \| uniq` |
| PR info | `gh pr view 123 --json title,body` |
| Create release | `gh release create v1.3.0 --notes-file changelog.md` |

## Common Patterns

**Pattern 1: Quick release notes**
```bash
git log v1.2.0..v1.3.0 --oneline --no-merges | \
  sed 's/^[a-f0-9]* /- /' > release_notes.md
```

**Pattern 2: Group by author**
```bash
git log v1.2.0..v1.3.0 --format="%an: %s" --no-merges | \
  sort | uniq
```

**Pattern 3: Extract breaking changes**
```bash
git log v1.2.0..v1.3.0 --format="%B" --no-merges | \
  grep -A 5 "BREAKING CHANGE"
```
