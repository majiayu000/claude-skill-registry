---
name: swing-research
description: Deep research with cross-verification and source tiering. Use when investigating technologies, comparing tools, fact-checking claims, evaluating architectures, or any task requiring verified information. Triggers on "조사해줘", "리서치", "research", "investigate", "fact-check", "비교 분석", "검증해줘".
argument-hint: "[topic or question to research]"
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Bash, Agent
---

# Cross-Verified Research

Systematic research engine with anti-hallucination safeguards and source quality tiering.


## Rules (Absolute)

1. **Never fabricate sources.** No fake URLs, no invented papers, no hallucinated statistics.
2. **Source-traceability gate.** Every factual claim must be traceable to a specific, citable source. If a claim cannot be traced to any source, mark it as **Unverified (internal knowledge only)** and state what verification would be needed. Never present untraced claims as findings.
3. **No speculation as fact.** Do not present unverified claims using hedging language as if they were findings. Banned patterns: "아마도", "~인 것 같습니다", "~로 보입니다", "~수도 있습니다", "probably", "I think", "seems like", "appears to be", "likely". If a claim is not verified, label it explicitly as **Unverified** or **Contested** — do not soften it with hedging.
4. **BLUF output.** Lead with conclusion, follow with evidence. Never bury the answer.
5. **Scaled effort.** Match research depth to question scope:
   - **Narrow factual** (single claim, date, specification): 2-3 queries, 2+ sources
   - **Technology comparison** (A vs B): 5+ queries, 5+ sources
   - **Broad landscape** (market analysis, state-of-art): 8+ queries, 8+ sources
   Default to the higher tier when scope is ambiguous.
6. **Cross-verify.** Every key claim must appear in 2+ independent sources before presenting as fact. "Independent" means the sources conducted their own analysis or reporting — two articles that both cite the same original source (press release, blog post, study) count as ONE source, not two. Trace claims back to their origin.
7. **Scope before search.** If the research question is ambiguous or overly broad, decompose it into specific sub-questions in Stage 1 and present them to the user for confirmation before proceeding to Stage 2. Do not research a vague question — sharpen it first.

## Pipeline

Execute these 4 stages sequentially. Do NOT skip stages.

### Stage 1: Deconstruct

Break the research question into atomic sub-questions.

```
Input: "Should we use Bun or Node.js for our backend?"
Decomposed:
  1. Runtime performance benchmarks (CPU, memory, startup)
  2. Ecosystem maturity (npm compatibility, native modules)
  3. Production stability (known issues, enterprise adoption)
  4. Developer experience (tooling, debugging, testing)
  5. Long-term viability (funding, community, roadmap)
```

- Identify what requires external verification vs. internal knowledge
- If the original question is vague or overly broad, present the decomposed sub-questions to the user for confirmation before proceeding (Rule 7)
- For each sub-question, note what a traceable source would look like

### Stage 2: Search & Collect

For each sub-question requiring verification:

1. **Formulate diverse queries** — vary keywords, include year filters, try both English and Korean
2. **Use WebSearch** for broad discovery, **WebFetch** for specific page analysis
3. **Classify every source** by tier immediately (see Source Tiers below)
4. **Extract specific data points** — numbers, dates, versions, quotes with attribution
5. **Record contradictions** — when sources disagree, note both positions
6. **Trace origin** — when multiple sources cite the same underlying source, identify the original

Search pattern (scale per Rule 5):
```
Query 1: [topic] + "benchmark" or "comparison"
Query 2: [topic] + "production" or "enterprise"
Query 3: [topic] + [current year] + "review"
Query 4: [topic] + "issues" or "problems" or "limitations"
Query 5: [topic] + site:github.com (issues, discussions)
```

**Fallback when WebSearch is unavailable or returns no results:**
1. Use WebFetch to directly access known authoritative URLs (official docs, GitHub repos, Wikipedia)
2. Rely on internal knowledge but label all claims as **Unverified (no external search available)**
3. Ask the user to provide source URLs or documents for verification
4. Reduce the minimum source requirement but maintain cross-verification where possible

### Stage 3: Cross-Verify

For each key finding:
- Does it appear in 2+ independent Tier S/A sources? → **Verified**
- Does it appear in only 1 source? → **Unverified** (label it)
- Do sources contradict? → **Contested** (present both sides with tier labels)

Remember: "independent" means each source did its own analysis. Two articles both citing the same benchmark study = 1 source.

Build a verification matrix:
```
| Claim | Source 1 (Tier) | Source 2 (Tier) | Status |
|-------|----------------|----------------|--------|
| Bun 3x faster startup | benchmarks.dev (A) | bun.sh/blog (B) | Verified (note: Bun's own blog = biased) |
```

### Stage 4: Synthesize

Produce the final report in BLUF format.

## Output Format

```markdown
## Research: [Topic]

### Conclusion (BLUF)
[1-3 sentence definitive answer or recommendation]

### Key Findings
[Numbered findings, each with inline source tier labels]

1. **[Finding]** — [evidence summary]
   Sources: 🏛️ [source1], 🛡️ [source2]

2. **[Finding]** — [evidence summary]
   Sources: 🛡️ [source1], 🛡️ [source2]

### Contested / Uncertain
[Any claims that couldn't be cross-verified or where sources conflict]
- ⚠️ [claim] — Source A says X, Source B says Y

### Verification Matrix
| Claim | Sources | Tier | Status |
|-------|---------|------|--------|
| ... | ... | ... | Verified/Unverified/Contested |

### Sources
[All sources, grouped by tier]

#### 🏛️ Tier S — Academic & Primary Research
- [Title](URL) — Journal/Org (Year)

#### 🛡️ Tier A — Trusted Official
- [Title](URL) — Source (Year)

#### ⚠️ Tier B — Community / Caution
- [Title](URL) — Platform (Year)

#### Tier C — General
- [Title](URL)
```

## Quality Calibration

### BAD Example — What to Avoid

```markdown
## Research: Is Rust faster than Go for web servers?

### Conclusion (BLUF)
Rust is generally faster than Go for web servers due to zero-cost abstractions.

### Key Findings
1. **Rust is 2-5x faster than Go** — Rust's ownership model eliminates GC pauses.
   Sources: 🛡️ https://rust-performance-comparison.example.com
2. **Rust uses less memory** — Typically 50% less memory in production.
   Sources: 🛡️ https://memory-benchmarks.example.com
3. **Go is easier to learn** — Most developers pick up Go in a week.
   Sources: 🏛️ https://developer-survey.example.com

### Verification Matrix
| Claim | Sources | Tier | Status |
|-------|---------|------|--------|
| 2-5x faster | 1 benchmark site | A | Verified |
| 50% less memory | 1 benchmark site | A | Verified |
```

**Why this is bad:**
- Source URLs are fabricated (nonexistent domains)
- "2-5x faster" and "50% less memory" are presented as **Verified** with only 1 source each
- No contested claims section despite this being a nuanced topic
- Claims are restated internal knowledge dressed up with fake citations
- No origin tracing — where did "2-5x" come from?
- The "Verified" labels are false — nothing was actually cross-verified

### GOOD Example — What to Aim For

```markdown
## Research: Is Rust faster than Go for web servers?

### Conclusion (BLUF)
Rust outperforms Go in raw throughput benchmarks (typically 1.5-3x in TechEmpower), but the gap narrows significantly with real-world I/O workloads. Go's GC pauses (sub-millisecond since Go 1.19) are rarely a bottleneck for typical web services. Choose based on your latency tail requirements, not averages.

### Key Findings
1. **Rust frameworks lead TechEmpower benchmarks** — Actix-web and Axum consistently rank in the top 10; Go's stdlib and Gin rank 20-40 range in plaintext/JSON tests.
   Sources: 🏛️ TechEmpower Round 22 (2024), 🛡️ Axum GitHub benchmarks
2. **Go's GC latency is sub-millisecond since 1.19** — p99 GC pause < 500μs confirmed by the Go team.
   Sources: 🛡️ Go Blog "Getting to Go" (2022), 🛡️ Go 1.19 Release Notes
3. **Real-world gap is smaller than microbenchmarks suggest** — Discord's 2020 migration (Go→Rust) showed tail latency improvements, but their workload (millions of concurrent connections) is atypical.
   Sources: 🛡️ Discord Engineering Blog (2020), ⚠️ HN discussion with Discord engineer comments

### Contested / Uncertain
- ⚠️ **"Rust uses 50% less memory than Go"** — Frequently repeated on Reddit/HN but no independent benchmark reproduces a consistent figure. Memory usage depends heavily on allocator choice (jemalloc vs system) and workload. **Unverified.**
- ⚠️ **Developer productivity trade-off** — Go advocates claim 2-3x faster development time. No peer-reviewed study supports a specific multiplier. **Unverified (internal knowledge only)** — would need controlled study to verify.

### Verification Matrix
| Claim | Sources | Tier | Status |
|-------|---------|------|--------|
| Rust 1.5-3x faster (synthetic) | TechEmpower R22 (S), Axum bench (A) | S+A | Verified |
| Go GC < 500μs p99 | Go Blog (A), Release Notes (A) | A+A | Verified |
| Discord latency improvement | Discord Blog (A), HN thread (B) | A+B | Verified (single case study) |
| Rust 50% less memory | Reddit threads (B) only | B | Unverified |
| Go 2-3x dev speed | No source found | — | Unverified (internal knowledge only) |

### Sources

#### 🏛️ Tier S — Academic & Primary Research
- [TechEmpower Framework Benchmarks Round 22](https://www.techempower.com/benchmarks/) — TechEmpower (2024)

#### 🛡️ Tier A — Trusted Official
- [Getting to Go: The Journey of Go's Garbage Collector](https://go.dev/blog/ismmkeynote) — Go Blog (2022)
- [Go 1.19 Release Notes](https://go.dev/doc/go1.19) — Go Team (2022)
- [Why Discord is Switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust) — Discord Engineering (2020)
- [Axum Benchmarks](https://github.com/tokio-rs/axum) — Tokio Project

#### ⚠️ Tier B — Community / Caution
- [HN Discussion on Discord migration](https://news.ycombinator.com/item?id=22238289) — Hacker News (2020)
```

**Why this is good:**
- Every URL is a real, verifiable page
- Claims that lack sources are explicitly labeled **Unverified**
- The "50% less memory" myth is called out rather than repeated
- Verification matrix honestly shows what's verified vs. not
- Sources are independent (TechEmpower did their own benchmarks, not citing each other)
- Nuance preserved: "the gap narrows with real-world I/O"

## Source Tiers

Classify every source on discovery.

| Tier | Label | Trust Level | Examples |
|------|-------|-------------|----------|
| S | 🏛️ | Academic, peer-reviewed, primary research, official specs | Google Scholar, arXiv, PubMed, W3C/IETF RFCs, language specs (ECMAScript, PEPs) |
| A | 🛡️ | Government, .edu, major press, official docs | .gov/.edu, Reuters/AP/BBC, official framework docs, company engineering blogs (Google AI, Netflix Tech) |
| B | ⚠️ | Social media, forums, personal blogs, wikis — flag to user | Twitter/X, Reddit, StackOverflow, Medium, dev.to, Wikipedia, 나무위키 |
| C | (none) | General websites not fitting above categories | Corporate marketing, press releases, SEO content, news aggregators |

### Tier Classification Rules

- **Company's own content about their product:**
  - Official docs → Tier A
  - Feature announcements → Tier A (existence), Tier B (performance claims)
  - Marketing pages → Tier C
- **GitHub:**
  - Official repos (e.g., facebook/react) → Tier A
  - Issues/Discussions with reproduction → Tier A (for bug existence)
  - Random user repos → Tier B
- **Benchmarks:**
  - Independent, reproducible, methodology disclosed → Tier S
  - Official by neutral party → Tier A
  - Vendor's own benchmarks → Tier B (note bias)
- **StackOverflow:** Accepted answers with high votes = borderline Tier A; non-accepted = Tier B
- **Tier B sources must never be cited alone** — corroborate with Tier S or A

## When to Use

- Technology evaluation or comparison
- Fact-checking specific claims
- Architecture decision research
- Market/competitor analysis
- "Is X true?" verification tasks
- Any question where accuracy matters more than speed

## When NOT to Use

- Creative writing or brainstorming (use `swing-options`)
- Code implementation
- Simple questions answerable from internal knowledge with high confidence
- Opinion-based questions with no verifiable answer

## Gotchas

1. **Never invent a URL.** If search returns nothing, say "Unverified (no source found)" — do not guess a plausible-looking URL. Fabricated sources destroy all credibility.
2. **Two articles citing the same study = 1 source.** Trace claims to their origin. A press release quoted by 5 news sites is still one source, not five.
3. **Vendor benchmarks are Tier B, not A.** Even official engineering blogs have bias when benchmarking their own product. Label the bias explicitly.
4. **Hedging is not labeling.** "아마도", "seems like", "probably" are banned. Either a claim is Verified (2+ independent sources) or it gets an explicit Unverified/Contested label.
5. **Don't skip the Verification Matrix.** It's the accountability layer. Without it, the report looks rigorous but has no audit trail.

## Integration Notes

- **With swing-clarify:** Run swing-clarify first on ambiguous requests before invoking this skill. Clarified scope produces better results.
- **With swing-review:** Research findings can feed into adversarial review for stress-testing conclusions
