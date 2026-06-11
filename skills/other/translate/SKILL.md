---
name: translate
description: "Document translation: quick/normal/refined modes with chunked parallel subagents and glossary support."
user-invocable: true
routing:
  category: content
  triggers:
    - translate
    - translation
    - localize
    - localise
    - into English
    - into Spanish
    - into French
    - into Japanese
    - into Chinese
    - into German
    - into Portuguese
    - from English to
    - convert language
  not_for: "reformatting or restructuring text without changing language"
  pairs_with:
    - professional-communication
    - publish
    - voice-writer
---

# Translate Skill

Translate documents across languages using one of three modes: quick (single-pass), normal (analyze-then-translate), or refined (full four-step with polish). Core principle: **rewrite as a skilled native writer**, not word-for-word conversion.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Any translation task | `references/modes.md` | Mode detection, chunking algorithm, parallel dispatch pattern |
| "technical", "specialized", "glossary", "terms", or domain vocabulary in request | `references/glossary-template.md` | Glossary build, chunk injection, term-preservation rules |

---

## Phase 1: DETECT MODE AND PREPARE

**Goal**: Identify mode, language pair, and document scale before any translation work.

**Step 1: Infer mode from request language**

| Request contains | Mode |
|---|---|
| "quick", "fast", "draft", "rough" | quick |
| "professional", "publication-quality", "polished", "refined" | refined |
| anything else | normal (default) |

**Step 2: Detect language pair**

- Source language: identify from content if not stated; flag ambiguity to user.
- Target language: take from request; ask if absent.

**Step 3: Load references**

- Load `references/modes.md` for all modes.
- Load `references/glossary-template.md` when the request contains "technical", "specialized", "glossary", "terms", or a domain-specific vocabulary word.

**Step 4: Assess document size**

- Count approximate words.
- Flag documents over 2000 words for chunked parallel translation (details in `references/modes.md`).

**Gate**: Mode, language pair, and size class confirmed. Proceed only when gate passes.

---

## Phase 2: ANALYZE

**Goal**: Extract structural and stylistic facts that guide accurate translation. Skip this phase in quick mode.

**Step 1: Language and dialect**

State the identified source language and dialect (e.g., Brazilian Portuguese vs European Portuguese, Simplified vs Traditional Chinese).

**Step 2: Register and tone**

Classify as one of: academic, technical, narrative, marketing, casual, legal. Register determines word-choice formality in the target language.

**Step 3: Document type**

Classify as one of: article, code comments, game text, marketing copy, legal text, UI strings, chat/informal. Document type determines sentence length conventions and formatting expectations in the target.

**Step 4: Specialized terminology**

List domain-specific terms that need consistent translation or should stay in the source language. For technical content, build an initial glossary using the format in `references/glossary-template.md`.

**Gate**: Language/dialect, register, document type, and terminology list complete. Proceed only when gate passes.

---

## Phase 3: TRANSLATE

**Goal**: Produce the translation using mode-specific approach from `references/modes.md`.

**Translation principles** (apply in all modes):

- Use idiomatic target-language word order, not source-language structure.
- Break long source sentences at natural target-language pause points.
- Render metaphors by their intended meaning, not literal equivalent.
- Annotate specialized terms on first occurrence: "machine learning (机器学习)".
- Match the register (formal/informal) established in Phase 2.
- Preserve source-language terms for proper nouns, brand names, and internationally recognized technical identifiers.

**For documents over 2000 words**: apply the chunking algorithm from `references/modes.md` — split at heading or paragraph boundaries, build a session glossary, dispatch parallel subagent calls per chunk with glossary injected, reassemble preserving document structure.

**Output file**: write translation to `{source-file-stem}-{target-lang}.md` when a source file is present. For inline text, deliver in-response.

**Gate**: All chunks translated, glossary consistent across chunks, document structure intact. Proceed only when gate passes.

---

## Phase 4: POLISH

**Goal**: Improve register consistency and idiomatic flow. Apply in refined mode only.

**Step 1: Register consistency scan**

Read the full translated output. Flag passages where formality level shifts unexpectedly.

**Step 2: Idiom review**

Identify literal-sounding constructions that a skilled native writer would phrase differently. Rewrite each flagged passage.

**Step 3: Specialized term audit**

Confirm every specialized term is handled consistently: annotated on first use, same translation throughout, source-language terms preserved where appropriate.

**Gate**: Register consistent, idiomatic constructions improved, term handling verified. Proceed only when gate passes.

---

## Phase 5: DELIVER

**Goal**: Report outcome with full traceability.

Deliver a brief summary:

```
Source: {source-file or "inline text"} ({source-language})
Target: {output-file or "inline"} ({target-language})
Mode: {quick | normal | refined}
Words translated: ~{count}
Chunks: {N} (if chunked)
Untranslated terms: {list with reasons, or "none"}
```

For multi-chunk documents, list any terms that differ between chunks and confirm the session glossary resolved them.

---

## Error Handling

### Ambiguous source language
Ask the user to confirm before translating. Guessing produces plausible but wrong output for closely related languages (Serbian vs Croatian, Malay vs Indonesian).

### Untranslatable term
Preserve the source-language term, add a bracketed explanation in target language on first use, and list the term in the delivery summary with the reason it was kept.

### Inconsistency detected across chunks
Re-translate the inconsistent chunk with the session glossary injected, replace the passage, and note the correction in the delivery summary.

### Source file has mixed languages
Treat each section by its actual language. Flag the structure to the user in the delivery summary.

---

## References

- `references/modes.md` — Mode detection table, quick/normal/refined workflow, chunk detection threshold, chunking algorithm, parallel dispatch pattern
- `references/glossary-template.md` — Glossary format, build procedure, chunk injection, term-preservation rules, example glossary
