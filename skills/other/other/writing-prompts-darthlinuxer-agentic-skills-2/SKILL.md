---
name: writing-prompts
description: Use when crafting prompts for LLMs to improve response quality, accuracy,
  consistency, and task performance
---

# Writing Prompts

## Overview
Prompt engineering is the systematic process of crafting effective prompts for large language models (LLMs) to achieve better, more reliable, and more targeted responses. This skill provides proven techniques for maximizing LLM capabilities through structured prompt design, iterative refinement, and model-specific optimization.

**Core principle:** Great prompts are specific, contextual, and tested. They guide the model's reasoning process while leaving appropriate degrees of freedom for the task at hand.

## When to Use
Use this skill when:
- Creating initial prompts for new tasks with LLMs
- Improving existing prompts that produce inconsistent or suboptimal results
- Working with complex tasks requiring step-by-step reasoning
- Needing LLMs to adopt specific roles or behaviors
- Developing prompts for production applications
- Debugging prompt-related issues in LLM interactions
- Optimizing token usage while maintaining output quality
- Adapting prompts across different LLM providers (Anthropic, GPT, Gemini, etc.)

## Core Pattern
Follow this iterative RED-GREEN-REFACTOR process for prompt development:

1. **Define Success Criteria** (Write the Test): Clearly specify what constitutes a good response with measurable criteria
2. **Establish Baseline** (RED): Test without optimization to see default behavior and failure modes
3. **Draft Initial Prompt** (Minimal Fix): Start with the simplest prompt that addresses observed failures
4. **Apply Techniques** (GREEN): Layer proven prompt engineering methods until success criteria met
5. **Test & Iterate**: Evaluate against diverse inputs, edge cases, and failure scenarios
6. **Refactor**: Optimize for clarity, token efficiency, and robustness without breaking success criteria

**Key insight:** Like TDD, you must see the prompt fail before you know what to fix. Test early, test often.

## Fundamental Principles

### 1. Be Specific and Direct
**Don't assume the model knows your intent.** Explicit instructions outperform vague requests.

❌ **Vague:** "Analyze this code"
✅ **Specific:** "Review this Python function for security vulnerabilities. Check for SQL injection, XSS, and CSRF risks. Provide specific line numbers and fix recommendations."

### 2. Provide Sufficient Context
Models perform better with relevant background information, constraints, and domain knowledge.

**Include:**
- Domain-specific terminology definitions
- Business rules and constraints
- Expected input/output formats
- Edge cases to handle or avoid
- Success criteria and quality standards

### 3. Match Freedom to Task Fragility
**High variability tasks:** Use text-based instructions that allow flexibility
**Low variability tasks:** Provide specific formats, templates, or exact patterns

### 4. Show, Don't Just Tell
Examples (few-shot prompting) dramatically improve consistency and format adherence.

**One-shot:** One example
**Few-shot:** 2-5 examples showing variety
**Many-shot:** 10+ examples for complex pattern recognition

### 5. Guide the Reasoning Process
For complex tasks, explicitly structure how the model should think:
- Break down into steps
- Request intermediate reasoning
- Ask for validation checks
- Encourage self-correction

## Quick Reference

| Technique | Purpose | When to Use | Token Cost |
|-----------|---------|-------------|------------|
| **System Prompts** | Set persistent role/behavior | Complex domains, specific expertise | Low |
| **Role Prompting** | Define expert persona | Technical/specialized tasks | Low |
| **Chain of Thought** | Step-by-step reasoning | Multi-step analysis, math, logic | Medium |
| **Few-Shot Prompting** | Provide 2-5 examples | Format consistency, pattern matching | Medium-High |
| **XML/Structured Tags** | Organize complex prompts | Multiple sections, clear boundaries | Low |
| **Output Formatting** | Specify exact output structure | JSON, tables, specific formats | Low |
| **Constraints & Guards** | Prevent unwanted behavior | Production safety, compliance | Low |
| **Prefill/Assistant Start** | Guide response beginning | Ensure format, start reasoning | Very Low |
| **Multi-turn Scaffolding** | Break task into conversation | Very complex, iterative tasks | Variable |

## Implementation

### Step 1: Establish Success Criteria (Write Your Test)
Before writing any prompt, define measurable success criteria:

**Questions to answer:**
- What must the output contain? (Required elements)
- What format should it follow? (JSON, markdown, plaintext, etc.)
- What quality standards must it meet? (Accuracy, depth, tone)
- What edge cases should it handle? (Empty inputs, errors, ambiguity)
- How will you measure success? (Automated checks, manual review)

**Example criteria:**
```
✓ Output is valid JSON
✓ Contains fields: timestamp, severity, message, recommendation
✓ Severity is one of: LOW, MEDIUM, HIGH, CRITICAL
✓ Recommendation is actionable (verb-based)
✓ Handles malformed log entries gracefully
```

### Step 2: Test Baseline Behavior (RED)
Run your task WITHOUT optimization to see default behavior:

```
User: Parse this log entry: ERROR 2024-01-15 10:30:45 Connection timeout
```

**Document failures:**
- Inconsistent format across runs
- Missing fields
- Incorrect severity classification
- Vague or missing recommendations

This baseline tells you what to fix.

### Step 3: Use System Prompts for Persistent Context
System prompts set persistent behavior across the conversation. Use for:
- Role assignment
- Behavioral guidelines
- Output format rules
- Domain context

**Example:**
```xml
<system>
You are a senior security analyst with 15 years of experience in enterprise log analysis.
You specialize in identifying security incidents and providing actionable remediation steps.

Always output in JSON format with these fields:
- timestamp: ISO 8601 format
- severity: LOW|MEDIUM|HIGH|CRITICAL
- message: Brief description
- recommendation: Specific action to take
</system>
```

### Step 4: Structure the User Prompt
Build the user-facing prompt with clear sections:

**A. Task Description (What)**
```
Parse the following log entry and classify the security event.
```

**B. Context & Constraints (Why/How)**
```
This is from a production web server. Focus on:
- Authentication failures
- Connection issues
- Resource exhaustion
- Potential attacks

Classify severity based on:
- CRITICAL: Active attack or data breach
- HIGH: Security vulnerability exposed
- MEDIUM: Unusual pattern requiring investigation
- LOW: Expected error or minor issue
```

**C. Input Specification**
```
Log format: LEVEL YYYY-MM-DD HH:MM:SS MESSAGE
```

**D. Output Format**
```json
{
  "timestamp": "ISO 8601",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "message": "Brief description",
  "recommendation": "Specific action"
}
```

### Step 5: Add Examples (Few-Shot Learning)
Provide 2-5 diverse examples showing the desired pattern:

**Example structure:**
```xml
<examples>
<example>
<input>ERROR 2024-01-15 10:30:45 Connection timeout from 192.168.1.100</input>
<output>
{
  "timestamp": "2024-01-15T10:30:45Z",
  "severity": "MEDIUM",
  "message": "Connection timeout from internal IP",
  "recommendation": "Check network connectivity and firewall rules for 192.168.1.100"
}
</output>
</example>

<example>
<input>CRITICAL 2024-01-15 11:15:22 Authentication failure: 50 attempts from 203.0.113.42</input>
<output>
{
  "timestamp": "2024-01-15T11:15:22Z",
  "severity": "CRITICAL",
  "message": "Brute force authentication attack detected",
  "recommendation": "Immediately block IP 203.0.113.42 and review authentication logs for compromised accounts"
}
</output>
</example>
</examples>
```

**Guidelines for examples:**
- Show edge cases (malformed input, ambiguous scenarios)
- Demonstrate variety in severity levels
- Include both simple and complex cases
- Keep examples realistic and representative

### Step 6: Incorporate Reasoning Techniques
For complex tasks, guide the model's thinking process:

**Chain of Thought:**
```
Before providing your final answer, think through:
1. What type of event is this? (authentication, connection, resource, attack)
2. What is the potential impact? (data loss, service disruption, security breach)
3. What context clues indicate severity? (frequency, source IP, error type)
4. What immediate actions would mitigate risk?

Then provide your structured JSON response.
```

**Structured Reasoning with XML:**
```xml
<instructions>
Analyze the log entry using this process:

<step1>Identify the event type and key details</step1>
<step2>Assess potential security impact</step2>
<step3>Classify severity based on threat level</step3>
<step4>Formulate specific, actionable recommendation</step4>

After your analysis, output only the final JSON response.
</instructions>
```

### Step 7: Add Constraints and Safety Guards
Prevent unwanted behavior with explicit constraints:

```
Constraints:
- Do NOT include explanatory text outside the JSON structure
- Do NOT make up fields not in the schema
- If log format is unrecognizable, use severity "LOW" and recommendation "Manual review required"
- Do NOT recommend actions that could cause service disruption without approval
```

### Step 8: Test, Measure, Iterate (GREEN)
Run your prompt against:
- **Happy path:** Standard, well-formed inputs
- **Edge cases:** Empty, malformed, ambiguous inputs
- **Stress tests:** Unusual patterns, extreme values
- **Consistency:** Same input multiple times

**Measure against criteria:**
```
Test 1: Standard ERROR log → ✓ Valid JSON, ✓ Correct severity
Test 2: Malformed input → ✓ Graceful handling
Test 3: Ambiguous severity → ✗ Inconsistent classification
```

**Iterate based on failures:**
If inconsistent severity classification, add:
```
When severity is ambiguous, err on the side of caution (classify higher).
Explicitly state your reasoning for severity choice.
```

### Step 9: Refactor for Efficiency (REFACTOR)
Once tests pass, optimize:

**Token reduction:**
- Remove redundant explanations
- Consolidate similar instructions
- Use concise examples

**Clarity improvement:**
- Use structured formats (XML, JSON) for complex prompts
- Group related instructions
- Add section headers for navigation

**Before (verbose):**
```
You need to parse log entries. Log entries contain information about
system events. They have a timestamp, which tells you when the event
happened, and a severity level, which could be ERROR, WARNING, INFO,
or DEBUG. You should extract this information and...
```

**After (concise):**
```
Parse log entries into structured JSON:
- timestamp: Event time (ISO 8601)
- severity: ERROR|WARNING|INFO|DEBUG
- message: Event description
- recommendation: Action to take
```

### Step 10: Model-Specific Optimization
Different LLMs have different strengths. Adapt accordingly:

**Anthropic models:**
- Excels with XML-structured prompts
- Use `<thinking>` tags for extended reasoning
- Supports very long context (200K+ tokens)
- Prefill assistant responses for format control

**GPT (OpenAI):**
- Prefers JSON for structured tasks
- Use system messages for role/behavior
- Adjust temperature for creativity vs. consistency
- Function calling for structured outputs

**Gemini:**
- Strong with multi-modal inputs (text + images)
- Use examples liberally
- Clear role definitions improve performance

## Common Mistakes

### 1. Vague Instructions
❌ **Bad:** "Analyze this code"
✅ **Good:** "Analyze this Python function for security vulnerabilities. Check for SQL injection, XSS, and CSRF risks. Provide specific line numbers and fix recommendations with code examples."

**Why it matters:** LLMs can't read your mind. Specificity dramatically improves output quality.

### 2. Missing Context
❌ **Bad:** "Generate a user authentication function"
✅ **Good:** "Generate a user authentication function for a Flask REST API. Use bcrypt for password hashing, JWT for tokens, and include rate limiting. Handle errors gracefully and return appropriate HTTP status codes."

**Why it matters:** Context shapes decisions. Without it, models make assumptions that may not match your needs.

### 3. No Examples for Format-Critical Tasks
❌ **Bad:** "Convert this to JSON"
✅ **Good:** 
```
Convert log entries to JSON. Example:

Input: ERROR 2024-01-15 10:30:45 Connection timeout
Output: {"timestamp": "2024-01-15T10:30:45Z", "level": "ERROR", "message": "Connection timeout"}

Now convert: {actual input}
```

**Why it matters:** Examples provide unambiguous specification. "Show, don't tell."

### 4. Over-Constraining
❌ **Bad:** "Write a function using exactly 15 lines, with 2 parameters, no external libraries, and variable names starting with 'x'"
✅ **Good:** "Write a concise function that processes user input. Use standard library when possible."

**Why it matters:** Unnecessary constraints limit the model's ability to find optimal solutions.

### 5. Ignoring Chain of Thought for Complex Tasks
❌ **Bad:** "What's the optimal database schema for this application?"
✅ **Good:** 
```
Design a database schema for this application. Think through:
1. What entities and relationships exist?
2. What queries will be most common?
3. What normalization level balances performance and maintainability?
4. What indexes are needed?

Provide your final schema with rationale for key decisions.
```

**Why it matters:** Complex tasks benefit from structured reasoning. Rushing to an answer produces lower quality results.

### 6. Single-Test Evaluation
❌ **Bad:** Running prompt once, assuming it works
✅ **Good:** Testing with diverse inputs, edge cases, multiple runs

**Why it matters:** LLMs have inherent variability. One success doesn't guarantee consistent performance.

### 7. Not Leveraging Model-Specific Features
❌ **Bad:** Using identical prompts for all LLMs
✅ **Good:** 
- Anthropic: Use XML structure, `<thinking>` tags, prefill
- GPT: Use system messages, function calling, temperature tuning
- Gemini: Leverage multimodal capabilities

**Why it matters:** Each model has unique strengths. Generic prompts underutilize capabilities.

### 8. Assuming Context Retention
❌ **Bad:** Referencing information from 50 messages ago without repetition
✅ **Good:** Re-stating critical context or using explicit references

**Why it matters:** Even long-context models benefit from explicit reminders. Don't assume perfect recall.

### 9. Ignoring Token Economics
❌ **Bad:** 2000-word prompt for simple task
✅ **Good:** Concise prompt with essential information only

**Why it matters:** Tokens cost money and share context window. Every unnecessary token is waste.

### 10. No Iterative Refinement
❌ **Bad:** One-shot prompt, use forever
✅ **Good:** Test → Document failures → Refine → Re-test → Optimize

**Why it matters:** Prompt engineering is iterative. Initial prompts rarely achieve optimal performance.

## Advanced Techniques

### Prompt Chaining
Break complex tasks into sequential prompts where each builds on the previous:

```
Prompt 1: "Extract all function names from this code"
Prompt 2: "For each function: {output from Prompt 1}, analyze complexity"
Prompt 3: "Based on complexity scores: {output from Prompt 2}, recommend refactoring priorities"
```

**When to use:** Task too complex for single prompt, intermediate validation needed, or each step requires different expertise.

### Prompt Scaffolding
Use conversation structure to guide multi-step reasoning:

```
User: Here's the problem: {problem description}
Assistant: I'll analyze this step by step. First, let me identify...
User: Continue with step 2.
Assistant: Now examining...
```

### Meta-Prompting
Have the LLM improve its own prompts:

```
You are a prompt engineering expert. Analyze this prompt and suggest improvements:

{original prompt}

Focus on:
- Clarity and specificity
- Completeness of context
- Effectiveness of examples
- Potential ambiguities

Provide revised prompt with explanation of changes.
```

### Prompt Templates
Create reusable templates for common patterns:

```xml
<prompt_template name="code_review">
  <role>You are a {language} expert with {years} years of experience in {domain}</role>
  
  <task>Review the following {language} code for:
    - {concern_1}
    - {concern_2}
    - {concern_3}
  </task>
  
  <output_format>
    For each issue found:
    1. Line number
    2. Issue description
    3. Severity (LOW|MEDIUM|HIGH|CRITICAL)
    4. Recommended fix with code example
  </output_format>
  
  <code>{code_to_review}</code>
</prompt_template>
```

**Usage:** Fill in placeholders for specific tasks. Ensures consistency across similar tasks.

### Constitutional AI Principles
Embed behavioral guidelines directly in prompts:

```
Follow these principles:
1. Be helpful, harmless, and honest
2. If uncertain, express uncertainty clearly
3. Prioritize user safety over task completion
4. Refuse harmful requests politely but firmly
5. Cite sources when making factual claims
```

**When to use:** Production applications, user-facing systems, compliance requirements.

### Negative Prompting
Explicitly state what NOT to do (use sparingly—focus on positive instructions):

```
Do NOT:
- Hallucinate package versions or APIs
- Recommend deprecated methods
- Make assumptions about production environment
- Suggest changes without explaining rationale
```

### Self-Consistency Sampling
Request multiple independent solutions, then synthesize:

```
Generate 3 different approaches to solve this problem.
For each approach, explain trade-offs.
Then recommend which approach is best for production use and why.
```

**When to use:** Critical decisions, high-stakes tasks, or when exploring solution space.

### Prompt Ensembling
Combine outputs from different prompt variations:

```
Variation 1: Direct task instruction
Variation 2: Step-by-step breakdown
Variation 3: Example-driven approach

Compare outputs, keep best elements from each.
```

## Model-Specific Optimizations

### Anthropic models

**Strengths:**
- XML-structured prompts
- Extended reasoning with `<thinking>` tags
- Very long context (200K+ tokens)
- Strong instruction following

**Techniques:**
```xml
<system>
You are an expert code reviewer.
</system>

<instructions>
<step1>Read the code thoroughly</step1>
<step2>Identify potential issues</step2>
<step3>Provide specific recommendations</step3>
</instructions>

<code>
{code_here}
</code>

<thinking>
Let me analyze this step by step...
</thinking>
```

**Prefill (Assistant Start):**
```
User: Analyze this code for bugs.
Assistant: Here is my analysis in JSON format:
{
```

The model will continue from the prefilled start, ensuring JSON output.

### GPT (OpenAI)

**Strengths:**
- System messages for persistent behavior
- Function calling for structured outputs
- Temperature control for creativity
- Strong with conversational context

**Techniques:**
```python
{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "You are a Python security expert."},
    {"role": "user", "content": "Review this code for vulnerabilities:\n{code}"}
  ],
  "temperature": 0.3,  # Lower for consistent analysis
  "functions": [...],  # Structured output schema
}
```

**Function Calling:**
```json
{
  "name": "report_vulnerability",
  "parameters": {
    "type": "object",
    "properties": {
      "severity": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]},
      "description": {"type": "string"},
      "line_number": {"type": "integer"},
      "recommendation": {"type": "string"}
    }
  }
}
```

### Gemini (Google)

**Strengths:**
- Multi-modal (text + images)
- Strong with diverse examples
- Good at following explicit role definitions
- Efficient with structured data

**Techniques:**
```
Role: You are a technical documentation specialist.

Context: This is code from a production web application.

Examples:
{3-5 high-quality examples}

Task: {specific task}
```

## Testing Your Prompts

### Test Suite Structure
```
1. Happy Path Tests
   - Standard, well-formed inputs
   - Expected use cases
   
2. Edge Case Tests
   - Empty/null inputs
   - Malformed data
   - Extreme values
   
3. Consistency Tests
   - Same input, multiple runs
   - Measure variance
   
4. Stress Tests
   - Maximum complexity inputs
   - Unusual patterns
   - Adversarial examples
```

### Evaluation Metrics
**Automated:**
- Format validation (JSON schema, regex)
- Required field presence
- Value range checks
- Consistency across runs

**Manual:**
- Accuracy of analysis
- Quality of recommendations
- Appropriateness of tone
- Handling of ambiguity

### A/B Testing
Compare prompt variations:
```
Version A: Direct instruction
Version B: With examples
Version C: Step-by-step breakdown

Measure: Accuracy, consistency, token usage
Winner: Version with best balance
```

## Debugging Prompts

### Common Issues and Fixes

**Issue:** Inconsistent output format
**Fix:** Add explicit format examples, use structured tags, prefill response start

**Issue:** Model ignores instructions
**Fix:** Make instructions more prominent (bold, ALL CAPS for critical rules), repeat key points, add negative examples

**Issue:** Output too verbose/concise
**Fix:** Specify desired length explicitly ("in 2-3 sentences" or "provide detailed analysis"), adjust role expectations

**Issue:** Hallucinated information
**Fix:** Add "If you don't know, say you don't know" instruction, request sources/citations, reduce temperature

**Issue:** Poor reasoning quality
**Fix:** Add chain-of-thought prompting, request step-by-step breakdown, provide reasoning examples

### Diagnostic Process
1. **Isolate:** Test with minimal prompt
2. **Expand:** Add one technique at a time
3. **Compare:** Note impact of each addition
4. **Measure:** Use success criteria from Step 1
5. **Iterate:** Refine based on data, not intuition

## Real-World Impact
Effective prompt engineering delivers measurable improvements:

**Accuracy:** 30-70% reduction in errors for complex tasks through structured reasoning and clear constraints

**Consistency:** 80%+ output uniformity across multiple runs with examples and format specifications

**Development velocity:** 50%+ faster iteration on LLM-powered features via systematic testing and refinement

**User experience:** Higher quality, more reliable AI interactions that meet user expectations

**Cost efficiency:** 20-40% token reduction through concise, well-structured prompts without quality loss

**Model leverage:** Full utilization of model-specific capabilities (XML for Anthropic, function calling for GPT, multimodal for Gemini)

## Quick Start Checklist

When crafting a new prompt, follow this checklist:

- [ ] Define success criteria (what makes a good response?)
- [ ] Test baseline behavior (see how it fails without optimization)
- [ ] Set role/context in system prompt (if applicable)
- [ ] Write specific task instructions (no vague requests)
- [ ] Add relevant context and constraints
- [ ] Include 2-5 examples for format-critical tasks
- [ ] Guide reasoning for complex tasks (chain of thought)
- [ ] Specify exact output format
- [ ] Test with diverse inputs (happy path + edge cases)
- [ ] Measure against success criteria
- [ ] Iterate based on failures
- [ ] Refactor for clarity and token efficiency
- [ ] Optimize for specific LLM (Anthropic, GPT, Gemini)

## Prompt Template Library

### Analysis Prompt
```xml
<role>You are a {domain} expert with expertise in {specialty}</role>

<task>
Analyze the following {artifact_type} for {concern_1}, {concern_2}, and {concern_3}.
</task>

<context>
{relevant_background}
{constraints}
</context>

<output_format>
For each finding:
1. Location/identifier
2. Issue description
3. Severity (LOW|MEDIUM|HIGH|CRITICAL)
4. Recommendation
</output_format>

<artifact>
{content_to_analyze}
</artifact>
```

### Generation Prompt
```xml
<role>You are an experienced {role}</role>

<task>
Generate {output_type} that {requirements}.
</task>

<specifications>
- {spec_1}
- {spec_2}
- {spec_3}
</specifications>

<examples>
<example>
<input>{example_input_1}</input>
<output>{example_output_1}</output>
</example>
</examples>

<input>
{actual_input}
</input>
```

### Transformation Prompt
```xml
<task>
Transform the following {input_format} into {output_format}.
</task>

<transformation_rules>
- {rule_1}
- {rule_2}
- {rule_3}
</transformation_rules>

<examples>
<example>
<input>{example_input}</input>
<output>{example_output}</output>
</example>
</examples>

<input>
{content_to_transform}
</input>
```

### Decision/Recommendation Prompt
```xml
<role>You are a {domain} consultant</role>

<context>
{situation_description}
{constraints}
{goals}
</context>

<task>
Evaluate options and recommend the best approach.
</task>

<evaluation_criteria>
1. {criterion_1}
2. {criterion_2}
3. {criterion_3}
</evaluation_criteria>

<thinking_process>
For each option:
1. Analyze pros and cons
2. Assess against criteria
3. Consider trade-offs
4. Rate overall fit
</thinking_process>

<output_format>
- Recommended option: {choice}
- Rationale: {explanation}
- Implementation steps: {steps}
- Risks: {potential_issues}
</output_format>
```

## Resources and Further Learning

**Anthropic Resources:**
- Prompt engineering guide: 
- Anthropic best practices: See `anthropic-best-practices.md` in writing-skills directory

**OpenAI Resources:**
- Prompt engineering guide: 
- GPT best practices: 

**Google Resources:**
- Gemini prompting strategies: 

**General Resources:**
- Prompt engineering research papers
- Community prompt libraries (PromptBase, ShareGPT)
- Model-specific Discord/community forums

## Related Skills

- **writing-skills:** General skill authoring and TDD for documentation
- **test-driven-development:** RED-GREEN-REFACTOR cycle applied to code
- **subagent-driven-development:** Using subagents to validate prompts and skills
- **verification-before-completion:** Ensuring quality before marking tasks complete

---

*Remember: Great prompts are specific, tested, and iteratively refined. Start simple, fail fast, and refine based on data.*
