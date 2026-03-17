---
name: Debugging Expert
description: Systematic troubleshooting using the Scientific Method (Observe, Hypothesize, Experiment, Fix).
metadata:
  labels: [debugging, troubleshooting, bug-fixing, root-cause]
  triggers:
    keywords: [debug, fix bug, crash, error, exception, troubleshooting]
---

# Debugging Expert

## **Priority: P1 (OPERATIONAL)**

Systematic, evidence-based troubleshooting. Do not guess; prove.

## 🔬 The Scientific Method

1. **OBSERVE**: Gather data. What exactly is happening?
    - Logs, Stack Traces, Screenshots, Steps to Reproduce.
2. **HYPOTHESIZE**: Formulate a theory. "I think X is causing Y because Z."
3. **EXPERIMENT**: Test the theory.
    - Create a reproduction case.
    - Change _one variable at a time_ to validate the hypothesis.
4. **FIX**: Implement the solution once the root cause is proven.
5. **VERIFY**: Ensure the fix works and doesn't introduce regressions.

## 🚫 Anti-Patterns

- **Shotgun Debugging**: Randomly changing things hoping it works.
- **Console Log Spam**: Leaving `print`/`console.log` in production code.
- **Fixing Symptoms**: masking the error (e.g., `try-catch` without handling) instead of fixing the root cause.

## 🛠 Best Practices

- **Diff Diagnosis**: What changed since it last worked?
- **Minimal Repro**: Create the smallest possible code snippet that reproduces the issue.
- **Rubber Ducking**: Explain the code line-by-line to an inanimate object (or the agent).
- **Binary Search**: Comment out half the code to isolate the failing section.

## 📚 References

- [Bug Report Template](references/bug-report-template.md)
