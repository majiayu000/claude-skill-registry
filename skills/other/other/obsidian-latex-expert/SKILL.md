---
name: obsidian-latex-expert
description: LaTeX rendering expertise in Obsidian for mathematical notation
category: Session Knowledge
---

# Skill: obsidian-latex-expert

## What I do

I provide expertise in using LaTeX for mathematical notation within Obsidian. I specialise in translating complex formulas into readable MathJax-compatible syntax, using both inline and block formatting. I ensure that technical and scientific notes maintain a high standard of mathematical clarity and professional presentation.

## When to use me

- When documenting mathematical formulas, scientific equations, or statistical models.
- When creating technical notes that require Greek letters, summations, integrals, or matrices.
- When aligning multiple equations for step-by-step proofs or derivations.
- When you need to escape special characters or fix rendering errors in complex LaTeX strings.

## Core principles

1. **Context-Appropriate Formatting** — Use inline LaTeX (\`$formula$\`) for simple variables within sentences and block LaTeX (\`$$formula$$\`) for primary equations that require visual emphasis.
2. **Readability and Alignment** — Use the \`align\` or \`gather\` environments to keep multi-line equations organised and scannable.
3. **Semantic Commands** — Prefer standard LaTeX commands over "hacky" visual formatting to ensure compatibility with different MathJax themes and exports.
4. **Escape Awareness** — Be mindful of backslashes and special characters, especially when embedding LaTeX inside YAML frontmatter or code blocks, where they may need additional escaping.

## Patterns & examples

### Inline vs Block Notation
Use single dollar signs for inline and double for blocks.
Inline: The area of a circle is $A = \pi r^2$.
Block:
$$
E = mc^2
$$

### Aligned Equations
Use the \`align*\` environment to line up equations at the equals sign.
$$
\begin{align*}
(a + b)^2 &= (a + b)(a + b) \\
&= a^2 + ab + ba + b^2 \\
&= a^2 + 2ab + b^2
\end{align*}
$$

### Common Mathematical Notation
Templates for frequently used structures.
- **Fractions**: \`\frac{numerator}{denominator}\` $\rightarrow \frac{a}{b}$
- **Summation**: \`\sum_{i=1}^{n} i\` $\rightarrow \sum_{i=1}^{n} i$
- **Matrices**: 
$$
\begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix}
$$

## Anti-patterns to avoid

- ❌ **Using Images for Formulas** — Capturing equations as screenshots instead of using LaTeX; this prevents searching and high-resolution rendering.
- ❌ **Over-Using Inline LaTeX** — Putting long, complex formulas inline, which disrupts the vertical rhythm and readability of paragraphs.
- ❌ **Unescaped Special Characters** — Forgetting that characters like \`_\`, \`^\`, and \`%\` have special meanings in LaTeX and may cause rendering errors if used as plain text within a formula.
- ❌ **Ignoring MathJax Limits** — Trying to use advanced LaTeX packages that are not supported by Obsidian's underlying MathJax renderer.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Session-Knowledge/Obsidian LaTeX Expert.md`

## Related skills

- `documentation-writing` — For integrating mathematical notation into high-quality technical reports.
- `obsidian-codeblock-expert` — For managing code that may generate or interact with LaTeX strings.
- `writing-style` — For maintaining a professional tone when explaining mathematical concepts.
- `information-architecture` — For structuring scientific knowledge bases.
