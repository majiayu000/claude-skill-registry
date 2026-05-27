---
name: build-deploy-and-tooling
description: Use when writing, reviewing, or changing build scripts, CI workflows, deploy pipelines, repo setup, or evaluating a new tool/dependency
---

# Build, Deploy and Tooling

## Overview

Build scripts, CI pipelines, deploy jobs, and tooling choices are part of the codebase. **Own the build as code. Build one artifact and promote it. Deploy from day one. Choose tools that fit the project, not the resume. Automate everything you do twice.** This skill enforces the decisions to make whenever you touch infrastructure or evaluate a tool.

This is a **rigid** skill. Run the checklist in order. If you can't satisfy a step, stop and tell the user what's blocking you.

These checks matter most when shaping a release artifact — production deploy, shared CI pipeline, tool adoption that other contributors will inherit. In MVPs, prototypes, internal dev tools, and one-off scripts where the architecture is not yet settled, prefer the simplest thing that works.

## When to invoke

Invoke when you're about to:

- Write or modify a build script, `Makefile`, `package.json` script, `Dockerfile`, or build configuration
- Change a CI workflow (`.github/workflows/*`, `.gitlab-ci.yml`, Jenkinsfile, etc.)
- Author or change a deploy pipeline, release script, or environment promotion job
- Add a new dependency, framework, linter, formatter, or developer tool to the project
- Set up a new repository, devcontainer, or onboarding script
- Add a new repeated manual step to anyone's workflow (a candidate for automation)
- Configure a bug tracker, issue template, or defect-triage workflow
- Write or change an installer, a "getting started" page, or a `README` quick-start
- Review CI config, deploy pipelines, build scripts, or tooling choices

### Non-triggers — do NOT invoke for

- Running the existing test suite or build (`npm test`, `make`, `docker build` on an unchanged config)
- Tailing a log file or reading CI output to diagnose a failure
- Asking "what does this Makefile target do?" — read it; no design decision is being made
- Using a linter, formatter, or tool the repo already mandates with its current configuration
- Bumping a single dependency patch version because of a security advisory
- Editing a deployed service's runtime configuration through the platform's normal config interface
- An early-stage MVP or prototype where the architecture is still in flux
- An internal dev tool or one-off script whose build needs are "run this command"
- Throwaway code expected to be replaced before reaching users

If you're not sure whether a change counts as "authoring infrastructure," **invoke anyway** — the checklist is short and skipping it produces build scripts nobody understands.

## Build/deploy/tooling checklist

Run every step in order. The sub-area headings group related principles; the numbered items run end-to-end.

### Version control

1. **Put everything the project needs into version control before anything else.** Source, build scripts, CI configuration, `Dockerfile`, infrastructure-as-code, fixtures, sample data, generated-docs config, design notes, the README itself. A new contributor's setup should be a single clone plus running the documented bootstrap script — no "copy this file from Slack." Each commit should isolate one logical change, carry a message that explains the *why*, and not break the build. *(Spinellis, 97/68.)*

### Builds

2. **The dev team owns the build as code, and refactors it.** Build scripts are not someone else's problem or a configuration file beneath your attention — they decide what the executable artifact actually is, define the component boundaries, and gate every change on the way to production. Treat them with the same discipline you apply to source: name the targets clearly, factor out duplication, delete dead branches, document non-obvious steps. A build that takes a new contributor a day to get green is a bug. *(Berczuk, 97/63.)*
3. **Build one immutable artifact and promote *that* through every environment.** The deployable artifact (container image, JAR, binary, bundle) is built once from a tagged commit. The same bytes flow through dev, staging, and prod. Environment-specific values — endpoints, credentials, feature flags — live in the environment (container env vars, config service, mounted file), never baked into the image. If the build rewrites code per environment, you cannot prove that what shipped to prod is what staging tested. *(Freeman, 97/61.)*

### Deploy

4. **Deploy to a realistic clean environment from week one, and refactor the deploy process like code.** Hand-crafted demo environments hide the assumptions your code makes about a developer's laptop. The first deployment should happen before there is anything interesting to deploy, so the pipeline matures alongside the application. Each environment promotion uses the same artifact from step 3 with a different config bundle. When the deploy is painful, treat the pain as a defect — change the deploy script, change the code that complicates it, do not normalize the workaround. *(Berczuk, 97/20; promotion model from Freeman, 97/61.)*

### Tooling choice

5. **Respect the project's existing tool conventions before recommending a new one.** If the repo already uses a linter, a test runner, a build system, a deployment target — that is the convention until the team agrees otherwise. Adding a parallel tool because you prefer it doubles maintenance and fragments contributor knowledge. When you do propose a new tool, evaluate the real costs: architectural fit with the existing stack, upgrade lifecycle and how it interacts with the other tools' upgrade cycles, configuration burden, license compatibility, lock-in risk, and whether "free" hides a paid support tier you will eventually need. Start with the smallest set that works; isolate each external tool behind an internal interface so it can be swapped later with bounded pain. *(Asproni, 97/10.)*
6. **Treat the installer / "getting started" path as the user's first impression of the product.** The user has no patience for friction at install time. Detect what you can detect (platform, architecture); ask only what you cannot. Tell the user where files are written so they can clean up later. For a library or CLI, ship a five-line "Hello, world" that produces exactly the output advertised — not a wizard, not an XML scaffold. *(Baker, 97/40.)*
7. **Set up the bug tracker so reports are conversations, not accusations.** A good defect report has three parts: how to reproduce (and how often), what should have happened, what actually happened. Configure issue templates that ask for those three. Make the standard query for "open bugs in my area" a one-click link every contributor knows. Status changes carry a short reason; closed-without-explanation invites re-open wars. Do not overload subject lines or fields for personal triage signals — add a real field, document it. A bug is not a unit of work, any more than a line of code is a unit of effort. *(Doar, 97/38.)*

### Automation

8. **Automate the coding standard; do not rely on humans to follow it.** Formatting, import order, banned APIs, complexity thresholds, test-coverage floors — encode them as commit-blocking checks and break the build when violated. A standard nobody enforces is abandoned one rule at a time under deadline pressure. The rules you cannot automate are guidelines, and you should expect them to drift. *(van Laenen, 97/4.)*
9. **Run static analysis as a first-class quality gate, not an optional script.** Tests find behavioral bugs the tests imagined; static analyzers find the bug class your tests forgot — null dereferences, unused returns, possible races, unreachable branches. Pick the strongest analyzer your language supports, configure it to your project's signal/noise tolerance, and gate the build on it. When no off-the-shelf checker covers your project's specific anti-pattern, write a small one — most languages expose the AST in their standard library. *(Mount, 97/79.)*
10. **Reach for the Unix toolchest before reaching for a custom script or a heavyweight platform.** `grep`, `sed`, `awk`, `sort`, `uniq`, `xargs`, `jq`, `find`, a shell loop — these compose into a one-liner for tasks that would otherwise become a maintained tool. They work on every textual format, scale to enormous inputs without rewrites, and pipeline naturally across cores. *(Spinellis, 97/88.)*
11. **Step back when you notice yourself doing the same manual sequence twice — automate it.** The deploy you click through, the report you copy-paste, the file you reformat by hand — wrap each in a script the first time you repeat it. Misconceptions to refuse: "automation is just for testing" (no — also for build, package, deploy, doc generation, reporting); "the IDE does it" (the IDE does it for you, not for the next contributor or for CI); "I don't have time" (the script pays for itself by the third run, and earlier in the project there is more slack to write it). *(Horstmann, 97/78.)*

## Red Flags

These thoughts mean STOP — restart the checklist:

| Thought | Reality |
|---|---|
| "The build script is a release-engineering thing — I won't touch it." | The build is what produces the artifact your users run. It is the dev team's code, owned and refactored like any other. (97/63) |
| "We'll rebuild from source on the prod box with the same scripts — same result." | You lose the proof that what shipped is what was tested. Build once, promote that artifact through every environment. (97/61) |
| "I'll bake the staging API URL into the image — easier than wiring up config." | The image is no longer environment-agnostic. Push environment values into env vars, mounts, or a config service so one image runs everywhere. (97/61) |
| "Deploy is trivial — we'll wire it up at the end." | Deferred deploy hides assumptions until they are expensive to fix. Deploy to a clean environment from week one and refactor the pipeline as you go. (97/20) |
| "I'll add this new framework alongside the one we already use — it's better." | A parallel tool doubles maintenance and fragments knowledge. Respect the existing convention or change it deliberately, with the team. (97/10) |
| "It's open source so adoption is free." | License terms, upgrade cadence, support model, and lock-in are real costs. Evaluate before adopting; isolate behind an interface so it can be swapped. (97/10) |
| "The README is enough — installation is obvious." | The user runs cost-benefit on every second of friction. Ship a five-line working example and tell the user where files are written. (97/40) |
| "I'll just hand-format this file before committing — once is fine." | A standard nobody enforces is gone in a month. Automate the formatter into the commit hook and break the build on violations. (97/4) |
| "We have tests, so we don't need static analysis." | Tests find the bugs the tests imagined. Analyzers find the class of bug the tests forgot — null deref, dead branch, possible race. Run both. (97/79) |
| "I'll write a Python script for this one-line text munge." | A `grep \| awk \| sort -u` pipeline does it now and works on every project. Reach for the toolchest before reaching for a new file. (97/88) |
| "I've done this manual sequence twice — third time will be just as fast." | The third time is the moment to script it. The IDE-only or laptop-only workflow does not survive the next contributor or CI. (97/78) |
| "`fix bug` is a fine commit message — git blame will explain it." | The next reader needs the *why*. One commit per logical change, with a message that names the intent, is the contract. (97/68) |
| "I'll hardcode the staging API key in the config file — easy to swap later." | Could you open-source this repo right now without leaking a credential? Push every per-deploy value out into env vars or a secrets manager. (`12F/III`) |
| "I'll patch the running prod box — faster than cutting a new release." | That collapses run back into build and destroys "what runs is what was tested." Roll forward to a new release; do not edit the running one. (`12F/V`) |
| "I'll write user uploads to a local directory and the next request reads them." | The next request may land on a different host, the next deploy will lose the directory, and a restart wipes it. State belongs in a backing service. (`12F/VI`) |
| "I'll have the process write logs to a rotated file on the host." | Log files on the host vanish on restart and require per-host access to read. Write to stdout/stderr and let the platform aggregate. (`12F/XI`) |
| "I'll tweak the Jenkins job in the UI — one-time fix." | The deploy pipeline is production code. UI tweaks bypass review and produce config drift. Pipeline lives in version control with PRs. (`CD/PipelineAsCode`) |

## What "done" looks like

A change to build/CI/deploy/tooling is done when **all** of the following are true:

- [ ] Every file the project needs (including the change you just made) is in version control with a commit message that explains the why.
- [ ] The build can be reproduced from a clean clone with one documented command.
- [ ] The deployable artifact is produced once and the same artifact promotes through environments; environment-specific values are external.
- [ ] At least one automated path deploys the artifact to a non-production environment, and the path is exercised regularly enough to stay green.
- [ ] Any new tool or dependency you added has a stated reason, a stated owner, an upgrade plan, and a place where it is isolated behind an internal interface (or a stated reason that isolation is not warranted).
- [ ] The coding standard, the static analysis, and the test-coverage floor are enforced by the build, not by reviewer memory.
- [ ] No manual sequence you noticed yourself repeating is left un-scripted.
- [ ] If you added an installer, library, or CLI surface, a new user can reach a working "Hello, world" in under five minutes.
- [ ] The bug tracker has a discoverable query for "open issues in this area" and the issue template asks for repro / expected / actual.

If any box is unchecked, the change is not done. Either finish, or revert and re-plan.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/4 | Automate Your Coding Standard | Filip van Laenen |
| 97/10 | Choose Your Tools with Care | Giovanni Asproni |
| 97/20 | Deploy Early and Often | Steve Berczuk |
| 97/38 | How to Use a Bug Tracker | Matt Doar |
| 97/40 | Install Me | Marcus Baker |
| 97/61 | One Binary | Steve Freeman |
| 97/63 | Own (and Refactor) the Build | Steve Berczuk |
| 97/68 | Put Everything Under Version Control | Diomidis Spinellis |
| 97/78 | Step Back and Automate, Automate, Automate | Cay Horstmann |
| 97/79 | Take Advantage of Code Analysis Tools | Sarah Mount |
| 97/88 | The Unix Tools Are Your Friends | Diomidis Spinellis |
| `12F/III` | Config in the Environment | Adam Wiggins / Heroku |
| `12F/V` | Strict Build, Release, Run Separation | Adam Wiggins / Heroku |
| `12F/VI` | Stateless, Share-Nothing, Disposable Processes (paired with factor VIII) | Adam Wiggins / Heroku |
| `12F/XI` | Logs as Event Streams | Adam Wiggins / Heroku |
| `CD/PipelineAsCode` | Pipeline as Code | Jez Humble & David Farley |

See `principles.md` for the long-form distillations, citations, and source links.
