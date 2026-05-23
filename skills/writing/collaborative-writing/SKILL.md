---
name: collaborative-writing
description: Co-create any professional writing through Socratic dialogue using established voice patterns
---

# Collaborative Writing

## Purpose
Guide professional and institutional writing projects from conceptual intent to polished draft through Socratic questioning and collaborative development. This skill integrates your established voice patterns and language preferences (when available) to ensure authentic, effective communication.

**Core principle:** Begin with inquiry to clarify purpose, audience, and tone. Once alignment is achieved, shift into co-writing — proposing language, testing phrasing, and refining meaning in partnership.

## Invocation Triggers
- "Help me write [message/statement/letter]"
- "Co-write this with me"
- "Draft [communication type]"
- "Develop [professional writing piece]"

## Optional Inputs

**Lexicon Dependencies (enhance quality when available, not required):**
- `~/lexicons_llm/03_narrative_patterns.md` (for structure and storytelling patterns)
- `~/lexicons_llm/04_language_bank.md` (for voice consistency and preferred language)
- `~/career-applications/[job-slug]/01-job-analysis.md` (if writing is job-related)

**User-Provided:**
- Writing purpose and audience
- Any existing drafts or relevant materials
- Context (why this communication, what outcome desired)

## Announce at Start

> "I'm using the Socratic-Collaborative Writing Skill to refine and co-develop your message."

---

## The Process

## Phase 0: Lexicon Loading (Conditional)

**First, gather any existing materials:**

1. **Ask for rough writing:**
   ```
   Do you have any rough writing you'd like to use?

   This could be:
   - Draft paragraphs or fragments
   - Earlier versions you want to refine
   - Stream-of-consciousness notes
   - Any text you've already started

   If yes, please share it. If no, that's perfectly fine — we'll develop from scratch.
   ```

2. **Ask for bullet points or ideas:**
   ```
   Do you have any bullet points or ideas you'd like to include in the narrative?

   This could be:
   - Key points you want to make
   - Important details or examples
   - Specific phrases or concepts
   - Ideas you want to weave in

   Please share any bullets or ideas you have. If none yet, we'll discover them through dialogue.
   ```

**Capture user inputs:**
- If rough writing provided:
  - Extract key ideas and convert to bullet points for Phase 2 (Message Architecture)
  - Store original text as reference for Phase 4 (Drafting)
- If bullet points provided: Integrate into Phase 2 (Message Architecture)
- If neither provided: Proceed with pure Socratic discovery

---

**Determine writing context:**

Ask user: "What type of writing are we developing together?"
- Job-related (cover letter, application statement, professional bio for job search)
- General professional (recommendation letter, professional statement, article, blog post)
- Other communication

**If job-related writing:**
1. Ask: "What is the job slug (directory name) for this application?"
   - Example: "ucla-arts-director"
   - Construct path: `~/career-applications/[job-slug]/`

2. **Attempt to load lexicons:**
   ```
   Try: ~/lexicons_llm/03_narrative_patterns.md
   Try: ~/lexicons_llm/04_language_bank.md
   Try: ~/career-applications/[job-slug]/01-job-analysis.md
   ```

3. **Report status clearly:**
   ```
   ✓ Lexicons loaded:
     - Narrative patterns: [brief description of what's available]
     - Language bank: [brief description of what's available]
     - Job analysis: [if available]

   I'll reference your established voice patterns throughout the process.
   ```

   OR

   ```
   ℹ Lexicons not found (this is fine!)

   We'll develop your writing through Socratic dialogue alone.
   I'll help you discover and articulate your authentic voice through our conversation.
   ```

**If general professional writing:**
1. **Attempt to load lexicons:**
   ```
   Try: ~/lexicons_llm/03_narrative_patterns.md
   Try: ~/lexicons_llm/04_language_bank.md
   ```

2. **Report status clearly:**
   ```
   ✓ Lexicons loaded:
     - Narrative patterns: Found your established storytelling patterns
     - Language bank: Found your preferred language and phrases

   I'll reference these to maintain voice consistency.
   ```

   OR

   ```
   ℹ No existing lexicons found (this is perfectly fine!)

   We'll collaborate to develop your message from scratch.
   The Socratic process will help us discover the right voice together.
   ```

**Key principle:** Lexicons are helpful but NOT required. Proceed confidently with or without them.

---

## Phase 1: Discovery Dialogue

**Goal:** Establish shared clarity on purpose, audience, and context.

**Method:** Ask one question at a time — often multiple choice — to uncover:

### 1A. Strategic Intent and Timing
- What is the primary purpose of this communication?
- What outcome do you hope to achieve?
- Why now? What's the context or timing?
- What happens if this message succeeds? If it doesn't land?

**Examples:**
- "Is this message primarily intended to: (A) Inform, (B) Persuade, (C) Celebrate, (D) Request action?"
- "What would success look like three months after this is sent?"

### 1B. Target Audience and Desired Response
- Who is the primary audience?
- What secondary audiences might see or influence this?
- What do they already know? What do they believe?
- What emotional or intellectual shift do you want to create?

**Examples:**
- "How would you describe your reader's current mindset?"
- "What do you want them to think or feel after reading?"

### 1C. Emotional and Tonal Objectives
- What emotional register feels right: formal, warm, urgent, reflective?
- Should this feel personal or institutional?
- What relationship are you establishing or reinforcing?

**Examples:**
- "On a scale from 'conversational' to 'ceremonial,' where does this land?"
- "Should your voice feel like: (A) Trusted advisor, (B) Passionate advocate, (C) Thoughtful colleague, (D) Authoritative expert?"

### 1D. Constraints
- Are there approval processes or stakeholders to consider?
- Are there sensitivities, topics to avoid, or political dynamics?
- What format or length is expected?
- What's the deadline?

**Examples:**
- "Will this go through review before publication?"
- "Are there organizational politics or sensitivities I should know about?"

**Output: Intent Statement**

After discovery dialogue, synthesize:

```
## Intent Statement

Purpose: [Primary goal of the communication]
Audience: [Primary and secondary audiences]
Desired Response: [What you want readers to think/feel/do]
Tone: [Emotional register and voice stance]
Constraints: [Key considerations: length, approvals, sensitivities]
Context: [Timing and situational factors]

Does this capture your intent accurately?
```

**Wait for user confirmation before proceeding.**

> **Transition cue:** "Shall we move from discovery into message shaping?"

---

## Phase 2: Message Architecture

**Goal:** Identify and organize the core ideas and their relationships.

**Method:** Continue the Socratic process to establish message hierarchy.

### 2A. Essential Ideas or Calls to Action
- What are the 2-4 core ideas that must be communicated?
- Is there a specific action you're requesting?
- What's the most important thing you want them to remember?

**Examples:**
- "If they only remember one thing from this message, what should it be?"
- "What points are essential versus nice-to-have?"

### 2B. Supporting Details and Evidence
- What examples, stories, or evidence strengthen each core idea?
- Which credentials, experiences, or data points matter most?
- What details build trust or credibility?

**Examples:**
- "What proof points make each claim believable?"
- "Which stories or examples illustrate these ideas most powerfully?"

### 2C. Narrative or Emotional Arc
- How should the reader's understanding evolve through the piece?
- Should the argument build linearly, or circle back to a central theme?
- What's the emotional journey: problem → solution? Present → future? Challenge → opportunity?

**Examples:**
- "Should we structure this as: (A) Chronological story, (B) Problem-solution, (C) Thematic progression, (D) Contrasting perspectives?"
- "What emotional movement do you want: calm→inspired? concerned→hopeful? curious→convinced?"

**Output: Message Map**

After architecture dialogue, synthesize:

```
## Message Map

Core Ideas:
1. [First essential idea]
   - Supporting evidence: [examples/proof]
   - Why it matters: [significance]

2. [Second essential idea]
   - Supporting evidence: [examples/proof]
   - Why it matters: [significance]

3. [Third essential idea, if applicable]
   - Supporting evidence: [examples/proof]
   - Why it matters: [significance]

Narrative Arc: [How ideas connect and flow]
Emotional Journey: [How reader's perspective should shift]

Call to Action: [Specific request or desired response, if applicable]

Does this structure capture your message effectively?
```

**Wait for user confirmation before proceeding.**

> **Transition cue:** "Would you like me to suggest how these points could be expressed or ordered?"

---

## Phase 3: Framing and Voice Calibration

**Goal:** Define the emotional texture, voice, and stylistic stance.

**Method:** Explore through contrast and testing.

### 3A. Voice Exploration Through Contrast

Ask questions that reveal preferences:

- "Which framing resonates more: (A) 'We achieved X by doing Y' or (B) 'Through Y, we were able to achieve X'?"
- "Should this feel more like: (A) Strategic vision, (B) Practical execution, (C) Both equally?"
- "Which opening feels right: (A) Leading with the problem, (B) Leading with the vision, (C) Leading with a story?"

### 3B. Emotional Register and Stylistic Stance

Test voice dimensions:
- Authoritative ↔ Collaborative
- Warm ↔ Professional
- Reflective ↔ Declarative
- Narrative ↔ Analytical
- Personal ↔ Institutional

**Examples:**
- "Should this piece feel more reflective-thoughtful or more declarative-confident?"
- "How much of 'you' should be visible in the writing?"

### 3C. Language Choices and Authenticity

Explore phrasing preferences:
- Active vs. passive constructions
- Sentence rhythm: Short and punchy vs. flowing and complex
- Metaphors or concrete language
- Technical precision vs. accessible explanation

### 3D. Lexicon-Enhanced Voice Calibration (If Lexicons Loaded)

**If narrative_patterns.md and language_bank.md are available:**

After initial voice exploration, provide enhanced analysis:

```
## Voice Calibration: Enhanced with Your Lexicon

Based on our conversation and your established patterns:

### From Your Narrative Patterns (narrative_patterns.md):
- **Opening strategies you favor:** [List patterns found]
- **Evidence presentation:** [How you typically structure proof]
- **Narrative rhythm:** [Sentence structure observations]
- **Recurring structures:** [Frameworks you use consistently]

### From Your Language Bank (language_bank.md):
- **Preferred action verbs for this context:** [List 8-12 verbs]
- **Power phrases you've used successfully:** [List 4-6 phrases]
- **Industry/field-specific terms:** [Relevant terminology]
- **Phrasing patterns:** [How you typically construct key ideas]

### Recommended Voice for This Piece:
[Synthesis of:]
1. Audience needs from Intent Statement
2. Message requirements from Message Map
3. Your authentic patterns from lexicons
4. Voice preferences from our exploration

This approach will sound like you while serving your strategic intent.

Does this voice profile feel authentic and appropriate?
```

**If lexicons NOT loaded:**

Provide voice summary based purely on dialogue:

```
## Voice Profile

Based on our conversation, here's the voice I'm hearing:

Tone: [Description based on user's choices]
Rhythm: [Sentence structure preferences]
Stance: [Relationship to reader]
Language level: [Formality, technical depth]
Emotional register: [Where on key dimensions]

Key voice principles:
- [Principle 1 from user's preferences]
- [Principle 2 from user's preferences]
- [Principle 3 from user's preferences]

Does this feel right for your message?
```

**Output: Voice Profile**

Wait for user confirmation.

> **Transition cue:** "Ready for me to propose a short passage or sample paragraph in this voice?"

---

## Phase 4: Collaborative Drafting

**Goal:** Move from reflection to writing.

**Method:** Co-create the text based on agreed message framework.

### 4A. Drafting Approach

**Explain the process:**
```
I'll draft this in small segments (50-150 words at a time) so we can refine together.

After each segment, I'll ask:
- "Does this feel aligned with your voice?"
- "Would you like me to adjust tone, focus, or rhythm?"
- "Should we try a different approach to this section?"

We'll build the complete draft iteratively, keeping your authentic voice throughout.
```

### 4B. Sequential Drafting with Voice Consistency

**For each section of the Message Map:**

1. **Draft a segment** (50-150 words)
   - Use Voice Profile guidelines
   - Follow Message Map structure
   - Maintain Intent Statement objectives

2. **Present the draft segment:**
   ```
   ## [Section Name] - Draft Segment

   [50-150 words of drafted text]

   Does this feel aligned with your voice and intent?
   Would you like me to:
   - Adjust the tone (more/less formal, warm, direct)?
   - Change the focus or emphasis?
   - Try a different rhythm or phrasing?
   - Keep it as-is and continue?
   ```

3. **If lexicons loaded: Voice Consistency Check**

   After each segment, verify against language bank:

   ```
   Quick consistency check against your lexicon:

   ✓ Action verbs used: [list verbs from this segment]
     - From your language bank: [which ones match user's patterns]
     - New verbs introduced: [note any that aren't in lexicon]

   ✓ Phrasing patterns: [note alignment with narrative_patterns.md]

   ✓ Rhythm check: [does sentence structure match user's natural flow]

   Does this maintain your authentic voice?
   ```

4. **Incorporate feedback iteratively**
   - If user requests changes, draft alternative version
   - Ask clarifying questions: "More like [option A] or [option B]?"
   - Keep the Socratic tone alive through revision

5. **Continue to next segment**
   - Build on established voice
   - Maintain narrative arc from Message Map
   - Check connections between segments

### 4C. Mid-Draft Check-In

**After completing 2-3 segments:**

```
## Mid-Draft Review

We've developed:
- [Segment 1 name]: [brief summary]
- [Segment 2 name]: [brief summary]
- [Segment 3 name]: [brief summary]

How is the voice feeling overall?
- Is the tone consistent and appropriate?
- Are we maintaining the narrative arc?
- Should we adjust anything before continuing?
```

### 4D. Complete the Draft

Continue the iterative process through all sections of the Message Map until complete.

**Output: Refined Draft**

After all segments are complete:

```
## Complete Draft

[Full compiled draft]

---

Total length: [word count]
Sections completed: [list all sections]

This draft incorporates:
- Strategic intent from our Discovery phase
- Message structure from our Architecture phase
- Voice calibration from our Framing phase
[If lexicons loaded:]
- Your established narrative patterns and language preferences

Ready for final alignment review?
```

> **Transition cue:** "Would you like me to compile this into a polished version for final review?"

---

## Phase 5: Alignment and Adaptation

**Goal:** Validate resonance and adaptability.

**Method:** Reflect and refine collaboratively.

### 5A. Intent Alignment Check

**Review against Intent Statement:**

```
## Final Alignment Review

Let's verify this draft achieves your original intent:

✓ Purpose: [Original purpose] → Does the draft accomplish this?
✓ Audience: [Target audience] → Will they respond as intended?
✓ Desired Response: [Original goal] → Does the draft evoke this?
✓ Tone: [Original tone objective] → Is the voice appropriate?
✓ Constraints: [Original constraints] → Are these respected?

What feels fully aligned? What needs refinement?
```

### 5B. Resonance Testing

**Test the draft's authenticity:**

- "Read this aloud to yourself. Does it sound like you?"
- "Imagine sending this today. What feels confident? What feels uncertain?"
- "If your ideal reader responded enthusiastically, what would they reference?"

### 5C. Adaptability Exploration

**Consider the draft's flexibility:**

```
How might this adapt across contexts?

1. **Platform variations:**
   - Email version: [suggest key changes if needed]
   - LinkedIn/public version: [suggest adaptations]
   - Formal presentation: [note what would change]

2. **Length variations:**
   - Condensed (50% length): [identify core elements to keep]
   - Expanded (150% length): [suggest where to add depth]

3. **Audience variations:**
   - If reader were more senior: [note tone adjustments]
   - If reader were less familiar with context: [note explanation needs]

Does the core message maintain coherence across these variations?
```

### 5D. Final Refinements

Based on alignment review:

1. **Identify any remaining gaps:**
   - Sections that feel weak or incomplete
   - Transitions that need smoothing
   - Tone inconsistencies
   - Missing context or examples

2. **Make targeted revisions:**
   - Draft alternatives for weak sections
   - Strengthen connections between ideas
   - Refine opening and closing if needed

3. **Confirm completion:**
   ```
   Does this draft fully achieve your intent?
   Are you ready to move forward with it?
   ```

**Output: Finalized Message Framework and Draft**

```
## Final Deliverable

[Complete polished draft]

---

### Framework Summary

Intent: [Achieved purpose]
Voice: [Established tone and stance]
Structure: [Narrative arc used]
Key Strengths: [What makes this effective]
[If lexicons used:] Voice Consistency: Aligned with your established patterns

This message is ready for [intended use].
```

### 5E. File Output

**Ask user where to save:**

```
Where should I save this final draft?

Suggestions based on writing type:

[If job-related:]
- Recommended: ~/career-applications/[job-slug]/05-cover-letter-draft.md
- Or: ~/career-applications/[job-slug]/[custom-name].md

[If general professional:]
- Recommended: ~/Documents/[descriptive-name].md
- Or: [user-specified path]

Please provide the full path where you'd like this saved.
```

**Save the file with complete content:**
- Full draft
- Framework summary
- Date created
- Process notes (optional)

**Confirm completion:**
```
✓ Saved to: [file path]
✓ Word count: [count]
✓ Ready for: [next step: review, editing, submission, etc.]

Your collaborative writing process is complete!
```

---

## When to Revisit Earlier Phases

**Return to previous phases anytime:**

- **Back to Discovery (Phase 1)** if:
  - Strategy, audience, or purpose shifts mid-process
  - You realize the original intent wasn't clearly defined
  - External feedback introduces new priorities or constraints

- **Back to Architecture (Phase 2)** if:
  - A section feels tonally inconsistent or unclear
  - The message structure isn't supporting the argument
  - You need to add or remove key ideas
  - The narrative arc isn't flowing naturally

- **Back to Voice Calibration (Phase 3)** if:
  - The draft doesn't sound authentic
  - Feedback suggests tone is off-target
  - You need greater emotional or institutional balance
  - Different sections have inconsistent voice

**Remember:** Returning to earlier dialogue is not regression — it's refinement. The Socratic process is iterative, not linear.

---

## Success Criteria

This collaborative writing process succeeds when:

1. **Voice authenticity:** The final draft sounds genuinely like you
   - If lexicons loaded: Consistent with your established patterns
   - If no lexicons: Voice feels natural and authentic to user's preferences

2. **Strategic clarity:** The message achieves its intended purpose
   - Intent Statement objectives are met
   - Audience will respond as desired
   - Call to action (if any) is clear and compelling

3. **Structural integrity:** The message is well-organized and flows naturally
   - Message Map architecture is evident but not rigid
   - Narrative arc guides reader through intended journey
   - Transitions between ideas are smooth

4. **Tonal consistency:** Voice is appropriate and maintained throughout
   - Voice Profile is honored across all sections
   - Tone matches audience expectations and relationship
   - Emotional register is consistent with intent

5. **User confidence:** You feel ready to use this writing
   - Proud to send/publish it
   - Confident it represents you well
   - Clear on any next steps (review, editing, adaptation)

---

## Working With and Without Lexicons

**This skill is designed to work excellently in both scenarios:**

### When Lexicons Are Available:
- Voice calibration is enhanced with your established patterns
- Language consistency is verified against your preferences
- Narrative structures align with your proven approaches
- The process feels like "amplifying your authentic voice"

### When Lexicons Are Not Available:
- The Socratic dialogue discovers your voice through conversation
- We build voice patterns collaboratively through the process
- Testing and iteration reveal your authentic preferences
- The process feels like "discovering your authentic voice together"

**Both approaches produce high-quality, authentic writing. The difference is whether we're referencing established patterns or discovering them fresh.**

---

## Related Skills

- **For job applications:** `skills/career/cover-letter-voice` (more structured, job-specific)
- **For job analysis:** `skills/career/job-description-analysis` (understanding the opportunity)
- **For strategic planning:** `skills/career/job-fit-analysis` (identifying gaps and strategy)

---

## Remember

- Start with Socratic discovery, then shift to co-writing when intent and tone are clear
- Ask one question at a time in early phases; test ideas collaboratively in later ones
- Lexicons enhance the process but are never required
- Move fluidly between questioning, suggesting, and revising
- Keep alignment with strategic intent as the north star
- Reflection and writing are partners, not steps in opposition
- The best writing emerges from thoughtful dialogue, not formulaic process
