---
name: paper-polish
description: This skills helps agents to review and polish research papers written in LaTeX, focusing on writing clarity, grammar, LaTeX best practices, and document structure.
metadata:
  short-description: fixing writing errors in academic papers

---
# Polishing and reviewing research papers in LaTeX

## On writing

### Contents

- Your paper should be easily comprehensible by its reviewers.
  They are far less familiar with your work than you.
  They may not be an expert on the topic and may not be able to afford much time on your paper.
- The introduction should convey curiosity or excitement
  (new problem, new solution, improved solution, impressive results, or high impact),
  the design novelty, substantiality, and correctness,
  and the evaluation relevancy and comprehensiveness.
- Conciseness: Remove every word that contributes no meaning, such as `kind of`.
- Use proper tenses:
  - [1](https://www.unlv.edu/sites/default/files/page_files/27/GradCollege-VerbTenseScientificManuscripts.pdf)
  - [2](https://berks.psu.edu/sites/berks/files/campus/VerbTense_Handout.pdf)
  - [3](https://www.nature.com/scitable/topicpage/effective-writing-13815989/)

### Grammar

- Section titles should have consistent [capitalization](https://www.grammarly.com/blog/title-case-sentence-case/).
  - Title Case: Capitalize the first and last words and all major words in between.
    - Good: Introduction to Fuzzing with LLMs
  - Sentence case: Capitalize only the first word and proper nouns.
    - Good: Introduction to fuzzing with LLMs
  - Choose one style and be consistent throughout the paper.

- Avoid passive voice unless strongly justifiable.
  Passive voice is ambiguous because it has no subject unless followed by "by...".
  - Bad: LLM was applied to fuzzing. (Who applied it? The authors or someone else?)
  - Good: We applied LLM to fuzzing.

- Avoid [nominalization](https://en.wikipedia.org/wiki/Nominalization).
  - Bad: He made a proposal to use Rust.
  - Good: He proposed to use Rust.

- Avoid "There is/are".
  - Bad: There are many developers of Rust.
  - Good: Many developers use Rust.
  - Good: Rust has many developers.

- "Which" vs "that": Use "which" in a nonrestrictive clause and "that" in a restrictive clause.
  [More...](https://www.grammarly.com/blog/which-vs-that/)
  - Wrong: Rust that is safe is popular.
    (This is wrong because there is only one Rust.)
  - Right: Rust, which is safe, is popular.

- Distinguish [coordinating conjunction vs conjunctive adverbs](https://www.iup.edu/writingcenter/writing-resources/grammar/common-problems-with-however-therefore-and-similar-words.html).
  - Wrong: C is dangerous, Rust is safe. (Cannot join two sentences by a comma)
  - Right: C is dangerous, but Rust is safe.
  - Wrong: C is dangerous, however Rust is safe.
  - Right: C is dangerous; however, Rust is safe.

- "Fewer" modifies countable nouns whereas "less" uncountable nouns.
  - Wrong: ten items or less
  - Right: ten items or fewer
  - Wrong: fewer feedback
  - Right: less feedback

- Use articles (`a`, `an`, `the`) properly.
  - A singular countable noun must be preceded by an article.
    - Wrong: I wrote Rust program.
    - Right: I wrote a Rust program.
    - Right: I wrote Rust programs.

  - `The` must have a reference that is unique either by fact or in the context.
    - Right: the first Rust programmer (unique by fact)
    - Right: Our team has a Rust and a C++ programmer.
      The Rust programmer produces the fastest, most robust code.
      (unique in the context)
    - Wrong: Our team has two Rust and two C++ programmers.
      The Rust programmer is more productive than the C++ programmer.

- Distinguish between [compare with and compare to](https://www.noslangues-ourlanguages.gc.ca/en/writing-tips-plus/compare-to-compare-with)
  - Right: Rust is safer compared with C.
  - Right: Some people compare Rust to a panacea for memory safety problems.

## On LaTeX

- Use modern implementations of LaTeX to take advantage of Unicode and other useful features.
  - Use [LuaLaTeX](https://www.luatex.org/) instead of LaTeX or pdfLaTeX
  - Use [BibLaTeX](https://www.overleaf.com/learn/latex/Bibliography_management_with_biblatex) for `acmart` and `ieeetrans` templates instead of BibTex

- Use correct [typefaces](https://physics.nist.gov/cuu/pdf/typefaces.pdf).
  Particularly, _italics_ should be used for variables but not for descriptive terms. [More...](https://en.wikibooks.org/wiki/LaTeX/Mathematics#Adding_text_to_equations)
  - Wrong: $t_{max}$
  - Right: $t_\text{max}$

- Do not manually add separators in large numbers.
  `\usepackage{siunitx}`.
  Then, wrap large numbers in `\num{}`.
  - Bad: 12,345
  - Good: `\num{12345}`

- Do not manually type reference names, such as Table, Figure, Theorem.
  Instead, `\usepackage{hyperref}`,
  and then `\autoref{fig:xxx}`, `\autoref{sec:xxx}`, `\autoref{table:xxx}`.
  - Not recommended: In Figure~\ref{fig:overview}
  - Good: In \autoref{fig:overview}

## Structure

- `main.tex` is the entry root of the LaTeX project, containing the `usepackage` commands and the document structure.
- `src/` contains all the sections.
- `tables/` contains all the tables.
- `figures/` or `fig/` contains the figures. Figures are PDF files or `.tex` files.
  `.tex` in figures are algorithms.
- `code/` contains code listings used in the text.
