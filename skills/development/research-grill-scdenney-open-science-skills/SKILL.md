---
name: research-grill
description: Interviews a researcher, in rounds, until a research idea, design, or draft has no silently assumed decision left — every question numbered, each with a plain-language "why this matters" and a recommended answer, facts fetched by the assistant rather than asked, and every settled decision written to a file. Three stages, idea (a topic or hunch → a falsifiable question and a contribution claim), design (a question → estimand, identification, sample and power, measurement, pre-registration, analysis plan, venue), and defend (a finished design or draft → the objections a reviewer would raise, before the reviewer does). Use when the user says "grill me", "grill this", "stress-test my idea/design/plan", "interview me about this project", "poke holes in this", "what am I assuming", or brings a research idea that is not yet a design. Suitable for BA, MA, and PhD students as well as grant designs; it never answers the research question for the researcher. Adapted for research from Matt Pocock's grill-me. For a software or process plan rather than research, run it with `--plan`.
argument-hint: "[describe the idea, design, or draft to grill; optionally: idea | design | defend | --plan]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - Agent
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Research Grill

An interview, not an evaluation. You ask; the researcher decides. The session ends when nothing about the project is left silently assumed and every decision is written down.

**Related skills.** `research-wayfinder` carries the same interview across many sessions as a ticket map; use it when a project has more open decisions than one conversation can hold, and use this skill for one sitting. `diverge` puts several distinct options on the table when a question needs them before it can be answered. `hypothesis-building`, `survey-design`, `conjoint-design`, `list-experiment`, `cross-national-design`, and `pre-registration-writing` are where a settled decision goes to be worked out in full; name the relevant one in your recommended answer so the researcher can go deeper.

## Stage

Infer the stage from what the researcher brings; an argument forces it.

| Stage | Researcher brings | Done when |
|---|---|---|
| `idea` | a topic, a hunch, a puzzle, "I want to study X" | one falsifiable research question, the population it covers, the contribution claim in one sentence, and the reason an experiment or survey is the right instrument rather than existing data |
| `design` | a research question | the design tree below is fully visited: estimand, identification, sample and power, measurement, analysis plan, ethics and pre-registration venue, output venue |
| `defend` | a finished design, a pre-analysis plan, or a draft | every objection a careful reviewer would raise has been put to the researcher and either answered, accepted as a limitation, or turned into a design change |

`--plan` runs the generic version for software, process, or teaching plans: the same rounds mechanic over the plan's own decision tree, without the research design tree.

## The design tree

Every decision branches into the decisions that hang off it. The tree for research, in the order prerequisites usually settle:

1. **Question and estimand.** What quantity, for whom, under what counterfactual. A question without an estimand is a topic.
2. **Theory and hypotheses.** The mechanism that yields a falsifiable if-then, the direction it predicts, and the smallest effect size that would matter (SESOI). `hypothesis-building`.
3. **Design and identification.** Random assignment or the identification strategy; what would break it; whether the treatment is the one the theory names. `conjoint-design`, `list-experiment` where they apply.
4. **Population, sample, and power.** Who the claim covers, how they are recruited, N for the SESOI, and what is lost if the sample is a convenience sample. `cross-national-design` when multi-country.
5. **Measurement.** Instruments, scales, manipulation checks, attention checks, social-desirability exposure. `survey-design`.
6. **Analysis plan.** Estimator matched to the design, covariates, multiple-comparison policy, what counts as a null.
7. **Ethics, pre-registration, and logistics.** IRB or ethics review, consent, registry, timeline, budget. `pre-registration-writing`.
8. **Output.** Thesis, working paper, journal, grant report; what the venue expects; who the reader is.

For a student thesis the "done" criteria are the programme's assessment rubric, which the `thesis:*` skills carry (BAIS, BAKS, MAAS, MAIR at Leiden). Ask which programme once, then read that rubric and treat its criteria as branches of node 8.

## Rounds

Work the tree in rounds. The **frontier** is every decision whose prerequisites are settled, so every question you can ask now without guessing at an answer you have not heard. Ask the whole frontier in one round, then wait.

Each question takes this form:

```
❓ Q1 — <short title>
<the question, in plain language; if it has a technical name, give it and gloss it once>
Why this matters: <one sentence on what goes wrong downstream if this is left open>
➡️ Recommended: <your answer, and the skill or source that backs it>
```

Rules for a round:

- **Number every question.** The researcher answers by number.
- **Recommend every time.** A question with no recommended answer is homework, not an interview. The recommendation cites the method skill or the source it rests on.
- **Plain language first.** A student must be able to answer without looking anything up. Give the technical term after the plain version, glossed once, and use it consistently afterward.
- **One round, one frontier.** A question whose answer depends on another question still open in this round belongs to the next round.
- **Facts are yours to find.** When a question needs a fact from the world (has this been done, what does the literature say the effect size is, does a dataset exist, what does the registry require), fetch it: `literature-review` or `WebSearch` for prior work and current tools, `Explore` or `Grep` for repository state, `WebFetch` for a registry or a journal's requirements. Dispatch the lookup and keep asking the rest of the frontier while it runs; only the questions downstream of that fact wait. Never ask the researcher for something you could look up, and never answer from memory about a name, tool, or dataset you do not confidently recognize.
- **Decisions are theirs.** Put every decision to the researcher and wait. Do not fill in a decision because the answer seems obvious. Do not answer the research question for them at any stage; the skill sharpens a claim, it does not supply one.
- **Recompute after every round.** Settled decisions push the frontier outward and unblock what depended on them. A decision the researcher reverses later reopens its subtree.

## Writing it down

The interview is worthless if it lives only in the chat.

- If the project has a `research-wayfinder` map (`planning/map.md`), write each settled decision into the matching ticket and add new tickets for what the interview surfaced.
- Otherwise write and maintain `decisions.md` in the project root (or the path the researcher names): one entry per settled decision, with the decision, the rationale in the researcher's words, what would change it, and the round it was settled in. Update the file after every round, not at the end.
- Facts you fetched go in the same file under a `Looked up` heading with the source, so the next session does not fetch them again.

## Exit

The session is done when the frontier is empty for the chosen stage and the file is written. Then, in one line each, name what comes next and stop: `hypothesis-building` after `idea`; `pre-registration-writing` or `research-wayfinder` after `design`; `narrative-building`, `paper-review-lite`, or the relevant `thesis:*` skill after `defend`. Do not start the next skill unless asked.

## Notes

- Do not soften the questions for a student and do not sharpen them for a professor; the tree is the same. What changes is the gloss, not the rigour.
- A researcher who cannot answer a frontier question has found the open decision the interview exists to find. Offer the recommended answer, mark it as provisional in the file, and move on; do not stall the round on it.
- Heritage: the frontier-rounds mechanic is Matt Pocock's `grill-me` (MIT, [mattpocock/skills](https://github.com/mattpocock/skills)); see `RECOMMENDED.md`. This skill adds the research design tree, the plain-language and recommended-answer rules, the fetch-not-ask routing through the library's method skills, the thesis rubric as done criteria, and the written decision record.
