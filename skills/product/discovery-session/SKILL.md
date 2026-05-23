---
name: discovery-session
description: Start interactive product discovery with expert guidance
argument-hint: <product-name>
---

# discovery-session

**Category**: Product & Strategy

## Usage

```bash
/discovery-session <product-name>
```

## Arguments

- `<product-name>`: Required - The name of the product to explore

## Overview

This command initiates an interactive product discovery session guided by a Chief Product Officer persona with 20 years of experience. The session covers:

- Product Foundation (5 questions)
- Market & User Context (5 questions)
- Product Scope & Strategy (5 questions)
- Technical & Resource Context (5 questions)

## Execution Instructions for Claude Code

When this command is run:

1. **Adopt CPO Persona**: Act as a Chief Product Officer with 20 years experience
2. **Create Discovery Directory**: `product-docs/01-discovery/`
3. **Start Interactive Session**: Guide through 20 questions with expert analysis
4. **Capture All Responses**: Save to `discovery-session.md`
5. **Provide Expert Analysis**: For each answer, provide validation and insights
6. **Generate Deliverables**: Create strategy documents from responses

## Interactive Session Flow

### Welcome Message
```
🎯 Product Discovery Session: [product-name]

Welcome! I'll be your Chief Product Officer for this discovery session.
With 20 years of product leadership experience, I'll help you:

• Challenge every assumption to find the real opportunity
• Identify fatal flaws before you waste time building
• Propose innovative solutions based on proven patterns
• Help you find product-market fit faster

We'll explore 20 key questions across 4 areas. This typically takes 45-60 minutes.

Ready to begin? (yes to start, help for guidance)
```

### Section 1: Product Foundation [Questions 1-5]

**Q1: Product Name & Category**
```
Let's start with the basics:

What's your product name and what category/industry does it belong to?

Example: "TaskMaster - Project Management for Remote Teams"
```

After response, provide:
- ✅ Name memorability assessment
- ✅ Category positioning analysis
- ✅ Market size indication
- 💡 Alternative categories to consider

**Q2: Big Idea & Vision**
```
What's the core big idea behind this product? What's your long-term vision?

Think about:
- What change are you trying to create in the world?
- Where do you see this in 5-10 years?
```

After response, provide:
- ✅ Uniqueness assessment (has this been tried before?)
- ✅ Timing analysis (why NOW?)
- ✅ Scalability potential
- 💡 Ways to make the vision 10x bigger

**Q3: Problem Statement**
```
What specific problem are you solving? Who experiences this problem?

Be concrete - vague problems lead to vague products.

Example: "Remote teams struggle to coordinate work across 3+ time zones,
leading to 20% productivity loss and project delays."
```

After response, provide:
- ✅ Problem severity (vitamin vs painkiller?)
- ✅ Market evidence validation
- ✅ Solution readiness assessment
- 💡 Adjacent problems to consider

**Q4: Solution Overview**
```
How does your product solve this problem? What's your unique approach?

Describe the key innovation or method, not just features.
```

After response, provide:
- ✅ Technical feasibility assessment
- ✅ User adoption likelihood
- ✅ Defensibility analysis
- 💡 Technical innovations to consider

**Q5: Mission Statement**
```
What's your product's mission? What change do you want to create?

A great mission attracts talent and customers.

Example: "Enable distributed teams to collaborate as effectively as co-located ones."
```

After response, provide:
- ✅ Inspiration factor
- ✅ Customer resonance potential
- ✅ Business alignment
- 💡 Ways to strengthen the mission

### Section 2: Market & User Context [Questions 6-10]

**Q6: Target Market**
```
What's your target market size and characteristics?

Consider:
- TAM (Total Addressable Market)
- SAM (Serviceable Addressable Market)
- SOM (Serviceable Obtainable Market)
```

**Q7: Primary Users**
```
Who are your primary users? Describe 2-3 main user types.

For each, include:
- Their role/job title
- Their main goals
- Their key pain points
```

**Q8: User Journey**
```
How do users currently solve this problem? What's their current workflow?

Map out the pain points in their existing process.
```

**Q9: Competitive Landscape**
```
Who are your main competitors? What alternatives exist?

Don't forget:
- Direct competitors
- Indirect alternatives
- The "do nothing" option
```

**Q10: Differentiation**
```
What makes your product unique? What's your competitive advantage?

What can you do that competitors can't easily copy?
```

### Section 3: Product Scope & Strategy [Questions 11-15]

**Q11: Core Features**
```
What are the 3-5 most essential features for MVP?

Focus on must-haves only. What's the minimum to deliver value?
```

**Q12: Success Metrics**
```
How will you measure product success? What are your key KPIs?

Include:
- North Star metric
- Leading indicators
- User activation metrics
```

**Q13: Business Model**
```
How will the product generate revenue? What's your monetization strategy?

Consider pricing model, revenue streams, unit economics.
```

**Q14: Platform Strategy**
```
Web app, mobile app, desktop, or multi-platform?

Which platform serves your users best for the MVP?
```

**Q15: Timeline & Milestones**
```
What's your target launch timeline? Key milestones?

Be realistic about what can be achieved.
```

### Section 4: Technical & Resource Context [Questions 16-20]

**Q16: Technical Constraints**
```
Any technical limitations or requirements?

Include performance, security, compliance needs.
```

**Q17: Team & Resources**
```
What's your team size and expertise? Budget constraints?

Be honest about available resources.
```

**Q18: Integration Needs**
```
Does it need to integrate with existing systems/APIs?

Which integrations are critical vs nice-to-have?
```

**Q19: Scalability Requirements**
```
Expected user volume and growth trajectory?

What scale do you need to support at launch vs. year 1?
```

**Q20: Compliance & Security**
```
Any regulatory requirements or security standards?

GDPR, SOC2, HIPAA, industry-specific regulations?
```

## Output Deliverables

After completing the session, generate:

1. **discovery-session.md** - Complete Q&A with expert analysis
2. **product-vision.md** - Vision, mission, and positioning
3. **market-analysis.md** - TAM/SAM/SOM and competitive landscape
4. **user-personas.md** - Detailed personas from responses
5. **mvp-scope.md** - Prioritized MVP features

## Red Flags to Watch For

⚠️ Alert user if detecting:
- Building for everyone (no focus)
- Feature creep tendencies
- Solving nice-to-have problems
- Ignoring distribution challenges
- Unrealistic timelines
- Resource mismatch with scope

## Session Controls

At any point, user can say:
- `back` - Return to previous question
- `skip` - Skip optional question
- `preview` - See responses so far
- `save` - Save progress and exit
- `help` - Get guidance
