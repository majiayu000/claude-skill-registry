---
name: bootstrap-product
description: |
  Transform a product briefing into comprehensive, research-backed product management artifacts.

  This skill conducts domain-expert research BEFORE user questioning to enable smarter questions
  and pre-populated artifacts with validated content. Uses Context7 for technology documentation,
  WebSearch for market/architecture/security research, and WebFetch for deep-dive analysis.

  Generates 4 research-enriched files:
  - product.md (product vision with market research citations)
  - roadmap.md (12-month roadmap with architecture research)
  - architecture.md (technical design with extensive Context7 references)
  - adr.md (architectural decisions with research-justified rationale)

  Triggers: "create product vision", "define new product", "product planning",
  "bootstrap product", "product documentation", "start new product", "product briefing"

allowed-tools:
  - AskUserQuestion
  - WebSearch
  - WebFetch
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
  - Read
  - Write
  - Edit
  - Grep
  - Glob

model: sonnet
---

# Bootstrap Product Skill

**Purpose**: Transform minimal product briefings into rich, research-backed product management artifacts that are market-viable and technically sound.

**Key Innovation**: Domain-expert research agent conducts comprehensive research BEFORE questioning, reducing user burden from 17 questions to typically 8-12 questions while delivering higher-quality, validated recommendations.

## Process Overview

```
1. Accept Product Briefing
   ↓
2. Conduct Domain-Expert Research (NEW)
   ├─ Context7: Technology documentation
   ├─ WebSearch: Market/architecture/security
   ├─ WebFetch: Deep-dive resources
   └─ Domain: Scientific/industry research
   ↓
3. Synthesize Research Report
   ↓
4. Ask Research-Informed Questions (8-12 instead of 17)
   ↓
5. Confirm Understanding (with research context)
   ↓
6. Generate Research-Enriched Artifacts (4 files)
   ↓
7. Update .context/ with Research Summary
   ↓
8. Provide Completion Summary with Citations
```

## Step 1: Accept & Analyze Briefing

**Input**: Product briefing from user (can be minimal - e.g., "Build a collaborative document editor")

**Actions**:
- Parse briefing for core concept, domain, technology hints
- Extract research keywords: product type, domain, use case, tech stack clues
- Identify what's missing that research can help fill

**Example**:
```
User: "Build a collaborative document editor"
→ Research keywords: "collaborative editing", "document editor", "real-time collaboration"
→ Technology areas: frontend frameworks, WebSocket libraries, rich text editors
→ Domain areas: market size, competitors (Google Docs, Notion), architecture patterns
```

## Step 2: Conduct Domain-Expert Research

**CRITICAL**: Research happens BEFORE questioning to inform smarter questions and pre-populate artifacts.

### 2.1 Technology Documentation Research (Context7)

**Purpose**: Identify best practices and recommended technologies

**Process**:
1. Identify 3-5 relevant technology candidates from briefing
2. For each technology:
   ```
   resolve-library-id(
     query="[Technology description]",
     libraryName="[framework name]"
   ) → libraryId

   query-docs(
     libraryId="[returned ID]",
     query="best practices for [specific use case]"
   ) → Documentation findings
   ```
3. Document findings with library IDs and queries used

**Limit**: 3-5 Context7 queries maximum

### 2.2 Architecture Pattern Research (WebSearch + WebFetch)

**Purpose**: Research proven architecture patterns for this domain

**Process**:
1. WebSearch for architecture patterns (5-8 queries):
   - "[domain/use case] architecture patterns 2026"
   - "[domain] scalability best practices 2026"
   - "microservices vs monolith [use case] 2026"
2. WebFetch 2-3 key resources:
   - Architecture whitepapers
   - Case studies from similar products
   - Implementation guides

**Limit**: 5-8 WebSearch queries, 2-3 WebFetch resources

### 2.3 Security & Compliance Research (WebSearch + WebFetch)

**Purpose**: Identify regulatory requirements and security best practices

**Process**:
1. WebSearch for compliance (5-8 queries):
   - "GDPR compliance [domain] applications 2026"
   - "HIPAA requirements [domain] 2026"
   - "SOC2 compliance SaaS applications 2026"
   - "OWASP top 10 [domain] security 2026"
2. WebFetch official compliance documentation

**Limit**: 5-8 compliance/security searches

### 2.4 Domain Knowledge Research (WebSearch + WebFetch)

**Purpose**: Understand market, competitors, and domain-specific insights

**Process**:
1. WebSearch for market intelligence (8-10 queries):
   - "[product type] market size 2026"
   - "[domain] industry trends 2026"
   - "[use case] competitive landscape"
   - "key competitors [product type]"
2. WebFetch 2-4 resources:
   - Market research reports
   - Academic papers (if applicable)
   - Industry analyses

**Limit**: 8-10 market/domain searches, 2-4 WebFetch resources

### 2.5 Research Synthesis

**Output**: Structured research report containing:
```markdown
## Research Report

### Technology Research (Context7)
- [Library 1]: [Key findings]
- [Library 2]: [Key findings]
- Recommendation: [Suggested tech stack]

### Architecture Research
- Pattern recommendation: [e.g., Monolith for MVP, microservices later]
- Scalability approach: [Key patterns found]
- Case studies: [Similar products]

### Security & Compliance
- Required standards: [GDPR, HIPAA, SOC2, etc.]
- Security measures: [OWASP compliance, encryption, etc.]

### Domain Knowledge
- Market size: [TAM from research]
- Key competitors: [List with strengths/weaknesses]
- Industry trends: [Relevant trends]

### Research Gaps (Need User Input)
- [Question 1 that research couldn't answer]
- [Question 2 that requires user preference]
- [Question 3 that needs validation]
```

## Step 3: Ask Research-Informed Questions

**Strategy**:
- Review research report before asking ANY questions
- Skip questions where research provides clear answers
- Ask validation questions to confirm research findings
- Focus on user preferences, constraints, and goals that research cannot determine
- Reduce from 17 questions to typically 8-12 questions

**Question Categories** (see full command file for complete question framework):

1. **Product Essence** (4 questions) - May be informed by domain research
2. **Market Context** (4 questions) - May have data from market research
3. **Technical Constraints** (3 questions) - Research identifies compliance needs
4. **Execution Context** (3 questions) - Research informs timeline estimates
5. **Product Scope** (3 questions) - Research identifies must-have features

**Example** (Collaborative Document Editor):
```
Research found:
- Market size: $5B TAM
- Competitors: Google Docs, Notion, Confluence
- Tech stack: React + WebSocket recommended
- Compliance: GDPR for EU customers
- Architecture: Operational Transform or CRDT patterns

Questions SKIPPED:
✗ "What's the market size?" (research found: $5B)
✗ "Who are competitors?" (research identified 3 major players)
✗ "Technology preferences?" (research suggests React + Socket.io)

Questions ASKED:
✓ "Do you need GDPR compliance?" (validate research finding)
✓ "What's your differentiation vs Google Docs?" (user vision)
✓ "Target scale?" (informs architecture choice)
✓ "MVP timeline?" (user constraint)
✓ "Team size?" (user constraint)
```

**Result**: 8 targeted questions instead of 17 generic ones

## Step 4: Confirm Understanding

Present research-enhanced confirmation:

```markdown
Let me confirm what I understand about your product:

**Product**: [Name/description]
**Core Problem**: [2-3 sentences]
**Target Users**: [User persona]
**Market Context**: [Size and competitors FROM RESEARCH]
**Key Differentiation**: [Unique value]
**Technical Approach**: [Architecture informed by Context7 research]
**Compliance Requirements**: [GDPR, HIPAA, SOC2 identified FROM RESEARCH]
**MVP Timeline**: [Timeline]
**Success Metrics**: [2-4 metrics]

**Research Conducted**:
- Technology: [Context7 libraries queried]
- Market: [Key findings]
- Security: [Standards identified]
- Domain: [Insights]

Is this correct? Please confirm or provide corrections.
```

## Step 5: Generate Research-Enriched Artifacts

**Generation Order** (dependency-driven):

### 5.1 product.md (150-250 lines)
- Product vision with market research citations
- Competitive landscape FROM RESEARCH
- Success metrics with industry benchmarks FROM RESEARCH

### 5.2 roadmap.md (200-250 lines)
- Phases informed by architecture research
- Timeline realistic based on technology research

### 5.3 architecture.md (200-300 lines)
- Technology stack backed by Context7 documentation
- Architecture pattern from research
- Security measures from compliance research
- **EXTENSIVE Context7 citations**

### 5.4 adr.md (100-150 lines)
- ADR-001: Technology Stack (Context7-backed)
- ADR-002: Architecture Pattern (research-validated)
- ADR-003: Database Choice (comparative research)
- ADR-004: Security & Compliance (regulatory research)
- All ADRs include research citations

**Progress Indicators**:
```
Generating research-enriched artifacts...
✓ Created product.md (187 lines) - with market research
✓ Generated roadmap.md (223 lines) - with architecture research
✓ Designed architecture.md (298 lines) - with Context7 references
✓ Documented adr.md (156 lines) - with research-justified decisions
```

## Step 6: Update .context/

### notes.md (< 150 lines)
Add Product Bootstrap Summary including:
- Product overview
- **Research Conducted** section
- **Key Research Findings**
- **Research Sources Summary**
- Key docs references

### changelog.md (< 70 lines)
Add bootstrap entry including:
- Decisions (7 key decisions)
- **Research Conducted** section
- Artifacts generated WITH research annotations
- Rationale with research backing

### handoff.md
Create comprehensive handoff including:
- Product artifacts generated
- Information gathered
- **Research Conducted** section (detailed)
- Important decisions
- Next steps

## Step 7: Provide Summary

**Summary Format**:
```markdown
## Product Bootstrapping Complete!

### Product Overview
- **Name**: [Name]
- **Vision**: [One sentence]
- **Target**: [User segment]
- **MVP Timeline**: [Timeline]

### Generated Artifacts
- product.md (X lines) - with market research citations
- roadmap.md (X lines) - with architecture research
- architecture.md (X lines) - with Context7 references
- adr.md (X lines) - 4 ADRs with research justification

### Research Conducted
**Context7**: [X] libraries documented
**WebSearch**: [Y] searches (market/architecture/security)
**WebFetch**: [Z] deep-dive resources

**Impact**:
- Questions reduced from 17 to [actual]
- All decisions research-backed
- Full citation traceability

### Next Steps
1. Review artifacts and research citations
2. Validate findings against domain expertise
3. Begin MVP development planning
```

## Important Guidelines

**DO**:
- ✅ Conduct research BEFORE asking questions
- ✅ Skip questions that research confidently answered
- ✅ Include research citations in ALL artifacts
- ✅ Use Context7 for all technology decisions
- ✅ Cite specific library IDs (/org/project format)
- ✅ Keep .context/ files under 500 lines
- ✅ Provide research sources summary

**DON'T**:
- ❌ Ask all 17 questions if research answered some
- ❌ Make technology recommendations without Context7 backing
- ❌ Skip research phase to save time
- ❌ Omit research citations from artifacts
- ❌ Exceed research query limits (causes token bloat)
- ❌ Generate artifacts without research validation

**Research Query Limits** (CRITICAL):
- Context7: 3-5 libraries max
- WebSearch: 5-8 per category (market, architecture, security)
- WebFetch: 2-4 deep resources max
- Enforce these to prevent token bloat and API overuse

## Success Criteria

After execution:
- ✅ 4 comprehensive product files generated (600-1000 lines total)
- ✅ All artifacts include research citations
- ✅ Technology decisions backed by Context7 documentation
- ✅ Architectural decisions validated by industry research
- ✅ Compliance requirements identified proactively
- ✅ Questions reduced to 8-12 based on research coverage
- ✅ .context/ files updated with research summary
- ✅ All .context/ files under 500 lines
- ✅ Full citation traceability for all recommendations

## Templates

**Note**: This skill uses abbreviated templates. For complete templates with all sections and examples, see:
- `.claude/commands/bootstrap-product.md` (full command file, ~2000 lines)

The full command file contains:
- Detailed question framework (all 17 questions with research annotations)
- Complete artifact templates (product.md, roadmap.md, architecture.md, adr.md)
- Research integration instructions
- Example execution flows

---

**Command Version**: For explicit invocation, use `/bootstrap-product [briefing]`
**Skill Version**: This file - activated by semantic triggers for product planning conversations
