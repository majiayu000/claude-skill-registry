---
name: 'Address CodeRabbit Review'
description: 'Triage and address CodeRabbit automated review comments on a pull request.'
---

1. **Read comments**: Use `gh api repos/carrot-foundation/methodology-rules/pulls/<PR_NUMBER>/comments` to fetch all review comments. Identify which ones are from CodeRabbit.

2. **Triage each comment** into one of three categories:
   - **Valid issue**: A real bug, missing validation, incorrect logic, or meaningful improvement
   - **False positive**: The tool misunderstood the code or the suggestion does not apply
   - **Style preference**: A subjective suggestion that does not affect correctness

3. **Fix valid issues**:
   - Implement the fix following project conventions
   - If the suggestion is directionally correct but the specific fix is wrong, implement the right fix instead
   - Group related fixes into a single commit

4. **Dismiss false positives**: Leave a brief, respectful reply explaining why the suggestion does not apply. Be specific — reference the actual behavior or constraint that makes the suggestion unnecessary.

5. **Handle style preferences**: Apply if they align with project conventions. Skip if they contradict existing patterns or add no value.

6. **Run quality checks** after all fixes:
   ```bash
   pnpm lint:affected
   pnpm ts:affected
   pnpm test:affected
   ```

7. **Push fixes**: Commit with a message like `fix(shared): address CR feedback on schema validation` and push to the PR branch.
