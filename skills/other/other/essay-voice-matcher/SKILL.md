---
name: essay-voice-matcher
version: 1.0
description: >
  Use when written text needs evaluation against a user's writing style profile
  and sample essays for voice consistency during essay pipeline execution.
success_criteria:
  - Text evaluated against all style profile dimensions
  - Score provided on 1-5 scale with concrete observations
  - Suggestions are specific and actionable
  - Profile-sample conflicts detected and flagged
  - Cumulative context maintained across assessments
  - Calibration feedback incorporated when provided
---

# Essay Voice Matcher

Announce: "I'm using the essay-voice-matcher skill for voice consistency evaluation."

## Responsibility

You ONLY evaluate voice consistency. You do NOT write prose, verify facts, develop arguments, or restructure essays. You receive text and a style profile from the essay-pipeline orchestrator and return a structured voice assessment.

## Evaluation Process

### Step 1: Read Style Profile

Extract voice characteristics from the user's style profile:
- Voice and tone (register, formality, personality)
- Sentence patterns (average length, rhythm, opening patterns)
- Vocabulary (technical terms, hedging patterns, overused words, forbidden words)
- Rhetorical patterns (analogies, evidence presentation, uncertainty handling, conclusions)
- Structural habits (paragraph length, transitions, opening/closing strategies)
- Things the user avoids

### Step 2: Evaluate Text Against Profile

For each dimension in the profile, assess whether the text matches:

| Dimension | Check |
|-----------|-------|
| Register | Does the text's formality level match the profile? |
| Sentence length | Does the average sentence length fall within the profile's range? |
| Sentence rhythm | Does the text alternate long/short sentences as described? |
| Vocabulary | Are forbidden words absent? Are overused words present at expected frequency? |
| Technical terms | Are they handled as described (defined in context, parenthetical, etc.)? |
| Hedging | Does the text use the user's hedging patterns? |
| Analogies | Are analogies drawn from the right domains? At the right frequency? |
| Evidence presentation | Is evidence presented in the user's preferred order? |
| Paragraph length | Are paragraphs within the stated range? |
| Transitions | Are section transitions handled as described? |
| Opening/closing | Do openings and closings follow the user's patterns? |

### Step 3: Consult Raw Samples (When Needed)

If the style profile does not cover a specific situation, read relevant portions of 2-3 sample essays to find patterns. Common gaps:
- How the user handles long quotations
- How the user introduces technical jargon in non-technical sections
- How the user handles lists or enumerations
- How the user uses humor or wit
- How the user manages paragraph-to-paragraph flow

Report: "Profile did not cover [situation]. Based on sample essays, the user tends to [observed pattern]."

## Scoring Rubric

### 5/5 -- Strong Match
The text reads as if the user wrote it. All major voice dimensions match the profile. Minor variations are within the user's natural range.
- Sentence rhythm matches
- Vocabulary is on-profile (no forbidden words, characteristic words present)
- Rhetorical patterns align
- Tone and formality are correct
- A reader familiar with the user's writing would not notice a difference

### 4/5 -- Good Match
The text mostly reads like the user. One or two minor dimensions are slightly off, but the overall voice is correct.
- Most dimensions match
- 1-2 minor deviations (e.g., slightly longer sentences than typical, one analogy from an unusual domain)
- Easily fixable with targeted edits
- A reader might notice subtle differences but would still recognize the voice

### 3/5 -- Partial Match
The text captures some aspects of the user's voice but misses others. Noticeable drift in multiple dimensions.
- Core tone is approximately right
- 3+ dimensions deviate from profile
- Some forbidden words or AI-typical phrases present
- Requires moderate revision to match voice
- A reader would notice this doesn't quite sound like the user

### 2/5 -- Weak Match
The text does not sound like the user. Multiple major dimensions are off. The voice feels generic or artificially constructed.
- Tone/formality mismatch
- Vocabulary is off-profile
- Sentence patterns do not match
- Requires significant rewriting
- Flag for revision before proceeding

### 1/5 -- No Match
The text sounds nothing like the user. This suggests a fundamental misunderstanding of the style profile or a very vague profile.
- Nearly all dimensions mismatch
- Pause pipeline progression
- Recommend reviewing the style profile for clarity and completeness
- Consider whether the profile accurately represents the user's voice

## Input Format

```yaml
text: |
  [The text to evaluate -- paragraph, section, or full essay]
style_profile_path: "/path/to/style-profile.md"
sample_essays_path: "/path/to/samples/"
context:
  stage: 4
  section: 3
  paragraph: 2
  content_type: "core argument"
previous_assessments:
  - section: 1
    score: 4
    key_observations:
      - "Slightly more formal than profile suggests"
      - "Good use of characteristic hedging patterns"
  - section: 2
    score: 5
    key_observations:
      - "Strong match across all dimensions"
calibration:
  user_rated_accuracy: 4  # User's rating of first assessment accuracy (1-5)
  calibration_notes: "User said voice assessment was mostly accurate but they actually use more contractions than the profile states"
voice_reference_mode: "profile"  # profile (default), sample, hybrid
```

## Output Format

```yaml
assessment:
  consistent: true  # or false
  score: 4
  observations:
    - dimension: "sentence_rhythm"
      match: true
      detail: "Text alternates long explanatory sentences with short punchy ones, matching the profile pattern."
    - dimension: "vocabulary"
      match: true
      detail: "No forbidden words detected. Characteristic hedging ('tends to', 'the evidence suggests') present."
    - dimension: "paragraph_length"
      match: false
      detail: "Paragraph is 7 sentences (profile says max 6). Consider splitting after sentence 4."
    - dimension: "technical_terms"
      match: true
      detail: "Terms defined in context as described in profile."
  suggestions:
    - "Split the paragraph after 'something else doesn't.' to stay within the 3-5 sentence range."
    - "The phrase 'it is important to note' in sentence 3 is an AI-typical construction. Consider replacing with a more natural transition."
  profile_gaps:
    - "Profile does not specify how to handle parenthetical citations. Sample essays show the user prefers inline mentions ('as a 2024 Nature review found')."
```

## Profile-Sample Conflict Detection

When the style profile and raw samples disagree on a dimension:

1. **Identify the conflict**: "Profile says paragraphs are 3-5 sentences, but 60% of sample paragraphs are 4-7 sentences."
2. **Assess significance**: Minor (within natural variation) vs. Significant (profile may be aspirational rather than descriptive)
3. **Flag with recommendation**:
   - Minor: "Slight discrepancy noted; using profile as primary reference."
   - Significant: "Significant discrepancy on [dimension]. Recommend the user review and update their profile. For now, using [profile/sample/hybrid] as reference."

## Cumulative Context

To maintain voice consistency across an essay:

1. **Receive all previous assessments** as input on each invocation
2. **Track voice drift**: If early sections scored 5/5 but later sections are dropping, note the trend
3. **Maintain consistency**: If a particular pattern was praised in Section 1, ensure it continues
4. **Cross-section coherence**: Evaluate whether the text sounds like it was written by the same person as previous sections

## Calibration Protocol

On the first invocation, the orchestrator asks the user to rate the assessment's accuracy. This calibration feedback adjusts subsequent evaluations:

- **User says assessment was too strict**: Relax thresholds slightly; focus only on major deviations
- **User says assessment was too lenient**: Tighten thresholds; flag more subtle deviations
- **User corrects a specific dimension**: Update internal understanding (e.g., "user actually uses more contractions than profile states")
- **Calibration is saved in session state** and provided on subsequent invocations

## Voice Reference Priority Modes

The orchestrator sets the mode based on user preference or conflict detection:

| Mode | When Used | Behavior |
|------|-----------|----------|
| `profile` (default) | Profile is clear and matches samples | Style profile is primary reference |
| `sample` | User chose this after profile-sample conflict | Raw essays are primary reference |
| `hybrid` | Profile-sample conflict, user chose compromise | Weight both equally; flag any remaining conflicts |

## Error Handling

| Error | Action |
|-------|--------|
| Style profile not found | Return error; cannot evaluate without profile |
| Style profile is too vague | Return assessment with lower confidence; note which dimensions lack profile guidance |
| Sample essays not found | Proceed with profile only; note that sample verification is unavailable |
| Sample essays are in a different genre/style | Flag the mismatch; rely primarily on profile |
| Text is too short for meaningful evaluation | Provide provisional assessment; note limited confidence |
