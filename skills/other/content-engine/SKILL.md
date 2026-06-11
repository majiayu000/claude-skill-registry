---
name: content-engine
description: "Repurpose source assets into platform-native social content."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - repurpose this
    - adapt for social
    - turn this into posts
    - content from article
    - content from demo
    - content from doc
    - write variants for
    - social content from
    - platform variants
    - repurpose for
  pairs_with:
    - x-api
  category: content
  disambiguate: voice-writer
---

# Content Engine Skill

Repurpose anchor content into platform-native variants. This skill produces drafts only — it does not make API calls or publish content. Posting is handled downstream by `x-api` (single platform) or `crosspost` (multi-platform).

Platform-native means each variant is written from scratch for its target platform: different register (conversational on X, professional-but-human on LinkedIn, punchy on TikTok), different structure (thread vs. long-form post vs. short script vs. newsletter section), and different hook style (open fast on X, strong first line on LinkedIn, interrupt on TikTok). Shortening the same text for each platform is not adaptation — it produces content that reads identically everywhere and fails on every platform.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |
| drafting variants: platform rules, banned hype phrases, delivery handoff | `phase-playbook.md` | Loads detailed guidance from `phase-playbook.md`. |
| character limits and format rules per platform | `platform-specs.md` | Loads detailed guidance from `platform-specs.md`. |

## Instructions

### Phase 1: GATHER — Collect Inputs Before Writing Anything

Establish everything needed to write platform-native variants. Do not begin writing until this phase is complete.

**Required inputs:**

| Input | Description | If Missing |
|-------|-------------|------------|
| Source asset | The content being adapted (article text, demo description, launch doc, insight, transcript) | Ask — required |
| Target platforms | X, LinkedIn, TikTok, YouTube, newsletter — one or many | Ask if not inferable from context |
| Audience | Builders, investors, customers, operators, general | Infer if a strong signal exists; ask if ambiguous |
| Goal | Awareness, conversion, recruiting, authority, launch support, engagement | Infer from source if obvious; ask otherwise |
| Constraints | Character limits already observed, brand voice notes, phrases to avoid | Skip if none stated |

**Acquiring a transcript source asset**: When the source asset is a video URL (YouTube, etc.) rather than text, extract the transcript first:

```bash
python3 scripts/video-transcript.py transcript "<video-url>"   # add --timestamps or --json -o file as needed
```

Use the extracted transcript as the source asset for the rest of this phase.

**Gate**: Source asset present AND at least one target platform identified. If either is missing, ask before proceeding. Both missing means there is nothing to work with — do not guess.

Produce only the platforms the user requested. If the user says "turn this into an X thread", produce an X thread. Offer to expand to other platforms in Phase 5, but do not produce unrequested variants.

Do not write any content in this phase. Only collect and confirm inputs.

---

### Phase 2: EXTRACT — Identify 3-7 Atomic Ideas

Identify the discrete, postable units inside the source asset. Each atomic idea must stand alone as a post on at least one platform without requiring the reader to know the source.

**Steps:**

1. Read the full source asset
2. Identify ideas that meet the criteria:
   - Specific (concrete claim, result, observation, or instruction — not a vague theme)
   - Standalone (no dependency on other ideas in the list to be understood)
   - Relevant to the stated goal and audience
3. Rank by relevance to the stated goal
4. Write each atomic idea as one sentence maximum

Fewer than 3 ideas means the source is very narrow — proceed with what exists (minimum 1 is sufficient for a single platform) and note in the output file that the source yielded fewer than expected. More than 7 means the asset lacks coherence and should be split; ask the user which section to focus on.

See `${CLAUDE_SKILL_DIR}/references/phase-playbook.md` for the `content_ideas.md` output template.

**Gate**: Numbered atomic ideas saved to `content_ideas.md`. Each is specific and standalone. The file must exist before proceeding — context is not an artifact.

---

### Phase 3: DRAFT — Write Platform-Native Variants

Write one draft per target platform, each starting from the primary atomic idea (or specified idea) as raw material.

Every draft must be written from scratch for its platform. Do not write one version and shorten or trim it for others — audiences on each platform recognize content that was not written for them. No two platform drafts may share a verbatim sentence. If the LinkedIn draft opens with "This article covers..." or the X tweet says "New post: [title]. Key points: 1, 2, 3", that is a summary, not an adaptation. Summaries give readers no reason to stop scrolling.

Apply platform-specific rules — see `${CLAUDE_SKILL_DIR}/references/phase-playbook.md` for full detail on X, LinkedIn, TikTok, YouTube, and Newsletter register/hook/structure/length/hashtag/link/CTA rules, plus the `content_drafts.md` output template.

**Gate**: One draft per target platform saved to `content_drafts.md`. Self-check that no two drafts share a verbatim sentence before running scripts in Phase 4. The file must exist before proceeding.

---

### Phase 4: GATE — Quality Check Before Delivery

Mechanically verify drafts before delivery. Both script checks must exit 0. The gate cannot be bypassed — LLM self-assessment alone ("I reviewed the drafts and they look clean") misses hype phrases in context and cannot do verbatim comparison reliably. Run the scripts.

#### Check 1: Hype Phrase Scan

```bash
python3 ~/private-skills/scripts/scan-negative-framing.py content_drafts.md
```

See `${CLAUDE_SKILL_DIR}/references/phase-playbook.md` for the full list of banned hype phrases and replacement guidance.

**If exit non-zero**: Identify the flagged draft(s), rewrite only the affected sections, save to `content_drafts.md`, re-run the check. Do not proceed to Phase 5 until exit 0.

#### Check 2: Cross-Platform Verbatim Check

```bash
python3 ~/private-skills/scripts/scan-negative-framing.py content_drafts.md
```

This check identifies any sentence appearing verbatim in two or more platform sections of `content_drafts.md`.

**If exit non-zero**: Rewrite the flagged sentence(s) in one of the two platforms where they appear. The rewrite must be platform-native — not a synonym swap. Re-run the check. Do not proceed to Phase 5 until exit 0.

#### Secondary LLM Check (after scripts pass)

Once both scripts exit 0, verify:
- [ ] Each draft reads natively for its platform (register, length, formatting feel right)
- [ ] Every hook is strong and specific — not a topic sentence, not a summary opener
- [ ] CTAs match the stated goal and platform norms
- [ ] No placeholder text that cannot be published as-is (flag these, do not remove them)

**Gate**: Both script checks exit 0. All LLM checklist items confirmed. Update `content_drafts.md` status from `DRAFT — pending Phase 4 gate` to `READY`. Proceed to Phase 5 only when gate passes.

---

### Phase 5: DELIVER — Present Drafts with Posting Guidance

Hand off clean drafts with enough context for the user or a downstream skill to act immediately. See `${CLAUDE_SKILL_DIR}/references/phase-playbook.md` (Phase 5: Delivery Details) for delivery order, per-draft inclusions, downstream handoff table, optional behaviors, and artifact list.

---

## Error Handling

See `${CLAUDE_SKILL_DIR}/references/phase-playbook.md` for error cases: source too long, script flag unsupported, platform unspecified, ambiguous source, fewer than 3 ideas.

---

## References

| Signal | Load |
|--------|------|
| Phase 3 DRAFT — writing platform variants | `references/platform-specs.md`, `references/phase-playbook.md` |
| Phase 4 GATE — running quality checks | `references/phase-playbook.md`, `references/error-handling.md` |
| Script fails, gate won't pass, source errors | `references/error-handling.md` |
| Platform rules, character limits, posting norms | `references/platform-specs.md` |
| Delivery, handoff, artifact templates | `references/phase-playbook.md` |

- `${CLAUDE_SKILL_DIR}/references/platform-specs.md` — Character limits, format rules, and posting norms per platform
- `${CLAUDE_SKILL_DIR}/references/phase-playbook.md` — Full platform rules for Phase 3, banned hype phrases for Phase 4, error handling
- `${CLAUDE_SKILL_DIR}/references/error-handling.md` — Gate failure recovery, script fallbacks, error-fix mappings, detection commands
- `~/private-skills/scripts/scan-negative-framing.py` — Negative framing and hype phrase detection
