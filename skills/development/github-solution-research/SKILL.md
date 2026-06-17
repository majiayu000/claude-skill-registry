---
name: github-solution-research
description: Use when a concrete engineering problem, bug, integration failure, dependency issue, unclear API usage, implementation blocker, or tool/capability need may already have a proven solution in GitHub open-source projects, issues, pull requests, discussions, code, examples, or release notes. Use it to find suitable repositories, report project basics including Stars when a repo-level solution applies, and adapt the existing solution with minimal local changes.
---

# GitHub Solution Research

Use GitHub as problem-solving evidence and an implementation source. The goal is to find open-source projects and GitHub evidence that already solve the user's specific engineering problem, report the relevant project information, then translate the existing solution into a local fix, implementation path, or verification plan.

This skill is for concrete problems first. For general tool or architecture selection, use it only after the local goal has been framed as a specific capability, blocker, workflow, or integration need.

## When to Use

- Runtime, build, test, deploy, package, SDK, API, dependency, framework, or integration errors.
- A feature implementation is blocked by an unclear edge case, missing usage pattern, or uncertain API behavior.
- A local issue resembles something that maintainers or other open-source users may have resolved in issues, PRs, examples, code, or release notes.
- The user asks whether GitHub/open-source projects can solve the same problem.
- Mature implementation examples or reusable projects would reduce uncertainty for one concrete capability.
- The answer should compare suitable GitHub repositories and explain how to use one with local adaptation.

Do not use for tiny edits, copy changes, local-only refactors where the codebase already dictates the answer, or requests that explicitly forbid web/GitHub research. Do not inspect private repositories unless the user explicitly scopes and authorizes that access.

## Default Workflow

1. **Frame the problem locally first.** Capture the goal, actual symptom, error signature, reproduction path, versions, runtime, dependency/framework names, recent changes, constraints, and attempted fixes. If a discoverable fact is missing, inspect local files/logs before asking.
2. **Choose the evidence mode.** For errors/regressions, search issues, PRs, releases, and code first. For capability or tool needs, search repository candidates first. For feature implementation, use both repository candidates and issue/PR/code evidence.
3. **Evaluate subagent usefulness.** Before substantial GitHub research, decide whether conditional subagent work would improve breadth, evidence quality, or review coverage. If not using subagents, state the reason briefly when reporting the search path.
4. **Create targeted searches.** Prefer exact error text, package/API names, version numbers, framework + symptom, file names, config keys, stack trace fragments, failing command names, or capability + framework/runtime/API names.
5. **Find suitable GitHub projects when relevant.** Prefer high-fit, high-Star, active, non-archived repositories with clear licenses and real examples. Lower the Star threshold when the high-Star set is too broad or misses the exact problem.
6. **Search GitHub evidence surfaces.** Use issues, PRs, discussions, code, examples, release notes, and official project docs within relevant open-source repos. Repository search is required when a project itself may solve the problem.
7. **Rank by problem fit first, with Stars as a strong maturity signal.** A high-Star repository is a strong candidate for inspection, but maintainer-confirmed issues, merged PRs, released fixes, official examples, and exact matching code beat popular adjacent projects. Use [research-rubric.md](references/research-rubric.md) when ranking matters.
8. **Deep-read the strongest projects and evidence.** Use [extraction-playbook.md](references/extraction-playbook.md) to extract project basics, reusable surfaces, root cause or implementation pattern, version constraints, risks, adaptation boundaries, and verification steps.
9. **Translate to local work with minimal adaptation.** Prefer the existing GitHub solution's public workflow, API, or architecture. Adapt only the parts required by the user's local interfaces, configuration, data/auth model, deployment target, or language/runtime.
10. **If evidence is weak, say so.** Do not stretch weak matches into a confident recommendation. Mark the recommendation as first-principles or local-only when GitHub evidence is insufficient.

## Subagent / Parallel Research Guidance

Subagents are conditional research aids, not a default requirement. The controller remains responsible for problem framing, scope control, evidence ranking, local adaptation, and final verification.

Use subagents when at least one of these applies:

- The problem spans 2+ independent ecosystems, frameworks, languages, tools, deployment surfaces, or GitHub communities.
- Repository discovery needs broad candidate coverage across multiple query families.
- Issue, PR, discussion, code, release, and example evidence can be split cleanly by project, version, or search surface.
- A final recommendation benefits from independent evidence review, risk review, or candidate rejection review.

Do not use subagents when any of these applies:

- The task is a narrow error with one obvious package, repository, API, or maintainer surface.
- Local repository context, logs, config, or reproduction details must be understood before external research can be scoped safely.
- GitHub rate limits, authorization boundaries, private repositories, secrets, production data, or sensitive logs would make delegation risky.
- Subagents would mostly duplicate the same searches or edit the same local files.

When using subagents, the controller must:

- Define each subagent's query family, repository scope, evidence surface, constraints, allowed write scope, and expected output.
- Require direct links, verified metadata, problem-fit rationale, risk notes, and explicit rejection reasons.
- Keep subagents read-only unless a separate implementation phase has a narrow allowed write scope.
- Merge and deduplicate results before ranking; do not count repeated reports of the same issue, PR, code path, or repository as independent evidence.
- Directly verify the strongest claims with `gh`, source reads, tests, logs, real requests, or official docs before finalizing.

## GitHub CLI First

Use the GitHub CLI (`gh`) as the default search and inspection surface. Prefer `gh search repos`, `gh search issues`, `gh search prs`, `gh search code`, `gh repo view`, `gh issue view`, `gh pr view`, and `gh api` before browser scraping or custom scripts. Do not add or rely on bundled search scripts for this skill.

Use these short command templates as starting points, then adjust the query, repo, fields, and limits to the local problem:

```bash
gh search repos "<query>" --archived=false --sort stars --order desc --limit 10 --json fullName,url,description,stargazersCount,forksCount,language,license,pushedAt,isArchived,openIssuesCount
gh search issues "<query>" --repo owner/repo --sort updated --order desc --limit 10 --json title,url,state,updatedAt,commentsCount,repository,body
gh search prs "<query>" --repo owner/repo --merged --sort updated --order desc --limit 10 --json title,url,state,updatedAt,commentsCount,repository,body
gh search code "<query>" --repo owner/repo --limit 10 --json path,url,repository,sha
gh repo view owner/repo --json nameWithOwner,url,description,stargazerCount,forkCount,licenseInfo,primaryLanguage,pushedAt,repositoryTopics,homepageUrl
gh api -X GET search/repositories -f q='<query> archived:false' -f sort=stars -f order=desc
```

Only run `gh auth status` when a command fails with 403, 429, a private repository authorization error, or an explicit `gh` not-authenticated message. If GitHub returns 403/429, inspect the emitted rate-limit or authorization context before retrying, reducing breadth, or switching endpoints. Do not paste or persist tokens, cookies, private repository contents, or credentials in prompts, files, logs, or memory.

## Search Strategy

- Start narrow: exact error string, exception class, CLI output, package + method name, config key, or stack trace fragment.
- Add constraints: package/framework version, language, platform, deployment target, bundler, database, auth provider, or runtime.
- Search surfaces in this order when relevant: issues/PRs/discussions, merged fixes, release notes/changelog, examples/templates, source code, then repository-level candidates.
- For implementation blockers without an error, search for the desired capability plus framework/runtime/API names.
- For public platform data needs such as trends, hot lists, topic search, or engagement metrics, do not start with visual browser scraping. First look for reusable public endpoints, open-source crawlers, archived datasets, and API field evidence; then verify the chosen source with a minimal real request and clearly separate anonymous hot-list data from logged-in search/topic data.
- For reusable project discovery, search repositories sorted by Stars, then deep-read only candidates that match the local problem. Record Stars, forks, language, license, activity, and basic content.
- Demote matches that are old, version-mismatched, archived, unresolved, speculative, or based only on user guesses.
- Use Stars/forks only as supporting maturity context and tie-breakers among similarly fitting repositories. They do not override problem fit, maintainer-confirmed evidence, merged PRs, release notes, official examples, or reproducible code.
- For security, auth, payments, infrastructure, or production operations, cross-check open-source findings against current official docs or repositories when facts may have changed.

## Evidence Standard

For each serious evidence item, identify:

- exact match: same error, behavior, API, version, environment, or workflow;
- evidence strength: maintainer confirmation, merged PR, released fix, reproducible code example, test fixture, or repeated independent reports;
- applicability: what conditions must match locally for the solution to apply;
- implementation value: patch, config, API usage, dependency version, workflow, test, or operational pattern worth adapting;
- project basics when a repository is a candidate: name, URL, Stars, forks, language, license, activity, basic content, fit rationale, and adaptation cost;
- risk: stale version, unresolved issue, unsafe workaround, license concern, security/privacy impact, deployment mismatch, or overbroad change.

## Output Contract

When this skill materially affects the answer, include:

- local problem profile: goal, symptom/error, versions/environment, and local constraints;
- search path: queries or discovery methods used, GitHub surfaces searched, and whether subagents were used or skipped;
- subagent trace when subagents were used: each subagent's scope, evidence surfaces, key findings, rejected candidates, deduplication results, and which claims the controller directly verified;
- project candidates when a GitHub project itself is relevant: repo link, Stars, forks, language, license, activity, basic content, match rationale, and how it can be used locally;
- key evidence: links to issues, PRs, code, examples, releases, or repos, with match rationale;
- recommended solution: what to reuse directly, what to adapt locally, what to avoid copying, and why it fits;
- rejected or risky options: why they do not apply or need caution;
- verification standard: test, build, reproduction command, real request, or manual check required to confirm the fix;
- confidence label when evidence is weak or no strong GitHub solution was found.

When repository-level solutions are relevant, include a compact project table. For pure issue/PR/code fixes, the table is optional, but include repository context if it affects trust or applicability.

Do not answer with only links, Stars, or popularity rankings. Do not write "common GitHub pattern" without linked evidence. Do not let external examples override local constraints.

For website, SaaS, landing-page, theme, or frontend-template candidate research, include both the repository URL and the live preview/demo URL for every serious candidate. If no preview is available or verified, state that explicitly and downgrade the candidate.

## Safety Boundaries

- Prefer reading patterns and reusing existing public interfaces over copying code. If code reuse is necessary, check the license and keep attribution/obligation risks visible.
- Avoid large rewrites of an existing GitHub solution. Keep its proven flow intact and make only the local adaptations required for the user's problem.
- Avoid large verbatim excerpts from repositories, READMEs, issues, PRs, or documentation.
- Do not save GitHub tokens, cookies, private repository contents, or credentials in outputs, logs, skills, or memory.
- Do not pass tokens, cookies, private repository contents, sensitive logs, secrets, production data, or credentials to subagents.
- If network access is unavailable, state that GitHub research could not be performed and mark the recommendation as local-only.
