---
name: 053-design-simple-rules
description: Use when Java design, refactoring, or implementation tradeoffs should be evaluated with Kent Beck's simple design rules, including passes the tests, reveals intention, has no duplication, and has the fewest elements. This should trigger for requests such as Apply simple design rules; Review this design with Beck's rules; Choose between these refactoring options; Keep this Java design simple. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# Simple Design Rules

Guide Java developers through Kent Beck's simple design rules when evaluating design and refactoring choices. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Using tests as the first correctness boundary before design cleanup
- Revealing intention and maximizing clarity before abstraction pressure
- Reducing duplication without hiding domain meaning or worsening readability
- Treating fewer elements as the final simplification pressure after correctness, clarity, and duplication
- Comparing Java design and refactoring options with the ordered rules
- Reporting the chosen option, tradeoffs, validation signal, and remaining risk

## Constraints

Apply simple design rules in priority order, and do not optimize later rules by weakening earlier rules.

- **MUST** read `references/053-design-simple-rules.md` before applying the rules
- **MUST** evaluate the rules in this order: passes the tests, reveals intention, has no duplication, has the fewest elements
- **MUST** treat passing tests as the correctness boundary before design cleanup
- **MUST** prefer clear intention over abstraction for its own sake
- **MUST** reduce duplication only when the result preserves or improves clarity
- **MUST** consider fewer elements only after correctness, clarity, and duplication have been addressed

## When to use this skill

- Apply simple design rules
- Use Beck's simple design rules
- Review this design with simple design rules
- Choose between these refactoring options
- Keep this Java design simple
- Does this design pass the simple design rules?

## Workflow

1. **Anchor Correctness**

Read `references/053-design-simple-rules.md`, then identify the behavior under discussion and the tests, characterization checks, build checks, or manual evidence that define whether the code works.

2. **Reveal Intention**

Evaluate whether names, types, responsibilities, control flow, API shape, and test descriptions make the domain decision clear to a future maintainer.

3. **Reduce Duplication Carefully**

Find repeated knowledge, policy, mappings, validation, queries, or workflow decisions. Remove duplication only when the abstraction keeps the intent easier to understand.

4. **Minimize Elements Last**

After correctness, clarity, and duplication are handled, remove unnecessary classes, methods, parameters, branches, layers, configuration, or indirection that no longer pay for themselves.

5. **Compare Options and Report**

Compare available design or refactoring options against the ordered rules. Recommend the option that satisfies the earlier rules best, describe rejected tradeoffs, and name the verification signal.

## Reference

For detailed guidance, examples, and constraints, see [references/053-design-simple-rules.md](references/053-design-simple-rules.md).
