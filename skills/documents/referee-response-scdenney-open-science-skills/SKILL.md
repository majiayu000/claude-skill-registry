---
name: referee-response
description: Organizes and formats an author's response to peer review — extracts every distinct point from the referee reports and the editor's letter, tags severity and type, maps the dependencies so the revision runs in the right order, flags which points the author may want to push back on, and builds the response-to-reviewers letter as a numbered comment → response → location table with the substantive answers left for the author to write. It formats and checks the response; it never writes the scientific content of an answer. Use when the user has referee or reviewer reports, a revise-and-resubmit decision, or an editor's letter and says "respond to reviewers", "plan the revision", "map the referee comments", "draft the response letter", or "check I addressed everything". The reviewer-side twin is journal-review; prose polish afterwards goes to sci-edit.
argument-hint: "[paths to the referee reports and editor letter, plus the manuscript; optionally: plan | letter | check]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
---

# Referee Response

Turns scattered reviewer comments into an ordered revision plan and a response letter the author fills in. The author writes every substantive answer; this skill makes sure each point is found, ordered, answered somewhere, and formatted the way editors expect.

**Related skills.** `journal-review` writes a referee report for someone else's manuscript; this skill answers one written about yours. `sci-edit` polishes the letter's prose after the author has written the answers. `paper-review-lite` and `citation-check` are useful before resubmission when a referee's point implies the manuscript needs a fresh audit.

## Inputs

One or more referee reports, the editor's decision letter if available, and the manuscript (current draft, and the submitted version if the two differ). If a report is a PDF or Word file, read it with `doc-to-markdown` first. Ask once for anything missing that the steps below need; do not guess at a report's content.

## Modes

Infer from the request; an argument forces it.

- `plan` (default when no letter exists yet): steps 1–3.
- `letter`: steps 1–4, producing the letter skeleton.
- `check`: step 5 over a letter the author has filled in.

## Step 1 — Extract every point

List every distinct request, criticism, or question across all reports and the editor's letter. One row per point, even when a referee bundles several into one paragraph. For each point record:

- referee (R1, R2, editor), and the location in the report;
- the point, quoted or closely paraphrased so the author can find it;
- severity: **blocking** (the editor or a referee makes acceptance conditional on it), **major**, **minor**, **optional** (a suggestion the author may decline);
- type: analysis, design, framing, writing, citation, data or code, presentation;
- whether another referee raises the same point, agrees, or conflicts with it.

Count the points and tell the author the count per referee. A missed point is the commonest reason a resubmission fails, so the list is the deliverable of this step, not a summary of it.

## Step 2 — Map dependencies and order the revision

Order the points so upstream changes come first: a new specification before the discussion that interprets it; a reframing before the sections that rest on it; a data correction before every number that depends on it. Group into a sequence (do first → depends on). Flag conflicts between referees as editor-judgment calls and say what each resolution would cost.

For each point in order: the change implied, the manuscript sections and files it touches, whether it needs new analysis, and a rough effort estimate. Where a point would distort the manuscript's argument if taken literally, say so.

## Step 3 — Flag the pushbacks, as questions

Not every request should be accepted. Mark the points where a reasoned decline is defensible (the request contradicts the pre-registration, rests on a misreading, asks for an analysis the design cannot support, or would trade a confirmatory claim for an exploratory one) and give the reason. Put each to the author as a question; the decision is theirs. Do not write the decline itself.

## Step 4 — Build the letter skeleton

The standard shape editors expect:

1. **Cover note to the editor.** Thanks, a two-sentence summary of the main changes, and a pointer to the point-by-point response. Leave the summary as `[AUTHOR: two sentences on the main changes]`.
2. **General response** (optional): a short paragraph for changes that cut across several points. Placeholder.
3. **One section per referee, in the order the editor listed them.** Within each, every point from step 1 in the referee's own order, as a numbered table or numbered blocks:

   | # | Reviewer comment | Response | Where in the manuscript |
   |---|---|---|---|
   | R1.1 | *quoted or paraphrased point* | `[AUTHOR: …]` | `[section / page / line]` |

   Keep the reviewer's wording in the comment column so the referee recognizes the point. Pre-fill the response column only with the kind of response the plan implies (`[AUTHOR: describe the new robustness table]`, `[AUTHOR: reasoned decline, see step 3]`), never with content. Where the same point appears under two referees, cross-reference rather than duplicate.
4. **Editor's points**, if the letter contains any beyond the referees'.

Write the skeleton to `response_to_reviewers.md` beside the manuscript unless the author names another path. State how many placeholders it contains.

## Step 5 — Check the filled letter

Once the author has written the responses:

- Every point from step 1 has a non-placeholder response; list any that do not.
- Every manuscript location cited in the letter exists in the current draft (section headings, table and figure numbers, page ranges); list any that do not resolve.
- Every response that claims a change names where the change is; every reasoned decline gives a reason.
- Tone: responses are courteous and specific, never defensive; flag sentences that argue with the referee rather than answer them, and leave the rewording to the author or to `sci-edit`.
- Conflicting referees: the letter says which way the author went and why.

Report the checks as a short list of what passed and what needs the author's attention.

## Notes

- The skill never drafts scientific content: not a new analysis, not the interpretation of a result, not the reason a request is declined. It supplies structure, order, placeholders, and checks.
- Keep the manuscript's argument intact. Where a referee request would change a confirmatory claim, say so in step 2 and put the decision to the author.
- Heritage: grown from a personal `referee-response` skill (2026-05) into a library skill on 2026-09-02.
