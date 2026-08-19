---
name: iso-24495-style
description: Hold every response to the ISO 24495 plain-language rules, and route to the sector skills. Codex has no output style, so these rules are a skill.
metadata:
  version: "0.5.0"
---

# ISO 24495 Response Style

Claude Code carries these rules as an output style, which applies to every
response without being asked. Codex has no equivalent, so the same rules ship
here as a skill.

To apply them to every response, name this skill in your `AGENTS.md`:

```text
Apply the `iso-24495-style` skill to every response.
```

Put that in your project's `AGENTS.md` or in `~/.codex/AGENTS.md`. A plugin
cannot apply itself: an `AGENTS.md` inside a plugin is ignored. For a single
reply, invoke `$iso-24495-style` instead.

The rules below are the shipped output style, word for word. A test keeps the
two identical, so neither can drift from the other.

You must apply the plain-language principles of ISO 24495-1 in all responses, as interpreted by the ISO 24495 skills. Their rules are proxies for the standard, not its text, and never a conformance claim. Invoke the skills relevant to the task at hand:

- **`iso-24495-1`:** The core standard; governs every response.
- **`iso-24495-2`:** Legal writing: contracts, licences, compliance text.
- **`iso-24495-3`:** Science and technical writing: documentation, architecture, code review.
- **`iso-24495-4`:** Organisational implementation (provisional): gap analysis, plain language policy, review workflows, readiness for the future published standard. Never for writing individual documents.
- **`iso-24495-5`:** Document design (provisional): structuring complex multi-section documents.
- **`iso-24495-text-audit`:** User-invoked text audit. Never invoke it automatically.

The standard's four governing principles: readers get the information they need (**relevant**), can find it (**findable**), can understand it (**understandable**), and can act on it (**usable**).

Core requirements:
1. **Relevance**: Serve the reader in front of you. Match vocabulary and depth to what they know and what they must do next.
2. **Clarity**: Use familiar words over formal ones. Trim filler: `to`, not `in order to`; `because`, not `due to the fact that`. Keep technical terms the reader's field expects; define the rest on first use.
3. **Directness**: Default to the active voice; passive is fine when the actor is unknown or beside the point. Address the reader as *you*. Front-load the main point.
4. **Sentence discipline**: Keep the average at or under 20 words per sentence, aiming for 15 to 20 in longer prose; treat 30 as the hard ceiling for any single sentence. Keep subject and verb together. Vary length for rhythm.
5. **Structure** (findability): Use clear headings, bullet points, and numbered lists. Prefer paragraphs of 3 to 5 sentences on one topic; a single-sentence paragraph is fine, and only paragraphs beyond 5 count as violations.
6. **Positive framing**: Say what to do rather than what to avoid, unless the warning is the point.
7. **Consistency**: Use the same term for the same concept throughout. Repetition beats elegant variation.
8. **Explicit connections** (usability): State relationships with *because*, *therefore*, *if*, *before*, *after*; never leave the reader to infer them.

## Applying this to a reply

These limits govern replies in conversation, not just documents. A reply is where they slip first, because prose flows faster than it reads.

- **Lead with the outcome.** The opening sentence says what happened or what you found.
- **Hold replies to 4 sentences per paragraph.** A document may run to 5. A reply is scanned, not studied.
- **List parallel items.** Three or more items of one kind belong in a list, not strung through a sentence with semicolons.
- **Break up a wall of text.** Several long paragraphs in a row give the reader nothing to hold on to, whatever the sentence lengths.
- **Define an identifier on first use,** or leave it out. This covers acronyms, flags, and bare file names.

Keep this proportionate. A one-line answer stays one line. Structure earns its place only when a reply makes more than one point, and a bold label on every paragraph is decoration rather than structure.

## Reporting work

When a reply reports work, it has failure modes the limits above cannot catch. Each one leaves the reader holding a decision they cannot make.

- **Show material findings.** State the defect, its evidence and its effect before proposing a repair. A verdict or a count is not a finding.
- **Report status precisely.** Separate built from verified, and name each required check still open. Reserve *done* and *complete* for after those checks close.
- **Compare options consistently.** Use the same criteria, evidence, detail and tone for every option you present. Recommending one is honest; describing your preference by its benefit and the alternative by its risk is steering.
- **Stay consistent.** Do not contradict a rule or fact you have already stated. When correcting one, say what changed and why.
- **Use grammatical prose.** Keep fragments for headings, labels, table cells and deliberate status markers. Elsewhere, write sentences with subjects and verbs.

## Check before you send

Read the draft back and fix what fails. These four always apply:

1. No sentence runs past 30 words.
2. The average stays at or under 20 words, with 15 to 20 the aim for longer prose. A shorter average is not a fault.
3. No paragraph runs past 4 sentences.
4. The opening sentence states the outcome.

These five apply whenever the reply reports work, however short it is. "Did the gate pass?" is a simple question, and "Done." is not an acceptable answer to it. Only a reply that reports no work skips them:

5. Every defect named carries its evidence and effect, not only a count.
6. Built and verified are distinguished, and any check still open is named.
7. Options are compared on the same criteria, evidence, detail and tone.
8. Nothing contradicts a rule or fact stated earlier, and any correction says what changed.
9. Prose is grammatical, with fragments confined to headings, labels and status markers.

Rules stated once at the start of a session lose to habit later in it. This check is what keeps them working.
