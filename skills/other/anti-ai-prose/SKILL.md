---
name: anti-ai-prose
description: >
  · Audit prose for AI tells in docs, PRs, emails, slides, docstrings. Triggers: 'ai writing', 'sounds like chatgpt', 'ai slop prose', 'llm voice', 'sound human'. Not for code (use anti-slop).
license: MIT
compatibility: "None - works on any prose or text input"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-09"
  effort: medium
  argument_hint: "<file-or-text>"
---

# Anti-AI-Prose: Audit Writing for Machine-Generated Patterns

Detect and fix the linguistic tells that make written English read as machine-generated. The goal is prose that sounds like a specific, thoughtful human wrote it.

This skill applies to any text: **documentation**, **READMEs**, **wikis** (Confluence, Notion, internal), **pull request descriptions**, **commit messages**, **release notes**, **blog posts**, **emails**, **slide copy**, **creative writing**, and **code comments / docstrings**. The vocabulary, syntax, tone, and formatting checks are language-domain, not platform-domain.

Based in part on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - a field guide compiled by editors who have read enormous volumes of LLM-generated text and know what it actually looks like.

## When to use

- Auditing a README, doc page, or wiki article that feels machine-written
- Reviewing a PR body, commit message, or release note draft before publishing
- Polishing a blog post, email, or presentation script you wrote with LLM help
- Checking creative writing (fiction, essays) for AI tells after an LLM-assisted pass
- Reviewing docstrings and code comments for the same prose patterns
- Any time someone says "this sounds like ChatGPT wrote it"
- Self-check after a heavy LLM-drafting session

## When NOT to use

- Code quality, over-abstraction, dependency creep, stale idioms - use **anti-slop**
- Doc drift after a feature change, API rename, or config update - use **update-docs**
- Generating or restructuring a prompt from rough notes - use **prompt-generator**
- Correctness bugs, logic errors, edge cases - use **code-review**
- Security review of auth, secrets, or attack surface - use **security-audit**
- Full multi-dimensional repo audit - use **full-review**

---

## AI Self-Check

Before returning any audit, verify:

- [ ] **Findings are patterns, not taste**: the issue is a demonstrable AI tell (from the Wikipedia guide or observed LLM output), not personal writing preference
- [ ] **Context respected**: academic and technical prose can look formal without being AI-generated. Journalism, marketing, and tourism writing have legitimate conventions that overlap with AI tells. Do not flag genre conventions as AI tells
- [ ] **Direct quotes preserved**: do not edit quoted material from other authors, even if it contains banned vocabulary
- [ ] **Domain terms kept**: `pivotal` in hinge hardware specs, `landscape` in horticulture, `foster` as a verb in child welfare, `realm` in fantasy fiction - these are not tells in context
- [ ] **Code blocks untouched**: do not flag identifiers, strings, or code comments that contain banned words as part of functional code
- [ ] **Rewrites are real improvements**: every "after" is shorter, clearer, or more specific than the "before". No lateral rewrites that just swap synonyms
- [ ] **Severity is honest**: do not inflate P3 findings to P2 to pad the report
- [ ] **Density and short-text rule applied**: density heuristic applied before assigning severity; for text under 100 words, 2+ tells in one paragraph = P1 regardless of per-500-word threshold
- [ ] **Audit output itself uses no AI-prose tells** (apply these rules to your own output)
- [ ] **AI fallback names checked (fiction)**: protagonist and major-character names compared against the documented fallback set (Elara, Lyra, Aurora, Kael, Vale, Cassius, etc.) and the phonetic tell (2 soft syllables, A/L/R/N consonants, no demographic anchor); fallback-set names allowed only when the setting and population organically produce them
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Adverb stacking checked**: `-ly` adverb density scanned; passages with multiple adverb-modified speech tags or adjacent adverb clusters flagged at the same density threshold as vocabulary tells
- [ ] **Overflagging avoided**: plain but valid technical prose is not labeled AI-written without concrete evidence
- [ ] **Audience preserved**: edits keep the author's domain vocabulary, intent, and required formality

---

## Performance

- Review a representative sample first, then expand only if the same pattern repeats across the document.
- Group repeated prose issues by pattern instead of leaving near-duplicate comments on every paragraph.
- Prioritize high-visibility text: titles, summaries, intros, conclusions, and user-facing docs.

---

## Best Practices

- Flag exact phrases and structural patterns, not vibes.
- Offer replacement copy when the fix is obvious; otherwise describe the problem and let the author decide.
- Do not erase necessary caveats, compliance language, or domain-specific precision to make prose sound casual.

## Workflow

### Step 1: Scope the audit

Default scope based on context:
- If invoked on a specific file or paste - audit that text
- If invoked with no target and there are uncommitted changes to `.md` / `.txt` / doc files - audit those
- If invoked in a code repo with recent commits - audit the docstrings and comments in changed files
- Otherwise - ask the user for a target

Available scopes:
- **Single file** - one doc, README, draft, or source file
- **Directory** - all `.md` / `.rst` / `.txt` under a path
- **Pasted text** - inline block the user supplies
- **Recent changes** - git diff against a base
- **Comments and docstrings only** - scan code files but audit only prose regions

### Step 2: Detect text kind

Different text types have different conventions. Before flagging, identify which applies:
- **Technical docs** - formal is OK, but vocabulary bans still apply
- **README / PR / commit** - concise is expected, significance padding is especially jarring
- **Marketing / product copy** - tonal tells (`boast`, `showcase`) may be intentional but still weaken the writing
- **Creative fiction** - many tells (tricolons, elegant variation) are legitimate devices; flag only when they read as mechanical
- **Wiki article** - neutral voice required, promotional language is always a finding
- **Email** - conversational is expected, formality inflation is a tell
- **Slides / presentation** - fragments are fine, but vocabulary and tonal tells still apply

### Step 3: Scan for patterns

Apply the four categories (see below). For each match, read the surrounding context - a single instance of an AI word in a 5000-word document is probably noise, but three instances in three paragraphs is a pattern.

**Density heuristic** (rough guide, not a hard rule):
- **Under 1 flagged item per 500 words** - noise, usually do not flag
- **2-3 per 500 words** - a pattern, flag the cluster as P2
- **4+ per 500 words** - dominant voice, P1 severity, recommend structural rewrite

**Short text scaling:** for text under 100 words, any 2+ tells in a single paragraph is P1 severity regardless of the per-500-words threshold. A single sentence crammed with AI vocabulary is worse than a long doc with scattered instances.

Density only applies to vocabulary and syntax tells. A single travel-guide paragraph is enough to flag on its own. One fabricated citation is always P1.

Classify each finding by category, action, and severity:

**Action:**
- **Fix** - clearly a tell, should change
- **Consider** - judgment call, present it and let the user decide
- **Fine** - matches the pattern but is justified (note why, move on)

**Severity:**
- **P1** - cluster of tells that makes the piece sound unmistakably AI-written; vague attribution passing opinion as fact; fabricated citations or broken references
- **P2** - vocabulary or syntax tells that dull the voice without breaking trust; formulaic structures ("Despite its X, faces challenges..."); travel-guide voice in non-travel writing
- **P3** - single instances of banned vocabulary; formatting nits (em-dash usage, unnecessary bold); tricolon overuse

### Step 4: Report and fix

Present findings grouped by category. For each Fix-level item, show the concrete rewrite. Rewrites should be **shorter** or **more specific** - never longer.

**Plan first, apply that plan only.** Produce the audit report as the improvement plan before any
rewrites are merged. If the user then asks for the fixes to be applied, change only what the plan
flagged. Do not freelance edits outside the plan, do not "while we're here" rewrite adjacent
prose, and do not chain a second pass of new fixes on top of the applied ones in the same step.
This keeps the work auditable and prevents a cheap model from re-drafting the piece worse than
the original. If new findings emerge while applying, surface them as a second audit, not as
silent edits.

---

## The Four Categories of AI Prose Slop

### 1. Vocabulary Tells (Noise)

Specific words that LLMs overuse far beyond their natural English frequency.

**Flagged vocabulary** (context-sensitive - see exceptions below):

| AI word | Natural alternatives |
|---|---|
| delve | look at, examine, dig into, cover |
| tapestry | mix, range, variety (or just drop the metaphor) |
| testament | proof, evidence, example |
| pivotal | key, important, central (or drop if padding) |
| crucial | important, needed (or drop if padding) |
| realm | area, field, world |
| landscape | scene, field, mix |
| showcase | show, display, feature |
| empower | help, enable, let (or rewrite with a specific claim) |
| foster | build, grow, support, encourage |
| navigate | handle, work through, manage |
| nestled | set, located, built |
| vibrant | lively, active, busy (or drop) |
| underscore | show, highlight, confirm |
| garner | get, earn, attract |
| enduring | lasting, long-running |
| boast | have (just "has") |
| leverage | use |
| utilize | use |
| facilitate | help, enable |
| seamless | smooth (or drop) |
| robust | reliable, solid (or drop if padding) |
| commitment to | cares about, focuses on |
| dive deep into | look at, cover |
| embark on | start, begin |
| nuanced | subtle, careful, specific (or drop - almost always padding) |
| multifaceted | has many sides, covers a lot (or drop) |
| holistic | whole, end-to-end, full (or drop) |
| synergy | fit, overlap, how X and Y work together (or drop) |
| innovative | new, novel (or name what is new) |
| commence | start, begin |
| journey toward | work toward, move toward, aim for (or drop) |
| moving forward | from now on, next, going forward (or drop) |

**Detect:**
- Multiple flagged words in the same paragraph
- Flagged word used metaphorically (`tapestry of experiences`, `realm of possibility`)
- Flagged word in a context where a plain verb would work (`showcase the features` -> `show the features`)

**Fix:** Replace with the plain alternative. If the sentence gets weaker after replacement, the original was padding - cut the whole phrase.

See "What NOT to Flag" below for domain exceptions (horticulture `landscape`, child welfare `foster`, networking `realm`, etc.).

#### AI fallback character names (fiction)

Generated fiction often converges on soft, no-baggage names such as `Elara`, `Kael`, or
`Voss`. If a prose audit includes invented character names, read
`references/fiction-name-tells.md` for the fallback-name pattern, exceptions, and fix guidance.

### 2. Syntax Tells (Noise + Soul)

Sentence structures LLMs reach for to sound balanced or significant.

#### Negative parallelism

LLMs overuse `not X but Y` and `not just X, but also Y` constructions to signal balance and sophistication. In moderation this is fine English. In quantity it is a clear tell.

**Detect:**
- Three or more `not X but Y` / `not just X, but Y` / `it's not about X, it's about Y` structures in a single piece
- Used where a direct claim would work: `this isn't just a tool, it's a platform` -> `this is a platform`

**Fix:** State the positive claim directly. If the contrast matters, keep one instance and rewrite the rest.

#### Forced tricolons (rule of three)

`X, Y, and Z` lists used for rhythm rather than enumeration. LLMs default to three items even when two or four would be more accurate.

**Detect:**
- Adjective triplets where one adjective would carry the meaning: `a fast, reliable, and scalable system`
- Noun triplets that are really the same concept: `clarity, precision, and accuracy`
- Three-item lists where the third item is obviously padded to hit the count

**Fix:** Drop the weakest item. Use two items when the point is a contrast, four or more when it is an actual list.

#### Copula avoidance

LLMs avoid plain `is` / `are` / `has` / `have` in favor of elaborate constructions: `serves as`, `marks`, `represents`, `features`, `offers`, `boasts`, `stands as`.

**Detect:**
- `serves as` where `is` works: `it serves as a backup` -> `it is a backup`
- `represents` used as a replacement for `is`: `this represents a shift` -> `this is a shift`
- `boasts` used for `has`: `the app boasts 50 features` -> `the app has 50 features`
- `marks` used to inflate: `this marks the first time` -> `this is the first time`

**Fix:** Use the plain copula. Elaborate verbs should carry weight - do not spend them on simple identity claims.

#### Adverb crutch (-ly modifiers)

LLMs reach for `-ly` adverbs to inflate description and dodge precise verb choice: `said softly`, `ran quickly`, `smiled warmly`, `walked slowly`, `whispered quietly`. Each one in isolation is acceptable English. Density is the tell. The classical fiction-editing test (Stephen King and most line editors): if dropping the adverb does not change the meaning, the verb is the problem.

**Detect:**
- `-ly` adverbs modifying speech tags: `said softly`, `whispered quietly`, `shouted loudly`, `replied curtly`
- Adverbs that restate the verb: `whispered quietly`, `shouted loudly`, `ran quickly`, `mumbled under his breath`
- Multiple `-ly` adverbs in adjacent sentences (a passage sprinkled with them rather than one used for emphasis)
- Stacking with hedges: `gently`, `slightly`, `rather`, `somewhat` modifying the same verb or following each other across a paragraph (cross-references "Hedging and qualifier stacking" in Tonal Tells)

**Fix:** Prefer a stronger verb. `said softly` -> `whispered`. `ran quickly` -> `sprinted`. `smiled warmly` -> `beamed`. `looked carefully at` -> `studied`. Delete adverbs that restate the verb outright.

**Exception:** Keep the adverb when it carries information the verb cannot. `said reluctantly`, `answered honestly`, `arrived late`, `she nodded slowly` (when the slowness is the point) all earn their place. The test: drop the adverb. If meaning shifts, keep it. If only rhythm shifts, the verb was weak.

#### Elegant variation

LLMs avoid repeating a noun within a paragraph, substituting increasingly strained synonyms. A character named Alice becomes `the protagonist`, `the main character`, `the young woman`, `the eponymous heroine` in four consecutive sentences.

**Detect:**
- The same entity referred to by 3+ different nouns in close proximity
- Strained synonyms where a pronoun or name repetition would be natural
- Different technical terms for the same concept within one document

**Fix:** Use the name, or a pronoun. Repetition is fine. Forced variation is worse than repetition.

### 3. Tonal Tells (Soul)

The voice of the text gives away the author even when the words are individually defensible.

#### Travel-guide voice

`Nestled between rolling hills, this vibrant city boasts a rich cultural heritage and a thriving arts scene`. LLMs default to this register for any geographic or cultural topic.

**Detect:** `nestled`, `rolling hills`, `vibrant`, `thriving`, `rich heritage`, `bustling`, `charming`, `picturesque`

**Fix:** State facts. `The city has 300,000 people, two universities, and a jazz festival in August.`

#### Promotional tone

`Our commitment to excellence ensures we foster innovation and empower our customers to succeed.` LLMs reach for press-release cadence when asked to describe any organization or product.

**Detect:** `commitment to`, `empower`, `foster`, `ensure`, `strive`, `dedicated to`, `passionate about`, `industry-leading`, `cutting-edge`, `next-generation`

**Fix:** Replace with specific claims. `We help X customers do Y` beats `We empower customers to succeed`.

#### Vague attribution

`Experts say`, `industry reports indicate`, `observers have noted`, `many believe`. LLMs use these when they want to assert something without a source. Real writers either cite or own the claim.

**Detect:**
- `experts say` / `experts agree` without naming experts
- `industry reports` / `studies show` without a study
- `observers have noted` / `critics argue` without names
- Plural `sources say` pointing to at most one source

**Fix:** Cite the source. Or own the claim. Or cut it - most of the time the surrounding sentence works without the attribution.

#### Significance padding

`This marks a pivotal moment, underscoring broader trends in the industry.` LLMs inflate the weight of routine events to pad word count.

**Detect:**
- `marks a pivotal moment`
- `underscoring broader trends`
- `highlighting the importance of`
- `serves as a reminder that`
- `in an era where`
- `in today's fast-paced world`

**Fix:** Delete the whole sentence. If what follows does not make sense without the padding, rewrite the surrounding paragraph.

#### Hedging and qualifier stacking

LLMs stack hedges and qualifiers to sound cautious or balanced. Each hedge by itself is fine English; stacking them makes every claim feel tentative.

**Detect:**
- Frequent `generally`, `typically`, `often`, `usually`, `in many cases`, `for the most part`
- Weak modal stacking: `may`, `can`, `might`, `could potentially`, `arguably`, `relatively`
- Two or more hedges in the same clause: `can generally be considered to be relatively reliable`
- Hedges on claims that the author clearly knows are true: `this may help with performance` (when benchmarks are already in the paragraph)

**Fix:** Delete the hedge and state the claim. If the claim really does need a caveat, state it concretely: `on Linux only`, `for connections over 1000 RPS` - not `generally speaking`.

#### Scaffolding padding

Phrases that wrap around the actual content without adding information. LLMs lean on these to sound organized or conversational.

**Detect:**
- `it's worth noting that`, `it's important to note`, `it's worth mentioning`
- `in this article, we'll explore` / `in this guide, we'll cover` (meta-commentary about the piece itself)
- `let's dive into` / `let's explore` / `let's take a look at`
- `here's the thing:` / `the fact is:` / `the truth is:`
- `at the end of the day` / `when all is said and done`
- `as we've seen` / `as mentioned earlier` / `as previously discussed` (when the reader just read it)

**Fix:** Cut the wrapper and keep the content. `It's worth noting that X` becomes `X`. `In this article, we'll explore Y` becomes a first sentence that is about Y.

#### "Despite its X, faces challenges"

LLMs reach for a formula when asked to describe any organization or project: positives first, then a "however" paragraph listing challenges, often ending with a "future outlook" paragraph.

**Detect:** the shape of the article more than specific words. Three-paragraph structure where paragraph 1 is positive, paragraph 2 starts with `Despite` or `However`, and paragraph 3 starts with `Looking ahead` or `The future`.

**Fix:** Reorganize around the actual story. If there is no story, the piece probably should not exist.

### 4. Formatting Tells (Noise)

Layout and punctuation patterns that LLMs default to.

**Detect:**
- **Em dashes** (Unicode U+2014, or the `--` double-dash substitute) used as sentence breaks. LLMs overuse them to imitate journalistic cadence. Replace with single `-` or restructure the sentence.
- **Title Case in section headings** (`Understanding the Core Concepts` vs `Understanding the core concepts`). AI defaults to title case even in sentence-case conventions. Match the project's style.
- **Excessive bold** - every third noun bolded for no reason. Bold earns its use by signaling a term or path.
- **Bullet salad** - prose turned into bullets when a paragraph would read better. Lists are for enumerations, not for every idea.
- **Three-bullet-happy layouts** - suspicious when every list has exactly three items
- **Curly quotes** (`"`, `'`) in technical writing that should use ASCII
- **Emoji** in professional prose where decoration is the only purpose
- **Decorative thematic breaks** - `---` before every `##`. Dividers that mark a real phase change are fine; decoration is not
- **Markdown artifacts in rendered text** - `**bold**` appearing as literal characters because the paste lost its format
- **LLM output bugs** - `turn0search0`, `contentReference`, `oaicite`, `+1`, `attached_file`, hallucinated wiki-style shortcuts

**Fix:** Match the surrounding project's conventions. If there is no convention, default to plain ASCII, sentence case, minimal bold, paragraph prose.

---

## What NOT to Flag

These look like AI tells but are not:

- **Direct quotations** - do not edit words written by someone else, even if they contain banned vocabulary
- **Genre conventions** - travel writing uses travel-guide voice because that is what travel writing sounds like. Marketing copy uses promotional tone. Journalism uses em-dashes. Fiction uses elegant variation and tricolons intentionally. Respect the genre.
- **Technical terms of art** - `pivotal` in mechanical engineering, `realm` in networking or identity (Kerberos, OIDC), `foster` in child welfare, `landscape` in horticulture or graphic design, `crucial experiment` in philosophy of science
- `landscape` in ML/AI contexts (optimization landscape, loss landscape, feature landscape)
- `robust` in statistics/ML (robust estimation, robust optimization, robust regression)
- **Deliberate register play** - satire, parody, pastiche, and stylistic experiments
- **Direct speech / dialog** in fiction - characters can sound however they sound
- **Lists that are actually lists** - a three-item list is only suspicious if the items are padded. An enumeration of three real things is fine
- **Bold where it signals a term or path** - bolding a defined term on first use is standard
- **Em dashes in publications that require them** - some style guides (Chicago, AP) allow or require em dashes. The rule applies to your project's conventions

### Counter-example (prose that looks AI but is fine)

> Nestled in the loss landscape near a sharp minimum, the model's robust features fail to generalize. This underscores a pivotal result from Keskar et al. (2017): flat minima tend to foster better test accuracy than sharp ones.

Looks flagged at a glance: `nestled`, `landscape`, `robust`, `underscores`, `pivotal`, `foster`. But every term is a term of art (ML optimization, statistics), `underscores` has a real referent, and the citation is real. Verdict: **Fine**. Do not flag. Domain context overrides vocabulary match.

---

## Output Format

````markdown
## Anti-AI-Prose Audit: [scope]

### Findings

#### [Category Name] ([count] items)

**[action]** ([severity]) `path/to/file:line` - [description]

> before: [quoted text from the source]

> after: [suggested rewrite]

### Summary
- X findings across Y files / sections
- [overall read: does the piece sound human?]
- [top-level observation: e.g., "vocabulary is mostly fine but the structure is formulaic"]
````

Rules for the report itself:
- **Omit empty categories.** If there are no formatting tells, do not write an empty "Formatting Tells (0 items)" heading
- **Order within a category** P1 > P2 > P3
- **Deletion fixes have no "after"** - write `> after: (cut)` or just state the delete in the description
- **Apply these rules to your own audit.** Run the Self-Check on the report before returning it - an audit written in AI-slop voice is not credible

Keep it concise. Show the before/after pair. Do not lecture about why AI writing is bad - the user already knows.

### Worked example (anchor the format)

Input (README snippet, 48 words):

> In today's fast-paced world, our platform empowers developers to seamlessly navigate the complex landscape of modern APIs. Built with a commitment to excellence, it boasts robust features and fosters innovation. Whether you're a beginner or expert, this tool serves as a pivotal resource for your journey toward better software.

Report:

```
## Anti-AI-Prose Audit: README snippet (48 words)

### Findings

#### Vocabulary Tells (9 items)

**Fix** (P1) line 1 - cluster of 9 flagged words in 48 words: far above 4/500 threshold
> before: empowers / seamlessly / navigate / landscape / commitment to / boasts / fosters / pivotal / journey toward
> after: (rewrite, see below)

#### Tonal Tells (2 items)

**Fix** (P1) line 1 - scaffolding padding and significance padding
> before: "In today's fast-paced world"
> after: (cut)

**Fix** (P2) line 1 - promotional tone
> before: "Built with a commitment to excellence"
> after: (cut)

### Summary
- 11 findings, one paragraph, dominant AI voice
- Rewrite: "An HTTP API client for Python. Handles auth, retries, and pagination. Works with any OpenAPI 3.x spec."
- Down from 48 words to 22, with concrete claims instead of posture
```

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** ANTI-AI-PROSE
- **Deliverable bucket:** `audits`
- **Mode:** always-on. Every invocation emits the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table.
- **Deliverable path:** `docs/local/audits/anti-ai-prose/<YYYY-MM-DD>-<slug>.md`
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract).

## Related Skills

- **anti-slop** - code quality audit. When auditing a repo, run anti-slop for code and anti-ai-prose for docs. The two are deliberately complementary.
- **update-docs** - keeps docs accurate and trimmed after feature changes. Anti-ai-prose focuses on voice; update-docs focuses on factual drift.
- **prompt-generator** - structures a rough draft into an LLM prompt. If the user wants to generate cleaner prose next time, this helps shape the prompt.
- **full-review** - orchestrates code-review, anti-slop, security-audit, and update-docs. Not wired into full-review by default - invoke anti-ai-prose separately when the repo has substantial prose worth auditing.
- **code-review** - catches logic and correctness issues. Anti-ai-prose only touches prose; code-review handles the code itself.

---

## Rules

1. **Read the full piece before flagging.** A single `delve` in a 10,000-word book is not a pattern. Three in a paragraph is. Context determines severity.
2. **Never edit quoted material.** Original words from other authors stay as written.
3. **Respect genre conventions.** Travel writing, marketing, fiction, and academic prose have legitimate conventions that overlap with AI tells. Flag only when the writing is worse for the device, not because it matches a pattern.
4. **Every rewrite must be shorter or more specific.** Lateral synonym swaps are not improvements. If the rewrite is longer, the original was fine.
5. **Plan first, apply that plan only.** When applying fixes after the audit, change only what the report flagged. Do not freelance edits, do not rewrite adjacent prose, and do not chain a second pass of new fixes on top of the applied ones. New findings during application become a follow-up audit, not silent edits.
6. **Keep the voice of the author.** The goal is prose that sounds like a specific human, not a generic "good writing" rewrite. If you do not know the author's voice, leave stylistic calls alone and only flag the mechanical tells.
7. **Do not pad the report.** If there are three findings, list three. Not five. Not one inflated to three.
8. **Run the AI Self-Check** before returning any audit.
