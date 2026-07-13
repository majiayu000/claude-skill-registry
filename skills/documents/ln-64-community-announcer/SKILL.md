---
name: ln-64-community-announcer
description: "Drafts and publishes fact-checked GitHub Discussions announcements. Use for releases, updates, or project news; not for release creation or issue responses."
---

# Community Announcer

Create a source-backed announcement and publish it only after the user approves the full draft.

## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Repository identity and permissions | Authenticated GitHub CLI or connector | Public GitHub API for read-only discovery |
| Discussion categories and publication | GitHub GraphQL API | `BLOCKED`; do not substitute an issue |
| Shipped-change evidence | Remote Git history, releases, and canonical files | Clean remote clone |
| Commands, paths, names, and counts | Focused repository search and direct reads | Hosting API content reads |
| Current external claims | Primary dated sources | Omit the claim when it cannot be verified |
| Draft publication | Temporary Markdown file passed to the API | Safely escaped API input with read-back verification |

Prefer the hosting API over scraping rendered pages. Use the browser only to inspect presentation or a page the API cannot expose.

Do not expose repository tokens, category node IDs, or other credentials in the announcement. IDs may be used for the mutation but are not audience content.

## Checklist

- [ ] Resolve the target repository from the authenticated hosting client and verify write access.
- [ ] Discover the repository ID, default branch, Discussions availability, and Announcements category ID through the API.
- [ ] Stop with `BLOCKED` when Discussions or a suitable category is unavailable; do not silently publish elsewhere.
- [ ] Identify the announcement subject from the user's request, a release, or a bounded commit range.
- [ ] Read repository communication guidance when present, but do not require a community strategy file.
- [ ] Read the current README, installation instructions, affected manifests, release notes, and relevant source diffs.
- [ ] Inspect recent commits and the latest three comparable announcements for cadence, repeated claims, and house style.
- [ ] Use the public remote state as the source for already-published changes; do not announce an unpushed local diff as available.
- [ ] Separate what shipped, what changed for users, migration needs, and future intent.

## Classification and Style

- [ ] Classify the announcement as release, breaking change, feature update, architecture change, or community news.
- [ ] Choose the shortest style that explains the user outcome and its significance.
- [ ] Use a concise release digest for several independent changes.
- [ ] Use a problem-to-solution narrative when the motivation is necessary to understand the redesign.
- [ ] Use migration-first structure when existing users must take action.
- [ ] Vary the opening from recent announcements when doing so remains natural; variety is not more important than clarity.
- [ ] Do not force emoji, slogans, dramatic metaphors, or a fixed template.
- [ ] Match the project's voice while keeping claims understandable without internal repository context.

## Draft

- [ ] Write a specific title that names the outcome rather than saying only "update" or "announcement".
- [ ] Open with the user problem or the most important shipped outcome.
- [ ] Explain why the change was made using evidence from commits, docs, or release notes.
- [ ] Summarize highlights in outcome language and name exact plugins or skills where useful.
- [ ] Include verified installation or update commands when the reader must act.
- [ ] Add an `IMPORTANT` migration block for breaking changes, including clear before-and-after steps.
- [ ] Link to canonical documentation at the default branch or immutable release tag as appropriate.
- [ ] Include a short "What's next" section only for committed or clearly labelled tentative work.
- [ ] Thank verified external contributors by handle; omit the section for solo work.
- [ ] End with one genuine, answerable feedback question when community input would be useful.

## Fact Check

- [ ] Verify every command against the current README and stable marketplace identifier.
- [ ] Verify every plugin, skill, file path, category, version, tag, and link against the remote repository.
- [ ] Recompute every count from the target commit; avoid counts when they add no user value.
- [ ] Confirm feature descriptions against the actual changed `SKILL.md` or manifest, not commit-title shorthand.
- [ ] Confirm removed capabilities and compatibility limits are stated explicitly.
- [ ] Do not invent adoption, download, search-volume, performance, compatibility, or roadmap claims.
- [ ] Label estimates, interpretations, and future intent instead of presenting them as shipped facts.
- [ ] Remove generic hype, repeated conclusions, excessive headings, canned transitions, and symmetrical filler lists.
- [ ] Prefer concrete verbs and varied sentence length; keep technical identifiers only where readers need them.
- [ ] Re-read the draft as a new user and ensure it explains both the value and any required action.

## Approval and Publication

- [ ] Present the exact title and full Markdown body to the user before creating external state.
- [ ] Include the selected category and evidence range with the draft.
- [ ] Wait for explicit approval; a request to draft or announce is not approval of unseen final copy.
- [ ] If the user changes any substantive claim or instruction, fact-check the revised draft again.
- [ ] Write the approved body to a temporary file to preserve formatting and avoid shell interpolation errors.
- [ ] Publish through the GitHub Discussions GraphQL mutation using discovered repository and category IDs.
- [ ] Read the created discussion back and verify its title, body, category, and URL.
- [ ] Remove the temporary draft safely after verification.
- [ ] Report the discussion URL and any manual action, such as pinning, that the API cannot perform.
- [ ] Do not create tags, releases, issues, comments, or cross-posts unless explicitly requested.

## Verdict

- `DRAFT READY` — fact-checked copy is awaiting explicit approval.
- `PUBLISHED` — the approved discussion exists and was read back successfully.
- `BLOCKED` — required source evidence, permissions, category, or publication verification is unavailable.

## Output Contract

Before approval, return classification, evidence range, selected category, title, full Markdown body, fact-check summary, and `DRAFT READY`.

After publication, return the approved title, discussion URL, verification evidence, `PUBLISHED`, and residual risks.

If a published discussion differs from the approved draft, report `BLOCKED` and ask before editing or deleting the external content.

Preserve the approved copy in the response so the user can compare it with the published discussion.
