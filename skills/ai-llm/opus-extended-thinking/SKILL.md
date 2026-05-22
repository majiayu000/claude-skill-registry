---
name: opus-extended-thinking
description: Leverage Claude Opus 4.5's extended thinking capabilities for deep reasoning, complex analysis, and multi-step synthesis. Use when problems require thorough deliberation before response.
version: 1.0.0
last_updated: 2025-12-19
external_version: "Claude Opus 4.5 (November 2025)"
changelog: |
  - 1.0.0: Initial skill for Opus 4.5 extended thinking patterns
---

# Claude Opus 4.5 Extended Thinking

This skill guides optimal use of Claude Opus 4.5's extended thinking capabilities - the model's ability to reason deeply before responding, leading to more thoughtful, accurate, and nuanced outputs.

---

## Understanding Extended Thinking

### What It Is
Extended thinking allows Opus 4.5 to:
- Deliberate longer before producing output
- Consider multiple perspectives and approaches
- Self-critique and refine reasoning
- Handle complex multi-step problems
- Produce more thoughtful, less reactive responses

### When It Activates
Extended thinking engages automatically when:
- Problems require multi-step reasoning
- Questions have nuance or ambiguity
- Tasks require weighing tradeoffs
- Complex analysis or synthesis is needed
- Creative work benefits from deliberation

---

## Prompt Patterns for Deep Thinking

### Pattern 1: Explicit Deliberation Request
```
Before answering, take time to:
1. Consider the problem from multiple angles
2. Identify potential pitfalls or edge cases
3. Weigh different approaches
4. Then provide your best response

Question: [Your complex question]
```

### Pattern 2: Multi-Perspective Analysis
```
I need a thorough analysis of [topic].

Please consider:
- The technical perspective
- The business/practical perspective
- The user/human perspective
- Potential risks and downsides
- Long-term implications

Take your time to reason through each before synthesizing.
```

### Pattern 3: Step-by-Step Reasoning
```
Walk me through your reasoning on this problem step by step.
Don't jump to conclusions - show your work.

Problem: [Complex problem]

For each step, explain:
- What you're considering
- Why you're making that choice
- What alternatives you rejected and why
```

### Pattern 4: Devil's Advocate
```
I'm planning to [action/decision].

Before you help me execute this:
1. Steelman the opposing view - what's the best argument against?
2. What am I potentially missing or underweighting?
3. What would make this fail?
4. Only then, if it still seems right, help me proceed.
```

### Pattern 5: Synthesis Request
```
I have [number] different sources/perspectives on [topic]:
[List them]

Please synthesize these into a coherent understanding that:
- Identifies where they agree
- Explains where they conflict and why
- Weighs the evidence/arguments
- Provides your reasoned conclusion
```

---

## Task Types That Benefit Most

### 1. Strategic Planning
```
Prompt pattern:
"Help me think through [strategic decision].
Consider: current state, desired outcome, constraints,
multiple paths, risks of each, second-order effects.
Don't rush to a recommendation - reason through thoroughly first."
```

### 2. Code Architecture Decisions
```
Prompt pattern:
"I'm deciding between [Option A] and [Option B] for [system].
Before recommending, analyze:
- Scalability implications
- Maintenance burden
- Team capability fit
- Migration complexity
- What we might regret in 2 years"
```

### 3. Creative Development
```
Prompt pattern:
"I want to create [creative work] about [theme].
Before writing, explore:
- Different narrative approaches
- Tonal variations
- Structural options
- What makes this theme resonate
Then develop the direction that feels most promising."
```

### 4. Problem Diagnosis
```
Prompt pattern:
"[System/situation] is exhibiting [problem].
Don't jump to the obvious cause.
Consider:
- What are all possible causes?
- What evidence supports/refutes each?
- What's the most likely root cause?
- What would I need to verify to be sure?"
```

### 5. Research Synthesis
```
Prompt pattern:
"Help me understand [complex topic].
I need you to:
- Break down the key concepts
- Explain how they relate
- Identify what's well-established vs debated
- Note what's commonly misunderstood
- Synthesize into a coherent mental model"
```

---

## Anti-Patterns to Avoid

### ❌ Rushing to Action
```
Bad: "Write me a function that does X"
Better: "I need a function that does X. Before coding,
        let's consider: edge cases, error handling,
        interface design, testing approach."
```

### ❌ Accepting First Answer
```
Bad: "What's the best database for my app?"
Better: "What database should I use for [specific requirements]?
        Consider multiple options, tradeoffs between them,
        and what factors should weight most heavily."
```

### ❌ Binary Thinking
```
Bad: "Should I do A or B?"
Better: "I'm choosing between A and B, but I'm open to
        alternatives I haven't considered. What's the
        best path forward given [context]?"
```

### ❌ Ignoring Uncertainty
```
Bad: "Tell me the answer to [complex question]"
Better: "Help me understand [complex question].
        Be explicit about what's certain vs uncertain,
        and what evidence supports different views."
```

---

## Extended Thinking Triggers

Use these phrases to encourage deeper deliberation:

**Analytical Triggers:**
- "Think through this carefully..."
- "Consider all angles before responding..."
- "What are the non-obvious implications?"
- "What am I likely missing?"
- "Reason through step by step..."

**Critical Triggers:**
- "What could go wrong with this approach?"
- "Steelman the opposing view..."
- "What's the strongest argument against?"
- "What assumptions am I making?"
- "Where might this reasoning break down?"

**Synthesis Triggers:**
- "How do these pieces fit together?"
- "What's the underlying pattern?"
- "Synthesize into a coherent view..."
- "What's the essence of this?"
- "How would you explain this to an expert?"

---

## Output Quality Indicators

Signs extended thinking is working well:
- Response acknowledges complexity and tradeoffs
- Multiple perspectives are genuinely considered
- Reasoning is visible, not just conclusions
- Uncertainty is explicitly addressed
- Edge cases and risks are surfaced proactively
- Recommendations are nuanced, not absolute

Signs it might need more prompting:
- Quick, surface-level response
- Only one perspective considered
- Confident without showing reasoning
- Missing obvious complexities
- Generic advice without context fit

---

## Combining with Other Patterns

### Extended Thinking + Agentic Execution
```
"First, think through the best approach to [task].
Consider alternatives and tradeoffs.
Once you have a clear plan, execute it autonomously,
but note any decision points where you chose between options."
```

### Extended Thinking + Iterative Refinement
```
"Draft an initial approach to [problem].
Then critique your own draft - what could be better?
Revise based on your critique.
Show me both the final version and key improvements you made."
```

### Extended Thinking + User Collaboration
```
"Analyze [situation] and identify the key decision points.
For each decision, explain the tradeoffs.
Before proceeding, I'll tell you my priorities,
then you can recommend the path that fits best."
```

---

## When NOT to Use Extended Thinking

Some tasks benefit from quick, direct responses:
- Simple factual questions
- Straightforward code snippets
- Clear instructions with no ambiguity
- Tasks where speed matters more than depth
- Follow-up execution after thinking is done

For these, don't add complexity. Just ask directly.

---

## Model-Specific Notes (Opus 4.5)

Opus 4.5 specifically excels at:
- **Sustained reasoning chains** - Can maintain coherence over long analytical sequences
- **Self-correction** - Will catch and correct its own errors when given space
- **Nuance handling** - Better at "it depends" answers with clear conditions
- **Multi-factor synthesis** - Can hold many variables in consideration simultaneously
- **Creative-analytical blend** - Can reason rigorously about creative work

---

## Integration with FrankX System

Use extended thinking for:
- **Starlight Council decisions** - Strategic synthesis across domains
- **Architecture planning** - System design for Arcanea, FrankX projects
- **Content strategy** - Weighing positioning, audience, platform fit
- **Creative development** - Book outlines, course structures, music direction
- **Technical decisions** - Framework choices, MCP design, agent orchestration

---

*Extended thinking is about quality of cognition, not length of output. The best responses come from genuine deliberation - use these patterns to unlock that capability.*
