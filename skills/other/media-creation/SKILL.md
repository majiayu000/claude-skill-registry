---
name: media-creation
description: Producing digital media -- writing, images, video, audio, presentations, and multimedia -- with an understanding of craft, audience, accessibility, and ethics. Covers composition principles, copyright-safe sourcing, accessibility features (alt text, captions, contrast), remix culture, attribution practices, and the difference between creating for yourself, for a small audience, and for the open web. Use when helping a learner move from media consumer to media producer.
type: skill
category: digital-literacy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/digital-literacy/media-creation/SKILL.md
superseded_by: null
---
# Media Creation

Media creation is the active side of digital literacy. A learner who can only consume media is subject to whatever the publishing platforms push at them; a learner who can produce media -- even clumsily -- participates in the information ecosystem on different terms. This skill covers the craft, the ethics, and the accessibility practices that let you make things other people can actually use. It draws from Henry Jenkins's participatory culture framework, Yasmin Kafai's constructionist pedagogy, and the accessibility standards community.

**Agent affinity:** jenkins (participatory culture, remix), kafai (constructionist making), ito (creative practice)

**Concept IDs:** diglit-digital-media-creation, diglit-copyright-attribution, diglit-collaborative-tools

## The Creator's Baseline

Before any specific medium, the creator's baseline is the same:

1. **Have something to say.** Medium is downstream of message. A beautiful video with no point is worse than an ugly video with one.
2. **Know your audience.** Making something "for everyone" usually means making something for no one. Even a single imagined reader is better than no imagined reader.
3. **Finish things.** A mediocre finished piece teaches you more than a perfect unfinished one. Kafai's constructionist principle is that learning happens in the completion, not the planning.
4. **Publish.** Sharing is part of the making. The feedback loop from publishing is where craft actually develops.

## Writing for the Web

Writing is the underlying medium for all digital media. Even a video needs a script; even a podcast needs an outline.

### Structure before style

Before writing, draft the spine: what are you saying, who cares, what is the evidence, what is the conclusion. A bad first draft is easy to fix. A beautiful first draft with no structure is unsalvageable.

### One sentence per paragraph when you have to

Web reading is scanning. Long paragraphs die. Short paragraphs, clear headings, and front-loaded claims make content readable on phones and desktops both.

### Show instead of tell

"The interface was confusing" tells. "I opened the settings menu and could not find the option to change my password -- it was nested under Security, which was nested under Privacy, which was nested under Account" shows. Showing is always more persuasive and more memorable.

### Cut ruthlessly

Every sentence should earn its place. If you can cut it and the meaning survives, cut it. This is the single most impactful editing skill. The revision move most beginner writers skip is the cut.

## Images and Graphics

Images carry most of the attention on modern platforms. A few principles:

### Composition basics

- **Rule of thirds.** Place the subject off-center, on one of the third-lines. Centered subjects feel static; off-center subjects feel dynamic.
- **Leading lines.** Roads, fences, gazes, gradients -- lines in the image pull the eye toward the subject.
- **Contrast.** High contrast (dark subject on light background, or vice versa) makes images pop. Low contrast makes them feel flat.
- **Negative space.** Empty areas are not wasted. They give the subject room to breathe.

### File formats, revisited

- **JPEG** for photos. Good compression, some artifacts.
- **PNG** for diagrams, screenshots, images with text. Lossless.
- **WebP** or **AVIF** when modern browsers are the audience. Best compression.
- **SVG** for diagrams, icons, illustrations. Vector, scales infinitely.

### Copyright-safe sourcing

Do not grab images from Google Images. Most are copyrighted. Use:

- **Unsplash, Pexels, Pixabay** -- free to use, no attribution required for most content
- **Wikimedia Commons** -- attribution required, check license per image
- **Your own camera** -- copyright is yours by default
- **Creative Commons search** (cc.openverse.org) -- filter by license

Always check the license. "Free to use" is not the same as "public domain." CC-BY requires attribution; CC-BY-SA requires attribution *and* share-alike.

## Video

Video is the dominant medium for attention. Making video well is harder than it looks, but the baseline is achievable:

### Audio matters more than video

Bad audio is unwatchable. Bad video is watchable with good audio. Invest in a cheap microphone (USB condenser, lavalier) before a better camera.

### Light your face

Natural window light from the side or front. A ring light for evening. Backlight is the cardinal sin -- it makes subjects look like silhouettes.

### Short is better than long

Attention on video is short. Say the point in the first 15 seconds. Pad nothing.

### Cut tightly

Most first cuts of a video are twice as long as the final should be. Cut pauses, filler, repetitions, and anything that does not serve the argument.

## Audio and Podcasts

Audio is an underrated medium for learning. People listen while commuting, exercising, doing dishes.

### Recording basics

- **Quiet room.** Turn off fans, AC, washing machines.
- **Close mic.** 4-6 inches from the speaker.
- **Pop filter.** A cheap nylon screen prevents plosive breath blasts.
- **Record at 48 kHz, 24-bit** when possible. Higher than CD quality, which is the professional standard.

### Editing

- **Audacity** (free, open source) for quick edits.
- **Reaper, Logic, Audition** for production work.
- **Noise reduction** carefully -- too much and voices sound synthetic.
- **Normalize, then gentle compression** -- makes quiet voices audible without making loud voices painful.

## Presentations

Slides are a specific medium with its own discipline.

### Slides are not documents

The worst mistake in slide design is writing paragraphs on slides and reading them aloud. Slides are visual aids -- the words should be the title of the point, not the full argument. The full argument is what you say out loud.

### Less is more

One idea per slide. Big text. One image. If you need more, use more slides.

### No speaker notes on screen

Speaker notes are for the presenter. Audiences should see only the visual aids.

## Accessibility

Accessibility is not optional. It is the difference between making media for a narrow group and making media for everyone. WCAG (Web Content Accessibility Guidelines) is the international standard.

### Alt text

Every image on the web should have descriptive alt text so screen readers can describe it to blind users. Alt text should describe the function the image serves in the document, not just what is in the image.

- **Bad:** "image.jpg"
- **Bad:** "A chart"
- **Good:** "Bar chart showing global temperature rising 1.1 degrees Celsius from 1880 to 2020"

Decorative images should have empty alt text (alt="") so screen readers skip them.

### Captions

Every video should have captions. Automatic captions (YouTube, Otter, Whisper) are usable starting points but must be reviewed for accuracy, especially for technical terms and proper nouns.

### Color contrast

Text needs sufficient contrast against its background. WCAG AA requires a contrast ratio of 4.5:1 for normal text. Tools like the WebAIM Contrast Checker let you verify. Do not rely on color alone to convey meaning -- use shape, position, or text labels as well.

### Keyboard navigation

Every interactive element (button, link, form field) should be reachable by keyboard alone. This is both an accessibility requirement and a usability improvement for power users.

## Remix and Attribution

Remix is a legitimate creative practice. The ethical foundation is attribution.

### What remix is

Taking existing work and transforming it into something new: sampling music, making memes, mashing up videos, reimagining characters. Creative Commons licenses specifically enable this when the original creator consents.

### Attribution practice

When remixing CC-licensed work, always include: the original creator's name, the original work's title, the license, and a link back. "Title by Creator, licensed under CC-BY-SA 4.0" is the minimum.

### Original over remix

Even when attribution is perfect, the best creative growth comes from making your own work more than remixing others'. Remix teaches technique; originality teaches thought.

## When NOT to Use This Skill

- **Evaluating media someone else made.** Use `information-evaluation`.
- **Behavior around sharing.** Use `digital-citizenship`.
- **Understanding why media is reaching you.** Use `algorithmic-awareness`.

## Decision Guidance

When starting a new piece of media, answer three questions:

1. **What is the one thing this is saying?** If you cannot name it in a sentence, draft more before producing.
2. **Who is the intended audience?** Name a specific person (real or imagined).
3. **What is the minimum viable version?** Make that first. Iterate.

## Cross-References

- **jenkins agent:** Participatory culture, remix, transformative work
- **kafai agent:** Constructionist making, learning through production
- **ito agent:** Creative practice, connected learning
- **digital-citizenship skill:** Behavior around publishing and sharing
- **information-evaluation skill:** The reader's counterpart to the creator

## References

- Jenkins, H. (2006). *Convergence Culture: Where Old and New Media Collide*. NYU Press.
- Kafai, Y. B., & Burke, Q. (2014). *Connected Code: Why Children Need to Learn Programming*. MIT Press.
- Lessig, L. (2008). *Remix: Making Art and Commerce Thrive in the Hybrid Economy*. Penguin.
- Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation.
- Williams, R. (2014). *The Non-Designer's Design Book*. 4th edition. Peachpit Press.
