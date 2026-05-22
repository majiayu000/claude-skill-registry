---
description: Evaluate and strengthen Northcote Curio brand style briefs by identifying
  vague language, testing applicability across component types, and suggesting specific
  examples that clarify edge cases and decision frameworks.
name: brand-brief-optimizer
---

# Brand Brief Optimizer Skill

## Overview

Transforms brand briefs from aspirational documents into **living standards** that reliably guide design decisions. Tests brief language against real-world component decisions to reveal gaps and ambiguities.

A powerful brief answers the questions your team will actually ask. This skill helps you write those answers clearly.

## When to Use This Skill

Use this skill when you need to:

- **Stress-test a draft brief** for clarity and coherence
- **Identify vague language** that won't guide team decisions
- **Test applicability** across different component types
- **Find edge cases** the brief doesn't address
- **Clarify assumptions** embedded in brief language
- **Validate brief coherence** (do principles work together or conflict?)
- **Strengthen brief language** through iterative refinement
- **Create brief coherence score** (how likely is this to guide decisions?)

## How It Works

The optimizer analyzes your brief across five dimensions:

### 1. Clarity Assessment
Are specific sections clear enough to guide decisions, or do they hedge?

**Weak**: "Use distinctive fonts that feel crafted"  
**Strong**: "Display typography (Lora/Fraunces) should evoke hand-lettered precision. Opt for Lora when scholarly rigor matters, Fraunces for warmth and personality."

### 2. Coherence Check
Do principles work together, or do they contradict?

Example: If brief says "maximize botanical motifs" but also "information clarity first," the contradiction needs resolving.

### 3. Applicability Testing
Can someone actually follow this brief across different component types?

The optimizer tests brief language against:
- Information-heavy components (job listings, dashboards)
- Emotional landing pages (career inspiration, pathway)
- Forms & input contexts (applications, data entry)
- Navigation & structure (side panels, headers)

### 4. Edge Case Identification
What questions will your team ask that the brief doesn't answer?

Examples:
- "Can I use a purple accent?"
- "How do I handle dark mode while preserving warmth?"
- "What's the maximum botanical motif before it feels decorative?"

### 5. Coherence Scoring
Quantifies brief quality across all dimensions. Not to compare against others, but to track your own improvement as you refine.

Scores 0-100:
- 80-100: Ready to deploy (team can use with confidence)
- 60-79: Close (needs targeted refinement)
- 40-59: Foundational (significant work needed)
- Below 40: Concept stage (too vague to guide decisions)

## Usage Examples

### Example 1: Stress-Test Draft Brief
"Evaluate this draft Northcote brief for clarity and coherence"

Claude will:
1. Analyze each section for vagueness
2. Test against example component decisions
3. Identify edge cases not addressed
4. Find contradictions or confusing language
5. Score overall coherence (0-100)
6. Provide targeted recommendations

### Example 2: Test Applicability
"Can this brief guide typography decisions across info-heavy dashboards, emotional landing pages, and form contexts?"

Claude will:
1. Take brief's typography guidance
2. Imagine decisions needed in each context
3. Test whether brief provides clear answer
4. Identify where guidance breaks down
5. Suggest clarifications needed

### Example 3: Edge Case Generation
"What questions will my team ask about this brief that it doesn't clearly answer?"

Claude will:
1. Identify assumed knowledge
2. Spot vague pronouncements
3. Generate likely edge cases
4. Suggest how brief could preemptively address them
5. Produce list of clarifications needed

### Example 4: Iterative Refinement
"I've incorporated your feedback. Here's the revised section. Is it clearer?"

Claude will:
1. Compare old vs. new language
2. Assess if revision added specificity
3. Identify remaining vagueness
4. Suggest further refinement
5. Track clarity improvement

## The Optimizer Report Format

```json
{
  "brief_evaluation": {
    "brief_name": "Northcote Curio Brand Brief",
    "evaluation_date": "2026-01-28",
    "overall_coherence_score": 0-100,
    
    "dimension_scores": {
      "clarity": 0-100,
      "coherence": 0-100,
      "applicability": 0-100,
      "edge_case_coverage": 0-100,
      "distinctiveness": 0-100
    },
    
    "clarity_findings": {
      "clear_sections": ["...", "..."],
      "vague_sections": ["...", "..."],
      "hedge_language": ["...", "..."],
      "recommendations": ["Make X more specific", "..."]
    },
    
    "coherence_findings": {
      "working_together": ["Typography + color establish dialogue", "..."],
      "potential_conflicts": ["Botanical maximalism vs. clarity priority", "..."],
      "resolution_suggestions": ["...", "..."]
    },
    
    "applicability_testing": {
      "information_heavy_context": "Brief guidance works for dashboards",
      "emotional_context": "Brief guidance works for landing pages",
      "form_context": "Brief guidance struggles with form inputs",
      "navigation_context": "Brief guidance works for headers/panels",
      "summary": "Applicable in 3/4 tested contexts"
    },
    
    "uncovered_edge_cases": [
      "How to handle dark mode while preserving warmth?",
      "Maximum botanical motif before decorative?",
      "Purple accent usage?",
      "Text over botanical elements clarity?"
    ],
    
    "overall_assessment": "Brief is close to deployment quality but needs targeted refinement in three areas..."
  }
}
```

## Key Capabilities

### Clarity Analysis
Identifies:
- Specific vs. vague language
- Rules vs. values (which guides better decisions?)
- Assumed knowledge (what does team need to know?)
- Ambiguities in terminology

### Coherence Validation
Checks:
- Do principles work together?
- Are there contradictions?
- Is hierarchy of values clear?
- Do examples support stated principles?

### Real-World Testing
Simulates decisions in:
- Information-dense contexts (clarity needed)
- Emotional communication (impact needed)
- Structural components (consistency needed)
- Forms & interaction (precision needed)

### Gap Identification
Reveals:
- Edge cases not addressed
- Assumed knowledge not stated
- Contradictions needing resolution
- Future maturation areas

## Workflow: Iterative Brief Refinement

1. **Write draft brief** (initial thinking)
2. **Run optimizer** (identify gaps)
3. **Revise based on feedback** (add specificity)
4. **Re-run optimizer** (verify improvements)
5. **Repeat until score stabilizes** at 80+
6. **Deploy brief** (team can use with confidence)
7. **Monitor real-world application** (refine based on usage)

This produces briefs that actually guide work, not just aspire to.

## Integration with Other Skills

### With Frontend-Design
Compare brief aesthetic philosophy against frontend-design thinking—do they align?

### With Northcote-Typography-Strategy
Test whether brief's typography guidance is specific and defensible.

### With Northcote-Visual-Audit
Brief clarity measured by whether audit results are consistent (clear brief = consistent audits).

### With Compliance-Dashboard
Dashboard tracks whether brief is actually guiding component development (visible through compliance patterns).

## Limitations

This skill:

✅ Identifies vague and unclear language  
✅ Tests brief against realistic scenarios  
✅ Generates edge cases you haven't considered  
✅ Provides coherence scoring for improvement tracking  

❌ Cannot write the brief for you (refining language is your work)  
❌ Cannot guarantee every team member interprets the same way  
❌ Doesn't replace human review and discussion  
❌ Coherence score is relative, not absolute

## Success Criteria

A brief is ready for deployment when it:

1. **Scores 80+ on coherence** (clear enough to guide decisions)
2. **Answers likely edge cases** (team knows what to do when uncertain)
3. **Works across component types** (applicable to your full product)
4. **Speaks to values, not just rules** (team internalizes, doesn't just follow)
5. **Distinguishes your brand** (brief reveals what makes you Northcote)

## Key Principle

The difference between a brief that sits on a shelf and one that becomes culture is the difference between **rules** and **values**.

Rules are obeyed. Values are internalized.

A brief optimized for clarity and coherence shifts your team from "what rules do I follow?" to "what values do I embody?"

That shift changes everything.

---

*A great brief doesn't just guide design decisions—it shifts how your team thinks about design.*
