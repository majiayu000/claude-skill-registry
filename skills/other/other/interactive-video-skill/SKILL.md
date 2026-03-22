---
name: interactive-video
description: Turns docs, posts, and codebases into interactive walkthroughs — narrated animation, quizzes, and widgets. Use when the user wants to create an interactive walkthrough, onboarding video, explainer, or tutorial from any source. Also triggers on "make a lesson", "teach this visually", "interactive explainer", "turn this into a walkthrough", or "onboarding video".
disable-model-invocation: false
user-invocable: true
argument-hint: "<URL, file path, topic description, or 'codebase'>"
---

# Interactive Video: $ARGUMENTS

Generate a self-contained HTML walkthrough from **$ARGUMENTS** with canvas animations, narrated audio, quizzes, and interactive widgets.

Parse `$ARGUMENTS` for source (URL, file, topic, or "codebase"), scope hints ("focus on X", "skip Y"), and audience/use-case hints ("onboarding", "knowledge transfer", "walkthrough", "beginner-friendly"). Pre-fill extracted hints into configurator URL params.

## Gotchas (things the references and validator don't catch)

- **Title-only visuals while narration gives details.** Extract 3-5 key phrases per scene and stagger `revealAt` to match when they're spoken: `revealAt = (phraseTime - sceneStart) / (sceneEnd - sceneStart)`. The canvas should reinforce what the ear hears.
- **Scenes too short for narration.** Don't create 5-second scenes with a single text element. Each scene needs enough content to fill its duration with progressive reveals.
- **Hardcoded colors instead of theme palette.** Pull colors from `styles.json` for the selected theme — hardcoded colors break theme switching.
- **`interactions` in content.json is an object keyed by ID**, not an array. The engine looks up by ID: `CONTENT.interactions[ix.id]`.
- **Visual reveal order mismatches narration order.** If the narration describes a stack bottom-to-top, the visual must reveal bottom-to-top (or flip the layout). The most recently revealed element must always be the thing currently being narrated. See `design-guide.md` § Spatial-temporal alignment.
- **Dead scenes.** A scene where everything fades in and sits still feels like a slideshow, not a video. Every scene >20s should have at least one source of continuous motion — flowing dashed arrows, a pulsing glow, gentle drift. See `design-guide.md` § Alive vs dead scenes.

## Quality principles

- **Research grounds the content.** Verify facts before writing. Calibrate depth to the use case.
- **Concrete beats generic.** "The auth service uses JWT with 15-min expiry" beats "many systems use tokens."
- **Narration is conversational.** Direct, "you" voice. Like explaining to a new team member on their first day.

---

## Phase 0: SETUP

### 0.1 One-time setup

Run `bash $SKILL_DIR/scripts/setup.sh` on first use. Skip if `edge-tts` is already on PATH.

### 0.2 Confirm language

Detect from source. Confirm with user — this is the **only** CLI question.

### 0.3 Research + extract topics

- **URL** → WebFetch the page. Optionally WebSearch for supplementary context.
- **File path** → Read the file. WebSearch for background on frameworks/concepts it references.
- **"codebase"** → Explore with Glob/Grep/Read. WebSearch for documentation on patterns found.
- **Topic string** → Research in parallel using Agent tool (WebSearch + WebFetch per agent). Wait for all agents, then extract topics from the research.

Extract the natural topic structure from the source as JSON:

```json
[{ "id": "topic-id", "label": "Topic Name", "desc": "One-line description" }]
```

### 0.4 Open configurator

```bash
cd $SKILL_DIR && npx tsx scripts/build_audio.ts --generate-previews --lang {lang}
cd $SKILL_DIR && npx --yes http-server -p {port} -c-1 --silent &
```

Open (pick unused port 8100-8199):
- macOS: `open "http://localhost:{port}/configurator.html?lang={lang}&source={encoded_source}&topics={encoded_topics}"`
- Linux: `xdg-open "http://localhost:{port}/..."`

Wait for user to paste configurator output.

### 0.5 Set output directory + copy engine

```bash
mkdir -p {out}/src/engine && \
cp -n $SKILL_DIR/engine/*.js {out}/src/engine/ && \
cp -n $SKILL_DIR/engine/lesson.css {out}/src/
```

**After this: no more questions. Run Phases 1-4 without stopping.**

---

## Phase 1: PARSE PREFERENCES

Parse the `Preferences:` block. Extract: Audience, Length, Interaction, Visual style, Language, Voice, Topics.

Theme keys are defined in `styles.json`. Length targets and interaction design rules are in `design-guide.md`.

---

## Phase 2: STRUCTURE

**Read** `$SKILL_DIR/references/design-guide.md`. Use it as a reference — adapt to what the content needs.

---

## Phase 3: GENERATE

**Read the reference files you need** (always in one parallel message):

- Always: `page-template.md`, `styles.json`, `engine-contracts.md`
- For custom draw functions or complex animations: also `render-patterns.md`

```
Read(engine-contracts.md)
Read(page-template.md)
Read(styles.json)
# Read(render-patterns.md) — only if this lesson uses custom draw
```

**Write content.json** → `{out}/src/content/{lessonId}/content.json`
- Follow schema in `engine-contracts.md` exactly
- Leave `t` and `duration` as `0` — build_audio fills them

**Start audio in background** → immediately after writing content.json:
```bash
cd $SKILL_DIR && npx tsx scripts/build_audio.ts {lessonId} \
  --content-dir {out}/src/content \
  --audio-dir {out}/audio/lessons
```
Use `run_in_background: true`. Audio only needs content.json.

**Write HTML while audio generates** → `{out}/{lessonId}.html`
- Follow the template in `page-template.md` exactly

---

## Phase 4: FINALIZE

**After audio completes** (you will be notified):
1. Read updated `content.json` for computed timing
2. Patch HTML: scene `s`/`e` values + IX `time` values

**Scene timing rules:**
- First scene starts at `0`. Last scene ends at `meta.duration`.
- Each scene's `s` equals the previous scene's `e`. **No gaps.** The audio `gap` (1.2s silence between segments) does NOT create scene gaps — scenes are wall-to-wall.
- Use interaction `time` values and narration `t` values as guides for where to place boundaries, but always ensure contiguity.

**Validate + serve in one command:**
```bash
cd $SKILL_DIR && npx tsx scripts/validate.ts {lessonId} \
  --content-dir {out}/src/content \
  --audio-dir {out}/audio/lessons \
  --html {out}/{lessonId}.html && \
cd {out} && npx --yes http-server -p {port} -c-1 --silent & \
sleep 1 && open "http://localhost:{port}/{lessonId}.html"
```

Show the user: title, duration, scene count, interaction count, scene breakdown, files created.

**Optional: visual verification** — skip if it fails (Playwright may not be installed):
```bash
cd $SKILL_DIR && npx tsx scripts/visual_verify.ts {lessonId} \
  --html {out}/{lessonId}.html --out {out}/verify-{lessonId} || true
```
If it succeeds, screenshots are saved to `verify-{lessonId}/`. If it fails, continue — the lesson is already validated and served.

**Log the lesson** — append to `${CLAUDE_PLUGIN_DATA}/lessons.json` (create if missing):
```json
{ "id": "{lessonId}", "title": "...", "theme": "...", "duration": 0, "scenes": 0, "interactions": 0, "date": "YYYY-MM-DD", "output": "{out}" }
```
This lets future invocations see what's been built before.
