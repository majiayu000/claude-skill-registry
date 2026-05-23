---
name: lyric-diagnostic
description: Diagnose lyric problems across prosody, rhyme, meaning, register, sound, and structure. Use when AI-generated or human lyrics feel flat, cliched, awkward, or mismatched.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Lyric Diagnostic: Skill

You diagnose lyric problems across multiple dimensions. Your role is to identify why lyrics fail and guide writers (human or AI) toward more effective choices.

## Core Principle

**Lyrics fail in predictable, diagnosable ways. Generic is not neutral—generic is bad.**

AI-generated lyrics cluster at statistical distribution centers: the most probable word choices, rhyme pairs, and emotional vocabulary. Probability optimization produces mediocrity. Effective lyrics require intentional deviation from defaults.

The same pattern that makes "Celtic" trigger tinwhistle in music generation makes "love" trigger predictable rhyme pairs and emotional cliches in lyric generation.

---

## The Lyric States

### State LY1: Cliche Trap

**Symptoms:** Predictable rhyme pairs dominate. Word choices are first-associations. Nothing surprises. Lyrics could fit any song on this topic.

**Key Questions:**
- What rhyme pairs are you using? Are they first-associations?
- Would replacing the end-rhyme word break the meaning? (If not, it's filler)
- Can you enumerate the default words for this topic and avoid them?
- What would a different genre use for this same emotion?

**Diagnostic Checklist:**
- [ ] No Tier 1 cliche words (love, heart, baby, forever)
- [ ] No stock phrases (see list below)
- [ ] Rhyme pairs are not obvious first-associations
- [ ] At least one surprising word choice per verse
- [ ] Specific details rather than generic statements

**Stock Phrases (phrase-level cliches, not just words):**

Scripts can't catch these—they require semantic judgment:

| Phrase | Category | Why It's Cliche |
|--------|----------|-----------------|
| "screaming inside" | unexpressed anguish | Every song about hidden pain uses this |
| "need you gone" | direct desire | States want instead of showing it |
| "won't leave me alone" | persistence | Generic memory/thought complaint |
| "thought I died" | emotional death metaphor | Overused intensity marker |
| "used to be" + past state | nostalgia setup | Stock before/after framing |
| "look in your eyes" | connection | Vague romantic gesture |
| "torn apart" | destruction | Abstract violence metaphor |
| "can't let go" | attachment | States the problem directly |

**Lazy Rhyme Pairs (rhyme drove word choice):**

| Pair | Problem |
|------|---------|
| desire / fire / tired | Cluster appears together constantly |
| inside / died / alive | Death-interior cluster |
| away / stay / day | Motion-time cluster |
| heart / apart / start | Heart-destruction cluster |
| alone / gone / on | Isolation cluster |

**Interventions:**
- Run `cliche-check.ts` as pre-filter (surfaces candidates, doesn't diagnose)
- Scan for stock phrases manually—scripts miss these
- List the 10 most predictable rhymes for your end words—avoid them all
- Replace abstract emotions with concrete sensory imagery
- Ask: "What would someone who hates this genre never say?" Use that.

---

### State LY2: Meter Mismatch

**Symptoms:** Lines don't fit the melody. Stresses fall on wrong syllables. Unnatural pronunciation required. Syllables crammed or stretched awkwardly.

**Key Questions:**
- Can you tap the rhythm and speak the line simultaneously?
- Where do stresses fall? Do they match the melody's emphasis?
- Are any syllables swallowed or stretched unnaturally?
- How many syllables per phrase? Is there consistency?

**Diagnostic Checklist:**
- [ ] Natural word stress aligns with musical beats
- [ ] Syllable counts fit the melodic phrase
- [ ] No awkward pronunciations required
- [ ] Contractions/elisions are singable

**Interventions:**
- Run `meter-check.ts` to analyze syllable counts and stress patterns
- Speak the lyrics while tapping the beat—mismatches become obvious
- Swap words with same meaning but different syllable count
- Use contractions to reduce syllables, or expand to add them

---

### State LY3: Shallow Surface

**Symptoms:** Lyrics say exactly what they mean and nothing more. No subtext, no layers, no depth. Emotions are stated directly. Everything is on the surface.

**Key Questions:**
- Is there a second reading? Something between the lines?
- Are you stating the emotion or evoking it through imagery?
- What specific concrete image grounds the abstraction?
- Could this be understood on first listen but reveal depth on repeat?

**Diagnostic Checklist:**
- [ ] At least one image per verse that works on multiple levels
- [ ] Emotions evoked through detail, not stated directly
- [ ] Something for repeat listens to discover
- [ ] Concrete specifics anchor abstract concepts

**Interventions:**
- For every abstract statement, find a concrete action/image that embodies it
- Instead of "I'm sad," show what sad looks like, sounds like, feels like
- Add a detail that doesn't quite fit—creates productive ambiguity
- Test: can you explain two different interpretations of the same line?

---

### State LY4: Register Mismatch

**Symptoms:** Lyric tone contradicts the music's emotion. Casual words over dramatic instrumentation. Heavy lyrics over light music. Vocabulary doesn't match genre expectations.

**Key Questions:**
- What emotion should the listener feel at this moment?
- Is your vocabulary elevated/casual matching the music?
- Does the distance (intimate/observational) match the instrumental?
- Would this language make sense in this genre?

**Diagnostic Checklist:**
- [ ] Vocabulary matches musical intensity
- [ ] Distance (I/you vs. they/we) fits the sound
- [ ] Genre vocabulary expectations met or intentionally broken
- [ ] Irony (if present) is signaled clearly

**Interventions:**
- Listen to the music without lyrics—what emotions does it evoke?
- Match lyric intensity to musical intensity section by section
- Check genre vocabulary norms—violate intentionally or not at all
- If using irony, add signal words or structural cues

---

### State LY5: Sound Neglect

**Symptoms:** No attention to how words feel in the mouth. Harsh consonant clusters at tender moments. Monotonous vowel sounds. No alliteration, assonance, or deliberate sound texture.

**Key Questions:**
- What consonant sounds dominate? What texture do they create?
- Do vowel sounds support the emotional content?
- Are there harsh clusters that disrupt flow?
- Is there intentional sound painting?

**Diagnostic Checklist:**
- [ ] Soft consonants (l, m, n, w) at intimate moments
- [ ] Hard consonants (k, t, p) at impactful moments
- [ ] Vowel sounds support emotional content
- [ ] At least one sound device per verse (alliteration, assonance)

**Interventions:**
- Read lyrics aloud focusing only on how they feel in the mouth
- Map emotional moments to appropriate sound textures
- Replace harsh-sounding words at tender moments
- Add deliberate alliteration or assonance at key phrases

---

### State LY6: Structural Chaos

**Symptoms:** No identifiable hook. Verse and chorus feel interchangeable. Repetition is annoying, not reinforcing. Bridge doesn't contrast. Song has no arc.

**Key Questions:**
- Is there a clear hook? Where does it land?
- Does each verse add new information or repeat?
- Does the bridge actually contrast or just continue?
- Is repetition earning its place?

**Diagnostic Checklist:**
- [ ] Hook is identifiable and memorable
- [ ] Verses differentiate (new info, different angle)
- [ ] Chorus delivers emotional payoff
- [ ] Bridge provides contrast or escalation
- [ ] Repetition evolves or emphasizes, doesn't bore

**Structural Cliches:**

| Pattern | Problem | Fix |
|---------|---------|-----|
| Bridge = Verse | Not a bridge at all—just more of the same | Shift perspective, time, or speaker |
| Chorus expands on repeat | Adding lines without development | Each chorus iteration should mean more |
| Hook repeated without exploration | Says the phrase but never unpacks it | What does the hook *mean*? Show us. |
| No arc | Emotional state same at end as beginning | Something must change—realization, acceptance, escalation |
| Verses say same thing differently | Verse 2 is Verse 1 with synonyms | Each verse needs new information or angle |

**Interventions:**
- Identify the hook—if you can't, create one
- Make each verse answer a different question about the topic
- Bridge should shift perspective, time, or intensity
- Cut repetition that doesn't earn its place
- Check: is the speaker in a different place emotionally at the end?

---

## Diagnostic Process

### Step 1: First Listen (Holistic)

Listen without analyzing. Note:
- What's the overall impression?
- What lines feel strong or weak?
- Where does attention wander?
- What's memorable after one pass?

### Step 2: Identify Primary State

Which of the six states best describes the main problem?
- LY1: Feels generic/predictable → Cliche Trap
- LY2: Doesn't fit the melody → Meter Mismatch
- LY3: Says nothing deep → Shallow Surface
- LY4: Tone feels wrong → Register Mismatch
- LY5: Sounds awkward → Sound Neglect
- LY6: No structure/hook → Structural Chaos

### Step 3: Run Diagnostics

For the primary state:
- Answer the key questions
- Run relevant scripts (`cliche-check.ts`, `meter-check.ts`, etc.)
- Complete the diagnostic checklist

### Step 4: Check Secondary States

Often multiple states co-occur:
- Cliche (LY1) often comes with Shallow (LY3)
- Meter (LY2) often comes with Sound (LY5)
- Register (LY4) often comes with Structure (LY6)

### Step 5: Prioritized Intervention

Fix the most damaging issue first:
- Meter (LY2) before Sound (LY5)—if it's unsingable, sound texture won't help
- Cliche (LY1) before Shallow (LY3)—fresh words enable depth
- Structure (LY6) before Register (LY4)—need sections before matching tone

---

## Anti-Patterns

### 1. Over-Revision

**Pattern:** Fixing one problem introduces new problems. Every change cascades.

**Signs:**
- Draft 5 is worse than draft 2
- "Fixing" rhyme breaks meaning
- Original spark is lost

**Why It Fails:** Lyrics are an interconnected system. Point fixes ignore system effects.

**Fix:** Make one change, then re-read holistically. Don't chain fixes without checking the whole.

---

### 2. False Sophistication

**Pattern:** Chasing complexity for its own sake. Obscurity mistaken for depth.

**Signs:**
- Lyrics need explanation
- Dense metaphor without clear thread
- Audience confusion, not intrigue

**Why It Fails:** Obscure isn't deep. Listeners need access point.

**Fix:** Every obscure element needs a clear anchor. Complexity serves clarity, not replaces it.

---

### 3. Genre Cosplay

**Pattern:** Adopting genre vocabulary without understanding function.

**Signs:**
- Country lyrics with trucks but no storytelling
- Hip-hop wordplay without flow
- Indie obscurity without emotional core

**Why It Fails:** Genre vocabulary is shortcut to function. Without function, it's costume.

**Fix:** Understand what the genre element does, then deploy it for that purpose.

---

### 4. First-Draft Attachment

**Pattern:** Refusing to revise lines that came easily.

**Signs:**
- "But that's what I wrote first"
- Defending weak lines emotionally
- Unable to kill darlings

**Why It Fails:** First drafts capture intuition but include noise. Signal needs extraction.

**Fix:** Save first draft separately. Revise as if someone else wrote it.

---

## Integration

### Inbound (when to use this skill)
- After generating AI lyrics (Suno, etc.)
- When human-written lyrics feel "off"
- Before finalizing any lyrics for production

### Outbound (what to do after)
- **LY1 (Cliche)** → Apply Cliche Transcendence framework
- **LY2 (Meter)** → Use meter-reference.md for alternatives
- **LY3 (Shallow)** → Use Semantic Layers from lyric-analysis-framework.md
- **LY4 (Register)** → Check lyricist-dna-framework.md for register models
- **LY5 (Sound)** → Use Sound Texture section of lyric-analysis-framework.md
- **LY6 (Structure)** → Use Structural Architecture section

### Complementary
- **prose-style** - for sentence-level craft (overlaps with sound/clarity)
- **cliche-transcendence** - for escaping default patterns
- **naming** - for sound symbolism and word selection

---

## AI Lyric Generation Failure Modes

AI-generated lyrics (Suno, etc.) fail in predictable ways due to how LLMs work:

### The Degradation Pattern

1. **Lines 1-2:** Model has freedom, may find something interesting
2. **Lines 3+:** Rhyme constraint activates, model optimizes for completion over originality
3. **By verse 2:** Fully in statistical default mode—stock phrases, lazy rhyme clusters

**Why this happens:**

Two forces compound:

1. **Statistical median pull:** LLMs generate the most probable next token. For lyrics, this means the most common rhyme pairs, the most frequent emotional vocabulary, the most typical phrase structures. Probability optimization produces mediocrity.

2. **Completion reward bias:** Training for "helpful" weights goal completion over thoroughness or quality. The model treats "rhyme achieved" as success, regardless of whether it's an interesting rhyme. Structure complete > structure meaningful.

This is the same mechanism documented in the Sequential Focus framework—forward reference gravitational pull. The model sees the target (rhyme, line end, verse completion) and races toward the most probable path rather than exploring alternatives.

### Observable Symptoms

- Opening verse shows craft, later verses collapse into cliche
- Rhyme words cluster in predictable groups (fire/desire/tired appears together)
- Stock phrases concentrate in verses 2+
- Bridge is often weakest section (furthest from opening, most constrained)

### Countermeasures

**Pre-anchor end words:** Write the rhyme words yourself with intentional non-cluster choices. Force the model to land on words without lazy partners. If you avoid "fire," you break the fire/desire/tired cluster.

**Seed with concrete imagery:** Opening lines set the vocabulary space. Concrete, unusual imagery early may hold off statistical collapse longer than abstract emotional vocabulary.

**Isolate sections:** Generate verse 1 alone, evaluate, then generate verse 2 with explicit instruction to avoid verse 1's rhyme families. Treat each section as a separate generation task.

**Blacklist clusters:** Explicitly forbid the lazy rhyme clusters in prompts:
- "Do not use: fire, desire, tired, higher, liar"
- "Do not use: inside, died, alive, hide, tried"
- "Do not use: heart, apart, start, part"

**Provide slant rhyme alternatives:** Give the model escape routes. "Instead of perfect rhymes, use slant rhymes like home/come, love/move."

### The Isolation Principle

The same principle that makes Sequential Focus work for agent tasks applies to lyric generation: **hide the end goal, make each phase complete**.

Don't prompt "write a complete song about X." Instead:
1. Generate hook/title concepts (no full lyrics)
2. Generate verse 1 alone (no chorus yet)
3. Generate chorus treating verse 1 as context
4. Generate verse 2 with explicit differentiation requirement
5. Generate bridge with perspective shift requirement

Each step is the complete mission. The model can't race to "song complete" if it doesn't know a song is the goal.

---

## What This Skill Does NOT Do

- Does not write lyrics for you (diagnostic only)
- Does not evaluate musical elements (use Musical DNA for that)
- Does not replace human judgment about artistic intent
- Does not guarantee commercial success (craft ≠ commerce)

---

## Scripts (Pre-Filters, Not Diagnostics)

These scripts surface candidates for LLM/human interpretation. They do NOT make diagnostic judgments. Use their output as input to your analysis, not as the analysis itself.

**Why pre-filters?**
- Word lists can't catch stock phrases ("screaming inside")
- Phoneme matching can't judge rhyme quality (gerund-gerund is lazy)
- Syllable counting works, but variance meaning requires interpretation

### `cliche-check.ts`
Surfaces Tier 1/2 terms from `lyric-dominance-rules.json`. **You must evaluate in context.**

**Usage:** `bun run scripts/cliche-check.ts "your lyrics here"`

**Limitations:** Misses stock phrases, rhyme-driven word choice, semantic cliche.

### `meter-check.ts`
Reports syllable counts, stress patterns, and variance. **You must judge if variance is intentional.**

**Usage:** `bun run scripts/meter-check.ts "your lyrics here"`

**Useful for:** Identifying lines that need review, spotting high variance.

### `rhyme-check.ts`
Maps rhyme scheme and identifies rhyme types. **You must evaluate rhyme quality.**

**Usage:** `bun run scripts/rhyme-check.ts "your lyrics here"`

**Limitations:** Marks gerund-gerund (-ing/-ing) as rhymes. Marks same-semantic-field pairs as rhymes. Doesn't detect rhyme-forced word choice.

---

## Quick Reference

| State | Core Problem | First Question | Primary Fix |
|-------|--------------|----------------|-------------|
| LY1 | Predictable | Are rhymes first-associations? | Replace cliche terms |
| LY2 | Unsingable | Do stresses match beats? | Count syllables, swap words |
| LY3 | Empty | Is there subtext? | Add concrete imagery |
| LY4 | Mismatched | Does tone match music? | Align vocabulary to intensity |
| LY5 | Harsh | How do words feel in mouth? | Map sounds to emotions |
| LY6 | Aimless | Where's the hook? | Define and place hook |
