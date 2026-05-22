---
sidebar_position: 6
title: "Build Script-Execution Skill"
description: "Create a skill that orchestrates the write-execute-analyze loop to autonomously process data. Learn to implement error recovery, iterate toward robust solutions, and test your skill across diverse input scenarios. This is where specification-driven development meets real problem-solving."
keywords: ["script execution skill", "write-execute-analyze implementation", "error recovery automation", "iterative refinement", "data processing skill", "skill testing", "convergence detection", "CSV analysis", "edge case handling"]
chapter: 39
lesson: 6
duration_minutes: 50

# HIDDEN SKILLS METADATA
skills:
  - name: "Script-Execution Skill Implementation"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can build a working skill that writes Python code from specifications, executes it, detects errors, generates fixes, and iterates until success criteria are met. Skill demonstrates error recovery handling syntax and runtime failures."

  - name: "Error Detection and Automated Recovery"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can parse error messages from code execution, categorize error types (syntax vs runtime), and prompt AI to generate corrected code. Student validates fixes against original specification."

  - name: "Convergence Validation and Iteration Control"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Analyze"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can define and implement convergence criteria (specification compliance, error-free execution, edge case handling) and iteration limits (max retries, timeouts) that prevent infinite loops while allowing sufficient attempts."

learning_objectives:
  - objective: "Write skill specification for script execution task including success criteria, edge cases, and convergence conditions"
    proficiency_level: "B2"
    bloom_level: "Create"
    assessment_method: "Students define complete skill spec with data inputs, transformation logic, success criteria, and at least 3 edge cases"

  - objective: "Implement write-execute-analyze loop with error detection and recovery"
    proficiency_level: "B2"
    bloom_level: "Create"
    assessment_method: "Students build working skill that generates code, executes it, catches errors, generates fixes, and validates results"

  - objective: "Design and test error recovery for syntax errors, runtime errors, and timeout scenarios"
    proficiency_level: "B2"
    bloom_level: "Apply"
    assessment_method: "Students test skill with intentional failures (malformed data, missing columns, timeout conditions) and validate recovery behavior"

  - objective: "Validate skill convergence through acceptance testing across clean, malformed, and edge case data"
    proficiency_level: "B2"
    bloom_level: "Analyze"
    assessment_method: "Students run skill against 5+ test scenarios and document pass/fail results with convergence evidence"

cognitive_load:
  new_concepts: 9
  assessment: "9 concepts (skill spec for script execution, script generation prompting, execution environment setup, error detection/parsing, iterative fix generation, iteration limits, output validation, state management, logging) within B2 limit (7-10 concepts) ✓"

differentiation:
  extension_for_advanced: "Add state checkpointing: If execution fails midway, can the skill resume from the last successful iteration rather than starting from scratch? Implement persistence layer and recovery mechanism. Also explore: how would you handle timeout scenarios where code starts but takes too long? Design a pause-analyze-resume strategy."
  remedial_for_struggling: "Start with a simpler specification (CSV row counting instead of complex analysis). Use the provided CSV template and walk through one complete iteration manually with AI. Focus on understanding the error messages first—what does each type tell you? Then practice generating one fix before building the full loop."
---

# Build Script-Execution Skill

You've learned the pattern (Lesson 5): write code from specification → execute it → analyze errors → iterate. Now you're going to build a skill that orchestrates this loop autonomously.

But here's what makes this different from following a tutorial: You'll specify what problem you're solving FIRST, then let AI help you build the skill while you validate each decision. You're not just learning a pattern—you're learning to think about error recovery, convergence criteria, and edge cases the way production systems demand.

## Step 1: Write Your Specification

Before touching any skill code, write a specification for the problem you're solving. You'll use a CSV data processing task because it's concrete and has natural edge cases.

Choose one of these:
- **CSV Analysis**: Analyze customer or sales data for patterns
- **CSV Transformation**: Clean and restructure messy CSV data
- **CSV Aggregation**: Group data by dimensions and calculate metrics

Or define your own data processing task.

### Your Specification

Write this to a file (skill-spec.md) or document:

```markdown
# CSV Analysis Skill Specification

## Intent
[What does this skill do? Be specific about the business problem it solves]

## Input
- data_file: [type and format, e.g., "CSV with columns: customer_id, purchase_date, amount"]
- parameters: [what configuration does skill accept?]

## Output
- format: [JSON, CSV, report?]
- required_fields: [exact fields that must be in output]
- validation_rules: [how to verify output is correct]

## Success Criteria
- All data processed without loss
- Output format exactly matches specification
- Edge cases handled gracefully (malformed rows, missing values, etc.)
- Execution completes within 30 seconds

## Edge Cases to Handle
- [Case 1: e.g., "Empty CSV file"]
- [Case 2: e.g., "Missing column header"]
- [Case 3: e.g., "Non-numeric values in amount field"]
```

**Key principle**: Your specification must be complete enough that AI can generate correct code without additional context. If your spec is vague, the generated code will be equally vague.

## Step 2: Design Your Skill's Persona and Questions

Before building, define how your skill thinks about this problem.

```yaml
# Skill Persona
persona: |
  You are a data orchestrator: your role is to write Python scripts that
  process data robustly. When you encounter errors, you read the error message
  carefully, understand why the code failed, and generate corrected code.
  You validate results against the specification. You handle edge cases explicitly
  rather than hoping they don't occur.

questions:
  - "What does the data structure look like? (columns, data types, edge cases)"
  - "What transformation or analysis does the specification require?"
  - "What output format must the code produce?"
  - "What validation proves the output is correct?"
  - "What edge cases are most likely to occur in real data?"

principles:
  - "Validate data before processing: Check columns exist, types are correct"
  - "Fail explicitly: Raise errors with clear messages rather than silently producing wrong results"
  - "Test assumptions: Don't assume column names; inspect actual data first"
  - "Document the transformation: Add comments explaining the logic"
```

## Step 3: Build the Skill Core with AI Collaboration

Now you're going to build this skill with AI. You'll test code, discover error patterns you hadn't anticipated, and learn what your actual data requires. As you iterate, the skill improves—not because you're following a formula, but because specification-driven feedback drives real improvements.

### Part A: Generate Initial Implementation

**Your prompt to AI:**

```
I'm building a skill that processes CSV data. Here's my specification:

[PASTE YOUR SPEC]

Generate a Python skill implementation that:
1. Reads the CSV file
2. Validates the data structure (check columns, types)
3. Performs the required transformation/analysis
4. Returns results in the specified format
5. Includes error handling for common CSV issues

The code should be production-quality (defensive, not assuming data format).
```

AI will generate code. Study it. Does it match your specification?

**Critical evaluation**:
- Does the code check for expected columns before using them?
- Does it handle missing/null values?
- Does it validate the output format matches your spec?

**Document what you notice**:
```
Things I observe:
- [Good pattern in the approach]
- [Assumption that might not hold]
- [Edge case not addressed yet]
```

Use these observations to guide your feedback to AI when iterating.

### Part B: Test with Real Data

Get or create sample CSV data that matches your specification's expected format.

**Run the generated code**:

```python
# Save AI-generated code to analysis.py
# Create test_data.csv with sample data
# Run it

python analysis.py test_data.csv
```

**What happens**?
- ✓ Success: Output matches specification → Great! Move to Part C
- ✗ Syntax Error: Code won't even parse
- ✗ Runtime Error: Code runs but crashes (KeyError, TypeError, etc.)
- ✗ Logic Error: Code runs, output is wrong or incomplete

### Part C: Recover from Errors

This is where error recovery becomes visible.

**If you got a syntax error:**

```
Show AI the error:
"Here's my code:
[show problematic section]

Error: [paste error message]

What's wrong and how do I fix it?"
```

AI explains and provides corrected code.

**If you got a runtime error:**

```
Show AI the error:
"The code crashed with:
[error message and traceback]

What does this error mean?
What assumption did the code make that's wrong?
How should I fix it to handle real data?"
```

**If output is wrong/incomplete:**

```
"My spec requires [required output].
My code produces [what it actually produces].

What's missing? How should the code be changed to match the spec?"
```

### Part D: Iterate Until Convergence

Keep improving until:

✓ Code runs without errors
✓ Output matches your specification exactly
✓ Edge cases are handled (test with malformed data)
✓ Execution completes within time limit

**Test with multiple scenarios:**

```python
# Test 1: Clean data (happy path)
python analysis.py clean_data.csv

# Test 2: Missing columns
python analysis.py missing_columns.csv

# Test 3: Non-numeric values where numeric expected
python analysis.py malformed_data.csv

# Test 4: Empty file
python analysis.py empty.csv

# Test 5: Large file (check performance)
python analysis.py large_data.csv
```

For each test, document:
- Did it run without error? (Yes/No)
- Does output match spec format? (Yes/No)
- Are edge cases handled gracefully? (Yes/No)

## Step 4: Build the Iteration Loop (The Skill Automating the Pattern)

Now that you've manually gone through the loop, you're going to build a skill that does this automatically.

**Your skill needs these components:**

```python
def build_analysis_skill():
    """
    The full script-execution skill that orchestrates:
    1. Generate code from spec
    2. Execute the code
    3. Check for errors
    4. Generate fixes if needed
    5. Iterate until convergence
    """

    # Component 1: Code Generation
    def generate_code(specification: str) -> str:
        """Generate Python code from specification using AI"""
        # Prompt AI with: "Given this spec: [spec],
        # write complete Python code that implements it"
        # Return the generated code
        pass

    # Component 2: Code Execution
    def execute_code(code: str, input_file: str, timeout: int = 30) -> tuple[bool, str, str]:
        """Execute code, return (success, output, error_message)"""
        # Run code with subprocess
        # Capture stdout, stderr
        # Return results with timeout protection
        pass

    # Component 3: Error Analysis
    def analyze_error(error_message: str, code: str) -> str:
        """Understand what went wrong"""
        # Parse error type (SyntaxError, RuntimeError, etc.)
        # Extract the problematic line
        # Return clear analysis of the issue
        pass

    # Component 4: Fix Generation
    def generate_fix(error_analysis: str, code: str, spec: str) -> str:
        """Generate corrected code"""
        # Prompt AI: "This code failed with: [error]
        # Here's the problem: [analysis]
        # The spec is: [spec]
        # Generate corrected code that fixes this"
        pass

    # Component 5: Convergence Check
    def check_convergence(output: str, spec: dict) -> bool:
        """Does output satisfy the specification?"""
        # Validate: all required fields present
        # Validate: output format correct
        # Validate: no error messages in output
        # Return True if spec is satisfied
        pass

    # Component 6: Main Iteration Loop
    def execute_skill(specification: str, input_file: str) -> str:
        """Main skill that orchestrates everything"""
        max_iterations = 5
        iteration = 0
        code = None

        while iteration < max_iterations:
            iteration += 1

            if iteration == 1:
                # First iteration: generate from spec
                code = generate_code(specification)

            # Execute the code
            success, output, error = execute_code(code, input_file)

            if success and check_convergence(output, spec):
                # ✓ Converged! Specification is satisfied
                return output

            if not success:
                # ✗ Error occurred
                analysis = analyze_error(error, code)
                code = generate_fix(analysis, code, specification)
                # Loop continues, retry with fixed code

            elif not check_convergence(output, spec):
                # ✗ Output doesn't match spec
                fix_request = f"Output is incomplete: {output}.
                               Required by spec: {spec}. Generate code that adds missing parts."
                code = generate_fix(fix_request, code, specification)
                # Loop continues, retry with improved code

        # If we get here, max iterations reached without converging
        raise RuntimeError(f"Failed to converge after {max_iterations} iterations")
```

## Step 5: Implementation Guidance with AI

You're going to build this skill using AI, but testing and validating each component.

### Get AI Help Building the Iteration Loop

```
I'm building a Python skill that generates code, executes it, and iterates
until a specification is satisfied.

Here's my specification:
[PASTE YOUR SPEC]

Here's my first attempt at code generation and execution:
[PASTE YOUR MANUAL CODE FROM STEP 3-4]

Now I need to build an automated loop that:
1. Generates code once (given spec)
2. Executes code (capture output/errors, 30-second timeout)
3. If error: analyze error, prompt you to generate fixed code
4. If output doesn't match spec: prompt you to improve code
5. Check convergence (spec is satisfied) → Stop
6. Repeat until convergence or 5 iterations max

Show me how to structure this as a Python class/functions.
Include error handling, timeout protection, and convergence checking.
```

### Build Convergence Validation

This is critical. Your skill must STOP when the specification is satisfied.

```python
def convergence_check(output: str, specification: dict) -> dict:
    """
    Validate whether output satisfies specification.
    Returns: {
        'converged': bool,
        'missing': [list of unsatisfied requirements],
        'issues': [any problems found]
    }
    """
    results = {
        'converged': True,
        'missing': [],
        'issues': []
    }

    # Check all required fields are present
    for field in specification.get('output', {}).get('required_fields', []):
        if field not in output:
            results['missing'].append(f"Field missing: {field}")
            results['converged'] = False

    # Check output format (if JSON specified)
    if specification.get('output', {}).get('format') == 'JSON':
        try:
            json.loads(output)
        except:
            results['issues'].append("Output is not valid JSON")
            results['converged'] = False

    # Add domain-specific validation based on your spec
    # Example: if analyzing customers, verify segments exist
    if 'required_segments' in specification:
        for segment in specification['required_segments']:
            if segment not in output:
                results['missing'].append(f"Segment missing: {segment}")
                results['converged'] = False

    return results
```

### Add Timeout and Resource Protection

```python
import subprocess
import signal

def execute_code_safely(code: str, input_file: str, timeout: int = 30) -> tuple[bool, str, str]:
    """
    Execute Python code with timeout and error capture.
    Returns: (success: bool, output: str, error: str)
    """
    # Write code to temporary file
    with open('_temp_analysis.py', 'w') as f:
        f.write(code)

    try:
        # Run with timeout
        result = subprocess.run(
            ['python', '_temp_analysis.py', input_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            # Success
            return (True, result.stdout, '')
        else:
            # Execution failed
            return (False, result.stdout, result.stderr)

    except subprocess.TimeoutExpired:
        return (False, '', 'TimeoutError: Execution exceeded 30 seconds')
    except Exception as e:
        return (False, '', f'ExecutionError: {str(e)}')
```

## Step 6: Test Your Skill Against Edge Cases

Your skill should handle:

### Test 1: Clean Data (Happy Path)

```python
skill = ScriptExecutionSkill(
    specification=your_spec,
    input_file='clean_data.csv'
)

result = skill.execute()
assert result is not None
assert 'error' not in result.lower()
```

**Expected**: Succeeds on first iteration

### Test 2: Malformed Data (Edge Case)

```python
# CSV with missing columns, non-numeric values, etc.
result = skill.execute(input_file='malformed_data.csv')

# Skill should detect error, fix code, retry
assert 'error' not in result.lower()  # After recovery, still valid
```

**Expected**: Skill generates fix after detecting error

### Test 3: Empty File (Non-Recoverable)

```python
result = skill.execute(input_file='empty.csv')

# This SHOULD fail (non-recoverable)
assert result is None or 'error' in result.lower()
```

**Expected**: Skill recognizes this is non-recoverable, stops gracefully

### Test 4: Timeout Scenario

```python
# Spec with large data processing that might timeout
result = skill.execute(input_file='large_data.csv', timeout=5)

# Skill should timeout gracefully, not hang
assert 'timeout' in result.lower() or result is None
```

**Expected**: Skill times out, reports clearly

## Step 7: Document Your Skill

Real skills are documented for others to use.

```markdown
# CSV Analysis Skill

## Purpose
[What problem does this solve?]

## Usage
```python
from my_skill import ScriptExecutionSkill

skill = ScriptExecutionSkill(
    specification={
        'input': ['customers.csv'],
        'output': {'format': 'JSON', 'required_fields': [...]},
        'success_criteria': [...]
    },
    input_file='customers.csv'
)

result = skill.execute()
print(result)
```

## How It Works
1. Specification defines what code must do
2. Skill generates Python code from spec
3. Code executes against input file
4. Errors trigger automatic fix generation
5. Iteration continues until spec is satisfied or max retries reached

## Success Metrics
- Execution time: < 30 seconds
- Convergence rate: 95%+ (passes with clean data)
- Edge case handling: Gracefully recovers or fails clearly

## Known Limitations
- [What doesn't it handle?]
- [When should you use something else?]
```

---

## Try With AI

Now you'll refine your skill with AI collaboration, focused on error recovery and robustness.

### Prompt 1: Design Error Recovery Patterns

```
I've built a skill that generates Python code from specifications and
executes it. It encounters three types of errors:

1. Syntax errors (code won't parse)
2. Runtime errors (code crashes during execution)
3. Logic errors (code runs but output is wrong)

For each error type, help me design the recovery strategy:

**Syntax errors**:
- How should I prompt you to generate fixed code?
- What context should I provide?

**Runtime errors**:
- How should I parse the error message?
- What information helps you generate a better fix?

**Logic errors**:
- How do I detect these (they don't produce error messages)?
- How should I describe the problem to you?

Show me the exact prompts I should use for each type.
```

**What you're learning**: How to design prompts that help AI generate fixes, not just resuggest the same broken code.

### Prompt 2: Implement Convergence Testing

```
My specification requires these success criteria:
[PASTE YOUR CRITERIA FROM YOUR SPEC]

I need a function that validates whether code output satisfies these criteria.

For each criterion, what should the validation check?
- How do I verify the output format is correct?
- How do I verify all required fields are present?
- How do I detect if the output is incomplete or wrong?

Show me a Python function that validates all criteria and returns
which ones passed, which ones failed, and what's missing.
```

**What you're learning**: How to translate specification requirements into automated validation that tells you exactly when to stop iterating.

### Prompt 3: Test Your Skill with Intentional Failures

```
I want to test my skill's error recovery. Help me design test cases:

**Test Case 1: Missing column**
- Create CSV data where a required column is missing
- Show me what error the generated code will produce
- What should my skill do to recover?

**Test Case 2: Wrong data type**
- Create data where a numeric column contains text
- Show the error this produces
- How should the skill fix this?

**Test Case 3: Timeout scenario**
- What operation would cause a timeout?
- How should my skill handle timeouts gracefully?

For each test case, show me:
1. The test data
2. The error produced
3. How my skill should recover
```

**What you're learning**: Testing is not about success cases—it's about understanding how your skill behaves when things break.

### Prompt 4: Validate Convergence Against Diverse Inputs

```
My skill has processed the following test scenarios:

**Test 1 - Clean data**: PASSED
**Test 2 - Missing column**: RECOVERED (3 iterations)
**Test 3 - Empty file**: FAILED (non-recoverable)
**Test 4 - Malformed values**: RECOVERED (2 iterations)

Based on these results:
- Is my skill ready for production?
- What patterns suggest robustness?
- What edge cases might still break it?
- What should I test next?

Help me evaluate the skill's readiness.
```

**What you're learning**: Testing isn't a binary pass/fail. It's about understanding your skill's behavior patterns and building confidence in its robustness.

---

## Success Criteria

Your skill is complete when:

✓ **Specification is clear and complete** — AI can generate code from it without asking questions
✓ **Code executes successfully on clean data** — Happy path works
✓ **Error recovery works** — Syntax and runtime errors trigger fixes
✓ **Convergence is detected** — Skill stops when spec is satisfied
✓ **Edge cases are handled** — Tested with malformed, empty, large data
✓ **Iteration limits work** — Skill stops after 5 attempts or timeout
✓ **Skill is documented** — Someone else could use it

Your skill will become a reusable component in Lesson 7 (orchestration) when you combine it with MCP-wrapping skills to create complete workflows.

---

**Takeaway**: You didn't just learn the write-execute-analyze loop—you built a skill that automates it. You discovered that error recovery isn't magic; it's specification clarity + intelligent prompting + convergence validation. In Lesson 7, you'll orchestrate this skill with MCP-wrapping skills to build complex workflows that combine code execution with external tools.
