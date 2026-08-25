---
name: xray
description: Investigate how a concept, code path, application, network flow, system, incident, document, or local artifact actually works, then deliver a two-depth visual HTML explainer with a dead-simple big-picture first layer and source-backed technical depth behind it. Use when the user invokes $xray, asks how something works under the hood, wants a module or app behavior traced across boundaries, requests web, code, network, or safe static artifact research before explanation, or asks for an evidence-backed explainer. Do not use for answer-only definitions, general web design, full codebase audits, or invasive binary reverse engineering without explicit authorization.
---

# X-Ray Explainer

Investigate first and explain second. The HTML is a projection of verified understanding, not decoration around an early guess.

## Operating Boundary

- Directly perform read-only research, repository inspection, log/config examination, source archaeology, and creation of the requested explainer artifact.
- When the user asks to analyze a clearly identified app, CLI, or local compiled artifact they are entitled to inspect, include safe read-only static inspection when it can answer the teaching question. Record identity and hash first; inspect metadata, signatures, dependencies, imports, recoverable symbols, strings, entitlements, and bundled resources without modifying or executing the target.
- For an authorized native binary or compiled CLI, load `$claude-code-reverse` first and use its tested `extract.sh` workflow as the canonical identity, hash, cache, and safe static baseline. Do not duplicate that baseline inside X-Ray.
- When the canonical static baseline cannot establish the requested mechanism, or the authorized target is an APK, JavaScript bundle, or protocol flow, read [reverse-core.md](references/reverse-core.md). Load only the matching specialist adapter, use tools already available in the environment, and return its evidence to the ordinary X-Ray causal model. Reverse Core is an internal depth route, not a second user-facing skill or a reason to install a full security pack.
- Ask before executing an unknown binary, attaching a debugger, intercepting or decrypting traffic, patching an artifact, installing reverse-engineering tools, using a paid endpoint, touching production, accessing credentials, or changing product code.
- Never bypass access controls, fabricate evidence, or treat agreement between models as corroboration.
- If the target, revision, authorization, or intended audience would materially change the investigation, clarify that one fact before acting.

## Investigate

Read [research-routing.md](references/research-routing.md), then choose the narrowest route that can answer the question.

| Target | Default route |
|---|---|
| Stable concept with adequate supplied material | Explain from supplied evidence; verify pivotal facts only |
| Current, niche, disputed, or unfamiliar topic | Search the web; prefer primary and authoritative sources |
| Repository, module, app behavior, API path, or architecture | Trace the reachable path across code, network, persistence, and background work |
| Incident or wrong runtime behavior | Inspect persisted state, logs, metrics, running revision, then code |
| Clearly identified local app, CLI, or compiled artifact | Use `$claude-code-reverse` for the native static baseline, then load one Reverse Core specialist adapter only if the question remains unresolved |

Do not invoke extra agents or external AI systems by default. Add them only when the user requests delegation or a separate workflow explicitly requires it.

### 1. Frame the teaching question

Write one sentence naming what the reader must understand or decide after viewing the explainer. Default to a curious adult who is new to the topic; never infantilize the reader.

### 2. Acquire ground truth

Read [evidence-contract.md](references/evidence-contract.md). For code or runtime targets, also read [code-archaeology.md](references/code-archaeology.md).

- Establish the exact target and relevant version before explaining it.
- For a compiled target, record the artifact path, cryptographic hash, architecture, and signature before drawing conclusions. Treat strings, imports, symbols, and decompiled fragments as clues until another observation establishes their role.
- For authorized specialist reverse work, keep the reverse phase bounded to the teaching question. Prefer one reachable path over exhaustive decompilation, and bring exact addresses, symbols, tool versions, and uncertainty back into the same evidence model.
- Search the local target before searching the web for explanations of it.
- Use web research for current, niche, disputed, unfamiliar, or explicitly source-backed claims.
- For incidents, prefer the actual persisted state and running revision over remembered browser behavior or design intent.
- For application behavior, follow the user action through internal control flow, network boundaries, server handling, persistence or background work, and the result or failure path. Inspect or capture traffic only when it is safe, authorized, and materially useful.
- Keep exact URLs, code anchors, revision identifiers, timestamps, and uncertainty for the claims that matter to the explanation.

### 3. Form the causal model

- Write scratch notes in whatever form helps distinguish evidence from interpretation; do not create a manifest or fixed ledger unless the task genuinely benefits from one.
- Identify the input, meaningful transformations or decisions, state changes, outputs, and failure boundaries that explain the behavior. Use as many or as few steps as the mechanism needs.
- State confirmed behavior plainly. Label material inference and unknowns where a reader could otherwise mistake them for fact; do not badge every sentence mechanically.
- Preserve technical truths that affect behavior. Simplify vocabulary, not causality.
- Introduce a real mechanism before using an analogy. Label where the analogy stops matching reality.
- Keep unresolved contradictions and missing evidence visible.

### 4. Design the visual story

Read [visual-explanation.md](references/visual-explanation.md). Choose the diagram from the causal structure: flow, sequence, state machine, architecture, timeline, comparison, or a small simulator.

When the investigation produces meaningful technical evidence, project the same causal model at two depths:

- The orientation layer comes first. Give the shortest accurate answer and one dominant, plain-language visual that a newcomer can understand without reading the evidence layer. Lead with how the subject works, not what the researcher inspected.
- The evidence layer follows or expands on demand. Preserve code symbols, network branches, persistence, failure behavior, sources, and material unknowns for readers who want to verify or continue digging.

Keep the first layer visually quiet and low in terminology. Move implementation detail down instead of deleting it. Do not impose a fixed word count, step count, card count, or DOM structure; use the smallest first layer that carries the real mechanism. A genuinely simple topic does not need a padded second layer.

- Use [feature-explainer.html](assets/feature-explainer.html) or [concept-explainer.html](assets/concept-explainer.html) only as optional visual references. Freely change their structure, step count, sections, and styling; do not bend the explanation to fit a template.

### 5. Write for a person

- For a Chinese explainer, read and apply [chinese-writing.md](references/chinese-writing.md) after the evidence and causal model are stable. Use this built-in writing pass to revise headings, body copy, captions, and the handoff so the prose sounds like a knowledgeable person walking the reader through what they found.
- Keep technical literals, code symbols, versions, direct quotations, uncertainty, and citation meaning unchanged during the prose pass. When naturalness and precision conflict, preserve precision and rewrite the surrounding sentence.
- Let concrete observations carry the explanation. Remove report-like labels, repetitive summaries, symmetrical card copy, fake suspense, and generic insight phrases.
- For other languages, match the same audience-aware standard without forcing Chinese writing rules onto the text.

### 6. Render the artifact

- Produce one self-contained HTML file with inline CSS and SVG or canvas. Avoid remote fonts, scripts, images, and stylesheets; ordinary source links are allowed.
- Create the artifact in a temporary task directory by default. Put it in a project only when the user requests a durable project artifact.
- Organize the page around the teaching question. Do not force fixed sections, card counts, or diagram shapes.
- Keep the orientation layer visible before technical inventory, provenance, or methodology. Use progressive disclosure when the evidence layer would otherwise compete with the main explanation.
- Keep source markers adjacent to the claim or diagram step they support.
- Use JavaScript only when interaction materially teaches the mechanism.

### 7. Verify before delivery

Open or render the page at a desktop and narrow viewport when a renderer is available. Inspect clipping, overflow, legibility, unresolved placeholders, source-link behavior, and whether the visual sequence still makes sense without narration. Exercise any interaction that carries explanatory meaning. If no renderer is available, report visual verification as incomplete instead of implying it passed.

## Done When

- Pivotal claims are traceable to current evidence or explicitly labeled inference/unknown.
- Repository explanations include exact paths and symbols; web explanations include direct source URLs.
- Specialist reverse explanations identify the exact artifact and tool, preserve address or symbol anchors, distinguish static clues from reachable behavior, and disclose any action that crossed the static-analysis boundary.
- The mechanism is simpler than the source material without losing a behavior-changing fact.
- A reader can understand and remember the central mechanism from the orientation layer alone, while the evidence layer still supports the technical claims.
- Chinese prose has received the built-in Chinese writing pass without changing evidence or technical meaning.
- The page has been checked in proportion to its complexity; when possible, it has been visually inspected at wide and narrow widths.
- The final response links the artifact and briefly states sources, uncertainty, and any boundary that prevented deeper investigation.

## Gotchas

- “Few words” does not mean “few facts.” Remove repetition before removing causal steps.
- Deep research does not earn the first screen. Packaging, methodology, provider matrices, hashes, and source inventories belong below the central mechanism unless one of them is the teaching question.
- A beautiful diagram of an unverified mechanism is still wrong.
- Safe static inspection of an identified local artifact belongs in ordinary X-Ray investigation. Debugging, interception, patching, protection bypass, credential access, and execution of an unknown artifact are separate authorization levels.
- Multiple model answers are leads, not independent sources.
- Local code and runtime evidence outrank generic web explanations of a similarly named system.
- Do not turn the investigation into an exhaustive audit. Stop when further research would add detail without changing the causal model.
- Do not dump a reverse-engineering tool inventory into the explainer. Load one matching adapter, collect the evidence that changes the causal model, then return to X-Ray.
- Do not turn quality guidance into a hardcoded content validator. Use judgment for semantic quality and ordinary rendering or syntax checks for mechanical defects.
- Do not let a prose rewrite strengthen a claim, erase a limitation, or detach a citation from the fact it supports.
- Avoid decorative dashboards, excessive cards, and meaningless animation. Every visual element must teach a relationship.
- When evidence is insufficient, explain what is known, what is unknown, and the next cheapest observation that would resolve it.

## Drift and Feedback

Representative prompts live in [evals/evals.json](evals/evals.json). When a run produces invented anchors, missing citations, shallow research, text walls, or a misleading visual structure, patch the smallest responsible instruction, reference, template, or eval case rather than expanding the main instructions indiscriminately.
