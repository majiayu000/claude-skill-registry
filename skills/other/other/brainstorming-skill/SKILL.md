---
name: brainstorming-skill
description: This skill should be used when users need to generate ideas, explore creative solutions, or systematically brainstorm approaches to problems. Use when users request help with ideation, content planning, product features, marketing campaigns, strategic planning, creative writing, or any task requiring structured idea generation. The skill provides 30+ research-validated prompt patterns across 14 categories with exact templates, success metrics, and domain-specific applications.
---

# Brainstorming Skill

## Overview

This skill provides comprehensive, research-validated brainstorming patterns and prompt templates to help generate high-quality ideas across any domain. It contains 30+ documented patterns from 14 primary sources, organized into systematic categories with exact prompt wording, output format specifications, and proven success metrics.

## When to Use This Skill

Activate this skill when users need:

<trigger_scenarios>

- Idea generation for products, features, or content
- Creative problem-solving approaches
- Marketing campaign concepts
- Strategic planning and decision-making
- Content creation (blog posts, social media, presentations)
- Product feature ideation
- Business strategy development
- Creative writing (plot development, character creation)
- QA test case brainstorming
- Innovation workshops or facilitation
- Breaking through creative blocks
- Systematic exploration of solution spaces </trigger_scenarios>

## Pattern Categories

The skill organizes brainstorming patterns into 14 systematic categories. Each pattern includes exact prompt templates, output format specifications, concrete examples, and reported success metrics.

### Core Pattern Categories

<category_index>

1. Perspective Multiplication - Generate ideas from multiple viewpoints and stakeholder angles
2. Constraint Variation - Explore idea space through artificial constraints
3. Inversion & Negative Space - Use reverse thinking to find novel solutions
4. Analogical Transfer - Apply patterns from different domains
5. Systematic Feature Decomposition - SCAMPER and attribute-based ideation
6. Scenario Exploration - Future-based and "what if" thinking
7. Constraint-Based Structured Ideation - Build within hard constraints
8. Chain-of-Thought Reasoning - Multi-step refinement processes
9. Combination & Morphological Exploration - Force novel feature combinations
10. Assumption Challenge - Question premises and invert assumptions
11. Fill-in-the-Blank Templates - Structured completion formats
12. Competitive Positioning - Differentiation matrix approaches
13. Extreme Scaling - 10x thinking and exponential scenarios
14. Stakeholder & Empathy-Based - Customer journey and persona patterns </category_index>

## Quick Pattern Selection

<selection_guide> For rapid quantity (8-15 ideas): Use Perspective Multiplication patterns For quality/depth: Use Multi-stage refinement with constraint variation For breakthrough innovation: Combine Inversion + Extreme Scaling For practical implementation: Use Constraint-Based patterns For market differentiation: Use Competitive Positioning patterns For customer-centric features: Use Stakeholder & Empathy patterns </selection_guide>

## Key Research Findings

<research_insights>

- Constraint-based patterns generate 20-30% MORE ideas than open-ended prompts
- Specifying output format (table/numbered list) improves quality without reducing quantity
- Multiple perspective iteration (3-5 viewpoints) consistently outperforms single-perspective
- Requiring reasoning visibility ("explain why") increases implementability by 40%
- Successful patterns share: role definition, constraint specification, output format, reasoning requirements </research_insights>

## Pattern Documentation

Complete pattern documentation is organized in reference files:

### Main Pattern Categories

[Pattern Categories and Documentation](./references/pattern-categories-and-documentation.md) - All 14 categories with 30+ patterns, exact templates, examples, and success metrics (1,303 lines)

### Domain Applications

[Domain-Specific Applications](./references/domain-specific-applications-and-variations.md) - Marketing, Product Development, QA Testing, Business Strategy, Creative Writing patterns

### Supporting Guides

[Pattern Selection Guide](./references/pattern-selection-guide.md) - Decision framework for choosing appropriate patterns [Synthesis: What Makes Patterns Work](./references/synthesis-what-makes-these-patterns-work.md) - Common structural elements and effectiveness analysis [Comprehensive Prompt Library](./references/comprehensive-prompt-library-ready-to-use-templates.md) - Ready-to-use templates organized by use case [Executive Summary](./references/executive-summary.md) - High-level overview and key findings

### Bibliographic Research

Research from authoritative sources with verified prompt patterns:

**Primary Pattern Sources:**

- [ITONICS Innovation Platform](./references/itonics-innovation-platform.md) - 79 documented prompts across 8 categories
- [Machine Learning Mastery](./references/machine-learning-mastery.md) - Actor-Request-Context-Constraints framework
- [Medium: Shushant Lakhyani](./references/medium-shushant-lakhyani.md) - 10 creative + 10 LinkedIn content templates
- [Geeky Gadgets](./references/geeky-gadgets.md) - Advanced techniques (TRIZ, Six Thinking Hats, Disney Method)

**Academic & Research Sources:**

- [Vanderbilt Prompt Patterns](./references/vanderbilt-prompt-patterns.md) - 15 academic patterns with theoretical framework
- [PromptHub Role Prompting Research](./references/prompthub-role-prompting.md) - Empirical validation and effectiveness data
- [LearnPrompting.org](./references/learn-prompting.md) - Chain-of-Thought, Zero-Shot CoT, prompt structure

**Practical Application Sources:**

- [Better Creator](./references/better-creator.md) - 20 brainstorming techniques for content creators
- [LinkedIn: Ruben Hassid](./references/linkedin-ruben-hassid.md) - 8 prompts → 625 ideas scaling methodology
- [ClickUp Templates](./references/clickup-templates.md) - Product management, LinkedIn, competitor analysis prompts
- [Software Testing Prompts](./references/software-testing-prompts.md) - QA-specific patterns and test case generation

### Source Documentation

[Bibliography and Source Documentation](./references/bibliography-and-source-documentation.md) - Complete citations with URLs [Verification Note](./references/verification-note.md) - Evidence strength assessment

## Using This Skill

<usage_workflow> Step 1: Identify the brainstorming goal (quantity, quality, innovation level, domain) Step 2: Consult Pattern Selection Guide to choose appropriate pattern category Step 3: Load relevant pattern documentation for exact templates Step 4: Apply pattern with user's specific context Step 5: If needed, combine patterns or iterate with constraint variation </usage_workflow>

## Pattern Application Examples

<example_simple> User: "Help me brainstorm marketing campaign ideas" Pattern: Perspective Multiplication (Pattern 1A: Role-Based Persona) Approach: Generate ideas from Customer Success Manager, Sales VP, and Product Manager perspectives Expected Output: 15 ideas with reasoning from each viewpoint </example_simple>

<example_constraint> User: "Generate product features with $20k budget, 4-week timeline" Pattern: Constraint Variation (Pattern 2B: Resource Type Constraints) Approach: Use exact budget/time constraints to force creative solutions within reality Expected Output: 5 implementable features with resource breakdowns </example_constraint>

<example_innovation> User: "Break through conventional thinking on user onboarding" Pattern: Inversion (Pattern 3A: Worst Possible Idea) + Analogical Transfer (Pattern 4A) Approach: First invert ("worst onboarding"), then apply cross-domain analogies (Netflix, hotel service) Expected Output: 3-5 genuinely novel approaches that competitors miss </example_innovation>

## Output Format Optimization

<format_guidance> Successful brainstorming patterns specify exact output formats:

- "Numbered list" > "bullet points" (better for idea tracking)
- "Table format: Idea | Reasoning | Implementation | Trade-offs" (forces completeness)
- "For each idea, explain your reasoning" (increases quality 40%)
- Specify word count ranges (200-400 words prevents both brevity and verbosity) </format_guidance>

## Skill Resources

This skill contains:

- **references/** - Pattern documentation, research sources, domain guides
- **scripts/** - (Optional: future automation for pattern selection, template generation)
- **assets/** - (Optional: future workshop templates, ideation canvases)

All pattern content is verified against original sources. No fabricated patterns or unverified claims.

## Notes for Claude Instances

<ai_instructions> When using this skill:

- Always verify pattern category matches user's actual need
- Provide exact prompt templates from reference files, not paraphrased versions
- Cite source files when referencing specific patterns
- Combine patterns when single pattern insufficient
- Adjust templates to user's specific context while preserving structural elements
- Use progressive disclosure: start with pattern overview, load detailed references as needed </ai_instructions>
