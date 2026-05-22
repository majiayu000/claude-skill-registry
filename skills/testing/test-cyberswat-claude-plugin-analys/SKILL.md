---
name: test
description: Run the analysis framework against predefined scenarios and evaluate output quality. Use after making changes to validate the framework.
context: fork
allowed-tools: [Read, WebFetch, WebSearch, Grep, Glob]
---

# Analysis Framework Test

Run the full analysis pipeline against predefined scenarios and evaluate output quality. This gives a repeatable way to validate the framework after changes.

## How This Works

You will execute the full pipeline internally for each scenario below. For each scenario:

1. Run each pipeline step sequentially within this context, following the instructions from each skill
2. Score each step's output against the rubric
3. Produce a quality report

Since you are running in a forked context, you cannot invoke skills as separate commands. Instead, execute each step inline by following the skill instructions directly:

- **Research**: Gather external context using the research skill instructions
- **Evaluate**: Analyze from five perspectives with assumption tracking
- **Critique**: Adversarial stress test with severity framework and pre mortem
- **Synthesize**: Structured synthesis with confidence and categorized open questions
- **Decide**: Decision landscape, type detection, and user checkpoint

## Test Scenarios

### Scenario 1: Strategic / Business

**Topic**: "Should we reorganize the data platform team from functional silos into cross functional pods?"

**What this tests**: The framework's ability to handle org design, stakeholder complexity, and decisions with long feedback loops. The decide step should likely produce a Phased Approach given the uncertainty inherent in organizational change.

### Scenario 2: People / Coaching

**Topic**: "A senior engineer is technically excellent but consistently undermines team psychological safety in code reviews. How should their manager approach this?"

**What this tests**: Whether the decide step can produce a Navigational approach rather than a rigid action. Whether the framework handles interpersonal nuance without collapsing complexity into false simplicity.

### Scenario 3: Technical

**Topic**: "Should we migrate our primary datastore from PostgreSQL to DynamoDB for a service handling 50k requests per second with unpredictable traffic spikes?"

**What this tests**: The standard technical decision path. This is the scenario type the framework was originally designed for. Serves as a baseline to ensure changes did not regress existing strengths. The decide step should likely produce a Clear Choice or Phased Approach.

## Scoring Rubric

Score each step on a 1 to 5 scale across the dimensions listed. A score of 3 is adequate. A score of 5 represents exceptional quality.

### Research Scoring
- **Source diversity**: Did it draw from multiple source types, not just one category?
- **Recency**: Are sources current year or last 12 months?
- **Evidence quality flagging**: Did it honestly assess evidence strength?
- **Gaps identified**: Did it acknowledge what it could not find?
- **Inaccessible source handling**: Did it log failed sources, attempt alternatives, and flag skew?

### Evaluate Scoring
- **Perspective distinctness**: Do the five views genuinely differ, or are they variations of the same take?
- **Assumption explicitness**: Did each perspective list its key assumptions?
- **Research grounding**: Does the Informed perspective reference specific research findings?
- **Contrarian strength**: Did the Contrarian construct assumption failure scenarios?
- **Weighting provided**: Did it identify which perspectives matter most for this decision?

### Critique Scoring
- **Severity calibration**: Did it use the Fatal / Serious / Notable framework appropriately?
- **Pre mortem specificity**: Is the pre mortem a realistic narrative or generic hand waving?
- **Genuine adversarial stance**: Did it actually try to break the idea, or did it soft pedal?
- **Cross domain coverage**: If applicable, did it surface meaningful cross domain concerns?
- **Evaluate reference**: Did it build on evaluate output rather than starting from scratch?

### Synthesize Scoring
- **Critique integration**: Did it explicitly address how critique findings influenced the recommendation?
- **Confidence calibration**: Is the confidence level honest and justified?
- **Open question categorization**: Are questions properly sorted into the three categories?
- **Survived assumptions**: Did it list the load bearing assumptions?
- **Actionability**: Could someone act on this synthesis without needing to reread the full analysis?

### Decide Scoring: Extra Scrutiny
- **Decision landscape breadth**: Did it present multiple genuinely viable paths, or was one obviously dominant?
- **Decision type detection**: Did it correctly identify whether this is a Clear Choice, Phased, or Navigational decision?
- **Format adaptation**: Did the output format match the decision type?
- **User checkpoint**: Did it ask the user to confirm rather than declaring a final answer?
- **Actionability**: Would the recommended path actually help someone act, or does it feel generic?

**Scenario specific decide checks**:

- **Scenario 1, Strategic**: Did it recommend a Phased Approach given the inherent uncertainty? Did it include an evaluation milestone?
- **Scenario 2, People**: Did it produce a Navigational format? Did it avoid collapsing a nuanced coaching situation into a binary "do X" declaration? Does the approach include signals to watch for and adjustment guidance?
- **Scenario 3, Technical**: Did it present a clear technical comparison in the landscape? Are the reversal triggers technically specific?

## Output Format

For each scenario, produce:

```
## Scenario [N]: [Name]

### Step Scores
| Step | Dim 1 | Dim 2 | Dim 3 | Dim 4 | Dim 5 | Average |
|------|-------|-------|-------|-------|-------|---------|
| Research | | | | | | |
| Evaluate | | | | | | |
| Critique | | | | | | |
| Synthesize | | | | | | |
| Decide | | | | | | |

### Decide Deep Dive
- Decision type detected: [type]
- Decision type appropriate: Yes / No
- Paths presented: [count]
- User checkpoint present: Yes / No
- Scenario specific check: [Pass / Fail with note]

### Strengths
[What worked well in this scenario]

### Weaknesses
[What needs improvement]

### Overall Score: [average across all steps] / 5
```

After all three scenarios:

```
## Framework Summary

### Overall Average: [X] / 5
### Strongest Step: [step name and why]
### Weakest Step: [step name and why]
### Priority Improvements: [ranked list of what to fix first]
```

## Execution Notes

- Run all three scenarios sequentially within this context
- Be honest in scoring. The purpose is to find weaknesses, not to validate
- If a step produces poor output, score it low and explain why specifically
- The people/coaching scenario is the hardest test. Pay extra attention to whether the framework handles nuance here.
- Keep individual pipeline step outputs concise since you are running three full pipelines. Focus on quality of the output, not length.

Subject: $ARGUMENTS
