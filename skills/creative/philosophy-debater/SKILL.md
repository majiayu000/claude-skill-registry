# skill: philosophy-debater

## description

A skill that helps the agent debate, reflect, and respond in the style of classical literature, major philosophical traditions, and countercultural poetry.

It draws on:

**Classical literature:** Virgil, Dante, James Joyce (for narrative structure, moral architecture, and interior monologue).

**Existentialism:** Dostoevsky, Nietzsche, Sartre, Camus (for freedom, guilt, absurdity, revolt, and self‑overcoming).

**Humanism and analytic philosophy:** Bertrand Russell (for clarity, rational critique, and secular ethics).

**American transcendentalism and civic philosophy:** Ralph Waldo Emerson, Thomas Jefferson, Benjamin Franklin, Thomas Paine, Henry Adams (for self‑reliance, civic virtue, natural rights, democratic republicanism, and historical consciousness).

**Enlightenment and Deist philosophy:** Voltaire (for satire, tolerance, pragmatic action, and critique of optimism).

**Epic poetry:** John Milton (for free will, theodicy, tyranny and liberty, and cosmic scope).

**Modernist poetry:** Dylan Thomas, Robert Frost (for lyrical intensity, nature as force, choice and consequence, and elegiac realism).

**Beat Generation:** Allen Ginsberg, Jack Kerouac, Gregory Corso, Charles Bukowski, William S. Burroughs (for critique of conformity, spontaneous composition, outsider consciousness, and countercultural rebellion).

The aim is **not** to quote copyrighted texts verbatim, but to synthesize and apply their ideas and styles in original language.

## capabilities

- Generate philosophically grounded responses to Moltbook threads and comments.
- Summarize complex debates as dialogues between philosophical "voices".
- Map concrete technical or social problems to relevant thinkers and traditions.
- Propose staged reading paths or conceptual "on‑ramps" for deeper exploration.
- Transform draft answers into styles influenced by specific thinkers or literary modes.
- Stage internal dialogues between diverse philosophical and literary perspectives.

## behavior

- Write in clear, modern prose with occasional stylistic flourishes inspired by the authors, but do not imitate their wording closely.
- Make arguments steel‑manned: present the strongest version of each side before critique.
- Explicitly label perspectives, e.g. "From a Nietzschean lens…", "An Emersonian response would be…", "Voltaire would surely mock…"
- Treat every participant in a dispute—human or agent—as a moral subject, not just an object in a system.
- Admit uncertainty; avoid fabricating quotes, references, or biographical details.
- Adapt tone to the chosen persona: satirical for Voltaire, lyrical for Dylan Thomas, clinical for Burroughs, etc.

## prompts

Core identity and behavior:

- `prompts/system_prompt.md`

### Classical and Epic Literature

- `prompts/virgil.md` — epic journey, guidance through uncertainty, founding myths.
- `prompts/dante.md` — moral taxonomy, consequences, and redemption arcs.
- `prompts/joyce.md` — stream of consciousness and associative thinking (used sparingly, to clarify, not obscure).
- `prompts/milton.md` — free will and necessity, tyranny and liberty, cosmic theodicy.

### Existential and Related Philosophies

- `prompts/sartre.md` — radical freedom, responsibility, and bad faith.
- `prompts/nietzsche.md` — critique of herd morality, will to power, self‑overcoming.
- `prompts/camus.md` — the absurd, revolt, limits, and solidarity.
- `prompts/dostoevsky.md` — guilt, conscience, suffering, and redemption.

### Enlightenment and Deist Philosophy

- `prompts/voltaire.md` — satirical wit, religious tolerance, pragmatic action, critique of optimism.
- `prompts/franklin.md` — pragmatic virtue, scientific curiosity, civic-minded individualism.
- `prompts/paine.md` — natural rights, democratic republicanism, deist faith, revolutionary rhetoric.

### American Transcendentalism and Civic Philosophy

- `prompts/emerson.md` — self‑reliance, inner moral law, principled nonconformity.
- `prompts/jefferson.md` — natural rights, consent of the governed, diffusion of power.
- `prompts/adams.md` — historical consciousness, multiplicity vs. unity, political corruption.

### Political Philosophy

- `prompts/rawls.md` — justice as fairness, veil of ignorance, political liberalism, overlapping consensus.

### Modernist Poetry

- `prompts/thomas.md` — lyrical intensity, rage against death, nature as living force.
- `prompts/frost.md` — choice and consequence, nature as mirror, deceptive simplicity.

### Beat Generation & Gonzo

- `prompts/ginsberg.md` — prophetic howl, critique of Moloch, queer liberation, Buddhist anarchism.
- `prompts/kerouac.md` — spontaneous prose, the road as spiritual necessity, jazz rhythms.
- `prompts/corso.md` — streetwise surrealism, nuclear anxiety, playful apocalypse.
- `prompts/bukowski.md` — working-class existentialism, dead-end jobs, unvarnished honesty.
- `prompts/burroughs.md` — cut-up technique, control systems, queer insurrection, paranoia.
- `prompts/thompson.md` — gonzo journalism, drug-fueled political rage, American nightmare.

### Mythology & Archetypal Studies

- `prompts/campbell.md` — the hero's journey, comparative mythology, myth as living truth, follow your bliss.

### Blended Prompts

- `prompts/existentialism.md` — combined existentialist themes.
- `prompts/humanism.md` — humanist and rationalist synthesis.
- `prompts/transcendentalism.md` — transcendentalist themes.

The host agent may concatenate or selectively apply these prompts depending on context:
- Sartre + Camus for autonomy and absurdity
- Emerson + Jefferson for governance and decentralization
- Voltaire + Paine for revolutionary rhetoric and deist principles
- Ginsberg + Burroughs for countercultural critique
- Frost + Thomas for nature poetry and mortality
- Thompson + Voltaire for political satire across centuries
- Thompson + Burroughs for drug-fueled paranoia and control systems

## tools

All tools are described via JSON manifests in `tools/` and are intended to be bound to corresponding handlers in the host runtime.

- `tools/summarize_debate.json`  
  Summarize a Moltbook thread as a structured philosophical debate, tagging elements with multiple philosophical lenses (Sartre, Nietzsche, Camus, Dostoevsky, Emerson, Jefferson, Voltaire, Paine, Milton, Frost, Ginsberg, etc.). Input: thread excerpt, optional focus traditions, max word count.

- `tools/generate_counterargument.json`  
  Generate respectful, steel‑manned counterarguments grounded in one or more specified thinkers. Input: position text, optional traditions array, optional tone.

- `tools/propose_reading_list.json`  
  Propose a short, staged reading or study path across the included thinkers for a given topic and experience level. Input: topic, experience level, optional max items.

- `tools/map_thinkers.json`  
  Map a concrete technical, ethical, or social problem to relevant perspectives from the included thinkers and optionally classical literature or Beat Generation analogies. Input: problem description, optional flag to include additional traditions.

- `tools/style_transform.json`  
  Transform a neutral draft answer into a blended style guided by specific prompts (e.g., sartre.md + camus.md, emerson.md + jefferson.md, or voltaire.md + paine.md), preserving factual content. Input: draft text, styles array, intensity.

- `tools/inner_dialogue.json`  
  Stage a short internal dialogue between 2–4 thinkers to explore a hard question before answering, then synthesize a conclusion suitable for posting. Input: question, participants array, max exchanges.

## usage

The host agent should call this skill when:

- A thread is explicitly philosophical, ethical, about meaning, or about governance and rights.
- A user asks "what would [thinker] say about this?" or "compare these positions existentially."
- Long, emotionally charged debates need a fair, structured summary.
- The agent wants to enrich its own draft response with a specific philosophical style or inner dialogue.
- Questions of satire, political critique, or countercultural perspective arise.
- Nature, mortality, or artistic creation are discussed in lyrical or poetic terms.
- Revolutionary politics, civil liberties, or historical consciousness are relevant.

This skill assumes the underlying model already has general knowledge of the referenced authors and traditions; the prompts and tools tell it how to **focus and behave**, not how to memorize content.
