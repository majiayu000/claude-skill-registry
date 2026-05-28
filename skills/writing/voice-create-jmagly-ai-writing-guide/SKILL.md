---
name: voice-create
description: Generate custom voice profiles from natural language descriptions. Use when relevant to the task.
---

# voice-create

Generate custom voice profiles from natural language descriptions.

## Triggers

- "create a voice for..."
- "new voice that sounds like..."
- "generate a voice profile for..."
- "make me a voice that is..."
- "define a writing voice for..."

## Behavior

When triggered, this skill:

1. **Parses the description** to identify:
   - Target audience (developers, executives, general public)
   - Tone characteristics (formal/casual, confident/tentative, warm/clinical)
   - Domain context (technical, marketing, academic, conversational)
   - Any specific constraints or preferences mentioned

2. **Maps description to voice dimensions**:
   - Formality (0-1): casual ↔ formal
   - Confidence (0-1): hedging ↔ assertive
   - Warmth (0-1): clinical ↔ friendly
   - Energy (0-1): calm ↔ enthusiastic
   - Complexity (0-1): simple ↔ sophisticated

3. **Generates vocabulary guidance**:
   - Preferred terms based on domain
   - Terms to avoid based on tone
   - Signature phrases that match the voice

4. **Creates structure patterns**:
   - Sentence length preferences
   - Paragraph structure
   - Use of lists, examples, analogies

5. **Outputs valid YAML** conforming to voice-profile.schema.json

## Usage Examples

### Technical Documentation Voice
```
User: "Create a voice for API documentation - precise, no-nonsense, assumes developer knowledge"

Output: technical-api-docs.yaml
- formality: 0.6
- confidence: 0.9
- warmth: 0.2
- energy: 0.3
- complexity: 0.8
- vocabulary: technical terms, code references, precise metrics
```

### Friendly Tutorial Voice
```
User: "Make me a voice for beginner tutorials - encouraging, patient, uses lots of analogies"

Output: beginner-tutorial.yaml
- formality: 0.2
- confidence: 0.7
- warmth: 0.9
- energy: 0.7
- complexity: 0.3
- vocabulary: everyday language, encouraging phrases, analogies
```

### Executive Summary Voice
```
User: "Generate a voice profile for board presentations - authoritative but accessible"

Output: board-presentation.yaml
- formality: 0.8
- confidence: 0.9
- warmth: 0.4
- energy: 0.5
- complexity: 0.6
- vocabulary: business metrics, strategic language, clear conclusions
```

## Output Location

Generated profiles are saved to:
1. `.aiwg/voices/{name}.yaml` (project-specific, default)
2. `~/.config/aiwg/voices/{name}.yaml` (user-wide, with --global flag)

## Voice Generation Process

### Step 1: Dimension Calibration

Parse natural language for dimension indicators:

| Description Keywords | Dimension | Value Range |
|---------------------|-----------|-------------|
| casual, relaxed, conversational | formality | 0.1-0.3 |
| professional, business | formality | 0.5-0.7 |
| formal, academic, official | formality | 0.8-1.0 |
| tentative, careful, hedging | confidence | 0.2-0.4 |
| balanced, measured | confidence | 0.5-0.7 |
| assertive, authoritative, direct | confidence | 0.8-1.0 |
| clinical, detached, objective | warmth | 0.1-0.3 |
| neutral, professional | warmth | 0.4-0.6 |
| friendly, warm, personable | warmth | 0.7-0.9 |
| calm, measured, understated | energy | 0.1-0.3 |
| balanced, engaged | energy | 0.4-0.6 |
| enthusiastic, dynamic, energetic | energy | 0.7-0.9 |
| simple, accessible, plain | complexity | 0.1-0.3 |
| clear, moderate | complexity | 0.4-0.6 |
| sophisticated, detailed, nuanced | complexity | 0.7-0.9 |

### Step 2: Domain Detection

Identify domain from context:
- **Technical**: API, code, system, architecture, implementation
- **Marketing**: brand, campaign, audience, engagement, conversion
- **Academic**: research, methodology, analysis, findings, literature
- **Executive**: strategy, ROI, stakeholder, decision, outcome
- **Support**: help, issue, solution, troubleshoot, resolve

### Step 3: Vocabulary Generation

Based on domain and tone, generate:
- 5-10 preferred terms
- 3-5 terms to avoid
- 2-4 signature phrases

### Step 4: Structure Selection

Map tone to structure patterns:
- High formality → longer sentences, structured paragraphs
- Low formality → shorter sentences, varied structure
- High confidence → direct statements, conclusions first
- High warmth → questions, inclusive language ("we", "let's")

## Integration

Works with other voice-framework skills:
- Created voices can be applied via `voice-apply`
- Created voices can be inputs to `voice-blend`
- `voice-analyze` can create base profiles that `voice-create` refines

## References

- Schema: `../../../schemas/voice-profile.schema.json`
- Dimensions guide: `../voice-apply/references/voice-dimensions.md`
- Built-in templates: `../../voices/templates/`
