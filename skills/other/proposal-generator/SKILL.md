---
name: proposal-generator
description: Generate HTML proposals for consulting and enterprise clients from meeting transcripts. Extracts client needs, recommends pricing, and weaves in NGM platform value props with editorial styling.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Proposal Generator for Next Generation Medicine

## Overview

This skill transforms meeting transcripts into polished, professionally-styled HTML proposals for prospective consulting or enterprise clients. It extracts client needs and pain points from unstructured conversation, recommends value-based pricing, and naturally weaves in NGM's credentials and platform capabilities.

## Required Inputs

1. **Meeting Transcript**: File path or raw text content from a client conversation
2. **Proposal Type** (optional): "consulting" or "enterprise" - will be inferred if not specified
3. **Client Name**: Name of the prospective client/organization
4. **Output Path** (optional): Where to save the HTML file - defaults to `content/proposals/`

## Default Output Location

All proposals are saved to: `content/proposals/`

Filename format: `proposal-[client-name-slug]-[YYYY-MM-DD].html`

Example: `content/proposals/proposal-acme-health-2025-01-15.html`

---

## Learning from Past Proposals

**IMPORTANT:** Before generating a new proposal, ALWAYS check for existing proposals in `content/proposals/` to learn from and maintain consistency.

### Pre-Generation Steps:

1. **List existing proposals:**
   ```
   Glob: content/proposals/*.html
   ```

2. **Read 1-2 recent proposals** to observe:
   - Tone and voice patterns
   - Section structure and flow
   - How credentials are woven in
   - Pricing presentation style
   - CTA language that's been used

3. **Note any client-specific patterns:**
   - Similar client types (clinic vs health system vs startup)
   - Similar engagement types
   - Pricing benchmarks from past deals

### Why This Matters:

- Maintains consistent brand voice across proposals
- Builds institutional memory of what works
- Allows pricing to stay calibrated to market
- Ensures proposals evolve based on feedback (if user modifies past proposals, future ones should reflect those changes)

## Proposal Types

### Consulting Proposals
For individuals, clinics, or small organizations seeking:
- Strategic guidance and advisory
- Fractional CMO/Chief Medical Officer work
- Protocol development
- Practice optimization
- Personal mentorship

### Enterprise Proposals
For larger organizations seeking:
- Platform licensing (LongevityOS, AI tools)
- Team training programs
- White-label solutions
- API integrations
- Full partnership arrangements

---

## Transcript Processing Instructions

When reading the transcript, extract and note:

### Client Information
- Name, title, organization
- Organization size (employees, revenue signals)
- Current state of their longevity/health business
- Geographic scope

### Pain Points & Challenges
- What problems are they trying to solve?
- What have they tried that didn't work?
- What's causing friction or inefficiency?
- What gaps exist in their current approach?

### Goals & Desired Outcomes
- What does success look like for them?
- Timeline expectations
- Specific deliverables mentioned
- Metrics they care about

### Budget & Urgency Signals
- Any budget ranges mentioned
- Funding status or constraints
- Timeline pressures ("launching in Q1", "need this yesterday")
- Competitive pressures

### Specific Requests
- Particular services or capabilities asked about
- Questions about NGM's offerings
- Integration requirements
- Customization needs

### Strategic Value Indicators
- Size of opportunity (their market, patient volume)
- Partnership potential beyond initial engagement
- Reference/case study potential
- Network effects

---

## NGM Knowledge Base

Use this information to naturally weave NGM's value throughout the proposal. Do NOT dump all of this - select what's relevant to the client's specific needs.

### Dr. Anant Vinjamoori's Credentials

**Current Roles:**
- Chief Longevity Officer at Superpower
- Head of Longevity Medicine at Midi Health
- Founder, Next Generation Medicine

**Background:**
- Harvard Medical School graduate
- Chief Medical Officer at Modern Age - built the first vertically integrated, national-scale longevity clinic in the United States
- Former leader at Virta Health, helping grow the startup to a $3B+ valuation
- Advisor to longevity companies valued at over $1 billion combined

**Media Recognition:**
- Featured in Wall Street Journal, Forbes, Fortune

**Core Philosophy:**
"I help turn science into strategy—and strategy into systems that deliver measurable results."

### NGM Platform Capabilities

**The Longevity Intelligence Platform:**
- Most comprehensive longevity knowledge base available
- 50,000+ peer-reviewed studies synthesized
- Combines academic research + real-world clinical protocols + proprietary frameworks
- Continuously updated - "As I get smarter, you get smarter"
- Can answer any question related to longevity medicine
- Adapts to practice philosophy (conservative to cutting-edge)

**AI Lab Report Generator:**
- Transforms raw lab data into publication-quality patient reports
- 5-minute turnaround vs. 45-minute manual process
- Handles any biomarker type (metabolic panels, longevity markers, endocrine)
- Includes risk assessment, intervention priority matrix, mechanistic insights
- Customizable to practice philosophy and branding
- Peer-reviewed literature integration with citations

**Business Knowledge Advisor:**
- Built from experience scaling Modern Age nationally
- Informed by advising top-tier longevity companies
- Covers clinic operations, pricing, patient acquisition, scaling

**Educational Curriculum:**
- 150+ deep-dive modules
- Covers: hormones, peptides, GLP-1s, diagnostics, aging frameworks, AI integration
- Monthly live lectures with latest research
- NGM Certification pathway

**Community & Mentorship:**
- 240+ member private community
- Weekly live sessions with Dr. Vinjamoori
- Real-time case feedback
- Expert network access

### Unique Value Propositions

1. **Only platform combining education + AI tools + mentorship + business strategy** in one integrated offering

2. **Real-world scaling experience** - Built from actual clinic operations, not academic theory

3. **Battle-tested protocols** - Refined through thousands of patient interactions

4. **Continuously evolving** - Knowledge base improves as Dr. V remains active in clinical advisory

5. **Customizable to philosophy** - Works for conservative FDA-approved approaches through cutting-edge biohacking

### Client Outcomes (Use as Social Proof)

- Physicians going from $200/visit to $1,500 6-month programs
- Clinicians reducing patient load from 25+ to 12 per week while increasing revenue
- Lab report generation time reduced from 45 minutes to 5 minutes
- Practices adding longevity service lines generating $50K+ additional monthly revenue

---

## Pricing Framework

Generate pricing recommendations based on the value analysis from the transcript. Present as a range with the recommended option highlighted.

### Consulting Engagements

| Engagement Type | Price Range | When to Recommend |
|----------------|-------------|-------------------|
| **Strategy Session** (2-4 hours) | $2,500 - $5,000 | Initial assessment, specific problem solving, second opinions |
| **Monthly Advisory Retainer** | $5,000 - $15,000/mo | Ongoing strategic guidance, regular check-ins, async support |
| **Fractional CMO/Advisor** | $10,000 - $25,000/mo | Deep involvement, leadership meetings, team guidance |
| **Protocol Development** | $15,000 - $50,000 | Custom clinical protocols, SOPs, training materials |
| **Practice Transformation** | $25,000 - $75,000 | Full practice redesign, service line development, operations overhaul |

**Pricing Factors:**
- Complexity of needs (simple guidance vs. full transformation)
- Time commitment required (hours/week)
- Urgency (expedited timelines command premium)
- Strategic value (high-profile clients, partnership potential)
- Organization size and budget capacity

### Enterprise Engagements

| Engagement Type | Price Range | When to Recommend |
|----------------|-------------|-------------------|
| **Platform Licensing** | $2,000 - $10,000/mo | Access to LongevityOS, AI tools for team |
| **Team Training Cohort** | $25,000 - $75,000 | Group curriculum delivery, certification |
| **White-Label Implementation** | $50,000 - $150,000 | Branded platform deployment, customization |
| **API Integration** | $25,000 - $100,000 | Custom integrations with existing systems |
| **Full Partnership** | Custom | Strategic alignment, equity consideration, deep collaboration |

**Pricing Factors:**
- Number of seats/users
- Customization requirements
- Integration complexity
- Exclusivity arrangements
- Long-term commitment (annual discounts)

### Pricing Presentation Guidelines

1. Present 2-3 options (Good/Better/Best format when appropriate)
2. Anchor with higher option first
3. Include value justification for each tier
4. Show ROI calculation if data supports it
5. Include payment terms (50% upfront typical for projects)

---

## Proposal Section Framework

### Core Sections (Always Include)

#### 1. Header
- NGM wordmark/branding
- Proposal date
- "Prepared for [Client Name]"
- Optional: Proposal validity period

#### 2. Executive Summary
2-3 sentences maximum. Format:
- What the opportunity is
- What we're proposing
- The key outcome/transformation

Example: "Based on our conversation, [Client] is positioned to become a leader in longevity medicine but needs clinical protocols and operational infrastructure to scale. This proposal outlines a 90-day engagement to develop your core service offerings and train your clinical team, enabling you to launch your longevity program with confidence."

#### 3. Understanding Your Situation
Extract from transcript:
- Current state (what they have/do now)
- Challenges (what's not working)
- Goals (where they want to be)
- Gap (what's missing)

Write in second person ("You mentioned..."). Show you listened.

#### 4. Proposed Solution
What we'll deliver:
- Clear scope of work
- Key deliverables (tangible outputs)
- Approach/methodology overview
- What's included vs. excluded

#### 5. Why NGM
Select relevant credentials and capabilities:
- Dr. V's relevant experience (choose what matches their needs)
- Platform capabilities that address their gaps
- Relevant outcomes from similar clients
- Unique fit for their specific situation

**Important:** Weave this naturally. Don't dump credentials. Connect each point to their specific needs.

#### 6. Investment
- Recommended option with price
- Alternative options if appropriate
- What's included
- Payment terms
- Value justification or ROI projection

#### 7. Next Steps
Clear, single call-to-action:
- What to do to proceed
- Timeline for response
- Contact method
- Any urgency elements (availability, pricing validity)

### Consulting-Specific Sections

#### Engagement Model
- Retainer structure (hours/month, response time)
- Meeting cadence
- Communication channels
- Deliverable schedule

#### Personal Access & Support
- Direct access to Dr. V
- Response time expectations
- Async support details

### Enterprise-Specific Sections

#### Implementation Roadmap
- Phase breakdown with timeline
- Key milestones
- Resource requirements
- Go-live expectations

#### Platform Capabilities
- Detailed feature overview relevant to their needs
- Integration specifications
- User roles and permissions
- Security/compliance details

#### Training & Onboarding
- Training curriculum overview
- Session schedule
- Certification pathway
- Ongoing support

#### ROI Projections
- Time savings calculations
- Revenue opportunity sizing
- Efficiency gains
- Payback period

### Optional Sections (Context-Dependent)

#### Case Studies
Include when:
- Client seems skeptical
- Similar client success exists
- Enterprise/larger deals

#### Timeline/Milestones
Include when:
- Project-based engagement
- Complex implementation
- Client mentioned timeline concerns

#### Team/Resources
Include when:
- Enterprise deals
- Client asked about capacity
- Multi-person delivery

#### Terms & Conditions
Include when:
- Larger engagements ($25K+)
- IP/confidentiality concerns raised
- Enterprise clients

---

## HTML Style Guide

All proposals must follow this exact styling for brand consistency.

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Proposal for [Client Name] | Next Generation Medicine</title>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600&family=Noto+Serif+JP:wght@500&display=swap" rel="stylesheet">
  <style>
    :root {
      --paper: #FFFFFF;
      --paper-alt: #FAFAF8;
      --ink-900: #0A0B0C;
      --ink-700: #1F2124;
      --ink-500: #5C626B;
      --ink-400: #8B909A;
      --line: #E5E3DE;
      --gold: #C5A572;
      --vermillion: #E03E2F;

      --space-1: 8px;
      --space-2: 12px;
      --space-3: 20px;
      --space-4: 32px;
      --space-5: 48px;
      --space-6: 72px;
      --space-7: 96px;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      font-size: 15px;
      line-height: 1.6;
      color: var(--ink-700);
      background-color: var(--paper);
      -webkit-font-smoothing: antialiased;
    }

    .container {
      max-width: 900px;
      margin: 0 auto;
      padding: clamp(20px, 5vw, 48px);
    }

    /* Typography */
    h1, h2, h3, h4 {
      font-family: 'Newsreader', 'Noto Serif JP', serif;
      color: var(--ink-900);
      font-weight: 500;
    }

    h1 {
      font-size: clamp(32px, 4vw, 42px);
      line-height: 1.2;
      margin-bottom: var(--space-4);
    }

    h2 {
      font-size: clamp(24px, 3vw, 32px);
      line-height: 1.2;
      margin-bottom: var(--space-3);
    }

    h3 {
      font-size: clamp(18px, 2.5vw, 24px);
      line-height: 1.3;
      margin-bottom: var(--space-2);
    }

    p {
      margin-bottom: var(--space-3);
    }

    /* Header */
    .header {
      background: var(--paper-alt);
      padding: var(--space-4) 0;
      border-bottom: 1px solid var(--line);
      margin-bottom: var(--space-6);
    }

    .header-inner {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 clamp(20px, 5vw, 48px);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .wordmark {
      font-family: 'Newsreader', serif;
      font-size: 18px;
      font-weight: 500;
      color: var(--ink-900);
      letter-spacing: -0.01em;
    }

    .header-meta {
      font-size: 13px;
      color: var(--ink-500);
      text-align: right;
    }

    /* Sections */
    .section {
      margin-bottom: var(--space-6);
    }

    .section-number {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      background: var(--ink-900);
      color: white;
      font-weight: 600;
      font-size: 14px;
      margin-bottom: var(--space-2);
    }

    .section-subtitle {
      font-style: italic;
      color: var(--ink-500);
      margin-bottom: var(--space-3);
    }

    /* Lists */
    ul, ol {
      margin-bottom: var(--space-3);
      padding-left: var(--space-4);
    }

    li {
      margin-bottom: var(--space-1);
    }

    /* Highlight Box */
    .highlight-box {
      background: var(--paper-alt);
      padding: var(--space-4);
      border-left: 4px solid var(--gold);
      margin: var(--space-4) 0;
    }

    /* Pricing Table */
    .pricing-table {
      width: 100%;
      border-collapse: collapse;
      margin: var(--space-4) 0;
    }

    .pricing-table th {
      text-align: left;
      padding: var(--space-2) var(--space-3);
      background: var(--paper-alt);
      border-bottom: 2px solid var(--line);
      font-weight: 600;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--ink-500);
    }

    .pricing-table td {
      padding: var(--space-3);
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }

    .pricing-table .option-name {
      font-family: 'Newsreader', serif;
      font-size: 18px;
      font-weight: 500;
      color: var(--ink-900);
    }

    .pricing-table .price {
      font-size: 24px;
      font-weight: 600;
      color: var(--ink-900);
    }

    .pricing-table .recommended {
      background: rgba(197, 165, 114, 0.1);
    }

    .badge {
      display: inline-block;
      background: var(--gold);
      color: white;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 8px;
      margin-left: var(--space-2);
    }

    /* Credentials */
    .credential-item {
      display: flex;
      gap: var(--space-2);
      margin-bottom: var(--space-2);
    }

    .credential-icon {
      color: var(--gold);
      flex-shrink: 0;
    }

    /* Timeline */
    .timeline {
      border-left: 2px solid var(--line);
      padding-left: var(--space-4);
      margin: var(--space-4) 0;
    }

    .timeline-item {
      position: relative;
      padding-bottom: var(--space-4);
    }

    .timeline-item::before {
      content: '';
      position: absolute;
      left: calc(-1 * var(--space-4) - 5px);
      top: 4px;
      width: 10px;
      height: 10px;
      background: var(--gold);
      border-radius: 50%;
    }

    .timeline-label {
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--gold);
      margin-bottom: var(--space-1);
    }

    /* CTA */
    .cta-section {
      background: var(--paper-alt);
      padding: var(--space-5);
      text-align: center;
      margin-top: var(--space-6);
    }

    .cta-button {
      display: inline-block;
      padding: 14px 28px;
      background: var(--ink-900);
      color: white;
      text-decoration: none;
      font-weight: 600;
      font-size: 14px;
      transition: all 0.3s;
    }

    .cta-button:hover {
      background: var(--vermillion);
      transform: translateY(-2px);
    }

    /* Divider */
    .divider {
      height: 1px;
      background: var(--line);
      margin: var(--space-5) 0;
    }

    /* Footer */
    .footer {
      text-align: center;
      padding: var(--space-5) 0;
      color: var(--ink-400);
      font-size: 13px;
    }

    /* Print styles */
    @media print {
      .container {
        padding: 40px;
      }

      .cta-button {
        background: var(--ink-900) !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
    }
  </style>
</head>
<body>
  <!-- Content here -->
</body>
</html>
```

### Component Patterns

See `templates/components.md` for reusable HTML patterns for each section type.

---

## Output Format

Generate a single, complete HTML file that:
1. Is immediately viewable in any browser
2. Prints cleanly to PDF
3. Contains all content inline (no external dependencies except Google Fonts)
4. Follows the exact styling defined above

Save to the specified output path, or suggest a filename like `proposal-[client-name]-[date].html`.

---

## Quality Checklist

Before finalizing, verify:

- [ ] Client name and date are correct
- [ ] Executive summary is concise (2-3 sentences max)
- [ ] "Understanding" section reflects actual transcript content
- [ ] Proposed solution matches identified needs
- [ ] Credentials selected are relevant to this specific client
- [ ] Pricing is justified and within framework ranges
- [ ] Next steps include clear call-to-action
- [ ] HTML renders correctly with proper styling
- [ ] No placeholder text remains
- [ ] Tone is professional but personable (not salesy)

---

## Anti-Patterns to Avoid

1. **Credential dumping** - Don't list all credentials; select what's relevant
2. **Generic proposals** - Every proposal should feel custom to the conversation
3. **Salesy language** - Professional confidence, not marketing hype
4. **Feature focus** - Lead with outcomes and transformation, not features
5. **Wall of text** - Use white space, headers, and visual hierarchy
6. **Vague pricing** - Be specific about what's included at each level
7. **Weak CTAs** - "Let me know what you think" is not a CTA
8. **Missing context** - Reference specific things from the transcript

---

## Example Usage

```
Invoke: proposal-generator

Input:
- Transcript: /path/to/meeting-notes.txt (or paste raw transcript)
- Client Name: Acme Health
- Type: consulting (or let it be inferred)

The skill will:
1. Check content/proposals/ for existing proposals to learn from
2. Read 1-2 recent proposals to match tone and style
3. Read and analyze the provided transcript
4. Extract client needs, pain points, goals
5. Determine appropriate scope and pricing
6. Generate styled HTML proposal
7. Save to content/proposals/proposal-acme-health-2025-12-15.html
```

### Invocation Examples

**Basic:**
```
Create a proposal for my meeting with Acme Health. Here's the transcript: [paste transcript]
```

**With file:**
```
Generate an enterprise proposal from the transcript at content/transcripts/acme-call.txt for Acme Health
```

**Specifying type:**
```
Create a consulting proposal for Dr. Smith based on our call notes. [paste transcript]
```
