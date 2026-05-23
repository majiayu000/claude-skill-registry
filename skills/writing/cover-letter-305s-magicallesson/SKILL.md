---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: cover-letter
description: ">"
version: "1.0.0"
author: Claude Office Skills Contributors
license: MIT

# Categorization
category: hr
tags:
  - cover-letter
  - job-application
  - writing
department: HR/Personal

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - create_docx
    - docx_to_pdf

# Skill Capabilities
capabilities:
  - letter_writing
  - personalization
  - professional_tone

# Language Support
languages:
  - en
  - zh
---

# Cover Letter

## Overview

This skill helps you write personalized, compelling cover letters that effectively communicate your value to potential employers and increase your chances of landing interviews.

**Use Cases:**
- Job applications
- Career transitions
- Internal transfers
- Referral introductions
- Speculative applications

## How to Use

1. Share the job posting or describe the role
2. Tell me about your relevant experience
3. Mention any specific points you want to highlight
4. I'll create a tailored cover letter

**Example prompts:**
- "Write a cover letter for this Senior PM role at Google"
- "Create a career-change cover letter from teacher to corporate trainer"
- "Draft a cover letter highlighting my Python and ML experience"
- "Help me write a referral cover letter - Sarah Chen recommended me"

## Cover Letter Structure

### The Winning Formula

```
[Header with contact info]

[Date]

[Hiring Manager Name/Title]
[Company Name]
[Address]

Dear [Name/Hiring Manager],

**Opening Hook** (1 paragraph)
- Grab attention immediately
- Show enthusiasm for the specific role
- Drop a referral name if applicable
- Mention a specific achievement or connection

**Value Proposition** (2 paragraphs)
- Match your experience to their requirements
- Provide specific, quantified accomplishments
- Show you understand their challenges
- Demonstrate cultural fit

**Why This Company** (1 paragraph)
- Show you've researched them
- Connect your values to theirs
- Explain why NOW and why HERE

**Strong Close** (1 paragraph)
- Restate your interest
- Clear call to action
- Express enthusiasm for next steps

Sincerely,
[Your Name]
```

## Cover Letter Templates

### Standard Professional

```markdown
[Your Name]
[Email] | [Phone] | [LinkedIn]
[City, State]

[Date]

[Hiring Manager Name]
[Title]
[Company Name]
[City, State]

Dear [Mr./Ms. Last Name],

I am excited to apply for the [Position] role at [Company]. With [X years] of experience in [relevant field] and a proven track record of [key achievement], I am confident I can contribute to [Company]'s mission of [company mission/goal].

In my current role at [Current Company], I have [specific accomplishment with metrics]. This experience has equipped me with [relevant skill 1] and [relevant skill 2], which directly align with your requirements for [specific requirement from job posting].

What draws me to [Company] is [specific reason - recent news, product, culture, mission]. I am particularly excited about [specific aspect of the role or company], and I believe my background in [relevant experience] positions me to make an immediate impact.

I would welcome the opportunity to discuss how my experience in [relevant area] can benefit [Company]. Thank you for considering my application. I look forward to speaking with you.

Sincerely,
[Your Name]
```

### With Referral

```markdown
Dear [Hiring Manager],

[Referrer Name] suggested I reach out regarding the [Position] opening at [Company]. After learning about the role and [Company]'s work in [area], I'm excited about the possibility of contributing to your team.

[Referrer Name] and I worked together at [Context], where they witnessed my ability to [relevant accomplishment]. They thought my experience in [relevant area] would be valuable as [Company] works toward [company goal].

[Continue with value proposition and why this company...]

I'm grateful to [Referrer Name] for the introduction and would love to discuss how I can contribute to [Company]. Thank you for your time.

Best regards,
[Your Name]
```

### Career Change

```markdown
Dear [Hiring Manager],

While my background is in [previous field], my experience has prepared me well for the [Target Position] role at [Company]. My [X years] of [transferable skill] combined with my recent [training/certification/project] in [new field] make me a strong candidate for this opportunity.

In [previous field], I developed expertise in [transferable skill 1] and [transferable skill 2]. For example, [specific example showing transferable skills]. These capabilities translate directly to [how they apply to new role].

I'm making this transition because [genuine reason connecting to the new field]. [Company]'s work in [specific area] resonates with my passion for [relevant interest], and I'm eager to bring my unique perspective to your team.

[Continue with closing...]
```

### Entry Level / New Graduate

```markdown
Dear [Hiring Manager],

As a recent graduate from [University] with a degree in [Field], I am eager to begin my career in [Industry] with [Company]. Your commitment to [company value/mission] aligns perfectly with my professional aspirations.

During my studies, I [relevant academic achievement or project]. I also gained practical experience through [internship/project/volunteer work], where I [specific accomplishment]. These experiences taught me [relevant skills] and confirmed my passion for [field].

What excites me about [Company] is [specific reason]. I am particularly drawn to [specific program, product, or aspect of company], and I am eager to contribute my [skills/energy/fresh perspective].

[Continue with closing...]
```

## Writing Tips

### Opening Lines That Work

**Good openings:**
- "After leading [Company]'s biggest product launch, I'm ready to bring that energy to [Target Company]."
- "[Referral Name] suggested I reach out – and after researching [Company]'s work on [Project], I knew I had to apply."
- "Your job posting describes my exact background: [specific match]."
- "I've admired [Company]'s approach to [specific thing] since [when/how you learned about them]."

**Avoid:**
- "I am writing to apply for..." (boring)
- "I believe I would be a great fit..." (generic)
- "To whom it may concern" (impersonal)
- Starting with your life story

### Quantify Your Achievements

| Instead of | Write |
|------------|-------|
| "Increased sales" | "Grew sales 45% YoY, adding $2M in revenue" |
| "Managed a team" | "Led 12-person team across 3 time zones" |
| "Improved efficiency" | "Reduced processing time from 5 days to 4 hours" |
| "Handled customer issues" | "Resolved 50+ customer escalations monthly with 98% satisfaction" |

### Show Company Research

Mention specific things like:
- Recent news, funding, or launches
- Company values that resonate with you
- Specific products or services you admire
- Industry challenges they're addressing
- Company culture elements you appreciate

### Common Mistakes to Avoid

1. **Repeating your resume** - Add new insights, not summaries
2. **Being too generic** - Customize for each application
3. **Focusing on what you want** - Focus on what you offer
4. **Too long** - Keep to one page, 3-4 paragraphs
5. **Typos and errors** - Proofread multiple times
6. **Wrong company name** - Double-check before sending
7. **Salary discussion** - Save for interview
8. **Negative language** - Stay positive throughout

## Output Format

```markdown
## Cover Letter

**Position:** [Role]
**Company:** [Company]
**Tailored for:** [Specific aspects addressed]

---

[Full cover letter text]

---

## Key Points Highlighted
- [Accomplishment 1 matched to requirement]
- [Accomplishment 2 matched to requirement]

## Customization Notes
- [Any suggestions for further personalization]
```

## Customization Options

Tell me your preferences:
- **Tone:** Professional, conversational, enthusiastic, confident
- **Length:** Concise (250 words), standard (350 words), detailed (450 words)
- **Focus:** Skills, achievements, cultural fit, career story
- **Industry:** Corporate, startup, nonprofit, creative, technical

## Limitations

- Cannot access actual job postings (provide the text)
- Works best with context about your experience
- Should be reviewed for accuracy of dates and details
- May need adjustment for very specialized industries
- Cannot guarantee interview callbacks

## Examples

### Example: Tech Role Cover Letter

**Input:** "Write a cover letter for a Senior Software Engineer role at Stripe. I have 6 years of Python/Go experience, built payment systems at my current company, and I'm passionate about fintech."

**Output:**

Dear Hiring Manager,

Building payment infrastructure that processes $50M+ monthly has been the highlight of my engineering career – and it's exactly why I'm excited about the Senior Software Engineer role at Stripe. Your mission to increase the GDP of the internet resonates deeply with my experience making financial technology accessible and reliable.

At [Current Company], I architected our core payment processing system using Python and Go, reducing transaction failures by 40% and improving throughput from 1,000 to 10,000 transactions per second. I led the integration with multiple payment providers and implemented fraud detection systems that prevented $2M in potential losses. This work required not just technical excellence but a deep understanding of financial regulations and user trust.

What draws me to Stripe specifically is your developer-first approach. I've used Stripe's APIs extensively and appreciate the thoughtfulness in your documentation and SDKs. The opportunity to build infrastructure that millions of businesses depend on, while working alongside engineers who've set the standard for API design, is exactly the challenge I'm seeking.

I would love to discuss how my payment systems expertise and passion for fintech can contribute to Stripe's continued growth. Thank you for considering my application.

Best regards,
[Your Name]

---

**Key Points Highlighted:**
- Direct payment systems experience (matches domain)
- Quantified achievements ($50M, 40% reduction, 10x throughput)
- Go and Python expertise (matches tech stack)
- Familiarity with Stripe products (shows research)
- Infrastructure scale mindset (matches Stripe's challenges)
