---
name: names-check
description: Analyze examples and mock data for name diversity, understanding the context and purpose before suggesting changes. Use when reviewing test data, documentation, or seed data.
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Names Check

Analyze files for name diversity in examples and mock data, with emphasis on understanding context and purpose.

## Philosophy

This is not about flagging every "John Smith". It's about asking:

> "When someone from Lagos, Tokyo, or São Paulo sees our examples, do they see themselves?"

Names in examples signal who you built your product for. If every example user is John, Jane, or Bob, you're implicitly saying "this is for Western users."

## Scope

The user may specify a file path, glob pattern, or directory. If not specified, ask what they'd like to check.

## Config Integration

Before starting, check for `.inclusion-config.md` in the project root.

If it exists:
1. **Read** scope decisions and acknowledged findings
2. **Skip** acknowledged findings (note them in output)
3. **Respect** priority settings (if names-check is deprioritized, mention it)
4. **Note** at the top of output: "Config loaded: .inclusion-config.md"

## Process

### 1. Read and Understand

First, **read the files** to understand:
- What kind of data is this? (test fixtures, seed data, documentation examples, UI mockups)
- What's the purpose? (unit tests, demo data, user-facing examples)
- How visible is this to end users?

### 2. Assess the Current State

Look at the names holistically:
- How many example names are there?
- What's the current diversity? (all Western? some variety? good mix?)
- Are names just placeholders, or do they appear in user-facing content?

### 3. Apply Context

Not all names need changing. Use judgment:

**Higher priority:**
- Documentation examples users will read
- Demo/seed data shown in screenshots or videos
- UI mockups and design files
- Marketing materials

**Lower priority:**
- Internal unit test fixtures (though diversity here catches bugs)
- Temporary development data
- Single throwaway examples

**Consider the full picture:**
- If you have 20 example users and 18 are Western names, that's a pattern
- If you have 3 test users and one is "John", that's less concerning
- The goal is diversity across the codebase, not eliminating Western names

### 4. Think About Name Handling

Diverse names also catch bugs:
- Names with apostrophes (O'Brien, N'Golo)
- Names with diacritics (José, Müller, Björk)
- Single names (Suharto, Madonna)
- Long names (Wolfeschlegelsteinhausenbergerdorff)
- Names with non-Latin characters (田中, Иванов, محمد)

If the code only uses "John Smith" in tests, you might miss these edge cases.

## Reference

For diverse name suggestions by region, see `references/diverse-names.md`. Use this for inspiration, not as a quota.

## Output Format

Keep it **compact**. Tables for findings, brief assessment, actionable next steps.

```markdown
## Names Analysis: [path]

[1-2 sentences: What is this? Current diversity state? Main pattern?]

**Diversity:** Poor / Limited / Moderate / Good

---

### High Priority (user-facing)

| Location | Name | Suggested Alternatives |
|----------|------|------------------------|
| docs.md:17 | John Smith | Amara Okafor, Wei Chen, Priya Sharma |
| seed.ts:5 | Jane Doe | Yuki Tanaka, Fatima Hassan |

### Worth Considering (internal)

| Location | Name | Benefit |
|----------|------|---------|
| test.ts:12 | Bob Johnson | Tests apostrophe handling: O'Brien |
| fixtures.json:8 | user1 | Tests diacritics: José, Müller |

### Edge Cases to Add

Your test data should include names that catch bugs:
- [ ] Apostrophes (O'Brien, N'Golo)
- [ ] Diacritics (José, Müller, Björk)
- [ ] Single names (Suharto)
- [ ] Long names (30+ chars)

---

### Summary

**12 names** found, all Western. Priority: user-facing docs and seed data.

Run `/inclusive-names` to generate diverse alternatives.
```

## Output Guidelines

- **Use tables** for findings—location, current name, suggestion
- **Diversity rating upfront**—Poor/Limited/Moderate/Good
- **Separate user-facing from internal**—different priorities
- **Edge cases as checklist**—quick reference, not paragraphs
- **Summary as TL;DR**—count, assessment, next action

## What Makes This Different From a Linter

A linter would flag every "John". You should:

1. **Assess the whole picture** - One John among diverse names is fine
2. **Prioritize by visibility** - User-facing examples matter more
3. **Consider the purpose** - Is diversity here about inclusion or bug-catching?
4. **Suggest contextually** - A legal document example might use different names than a social app

Your value is seeing the **pattern across the codebase**, not individual strings.
