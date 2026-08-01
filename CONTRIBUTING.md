# Contributing to Claude Skills Registry

Thanks for your interest in contributing!

## How to Submit a New Skill

### Option 1: Open an Issue (Recommended)

Open an [issue](https://github.com/majiayu000/claude-skill-registry-core/issues/new) with the following info:

- **Name**: Skill name (kebab-case)
- **Repository**: GitHub URL of your skill repo
- **Description**: One-line description
- **Category**: e.g. `development`, `devops`, `productivity`, `data`, `design`, `testing`
- **Tags**: Relevant keywords

We'll review and add it to the registry.

### Option 2: Pull Request to This Core Repo

This repository (`claude-skill-registry-core`) is the **authoritative pipeline repo**. The separate main repository (`claude-skill-registry`) is a generated publish artifact and will be overwritten on the next publish cycle.

To submit a PR directly, open it against **this repo** and edit `sources/community.json`:

```json
{
  "name": "your-skill-name",
  "repo": "owner/repo",
  "path": "",
  "description": "One-line description of your skill.",
  "category": "development",
  "tags": ["tag1", "tag2"],
  "stars": 0
}
```

## How to Correct an Existing Archived Skill

The public `claude-skill-registry` repository is the browsing and compatibility
entrypoint, so corrections opened there are welcome even though `skills/**` is
generated. Contributors are not expected to understand the three-repository
publish pipeline before reporting or preparing a fix.

When a pull request changes an existing `skills/**` path in the main repository:

1. A maintainer verifies the correction and identifies the matching path in
   `claude-skill-registry-data`.
2. The maintainer ports the change to the data repository and preserves the
   contributor with a `Co-authored-by` trailer.
3. After the data change merges, the maintainer republishes main from pinned
   core and data commits.
4. The original pull request is closed with links to the data change and the
   published result.

Contributors may instead open the archive change directly against
[`claude-skill-registry-data`](https://github.com/majiayu000/claude-skill-registry-data).
Sending the same correction upstream is encouraged because a future archive
refresh may import upstream content again, but it is not required for the
registry maintainer to accept and credit the contribution.

The maintainer design and staged automation plan for this flow are documented
in [`docs/plan/main-generated-contribution-intake-spec.md`](docs/plan/main-generated-contribution-intake-spec.md).

## Requirements

- Your repo must contain a valid `SKILL.md` file (root or subdirectory)
- Must have an open-source license (MIT, Apache-2.0, etc.)
- No malicious code or credential harvesting

## Architecture

```
Core (source of truth) ──► Data (skills archive) ──► Main (publish artifact)
```

- **Core**: `majiayu000/claude-skill-registry-core` — scripts, sources, CI/CD
- **Data**: `majiayu000/claude-skill-registry-data` — archived `SKILL.md` tree
- **Main**: `majiayu000/claude-skill-registry` — merged artifact published from pinned core + data refs
