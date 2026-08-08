---
name: suede-video
description: "Suede-owned marketing video planning and production discipline. Use when choosing a format, scripting, storyboarding, generating, editing, reverse-engineering pacing, building a repeatable video pipeline, or repurposing one source into multiple cuts. NOT FOR: deciding the social calendar (use suede-social), paid ad concepts (use suede-ad-creative), image-only assets (use suede-image), or publishing unapproved media."
metadata:
  version: 2.1.0
---

# Suede Video Production

Suede Video turns an approved message and rights-cleared source material into
scripts, storyboards, generation plans, edit systems, and reusable production
pipelines. It keeps likeness, licensing, brand assets, render cost, and
publishing as explicit gates rather than assumptions.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Video Goal
- What type of video? (Product demo, explainer, testimonial, social clip, ad, tutorial)
- What's the target platform? (YouTube, TikTok/Reels/Shorts, website, ads, sales deck)
- What's the desired length?

### 2. Production Approach
- Do you need a human presenter? (AI avatar vs. voiceover vs. screen recording)
- Do you have existing footage or assets? (Screenshots, logos, product UI)
- Do you need generated footage? (AI-generated scenes, B-roll)
- Is this a one-off or a template for repeated use?

### 3. Technical Context
- What's your tech stack? (Node.js, Python, etc.)
- Do you have API keys for any video tools?
- Budget constraints? (Some tools charge per minute of video)

---

## Choosing Your Approach

Choose the production method from the job, available evidence, rights, and
currently callable tools:

| Approach | Candidate fit | Tools to evaluate | Use when |
|----------|---------------|-------------------|----------|
| **Programmatic** | Templated, data-driven, batch video | An installed HTML/CSS or React renderer | The format repeats and deterministic output matters |
| **AI generation** | Original footage from text/image prompts | Any currently authorized generation model | The scene cannot be filmed practically and output rights are verified |
| **AI avatars** | Approved presenter without filming | Any currently authorized avatar platform | Consent, likeness, voice, localization, and output rights are documented |
| **Editing/repurposing** | Cutting long-form into short clips | Any installed transcript or timeline editor | Source media and derivative-use rights are available |

---

## Programmatic Video

Programmatic video is a candidate for repeatable, templated, or data-driven
work; verify fit against the current stack, edit needs, cost, and review burden.

### HTML/CSS renderer candidate

Hyperframes may fit an HTML/CSS workflow. First check whether it is installed.
If it is, read the installed version's documentation, inspect its license, and
confirm the renderer and export path. If it is not installed, use a
renderer-neutral handoff or request explicit installation authorization after
showing the current package source, version, lockfile impact, and cost. The
following command must not run without that authorization:

```bash
npm install hyperframes
```

**Key concept:** Each frame is an HTML document. Compose frames into a timeline, render to MP4.

```typescript
import { render } from "hyperframes";

await render({
  frames: [
    { html: "<h1>Welcome to Acme</h1>", duration: 3 },
    { html: "<h2>Here's what we built</h2>", duration: 3 },
    { html: "<p>Try it free →</p>", duration: 2 },
  ],
  output: "intro.mp4",
  width: 1080,
  height: 1920, // 9:16 for vertical
});
```

**Candidate fit:** Product announcements, changelogs, data-driven reports, and
approved personalized outreach videos. Verify determinism with a repeat-render
test instead of assuming it.

### React renderer candidate

Remotion may fit a React-based workflow. Verify the installed or callable
version, current documentation, license, rendering path, and hosting cost. The
scaffold command may install packages or create files; run it only with explicit
authorization for that change, otherwise provide a renderer-neutral plan:

```bash
npx create-video@latest
```

**Key concept to verify:** React components express timed visuals and props
drive content. Confirm whether rendering is local or uses an authorized hosted
renderer.

```tsx
export const ProductDemo: React.FC<{ title: string; features: string[] }> = ({
  title, features
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#000", color: "#fff" }}>
      <h1>{title}</h1>
      {features.map((f, i) => (
        <Sequence from={i * 30} key={i}>
          <p>{f}</p>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

**Candidate fit:** Complex animation, interactive previews, or batch rendering
when the verified runtime supports them.

### When to Pick Which

| Factor | HTML/CSS renderer | React renderer |
|--------|-------------------|----------------|
| Existing stack | Browser and CSS capability | React and renderer capability |
| Animation needs | Test required transitions | Test required timeline primitives |
| Batch rendering | Verify local or hosted path | Verify local or hosted path |
| Team fit | Inspect maintainability in this repo | Inspect maintainability in this repo |
| Rights and cost | Verify current license and runtime cost | Verify current license and runtime cost |

---

## AI Video Generation

Generate original footage from text or image prompts. Use for B-roll, hero visuals, and scenes you can't practically film.

### Model comparison

Discover currently callable and authorized models before recommending one. Read
current official documentation and run a bounded test on the actual account.
Compare:

| Criterion | Evidence to capture |
|-----------|---------------------|
| Output fit | Resolution, duration, audio, motion, and consistency from current docs plus a test clip |
| Control | Reference-image, camera, edit, seed, and storyboard controls actually exposed |
| Operations | Queue time, failure rate, export path, and repeatability |
| Rights | Input rights, output rights, model restrictions, consent, and provenance |
| Economics | Current plan, per-generation cost, failed-generation treatment, and budget cap |

If no model is callable and authorized, return a shot list, prompt set,
reference-frame brief, and manual vendor-evaluation checklist.

### Prompting for Video Models

Good video prompts specify: **subject + action + camera + style + mood**

```
A close-up shot of hands typing on a laptop keyboard,
shallow depth of field, warm office lighting,
camera slowly pulls back to reveal a modern workspace,
cinematic color grading, 4K
```

**Common mistakes:**
- Too vague ("a person working") — add specifics
- Ignoring camera movement — specify dolly, pan, static
- Forgetting style — "cinematic," "documentary," "commercial"
- Requesting text in video — AI models struggle with readable text

**For detailed prompting guides**: See [references/ai-video-prompting.md](references/ai-video-prompting.md)

### AI Generation vs. Stock Evaluation

| Use Case | Generation evidence to test | Stock/original evidence to test |
|----------|-----------------------------|---------------------------------|
| Specific scene | Prompt control, continuity, review burden | Search coverage, license, edit fit |
| Style continuity | Cross-clip consistency in a bounded test | Match quality across licensed clips |
| Real location | Factual accuracy and disclosure risk | Provenance and location release |
| Product/brand | UI and mark fidelity; avoid fabricated product claims | Approved real captures or assets |
| B-roll | Queue time, failure rate, cost | Search and licensing time |

---

## AI Avatars

Create talking-head videos without filming. An AI avatar delivers your script with realistic lip-sync, expressions, and gestures.

### Avatar tool evaluation

HeyGen is one possible avatar platform, not a guaranteed or preferred
integration. Before naming it or another vendor, verify current official
documentation, authenticated access, callable API or connector availability,
plan limits, price, output rights, and the consent requirements for every voice
or likeness involved.

If no avatar tool is currently callable and authorized, provide a manual
vendor-neutral workflow: approved script, consent record, user-operated upload,
export checklist, and a real-camera or voiceover fallback.

**Possible fit to test:** product explainers, feature announcements,
multilingual versions, and approved personalized outreach.

### Another avatar candidate

An alternative avatar platform may fit training or presentation work. Confirm
its current features from official documentation and test consent, body-motion,
script-ingestion, localization, and export requirements on the authorized
account before recommending it.

### Avatar vs. Other-Approach Test

| Scenario | Avatar evidence to verify | Alternative to compare |
|----------|---------------------------|------------------------|
| Recurring content | Consent, repeatability, audience response | Recorded presenter or voiceover |
| Multilingual versions | Translation, pronunciation, disclosure | Human localization |
| Personalized outreach | Consent, claim review, cost, reply quality | Approved text or recorded template |
| Founder message | Trust and disclosure response | Direct recording |
| Product UI walkthrough | Presenter value around real captures | Screen recording |
| Creative/artistic video | Control, originality, rights | Original footage or generated scenes |

---

## Editing & Repurposing Tools

Turn existing content into multiple video formats.

Treat the named products as candidates. Discover what is currently installed or
callable, verify the user's account and rights, then map the workflow to the
available tool. If none is available, return an edit decision list, clip
timestamps, captions, and export settings for manual execution.

| Candidate capability | What to verify | Candidate fit |
|----------------------|----------------|---------------|
| Transcript editor | Speaker accuracy, cut control, export, privacy | Interviews, podcasts, webinars |
| Clip assistant | Selection controls, provenance, false-positive rate | Long-form to short-form review |
| Timeline editor | Caption, effect, audio-rights, and export controls | Platform-specific finishing |
| Accessibility assistant | Caption accuracy, eye-contact disclosure, dubbing consent | Approved talking-head content |

### Repurposing Workflow

```
Long-form content (podcast, webinar, demo)
    ↓
Transcript edit: Clean up, remove filler, polish
    ↓
Clip review: Propose moments with source timestamps
    ↓
Timeline edit: Add reviewed captions, effects, and platform styling
    ↓
Distribute: TikTok, Reels, Shorts, LinkedIn
```

### Reverse-Engineer a Viral Edit

To study the style of a reference edit, first discover whether an authorized
media-inspection, browser, or local-file viewer is currently callable. If one is
available, inspect the actual frames and timing. Otherwise ask the user to
attach the media, screenshots, or a timecoded export and provide a manual
frame-sampling checklist. Then extract a reusable beat sheet plus the 3–5
signature moves. Review it before execution in any currently available editor.
Copy the editing grammar, never the reference's footage, script, voice, or
music. Full method: [references/edit-anatomy.md](references/edit-anatomy.md).

---

## Video Production Workflows

### Product Demo Video

1. **Script** the key features and value props (use suede-copy skill)
2. **Screen record** the product flow
3. **Programmatic overlay** — use an available authorized renderer for titles,
   callouts, and transitions, or provide manual editor instructions
4. **AI B-roll** — only with a discovered authorized generator and verified
   rights; otherwise use licensed stock or original footage
5. **Voiceover** — record yourself or use AI avatar for narration
6. **Export** at platform-appropriate specs

### Explainer Video

1. **Script** the problem → solution → CTA arc
2. **Choose presenter** — an approved avatar workflow when available, or
   recorded voiceover plus visuals
3. **Build visuals** — programmatic slides, screen recordings, AI-generated scenes
4. **Add captions** as an accessibility default and verify their accuracy
5. **Export** only after checking current destination requirements and previewing
   the authenticated composer; do not assume a universal orientation

### Batch Social Clips

1. **Create master template** in an available authorized renderer or a manual
   editor project
2. **Feed data** — product features, testimonials, stats
3. **Render batch** — one template, many variations
4. **Add platform-specific captions** with an available editor
5. **Return approved export candidates** to `suede-social` for channel strategy;
   scheduling remains a separate explicit action

---

## Tool-Aware Video Pipeline

Use automation only after discovering currently callable, authenticated, and
authorized tools. Otherwise produce the same artifacts as a manual handoff.

```
Approved script (from product context)
    ↓
Available renderer/avatar/generator, if authorized
    or manual editor with timecoded instructions
    ↓
Review cut, rights, captions, and brand assets
    ↓
Output: Approved export candidate, not automatically published
```

When no production tool is available, return the script, shot list, asset
manifest, beat sheet, captions, edit decision list, and export settings so the
user can execute the cut manually.

---

## Common Mistakes

1. **Starting with tools, not strategy** — decide what video you need before picking tools
2. **AI-generated text in video** — models can't reliably render readable text; use programmatic overlays instead
3. **Unverified avatar quality** — test a short consented sample before paying
   for or producing a batch
4. **Inaccessible cut** — provide accurate captions without asserting a
   universal sound-off viewing rate
5. **Unverified export spec** — read current destination requirements and
   preview the actual composer before choosing ratio, resolution, or duration
6. **Unsupported production-style claim** — compare polished and informal
   treatments on the current account instead of claiming one universally wins

---

## Task-Specific Questions

1. What type of video do you need? (Demo, explainer, social clip, ad, tutorial)
2. Do you need a human presenter or can it be voiceover/text?
3. Is this a one-off or a repeatable template?
4. What platform and placement is it for? (We will verify its current ratio,
   duration, and composer requirements.)
5. Do you have existing assets to work with? (Screenshots, footage, scripts)
6. What's your budget for video tools?

---

## Tool Integrations

These are evaluation examples, not guaranteed integrations. Verify current
official documentation, authenticated access, licensing, model availability,
render cost, output rights, and callable tools in the current session.

| Tool | Type | Verify Before Use |
|------|------|-------------------|
| **HeyGen** | AI avatars | Likeness consent, plan rights, API access, cost |
| **Hyperframes** | Programmatic video | Installed runtime, renderer, asset licenses |
| **Remotion** | Programmatic video | Current license, runtime, renderer, hosting cost |
| **Runway** | AI generation | Model access, generation rights, price, limits |

---

## Boundaries

- Do not generate, render, purchase, upload, or publish media without approval
  of scope, tool cost, rights, and destination.
- Do not clone a real person's voice or likeness, use unlicensed source media,
  or promise an exact copy of a reference style or edit.
- For Suede-branded visuals, use only the approved transparent Suede S asset at
  `JasonColapietro/suede-creator-skills/docs/assets/suede-ai-logo-transparent.png`
  with SHA-256
  `83a7ee0317e4debe2e7b076c20ba067feb76a587f9e829dc6310ae4be4b44dfa`;
  if it is missing or changed, omit the mark and halt for the approved file.

## Routing

- Use `suede-social` to choose channel strategy, cadence, and distribution.
- Use `suede-ad-creative` for paid video ad concepts and variants.
- Use `suede-image` for still-image generation and editing.
- Use `suede-copy` for source-verified script and messaging polish.
