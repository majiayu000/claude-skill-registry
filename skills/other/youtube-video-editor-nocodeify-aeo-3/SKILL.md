---
name: youtube-video-editor
description: Edit YouTube videos using Ed Lawrence's retention-focused editing system with tournament-style thumbnail selection. Use when the user needs editing guidance, thumbnail creation, visual metaphor implementation, or production quality advice. Optimizes for viewer satisfaction through strategic cuts, pacing, and visual elements.
---

# YouTube Video Editor (Ed Lawrence Method + Thumbnail Tournament)

Edit videos that maximize retention through strategic cuts, visual metaphors, and the "boring but engaging" principle.

## Core Workflow

The editing process follows these steps:

1. **Raw Footage Review** - Identify key moments and visual metaphor needs
2. **Retention Edit** - Cut for engagement, not perfection
3. **Visual Layer** - Add graphics, frameworks, metaphors
4. **Thumbnail Tournament** - Generate and test 5 variations (5 → 3 → 1)
5. **Final Polish** - Audio, pacing, export

---

## Video Editor Tool (`tools/video-editor-remotion/`)

**Status:** Work in progress - core layouts working, more animations coming.

Claude can programmatically edit videos using the Remotion-based video editor. This generates a `timeline.json` that drives React-based rendering.

### Why Remotion (not MoviePy)

| Feature | MoviePy (old) | Remotion (current) |
|---------|---------------|-------------------|
| Styling | PIL drawing, complex math | CSS - just works |
| Borders | Manual superellipse paths | `border-radius` + `corner-shape` |
| Shadows | Complex compositing | `box-shadow` |
| Preview | Render to test | Live browser preview |

**Key discovery:** CSS `corner-shape: superellipse(2)` creates true iOS-style squircles.

### Available Layouts

| Layout | Description | Use Case |
|--------|-------------|----------|
| `speaker_full` | Speaker fills entire frame | Intro, personal stories, transitions |
| `slide_full` | Slide fills frame, speaker audio continues | Teaching, CTA slides, complex diagrams |
| `split_right` | Slide ~76% left, speaker ~24% right (squircle) | Teaching with speaker visible |
| `split_left` | Speaker ~24% left, slide ~76% right | Teaching with speaker (variety) |
| `jump_zoom_in` | Animated zoom punch (15-25%) | End of powerful statements, key reveals |
| `jump_zoom_out` | Animated zoom back to normal | After hold period |
| `jump_cut_in` | Instant zoom (no animation) | HOLD after jump_zoom_in |
| `jump_cut_out` | Instant back to normal | Hard cut reset |
| `zoom_transition_in` | Slide → Speaker with continuous zoom | Smooth transition to speaker |
| `zoom_transition_out` | Speaker → Slide with continuous zoom | Smooth transition to slide |
| `gradual_zoom` | Slow drift zoom over entire segment (10-15%) | Speaker segments, subtle movement |
| `gif_overlay` | GIF on top of speaker video | Reaction GIFs, humor beats (1-3s) |
| `gif_full` | GIF fills frame (speaker audio continues) | Big meme moments (2-4s) |
| `text_overlay` | Text on speaker video (Syne font, off-white) | Key words, stats, framework names (1-3 words) |

### Layout Distribution (~20% each)

| Layout | % of Video | When to Use |
|--------|------------|-------------|
| `speaker_full` | ~20% | Intro, personal stories, trust-building, transitions |
| `slide_full` | ~20% | Teaching, complex diagrams, CTA slides |
| `split_right` | ~20% | Teaching with speaker visible |
| `split_left` | ~20% | Teaching with speaker visible (variety) |
| `jump_zoom` + `gradual_zoom` | ~20% | Emphasis, energy, movement |

**No single layout dominates** - keeps visual variety throughout the video.

### Timeline Format

```json
[
  {"type": "speaker_full", "start": 0, "end": 3.0},
  {"type": "split_right", "start": 3.0, "end": 25.0, "content": "slides/slide-01.jpg"},
  {"type": "jump_zoom_in", "start": 25.0, "end": 26.5, "zoom": 1.20},
  {"type": "jump_zoom_out", "start": 26.5, "end": 28.0},
  {"type": "slide_full", "start": 28.0, "end": 35.0, "content": "slides/slide-02.jpg"}
]
```

### Zoom Guidelines

**Minimum 10% Rule:** All zooms must be at least 10% to be noticeable.

| Zoom Type | Amount | Duration | Use Case |
|-----------|--------|----------|----------|
| Jump zoom (standard) | 15-20% (1.15-1.20) | 0.3-0.5s | Emphasis, reveals |
| Jump zoom (major) | 20-25% (1.20-1.25) | 0.3-0.5s | Surprising numbers, breaking misconceptions |
| Gradual zoom in | 10-15% (1.10-1.15) | 4-10s | Energy, excitement |
| Gradual zoom out | 10-15% | 4-10s | Calm, reflective |

### Emphasis Hierarchy

| Level | Technique | Frequency |
|-------|-----------|-----------|
| **Subtle** | Layout change, gradual zoom | Frequent |
| **Moderate** | 15% jump zoom | Regular |
| **Strong** | 20% jump zoom | Sparingly |
| **Maximum** | 25% jump zoom | Rarely |

### When to Use Each Layout

**speaker_full:**
- Video introduction/welcome
- Personal stories
- Building trust moments
- Transitions between major sections

**slide_full:**
- Teaching content
- CTA slides (aeoprotocol.ai)
- Complex diagrams that need full attention

**split_right / split_left:**
- Teaching content with speaker visible
- Bullet points, lists, diagrams
- Alternate between right/left for variety

**jump_zoom_in → jump_cut_in → jump_zoom_out:**
- End of powerful statements
- Surprising numbers or results
- Key value propositions
- **Always HOLD with jump_cut_in before zooming out**

**zoom_transition_in/out:**
Smooth transitions between any layouts with continuous motion.

| Transition | Direction | Duration | What Happens |
|------------|-----------|----------|--------------|
| `zoom_transition_out` | Any → Slide-focused | 1-2s | Zooms OUT, cuts to slide_full or split |
| `zoom_transition_in` | Any → Speaker-focused | 1-2s | Zooms IN, cuts to speaker_full |

**Critical Rules:**
1. **Never zoom IN to slides** - cuts off content
2. **Match zoom levels** - Previous segment's zoom MUST match transition's starting zoom

**Zoom Level Matching (IMPORTANT):**

Before transitions: ramp UP to match starting zoom.
After `zoom_transition_in`: next segment must be zoomed in, then zoom out.

```json
// WRONG (jump before):
{"type": "speaker_full", ...},
{"type": "zoom_transition_out", "zoom": 1.15, ...}

// WRONG (jump after zoom_transition_in):
{"type": "zoom_transition_in", "zoom": 1.15, ...},
{"type": "speaker_full", ...}

// CORRECT (before):
{"type": "gradual_zoom", "zoomStart": 1.0, "zoomEnd": 1.15},
{"type": "zoom_transition_out", "zoom": 1.15, ...}

// CORRECT (after zoom_transition_in):
{"type": "zoom_transition_in", "zoom": 1.15, ...},
{"type": "jump_cut_in", "zoom": 1.15},
{"type": "jump_zoom_out", "zoom": 1.15},
{"type": "speaker_full", ...}
```

**Jump Zoom Emphasis Rules:**
- Key statistic: 20% zoom, 0.3-0.5s
- Surprising claim: 20-25%, 0.3-0.5s
- Word punch: 15-20%, 0.2-0.3s
- Max 1 per 30-60 seconds
- **Never back-to-back zoom sequences** - minimum 1s `speaker_full` breather between any two zoom sequences. A zoom-out immediately followed by a zoom-in feels abrupt and jarring.

**Supported Transitions:**
- `speaker_full` → `slide_full` (default)
- `speaker_full` → `split_right/left` (use `"toLayout": "split_right"`)
- `split_right/left` → `speaker_full` (use `"fromLayout": "split_right"`)
- `split_right/left` → `slide_full` (use `"fromLayout": "split_right"`)
- `slide_full` → `speaker_full` (default)

**gradual_zoom:**
- Applied over entire speaker segment
- Alternates in/out for variety
- Adds subtle movement/energy

### Split Layout Details

The split layout uses:
- Grid background video (`public/grid-loop.mp4`)
- Glass borders: 16px width, `rgba(120, 140, 160, 0.6)`
- Slide: 16:9 aspect ratio, rounded corners (`border-radius: 32px`)
- Speaker: True squircle shape using CSS:
  ```css
  border-radius: 50%;  /* Half the width */
  corner-shape: superellipse(2);  /* iOS-style continuous curve */
  ```
- Drop shadow: `0 8px 32px rgba(0, 0, 0, 0.4)`
- Padding: 64px edges, 32px gap between elements

---

## Core Principle: Edit for Retention, Not Perfection

**What viewers care about:**
- Is this keeping my attention?
- Am I learning something?
- Is this worth my time?

**What viewers DON'T care about:**
- Perfect lighting
- Professional studio
- Color grading
- Smooth transitions

**Ed's Rule:** "If it doesn't improve retention or understanding, don't add it."

---

## Step 1: Raw Footage Review

Before cutting, identify:

### Key Moments to Keep:
- Hook (first 30-60 seconds) - CRITICAL
- Framework explanations
- Stories/examples
- Results/proof (numbers, screen recordings)
- Visual metaphor setups
- Payoff/resolution
- CTA

### What to Cut Mercilessly:
- Umms, ahhs, verbal filler
- Long pauses (>2 seconds)
- Repetition of same point
- Tangents that don't serve script
- Setup that doesn't pay off
- "So, yeah..." or "Basically..."
- Anything that doesn't educate OR inspire

### Visual Metaphor Needs:
For each framework/concept in script, identify:
- What visual metaphor was planned?
- What graphics/diagrams needed?
- What screen recordings to include?
- What text overlays to add?

Document before cutting.

---

## Step 2: The Retention Edit (Ed & Greg System)

Ed's editing philosophy: **"Boring but informative beats flashy but empty"**

### Hook Editing (First 60 Seconds)

The hook decides if viewers stay. Edit aggressively.

**First 30s:** Max 5 seconds per segment. Something must change every 3-5 seconds — layout, zoom, text, GIF. All types fair game. At least 1 text overlay + 1 jump zoom.

**30-60s:** Max 7 seconds per segment. Still faster than the rest. Introduce first slides/teaching.

**60s+:** Normal pacing (5-15s segments).

### The Jump Cut System

**Ed's Approach:**
- Cut EVERY pause >1 second
- Cut all verbal filler
- Keep the pace moving
- BUT: Don't cut so fast it's jarring

**The Balance:**
- Too slow = viewers leave
- Too fast = viewers exhausted
- Sweet spot = conversational but tight

**Rule of thumb:**
- 1-2 second pauses: Keep (natural rhythm)
- 2-3 second pauses: Consider cutting
- 3+ second pauses: Always cut (unless intentional dramatic pause)

### Text Overlay Rules

Text overlays use Syne font, off-white (`#e8e4e0`) by default, with pop animation.

**CRITICAL:** Text overlays go ONLY on `speaker_full` segments. NEVER on slides or splits.

| Style | Position | Use Case |
|-------|----------|----------|
| `caption` | Bottom | Supporting emphasis |
| `center` | Big center | Framework names, key stats, impact moments |
| `heading` | Top area | Section headers |

**Rules:**
- 1-3 words max (power words: "AEO", "$100K", "THIS IS KEY")
- Duration 1.5-3 seconds
- Max 1 per 30-60 seconds
- Timed to when speaker says the word

### GIF Rules

GIFs add humor beats and pattern interrupts.

| Type | Use | Duration |
|------|-----|----------|
| `gif_overlay` | Reaction on speaker video | 1-3s |
| `gif_full` | Full screen meme moment | 2-4s |

**Rules:**
- Max 1 GIF per 45-60 seconds
- Always AFTER the statement (punctuate, don't interrupt)
- Never during: important explanations or data on screen
- 6-10 GIFs per 10-minute video

### When to Let It Breathe

**Don't cut everything:**
- After making a key point (2 second pause lets it sink in)
- Before a big reveal (build tension)
- During emotional moments (authenticity matters)
- When showing complex visuals (give time to read)

**Ed's Principle:** "Cut for meaning, not for speed."

### The Pacing Pattern

**Typical 10-minute video:**

**0:00-1:00 (Hook):** FAST pace
- Tight cuts
- High energy
- No wasted words
- Goal: Stop scrolling

**1:00-2:00 (Setup):** MEDIUM pace
- Slightly more breathing room
- Build context
- Still tight, but not frantic

**2:00-8:00 (Main Content):** VARIED pace
- Fast during transitions
- Slower during key explanations
- Speed up for examples
- Slow down for frameworks

**8:00-10:00 (Payoff):** MEDIUM pace
- Deliberate delivery
- Let key points land
- Build to satisfying conclusion

**10:00-11:00 (CTA):** FAST pace
- Quick recap
- Clear next step
- Strong ending

### Cuts That Kill Retention

**Avoid:**
- Cutting mid-word (makes you look choppy)
- Cutting between related sentences (breaks flow)
- Cutting before a payoff (creates confusion)
- Cutting natural gestures (looks unnatural)

**Instead:**
- Cut between complete thoughts
- Cut at natural breath points
- Preserve the setup → payoff flow
- Keep gestures that enhance meaning

---

## Step 3: Visual Layer (Where Ed Excels)

Ed's secret: **"Make the invisible visible."**

### Visual Metaphors on Screen

**For every framework, put it ON SCREEN:**

**Example: "The House of Cards"**
- Don't just say it
- Show an actual house of cards graphic
- Label the rows (Foundation, Middle, Top)
- Point to each row as you discuss it
- Viewers can SEE the metaphor

**Example: "The DM Leak"**
- Show a funnel with holes
- Money dripping out
- Label each hole with a problem
- Animate the leak as you explain

**Example: "The $100k ARR Ladder"**
- Show actual ladder graphic
- Each rung labeled with milestone
- Highlight current rung
- Show path to next rung

**Rules for visual metaphors:**
- Simple graphics (not overcomplicated)
- High contrast (readable on mobile)
- On screen for 5-10 seconds minimum
- Match your verbal explanation timing
- Can be hand-drawn style (authenticity > polish)

### Graphics and Text Overlays

**When to use text on screen:**

**Key Statistics:**
- "$100k ARR" appears on screen when you say it
- "90% of DMs go unanswered" 
- Any specific number worth emphasizing

**Framework Names:**
- "The House of Cards Framework" as title card
- "The DM Leak System"
- Brand your frameworks visually

**Key Quotes:**
- Your most important sentence
- Put it on screen as you say it
- Makes it memorable + shareable

**Lists/Steps:**
- "Mistake #1" appears on screen
- "Step 2: Planning"
- Helps viewer follow structure

**Text Overlay Rules:**
- Large font (readable on mobile)
- High contrast (white text on dark background or vice versa)
- On screen for entire sentence (not just flash)
- Maximum 5-7 words per overlay
- Simple animation (fade in, not spinning)

### B-Roll and Screen Recordings

**Ed rarely uses B-roll, but when he does:**

**Screen recordings:**
- DM conversations
- Revenue dashboards
- Analytics screenshots
- Process demonstrations
- Tool walkthroughs

**When showing screens:**
- Zoom in enough to read on mobile
- Highlight/circle key elements
- Don't show for too long (5-10 seconds max)
- Always narrate what viewer should notice

**B-roll (if used):**
- Only if it enhances understanding
- Never for decoration
- Must be relevant to what you're saying
- Keep it minimal

**Ed's Principle:** "Face-to-camera > B-roll for business content"
- Viewers connect with faces
- B-roll can feel like filler
- Only use when it adds clarity

---

## Step 4: Professional Thumbnail Creation

Thumbnail = 50% of video success. Must look like Netflix, not webcam.

### Workflow

1. **Extract freeze frame** from video with correct expression
2. **Run through Imagen** with prompt (adds text, effects, color grade)
3. **Review at mobile size** (160x90px)
4. **Export** JPEG under 2MB

### The 1+1=3 Rule

Title and thumbnail must COMPLEMENT, not repeat:

| Title Does | Thumbnail Does |
|------------|----------------|
| Creates curiosity about WHAT | Creates emotion about WHY IT MATTERS |
| Story setup | Stakes or payoff |

**Test:** If thumbnail text appears in title, you've failed.

### Professional Text Effects (MANDATORY)

Every text element needs this effects stack:

| Effect | Hero Text | Secondary Text |
|--------|-----------|----------------|
| **Stroke** | 6px black | 4px black |
| **Drop Shadow** | 12px, 25px blur, 90% black | 8px, 15px blur, 80% black |
| **Outer Glow** | 40px, 25% opacity | 20px, 15% opacity |

**Text that looks amateur:** Flat, no stroke, no shadow
**Text that looks pro:** Stroke + shadow + glow, pops off any background

### Text Sizing

| Element | Size (% of frame height) |
|---------|--------------------------|
| **Hero word** | 25-40% |
| **Secondary** | 12-18% |

### Color Palette

| Use Case | Color | Hex |
|----------|-------|-----|
| Default/success | Yellow | #FFE135 |
| Warning/loss | Red | #FF4444 |
| Achievement | Gold | #C9A86C |
| Tech/new | Teal | #00D4FF |
| Secondary text | White | #FFFFFF |
| All strokes | Black | #000000 |

### Cinematic Color Grade

Apply to EVERY freeze frame:

1. Crush blacks to navy (#0A1628)
2. Increase contrast 15-20%
3. Desaturate midtones 10-15%
4. Add subtle teal to shadows
5. Add dark vignette

**Result:** Netflix thumbnail, not webcam screenshot.

### Layout

```
+---------------------------------------+
|  [HERO TEXT - yellow]           [YOU] |
|  [Secondary - white]            RIGHT |
|                                  40%  |
|  [Visual Metaphor]                    |
|  (subtle accent)                      |
|                          [TIMESTAMP]  |
+---------------------------------------+
```

### Visual Metaphors

ONE per thumbnail (maximum), subtle accent:

| Concept | Visual | Opacity |
|---------|--------|---------|
| Money | Dollar amount, car | 40-50% |
| Invisible | Fading logo | 30-60% |
| Success | Trophy, #1 | 40-50% |
| Decline | Downward graph | 50-60% |

### Freeze Frame Selection

| Video Type | Expression |
|------------|------------|
| Confidence | Slight smirk |
| Concern | Furrowed brow |
| Success | Eyebrows raised |
| Authority | Serious, pointing |

**Technical:** Eyes open, not mid-word, sharp focus.

### Never Do

- Flat text without effects (amateur)
- Shocked/screaming face (clickbait)
- Red arrows and circles (2015)
- Ungraded raw footage
- Text repeating the title
- More than 5 words

See `youtube/templates/thumbnail-style-guide.md` for full specifications.

---

## Step 5: Final Polish

### Audio Optimization

**What matters:**
- Clear, intelligible speech
- Consistent volume
- No distracting background noise

**What doesn't matter:**
- Studio-quality sound
- Perfect acoustic treatment
- Expensive microphone (good USB mic is fine)

**Quick audio fixes:**
- Normalize audio levels
- Remove background hum/noise
- Slight compression for consistency
- Don't over-process (natural > perfect)

### Music and Sound Effects

**Ed's approach: Use sparingly or not at all**

**When to use music:**
- Background music can HURT business content
- Viewers may find it distracting
- If you use it: very low volume, subtle

**When NOT to use music:**
- During teaching/explanation
- When showing numbers/data
- During key points
- In hook (let your words do the work)

**Sound effects:**
- Whoosh for transitions (optional, subtle)
- Ding for key points (optional, minimal)
- Ed's preference: None. Let content carry itself.

### Export Settings

| Setting | Value |
|---------|-------|
| Resolution | 3840×2160 (4K) |
| FPS | 30 |
| Codec | H.264 |
| Format | MP4 |
| Bitrate | 35-45 Mbps |

**Why 4K at 40Mbps:**
- YouTube re-encodes everything - higher source = better result
- 4K gets VP9 codec on YouTube (better quality per bit)
- 35-45 Mbps is YouTube's recommended range for 4K

**Remotion render command:**
```bash
npx remotion render MainVideo out/video.mp4 --video-bitrate=40M --props='{"config":{...}}'
```

---

## The "Good Enough" Principle

### What Actually Matters for Business YouTube

**Critical (spend time here):**
- ✅ Tight retention editing
- ✅ Visual metaphors on screen
- ✅ Clear audio
- ✅ Strong thumbnail
- ✅ Good hook

**Doesn't matter (don't waste time):**
- ❌ Color grading
- ❌ Fancy transitions
- ❌ Studio lighting
- ❌ Expensive camera
- ❌ Professional backdrop

**Ed's Philosophy:**
"Business viewers care about learning, not production value. Edit for clarity, not beauty."

### Common Editing Mistakes

**Mistake 1: Over-editing**
❌ Every transition has an effect
✅ Simple cuts, let content shine

**Mistake 2: Too much B-roll**
❌ Cutting away from your face constantly
✅ Stay on face, add graphics when needed

**Mistake 3: Slow pacing**
❌ Leaving in all pauses and filler
✅ Cut tight, keep it moving

**Mistake 4: No visual metaphors**
❌ Just talking head for 10 minutes
✅ Put your frameworks on screen

**Mistake 5: Clickbait thumbnails**
❌ Screaming face + 10 words + effects
✅ Clean, simple, credible

**Mistake 6: Ignoring mobile**
❌ Text too small to read on phone
✅ Test thumbnail at phone size

---

## Editing Workflow (Practical)

### Time Budget for 10-Minute Video

**Total editing time: 2-4 hours**

**Breakdown:**
- Initial watch & note-taking: 15 minutes
- Retention edit (cuts): 60 minutes
- Visual layer (graphics/text): 45 minutes
- Thumbnail creation: 30 minutes
- Thumbnail tournament: 15 minutes
- Audio polish: 15 minutes
- Final review: 15 minutes
- Export & upload: 15 minutes

### Editing Software Recommendations

**Ed's approach: Use what you know**

**Good options:**
- Premiere Pro (industry standard, powerful)
- Final Cut Pro (Mac, intuitive)
- DaVinci Resolve (free, pro-level)
- CapCut (simple, fast, growing)

**Ed's principle:** "Software doesn't matter. Retention editing does."

### Batch Processing

**If making multiple videos:**
- Edit all at once (same day)
- Use templates for graphics
- Save thumbnail style
- Consistent export settings
- Streamline workflow

**Benefits:**
- Faster per-video
- More consistent look
- Easier to delegate
- Better use of time

---

## Visual Metaphor Library (Build This)

Create reusable graphics for your frameworks:

**Examples to build:**
- Your signature frameworks as graphics
- Common metaphors in your niche
- Number overlays (revenue, statistics)
- Before/after templates
- Step-by-step graphics

**Reuse across videos:**
- Builds brand recognition
- Saves editing time
- Creates consistency
- Viewers recognize your style

---

## Output Format

When providing editing guidance, structure as:

```
=== RETENTION EDIT PLAN ===
Hook (0:00-1:00): [Pacing notes]
Setup (1:00-2:00): [Cut strategy]
Main Content (2:00-8:00): [Key moments to emphasize]
Payoff (8:00-10:00): [Pacing notes]
CTA (10:00-11:00): [Cut strategy]

=== VISUAL LAYER PLAN ===
Visual Metaphor 1: [Timing, description]
Visual Metaphor 2: [Timing, description]
Text Overlays: [Key statistics/quotes to put on screen]
Screen Recordings: [What to show, when]

=== THUMBNAIL TOURNAMENT ===
[5 thumbnail variations]
[Round 1: 5 → 3]
[Round 2: 3 → 1]
WINNER: [Description + why it won]

=== TECHNICAL SPECS ===
Resolution: 1080p
Frame Rate: 30fps
Export: MP4 (H.264)
Thumbnail: 1280x720, <2MB
```

---

## Advanced Techniques

### The "Ed Style" Thumbnail

**Characteristics:**
- Clean, professional, not clickbait
- Your face, usually serious expression
- 2-3 words maximum
- Often uses "boring" in the text ironically
- High contrast
- Stands out by NOT being loud

**Why it works:**
- Pattern interrupt (calm in sea of chaos)
- Signals credibility
- Attracts right audience
- Repels wrong audience

### Tension Through Editing

**Ed's secret: Editing can BUILD tension**

**Techniques:**
- Cut faster as you approach reveal
- Use silence before big point (cut the pause BEFORE, not during)
- Visual metaphor appears at payoff moment
- Quick cuts for examples, slow cuts for key points

### The Hook Edit

**Most important 60 seconds of editing:**

**Rules:**
- ZERO wasted frames
- Every cut intentional
- Text overlays for key stats
- Your best facial expressions
- Fastest pacing of entire video
- If viewer survives first 60 seconds, they'll watch

---

## Thumbnail A/B Testing

After tournament winner is selected:

**Test with audience:**
- Post in community: "Which thumbnail?"
- Ask 5-10 people from your avatar
- Look for strong reactions (positive or negative)
- Pick the one that polarizes (not the safe choice)

**After publish:**
- YouTube allows thumbnail changes
- If CTR is low after 48 hours, try runner-up
- Compare performance
- Learn what works

---

## Remember:

- **Edit for retention, not perfection** - Tight cuts beat pretty shots
- **Visual metaphors are non-negotiable** - Put frameworks on screen
- **Thumbnails = 50% of success** - Use tournament, test variations
- **"Boring but informative" beats flashy** - Business audience values substance
- **Good enough is good enough** - Don't over-polish
- **Face-to-camera > B-roll** - Connection beats decoration

**Ed's final principle:** "If the foundation (goals, ideation, planning) is solid, editing is easy. If the foundation is weak, no amount of editing will save it."

Edit strategically. Test thumbnails systematically. Ship it.
