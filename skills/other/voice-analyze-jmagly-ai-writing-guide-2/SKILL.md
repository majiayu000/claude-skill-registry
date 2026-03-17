# voice-analyze

Reverse-engineer voice profiles from sample content by analyzing writing patterns.

## Triggers

- "analyze this writing style"
- "extract voice from..."
- "what voice is this?"
- "create profile from this sample"
- "match this writing style"

## Behavior

When triggered, this skill:

1. **Analyzes text samples** for:
   - Sentence structure and length patterns
   - Vocabulary sophistication and domain
   - Tone markers (formality, confidence, warmth)
   - Structural patterns (lists, examples, questions)
   - Perspective and voice choices

2. **Extracts measurable features**:
   - Average sentence length
   - Vocabulary complexity (syllables, word length)
   - Contraction usage
   - Personal pronoun frequency
   - Question density
   - List/bullet usage

3. **Maps features to voice dimensions**:
   - Statistical analysis → tone scale values (0-1)
   - Pattern detection → structure preferences
   - Vocabulary extraction → prefer/avoid lists

4. **Generates voice profile** matching the analyzed style

## Usage Examples

### Analyze Existing Documentation
```
User: "Analyze this writing style" + [paste technical docs]

Analysis:
- Formality: 0.7 (no contractions, structured sentences)
- Confidence: 0.85 (direct statements, few hedges)
- Warmth: 0.25 (impersonal, third-person)
- Complexity: 0.8 (technical vocabulary, long sentences)

Output: analyzed-technical-docs.yaml
```

### Match Brand Voice
```
User: "Extract voice from our marketing copy" + [paste samples]

Analysis:
- Formality: 0.3 (conversational, contractions)
- Confidence: 0.7 (benefit claims, but some hedging)
- Warmth: 0.85 (second person, friendly tone)
- Energy: 0.8 (exclamation points, action verbs)

Output: brand-marketing-voice.yaml
```

### Capture Personal Style
```
User: "Create profile from my blog posts" + [paste samples]

Analysis:
- Identifies personal writing quirks
- Extracts signature phrases
- Maps to voice dimensions

Output: personal-blog-voice.yaml
```

## Analysis Methodology

### Feature Extraction

| Feature | Measurement | Maps To |
|---------|-------------|---------|
| Sentence length | Avg words/sentence | complexity |
| Contractions | Frequency per 100 words | formality (inverse) |
| First person ("I", "we") | Frequency | warmth |
| Second person ("you") | Frequency | warmth |
| Passive voice | Percentage of sentences | confidence (inverse) |
| Questions | Per paragraph | warmth, engagement |
| Hedging words | "might", "perhaps", "could" | confidence (inverse) |
| Exclamation marks | Frequency | energy |
| Technical terms | Domain vocabulary density | complexity |

### Dimension Calibration

**Formality** (0-1):
- 0.0-0.3: Contractions frequent, casual language, fragments okay
- 0.4-0.6: Mixed style, professional but accessible
- 0.7-1.0: No contractions, complete sentences, formal structure

**Confidence** (0-1):
- 0.0-0.3: Many hedges ("might", "perhaps"), questions, qualifiers
- 0.4-0.6: Balanced certainty, occasional hedges
- 0.7-1.0: Direct statements, conclusions first, few qualifiers

**Warmth** (0-1):
- 0.0-0.3: Third person, passive voice, clinical tone
- 0.4-0.6: Professional but personable
- 0.7-1.0: Second person, inclusive language, empathetic

**Energy** (0-1):
- 0.0-0.3: Calm, measured, understated
- 0.4-0.6: Balanced engagement
- 0.7-1.0: Exclamation marks, action verbs, dynamic phrasing

**Complexity** (0-1):
- 0.0-0.3: Short sentences, simple vocabulary, accessible
- 0.4-0.6: Moderate complexity, clear but nuanced
- 0.7-1.0: Long sentences, technical vocabulary, layered ideas

### Vocabulary Extraction

**Signature phrases** - Identified by:
- Repeated patterns across samples
- Distinctive constructions
- Opening/closing patterns

**Domain vocabulary** - Extracted by:
- Technical term frequency
- Specialized jargon
- Industry-specific language

**Avoid patterns** - Detected by:
- Conspicuous absence of common phrases
- Consistent avoidance of certain constructions

## Output Format

```yaml
name: analyzed-sample-voice
version: 1.0.0
description: Voice profile extracted from sample content
analysis_source:
  sample_size: 1500  # words analyzed
  sample_count: 3    # number of samples
  confidence: 0.85   # analysis confidence score
tone:
  formality: 0.65
  confidence: 0.8
  warmth: 0.4
  energy: 0.5
  complexity: 0.7
vocabulary:
  prefer:
    - "extracted signature phrase 1"
    - "detected domain terminology"
  avoid:
    - "patterns not found in samples"
  signature_phrases:
    - "The key point is..."
    - "This demonstrates..."
structure:
  sentence_length: medium    # avg 15-20 words
  paragraph_length: medium   # avg 4-6 sentences
  sentence_variety: high     # varied structure detected
  use_lists: when-appropriate
  use_examples: frequently
  use_questions: rarely
perspective:
  person: third
  voice: active
  tense: present
extracted_patterns:
  opening_style: "context-first"
  closing_style: "conclusion-summary"
  transition_style: "logical-flow"
```

## CLI Usage

```bash
# Analyze from file
python voice_analyzer.py --input sample.txt

# Analyze from multiple files
python voice_analyzer.py --input "sample1.txt,sample2.txt,sample3.txt"

# Analyze from stdin (pipe content)
cat sample.txt | python voice_analyzer.py --stdin

# Specify output name
python voice_analyzer.py --input sample.txt --name my-extracted-voice

# Output to specific directory
python voice_analyzer.py --input sample.txt --output .aiwg/voices/

# JSON output for inspection
python voice_analyzer.py --input sample.txt --json
```

## Integration

- **Output**: Creates profiles usable by `voice-apply`
- **Chain**: `voice-analyze` → `voice-create` (to refine) → `voice-apply`
- **Chain**: `voice-analyze` + `voice-analyze` → `voice-blend` (combine styles)

## Accuracy Considerations

- **Minimum sample**: 500+ words for reliable analysis
- **Multiple samples**: 3+ samples improve accuracy
- **Consistent genre**: Mixing genres reduces accuracy
- **Confidence score**: Output includes analysis confidence (0-1)

## References

- Schema: `../../../schemas/voice-profile.schema.json`
- Dimensions guide: `../voice-apply/references/voice-dimensions.md`
- Generator: `../voice-create/scripts/voice_generator.py`
