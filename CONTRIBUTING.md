# Contributing to Claude Skills Registry

Thanks for your interest in contributing!

## How to Submit a New Skill

### Option 1: Open an Issue (Recommended)

Open an [issue](https://github.com/majiayu000/claude-skill-registry-core/issues/new) with the following info:

- **Name**: Skill name (kebab-case)
- **Repository**: GitHub URL of your skill repo
- **Skill path**: Path to `SKILL.md` if it is not at the repository root
- **Description**: One-line description
- **Category**: e.g. `development`, `devops`, `productivity`, `data`, `design`, `testing`
- **Tags**: Relevant keywords
- **License**: License identifier and link to the applicable license text
- **Dependencies and pricing**: Required tools, services, accounts, API keys, and any usage charges; say "none" where applicable
- **Setup and operations**: Local files or settings changed, data sent to external services, and how user authorization is obtained

We'll review the submission against the requirements below before deciding
whether to add it. Use the same disclosures in the PR description when
submitting directly.

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
  "stars": 0,
  "license": "MIT",
  "distribution": "compatible"
}
```

This example assumes MIT covers the skill and its bundled files. Use the
upstream's actual license and provide its license text; maintainers review
redistribution eligibility before accepting bundled assets. License disclosure
in the PR body must also be reflected in the source row. Bundled assets require
an approved compatible license and `distribution: "compatible"`, or GPL-3.0
(`GPL-3.0-only` / `GPL-3.0-or-later` also accepted) with
`distribution: "restricted"`. GPL entries are separate source works under
their upstream license, not relicensed as MIT. The downloader requires their
complete support files and a nonempty `LICENSE` or `LICENSE.md`, preferring
the skill directory's license and otherwise copying the repository-root
license from the same source revision. GPL skill text is preserved rather
than rewriting its frontmatter to match the catalog summary; security checks
still apply. Maintainers must verify that the
selected license covers the submitted files and retain upstream attribution.
GPL downloads fail if any source file falls outside the supported archive
scope. License provenance records the selected upstream path so liveness
checks cannot substitute a different license when the original disappears.

Community rows whose `source_url` cites a specific commit
(`/blob/<40-hex-sha>/` or `/tree/<40-hex-sha>/`) are archived at that exact
commit: sync verifies the commit still exists and fails closed rather than
substituting the branch head. Rows citing a branch (or no URL) are archived
at the probed branch head at acquisition time; for those, intake review is a
point-in-time review. Existing archives are never re-downloaded by sync; a
pin change only affects new acquisitions.

For Apache-2.0 sources with approved redistribution, the archive step keeps
the upstream `LICENSE`/`LICENSE.md` and any `NOTICE`/`NOTICE.md`/`NOTICE.txt`
when they exist, honoring Apache-2.0 section 4's license and NOTICE
conditions. Files in the skill directory take precedence over repository-root
files of the same name; root files are copied from the same archived
revision. Retention is keep-when-present: a missing or invalid upstream legal
file never blocks acquisition (unlike the GPL fail-closed license
requirement), because many repositories declare their license only in
metadata or a README. The selected upstream path of every retained legal
file is recorded in `license_source_paths`, and asset liveness checks track
those exact upstream paths so a disappearing root LICENSE or NOTICE is
reported as `partial` rather than silently ignored. Existing archives are
not retroactively backfilled by this policy; remediation of already-published
Apache-2.0 archives requires a separate maintainer-approved backfill.

## Upstream-only listings

For a source that should be discoverable without mirroring its instruction body,
submit a maintainer-reviewed row to `sources/listed.json`. Use the same name,
repo, description, canonical category and tags as a community submission; `path`
identifies the upstream skill directory (or `SKILL.md`) and `branch` defaults to
`main`. Disclose the same setup, service, pricing and operational requirements.

Listed entries appear in search with a **Listed only** label and an upstream
link. Their bodies are not downloaded, scanned or functionally verified. No
install command, verified-install discovery index, or scan-qualified static
guide is generated for a listed entry. Catalog metadata is validated and checked
against the existing source blocklist and instruction-override patterns; this
does not establish the safety or quality of the upstream body.

An existing archive of the same repo/path/branch takes precedence. Listing a
source also prevents the acquisition queue from downloading the same repo/path
through another discovery file; it does not delete any existing archive.
To request archival, remove its listed row and submit it through normal community
intake with the redistribution and security requirements below. Changes to the
listed catalog require maintainer review; the existing community append-only
and retirement policy continues to apply to `sources/community.json`.

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
- Include the applicable license text and attribution covering `SKILL.md` and any bundled files so the registry can archive and redistribute them
- Provide a usable task workflow and complete setup instructions, including required scripts and dependencies
- No malicious code or credential harvesting

### Commercial services and promotion

Commercial API integrations and free tools whose authors also sell paid
products are eligible for intake. Commercial affiliation or a link to a paid
product is not, by itself, a reason to reject a skill. The submitted workflow
must perform a concrete task under its disclosed prerequisites; content whose
primary purpose is advertising, referrals, or upselling without a usable task
workflow is not accepted.

Disclose the following in the submission and keep `SKILL.md` and README consistent:

- Required tools, network services, accounts, and API keys, distinguishing setup requirements from normal operation.
- Metered usage, free-tier limits, and paid requirements, with a link to current pricing where applicable. An open-source skill license does not make its external service free.
- Files and settings created or changed, including credential storage and optional shell-profile integration.
- Data sent to external services, its destination and purpose, and any account creation, subscriptions, or payments the workflow can initiate.

The skill must obtain explicit user authorization before sending personal data
for account creation, starting subscriptions or payments, or modifying shell
profiles. These actions must not follow merely from installing the skill.
Hidden charges, unauthorized signup or configuration changes, and collection
of credentials unrelated to the stated task are grounds for rejection.

Start the existing catalog `description` with material prerequisites, such as
"requires an account and metered API" or "requires a remote MCP server", so
truncated list summaries retain them. Keep detailed setup, pricing, and
operation disclosures in the upstream docs.

### Listing and recommendations

Catalog inclusion is not a maintainer recommendation or a guarantee of quality
or safety. Security scan results describe the checks performed; they do not
establish that a skill works. Automatically generated featured lists reflect
index ranking signals and do not imply functional verification. A maintainer's
explicit recommendation requires functional verification, with the tested
revision, scope, and limitations recorded. Review these disclosures during
intake using the existing review process.

## Architecture

```
Core (source of truth) ──► Data (skills archive) ──► Main (publish artifact)
```

- **Core**: `majiayu000/claude-skill-registry-core` — scripts, sources, CI/CD
- **Data**: `majiayu000/claude-skill-registry-data` — archived `SKILL.md` tree
- **Main**: `majiayu000/claude-skill-registry` — merged artifact published from pinned core + data refs

## Maintainer-reviewed catalog retirement

Community intake remains append-only. An unavailable URL (including a GitHub
404), contributor assertion, PR label, or proposed replacement does not authorize
retirement. Source retirement is separate from author takedowns in [REMOVAL.md](REMOVAL.md).

Use two separate PRs:

1. A maintainer verifies the evidence and records an explicit decision in a core
   issue or PR. An authorization-only PR appends a record to
   `policy/community-retirements.json`, copying the complete existing catalog
   row into `entry`, with a nonempty `reason`, the public `decision_url`, and
   `archive_policy: "retain"`. Review and merge that decision through the
   repository's normal maintainer process. Do not combine it with a removal.
2. A subsequent PR removes only those exact rows from `sources/community.json`.
   Do not edit, reorder, add, or reformat surviving rows; the final surviving
   row may lose its trailing comma. Multiple removals each need their own exact
   pre-existing authorization. No other file may change in the removal PR.

The guard reads authorizations from the target base commit, never from a new
record in the removal branch. Missing legacy ledgers authorize no retirement;
malformed ledgers fail closed. Decisions are append-only audit records. If row
metadata has changed, append a new exact-row decision in a separate reviewed
authorization PR; preserve the old decision rather than broadening it. A URL is
validated for shape only; maintainers must verify its contents and authority. The command-line interface is unchanged; the text-only validator
continues to enforce ordinary append-only intake.

This is a maintainer-reviewed process, not a security attestation: the existing
workflow runs checker code from the PR head. Maintainers must review ledger,
checker, and workflow changes before merging; this adds no label bypass, API
approval check, token permission, or branch-protection setting.

Historical archived content is retained by this procedure. Removing a source
row neither deletes the data archive nor removes generated listings or Git
history, and does not guarantee that another discovery route cannot find the
source again. Archive deletion, re-import blocking, replacement validation,
and publishing require separate decisions and work. Never describe catalog
retirement alone as a completed takedown.
