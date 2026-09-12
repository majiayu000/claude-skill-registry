---
name: illustrated-gallery
description: "Build an illustrated portfolio, creative-studio landing page, or brand showcase with a static art gallery and full-frame ASCII dissolve transitions. Use when the user requests Illustrated Gallery, this visual template, or $illustrated-gallery. Do not use for generic dashboards, standalone ASCII art, or image-to-video generation."
---

# Illustrated Gallery

Create a website from the retained [source template](assets/source/index.html).
Use [artifact-template.json](artifact-template.json) for reference paths. Preserve
its visual system and accepted interactions while adapting content to the brief.

## Workflow

1. Inspect the target project and its instructions. For a new site, copy
   `assets/source` into a new working directory; leave the skill's source intact.
   For an existing site, adapt only the requested surface instead of replacing
   the entire project.
2. Identify the audience, brand, text, and illustration subjects from the request.
   The five blue botanical artworks are examples, not mandatory subjects or a
   fixed image count.
3. Retain the large artwork stage, fixed text layer, restrained floating card,
   serif headline hierarchy, and compact navigation unless the user requests
   changes. Keep images still between transitions.
4. Replace or generate a coherent image set, then adjust each mobile crop and
   keep text and cards clear of faces, bird heads, and flower centers.
5. Validate the complete interaction and responsive layout. Prepare static output
   only when needed for hosting; use the user's authorized hosting workflow.

## Accepted interaction contract

- Keep the full-frame ASCII dissolve, approximately 1.5 seconds long. Reuse the
  implementation in [app.js](assets/source/app.js); do not substitute an edge wipe
  or ordinary crossfade as an unsolicited optimization.
- Keep artwork static. Do not add warping, ripples, floating particles, pointer
  parallax, or zoom unless explicitly requested. Improve image composition or
  crop instead when the image feels flat.
- Treat subject motion, slide transitions, and scroll animation independently.
  A request to stop image motion must not remove the transition animation.
- Preserve autoplay, pause, previous/next, direct slide selection, touch swipes,
  and reduced-motion support. Pause stops autoplay; manual navigation still works.
- Reuse existing sections without adding dashboards, forms, configuration panels,
  or theme systems. The sample brief-download form saves a local file; do not
  describe it as sending a message or collecting a lead.

## Artwork direction

Use user-provided images or an available image-generation tool. Keep a consistent
palette, drawing medium, lighting, and detail density across the set. If new
image generation is required but unavailable, report that limitation rather than
claiming example assets were newly generated.

For this composition, start with wide 16:9 artwork, a quiet left region for
headlines, and a subject near the center-right. Change this composition when the
text layout changes. Structure prompts around purpose, subject, scene, medium,
palette, focal placement, and text-free output. For example:

> Wide editorial illustration for a creative studio. An ivory heron among lotus
> leaves, fine blue ink engraving, restrained teal and ivory palette, subject at
> center-right, quiet dark left region for a headline. No text, logo, or border.

Set each `slides[].focus` independently for mobile. Never reuse one crop for all
subjects without inspecting it. Use full-sized WebP for the stage and smaller
WebP thumbnails for the work grid. Preload the current and next full-sized image;
load the remainder on demand.

## Source and runtime

- Edit branding and sections in [index.html](assets/source/index.html), visual
  rules in [style.css](assets/source/style.css), and image lists, crop positions,
  and transitions in [app.js](assets/source/app.js). The brief download heading
  and filename derive from the header `.brand` label and text, so rebranding the
  header keeps the downloaded markdown in sync without a separate JS edit.
- Keep the dependency-free HTML/CSS/JavaScript stack for new template sites.
  Do not introduce a framework solely to reuse the design.
- When changing image count, synchronize the slide array, initial counter,
  selection buttons, work cards, and total. Runtime counters use `slides.length`.
- Find and edit the relevant CSS declaration or media query rather than appending
  more overrides to the stylesheet.
- The retained `.openai/hosting.json` contains only static output configuration.
  When using Sites, follow the installed Sites workflow and register a new site.
  Never restore the original deployment ID or overwrite an unrelated live site.
- Without Sites, serve or host the same static files using the target project's
  established workflow. Do not invent an unavailable deployment integration.

## Build and verification

There are no build dependencies. In the new project, run `node --check app.js`.
For static hosting, create `out/`, copy `index.html`, `style.css`, `app.js`, and the
referenced WebP assets into it, preserving the `assets/` paths. Do not package
Git metadata, credentials, runtime files, or unused large image originals.

Done when:

- Every referenced script and image exists, all images load, and the counts and
  selection states agree with the actual artwork list.
- The full transition is observed in a browser, not merely checked for errors;
  images remain still before and after it.
- Pause, direct selection, wraparound, touch navigation, and reduced motion work.
- Desktop and mobile crops preserve subjects, floating cards do not obscure the
  focal point, and there is no horizontal overflow.
- The initial page loads only the current and next full-size artwork; work-grid
  thumbnails do not force all full-size images to load.

Use available browser tooling for these checks. If unavailable, report the exact
unverified behavior; syntax checks alone do not prove visual fidelity.

## Autonomy and gotchas

Perform requested local edits, previews, and validation directly. Honor explicit
local-only requests. Publishing, paid media generation, permissions, and existing
production changes require authorization for that action and destination; reuse
approval already provided in the conversation.

A still image distorted by a shader is not a generated video. A successful build
is not proof of the requested visual effect. If a user rejects an animation,
change that specific animation and preserve the other accepted interactions.
