---
name: fact-checking
description: Verify the accuracy of claims and statements by extracting individual assertions, identifying authoritative sources, cross-referencing evidence, and assigning confidence-scored verdicts. Use when the user requests fact checking or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Fact-Checking

This skill enables an AI agent to systematically verify claims and statements. Rather than offering a simple true/false judgment, the agent extracts discrete checkable claims from the input, identifies authoritative sources for each, cross-references evidence, and produces a structured verdict with a confidence score and supporting reasoning. The approach is designed to handle everything from single factual assertions to full articles containing dozens of claims.

## Workflow

1. **Extract Claims:** Parse the input text and isolate individual, verifiable assertions. Each claim should be a single, self-contained statement that can be independently checked. Discard opinions, subjective judgments, and unfalsifiable statements, but note them as "not checkable" in the output.

2. **Classify Claim Types:** Categorize each claim by type — statistical (involves numbers or data), historical (references past events), scientific (references research findings), definitional (defines a term), or attribution (attributes a statement to a person or organization). The category guides where to look for verification.

3. **Identify Authoritative Sources:** For each claim, determine the most appropriate verification sources. Use primary sources whenever possible: official datasets for statistics, peer-reviewed papers for scientific claims, archived transcripts for quotations, and government records for legal or policy assertions. Supplement with reputable secondary sources like established fact-checking organizations (Snopes, PolitiFact, Full Fact).

4. **Cross-Reference and Evaluate Evidence:** Check each claim against at least two independent sources. Note whether sources corroborate, partially support, or contradict the claim. Assess source credibility by considering authority, recency, methodology, and potential bias.

5. **Assign Verdicts and Confidence Scores:** For each claim, assign a verdict from the scale: **True**, **Mostly True**, **Half True**, **Mostly False**, **False**, or **Unverifiable**. Accompany each verdict with a confidence score (0.0-1.0) reflecting the strength and consistency of available evidence, and a brief justification.

6. **Compile the Fact-Check Report:** Present findings in a structured format: list each claim, its verdict, confidence score, supporting evidence, and source links. Include an overall assessment summarizing the accuracy of the original text.

## Usage

Provide the agent with a statement, paragraph, or full article to fact-check. You can optionally specify which claims to prioritize or request a particular output format.

```
Fact-check the following statement:
"Python is the most popular programming language in 2025 according to the TIOBE Index,
and it was created by James Gosling at Sun Microsystems in 1991."
```

## Examples

### Example 1: Fact-Checking a Technical Blog Post

**User Request:**
> Fact-check the key claims in this blog excerpt:
> "Rust has zero runtime overhead compared to C, making it the fastest systems language available. The Linux kernel adopted Rust as its primary development language in 2024, replacing C entirely. According to Stack Overflow's 2024 survey, Rust has been the most admired language for nine consecutive years."

**Extracted Claims:**

| # | Claim | Type |
|---|---|---|
| 1 | Rust has zero runtime overhead compared to C | Scientific/Technical |
| 2 | Rust is the fastest systems language available | Comparative |
| 3 | The Linux kernel adopted Rust as its primary language in 2024 | Historical |
| 4 | Rust replaced C entirely in the Linux kernel | Historical |
| 5 | Rust has been the most admired language for 9 consecutive years per Stack Overflow | Statistical |

**Fact-Check Results:**

| # | Verdict | Confidence | Evidence |
|---|---|---|---|
| 1 | **Mostly True** | 0.80 | Rust's zero-cost abstractions compile to machine code comparable to C. However, some runtime components (bounds checking, panic unwinding) introduce marginal overhead. Source: [Rust Performance Book](https://nnethercote.github.io/perf-book/) |
| 2 | **Half True** | 0.50 | Benchmarks show Rust and C performing within 0-5% of each other on most tasks, but neither consistently "wins." Fortran outperforms both in certain numerical workloads. Source: [Benchmarks Game](https://benchmarksgame-team.pages.debian.net/) |
| 3 | **Mostly False** | 0.90 | Rust was accepted for driver and module development in Linux 6.1 (2022) and expanded in later releases, but it supplements C — it was never adopted as the "primary" language. Source: [LWN.net kernel Rust coverage](https://lwn.net/) |
| 4 | **False** | 0.95 | C remains the dominant language of the Linux kernel. Rust is used in select new modules only. Source: [kernel.org Git stats](https://git.kernel.org/) |
| 5 | **Mostly True** | 0.85 | Stack Overflow renamed "Most Loved" to "Most Admired" in 2023. Rust topped "Most Loved" from 2016-2022 (7 years) and "Most Admired" in 2023-2024 (2 years), totaling 9 years. Source: [Stack Overflow Developer Survey Archives](https://survey.stackoverflow.co/) |

**Overall Assessment:** The blog post contains a mix of approximately true technical claims and significantly exaggerated statements about Rust's role in the Linux kernel. Readers should be cautious about the kernel-related claims.

---

### Example 2: Fact-Checking Statistical Claims

**User Request:**
> Verify: "Global AI spending reached $200 billion in 2024, with 75% of Fortune 500 companies deploying generative AI in production. The average ROI for enterprise AI projects is 3.5x within the first year."

**Extracted Claims:**

| # | Claim | Type |
|---|---|---|
| 1 | Global AI spending reached $200 billion in 2024 | Statistical |
| 2 | 75% of Fortune 500 companies deployed generative AI in production | Statistical |
| 3 | Average ROI for enterprise AI projects is 3.5x in the first year | Statistical |

**Fact-Check Results:**

| # | Verdict | Confidence | Evidence |
|---|---|---|---|
| 1 | **Mostly True** | 0.75 | IDC estimated global AI spending at $184 billion for 2024, with Gartner projecting $196 billion. The $200 billion figure is within range of the higher estimates but not exact. Sources: IDC Worldwide AI Spending Guide (Oct 2024), Gartner AI Forecast (Nov 2024) |
| 2 | **Half True** | 0.60 | McKinsey's 2024 survey found 72% of organizations surveyed (not specifically Fortune 500) had adopted AI in some form, with 65% using generative AI. "In production" vs. "piloting" is a meaningful distinction the original claim does not make. Source: McKinsey Global AI Survey 2024 |
| 3 | **Unverifiable** | 0.30 | No credible large-scale study has published a generalizable "average ROI" figure for enterprise AI. Individual case studies vary wildly (0.5x to 10x+). BCG and MIT Sloan have cautioned against generalized ROI claims. Source: MIT Sloan Management Review (2024) |

**Overall Assessment:** The spending figure is approximately correct, the adoption statistic is in the right ballpark but imprecise, and the ROI claim lacks credible sourcing and should not be cited without qualification.

## Best Practices

- **Isolate each claim before verifying.** Complex sentences often bundle multiple assertions. Splitting them ensures nothing is overlooked and verdicts remain precise.
- **Prioritize primary sources over secondary reporting.** A news article saying "a study found X" is less reliable than reading the study itself. Always trace claims to their origin.
- **Account for context and framing.** A technically true number can be misleading if taken out of context. Note when a claim is true but presented in a way that implies something false.
- **Use the confidence score honestly.** A score of 0.5 is not a failure — it reflects genuine ambiguity. Overconfident verdicts erode trust more than honest uncertainty.
- **Check the date of the claim and the source.** A claim that was true in 2020 may be false in 2025. Always verify that the evidence is temporally relevant to the assertion.
- **Distinguish between "false" and "unverifiable."** If no credible evidence exists either way, the verdict should be "Unverifiable," not "False."

## Edge Cases

- **Claims about the future:** Predictions ("AI will replace 50% of jobs by 2030") cannot be fact-checked against evidence. Label them as "Predictive — not verifiable" and note the credibility of the source making the prediction.
- **Rapidly changing statistics:** If the claim involves a metric that updates frequently (e.g., cryptocurrency prices, COVID case counts), note the date the claim refers to and the date of verification, since the answer may differ.
- **Satirical or hyperbolic content:** If the source material is clearly satirical or uses deliberate exaggeration for rhetorical effect, note this context rather than issuing a literal "False" verdict.
- **Claims with no authoritative source:** Some niche or proprietary claims (e.g., internal company metrics) may have no publicly verifiable source. Label these "Unverifiable — no public source" and recommend the user request documentation from the claimant.
- **Ambiguous wording:** When a claim can be interpreted multiple ways (e.g., "most popular" could mean by usage, by survey, or by downloads), evaluate the most reasonable interpretation and note the ambiguity.
