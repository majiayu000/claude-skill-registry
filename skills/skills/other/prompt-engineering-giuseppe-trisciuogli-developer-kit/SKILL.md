---
name: prompt-engineering
description: This skill should be used when creating, optimizing, or implementing advanced prompt patterns including few-shot learning, chain-of-thought reasoning, prompt optimization workflows, template systems, and system prompt design. It provides comprehensive frameworks for building production-ready prompts with measurable performance improvements.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Prompt Engineering

## Overview

This skill provides comprehensive frameworks for creating, optimizing, and implementing advanced prompt patterns that significantly improve LLM performance across various tasks and models. It covers few-shot learning, chain-of-thought reasoning, prompt optimization workflows, template systems, and system prompt design for production-ready AI applications.

## When to Use

Use this skill when:
- Creating new prompts for complex reasoning or analytical tasks
- Optimizing existing prompts for better accuracy or efficiency
- Implementing few-shot learning with strategic example selection
- Designing chain-of-thought reasoning for multi-step problems
- Building reusable prompt templates and systems
- Developing system prompts for consistent model behavior
- Troubleshooting poor prompt performance or failure modes
- Scaling prompt systems for production use cases

## Core Prompt Engineering Patterns

### 1. Few-Shot Learning Implementation

Select examples using semantic similarity and diversity sampling to maximize learning within context window constraints.

#### Example Selection Strategy
- Use `references/few-shot-patterns.md` for comprehensive selection frameworks
- Balance example count (3-5 optimal) with context window limitations
- Include edge cases and boundary conditions in example sets
- Prioritize diverse examples that cover problem space variations
- Order examples from simple to complex for progressive learning

#### Few-Shot Template Structure
```
Example 1 (Basic case):
Input: {representative_input}
Output: {expected_output}

Example 2 (Edge case):
Input: {challenging_input}
Output: {robust_output}

Example 3 (Error case):
Input: {problematic_input}
Output: {corrected_output}

Now handle: {target_input}
```

### 2. Chain-of-Thought Reasoning

Elicit step-by-step reasoning for complex problem-solving through structured thinking patterns.

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

### 3. Prompt Optimization Workflows

Implement iterative refinement processes with measurable performance metrics and systematic A/B testing.

#### Optimization Process
- Use `references/optimization-frameworks.md` for comprehensive optimization strategies
- Measure baseline performance before optimization attempts
- Implement single-variable changes for accurate attribution
- Track metrics: accuracy, consistency, latency, token efficiency
- Use statistical significance testing for A/B validation
- Document optimization iterations and their impacts

#### Performance Metrics Framework
- **Accuracy**: Task completion rate and output correctness
- **Consistency**: Response stability across multiple runs
- **Efficiency**: Token usage and response time optimization
- **Robustness**: Performance across edge cases and variations
- **Safety**: Adherence to guidelines and harm prevention

### 4. Template Systems Architecture

Build modular, reusable prompt components with variable interpolation and conditional sections.

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

Design comprehensive system prompts that establish consistent model behavior, output formats, and safety constraints.

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
   - Test with diverse input scenarios including edge cases
   - Measure performance against defined success criteria
   - Iterate refinement based on testing results
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
   - Deploy optimized prompts with controlled rollout
   - Monitor performance metrics in production environment
   - Compare against baseline using statistical significance
   - Document improvements and lessons learned

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

## Quality Assurance

### Validation Requirements
- Test prompts with at least 10 diverse scenarios
- Include edge cases, boundary conditions, and failure modes
- Verify output format compliance and structural consistency
- Validate safety guideline adherence and harm prevention
- Measure performance across multiple model runs

### Performance Standards
- Achieve >90% task completion for well-defined use cases
- Maintain <5% variance across multiple runs for consistency
- Optimize token usage without sacrificing accuracy
- Ensure response latency meets application requirements
- Demonstrate robust handling of edge cases and unexpected inputs

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

## Usage Examples

### Example 1: Classification Task with Few-Shot Learning
```
Classify customer feedback into categories using semantic similarity for example selection and diversity sampling for edge case coverage.
```

### Example 2: Complex Reasoning with Chain-of-Thought
```
Implement step-by-step reasoning for financial analysis with verification steps and confidence scoring.
```

### Example 3: Template System for Customer Service
```
Create modular templates with role-based components and conditional sections for different inquiry types.
```

### Example 4: System Prompt for Code Generation
```
Design comprehensive system prompt with behavioral guidelines, output requirements, and safety constraints.
```

## Common Pitfalls and Solutions

- **Overfitting examples**: Use diverse example sets with semantic variety
- **Context window overflow**: Implement strategic example selection and compression
- **Inconsistent outputs**: Specify clear output formats and validation requirements
- **Poor generalization**: Include edge cases and boundary conditions in training examples
- **Safety violations**: Incorporate comprehensive content policies and harm prevention

## Performance Optimization

- Monitor token usage and implement compression strategies
- Use caching for repeated prompt components
- Optimize example selection for maximum learning efficiency
- Implement progressive disclosure for complex prompt systems
- Balance prompt complexity with response quality requirements

## Best Practices

### Design Principles
- Write clear, specific instructions that leave no ambiguity
- Structure prompts with logical sections and consistent formatting
- Use role-based prompts for consistent behavioral patterns
- Include concrete examples to demonstrate expected outputs
- Define output format requirements explicitly

### Implementation Guidelines
- Start with simple prompts and iterate based on testing
- Test with diverse input scenarios including edge cases
- Document prompt versions and their performance metrics
- Implement error handling for unexpected inputs
- Monitor performance in production environments

### Common Pitfalls to Avoid
- Overfitting examples to specific patterns
- Ignoring context window limitations and token budgeting
- Neglecting output format specifications
- Failing to handle edge cases and error scenarios
- Not measuring and tracking prompt performance over time

## Constraints and Warnings

### Model Limitations
- Different models have varying capabilities and token limits
- Complex prompts may exceed context windows unexpectedly
- Model behavior can vary across different versions
- Some reasoning tasks require specific prompting techniques

### Resource Considerations
- Longer prompts consume more tokens and increase costs
- Complex few-shot examples impact context usage
- Multiple model calls for optimization increase expenses
- Testing requires sufficient sample sizes for statistical significance

### Quality Requirements
- Validate prompts with domain-specific test cases
- Ensure prompts generalize beyond training examples
- Implement monitoring for prompt performance drift
- Regularly review and update prompts as requirements evolve

This skill provides the foundational patterns and methodologies for building production-ready prompt systems that consistently deliver high performance across diverse use cases and model types.