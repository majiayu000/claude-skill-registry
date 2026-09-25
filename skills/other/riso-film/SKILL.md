---
name: riso-film
description: Design, build or improve procedural risograph animations and videos in this repo, including narrative films, abstract shorts, motion effects and visual inspection. Delivers self-contained Canvas 2D HTML and a verified MP4. For standalone still art use riso-still; for sound use riso-score. Not for editing tools/.
---

# Riso film

Deliver `films/<name>/index.html` plus a verified MP4 in `out/`. Every pixel is drawn in Canvas
2D; the deliverable has no libraries, fonts, images or network calls. External subject references
may be studied, never embedded. Paths are relative to the repo root; commands run in `tools/`.
Reference exclusions in the user's request take precedence.

## 1. Direction

Read `.claude/rules/riso-plates.md`, `docs/brief.md` and `docs/visual-development.md` first.
Add `docs/drawing.md` and `docs/motion.md` for what is being built, `docs/characters.md` for
people, animals or hands, `docs/scene-space.md` for complex objects, framing, perspective or
precise speed changes, and `docs/quality-bar.md` for print finish and playback defects. Load
`docs/sound.md` only when scoring. [examples.md](examples.md) maps techniques to the shipped
films; open the matching source before inventing a routine that already exists.

Extract subject, feeling, scope and constraints. For an open aesthetic brief, choose a direction
and proceed; if the user asks for proposals, propose first. Write `FILM.md` early: design
decisions, observed references, shot/action plan, user constraints, remaining work.

Plan actions and consequences, not illustrated nouns. Per substantial shot: camera and shot size,
what changes, a readable arrival/hold, and where the eye goes at the next cut. Keep subject
motion, camera motion, transition and atmosphere distinct. `docs/forms/resonance.md` is an
optional call-and-response form (used by `films/lumen` and `films/emergence`); use it only when
asked or deliberately chosen. A single journey through one fixed frame (`films/window-seat`) or
one continuous take of one event (`films/roost`, `films/nonpareil`, `films/eclosion`,
`films/passenger`) is an equally valid alternative to a montage. Preserve approved direction in revisions.

## 2. Prove the hard part first

Before filling a timeline, inspect real subject references and build one representative hard
frame. For complex art, compare small viewpoint/value thumbnails first. When the request remakes
a known video, measure the file itself (cuts, shots, actions) before choosing what to keep.
Figures get debug views and photo comparisons before shots: likeness judged at recognition scale,
a posable 3D hand per grip, 3D-solved arms (`docs/characters.md`). A subject that recurs at
several sizes goes on one sheet at its smallest and largest size first. Fix generic silhouettes
and inconsistent perspective before adding grain, hatching or more scenes.

Then build a short sample of the hardest action: the subject doing something, not just arriving.
Check attachments, mass, timing and aftermath. Encode that sample as soon as it exists
(`render.mjs --from a --to b`) and read its fastest frame at 1:1: strobing, mushy dots and bitrate
only show in the MP4. For a long film, make a full-duration silent rough cut before polishing.
Set holds and cut lengths from information and action, not equal slots or an
inherited timeline. These are working checks, not extra approval steps.

## 3. Build from a clean engine

```
node new-riso.mjs --kind film --duration 60 --out ../films/<name>/index.html
```

Choose the real duration. The generator refuses to overwrite and copies only the print, drawing
and motion kits plus `tools/lib/visual-kit.mjs`; it gives a blank `drawArt(t)`, a player and the
`__riso` contract. Edit the generated HTML directly. Copy routines from donors
(`prints/workings`, `studies/index.html`, the films in examples.md), never their scenes. When most
of the frame moves with tone (parallax, smears, moving gradients), copy the live-plate compositor
from `films/window-seat/index.html` (see `docs/live-plates.md`).

- Bake static scenes at displayed size. Screen moving geometry in page space. Reproject vectors
  for camera moves; never resize a screened bitmap.
- Share geometry between marks and their knockouts, and one clock between actions coupled
  across shots.
- Build in small batches; inspect each scene at its real duration and its render cost. Live
  plates run 100–200 ms/frame; profile per draw function before optimising
  (`docs/live-plates.md`, cost). The generated player buffers slow films, so share MP4s for
  judging pace.
- Keep `__riso.shots = [{id,start,end,readAt,action,transition}]` derived from the one
  authoritative timeline; `readAt` is a representative visible moment. No second set of timing
  constants.

## 4. Review picture and motion

```
node review.mjs ../films/<name>/index.html
node verify.mjs ../films/<name>/index.html
node shoot.mjs ../films/<name>/index.html --range 6.6:6.9:0.0333333333 --sheet --engine firefox
```

Use this film's event times. Read every sheet you generate. `verify.mjs` proves seek purity in
both browsers across the actual duration and shot boundaries; it proves repeatability, not beauty
or stable adjacent-frame texture, and a sheet cannot judge pacing or choppiness at speed. When it
fails, its `DIAGNOSIS` line names the per-seek state or the earlier frame that poisons the time.
Measure the playback defects in `docs/quality-bar.md` (flicker, jitter, pops, held stretches) and
watch a silent range render; `docs/motion.md` lists the traps that pass verify.

Inspect frame-spaced strips around handoffs, contacts, mask completions and visible wraps, on both
sides of each reset. For a retimable effect check 0.5x, 1x and 2x and move coupled clocks and holds
together. Settle texture questions on native PNGs or 1:1 crops; reduced sheets invent moiré and
hide small subjects. `docs/quality-bar.md` separates art, construction, print, action, pacing and
delivery evidence.

## 5. Export and finish

```
node render.mjs ../films/<name>/index.html --from 0 --to 6 --engine firefox --out ../out/section.mp4
node render.mjs ../films/<name>/index.html --fps 30 --size 1080 --engine firefox
node review.mjs ../films/<name>/index.html --mp4 ../out/<name>.mp4
```

Range renders are silent; render the whole film after picture review. `review.mjs --mp4` lists
every held stretch with its shot; confirm each is an intended hold (`--from` for a range render).
Score with `riso-score` first when sound is wanted. Decode the final MP4 and check duration,
dimensions, frame count and audio; inspect encoded motion too. Record evidence, remaining
weaknesses and anything not reviewed in `FILM.md`. Technical validity is not the user's artistic
approval.

For revisions, read `FILM.md` and edit the authoritative HTML; never rerun an old assembly script
over revised art. Keep the previous render for comparison and preserve approved pacing and score
during local fixes. Cut secondary detail before compromising the hard frame, the full progression
or verification.

When handing a revision to a fresh session, write a self-contained prompt: the film path; read
`FILM.md` first and treat `index.html` as authoritative; the user's words quoted; what is approved
and must not change, by time range; copy the delivered MP4 and WAV to `-v1` before editing; each
suspected cause labelled unconfirmed with the check that would confirm it; and how to read the
file safely (sampled films carry multi-MB lines). Keep it in the film folder (`HANDOVER.md`).
