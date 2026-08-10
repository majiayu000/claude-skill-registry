---
name: research-git
description: "Scans public GitHub repos for agent skills, dev practices, and code patterns. Use when enriching skills, setting team policy, or researching a build domain."
compatibility: Claude Code + Codex. Runtime-agnostic; scripts require `gh` CLI + `jq`.
version: "1.1"
last_validated: 2026-07-11
---

# Repo Research

Scan public GitHub repos for **agent skills** (SKILL.md ecosystem), **dev practices** (git/PR/CI workflows from real teams), or **code patterns** (framework idioms, config layouts) — then merge validated insights into the local catalog with full attribution.

Manual extraction is unsustainable. The agent-skill ecosystem alone has 1,400+ repos as of April 2026, and that's before counting the repos worth scanning for their CI, testing, or i18n setups. This skill makes the scan repeatable and the merge auditable.

## Navigation

- [Quick Reference](#quick-reference) — entry-point table by need
- [Three Modes](#three-modes) — skill / practice / code targeting
- [When to Use](#when-to-use) and [When NOT to Use](#when-not-to-use)
- [Default Workflow](#default-workflow) — discover → triage → fetch → diff → merge
- [Output Contract](#output-contract) — per-mode scan report shape
- [references/discovery-protocol.md](references/discovery-protocol.md) — discovery commands and triage (includes velocity/dependency signals and beyond-GitHub hosts)
- [references/code-pattern-mining.md](references/code-pattern-mining.md) — Mode C extraction
- [references/attribution-rules.md](references/attribution-rules.md) — licensing
- [references/code-search-syntax.md](references/code-search-syntax.md) — GitHub Blackbird qualifiers, `gh search code` CLI, rate-limit strategy, example queries per mode
- [references/graphql-triage.md](references/graphql-triage.md) — single-repo health query, batch-alias pattern, repo discovery via `search` connection
- [references/signal-quality.md](references/signal-quality.md) — fake-star/astroturf detection: fork ratio, GH Archive spike queries, contributor account-age checks
- [references/git-history-forensics.md](references/git-history-forensics.md) — single-repo git-history verification: pickaxe `-S`/`-G`, `blame -w -C -M`, `bisect run`, `range-diff`, when `git log` lies
- [data/sources.json](data/sources.json) — registries, authors, hot lists, ecosystem analytics, cross-host registries

## Quick Reference

| Need | Mode | Entry point |
|------|------|-------------|
| Find SKILL.md repos for a domain | `skill` | `scripts/search_repos.sh --kind skill <domain>` |
| Find teams with strong git/CI practice to copy | `practice` | `scripts/search_repos.sh --kind practice <topic>` |
| Find framework idioms in high-signal OSS | `code` | `scripts/search_repos.sh --kind code <language>/<framework>` |
| Find OSS clones of a commercial product (killer-feature signal) | `killer-feature` | `scripts/search_repos.sh --kind killer-feature <commercial-product>` |
| Fetch assets from a known repo | any | `scripts/fetch_repo_assets.sh <owner>/<repo> <out> --kind <mode>` |
| Compare external to local equivalent | any | `scripts/diff_against_local.sh <external> <local>` |
| Verify a claimed practice/pattern against real git history (not just static files) | `practice`, `code` | [references/git-history-forensics.md](references/git-history-forensics.md) |
| License/attribution rules | any | [references/attribution-rules.md](references/attribution-rules.md) |
| Registries + high-signal authors | any | [data/sources.json](data/sources.json) |

## Four Modes

### Mode A — Skill Discovery

**Target**: repos containing `SKILL.md` + `references/` (the agent-skill ecosystem).
**Fetch**: SKILL.md, references/, optionally scripts/.
**Output**: research pack → feeds existing `software-*`, `data-*`, `ai-*`, `ops-*` skills in your catalog.
**Use when**: enriching an existing skill, or auditing what already exists before building one.

### Mode B — Practice Scan

**Target**: real production repos (not skill repos) with strong process signals.
**Fetch**: `.github/` (workflows, PR/issue templates, CODEOWNERS), `CONTRIBUTING.md`, `SECURITY.md`, release notes cadence, `docs/adr/` (architecture decisions).
**Output**: research pack → feeds `dev-git-workflow`, `qa-*`, `ops-*` skills.
**Use when**: redesigning team policy (branching, PR review, CI gates, release cadence) and you want evidence from real teams, not just framework docs.

### Mode C — Code Pattern Extraction

**Target**: high-signal OSS repos in a specific language/framework.
**Fetch**: configs (tsconfig, biome, eslint, ruff, cargo), representative source modules, test layouts, `scripts/` or `Makefile`.
**Output**: patterns → feeds `software-*` skills.
**Use when**: a local skill covers a domain where mature OSS implementations exist and the team's patterns are better than anything in docs (think: React Query's cache patterns, tRPC's type-safety tricks, Turborepo's build graph).

### Mode D — Killer-Feature Mining

**Target**: OSS clones of a specific commercial product (e.g., `supabase/supabase` clones Firebase, `plausible/analytics` clones Google Analytics).
**Fetch**: README.md, CHANGELOG.md, docs/, landing pages — the marketing surface that reveals which features the OSS author chose to replicate (and which they explicitly didn't).
**Output**: rows on the shared `pay-trigger-ledger.tsv` with `signal_type=oss_clone_focus` → contributes to the bundle's [Killer-Feature Convergence Protocol](../startup-review-mining/references/killer-feature-convergence.md) owned by `startup-review-mining`.
**Use when**: the bundle is hunting a killer feature for a commercial product, OR you want to know what the OSS world considers the load-bearing feature(s) of a category leader.
**Premise**: OSS authors only reimplement what they think matters. That choice is revealed preference under cost — a strong proxy for monetizable core.
**Reference**: [references/killer-feature-mining.md](references/killer-feature-mining.md) — full extraction protocol + LLM prompts.

## When to Use

- **Enriching a skill**: you have `software-ios-native` and want to steal what other operators learned
- **Pre-build audit**: you're about to author a new skill — has the work already been done?
- **Policy redesign**: your team's PR workflow is breaking — scan how 5 leading OSS repos handle it
- **Framework adoption**: you're committing to a new framework — pull idioms from the repos that stress-test it
- **Periodic refresh**: quarterly re-scan of a domain to catch new patterns from active maintainers
- **Bundle handoff — killer-feature scan**: `startup-review-mining` Killer-Feature Mode asks Mode D for the OSS clone signal on a target commercial product

## When NOT to Use

- Web articles, papers, blog posts → `ai-deep-research`
- Library/package selection or upgrade path → `dev-dependency-management`
- Cross-repo *code context* for your own portfolio → `dev-context-multi-repo`
- Per-commit message generation or commit-policy *implementation* → `dev-git-commit-message`
- Branching-model *design* in isolation (no evidence-gathering needed) → `dev-git-workflow`
- One-off lookup of a specific file → plain `WebFetch`
- Cloning to fork → plain `git clone`
- Validated Q&A answers or known-error solutions → the Stack Overflow corpus (community MCP or the emerging Stack Overflow for Agents exchange), via `qa-debugging` — not repo mining

## Default Workflow

### ASCII Flow

```text
public repo research request
  -> Choose mode: skill, practice, or code
  -> Check prior packs, cached raw extracts, and target sources.json
  -> Discover and shortlist 3-5 high-signal repos
  -> Fetch only mode-specific assets and pin source commit SHAs
  -> Diff external material against the local target
  -> Mine novel patterns and write an attributed research pack
  -> Wait for explicit approval before merging changes
```

### Phase 0 — Context Check (always run first)

Before fetching anything from GitHub:

1. **Prior research packs**: `ls docs/research/*-scan.md` — if a recent pack covers this domain + mode, read it first
2. **Cached extractions**: `ls docs/research/*/raw/<owner>__<repo>/` — if a repo was extracted in the last 30 days, reuse unless `HEAD` advanced
3. **Target skill's `data/sources.json`**: if a source is already tracked, compare its `commit_sha` to the current repo to decide refresh vs reuse
4. **Existing pack as Level 1 input** — only re-fetch the delta

Mirrors the [context-first protocol](../agents-subagents/references/context-first-protocol.md): use prepared artifacts before raw fetches.

### Phase 1–9 — Active Research

1. **Frame the goal**: "Enrich `software-ios-native` with novel patterns from the iOS skill ecosystem" *or* "Redesign release workflow using practices from 3 active monorepos" *or* "Improve React i18n patterns in `software-localisation`"
2. **Discover**: `scripts/search_repos.sh --kind <mode> <domain>` → ranked shortlist
3. **Triage**: pick 3–5 repos using signals in [references/discovery-protocol.md](references/discovery-protocol.md) — applies to all modes
4. **Extract** (only what's missing or stale): `scripts/fetch_repo_assets.sh <owner>/<repo> docs/research/<scan-id>/raw/ --kind <mode>`
5. **Diff**: `scripts/diff_against_local.sh docs/research/<scan-id>/raw/<repo>/ <target-local-skill>/`
6. **Mine insights**: follow mode-specific guidance
   - Mode A → [references/insight-mining.md](references/insight-mining.md)
   - Mode B → [references/practice-scan-targets.md](references/practice-scan-targets.md)
   - Mode C → [references/code-pattern-mining.md](references/code-pattern-mining.md)
   - Mode D → [references/killer-feature-mining.md](references/killer-feature-mining.md) (output appends to shared bundle ledger, not a local skill)
7. **Synthesize**: research pack at `docs/research/<scan-id>.md`
8. **User reviews**: present the pack, wait for approval on what to merge
9. **Apply** (opt-in): follow [references/apply-protocol.md](references/apply-protocol.md)

## Output Contract

Research pack at `docs/research/YYYY-MM-DD-<mode>-<domain>-scan.md`:

```markdown
# <Mode> Scan: <Domain> — <Date>

## Mode
skill | practice | code | killer-feature

## Sources Reviewed
| Repo | Stars | Last commit | License | Scorecard | Quality | Action |
|------|-------|-------------|---------|-----------|---------|--------|

## Insights Extracted
For each insight:
- Source: <repo URL + commit SHA>
- Mode: skill | practice | code
- Pattern: <name and 1-line description>
- Why it matters: <evidence from the source>
- Where it goes: <target skill + reference file>
- Novel vs local: <new / extends existing / duplicates existing>
- Confidence: <high / medium / low + rationale>

## Recommended Merges
| Pattern | Target skill | Action | Approved? |

## Skipped
<insights reviewed and rejected, with reason>

## Attribution Pack
<full source list with URLs, commit SHAs, licenses, extraction dates>
```

## Attribution Rules

Mandatory before any merge:
1. Check the source repo's LICENSE — MIT / Apache-2.0 / BSD / CC-BY-4.0 permit derived work with attribution
2. Never copy `SKILL.md`, reference files, or source files verbatim — extract patterns, rewrite in local voice
3. Cite source URL + commit SHA + extraction date + license on every merged insight
4. Add the source to the target skill's `data/sources.json`
5. Pin to commit SHA, never `main` — supply-chain drift is real

Full rules: [references/attribution-rules.md](references/attribution-rules.md)

## Patterns

| Pattern | Why it works |
|---------|--------------|
| Pin every fetch to commit SHA | Makes extractions reproducible; survives repo renames, branch deletions, force-pushes |
| Filter by OpenSSF Scorecard ≥ 5 (Mode B/C) | Strong proxy for maintenance quality; weeds out abandoned and risky repos |
| Require CODEOWNERS for practice-scan targets | Repos without ownership signals usually have ad-hoc process — nothing to steal |
| Shortlist to 3–5 repos, not 20 | Extraction is the bottleneck; wide scans dilute signal |
| Apply one skill at a time, one commit per skill | Makes merges reviewable and revertable |
| Always diff-against-local before extracting | Prevents duplication, surfaces real novelty |
| Re-scan quarterly (not weekly, not yearly) | Best-practice drift is slow; weekly scans pay cache costs without new signal |
| Verify high-value practice/pattern claims against real git history, not just static files | `CODEOWNERS`, `CONTRIBUTING.md`, and merge-queue config describe policy; `blame -w -C -M`, `range-diff`, and `bisect run` show whether it's actually followed — see [references/git-history-forensics.md](references/git-history-forensics.md) |

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| Auto-applying insights without user review | Merges stale or wrong patterns | Always present research pack first |
| Cloning entire repos by default | Wastes context; most value is in ≤10 files | Default to mode-specific asset list |
| Copying content verbatim | License violation + voice drift | Always rewrite in local voice |
| Extracting without diff-against-local | Duplicates content, creates contradictions | Always run diff first |
| Trusting stars alone | LLM-spam repos farm stars via mutual-follow networks | Cross-check commit signing, Scorecard, contributor count |
| Trusting LLM-generated awesome-lists | Many April-2026 awesome-lists are LLM-synthesized and list dead repos | Spot-check 3 random entries before using the list as a registry |
| Fetching `main` branch without pinning | Content drifts; citations become unverifiable | Always capture commit SHA, cite it |
| Scanning repos flagged as mirrors/vendors | Duplicates upstream; wastes triage time | Filter `fork=false`, `archived=false`, check for `mirror` in description |
| Treating topic `agent-skills` as a quality signal | Topic is now noisy (>5000 repos, ~60% stale or LLM-generated) | Prefer `claude-skills`, `codex-skills`, or author-curated lists |
| Research pack with no attribution | Cannot re-verify, breaks audit trail | Every insight gets source URL + commit SHA + license |
| Re-fetching repos extracted in the last 30 days | Wastes API quota + duplicates context | Phase 0: check `docs/research/*/raw/` first |
| Ignoring prior research packs | Loses prior synthesis, agents do duplicate analysis | Phase 0: read existing packs as Level 1 context input |

## Known Issues (July 2026)

| Issue | Impact | Workaround |
|-------|--------|------------|
| `gh api` rate limit: 5000 req/hr authenticated | Bulk scans of 50+ repos blow the budget | Batch, pause, or use GraphQL (single call, deeper data) for listings |
| GitHub **Search API** has its own much lower limits, **separate from** the 5,000/hr core budget — **9 req/min** for code search specifically, **30 req/min** for repo/issue/user search (verified against GitHub REST docs, 2026-07-11) | A code-search sweep (e.g. `path:.github/workflows`) throttles in well under a minute even with core budget free | Budget code search at ≤9 calls/min, general search at ≤30 calls/min; pause between pages; prefer one wide query + local filtering over many narrow ones; never parallelise code search — see [references/code-search-syntax.md](references/code-search-syntax.md) |
| GitHub still hosts only SHA-1 repos as of mid-2026 — Git itself has shipped experimental SHA-1/SHA-256 "compat" object-format support since 2.45, and Git 3.0 (targeted late 2026) defaults new repos to the `reftable` ref backend, but no major forge (GitHub, GitLab, Bitbucket) serves SHA-256 repos yet | Don't assume a scanned repo's local git internals (hash algo, ref backend) match what `git version` on your machine defaults to | Treat SHA-256/reftable claims about a *target* repo as forge-side metadata, not inferable from clone behavior; re-verify at git-scm.com/docs before citing a specific version's default |
| Papers with Code is dead (Meta shutdown Jul 2025) | Any inherited workflow that used PwC for reproducibility signal is broken | research-git **is** the replacement reproducibility-signal channel (repo/reimplementation inspection); do not add PwC back as a source |
| Topic `agent-skills` is noisy since late 2025 | ~60% of results are LLM-generated shells with no real content | Prefer `--owner` filter on known authors; cross-check with awesome-lists |
| LLM-generated SKILL.md repos are visually convincing | Wastes extraction budget on zero-signal content | Red flags: no commit history before 2025-09, single-author, uniform file sizes, no issues/PRs, description ends in "...for Claude" |
| GitHub Search skips archived repos inconsistently | Dead repos appear in ranked output | Always pass `archived:false` in `gh search`; double-check in triage |
| `gh search` star threshold sorts but doesn't filter | Stars<100 repos appear on page 2+ | Use `--limit 30 --sort stars` and truncate manually |
| Some high-signal repos use nested skill dirs (`skill/`, `<name>-pro/`) | Default fetch misses SKILL.md | Always recursive-tree lookup, not root-only |
| OpenSSF Scorecard not present for private-forked public repos | Can't use Scorecard signal | Fall back to CODEOWNERS + commit-signing ratio |
| `gh api` GraphQL tree recursion caps at ~100k entries | Huge monorepos return empty tree | For monorepos, fetch the specific subtree by path, not the whole repo |
| Attribution strings break when source repo is renamed | Links 404 | Pin commit SHA; GitHub resolves old-name URLs at the SHA but not at branch refs |

## Scenarios

### Scenario 1 — Skill Discovery (Mode A)

*Goal: enrich `software-kafka` with patterns from the agent-skill ecosystem.*

```bash
scripts/search_repos.sh --kind skill kafka
# → ranked shortlist: confluentinc/kafka-agent-skill, redpanda-data/skills, ...

# Triage: keep 3, drop LLM-generated candidates
scripts/fetch_repo_assets.sh confluentinc/kafka-agent-skill \
  docs/research/2026-04-23-skill-kafka/raw/ --kind skill

scripts/diff_against_local.sh \
  docs/research/2026-04-23-skill-kafka/raw/confluentinc__kafka-agent-skill/ \
  frameworks/shared-skills/skills/software-kafka/
# → diff shows 2 new reference files, 1 new quick-reference row

# Mine, synthesize, present research pack, apply with attribution
```

### Scenario 2 — Practice Scan (Mode B)

*Goal: redesign the team's PR workflow; harvest practices from 3 active monorepos.*

```bash
scripts/search_repos.sh --kind practice monorepo
# → vercel/next.js, microsoft/vscode, nrwl/nx

scripts/fetch_repo_assets.sh vercel/next.js \
  docs/research/2026-04-23-practice-pr/raw/ --kind practice
# fetches .github/workflows/, CONTRIBUTING.md, CODEOWNERS, PR template, release-please config

# Mine via practice-scan-targets.md rubric: merge queue config, required checks,
# auto-assignment rules, review SLA signals

# Output feeds dev-git-workflow, not this skill
```

### Scenario 4 — Killer-Feature Mining (Mode D)

*Goal: contribute the OSS clone signal to the bundle's killer-feature hunt for Firebase.*

```bash
scripts/search_repos.sh --kind killer-feature firebase
# → supabase/supabase, appwrite/appwrite, nhost/nhost, pocketbase/pocketbase

# Triage: keep 3 with distinct owners; reject any that ship a paid hosted tier
# (their feature choices are biased by what they want to monetize)

scripts/fetch_repo_assets.sh supabase/supabase \
  docs/research/2026-05-26-killer-feature-firebase/raw/ --kind killer-feature
# fetches README, CHANGELOG, docs/, website/, package.json

# Feed README + landing pages to LLM prompt §1 in references/killer-feature-mining.md
# → JSONL of replicated features with monetization framing

# Feed "Limitations vs Firebase" section to LLM prompt §2
# → JSONL of explicitly-omitted features (inverse signal — these are the
#   parts of Firebase that OSS authors think aren't paid for)

# Append rows to ../startup-review-mining/assets/pay-trigger-ledger.tsv
#   signal_type = oss_clone_focus
# Run ../startup-review-mining/scripts/converge_killer_features.py
# Convergence Rule decides which feature_ids cross the 3-of-6 threshold
```

### Scenario 3 — Code Pattern Extraction (Mode C)

*Goal: improve `software-localisation` with real React i18n patterns.*

```bash
scripts/search_repos.sh --kind code react i18n
# → lingui-js/js-lingui, formatjs/formatjs, i18next/i18next

scripts/fetch_repo_assets.sh lingui-js/js-lingui \
  docs/research/2026-04-23-code-react-i18n/raw/ --kind code
# fetches: package.json, tsconfig, representative source modules, test layout

# Mine via code-pattern-mining.md: ICU plurals handling, runtime vs build-time,
# type-safe message catalogs

# Output feeds software-localisation
```

## Resources

**Workflow references:**
- [references/discovery-protocol.md](references/discovery-protocol.md) — finding repos via `gh` CLI + awesome lists (all modes); velocity/dependency signals; beyond-GitHub hosts
- [references/code-search-syntax.md](references/code-search-syntax.md) — Blackbird qualifiers, `gh search code`, rate-limit budget, example queries for Modes A/B/C
- [references/graphql-triage.md](references/graphql-triage.md) — single-repo health query, batch-alias for 5-10 repos, `search` connection for discovery
- [references/signal-quality.md](references/signal-quality.md) — fake-star detection: fork ratio, GH Archive spike query, contributor account-age, issue/star floor
- [references/git-history-forensics.md](references/git-history-forensics.md) — verify practice/pattern claims against real git history: pickaxe `-S`/`-G`, `blame -w -C -M --ignore-revs-file`, `bisect run`, `range-diff`, when `git log` lies
- [references/extraction-protocol.md](references/extraction-protocol.md) — fetching assets without cloning
- [references/insight-mining.md](references/insight-mining.md) — Mode A (skills) mining rubric
- [references/practice-scan-targets.md](references/practice-scan-targets.md) — Mode B (practices) mining rubric
- [references/code-pattern-mining.md](references/code-pattern-mining.md) — Mode C (code) mining rubric
- [references/killer-feature-mining.md](references/killer-feature-mining.md) — Mode D (oss_clone_focus signal) mining rubric + LLM prompts
- [references/attribution-rules.md](references/attribution-rules.md) — license compliance + citation format
- [references/apply-protocol.md](references/apply-protocol.md) — merging insights into target skills
- [references/claude-code-ecosystem-catalog.md](references/claude-code-ecosystem-catalog.md) — seed list of high-signal Claude Code / coding-agent repos for scan input

**Scripts:**
- [scripts/search_repos.sh](scripts/search_repos.sh) — `gh` CLI wrapper, mode-aware
- [scripts/fetch_repo_assets.sh](scripts/fetch_repo_assets.sh) — mode-aware asset fetcher
- [scripts/diff_against_local.sh](scripts/diff_against_local.sh) — compare external vs local

**Sources:**
- [data/sources.json](data/sources.json) — registries, high-signal authors, per-mode targets

## Related Skills

- [../ai-deep-research/SKILL.md](../ai-deep-research/SKILL.md) — web/paper research (this skill is repo research)
- [../dev-context-multi-repo/SKILL.md](../dev-context-multi-repo/SKILL.md) — code context across your own repos (this skill is external-repo pattern extraction)
- [../dev-dependency-management/SKILL.md](../dev-dependency-management/SKILL.md) — library/package selection (this skill is pattern extraction)
- [../dev-git-workflow/SKILL.md](../dev-git-workflow/SKILL.md) — target consumer of Mode B output
- [../dev-git-commit-message/SKILL.md](../dev-git-commit-message/SKILL.md) — per-commit message generation (disjoint scope)
- [../agents-skills/SKILL.md](../agents-skills/SKILL.md) — authoring your own skills (this skill enriches them)

## Fact-Checking

Verify repo activity, license, and Scorecard against current GitHub before citing findings. Repo research drifts fast — re-check before merging insights. Always confirm the repo is not LLM-generated (commit history, issue activity, real contributors) before trusting any pattern from it.

GitHub API rate limits and git-version facts cited in this skill (Known Issues table, [references/code-search-syntax.md](references/code-search-syntax.md), [references/git-history-forensics.md](references/git-history-forensics.md)) were verified against docs.github.com and git-scm.com on 2026-07-11 — re-verify at those sources before citing a specific number or version in a research pack, since both move faster than this skill's revision cadence.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
