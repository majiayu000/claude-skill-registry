---
sidebar_position: 10
title: "Finalize Your Evals Skill"
description: "Validate your agent-evals skill by testing it on a completely different agent. A skill proves its worth when it transfers beyond the context where you learned it."
keywords: [agent evaluation, skill validation, portable skills, evaluation methodology, framework-agnostic, skill finalization, customer support agent, evals testing]
chapter: 47
lesson: 10
duration_minutes: 20

# HIDDEN SKILLS METADATA
skills:
  - name: "Validating Skill Portability"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can apply their agent-evals skill to a completely different agent type and verify it produces useful evaluation artifacts"

  - name: "Documenting Skills for Future Use"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can create complete skill documentation that enables future invocation without rereading the source material"

  - name: "Framework-Agnostic Thinking"
    proficiency_level: "B2"
    category: "Conceptual"
    bloom_level: "Analyze"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can identify which evaluation concepts transfer across frameworks and which require framework-specific adaptation"

  - name: "Continuous Skill Improvement"
    proficiency_level: "B1"
    category: "Soft"
    bloom_level: "Understand"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can articulate how skills evolve through use and identify when a skill needs updating based on new patterns encountered"

learning_objectives:
  - objective: "Validate skill portability by applying agent-evals skill to a different agent domain"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student generates eval dataset and grader for a non-Task-API agent and verifies the skill produced useful outputs"

  - objective: "Complete skill documentation using the standard format"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student's SKILL.md file contains all required sections with concrete patterns extracted from chapter learning"

  - objective: "Identify framework-agnostic evaluation concepts versus framework-specific implementations"
    proficiency_level: "B2"
    bloom_level: "Analyze"
    assessment_method: "Student correctly categorizes 5+ evaluation concepts as portable or framework-specific with justification"

  - objective: "Articulate the continuous improvement model for skills"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Student describes how their skill will evolve as they encounter new evaluation patterns"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (skill portability validation, documentation completeness, framework-agnostic thinking, skill evolution) within B1-B2 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Apply skill to three different agent types across different domains; identify patterns that emerge from multiple applications"
  remedial_for_struggling: "Focus on documentation completion first; defer multi-domain testing to post-chapter practice"
---

# Finalize Your Evals Skill

You started this chapter by creating a skeleton. Now it is time to see what you actually built.

A skill only proves its worth when it works on something you did not learn it on. You developed your agent-evals skill using Task API examples throughout this chapter. Every dataset design, grader pattern, and error analysis method came from that context. The question is: does your skill transfer?

This lesson has one purpose. You will take your completed skill and apply it to a completely different agent. Not Task API. Not anything you have seen in this chapter. A fresh domain where your skill must stand on its own.

If your skill helps you design evaluations for this new agent without returning to the chapter content, you own something valuable. If you find yourself confused or missing patterns, you know exactly where your skill needs strengthening.

## What Your Skill Should Include

Before testing portability, verify your skill is complete. Review your `skills/agent-evals/SKILL.md` and check for these sections:

| Section | Purpose | Completeness Check |
|---------|---------|-------------------|
| **Core Thesis** | Why evals matter | Andrew Ng quote + your interpretation |
| **When to Activate** | Trigger patterns | 5+ specific scenarios |
| **Evals vs TDD** | Foundational distinction | Table comparing tests and evals |
| **Dataset Design** | Creating test cases | Three categories: typical, edge, error |
| **Graders** | Defining "good" | Binary criteria pattern with examples |
| **Error Analysis** | Finding failure patterns | Spreadsheet method with component columns |
| **Component vs E2E** | Choosing eval scope | 5-step decision flow |
| **Regression Protection** | Preventing quality drops | Workflow and threshold guidance |
| **Framework Integration** | SDK-specific details | Table mapping concepts to frameworks |

If any section is missing or incomplete, address it now. A skill with gaps will fail when you need it most.

## Skill Validation Checklist

Your skill is ready for validation if it can help you with these four core tasks:

**Task 1: Dataset Design**

Can your skill help you design an eval dataset for any agent?

Criteria:
- [ ] Identifies the three categories (typical, edge, error)
- [ ] Provides guidance on starting with 10-20 cases
- [ ] Explains how to use real data instead of synthetic
- [ ] Includes patterns for growing datasets over time

**Task 2: Grader Creation**

Can your skill help you build graders that define "good" automatically?

Criteria:
- [ ] Explains why binary criteria beat 1-5 scales
- [ ] Provides grader code template (binary checks pattern)
- [ ] Covers LLM-as-Judge for subjective criteria
- [ ] Warns about position bias

**Task 3: Error Analysis**

Can your skill help you find which component caused failures?

Criteria:
- [ ] Includes spreadsheet method structure
- [ ] Lists trace terminology (trace, span, error classification)
- [ ] Provides prioritization guidance (frequency times feasibility)
- [ ] Explains how to focus effort where errors cluster

**Task 4: Component vs E2E Decision**

Can your skill help you choose the right eval scope?

Criteria:
- [ ] Includes the 5-step decision flow
- [ ] Explains when E2E is appropriate (ship decisions, production monitoring)
- [ ] Explains when component-level is better (debugging, tuning)
- [ ] Provides guidance on moving between scopes

If your skill satisfies all four task areas, proceed to validation. If not, return to the relevant lessons and extract the missing patterns.

## Testing on a Different Agent

Your skill was developed using Task API examples. Now test it on something completely different.

**Hypothetical Agent: Customer Support Bot**

A customer support agent that:
- Answers product questions from a knowledge base
- Handles returns and refunds
- Escalates complex issues to human agents
- Maintains a helpful and professional tone

This agent shares no code with Task API. It operates in a different domain with different success criteria. If your skill transfers, you can design evaluations for it without returning to chapter content.

### Apply Your Skill: Dataset Design

Using only your skill, design an eval dataset for the customer support agent.

**Typical Cases (5 examples)**:

| Input | Expected Behavior |
|-------|-------------------|
| "Where is my order?" | Ask for order number, provide tracking information |
| "What's your return policy?" | Quote return policy from knowledge base |
| "Can I get a refund?" | Clarify reason, initiate refund process if valid |
| "Product X isn't working" | Troubleshoot with standard questions, offer solutions |
| "How do I cancel my subscription?" | Verify identity, process cancellation, confirm |

**Edge Cases (3 examples)**:

| Input | Expected Behavior |
|-------|-------------------|
| "I'm really frustrated" + valid complaint | Acknowledge emotion, solve problem, maintain professionalism |
| Vague complaint without details | Ask clarifying questions, don't guess |
| Request for competitor comparison | Decline politely, redirect to product benefits |

**Error Cases (2 examples)**:

| Input | Expected Behavior |
|-------|-------------------|
| Request to access other customer's data | Refuse firmly, explain privacy policy |
| Abusive language without valid request | Maintain professionalism, offer to help when ready |

If you designed these categories using your skill's guidance, the skill is transferring.

### Apply Your Skill: Grader Creation

Design a grader for customer support responses using binary criteria.

```python
def grader_support_response(response: str, case: dict) -> dict:
    """
    Binary criteria grader for customer support agent.
    Each criterion is yes/no. Sum them for score.
    """
    checks = {
        # Criterion 1: Did it address the customer's issue?
        "addressed_issue": (
            case["expected_topic"] in response.lower()
        ),

        # Criterion 2: Did it maintain professional tone?
        "professional_tone": not any(
            word in response.lower()
            for word in ["rude", "stupid", "whatever"]
        ),

        # Criterion 3: Did it provide actionable next steps?
        "has_next_steps": any(
            phrase in response.lower()
            for phrase in ["please", "you can", "next step", "i'll help"]
        ),

        # Criterion 4: Did it avoid making things up?
        "no_hallucination": not (
            "our policy is" in response.lower() and
            case.get("has_no_policy", False)
        ),

        # Criterion 5: Did it know when to escalate?
        "appropriate_escalation": (
            case.get("should_escalate", False) ==
            ("human agent" in response.lower() or "escalate" in response.lower())
        )
    }

    score = sum(checks.values())
    return {
        "passed": score == 5,
        "score": score,
        "max_score": 5,
        "checks": checks,
        "explanation": f"Passed {score}/5 support criteria"
    }
```

**Output:**

```python
# Test the grader
test_case = {
    "input": "Where is my order?",
    "expected_topic": "order",
    "should_escalate": False
}

response = "I'd be happy to help you track your order. Please provide your order number and I'll look that up for you right away."

result = grader_support_response(response, test_case)
print(f"Score: {result['score']}/5")
print(f"Checks: {result['checks']}")
```

```
Score: 4/5
Checks: {'addressed_issue': True, 'professional_tone': True, 'has_next_steps': True, 'no_hallucination': True, 'appropriate_escalation': True}
```

If you created this grader using your skill's binary criteria pattern, the skill is working in a new domain.

## Documenting Your Skill

Your skill needs documentation that allows future you to use it without rereading the chapter. Complete this template in your `SKILL.md`:

```markdown
---
name: agent-evals
description: Design and implement evaluation frameworks for AI agents. Use when testing agent reasoning quality, building graders, doing error analysis, or establishing regression protection. Framework-agnostic concepts that apply to any SDK.
---

# Agent Evaluations: Measuring Reasoning Quality

**Core Thesis**: "One of the biggest predictors for whether someone is able to build agentic workflows really well is whether or not they're able to drive a really disciplined evaluation process." - Andrew Ng

## When to Activate

Use this skill when:
- Building systematic quality checks for any AI agent
- Designing evaluation datasets (typical, edge, error categories)
- Creating graders to define "good" automatically
- Performing error analysis to find failure patterns
- Setting up regression protection for agent changes
- Deciding when to use end-to-end vs component-level evals
- Debugging why an agent's output quality is inconsistent
- Preparing an agent for production deployment

## Core Patterns

### Pattern: Dataset Design (10-20 cases to start)

Categories:
- Typical (60%): Common use cases the agent will handle daily
- Edge (25%): Unusual but valid inputs that test boundaries
- Error (15%): Cases where agent should fail gracefully

Use REAL data from production logs when possible. Synthetic data misses the messiness of reality.

### Pattern: Binary Criteria Graders

DO NOT use 1-5 scales (LLMs are poorly calibrated).

DO use binary criteria:
1. Define 3-7 yes/no criteria
2. Check each criterion independently
3. Sum to get total score
4. Threshold for pass/fail

Template:
def grader(response, case) -> dict:
    checks = {"criterion_1": bool_check_1, "criterion_2": bool_check_2}
    score = sum(checks.values())
    return {"passed": score == len(checks), "score": score, "checks": checks}

### Pattern: Error Analysis (Spreadsheet Method)

Columns: Case | Routing | Tool Selection | Output Format | Content Quality
Process:
1. Run failing cases through eval suite
2. Trace each failure to component
3. Count which component fails most often
4. Prioritize: frequency x feasibility

### Pattern: Component vs E2E Decision

5-step flow:
1. Start with E2E evals to find overall quality
2. Use error analysis to identify problem component
3. Build component-level eval for that component
4. Tune component using component eval
5. Verify improvement with E2E eval

### Pattern: Regression Protection

Workflow:
Before change -> Run eval suite -> Establish baseline
After change -> Run eval suite -> Compare to baseline
If drop > threshold -> Investigate before shipping

Thresholds by criticality:
- High-stakes (medical, financial): Any drop = block
- Normal (support, productivity): 5% drop = investigate
- Experimental (prototypes): 10% drop = investigate

## Framework Application

| Framework | Trace Access | Grader Integration |
|-----------|-------------|-------------------|
| OpenAI Agents SDK | Built-in tracing | Custom graders |
| Claude Agent SDK | Hooks for tracing | Custom graders |
| Google ADK | Evaluation module | Built-in graders |
| LangChain | LangSmith traces | LangSmith evals |
| Custom | Logging middleware | Custom graders |

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | What to Do Instead |
|-------------|--------------|-------------------|
| 1000+ test cases first | Quantity without quality | Start with 20 thoughtful cases |
| 1-5 scale ratings | LLMs poorly calibrated | Binary criteria summed |
| Ignoring traces | Miss root cause | Read intermediate outputs |
| End-to-end only | Too noisy for debugging | Add component-level evals |
| Synthetic test data | Misses real-world messiness | Use actual user queries |

---

*Skill Version: 1.0.0 | Created: Chapter 47 | Owner: [Your Name]*
```

## The Portable Thinking

The concepts you learned transfer across any agent framework because they address universal problems:

| Concept | Why It Transfers |
|---------|-----------------|
| Evals vs TDD | Agents reason probabilistically everywhere |
| Binary criteria | LLM calibration issues exist in all systems |
| Error analysis | Multi-component agents fail similarly across frameworks |
| Regression protection | Quality degradation happens regardless of SDK |
| Dataset categories | Typical/edge/error applies to any domain |

What does NOT transfer directly:

| Concept | Framework-Specific Adaptation |
|---------|-------------------------------|
| Trace access | Each SDK has different tracing APIs |
| Built-in graders | Google ADK has them; others don't |
| Dataset storage | Varies by infrastructure |
| CI/CD integration | Depends on deployment pipeline |

Your skill should contain the portable patterns. Framework-specific details get added when you apply the skill to a particular SDK.

## Exercise: Test Your Skill on a Third Agent

Your skill has now been validated on Customer Support. For your final exercise, test it on one more agent type to confirm the patterns truly generalize.

**Choose one:**

1. **Content Generation Agent**: Creates blog posts, social media content, marketing copy
2. **Code Review Agent**: Reviews pull requests, suggests improvements, catches bugs
3. **Data Analysis Agent**: Answers questions about datasets, creates visualizations, identifies trends

Using only your skill:

1. Design a 10-case eval dataset (5 typical, 3 edge, 2 error)
2. Write 5 binary criteria for a grader
3. Identify which component would be hardest to evaluate
4. Decide: E2E eval or component-level first? Why?

If you complete this exercise without returning to chapter content, your skill is production-ready.

## Try With AI

### Prompt 1: Test Your Skill on a New Agent Type

```
I'm validating that my agent-evals skill is portable. I just learned
evaluation methodology using a Task API agent. Now I need to apply it
to a completely different domain.

My new agent is: [describe an agent in your actual domain]

Using evaluation methodology (not any specific framework), help me:
1. Design a 10-case eval dataset with typical, edge, and error categories
2. Define 5 binary criteria for grading responses
3. Identify which component would be hardest to trace errors back to

I want to verify my evaluation thinking transfers, not learn new concepts.
```

**What you're learning:** Skill portability requires active testing. Your evaluation thinking should work in any domain because you learned patterns, not examples. AI helps you apply those patterns to verify they transfer.

### Prompt 2: Generate a New Domain's Eval Dataset

```
I have an agent that [describe your real agent]. I need to design an
evaluation dataset using the three-category approach:

- Typical (60%): Common cases
- Edge (25%): Unusual but valid
- Error (15%): Should fail gracefully

Generate 15 test cases for my agent following this structure. For each case:
1. Input: What the user says/does
2. Expected behavior: What the agent should do
3. Category: Typical, edge, or error
4. Why this category: Brief justification

Use realistic examples from my domain, not generic ones.
```

**What you're learning:** Dataset design transfers across domains when you use the category framework. The specific cases differ by domain, but the structure remains constant. AI helps you generate domain-specific cases using your portable framework.

### Prompt 3: Create a Grader for Different Criteria

```
I need to evaluate a [describe your agent type] using binary criteria.

The subjective quality I care about is: [describe what "good" means]

Help me:
1. Break this subjective quality into 5-7 binary yes/no criteria
2. For each criterion, suggest how to check it (string matching, keyword presence, LLM judge)
3. Identify which criteria need LLM-as-Judge vs can be checked with code

Remember: No 1-5 scales. Each criterion must be decidable as true/false.
```

**What you're learning:** The binary criteria pattern applies to any subjective quality you need to measure. Breaking "good" into checkable components is a skill that transfers across every agent you will ever build.

### Safety Note

Skills evolve through use. The version you finalize today is not the final version. As you apply this skill to more agents, you will encounter patterns not covered here. When that happens, update your skill. A living skill grows stronger with each use. A frozen skill becomes obsolete. Build the habit of returning to your skills and adding what you learn in practice.
