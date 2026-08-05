---
name: craft-plugin-release
description: "Releasing Craft CMS plugins — tagging, Packagist propagation, GitHub releases, branch promotion. ALWAYS load when cutting, preparing, verifying, or debugging a plugin release: bumping a version, dating a changelog, creating or moving a git tag, editing a GitHub release, or checking what Packagist serves. Covers the composer.json version key (bump-or-omit trade-off, same-commit rule, verifying the tag's own blob), Packagist verification via repo.packagist.org/p2, the 'Skipped tag ... does not match version' silent failure, the tag recreation risk model (unserved tags safe to recreate, served tags never), GitHub release objects drifting from tags, gh api PATCH wiping tag_name to untagged-<hash>, releases/latest 404 when all releases are prereleases, drafts minting their tag from target_commitish at publish time, two-way origin branch comparison before promotion, and Composer path repositories for multi-plugin local dev (canonical semantics, no exclude on wildcards, extra.branch-alias, duplicate package names). Triggers on: cut/prepare a release, tag a version, bump the version, Packagist not serving the new version, 'Skipped tag', repo.packagist.org, packagist webhook, gh release create/edit, untagged- release, prerelease latest 404, target_commitish, draft release, promote develop to main, commits behind/ahead, path repository, branch-alias, dev-develop, symlinked plugin dependency. NOT for writing changelog entries, CI workflow YAML (craftcms skill quality.md), or plugin store listings."
---

# Releasing Craft Plugins

A plugin release involves three independent systems that all claim to describe the same version: **git tags**, **Packagist**, and **GitHub release objects**. They drift from each other silently, and every observable signal can say "success" while consumers get nothing. This skill is the checklist and risk model for keeping them in agreement.

**Core rule: verify what each system actually serves, not what you pushed to it.** A `202 Accepted` from the Packagist webhook, a green tag push, and a rendered releases page each prove nothing about the other two.

## Companion Skills

- **`craft-php-guidelines`** — `references/tooling.md` for commit conventions and composer hygiene of the plugin manifest itself.
- **`craftcms`** — `references/quality.md` for the CI workflows a release depends on (`code-analysis`, `create-release.yml`).
- **`craft-pest`** — the suite must be green from the plugin's own root before tagging.

## The release commit

If the plugin's `composer.json` carries a `version` key, **bumping it is a mandatory release step, in the same commit that dates the changelog.** A tag whose `composer.json` says a different version is silently useless: Packagist reads the manifest from the tag's own tree, sees the mismatch, and skips the tag —

```
Reading composer.json of acme/craft-thing (1.7.4)
Skipped tag 1.7.4, tag (1.7.4.0) does not match version (1.7.3.0) in composer.json
```

— while the GitHub webhook still returns `202 Accepted`. Nothing in the push, the tag, or the webhook response surfaces this. Consumers simply never see the version.

After tagging, verify against the **tag's own blob**, not the branch head:

```bash
git show 1.7.4:composer.json | grep '"version"'
```

The branch can be correct while the tag isn't (the bump landed one commit after the tag), and vice versa.

### The `version` key: bump it or omit it

Composer's schema documentation recommends **omitting** `version` for VCS-distributed packages — the tag is the version, and an explicit key is a drift risk that `composer validate` warns about. Both choices are legitimate; know the trade-off:

- **Omit it**: the entire class of skipped-tag failures disappears. But a version-less package loaded through a `path` repository resolves as `dev-<branch>`, and `version_compare("dev-develop-v5", "5.9.0", ">=")` is **false** — any peer-plugin version check silently fails, and the CP shows a branch name where a version should be. `extra.branch-alias` mitigates this (see `references/path-repositories.md`).
- **Keep it**: local path-repository development gets a real, comparable version. The cost is that every release must bump it, enforced by the same-commit rule and the tag-blob check above. A release script that edits changelog date + `version` together and refuses to tag on mismatch removes the human step.

Present this as a per-plugin decision, not a doctrine — but whichever way a repo goes, it must go all the way: a `version` key that exists and doesn't get bumped is strictly worse than either consistent choice.

## Verifying Packagist

**Check `https://repo.packagist.org/p2/<vendor>/<name>.json`** — the metadata endpoint Composer itself resolves from. Do **not** use `https://packagist.org/packages/<vendor>/<name>.json`; it is served from a staler pipeline and can show a version p2 doesn't have (or lack one it does).

```bash
curl -s https://repo.packagist.org/p2/acme/craft-thing.json | jq -r '.packages["acme/craft-thing"][].version'
```

Compare that list against `git tag --list` — every releasable tag should appear. A tag missing here with no error anywhere is the skipped-tag failure above; fetch the package's update log on packagist.org (or re-trigger the webhook and watch the response body) to see the skip reason.

### The tag risk model

- **Recreating a tag Packagist has never served is safe.** Nothing downstream has cached that version, so delete-and-repush (with the fixed manifest) is the standard remedy for a skipped tag.
- **Moving a tag Packagist HAS served breaks that version permanently.** Composer's metadata and dist archives are cached by reference; a moved served tag means checksum mismatches and split-brain installs. Ship a new patch version instead.

That distinction is the whole model. Before touching any existing tag, check p2 for whether the version was ever served.

## GitHub release objects are not tags

A GitHub *release* is a separate object that references a tag — and the two drift independently. Packagist reads **tags**; humans read the **releases page**. A repo can be tagged several versions past its newest release object, so the releases page lies while Packagist is correct. Verify both:

```bash
git ls-remote --tags origin | tail -5
gh release list --limit 5
```

Editing and publishing pitfalls, each observed in practice:

- **`gh api -X PATCH /repos/O/R/releases/<id>` with only a `body` field wipes `tag_name`** — the release becomes `untagged-<hash>`, silently unbound from its tag. Update notes with `gh release edit <tag> --notes-file <file>` instead, then re-verify `tag_name`, `draft`, `prerelease`, and `target_commitish` on the release object.
- **`gh api repos/O/R/releases/latest` returns 404 when every release is a prerelease** — that endpoint excludes prereleases and drafts by design. Not a bug; use `gh release list` instead of chasing it.
- **Publishing a draft release mints its tag from the tip of `target_commitish` at publish time.** Anything pushed to that branch between drafting and publishing lands in the release. Useful when intentional; a footgun when the branch moved. Pin the draft to a SHA, or verify the branch tip immediately before publishing.

## Branch promotion: never trust local refs

When deciding what to promote from a development branch to a release branch, stale local refs produce confidently wrong answers. Always:

```bash
git fetch --prune origin
git rev-list --left-right --count origin/develop...origin/main
```

Compare **origin against origin, in both directions**. A one-way "commits behind" count cannot distinguish *behind* from *diverged*, and cannot detect an *inverted* pair (release branch ahead of the dev branch) — both of which occur in real estates and both of which make a naive promotion destructive.

## Release verification checklist

1. Suite green from the plugin's own root; `check-cs` and `phpstan` pass.
2. Changelog dated and `composer.json` `version` bumped (if present) **in the same commit**.
3. Tag created; `git show <tag>:composer.json` shows the right version.
4. `repo.packagist.org/p2/<name>.json` lists the new version (allow a minute for the webhook).
5. GitHub release object exists, `tag_name` matches, `prerelease`/`draft` flags correct.
6. If promoting branches first: `git fetch --prune`, two-way `origin...origin` comparison, no unexplained divergence.

## Reference Files

| Task | Read |
|------|------|
| Multi-plugin local dev: path repositories, canonical semantics, branch aliases, duplicate package names | `references/path-repositories.md` |
