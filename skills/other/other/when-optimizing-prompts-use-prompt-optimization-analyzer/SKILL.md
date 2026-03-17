---
name: when-optimizing-prompts-use-prompt-optimization-analyzer
version: 1.0.0
description: Active diagnostic tool for analyzing prompt quality, detecting anti-patterns, identifying token waste, and providing optimization recommendations
tags:
  - meta-tool
  - prompt-engineering
  - optimization
  - analysis
  - diagnostics
complexity: MEDIUM
agents_required:
  - code-analyzer
  - researcher
auto_trigger: false
---

# Prompt Optimization Analyzer

**Purpose:** Analyze prompt quality and provide actionable optimization recommendations to reduce token waste, improve clarity, and enhance effectiveness.

## When to Use This Skill

- Before publishing new skills or slash commands
- When prompts exceed token budgets
- When responses are inconsistent or unclear
- During skill maintenance and refinement
- When analyzing existing prompt libraries

## Analysis Dimensions

### 1. Token Efficiency Analysis
- Redundancy detection (repeated concepts, phrases)
- Verbosity measurement (word count vs. information density)
- Compression opportunities (equivalent shorter forms)
- Example bloat (excessive or redundant examples)

### 2. Anti-Pattern Detection
- Vague instructions ("do something good")
- Ambiguous terminology (undefined jargon)
- Conflicting requirements (contradictory rules)
- Missing context (insufficient background)
- Over-specification (unnecessary constraints)

### 3. Trigger Issue Analysis
- Unclear activation conditions
- Overlapping trigger patterns
- Missing edge cases
- Too broad/narrow scope

### 4. Structural Optimization
- Information architecture (logical flow)
- Section organization (grouping, hierarchy)
- Reference efficiency (cross-references, links)
- Progressive disclosure (layered detail)

## Execution Process

### Phase 1: Token Waste Detection

```bash
# Analyze prompt for redundancy
npx claude-flow@alpha hooks pre-task --description "Analyzing prompt for token waste"

# Store original metrics
npx claude-flow@alpha memory store --key "optimization/original-tokens" --value "{
  \"total_tokens\": <count>,
  \"redundancy_score\": <0-100>,
  \"verbosity_score\": <0-100>
}"
```

**Analysis Script:**
```javascript
// Embedded token analysis
function analyzeTokenWaste(promptText) {
  const metrics = {
    totalWords: promptText.split(/\s+/).length,
    totalChars: promptText.length,
    redundancyScore: 0,
    verbosityScore: 0,
    issues: []
  };

  // Detect phrase repetition
  const phrases = extractPhrases(promptText, 3); // 3-word phrases
  const phraseCounts = countOccurrences(phrases);
  const repeated = Object.entries(phraseCounts).filter(([_, count]) => count > 2);

  if (repeated.length > 0) {
    metrics.redundancyScore += repeated.length * 10;
    metrics.issues.push({
      type: "redundancy",
      severity: "medium",
      count: repeated.length,
      examples: repeated.slice(0, 3).map(([phrase]) => phrase)
    });
  }

  // Measure verbosity
  const avgWordLength = promptText.split(/\s+/)
    .reduce((sum, word) => sum + word.length, 0) / metrics.totalWords;

  if (avgWordLength > 6) {
    metrics.verbosityScore += 20;
    metrics.issues.push({
      type: "verbosity",
      severity: "low",
      avgWordLength: avgWordLength.toFixed(2),
      suggestion: "Consider shorter, clearer words"
    });
  }

  // Detect filler words
  const fillerWords = ["very", "really", "just", "actually", "basically", "simply"];
  const fillerCount = fillerWords.reduce((count, filler) => {
    const regex = new RegExp(`\\b${filler}\\b`, 'gi');
    return count + (promptText.match(regex) || []).length;
  }, 0);

  if (fillerCount > 5) {
    metrics.redundancyScore += fillerCount * 2;
    metrics.issues.push({
      type: "filler-words",
      severity: "low",
      count: fillerCount,
      suggestion: "Remove unnecessary filler words"
    });
  }

  return metrics;
}

function extractPhrases(text, wordCount) {
  const words = text.toLowerCase().split(/\s+/);
  const phrases = [];
  for (let i = 0; i <= words.length - wordCount; i++) {
    phrases.push(words.slice(i, i + wordCount).join(' '));
  }
  return phrases;
}

function countOccurrences(items) {
  return items.reduce((counts, item) => {
    counts[item] = (counts[item] || 0) + 1;
    return counts;
  }, {});
}
```

### Phase 2: Anti-Pattern Detection

**Common Anti-Patterns:**

1. **Vague Instructions**
   - ❌ "Make it better"
   - ✅ "Reduce token count by 20% while maintaining clarity"

2. **Ambiguous Terminology**
   - ❌ "Handle errors appropriately"
   - ✅ "Catch exceptions, log to memory, return user-friendly message"

3. **Conflicting Requirements**
   - ❌ "Be concise but provide detailed explanations"
   - ✅ "Provide concise summaries with optional detail links"

4. **Missing Context**
   - ❌ "Use the standard format"
   - ✅ "Use JSON format: {type, severity, description}"

5. **Over-Specification**
   - ❌ "Always use exactly 4 spaces, never tabs, indent 2 levels..."
   - ✅ "Follow project .editorconfig settings"

**Detection Script:**
```javascript
function detectAntiPatterns(promptText) {
  const patterns = [];

  // Vague instruction markers
  const vagueMarkers = ["better", "good", "appropriate", "proper", "suitable"];
  vagueMarkers.forEach(marker => {
    if (new RegExp(`\\b${marker}\\b`, 'i').test(promptText)) {
      patterns.push({
        type: "vague-instruction",
        marker: marker,
        severity: "high",
        suggestion: "Replace with specific, measurable criteria"
      });
    }
  });

  // Missing definitions
  const technicalTerms = promptText.match(/\b[A-Z][A-Za-z]*(?:[A-Z][a-z]*)+\b/g) || [];
  const definedTerms = (promptText.match(/\*\*[^*]+\*\*:/g) || []).length;

  if (technicalTerms.length > 5 && definedTerms < technicalTerms.length * 0.3) {
    patterns.push({
      type: "undefined-jargon",
      severity: "medium",
      technicalTermCount: technicalTerms.length,
      definedCount: definedTerms,
      suggestion: "Add definitions for technical terms"
    });
  }

  // Conflicting modal verbs
  const mustStatements = (promptText.match(/\b(must|required|mandatory)\b/gi) || []).length;
  const shouldStatements = (promptText.match(/\b(should|recommended|optional)\b/gi) || []).length;

  if (mustStatements > 10 && shouldStatements > 10) {
    patterns.push({
      type: "requirement-confusion",
      severity: "medium",
      mustCount: mustStatements,
      shouldCount: shouldStatements,
      suggestion: "Separate MUST vs SHOULD requirements clearly"
    });
  }

  return patterns;
}
```

### Phase 3: Trigger Analysis

```javascript
function analyzeTriggers(triggerText) {
  const issues = [];

  // Check clarity
  if (!triggerText.includes("when") && !triggerText.includes("if")) {
    issues.push({
      type: "unclear-condition",
      severity: "high",
      suggestion: "Use explicit 'when' or 'if' conditions"
    });
  }

  // Check specificity
  const vagueTerms = ["thing", "stuff", "something", "anything"];
  vagueTerms.forEach(term => {
    if (new RegExp(`\\b${term}\\b`, 'i').test(triggerText)) {
      issues.push({
        type: "vague-trigger",
        term: term,
        severity: "high",
        suggestion: "Replace with specific entity or action"
      });
    }
  });

  // Check scope
  if (triggerText.split(/\s+/).length < 5) {
    issues.push({
      type: "too-narrow",
      severity: "medium",
      wordCount: triggerText.split(/\s+/).length,
      suggestion: "Consider broader applicability"
    });
  }

  return issues;
}
```

### Phase 4: Optimization Recommendations

**Code Analyzer Agent Task:**
```bash
# Spawn analyzer agent
# Agent instructions:
# 1. Analyze prompt structure and flow
# 2. Identify optimization opportunities
# 3. Generate before/after comparisons
# 4. Calculate token savings
# 5. Store recommendations in memory

npx claude-flow@alpha memory store --key "optimization/recommendations" --value "{
  \"structural\": [...],
  \"content\": [...],
  \"examples\": [...],
  \"estimated_savings\": \"X tokens (Y%)\"
}"
```

### Phase 5: Before/After Comparison

**Optimization Report Format:**

```markdown
## Prompt Optimization Report

### Original Metrics
- Total tokens: <count>
- Redundancy score: <0-100>
- Verbosity score: <0-100>
- Anti-patterns found: <count>

### Issues Detected

#### High Severity
1. [Type] <description>
   - Location: <section>
   - Impact: <token/clarity impact>
   - Fix: <recommendation>

#### Medium Severity
...

#### Low Severity
...

### Recommended Changes

#### Structural
- [ ] Reorganize sections for logical flow
- [ ] Consolidate redundant examples
- [ ] Extract repetitive content to references

#### Content
- [ ] Replace vague terms with specific criteria
- [ ] Add missing definitions
- [ ] Remove filler words (identified: <count>)

#### Examples
- [ ] Reduce example count from <old> to <new>
- [ ] Consolidate similar examples
- [ ] Add missing edge cases

### Estimated Improvements
- Token reduction: <count> tokens (<percentage>%)
- Clarity score: +<points>
- Maintainability: +<points>

### Before/After Comparison

**Before (excerpt):**
```
<original problematic section>
```

**After (optimized):**
```
<optimized version>
```

**Savings:** <tokens> tokens, <improvement description>
```

## Concrete Example: Real Analysis

### Input Prompt (Fragment)
```markdown
You are a code reviewer. Your job is to review code and make sure it's good.
You should look at the code and find problems. When you find problems, you
should tell the user about them. Make sure to check for bugs and also check
for style issues. You should be thorough and careful. Don't miss anything
important. Always be professional and constructive in your feedback. Try to
help the developer improve. Make suggestions that are actually helpful and
not just critical. Be nice but also be honest. Make sure your reviews are
really good and comprehensive.
```

### Analysis Output

**Token Waste Analysis:**
```json
{
  "totalWords": 98,
  "totalTokens": 124,
  "redundancyScore": 45,
  "verbosityScore": 30,
  "issues": [
    {
      "type": "redundancy",
      "severity": "high",
      "examples": [
        "make sure" (3 occurrences),
        "you should" (4 occurrences),
        "be [adjective]" (3 occurrences)
      ]
    },
    {
      "type": "vague-instructions",
      "severity": "high",
      "examples": [
        "good", "thorough", "careful", "helpful",
        "important", "professional", "constructive"
      ]
    },
    {
      "type": "filler-words",
      "severity": "medium",
      "count": 8,
      "examples": ["really", "actually", "just"]
    }
  ]
}
```

**Optimization Recommendations:**
1. Remove repeated "you should" → use imperative mood
2. Replace vague terms with specific criteria
3. Consolidate feedback guidelines into structured list
4. Remove redundant emphasis phrases

### Optimized Output
```markdown
You are a code reviewer analyzing pull requests for quality and correctness.

Review Process:
1. Scan for logic errors, null checks, edge cases
2. Verify style compliance (linting, formatting)
3. Assess test coverage (>80% target)
4. Check documentation completeness

Feedback Format:
- Issue: [category] - [specific finding]
- Impact: [low/medium/high]
- Fix: [concrete suggestion with code example]

Tone: Professional, constructive, solution-focused
```

**Results:**
- Original: 124 tokens
- Optimized: 67 tokens
- Savings: 57 tokens (46% reduction)
- Clarity: Improved (specific criteria vs. vague terms)
- Actionability: Improved (structured process vs. general instructions)

## Integration with Development Workflow

### Pre-Publish Checklist
```bash
# 1. Analyze new skill
npx claude-flow@alpha hooks pre-task --description "Optimizing new skill prompt"

# 2. Run analysis (spawn analyzer agent)
# Agent performs full analysis as documented above

# 3. Review recommendations
npx claude-flow@alpha memory retrieve --key "optimization/recommendations"

# 4. Apply fixes
# Make recommended changes to skill

# 5. Re-analyze and verify improvements
# Re-run analysis, compare metrics

# 6. Store final metrics
npx claude-flow@alpha hooks post-task --task-id "skill-optimization"
```

## Success Metrics

- Token reduction: 20-50% typical
- Clarity score: +30-50 points
- Trigger precision: 90%+ accuracy
- Anti-pattern elimination: 100% high-severity
- Maintainability: Easier to update and extend

## Related Skills

- `when-analyzing-skill-gaps-use-skill-gap-analyzer` - Analyze overall library
- `when-managing-token-budget-use-token-budget-advisor` - Budget planning
- `prompt-architect` - Advanced prompt engineering

## Notes

- Run before publishing new skills
- Re-analyze periodically (monthly maintenance)
- Track improvements over time
- Share optimization patterns across team
- Update analysis scripts as new anti-patterns emerge
