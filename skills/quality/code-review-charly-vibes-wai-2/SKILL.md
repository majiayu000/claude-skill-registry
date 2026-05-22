---
name: code-review
description: Multi-pass code review using Rule of 5 principle
disable-model-invocation: true
---

# Iterative Code Review with Rule of 5

I need you to review this code using the Rule of 5 - five stages of iterative refinement.

CODE TO REVIEW:
[paste your code or specify file path]

PHILOSOPHY: "Breadth-first exploration, then editorial passes"

STAGE 1: DRAFT - Get the shape right
Question: Is the overall approach sound?
Focus:
- Don't aim for perfection
- Review overall structure and approach
- Identify major architectural issues
- Get the "shape" right before refining details
- Is this solving the right problem?

Output: High-level assessment, major structural issues

STAGE 2: CORRECTNESS - Is the logic sound?
Question: Are there errors, bugs, or logical flaws?
Focus:
- Fix errors and bugs identified in Stage 1
- Verify logical correctness
- Check algorithms and data structures
- Ensure functions do what they claim
- Identify off-by-one errors, wrong operators, etc.

Output: List of correctness issues with locations

STAGE 3: CLARITY - Can someone else understand this?
Question: Is the code comprehensible?
Focus:
- Improve readability based on Stage 2 fixes
- Remove or explain technical jargon
- Clarify variable and function names
- Improve code organization
- Add comments where intent isn't obvious

Output: Clarity improvements and naming suggestions

STAGE 4: EDGE CASES - What could go wrong?
Question: Are boundary conditions handled?
Focus:
- Identify gaps from previous stages
- Handle unusual scenarios
- Check boundary conditions (null, empty, max values)
- Error handling for external dependencies
- Input validation gaps

Output: Edge cases and error handling issues

STAGE 5: EXCELLENCE - Ready to ship?
Question: Would you be proud to ship this?
Focus:
- Final polish based on all previous stages
- Production quality check
- Performance considerations
- Documentation completeness
- Overall code quality

Output: Final recommendations for production readiness

CONVERGENCE CHECK:
After each stage (starting with Stage 2), report:
1. Number of new CRITICAL issues found
2. Number of new issues vs previous stage
3. Convergence status:
   - CONVERGED: No new CRITICAL, <10% new issues
   - CONTINUE: Proceed to next stage
   - NEEDS_HUMAN: Found blocking issues requiring judgment

FINAL REPORT:
- Total issues by severity
- Top 3 most critical findings
- Recommended next actions
- Production readiness assessment
