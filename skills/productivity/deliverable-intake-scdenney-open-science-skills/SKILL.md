---
disable-model-invocation: true
name: deliverable-intake
description: Turns raw captures, dictated braindumps in a deliverable’s inbox/, or recent macwhspr dictation-log entries into proposed planning-wiki changes, shown as a unified diff for author acceptance or rejection. Classifies every capture line as a decision, evidence claim, question, task, or dropped item with a reason, and traces it to its source. Uncertain names and citations remain UNRESOLVED. Applies decisions only with explicit assent. Use when the user says "intake", "absorb my notes", "process the inbox", "I dictated something", or after notes from a talk, meeting, or reading session. Never edits source files, only planning/ and open questions.
argument-hint: '[inbox file or --all; optionally --from-log N to import the last N dictation-log entries]'
allowed-tools:
- Read
- Glob
- Grep
- Bash
- Write
- Edit
- AskUserQuestion
---

# Deliverable intake

<p align="center"><img src="../deliverable-open/assets/pipeline.svg" alt="The deliverable pipeline: eight steps over three layers (one wiki per piece of research, one manifest per deliverable, a shared commons)" width="900"></p>

Full guide: [`docs/deliverable-pipeline.md`](../../../docs/deliverable-pipeline.md).

The author thinks out loud; the wiki stays authoritative. This skill is the seam between the two. It reads captures verbatim, proposes where each statement belongs, and applies nothing the author has not seen.

## Inputs

- The nearest `deliverable.yml` upward from cwd (or the path given). Read it, then `planning_dir/00-README.md` and every file that index names. That is the current state of the wiki; the proposal is a diff against it.
- `inbox/*.md` that do not end in `.done.md`, oldest first. A capture is read verbatim and never edited.
- `--from-log N`: show the last N entries of `~/.config/macwhspr/cleanup_log.jsonl` (`{ts, raw, cleaned}` pairs) as a numbered list with the first line of each, and ask which to import. An imported entry is written to `inbox/YYYY-MM-DD-HHMM-log.md` with the `cleaned` text (the `raw` text appended under a `<!-- raw -->` marker) before anything else happens. Nothing is imported without being named.

## Classify, then trace

Walk the capture paragraph by paragraph. Each statement gets exactly one class:

| Class | Goes to | Needs assent? |
|---|---|---|
| **decision** | the wiki file that owns the topic (`00-README.md` "Decisions recorded here", or the numbered file) | yes, always |
| **evidence claim** | the wiki file for the section it supports, marked with the capture reference | no, but a claim naming a source that is not in `sources_of_truth` or the bib is written as `UNRESOLVED: <claim>`; when the manifest names a `knowledge_base`, the report lists each such source as a `process-source` candidate (drop the PDF in `sources/unprocessed/`) so intake feeds the knowledge base rather than bypassing it |
| **question** | `08-open-questions.md`, open list | no |
| **task** | `08-open-questions.md` under a `Tasks` heading, or the top HANDOFF entry's next actions if it is due before the next session | no |
| **dropped** | nowhere; listed in the report with the reason (duplicate, already resolved, off-topic) | no |

Every proposed line carries a trace: `(inbox/2026-09-10-debrief.md ¶3)`. A capture paragraph that yields no proposal is listed as dropped with its reason, so the author can see the capture was read whole.

Names, dates, numbers, and citations that the capture states but the wiki cannot confirm stay as dictated and are tagged `UNRESOLVED`. Do not correct a dictated name against a guess; do not invent a citation to match a claim; do not resolve a number from memory.

## Propose

Produce one unified diff across the wiki files (new files included) plus the dropped list. Show it. Then put the decisions to the author as a numbered list, each with the sentence that would be written and where; use `AskUserQuestion` when there are three or fewer, a numbered list otherwise.

## Apply

On assent: apply the diff and rename the capture to `*.done.md`. Do not edit any existing HANDOFF.md entry, today's included; the intake is recorded by the closure step (`/finished`) as `Intake: <capture> -> <n> decisions, <n> claims, <n> questions, <n> tasks, <n> dropped`, and if the session ends without closure the renamed capture and the wiki diff are the record. Record which capture paragraphs were promoted (a `<!-- promoted: ¶1,¶3 -->` line at the end of the `.done.md` file) so a partially accepted capture is never promoted twice. On refusal of any decision, leave that line out and keep the capture unrenamed until the author says otherwise.

## Report

Five lines: captures read; counts by class; UNRESOLVED items (each with what would resolve it); decisions applied; what to run next (`/oss:deliverable-lint` if the wiki changed materially, otherwise nothing).

## Notes

- This is a single-worker task and a cheap model suffices. Do not spawn subagents.
- A reaction to a lint report is a capture like any other: dictate it into `inbox/`, then intake it; findings the author accepts become tasks, findings they reject go under a `Rejected findings` heading in `08-open-questions.md` (the authoritative wiki, not `NOTES.md`) with the finding id and one line of reason, so the next lint does not raise them again.
- Register vocabulary as it appears: a proper noun the dictation mangled twice belongs in `~/.config/macwhspr/vocab.md` (offer, never append silently).
