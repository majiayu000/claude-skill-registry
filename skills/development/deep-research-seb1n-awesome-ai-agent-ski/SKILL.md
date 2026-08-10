---
name: deep-research
description: Conduct in-depth, multi-step research on a given topic by decomposing queries, finding diverse sources, cross-referencing findings, and synthesizing a comprehensive report. Use when the user requests deep research or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Deep Research

This skill enables an AI agent to perform rigorous, multi-step research on complex topics. Rather than returning a single search result, the agent decomposes the research question into sub-queries, gathers information from diverse source types (academic papers, industry reports, official documentation, news articles, and expert commentary), cross-references findings for consistency, and synthesizes everything into a structured, citation-backed report. The result is a thorough analysis that surfaces nuance, identifies conflicting viewpoints, and highlights knowledge gaps.

## Workflow

1. **Decompose the Research Query:** Break the user's high-level question into 3-6 targeted sub-queries that cover distinct facets of the topic. Each sub-query should address a specific angle such as historical context, current state, key players, technical details, or future outlook. This ensures broad coverage rather than shallow retrieval from a single search.

2. **Identify and Gather Sources:** For each sub-query, search across multiple source categories: academic databases, official documentation, reputable news outlets, industry analyst reports, and community forums. Aim for at least 2-3 sources per sub-query. Record the URL, publication date, author, and a relevance score for each source to enable later prioritization.

3. **Extract and Organize Key Findings:** Read each source and extract the core claims, data points, statistics, and expert opinions. Organize findings into a structured outline grouped by theme or sub-query. Tag each finding with its source for traceability.

4. **Cross-Reference and Validate:** Compare findings across sources to identify consensus, contradictions, and gaps. Flag any claims that appear in only one source or that conflict with the majority of evidence. Note the recency and authority of each source when resolving disagreements.

5. **Synthesize the Report:** Combine validated findings into a coherent narrative. Structure the report with an executive summary, detailed sections for each theme, a discussion of limitations and open questions, and a full reference list. Use clear headings and bullet points for readability.

6. **Review and Refine:** Re-read the report for logical flow, unsupported claims, and missing context. Verify that all citations are accurate and that the executive summary faithfully reflects the detailed findings. Offer the user suggestions for further research if gaps remain.

## Usage

Provide the agent with a research topic and, optionally, specific sub-questions, desired depth level, or preferred source types. The agent will follow the full workflow and return a structured report.

```
Research the current state of WebAssembly adoption in 2025.

Focus areas:
- Browser and server-side runtime support
- Major companies and projects using WebAssembly in production
- Performance benchmarks compared to native code
- Toolchain maturity (languages, compilers, debugging)
- Key limitations and open challenges
```

## Examples

### Example 1: State of WebAssembly in 2025

**User Request:**
> Conduct deep research on the state of WebAssembly in 2025 — adoption, toolchains, performance, and outlook.

**Query Decomposition:**
| Sub-Query | Angle |
|---|---|
| "WebAssembly browser support 2025 Chrome Firefox Safari" | Runtime support |
| "WebAssembly server-side WASI Wasmtime Wasmer production" | Server-side adoption |
| "WebAssembly performance benchmarks vs native 2024 2025" | Performance data |
| "Rust Go C++ compile to WebAssembly toolchain maturity" | Toolchain ecosystem |
| "WebAssembly limitations garbage collection threads 2025" | Open challenges |

**Sources Gathered (excerpt):**
- W3C WebAssembly Working Group Status Report (w3.org, Jan 2025)
- "Wasm in Production at Figma" — Figma Engineering Blog (2024)
- Bytecode Alliance WASI 0.2 Announcement (bytecodealliance.org, 2024)
- "WebAssembly vs JavaScript: 2025 Benchmarks" — InfoQ (2025)
- MDN Web Docs — WebAssembly GC Proposal Status (developer.mozilla.org)

**Synthesized Report (excerpt):**
> **Executive Summary:** WebAssembly has matured from a browser-only technology to a portable compilation target for server-side, edge, and embedded workloads. All major browsers ship full Wasm 2.0 support including the GC and Threads proposals. WASI 0.2 has stabilized the component model, enabling language-agnostic plug-in architectures adopted by Fastly, Fermyon, and Cloudflare Workers. Performance benchmarks show Wasm executing at 85-95% of native speed for compute-heavy tasks, though startup latency and GC integration remain areas of active work. The toolchain ecosystem is strongest for Rust and C/C++, with Go and Python support improving rapidly. Key open challenges include the lack of a standardized debugging protocol and limited direct DOM access for UI-heavy browser applications.

---

### Example 2: Competitive Analysis for a Product Launch

**User Request:**
> Research the competitive landscape for AI-powered code review tools ahead of our product launch.

**Query Decomposition:**
| Sub-Query | Angle |
|---|---|
| "AI code review tools market 2025 overview" | Market landscape |
| "GitHub Copilot code review features pricing" | Competitor deep-dive |
| "CodeRabbit AI automated code review capabilities" | Competitor deep-dive |
| "developer survey AI code review adoption satisfaction" | User sentiment |
| "AI code review tool limitations false positives" | Weaknesses and gaps |

**Synthesized Report (excerpt):**
> **Market Overview:** The AI code review market has consolidated around three tiers: integrated platform tools (GitHub Copilot, GitLab Duo), standalone AI review services (CodeRabbit, Codacy AI), and open-source linters with LLM augmentation (MegaLinter + GPT wrappers). Developer adoption surveys indicate 42% of teams in companies with 50+ engineers use some form of AI-assisted review.
>
> **Competitive Gap Identified:** No current tool provides repository-wide architectural consistency checks — they operate at the PR diff level. A product that combines diff-level suggestions with codebase-wide pattern enforcement could capture the underserved "platform engineering" segment.

## Best Practices

- **Diversify source types.** Never rely on a single category of source. Mix primary sources (official docs, data sets) with secondary analysis (blog posts, analyst reports) to get a balanced view.
- **Record provenance for every claim.** Attach the source URL, author, and date to each extracted finding so the final report can be audited and citations verified.
- **Prefer recent sources but include seminal works.** Prioritize sources published within the last 1-2 years, but include foundational papers or documents that define the field.
- **Quantify when possible.** Replace vague claims like "widely adopted" with specific numbers like "used by 38% of surveyed teams" to make the report more actionable.
- **Surface disagreements explicitly.** When sources conflict, present both sides with their evidence rather than silently choosing one. This builds trust and lets the reader decide.
- **Set a scope boundary early.** Clearly define what is in-scope and out-of-scope for the research to avoid unbounded rabbit holes and keep the report focused.

## Edge Cases

- **Rapidly evolving topics:** If the research subject changes weekly (e.g., active policy debates, breaking security vulnerabilities), note the knowledge cutoff date prominently and recommend the user verify findings before acting on them.
- **Limited or paywalled sources:** When key sources are behind paywalls or restricted access, note the gap, cite the abstract or summary where available, and suggest the user obtain full access for verification.
- **Contradictory high-authority sources:** If two equally credible sources directly contradict each other, present both claims side by side, describe the methodology of each, and label the finding as "disputed" rather than forcing a verdict.
- **Emerging topics with sparse literature:** For very new technologies or concepts, acknowledge the limited evidence base, lean on primary sources (release notes, RFCs, official announcements), and clearly separate established facts from speculation.
- **Multilingual or region-specific research:** When the topic spans geographies, note which regions the sources cover and flag if findings may not generalize globally.
