---
name: releasing
description: Automate semantic versioning releases with CHANGELOG validation, comparison link management, GitHub Actions workflow triggering, and monitoring. Scaffold release infrastructure for new projects. Use when user runs /release command, mentions "release version", "cut a release", "create release", "publish release", "tag release", "release setup", or "scaffold release pipeline".
---

# Release Workflow

Execute semantic versioning releases or scaffold release infrastructure for projects.

## Usage

This skill is invoked when:
- User runs `/release` command with a version argument
- User runs `/release --setup` to scaffold release infrastructure

## Two Operation Modes

### Mode 1: Release (`/release <version>`)
Validates, prepares, and triggers a GitHub release.

### Mode 2: Setup (`/release --setup`)
Scaffolds release scripts and GitHub Actions workflow into the target project.

## Supported Arguments

Parse arguments from user input:

- **`<version>`**: Version to release (e.g., `1.6.0` or `v1.6.0`)
- **`--setup`**: Scaffold release infrastructure into current project
- **`--skip-monitor`**: Trigger workflow but don't wait for completion

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- Git configured with push access to remote
- CHANGELOG.md with a version entry (use `/changelog` to generate)
- `.github/workflows/release.yml` exists (use `--setup` to create)

## Release Flow Steps

### Step 1: Parse and Validate Version

```bash
VERSION="${1:-}"

# Strip 'v' prefix if present
VERSION="${VERSION#v}"

# Validate semver format
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid version format '$VERSION'"
    echo "Expected semantic version (e.g., 1.6.0)"
    exit 1
fi

echo "Releasing version: $VERSION"
```

### Step 2: Pre-flight Checks

```bash
# Check CHANGELOG.md entry exists
if ! grep -qE "^## \[$VERSION\]" CHANGELOG.md; then
    echo "Error: No CHANGELOG entry found for version $VERSION"
    echo "Add entry with header: ## [$VERSION] - $(date +%Y-%m-%d)"
    echo "Tip: Use '/changelog' to generate the entry."
    exit 1
fi
echo "CHANGELOG entry found"

# Check release doesn't already exist
if gh release view "v$VERSION" &>/dev/null; then
    echo "Error: Release v$VERSION already exists"
    echo "Delete first: gh release delete v$VERSION --yes"
    exit 1
fi
echo "Release does not exist, proceeding"
```

### Step 3: Add Comparison Link to CHANGELOG.md

```bash
REPO_URL=$(gh repo view --json url -q '.url')

# Skip if link already exists
if grep -qE "^\[$VERSION\]:" CHANGELOG.md; then
    echo "Comparison link already exists"
else
    # Find previous version (second version header)
    PREV_VERSION=$(grep -E "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md \
        | head -2 | tail -1 | sed 's/.*\[\([0-9.]*\)\].*/\1/')

    if [[ "$PREV_VERSION" != "$VERSION" ]] && [[ -n "$PREV_VERSION" ]]; then
        COMPARE_LINK="[$VERSION]: $REPO_URL/compare/v$PREV_VERSION...v$VERSION"
    else
        COMPARE_LINK="[$VERSION]: $REPO_URL/releases/tag/v$VERSION"
    fi

    # Update [Unreleased] link and add version link
    sed -i.bak "s|\[Unreleased\]:.*|[Unreleased]: $REPO_URL/compare/v$VERSION...HEAD|" CHANGELOG.md
    sed -i.bak "/^\[Unreleased\]:/a\\
$COMPARE_LINK" CHANGELOG.md
    rm -f CHANGELOG.md.bak

    echo "Added comparison link for $VERSION"
fi
```

### Step 4: Commit and Push CHANGELOG Changes

Check if CHANGELOG.md has uncommitted changes. If so, **confirm with the user** before committing:

```bash
if ! git diff --quiet CHANGELOG.md 2>/dev/null; then
    echo "CHANGELOG.md has uncommitted changes."
    # Ask user: "CHANGELOG.md updated with comparison links. Commit and push to main?"
    # If confirmed:
    git add CHANGELOG.md
    git commit -m "docs: prepare release $VERSION"
    git push origin main
    echo "Changes committed and pushed"
fi
```

**Important**: Use conversation to confirm with the user before committing and pushing. Do NOT auto-commit without confirmation.

### Step 5: Trigger Release Workflow

```bash
echo "Triggering release workflow for v$VERSION..."
gh workflow run release.yml -f version="$VERSION"
echo "Workflow triggered"
```

### Step 6: Monitor Workflow

```bash
sleep 5

RUN_ID=$(gh run list --workflow=release.yml --limit=1 --json databaseId -q '.[0].databaseId')
REPO_URL=$(gh repo view --json url -q '.url')

echo "Monitoring workflow run $RUN_ID..."
echo "View at: $REPO_URL/actions/runs/$RUN_ID"

# Poll for completion
while true; do
    STATUS=$(gh run view "$RUN_ID" --json status -q '.status')
    if [[ "$STATUS" == "completed" ]]; then
        CONCLUSION=$(gh run view "$RUN_ID" --json conclusion -q '.conclusion')
        break
    fi
    echo "  Status: $STATUS..."
    sleep 5
done

if [[ "$CONCLUSION" == "success" ]]; then
    echo "Release v$VERSION created successfully!"
    echo "View: $REPO_URL/releases/tag/v$VERSION"
else
    echo "Workflow failed: $CONCLUSION"
    echo "Logs: $REPO_URL/actions/runs/$RUN_ID"
    exit 1
fi
```

If `--skip-monitor` is specified, skip this step and report the workflow URL instead.

## Setup Mode (`--setup`)

When `--setup` is specified, scaffold release infrastructure into the current project.

### What Gets Scaffolded

| Template File | Target Location | Purpose |
|---------------|----------------|---------|
| `scripts/release.sh` | `scripts/release.sh` | Local release orchestrator |
| `templates/release.yml` | `.github/workflows/release.yml` | GitHub Actions workflow |
| `scripts/validate-changelog.sh` | `.github/workflows/scripts/validate-changelog.sh` | CHANGELOG validator |
| `scripts/extract-release-notes.sh` | `.github/workflows/scripts/extract-release-notes.sh` | Release notes extractor |
| `scripts/create-github-release.sh` | `.github/workflows/scripts/create-github-release.sh` | GitHub release creator |

### Scaffolding Process

1. Read each template file from this skill's `scripts/` and `templates/` directories
2. Create target directories (`scripts/`, `.github/workflows/scripts/`)
3. Write files to target project locations
4. Set executable permissions (`chmod +x`) on all shell scripts
5. Verify all files exist
6. Report created files and next steps

```bash
# Create directories
mkdir -p scripts
mkdir -p .github/workflows/scripts

# Set permissions after writing files
chmod +x scripts/release.sh
chmod +x .github/workflows/scripts/validate-changelog.sh
chmod +x .github/workflows/scripts/extract-release-notes.sh
chmod +x .github/workflows/scripts/create-github-release.sh
```

### Post-Setup Next Steps

After scaffolding, inform the user:
1. Ensure CHANGELOG.md exists (use `/changelog` to create)
2. Commit the scaffolded files
3. Run `/release <version>` to create the first release

## Important Notes

- **CHANGELOG format**: Assumes Keep a Changelog format with `## [VERSION]` headers
- **Branch**: Commits and pushes to the current branch (auto-detected via `git rev-parse`)
- **Integration with /changelog**: Use `/changelog` to generate CHANGELOG entries before releasing
- **GitHub CLI required**: Must have `gh` installed and authenticated
- **Workflow file**: Expects `.github/workflows/release.yml` (use `--setup` to create)

## Supporting Documentation

- **[WORKFLOW.md](WORKFLOW.md)** - Detailed 7-phase release process and script template reference
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world release scenarios including first release, patch release, and setup
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues with workflow triggers, CHANGELOG format, and gh CLI
- **[templates/release.yml](templates/release.yml)** - GitHub Actions workflow template for scaffold setup
