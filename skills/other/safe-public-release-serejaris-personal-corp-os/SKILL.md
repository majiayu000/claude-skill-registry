---
name: safe-public-release
description: >-
  Use when publishing, open-sourcing, exporting, sanitizing, or moving code,
  agent skills, prompts, templates, fixtures, datasets, workshop assets, or
  other artifacts from a private repository, vendor/runtime environment, or
  mixed working directory into a public repository or registry. Builds a
  provenance inventory, license/security review, explicit allowlist, clean
  staging package, approval dry run, and fresh public clone/install smoke.
  Triggers on "open source this", "publish these skills", "make this repo
  public", "export and sanitize", "подготовь публичный релиз", "выложи
  скиллы", "опенсорсни", "санитизируй и опубликуй". NOT for ordinary
  upstream bugfix PRs, vulnerability disclosure, or creating a corp-* department.
---

# Safe Public Release

Turn a private, vendor-provided, runtime-generated, or mixed artifact into a public package without leaking secrets, private state, or material that cannot be redistributed.

One pipeline:

`intent → owner issue tree → inventory → provenance → license → security/privacy → allowlist → clean package → approval → publish → fresh public verification → maintenance`

The skill is **allowlist-first**. Never copy a whole runtime/private directory and hope denylist cleanup finds everything.

## Hard safety boundary

Publishing is an outward mutation. Before creating a public repository, changing visibility, pushing a release, or publishing to a registry:

1. complete the inventory and release manifest;
2. reach `PACKAGE-READY` with no unresolved provenance/license/security blockers;
3. show the user the release dry run;
4. receive explicit approval for the named public target and artifact set.

A request to "prepare" or "review" a release authorizes read-only analysis and private/internal artifacts, not public publication.

## What this skill is for

- public agent skills or plugin bundles;
- prompts, templates, playbooks, starter kits, examples;
- reusable source extracted from a private project;
- workshop/course assets selected for public release;
- benchmark fixtures or datasets;
- demo repos derived from production/private work;
- vendor/runtime exports with uncertain provenance;
- moving an existing private repo or selected subtree to a public repo.

## What this skill is NOT for

- **Upstream bugfix PR:** use the repository's contribution/PR workflow and regression tests.
- **Security vulnerability disclosure:** use the vendor's private security route.
- **Tool/product evaluation:** route to the product/runtime owner; evaluation does not grant redistribution rights.
- **Creating a private corp-* department:** use `corp-new`; it requires a separate approval dry run.
- **Simple public edit:** when the source is already public, owner-authored, clearly licensed, and contains no mixed private/runtime state, use the normal repository workflow.

## Setup

Resolve configuration from the user, project instructions, then defaults:

```markdown
## Safe Public Release Config

- internal_owner_repo: owner/corp-opensource-or-project
- public_github_owner: owner
- staging_root: /tmp/safe-public-release
- allowed_public_licenses: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause
- secret_scanners: gitleaks, trufflehog
- approval_mode: explicit-before-publish
```

Do not block preparation when optional scanners are unavailable. Record the limitation and keep the release blocked until equivalent manual and repository-native checks are completed. Never claim a scan ran when it did not.

## Owner issue tree

Before extraction or packaging, find or create three scopes in the internal owner repo:

1. **Owner epic** — intended release, audience, source, risk owner, definition of done.
2. **Inventory/review child** — provenance, licenses, companion files, security classification, allowlist.
3. **Publish/verify child** — public repo/package creation after approval, fresh-clone verification, maintenance.

Separate unrelated work:

- product/tool smoke → product/runtime owner;
- runner or CI provisioning → infrastructure owner;
- launch content/distribution → media/community owner;
- commercial negotiation → sales/CRM owner.

If the user has an issue-management skill such as `manager`, use it for the issue tree and cross-repo links.

## Status model

Use exactly one current status:

### Progress states

- `DISCOVERED`
- `INVENTORY`
- `PROVENANCE-CLEARED`
- `LICENSE-CLEARED`
- `SECURITY-CLEARED`
- `PACKAGE-READY`
- `APPROVED`
- `PUBLISHED`
- `VERIFIED`
- `MAINTAINED`

### Block states

- `BLOCKED-PROVENANCE`
- `BLOCKED-LICENSE`
- `BLOCKED-SECURITY`
- `BLOCKED-OWNER-APPROVAL`
- `NO-GO-VENDOR-PROTECTED`
- `NO-GO-MIXED-PRIVATE-DATA`

Every blocked status needs one concrete `unblock_event`: source found, written permission, license clarified, secret removed and rotated, scope reduced, or owner approval.

## Step 1 — Capture the release intent

Record:

- intended public artifact/repository;
- target audience and use case;
- source environments/repositories/providers;
- expected bundles;
- intended public license;
- owner who can approve publication;
- maintenance owner after publication.

Do not create the public repository yet.

## Step 2 — Inventory before copying

Create `release-manifest.yaml` using [the bundled template](references/release-manifest.example.yaml).

For each candidate artifact record:

- stable artifact ID;
- source provider/owner;
- source version, tag, commit, or product version;
- source locator in an **internal** note; public manifest must not contain private absolute paths or internal URLs;
- original license/terms;
- redistribution basis;
- whether it was modified and how;
- complete companion-file bundle;
- exclusions and reason;
- current decision.

Visibility inside an application or runtime does not prove ownership or permission to redistribute.

## Step 3 — Classify every file

| Class | Default decision |
|---|---|
| Owner-authored source | Candidate after license/security review |
| Third-party redistributable source | Candidate with preserved notices |
| Generated build artifact | Regenerate from allowlisted source |
| Runtime state, cache, queue, session | Exclude |
| Logs, transcripts, histories | Exclude or separate privacy review |
| Credentials, tokens, cookies, keys | Exclude; rotate if exposed |
| Customer, student, employee, user data | Exclude; aggregate only under a separate privacy owner |
| Vendor-protected or unknown source | Block |
| Mixed bundle | Split before review |
| Symlink, submodule, archive, binary | Inspect target/content and license before allowlist |

Every file in the future public tree must be reachable from an explicit allowlist entry.

## Step 4 — Provenance gate

For each candidate prove:

- who authored/owns it;
- which exact version is being released;
- where companion files come from;
- what modifications were made;
- which public license will apply;
- why redistribution is permitted.

Unknown provenance → `BLOCKED-PROVENANCE`.

Do not publish a "cleaned up" artifact whose origin cannot be explained.

## Step 5 — License gate

Check:

- root and per-file licenses/notices;
- dependency and embedded asset licenses;
- generated-output terms;
- trademark/name restrictions;
- copyleft/share-alike obligations;
- redistribution/extraction restrictions;
- compatibility between source license and intended public license.

Attribution is not permission. A missing, custom, or unclear license means `BLOCKED-LICENSE` until the artifact is excluded or permission is obtained.

The skill does not provide legal advice. When license interpretation changes material risk, record the evidence and route the decision to the appropriate owner or counsel.

## Step 6 — Security and privacy gate

Exclude at minimum:

- `.env*`, API keys, OAuth state, cookies, credentials;
- SSH/private keys, certificates, signing material;
- logs, queues, caches, sessions, histories;
- browser profiles/local storage;
- private/customer/student/user data;
- private absolute paths, internal hostnames, private repo/document links;
- internal issue IDs when they expose confidential structure;
- vendor binaries/assets without redistribution rights;
- hidden files, archives, symlink targets not explicitly reviewed.

Run checks on the **clean staging tree**, not only the source directory:

```bash
find . -type l -print
find . -type f -size +10M -print
rg -n --hidden -S '(api[_-]?key|secret|token|password|BEGIN [A-Z ]*PRIVATE KEY|Authorization: Bearer)' .
rg -n --hidden -S '(/Users/|/home/|C:\\Users\\|private-|corp-|localhost:[0-9]{2,5})' .
git diff --check
```

When approved tools are available:

```bash
gitleaks detect --no-git --source .
trufflehog filesystem --no-update .
```

A scanner passing does not replace manual review. A live secret finding stops the release: remove it, rotate it, document internally, rerun all relevant checks.

## Step 7 — Build an explicit allowlist

Never copy the whole source tree first.

1. Derive `allowlist.txt` from the reviewed manifest.
2. Include whole functional bundles: main file, references, examples, scripts, required notices.
3. Regenerate generated files from allowlisted source when possible.
4. Copy into a new clean staging directory.
5. Compare the complete staged file list with the manifest.

Example:

```bash
rm -rf "$STAGING_ROOT/package"
mkdir -p "$STAGING_ROOT/package"
rsync -a --files-from=allowlist.txt SOURCE_ROOT/ "$STAGING_ROOT/package/"
cd "$STAGING_ROOT/package"
find . -type f -print | sort
```

Orphaning a `SKILL.md` from its references/scripts is a failed package, even when the main file is safe.

## Step 8 — Documentation gate

The package must contain or link to:

- human-readable `README.md`;
- install/use/verification command;
- source attribution and preserved notices;
- public license;
- security contact;
- compatibility/version information;
- known limitations;
- maintenance owner and update policy.

Do not claim compatibility that the public smoke test has not verified.

## Step 9 — Release dry run

Use [the bundled checklist](references/release-checklist.md). Show the user:

```text
Release: <name>
Target: <public owner/repo or registry>
Allowed artifacts: <count and short list>
Blocked/excluded artifacts: <count and reasons>
Source licenses: <summary>
Security/privacy checks actually run: <commands and results>
Fresh-clone verification plan: <command>
Maintenance owner: <owner>
Open risks: <none or list>
Proposed outward action: create repo | change visibility | push | publish package
```

Stop and request explicit approval. Continue only for the exact target and artifact set approved.

## Step 10 — Publish from the clean package

After approval:

1. create/update the public repository or registry package from the staging tree;
2. preserve public history; never force-push unrelated work;
3. include the public license and notices;
4. link the internal owner issue in the commit trailer when appropriate: `refs owner/repo#N`;
5. verify visibility, default branch, public URL, and release metadata;
6. never copy private issue bodies/comments into the public repository.

If the public target is different from the approved dry run, stop and re-approve.

## Step 11 — Verify the public boundary

Test as an external user from a fresh directory:

```bash
workdir=$(mktemp -d)
git clone --depth 1 https://github.com/OWNER/REPO.git "$workdir/repo"
cd "$workdir/repo"
```

Run the documented public command:

- skill/plugin discovery;
- package install/import;
- CLI `--help` or bounded smoke;
- example/test fixture;
- public read/link access without authentication.

Repeat the relevant secret/private-path scans on the fresh clone. `PUBLISHED` becomes `VERIFIED` only after this passes.

## Step 12 — Record evidence and maintenance

Write a release evidence card in the internal owner issue:

```text
release_status: VERIFIED
public_url: https://github.com/OWNER/REPO
source_version: ...
manifest: release-manifest.yaml
license_basis: ...
security_checks: ...
publication_commit: ...
fresh_clone_command: ...
fresh_clone_result: PASS
maintenance_owner: ...
next_review: YYYY-MM-DD
```

After every release or blocked decision, add the new failure mode or rule to this skill or its references.

## Failure without the skill → rule

| Failure | Rule |
|---|---|
| Runtime folder copied wholesale | Allowlist-first clean staging |
| Attribution added, license still unknown | Attribution is not permission; block |
| Main skill copied without references/scripts | Release the complete functional bundle |
| Secret scan green, private path leaked | Manual classification plus private-path scan |
| Works in owner checkout, fails after clone | Fresh public-boundary smoke is mandatory |
| Evaluation mixed with redistribution | Separate issues and risk owners |
| Public repo created before inventory | No outward mutation before `PACKAGE-READY` and approval |
| Vendor asset visible in UI/runtime | Visibility does not imply redistribution rights |
| Release published with no owner | Maintenance owner and next review are required |

## Final response

Report only verified facts:

```text
Prepared: <artifact/release>
Status: <state>
Public action: published | not published
Target: <URL or planned target>
Allowed: <count>
Blocked/excluded: <count + reasons>
Checks run: <summary>
Fresh public verification: PASS | NOT RUN | FAILED
Owner issue: <reference>
Next gate: <one concrete action>
```
