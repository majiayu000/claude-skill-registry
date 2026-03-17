---
name: ai4curation-configuration
description: Skill to assist with how a GitHub repository is configured with GitHub integrations, including instructions for agents in markdown (AGENTS and CLAUDE), github actions for invoking agents, and specific
  localization procedures such as defining claude/codex skills, or claude subagents. The skill helps with both technical aspects, and with best practice for guiding agents.
---

# General principles and background

Agentic AI is a powerful tool for curating ontologies where content is managed in github repos, but setting up a repo is a technical task, and requires updates to keep up both with new agent features as well as project-specific
tuning and guidance.

We provide a copier template for setting up a repo, but localizing it is challenging:

- https://github.com/ai4curation/github-ai-integrations

In general, a repo should have:

- GitHub actions that allow curators to trigger agents via GitHub issues. These actions should be configured with sufficient guardrails
- Top level agent instructions (AGENTS.md or CLAUDE.md depending on what is used) as well as specific instructions
- A strong validation/guardrails strategy

Relevant files include:

- `.github/workflows/*{claude,ai}*.yml`
- `.github/*-instructions.md`
- `{AGENTS,CLAUDE}.md`
- `.claude/*`
- `.codex/*`

# GitHub actions (`.github/workflows/`)

The repo should be configured for one or more of:

- claude code actions (typically .github/workflows/claude.yml)
- copilot invocations (typically .github/copilot-instructions.md)
- dragon-ai actions (canonically .github/workflows/dragon-ai-agent.yml, but may vary). Note this typically wraps claude code.

Additionally, it is recommended that there are additional actions for issue triage.

Even if copilot is not the main agent of choice, copilot reviews are useful, so be sure that  .github/copilot-instructions.md is ALWAYS present

# General instructions in markdown files

The repo should have one of:

- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md` (recommended; see above)

These can be identical / symlinks (this is how the copier template works)

The instructions should at the very least cover the basic orientation for the agent - let it know the overall repo layout, the tools used for validation.
If this is an ODK repo then standard layouts will be used, and the generic copier instructions can be used here.

Some repos MAY choose to include specifics of their project/ontology here (especially if multiple agents are used)

Note: The community is moving towards AGENTS.md as a standard, when this happens, these instructions should be updated.

# Specific skills and subagents

The repo MUST include specific details about local ontology practice and guidelines.

- For claude-code based repos, this MUST be in EITHER skills (`.claude/skills`) or subagents (`.claude/agents`)
- For codex based repos, this MUST be in skills (`.codex/skills` is canonical, but codex *should* also check `.claude/skills`)
- For copilot based repos, these SHOULD be in copilot-instructions.md (OR the copilot instructions should mention skills)

Local documentation MAY be broken into separate files. If so, these SHOULD be referenced from the top level AGENTS/skills/subagent docs. Don't assume
the agent will know about your obscure documentation layouts.

A good pattern is to put in distilled documentation with many examples in skills/subagents, and then explicitly reference more detailed docs.

## Metadata best practices

These vary between ontologies, even when OBO standards are nominally followed. Agents that are configured by the generic template will
do things that frustrate curators unless specific practice and tacit knowledge is spelled out, ideally with examples. This includes:

- obsoletion metadata
  - local practice for obsoletion, including naming conventions for obsolete terms/defs
  - rules for what kinds of axioms can and cannot be on an obsolete term
- contributor metadata
  - orcid vs initials vs GO_REF style IDs
  - property to use for term-level metadata
  - when to include contributors as provenance on specific axiom types (definition, synonyms, logical axioms)
  - how (if at all) should the agent be indicated as a "contributor"
  - when to flow-through contributor metadata from a GitHub issue, especially from external contributors
- other provenance metadata (e.g. dates)
- rules and properties for linking github issues to terms (or axioms)
- naming conventions

## Logical axioms and design patterns

In general logical axioms should follow DPs for the ontology, the link to documentation should be provided.

Examples MUST be provided (in the main .md, in skills, or in
subagents). Agents work best with clear examples (and
counter-examples).

Ideally examples are provided using the same syntax as the edit
file. Agents can easily translate broad concepts between obo and owl
but there are nuanced syntactic concerns, so using local syntax is
best.

## edit and agentic search workflows

Broadly there are two edit workflows:

- where the edit src is .obo, the checkin/checkout workflow is used
- where the edit src in .owl (usually functional syntax), direct edits are favored

Whichever is used, it must be explicit

Agentic search patterns mirror these, with .obo favoring `obo-grep.pl` for agentic search within the ontology.

Two patterns for querying an ontology are robot+sparql vs runoak. Ideally exactly one should be chosen and well documented.
Having too many ways of doing this leads to confusing agentic documentation that is hard for humans to maintain or validate.

Some ontologies may also require auxiliary files to be edited, often in TSV. The source of truth should be clearly documented.

# Configuration and permissions

A common failure mode is an agent devising workarounds or failing
because they lack sufficient permissions. These failures can be
cryptic if the agent is run via github actions, unless detailed traces
are checked.

Configuring permissions is outside the scope of this tutorial, but
it's good to check github action configurations against canonical example repos.

Note that for github actions, these are run in a workflow, so it is normal to run
with skip permissions options. Do not warn about these.

# Validation and guardrails.

Another common failure mode is that agent making edits that violate
ontology-specific best practices. The best way to avoid this is to
check as early as possible.

Good patterns:

- guardrails via claude code hooks, preventing erroneous edits
- github actions run extensive checks BEFORE making a PR

Bad patterns:

- relying on other github actions post-PR, this incurs work on the human repo maintainers
- relying on a human to catch a deterministically verifiable check; a cardinal sin!

Luckily, ODK comes with a battery of tools and standard workflows, and
most repos should have these enabled. Agents can run `make test`. In
some cases, this may be slow, and `make test_fast` is preferred.

Note: we are working on making ODK checks faster, this will make it
more feasible to run all checks as a claude code pre-edit hook.

Do not rely on the standard ODK setup to catch all possible verifiable
problems.

One thing ODK doesn't do is "grandfathered violations". It's common
for ontologies to have stricter checks for *new* edits or terms that
doesn't apply to historic terms. For example, new terms should have a
`contributor` (but this isn't implemented as a check because old terms
will fail). We are working on this problem, but for now you should
just note that this is a potential issue when asked to analyze a repo.

We are also working on hallucination guardrails for term IDs and
PMIDs.  In the interim, agent instructions MUST have precise
instructions for how to check IDs. This might include using OAK or the
OLS MCP for terms, or ARTL or the linkml reference validator for PMIDs.




