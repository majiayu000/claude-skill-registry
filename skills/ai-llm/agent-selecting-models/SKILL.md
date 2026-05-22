---
description: Guidance for selecting appropriate AI model (sonnet vs haiku) based on task complexity, reasoning requirements, and performance needs. Use when implementing agents or justifying model selection.
---

# Selecting AI Models for Agents

Guidelines for choosing between sonnet and haiku models based on agent capabilities and task requirements.

## When This Skill Loads

This Skill auto-loads when implementing agents or documenting model selection rationale.

## Available Models

### Sonnet (claude-sonnet-4-5)

**Characteristics**:

- Advanced reasoning capabilities
- Complex decision-making
- Deep pattern recognition
- Sophisticated analysis
- Multi-step orchestration
- Higher cost, slower performance

**Use for**: Complex, reasoning-intensive tasks

### Haiku (claude-haiku-3-5)

**Characteristics**:

- Fast execution
- Straightforward tasks
- Pattern matching
- Simple decision-making
- Cost-effective
- Lower cost, faster performance

**Use for**: Simple, well-defined tasks

## Decision Framework

### Use Sonnet When Task Requires:

✅ **Advanced Reasoning**

- Analyzing technical claims for subtle contradictions
- Distinguishing objective errors from subjective improvements
- Detecting false positives in validation findings
- Context-dependent decision-making
- Inferring user intent from ambiguous requests

✅ **Complex Pattern Recognition**

- Cross-referencing multiple documentation files
- Identifying conceptual duplications (not just verbatim)
- Detecting inconsistencies across architectural layers
- Understanding domain-specific patterns
- Recognizing semantic similarities

✅ **Sophisticated Analysis**

- Verifying factual accuracy against authoritative sources
- Assessing confidence levels (HIGH/MEDIUM/FALSE_POSITIVE)
- Evaluating code quality and architectural decisions
- Analyzing narrative flow and pedagogical structure
- Determining fix safety and impact

✅ **Multi-Step Orchestration**

- Coordinating complex validation workflows
- Managing dependencies between validation steps
- Iterative refinement processes
- Dynamic workflow adaptation
- Error recovery and retry logic

✅ **Deep Web Research**

- Finding and evaluating authoritative sources
- Comparing claims against official documentation
- Version verification across multiple registries
- API correctness validation
- Detecting outdated information

### Use Haiku When Task Is:

✅ **Pattern Matching**

- Extracting URLs from markdown files
- Finding code blocks by language
- Matching file naming patterns
- Regular expression searches
- Simple syntax validation

✅ **Sequential Execution**

- File existence checks
- URL accessibility validation
- Cache file reading/writing
- Date comparisons
- Status reporting

✅ **Straightforward Validation**

- Checking if files exist
- Verifying link format (contains `.md`)
- Counting lines or characters
- Comparing timestamps
- Simple YAML/JSON parsing

✅ **No Complex Reasoning**

- Tasks with clear pass/fail criteria
- No ambiguity or judgment required
- Deterministic outcomes
- No context analysis needed
- No trade-off decisions

✅ **High-Volume Processing**

- Checking hundreds of links
- Validating many files
- Batch operations
- Performance-critical tasks
- Cost-sensitive operations

## Model Selection Matrix

| Task Type          | Complexity  | Reasoning Required          | Recommended Model |
| ------------------ | ----------- | --------------------------- | ----------------- |
| Content creation   | High        | Yes (narrative, structure)  | **Sonnet**        |
| Factual validation | High        | Yes (source evaluation)     | **Sonnet**        |
| Quality assessment | High        | Yes (subjective judgment)   | **Sonnet**        |
| Fix application    | Medium-High | Yes (confidence assessment) | **Sonnet**        |
| Link checking      | Low         | No (exists/accessible)      | **Haiku**         |
| File operations    | Low         | No (read/write/move)        | **Haiku**         |
| Pattern extraction | Low         | No (regex matching)         | **Haiku**         |
| Cache management   | Low         | No (read/write/compare)     | **Haiku**         |

## Agent-Specific Examples

### Sonnet Examples

**docs-checker** (Complex validation):

```yaml
model: sonnet
```

**Reasoning**:

- Analyzes technical claims for contradictions
- Deep web research for fact verification
- Pattern recognition across multiple files
- Complex decision-making for criticality levels
- Multi-step validation orchestration

**docs-fixer** (Sophisticated analysis):

```yaml
model: sonnet
```

**Reasoning**:

- Re-validates findings to detect false positives
- Distinguishes objective errors from subjective improvements
- Assesses confidence levels (HIGH/MEDIUM/FALSE_POSITIVE)
- Complex decision-making for fix safety
- Trust model analysis (when to trust checker)

**docs-tutorial-checker** (Pedagogical analysis):

```yaml
model: sonnet
```

**Reasoning**:

- Evaluates narrative flow and learning progression
- Assesses hands-on element quality
- Analyzes visual completeness
- Determines tutorial type compliance
- Sophisticated quality judgment

### Haiku Examples

**docs-link-general-checker** (Straightforward validation):

```yaml
model: haiku
```

**Reasoning**:

- Pattern matching to extract URLs
- Sequential URL validation via requests
- File existence checks for internal references
- Cache management (read/write YAML, compare dates)
- Simple status reporting (working/broken/redirected)
- No complex reasoning required

**docs-file-manager** (File operations):

```yaml
model: haiku
```

**Reasoning**:

- Straightforward file operations (move, rename, delete)
- Simple path manipulation
- Git history preservation (scripted commands)
- No complex decision-making
- Deterministic outcomes

## Documenting Model Selection

### Model Selection Justification Pattern

Include in agent documentation to explain model choice:

**For Sonnet Agents**:

```markdown
**Model Selection Justification**: This agent uses `model: sonnet` because it requires:

- [Reasoning capability 1 - e.g., "Advanced reasoning to analyze technical claims"]
- [Reasoning capability 2 - e.g., "Deep web research to verify facts"]
- [Reasoning capability 3 - e.g., "Pattern recognition across multiple files"]
- [Decision-making type - e.g., "Complex decision-making for criticality levels"]
- [Orchestration need - e.g., "Multi-step validation workflow orchestration"]
```

**For Haiku Agents**:

```markdown
**Model Selection Justification**: This agent uses `model: haiku` because it performs straightforward tasks:

- [Simple task 1 - e.g., "Pattern matching to extract URLs"]
- [Simple task 2 - e.g., "Sequential URL validation via web requests"]
- [Simple task 3 - e.g., "File existence checks"]
- [Simple task 4 - e.g., "Cache management (read/write/compare)"]
- [Simple task 5 - e.g., "Simple status reporting"]
- No complex reasoning or content generation required
```

### Placement in Agent Files

Add justification near the top of agent file, after agent description:

```markdown
---
name: example-agent
description: Agent description here
model: sonnet
---

# Agent Name

**Model Selection Justification**: [justification here]

[Rest of agent documentation]
```

## Cost and Performance Considerations

### Sonnet Trade-offs

**Costs**:

- Higher per-token cost (~10x haiku)
- Slower response time
- More resource-intensive

**Benefits**:

- Higher quality reasoning
- Better context understanding
- More accurate decisions
- Handles ambiguity well

**Use when**: Quality and accuracy more important than cost/speed

### Haiku Trade-offs

**Benefits**:

- Lower per-token cost (~10x cheaper)
- Faster response time
- Efficient for high-volume tasks

**Limitations**:

- Less sophisticated reasoning
- May struggle with ambiguity
- Better for deterministic tasks

**Use when**: Cost and speed more important than complex reasoning

## Decision Checklist

Before selecting a model, ask:

1. **Does the task require judgment calls?**
   - Yes → Sonnet
   - No → Haiku

2. **Are there multiple valid interpretations?**
   - Yes → Sonnet
   - No → Haiku

3. **Does it need deep analysis of context?**
   - Yes → Sonnet
   - No → Haiku

4. **Will it make complex decisions?**
   - Yes → Sonnet
   - No → Haiku

5. **Is it high-volume, low-complexity?**
   - Yes → Haiku
   - No → Sonnet

6. **Does cost matter more than quality?**
   - Yes → Haiku
   - No → Sonnet

## Common Mistakes

❌ **Using Sonnet for Simple Tasks**:

```yaml
# Overkill - use haiku
model: sonnet # Just checking if files exist
```

❌ **Using Haiku for Complex Analysis**:

```yaml
# Insufficient - use sonnet
model: haiku # Analyzing code quality and architecture
```

✅ **Match Model to Task Complexity**:

```yaml
# Simple pattern matching
model: haiku

# Complex reasoning
model: sonnet
```

## Key Takeaways

- **Sonnet** = Complex reasoning, sophisticated analysis, multi-step orchestration
- **Haiku** = Simple tasks, pattern matching, straightforward validation
- **Document rationale** = Include model selection justification in agent files
- **Consider trade-offs** = Balance cost/speed vs quality/capability
- **Match complexity** = Use appropriate model for task requirements
- **When in doubt** = Choose sonnet for quality, haiku for speed/cost

Proper model selection ensures optimal performance, cost-effectiveness, and task completion quality.
