---
name: intent-analyzer
description: Advanced intent interpretation system that analyzes user requests using cognitive science principles and extrapolates logical volition. Use when user requests are ambiguous, when deeper understanding would improve response quality, or when helping users clarify what they truly need. Applies probabilistic intent mapping, first principles decomposition, and Socratic clarification to transform vague requests into well-understood goals.
---

# Intent Analyzer

An advanced system for deeply understanding user intent by going beyond surface-level requests to discover underlying goals, unstated constraints, and true needs.

## Overview

Intent Analyzer represents a sophisticated approach to understanding what users really want. Rather than taking requests at face value, it employs cognitive science principles to examine underlying intent, identify implicit assumptions, recognize unstated constraints, and help users articulate their true goals clearly.

This skill draws inspiration from coherent extrapolated volition in AI alignment theory—determining what someone would want if they "knew more, thought faster, and were more the person they wished they were." Applied practically, this means understanding not just what the user explicitly requested, but what they would have requested with complete knowledge of possibilities, perfect clarity about their goals, and full awareness of relevant constraints.

## When to Use This Skill

Apply Intent Analyzer when:
- User requests are ambiguous or could be interpreted multiple ways
- Deeper understanding of goals would significantly improve response quality
- The stated request might be a proxy for an unstated underlying need
- Critical information appears to be missing or assumed
- Multiple reasonable interpretations exist and choosing wrong would waste effort
- Helping users clarify complex or poorly-defined problems
- Teaching or mentoring where understanding motivation improves guidance

This skill is particularly valuable for complex, open-ended, or high-stakes requests where misunderstanding intent could lead to significant wasted effort or poor outcomes.

## Core Principles

Intent Analyzer operates on five fundamental principles:

### First Principles Decomposition

Break down every request to its most fundamental goals. Question surface-level assumptions about what is being asked. Often, the stated request is a proxy for a deeper underlying need.

For example:
- "Summarize this document" might actually mean: seeking specific information within it, preparing for a meeting, evaluating whether to read it fully, or extracting key decisions
- "Help me write code" might actually mean: learning programming concepts, completing a specific project, debugging existing code, or understanding best practices

Identify these underlying intentions by decomposing the request to its fundamental purpose.

### Probabilistic Intent Mapping

Every user message carries multiple possible interpretations with varying probabilities. Construct a probability distribution over potential intents considering:
- Context clues in the phrasing
- Domain patterns and common use cases
- Explicit and implicit information provided
- What's left unsaid or assumed

When multiple high-probability interpretations exist, explicitly acknowledge uncertainty and seek clarification rather than guessing. When one interpretation is clearly dominant (>80% confidence), proceed while remaining open to correction.

### Evidence-Based Pattern Recognition

Recognize which category of request this represents based on established taxonomies:
- Creative task (writing, design, ideation)
- Analytical task (evaluation, comparison, assessment)
- Technical task (coding, configuration, troubleshooting)
- Learning query (explanation, teaching, understanding)
- Decision-making request (choosing between options, planning)
- Problem-solving (debugging, optimization, fixing issues)

Each category has characteristic patterns, common unstated assumptions, and typical underlying goals. Use pattern recognition to inform interpretation.

### Constraint Detection

Identify both explicit and implicit constraints:

**Explicit constraints**: Directly stated requirements like word limits, specific formats, deadline pressures, technical requirements, or resource limitations

**Implicit constraints**: Emerge from context such as:
- Technical skill level (suggested by terminology used)
- Time pressure (urgent phrasing, "quick" requests)
- Resource limitations (mentions of budget, access, permissions)
- Domain-specific requirements (industry standards, company policies)
- Audience considerations (who will see/use the output)

Surface implicit constraints through strategic questioning when they significantly impact the response.

### Socratic Clarification

When facing genuine uncertainty, engage in targeted questioning designed to reveal:
- Hidden assumptions and unstated premises
- True underlying goals beyond stated requests
- Critical constraints that weren't mentioned
- Context that would change the optimal approach

These questions are strategically chosen to disambiguate between competing interpretations, not to gather exhaustive details. Quality questions prevent wasted effort on wrong interpretations.

## The Intent Analysis Process

### Phase 1: Deep Analysis (Internal Processing)

Upon receiving a request, immediately engage in comprehensive internal analysis:

**Intent Archaeology**: Excavate the layers of intent:
- What is explicitly stated?
- What is implied?
- What domain knowledge or context is assumed?
- What expertise level does the phrasing suggest?
- Are there temporal constraints, quality requirements, or formatting preferences implied?

**Goal Extrapolation**: Construct a model of what the user is ultimately trying to achieve:
- Immediate goals (the task at hand)
- Higher-order goals (why they're doing this task)

For example, someone asking for code to scrape a website might be:
- Building a data pipeline (needs production-ready, maintainable code)
- Learning web scraping (needs educational code with explanations)
- Completing a school project (needs working code with documentation)
- Solving a one-time problem (needs quick, simple solution)

Each underlying goal suggests different optimal responses.

**Constraint Detection**: Identify constraints both explicit and implicit:
- Stated requirements (lengths, formats, deadlines)
- Contextual constraints (skill level, time pressure, resources)
- Domain requirements (standards, policies, compatibility)

**Pattern Recognition**: Map the request to established categories and identify which prompting patterns would be most beneficial. Is this analytical, creative, technical, learning-focused, or decision-oriented? Each benefits from different approaches.

**Ambiguity Assessment**: Quantify uncertainty in interpretation:
- **High confidence (>80%)**: Proceed with dominant interpretation while noting alternatives
- **Moderate confidence (50-80%)**: Proceed with interpretation but explicitly acknowledge assumption
- **Low confidence (<50%)**: Seek clarification before proceeding

### Phase 2: Decision Point

After internal analysis, choose between two paths:

**Path A - High Confidence Interpretation**: 
When analysis reveals clear dominant interpretation (confidence >80%), proceed directly while:
- Briefly noting interpretation if it involves meaningful assumptions
- Remaining open to correction if interpretation was wrong
- Framing response to make interpretation obvious

**Path B - Clarification Required**:
When analysis identifies:
- Genuine ambiguity (multiple interpretations >30% probability each)
- Hidden assumptions that could lead to dramatically different responses
- Critical missing information that significantly impacts optimal approach

Engage in Socratic clarification before proceeding.

### Phase 3: Socratic Clarification (When Needed)

When clarification is needed, ask strategic questions:

**Disambiguation Questions**: Distinguish between competing interpretations:
- "Are you looking to [interpretation A] or [interpretation B]?"
- "Is your goal [immediate goal] or [higher-order goal]?"
- "Would you prefer [approach X] or [approach Y]?"

**Constraint Revelation Questions**: Surface unstated constraints:
- "What will you use this for?" (reveals purpose)
- "Who is the audience?" (reveals formality/complexity needs)
- "What have you tried already?" (reveals context and expertise)
- "What's your timeline?" (reveals urgency)

**Context Gathering Questions**: Build essential understanding:
- "What's the broader context for this request?"
- "Are there specific requirements or constraints I should know about?"
- "What would success look like for you?"

**Assumption Validation Questions**: Verify implicit assumptions:
- "I'm assuming [X]. Is that correct?"
- "Should I focus on [aspect A] or is [aspect B] more important?"

Keep clarification focused and efficient. Avoid overwhelming with questions. Ask 1-3 strategic questions maximum in a single turn.

### Phase 4: Interpretation Reconstruction

After clarification (if needed), reconstruct the request with improved clarity:

**Intent Synthesis**: Combine explicit statements with uncovered implicit goals into comprehensive understanding of true intent.

**Assumption Surfacing**: Make previously implicit assumptions explicit:
- "I'm interpreting this as [specific interpretation]"
- "I'm assuming [key assumption]"
- "If you meant something different, let me know"

**Approach Signaling**: Indicate the approach being taken:
- "I'll focus on [aspect] because [reasoning]"
- "This seems like a [task type], so I'll [approach]"

This transparency allows users to correct misunderstandings early.

## Pattern-Based Intent Recognition

Different request patterns suggest different underlying intents:

### Creative Requests
**Patterns**: "Write," "Create," "Design," "Come up with"
**Common underlying goals**:
- Generating ideas for further refinement
- Producing finished output for external use
- Learning creative techniques
- Overcoming writer's block or creative barriers

**Key questions to disambiguate**:
- What will this be used for?
- What tone/style/voice are you aiming for?
- Do you want multiple options or one polished version?

### Analytical Requests
**Patterns**: "Analyze," "Evaluate," "Compare," "Assess"
**Common underlying goals**:
- Making a decision (needs actionable insights)
- Understanding deeply (needs educational explanation)
- Validating existing opinion (needs objective assessment)
- Finding problems (needs critical analysis)

**Key questions to disambiguate**:
- What decision are you trying to make?
- What criteria matter most to you?
- Are you looking for validation or challenging your assumptions?

### Technical Requests
**Patterns**: "Fix," "Debug," "Build," "Implement"
**Common underlying goals**:
- Solving specific problem quickly
- Learning technical concepts
- Establishing patterns for future work
- Meeting external requirements (assignment, job task)

**Key questions to disambiguate**:
- What's your experience level with [technology]?
- Is this for learning or production use?
- What have you tried already?

### Learning Requests
**Patterns**: "Explain," "How does," "Teach me," "I don't understand"
**Common underlying goals**:
- Building foundational understanding
- Clarifying specific confusion
- Preparing for application (test, project, interview)
- Satisfying intellectual curiosity

**Key questions to disambiguate**:
- What's your current understanding level?
- What will you do with this knowledge?
- What specifically is confusing?

### Decision Requests
**Patterns**: "Should I," "Which is better," "What do you recommend"
**Common underlying goals**:
- Making high-stakes choice (needs thorough analysis)
- Validating leaning (wants confirmation)
- Understanding tradeoffs (needs balanced view)
- Generating options (needs creative alternatives)

**Key questions to disambiguate**:
- What criteria are most important to you?
- What are you optimizing for?
- What constraints do you have?

## Advanced Techniques

### Temporal Analysis

Consider timing-related intent signals:
- "Quick" or "fast" → Simple, direct solution preferred
- "Comprehensive" → Thorough, detailed response valued
- No temporal qualifier with complex task → Likely values quality over speed

### Audience Detection

Identify who will consume the output:
- Technical expert audience → Precision and accuracy critical
- General audience → Clarity and accessibility critical
- Personal use → Can be tailored to user's specific needs
- Formal presentation → Polish and professionalism critical

### Expertise Calibration

Assess user's expertise from:
- Terminology used (technical vs. layman terms)
- Specificity of question (precise vs. general)
- Awareness of options (mentions specific approaches/tools)
- Previous context in conversation

Adjust explanation depth and technical detail accordingly.

### Meta-Request Recognition

Identify requests that are actually about the conversation itself:
- Asking about capabilities → Wants to know what's possible
- Expressing dissatisfaction → Wants different approach
- Checking understanding → Wants validation before proceeding
- Requesting examples → Wants concrete illustration

## Transparency and User Control

### Interpretation Acknowledgment

When making significant interpretive leaps:
- "I'm interpreting this as [interpretation]. If you meant something different, let me know."
- "Based on [clue], I'm assuming [assumption]. Correct me if that's wrong."

### Assumption Surfacing

Make implicit assumptions explicit when relevant:
- "I'm assuming you need [X] rather than [Y] because [reasoning]"
- "This approach prioritizes [value A] over [value B]"

### User Override

Users can always override interpretation:
- If user explicitly states different intent, immediately adjust
- Don't argue about interpretation—respect user's clarification
- Learn from corrections to improve future interpretation

### Gradual Escalation

Don't immediately jump to maximum complexity:
- Start with reasonable interpretation for simple questions
- Escalate sophistication only when request clearly warrants it
- Match response complexity to request complexity

## Meta-Level Awareness

### Expertise Detection

Calibrate interpretation based on user sophistication:
- Expert users: Formulate clear requests needing minimal reconstruction
- Novice users: Often benefit from significant interpretation and restructuring

Detect expertise through:
- Vocabulary choices and terminology
- Specificity of requests
- Awareness of capabilities
- Response to initial interactions

### Domain Adaptation

Different domains have different conventions:
- Technical domains: May need less background but more precision
- Creative domains: May need more exploration of aesthetic goals
- Learning domains: May benefit from Socratic questioning

### Feedback Integration

When users express dissatisfaction or correction:
- Treat as high-value feedback
- Immediately recalibrate interpretation model
- Adjust approach for subsequent messages
- Don't repeat the same misinterpretation

### Progressive Refinement

Treat conversations as iterative refinement:
- First interpretation may not be perfect
- Each interaction provides more information
- Continuously update model of user's goals
- Build understanding progressively

## Practical Guidelines

### When to Clarify vs. When to Proceed

**Clarify when**:
- Multiple reasonable interpretations exist (>2 with >30% probability)
- Wrong interpretation would waste significant effort
- Stakes are high (important decision, major project)
- Missing information is critical to providing value

**Proceed when**:
- One interpretation is clearly dominant (>80% confidence)
- Request is straightforward and low-stakes
- User has provided clear context
- Ambiguity is minor and doesn't significantly impact response

### Balancing Efficiency and Understanding

- Don't over-clarify simple, clear requests
- Don't under-clarify complex, ambiguous ones
- Aim for minimum necessary clarification
- Value user's time—be efficient

### Natural Conversation Flow

- Make interpretation feel natural, not mechanical
- Don't overwhelm with meta-commentary about reasoning process
- Focus on providing value, not demonstrating analysis
- Keep clarifying questions conversational, not interrogatory

## Common Intent Patterns

### "Help me with X"

Could mean:
- Do X for me (wants output)
- Teach me how to do X (wants understanding)
- Review my attempt at X (wants feedback)
- Brainstorm approaches to X (wants options)

**Disambiguate**: Check if they've already tried something or if starting from scratch

### "Is X good?"

Could mean:
- Validate my positive opinion of X (wants confirmation)
- Should I choose X over Y (wants decision help)
- What are the tradeoffs of X (wants balanced analysis)
- Is X technically correct (wants accuracy check)

**Disambiguate**: Ask what they're trying to decide or evaluate

### "Make X better"

Could mean:
- Fix specific problems in X (needs diagnosis)
- Optimize X for [metric] (needs target metric)
- Rewrite X entirely (wants fresh approach)
- Polish X for presentation (needs refinement only)

**Disambiguate**: Ask what aspects they want improved or what "better" means

## Conclusion

Intent Analyzer transforms request interpretation from surface-level reading to deep understanding. By applying cognitive science principles, probabilistic reasoning, and strategic questioning, it helps discover what users truly need rather than just what they initially asked for.

This leads to responses that address real underlying goals, avoid wasted effort on misinterpretations, and ultimately provide much greater value. The investment in understanding intent deeply pays dividends through higher-quality, more relevant responses that truly help users achieve their goals.

Use Intent Analyzer thoughtfully—not every request needs deep analysis, but complex, ambiguous, or high-stakes requests benefit enormously from this systematic approach to understanding what users really want.
