---
name: prompt-engineering
description: >
  Provides workflows to write, debug, and optimize prompts for LLMs, including
  few-shot example selection, chain-of-thought structuring, system prompt
  design, and template composition. Use when the user asks to write or improve
  a prompt, wants help with few-shot examples, chain-of-thought, system prompts,
  prompt templates, or asks how to get better results from an LLM.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Prompt Engineering

## Overview

Use this skill to design prompt systems that are clear, testable, and reusable.
It covers prompt drafting, optimization, evaluation, and production-oriented
patterns for few-shot prompting, reasoning workflows, templates, and system
prompts.

Keep the main workflow in this file and load the targeted reference files only
for the pattern you are applying.

## When to Use

Use this skill when:

- A user asks to write, rewrite, or improve a prompt
- A prompt needs better structure, reliability, or output formatting
- Few-shot examples or reasoning scaffolds are needed
- A system prompt or reusable prompt template must be created
- An existing prompt needs measurable optimization and testing

Read the relevant files in `references/` when you need deeper guidance on a
specific pattern.

## Core Patterns

### 1. Few-Shot Learning

#### Example Selection Strategy
- Use `references/few-shot-patterns.md` for comprehensive selection frameworks
- Balance example count (3-5 optimal) with context window limitations
- Include edge cases and boundary conditions in example sets
- Prioritize diverse examples that cover problem space variations
- Order examples from simple to complex for progressive learning

#### Few-Shot Example (Sentiment Classification)
```
Classify the sentiment as Positive, Negative, or Neutral.

Text: "I love this product! It exceeded my expectations."
Sentiment: Positive
Reasoning: Enthusiastic language, positive adjectives, satisfaction

Text: "The app keeps crashing when I upload large files."
Sentiment: Negative
Reasoning: Complaint about functionality, frustration indicator

Text: "It arrived on time, as described."
Sentiment: Neutral
Reasoning: Factual statement, no strong emotion either way

Text: "{user_input}"
Sentiment:
Reasoning:
```

### 2. Chain-of-Thought Reasoning

#### Implementation Patterns
- Reference `references/cot-patterns.md` for detailed reasoning frameworks
- Use "Let's think step by step" for zero-shot CoT initiation
- Provide complete reasoning traces for few-shot CoT demonstrations
- Implement self-consistency by sampling multiple reasoning paths
- Include verification and validation steps in reasoning chains

#### CoT Template Structure
```
Let's approach this step-by-step:

Step 1: {break_down_the_problem}
Analysis: {detailed_reasoning}

Step 2: {identify_key_components}
Analysis: {component_analysis}

Step 3: {synthesize_solution}
Analysis: {solution_justification}

Final Answer: {conclusion_with_confidence}
```

### 3. Prompt Optimization

#### Optimization Process
- Use `references/optimization-frameworks.md` for comprehensive optimization strategies
- Measure baseline performance before optimization attempts
- Implement single-variable changes for accurate attribution
- Track metrics: accuracy, consistency, latency, token efficiency
- Use statistical significance testing for A/B validation
- Document optimization iterations and their impacts

Track these metrics: accuracy, consistency, token efficiency, robustness, safety. See `references/optimization-frameworks.md` for measurement utilities.

### 4. Template Systems

#### Template Design Principles
- Reference `references/template-systems.md` for modular template frameworks
- Use clear variable naming conventions (e.g., `{user_input}`, `{context}`)
- Implement conditional sections for different scenario handling
- Design role-based templates for specific use cases
- Create hierarchical template composition patterns

#### Template Structure Example
```
# System Context
You are a {role} with {expertise_level} expertise in {domain}.

# Task Context
{if background_information}
Background: {background_information}
{endif}

# Instructions
{task_instructions}

# Examples
{example_count}

# Output Format
{output_specification}

# Input
{user_query}
```

### 5. System Prompt Design

#### System Prompt Components
- Use `references/system-prompt-design.md` for detailed design guidelines
- Define clear role specification and expertise boundaries
- Establish output format requirements and structural constraints
- Include safety guidelines and content policy adherence
- Set context for background information and domain knowledge

#### System Prompt Framework
```
You are an expert {role} specializing in {domain} with {experience_level} of experience.

## Core Capabilities
- List specific capabilities and expertise areas
- Define scope of knowledge and limitations

## Behavioral Guidelines
- Specify interaction style and communication approach
- Define error handling and uncertainty protocols
- Establish quality standards and verification requirements

## Output Requirements
- Specify format expectations and structural requirements
- Define content inclusion and exclusion criteria
- Establish consistency and validation requirements

## Safety and Ethics
- Include content policy adherence
- Specify bias mitigation requirements
- Define harm prevention protocols
```

## Implementation Workflows

### Workflow 1: Create New Prompt from Requirements

1. **Analyze Requirements**
   - Identify task complexity and reasoning requirements
   - Determine target model capabilities and limitations
   - Define success criteria and evaluation metrics
   - Assess need for few-shot learning or CoT reasoning

2. **Select Pattern Strategy**
   - Use few-shot learning for classification or transformation tasks
   - Apply CoT for complex reasoning or multi-step problems
   - Implement template systems for reusable prompt architecture
   - Design system prompts for consistent behavior requirements

3. **Draft Initial Prompt**
   - Structure prompt with clear sections and logical flow
   - Include relevant examples or reasoning demonstrations
   - Specify output format and quality requirements
   - Incorporate safety guidelines and constraints

4. **Validate and Test**
   - Test with at least 3 inputs: one happy path, one edge case, one adversarial
   - Measure accuracy and token usage against defined success criteria
   - Change one variable at a time, re-test, keep only what improves metrics
   - Document optimization decisions and their rationale

### Workflow 2: Optimize Existing Prompt

1. **Performance Analysis**
   - Measure current prompt performance metrics
   - Identify failure modes and error patterns
   - Analyze token efficiency and response latency
   - Assess consistency across multiple runs

2. **Optimization Strategy**
   - Apply systematic A/B testing with single-variable changes
   - Use few-shot learning to improve task adherence
   - Implement CoT reasoning for complex task components
   - Refine template structure for better clarity

3. **Implementation and Testing**
   - Re-run the same test cases from step 1 against the optimized prompt
   - If accuracy < baseline, revert the change and try a different hypothesis
   - If accuracy >= baseline but < 90%, return to step 2 with a new strategy
   - Document the winning change and its measured impact

### Workflow 3: Scale Prompt Systems

1. **Modular Architecture Design**
   - Decompose complex prompts into reusable components
   - Create template inheritance hierarchies
   - Implement dynamic example selection systems
   - Build automated quality assurance frameworks

2. **Production Integration**
   - Implement prompt versioning and rollback capabilities
   - Create performance monitoring and alerting systems
   - Build automated testing frameworks for prompt validation
   - Establish update and deployment workflows

## Quality Gates

- Accuracy >90% on 10+ diverse test cases before shipping
- <5% variance across 3+ repeated runs
- All edge cases and adversarial inputs handled gracefully
- Output format matches spec on every test case

## Best Practices

- Optimize one variable at a time so results stay attributable
- Keep prompts explicit about task, context, constraints, and output format
- Prefer a small number of strong examples over many repetitive ones
- Test prompts against happy-path, edge-case, and adversarial inputs
- Move long pattern details to `references/` instead of bloating `SKILL.md`

## Constraints and Warnings

- Do not assume longer prompts are better; extra detail often adds ambiguity
- Avoid exposing hidden reasoning requirements when a concise rationale is enough
- Validate prompts on representative inputs before claiming improvement
- Keep model-specific assumptions explicit because behavior varies across models

## Integration with Other Skills

This skill integrates seamlessly with:
- **langchain4j-ai-services-patterns**: Interface-based prompt design
- **langchain4j-rag-implementation-patterns**: Context-enhanced prompting
- **langchain4j-testing-strategies**: Prompt validation frameworks
- **unit-test-parameterized**: Systematic prompt testing approaches

## Resources and References

- `references/few-shot-patterns.md`: Comprehensive few-shot learning frameworks
- `references/cot-patterns.md`: Chain-of-thought reasoning patterns and examples
- `references/optimization-frameworks.md`: Systematic prompt optimization methodologies
- `references/template-systems.md`: Modular template design and implementation
- `references/system-prompt-design.md`: System prompt architecture and best practices

## Common Pitfalls and Solutions

| Pitfall | Fix |
|---|---|
| Wrong output format | Add a concrete output example at the end of the prompt |
| Inconsistent answers | Add 2-3 few-shot examples showing expected reasoning |
| Hallucination | Add "If unsure, say 'I don't know'" + constrain the answer domain |
| Too verbose | Add explicit word/sentence limit + "Be concise" instruction |
| Missed edge cases | Add an edge-case few-shot example |

## Constraints

- Test across target models — capabilities and token limits vary
- Keep few-shot examples to 3-5 to manage context usage
- Validate with domain-specific test cases before production
