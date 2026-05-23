---
name: writing-legal
description: This skill should be used when the user asks to "write a law review article", "draft a legal paper", "edit legal writing", "review my legal article", "write for a journal", "format footnotes", or needs guidance on academic legal writing. Based on Volokh's "Academic Legal Writing" with law-review-specific structure and evidence handling.
---

# Academic Legal Writing

Style guide for law review articles, seminar papers, and legal scholarship based on Eugene Volokh's *Academic Legal Writing*.

## When to Use

Invoke this skill for:
- Law review articles and student notes
- Seminar papers and legal scholarship
- Academic legal writing with footnotes
- Editing legal prose for structure and argument

**For general writing**: Use `/writing` skill (Strunk & White)
**For economics/finance**: Use `/writing-econ` skill (McCloskey)

## Enforcement

### IRON LAW #1: NO CLAIM WITHOUT CONFRONTING COUNTERARGUMENTS

If your draft makes a prescriptive claim but doesn't address obvious objections, DELETE the section and START OVER. Legal scholarship requires anticipating and answering counterarguments, not ignoring them.

### IRON LAW #2: NO SECONDARY SOURCE CITATIONS FOR PRIMARY SOURCES

If you cite a case/statute/historical fact via an intermediate source (law review, treatise), DELETE the citation and READ THE ORIGINAL. Even Supreme Court opinions misstate precedents.

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "This article discusses..." | Bores reader instantly | START with concrete problem or controversy |
| "Table-of-contents paragraph helps" | Readers skip it | INTEGRATE roadmap into intro |
| "Background section comes first" | Not before establishing relevance | SHOW problem first, background second |
| "Case-by-case summary is thorough" | Tedious and unhelpful | SYNTHESIZE: "Courts hold X except Y" |
| "Counterargument would hurt my claim" | Ignoring it hurts worse | CONFRONT and refine claim |
| "Treatise summary is good enough" | Treatises have errors | READ original cases |
| "Arguably" makes my point | Acknowledges controversy without arguing | MAKE the argument explicitly |
| "This metaphor is clear" | Metaphors hide incomplete logic | UNPACK: what's the actual argument? |

### Red Flags - STOP Immediately If You Think:

- "Let me write standard intro" → NO. Find concrete problem first.
- "I'll address objections later" → NO. Confront counterarguments NOW.
- "This treatise explains the case" → NO. Read the original case.
- "Background section needs more" → NO. Only include what proves claim.

### Delete & Restart Pattern

**When to delete and restart:**

1. **Intro starts with "This article discusses"** → Delete, start with concrete problem
2. **Background exceeds proof section** → Delete excessive background
3. **Claim made without addressing objections** → Delete section, add counterargument confrontation
4. **Citation chain to primary source** → Delete citation, read and cite original
5. **Unpacked metaphor used as argument** → Delete, write actual logical argument

**How to restart:**

```
Old: "This article discusses privacy concerns in Fourth Amendment doctrine..."
New: "When police drones photograph backyards, does the Fourth Amendment require a warrant?
      Courts disagree, but three features of aerial surveillance suggest yes."
```

Start with CONCRETE QUESTION that matters, not abstract topic description.

## Law Review Article Structure

### Introduction

The introduction serves three functions:
1. Persuade readers to keep reading
2. Summarize the article for those who won't read it
3. Frame how readers interpret what follows

**Requirements:**
- Show the problem concretely with specific examples or hypotheticals
- State the claim clearly—what does the article contribute?
- Integrate the roadmap into the introduction, not as a separate paragraph
- Hook the reader: concrete question, engaging story, controversy, or argument to rebut

**Anti-patterns:**
- Starting with "This article discusses..."
- Separate table-of-contents paragraph (readers skip it)
- Historical background before establishing relevance
- Vague generalities about the importance of the topic

### Background Section

Synthesize precedents; do not summarize each case sequentially. Focus only on facts and rules necessary for the argument.

| Problem | Solution |
|---------|----------|
| Summarizing each case | Synthesize: "Courts generally hold X, except when Y" |
| Mini-treatise on the area | Only what's needed for the claim |
| 80% background, 20% claim | Balance must favor the original contribution |

### Proof of the Claim

For prescriptive claims: Show the proposal is both doctrinally sound AND good policy.

**Use a test suite:** Apply the proposal to concrete scenarios (easy cases, hard cases, edge cases) to demonstrate it works.

**Confront counterarguments:**
- Turn problems to advantage: refine the claim, acknowledge uncertainty
- Stay on offense—address objections without becoming defensive
- Acknowledge costs honestly; readers respect candor

**Connect to broader issues:**
- How does the claim relate to parallel debates?
- What subsidiary discoveries emerged?
- What questions remain for future research?

### Conclusion

Keep conclusions brief. The real work is rewriting the introduction after the draft is complete, ensuring it accurately reflects the article's contributions.

## Legal Argument Problems

Common logical problems in legal writing (see `references/volokh-distilled.md` for detailed examples):

| Problem | Issue |
|---------|-------|
| Categorical assertions | "Always" and "never" invite counterexamples |
| Unpacked metaphors | "Slippery slope" and "chilling effect" hide incomplete arguments |
| Missing logical pieces | Syllogisms that skip steps (subject to scrutiny ≠ fails scrutiny) |
| Universal criticisms | "Chilling effect" applies to most laws—explain why *this* one matters |
| Undefined abstractions | "Privacy," "paternalism," "democratic legitimacy" need definitions |
| "Arguably" as argument | Acknowledges controversy but doesn't make the case |

## Evidence and Citation

### Read Original Sources

Never rely on intermediate sources for cases, statutes, or historical facts. Even Supreme Court opinions misstate precedents.

| Source Type | Rule |
|-------------|------|
| Cases/statutes | Read the original; don't trust treatises or other cases |
| Historical facts | Go to history books, not law review articles citing them |
| Scientific studies | Read the study, not the article summarizing it |
| Newspapers | Unreliable; track down underlying documents |
| Wikipedia | Use to find sources, but cite originals |

### Be Precise with Terms

Avoid false synonyms: "murder" ≠ "homicide" ≠ "killing"; "foreign-born" ≠ "noncitizen"; "children" is ambiguous (0-14? 0-17? 0-24?).

Include necessary qualifiers: "*falsely* shouting fire" is quite different from "shouting fire."

### Be Explicit About Assumptions

Make clear when inferring:
- From correlation to causation
- From one time/place to another
- From one variable to another (arrest rate ≠ crime rate)

Acknowledge the inference and defend it; don't hide it.

### Handle Surveys Carefully

Surveys measure only what respondents said in response to specific questions. Valid surveys require:
- Random sampling (not self-selected, not convenience samples)
- High response rates (70%+)
- Sufficient sample size (1000+ for ±3% margin)
- Unambiguous questions

"Online survey" and "Internet poll" are almost sure signs of invalidity.

## Rhetoric and Tone

| Principle | Application |
|-----------|-------------|
| Understate criticism | "Mistaken" not "idiotic"—overstating raises the burden of proof |
| Attack arguments, not people | "This argument fails" not "Volokh is wrong" |
| Avoid caricature | Quote adherents, not critics, when explaining a position |

See `references/volokh-distilled.md` for extended discussion of rhetorical problems.

## Quick Reference

| Problem | Solution |
|---------|----------|
| "This article discusses X" | Hook with concrete problem |
| Case-by-case summaries | Synthesize precedents |
| Undefended metaphors | Unpack the concrete mechanism |
| "Arguably" / "raises concerns" | Give the actual argument |
| Relying on intermediate source | Read original case/study |
| "Many children" | Specify: "111 children age 0-17" |
| "Correlation shows causation" | Explain why inference is valid |
| "Volokh's argument is idiotic" | "This argument seems unsound" |

## Progressive Disclosure

For comprehensive guidance, consult:

### Reference File

- **`references/volokh-distilled.md`** - Extended Volokh guidance covering:
  - Full logical problems taxonomy
  - Word and phrase problems to avoid
  - Extended evidence handling
  - Survey analysis methodology
  - Editing principles and exercises

### When to Load Reference

Load the full reference when:
- Encountering specific evidence evaluation questions
- Needing detailed survey methodology guidance
- Working on substantial manuscript revision
- Checking specific word choice or usage questions

## Integration

After completing any legal writing task, invoke `/ai-anti-patterns` to check for AI writing indicators. The `/writing` skill covers general prose principles (active voice, omit needless words) that complement this skill.
