---
skill: 'tool-evaluation'
version: '2.0.0'
updated: '2025-12-31'
category: 'technical-integration'
complexity: 'intermediate'
prerequisite_skills: []
composable_with:
  - 'financial-modeling'
  - 'risk-assessment'
  - 'vendor-negotiation'
---

# Tool Evaluation Skill

## Overview
Structured methodology for objectively evaluating, comparing, and selecting AI tools for vendor replacement initiatives, ensuring data-driven decisions.

## Evaluation Framework

### Evaluation Criteria

**Core Dimensions (80% of score):**

1. **Functionality (25%):** Does it do what we need?
   - Core feature completeness
   - Use case coverage
   - Accuracy and quality
   - Advanced capabilities

2. **Cost (20%):** Is it affordable?
   - Pricing model (per-seat, usage-based, enterprise)
   - Total cost of ownership (TCO)
   - ROI projections
   - Hidden costs

3. **Integration (15%):** How hard to implement?
   - Setup complexity
   - API quality
   - IDE/tool compatibility
   - Technical requirements

4. **Performance (10%):** Is it fast and reliable?
   - Response time/latency
   - Throughput capacity
   - Uptime and availability
   - Scalability

5. **Vendor (10%):** Is the company reliable?
   - Financial stability
   - Product maturity
   - Customer base
   - Roadmap clarity

**Secondary Dimensions (20% of score):**

6. **Support (5%):** Help when needed?
   - Documentation quality
   - Support responsiveness
   - Community size
   - Training resources

7. **Security & Compliance (10%):** Enterprise-ready?
   - Security posture (SOC2, ISO)
   - Compliance support (GDPR, HIPAA)
   - Data privacy practices
   - Audit capabilities

8. **Flexibility (5%):** Can we customize/control?
   - Configuration options
   - Customization capability
   - Data portability
   - Lock-in risk

### Scoring Methodology

**Rating Scale (1-10):**
- 9-10: Exceptional, best-in-class
- 7-8: Very good, meets needs well
- 5-6: Acceptable, some limitations
- 3-4: Marginal, significant gaps
- 1-2: Poor, does not meet needs

**Weighting:**
- Multiply raw score by weight percentage
- Sum weighted scores for total
- Example: Functionality 8/10 × 25% = 2.0 points

**Overall Score:**
- 8.5-10.0: Highly Recommended
- 7.0-8.4: Recommended
- 5.5-6.9: Conditional (with mitigations)
- 4.0-5.4: Not Recommended
- <4.0: Reject

### Tool Comparison Matrix Template

```markdown
## AI Tool Comparison: [Category]

**Date:** [Evaluation date]
**Evaluators:** [Names]
**Use Case:** [Specific scenario]

### Quick Comparison

| Criterion | Weight | Tool A | Tool B | Tool C |
|-----------|--------|--------|--------|--------|
| **Functionality** | 25% | 8/10 (2.0) | 7/10 (1.75) | 9/10 (2.25) |
| **Cost** | 20% | 6/10 (1.2) | 8/10 (1.6) | 7/10 (1.4) |
| **Integration** | 15% | 9/10 (1.35) | 6/10 (0.9) | 7/10 (1.05) |
| **Performance** | 10% | 8/10 (0.8) | 9/10 (0.9) | 7/10 (0.7) |
| **Vendor** | 10% | 8/10 (0.8) | 7/10 (0.7) | 6/10 (0.6) |
| **Support** | 5% | 7/10 (0.35) | 8/10 (0.4) | 6/10 (0.3) |
| **Security** | 10% | 9/10 (0.9) | 8/10 (0.8) | 7/10 (0.7) |
| **Flexibility** | 5% | 6/10 (0.3) | 7/10 (0.35) | 8/10 (0.4) |
| **TOTAL** | **100%** | **7.70** | **7.40** | **7.40** |
| **Verdict** | | **Recommended** | Recommended | Recommended |

### Detailed Analysis

**Tool A (Score: 7.70):**
- **Strengths:** Best integration, strong security, proven vendor
- **Weaknesses:** Higher cost, less flexible
- **Best for:** Enterprise deployment, security-conscious orgs
- **Cost:** $39/user/month enterprise

**Tool B (Score: 7.40):**
- **Strengths:** Affordable, fast performance, good support
- **Weaknesses:** Weaker integration, newer vendor
- **Best for:** Cost-conscious teams, high-volume usage
- **Cost:** $25/user/month + usage

**Tool C (Score: 7.40):**
- **Strengths:** Top functionality, most flexible
- **Weaknesses:** Newer vendor, security not SOC2 yet
- **Best for:** Innovative features, customization needs
- **Cost:** $30/user/month

### Recommendation

**Primary Choice:** Tool A
- **Rationale:** Best overall fit for enterprise requirements, strong integration and security despite higher cost
- **Confidence:** High (thorough evaluation)
- **Timeline:** Ready to deploy immediately

**Alternative:** Tool B if budget constrained
**Not Recommended:** Tool C until SOC2 certification
```

## Tool Category Evaluations

### Code Generation Tools

**Evaluation Criteria:**

```markdown
## GitHub Copilot vs. Cursor vs. Codeium

### Functionality Comparison

| Feature | Copilot | Cursor | Codeium |
|---------|---------|--------|---------|
| **Inline suggestions** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Multi-line completion** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Chat interface** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Codebase understanding** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Multi-file editing** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Terminal integration** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |

### Cost Comparison

| Plan | Copilot | Cursor | Codeium |
|------|---------|--------|---------|
| **Individual** | $10/mo | $20/mo | Free |
| **Business** | $19/mo | $40/mo | $12/mo |
| **Enterprise** | $39/mo | Custom | $30/mo |

### Integration

| IDE | Copilot | Cursor | Codeium |
|-----|---------|--------|---------|
| **VS Code** | Native | Fork | Extension |
| **JetBrains** | Plugin | No | Plugin |
| **Visual Studio** | Plugin | No | Plugin |
| **Vim/Neovim** | Plugin | No | Plugin |

### Language Support

All three support 30+ languages, but quality varies:
- **Best for Python:** Copilot, Cursor
- **Best for JavaScript/TS:** Copilot, Cursor
- **Best for Go:** Copilot
- **Best for Java:** Copilot, Codeium
- **Best for C++:** Copilot

### Verdict

**GitHub Copilot:**
- **Best for:** Broad language support, enterprise adoption
- **Score:** 8.5/10
- **Strengths:** Most mature, best language coverage, enterprise support
- **Weaknesses:** Less advanced codebase understanding than Cursor

**Cursor:**
- **Best for:** Modern workflows, codebase-aware editing
- **Score:** 8.8/10
- **Strengths:** Best codebase understanding, innovative features
- **Weaknesses:** VS Code only, newer vendor

**Codeium:**
- **Best for:** Budget-conscious teams, free tier
- **Score:** 7.5/10
- **Strengths:** Free option, good performance
- **Weaknesses:** Less advanced features, smaller community
```

### LLM API Comparison

**GPT-4 vs. Claude vs. Gemini:**

```markdown
## LLM API Selection Guide

### Capability Matrix

| Capability | GPT-4 Turbo | Claude 3.5 Sonnet | Gemini 1.5 Pro |
|------------|-------------|-------------------|----------------|
| **Code generation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Code review** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Data analysis** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Reasoning** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Following instructions** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Context handling** | ⭐⭐⭐⭐ (128K) | ⭐⭐⭐⭐⭐ (200K) | ⭐⭐⭐⭐⭐ (2M) |

### Pricing (as of Dec 2025)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| **GPT-4 Turbo** | $10 | $30 |
| **GPT-4o** | $2.50 | $10 |
| **Claude 3.5 Sonnet** | $3 | $15 |
| **Claude 3.5 Haiku** | $0.80 | $4 |
| **Gemini 1.5 Pro** | $3.50 | $10.50 |
| **Gemini 1.5 Flash** | $0.075 | $0.30 |

### Speed (Tokens per second)

| Model | TPS | Latency |
|-------|-----|---------|
| **GPT-4 Turbo** | ~40 | Medium |
| **GPT-4o** | ~80 | Low |
| **Claude 3.5 Sonnet** | ~50 | Medium |
| **Gemini 1.5 Pro** | ~60 | Low-Medium |

### Use Case Recommendations

**Code Generation:**
- **Primary:** Claude 3.5 Sonnet (best reasoning)
- **Alternative:** GPT-4 Turbo
- **Budget:** GPT-4o mini or Claude Haiku

**Code Review:**
- **Primary:** Claude 3.5 Sonnet (thorough analysis)
- **Alternative:** GPT-4 Turbo

**Documentation:**
- **Primary:** GPT-4 Turbo (excellent writing)
- **Alternative:** Claude 3.5 Sonnet
- **Bulk:** GPT-4o (cost-effective)

**Data Analysis:**
- **Primary:** Gemini 1.5 Pro (multimodal, charts)
- **Alternative:** Claude 3.5 Sonnet

**Long Context (>50K tokens):**
- **Primary:** Gemini 1.5 Pro (2M context)
- **Alternative:** Claude 3.5 Sonnet (200K)

### Multi-Provider Strategy

**Recommended Approach:**
```python
# Primary: Claude 3.5 Sonnet for most tasks
primary_model = "claude-3-5-sonnet-20241022"

# Fallback: GPT-4 Turbo if Claude unavailable
fallback_model = "gpt-4-turbo"

# Bulk/high-volume: GPT-4o for cost efficiency
bulk_model = "gpt-4o"

# Long context: Gemini 1.5 Pro for >100K tokens
long_context_model = "gemini-1.5-pro"
```

**Benefits:**
- Reduced vendor lock-in
- Best-of-breed for each use case
- Redundancy if provider down
- Cost optimization

**Tradeoffs:**
- More complex integration
- Higher management overhead
- Inconsistent outputs across models
```

## Proof-of-Concept Framework

### POC Planning Template

```markdown
## AI Tool POC Plan: [Tool Name]

### Objectives
**Primary Goal:** Determine if [Tool] can replace [Vendor/Process]

**Success Criteria:**
- [ ] Quality: Meets or exceeds current baseline (≥95%)
- [ ] Speed: [X]% faster than current approach
- [ ] Cost: ≤ $[Y] per [unit]
- [ ] Adoption: Team satisfaction ≥ 4/5
- [ ] ROI: Payback period < [Z] months

### Scope
**Duration:** 4 weeks
**Team:** 3-5 people (early adopters)
**Tasks:** 5-10 representative use cases
**Budget:** $[X] (tool costs + time)

### Week 1: Setup & Training
- [ ] Tool procurement and access
- [ ] Team training (4 hours)
- [ ] Environment configuration
- [ ] Success metrics baseline
- [ ] Kickoff meeting

### Week 2-3: Testing
**Week 2 Tasks:**
1. [Task 1: Description]
   - Owner: [Name]
   - Expected: [Outcome]
   - Metrics: [Quality, time, cost]

2. [Task 2: Description]
   - Owner: [Name]
   - Expected: [Outcome]
   - Metrics: [Quality, time, cost]

[...continue for 5-10 tasks]

**Week 3:** Continue testing, gather feedback

### Week 4: Evaluation
- [ ] Results analysis
- [ ] Cost calculation
- [ ] ROI projection
- [ ] Team feedback collection
- [ ] Final recommendation report
- [ ] Go/no-go decision

### Risk Mitigation
- **Risk:** Tool doesn't perform as expected
  - **Mitigation:** Have fallback options evaluated
- **Risk:** Team rejects tool
  - **Mitigation:** Involve them in selection, address concerns
- **Risk:** Integration issues
  - **Mitigation:** Technical spike before POC
```

### POC Evaluation Scorecard

```markdown
## POC Results: [Tool Name]

### Quantitative Results

| Metric | Baseline | POC Result | Change | Target | Status |
|--------|----------|------------|--------|--------|--------|
| **Task completion time** | 8 hours | 3 hours | -62% | -50% | ✅ Exceeded |
| **Quality score** | 92% | 96% | +4% | ≥95% | ✅ Met |
| **Cost per task** | $400 | $120 | -70% | <$200 | ✅ Met |
| **Error rate** | 5% | 2% | -60% | <5% | ✅ Met |

### Qualitative Results

**Team Satisfaction:** 4.2/5 (Target: ≥4.0) ✅

**Feedback Themes:**
- ✅ "Saves time on repetitive tasks"
- ✅ "Better than expected quality"
- ⚠️ "Learning curve first few days"
- ⚠️ "Some edge cases need manual work"

### Cost Analysis

**POC Costs:**
- Tool subscription (1 month): $500
- Training time: $2,000
- Integration/setup: $1,500
- **Total POC cost:** $4,000

**Projected Annual Costs:**
- Tool subscription: $6,000/year
- Training (one-time): $2,000
- Ongoing support: $1,000/year
- **Total annual:** $9,000

**Current Vendor Cost:** $48,000/year
**Projected Savings:** $39,000/year (81%)
**Payback Period:** 1.5 months

### Risks & Limitations

**Identified Risks:**
- Tool struggles with [specific scenario]
- Requires human review for [situation]
- Integration with [system] needs work

**Mitigation Plans:**
- Keep manual process for [scenario]
- Implement review workflow
- Schedule integration sprint

### Recommendation

**Decision:** ✅ **PROCEED TO FULL DEPLOYMENT**

**Rationale:**
- All success criteria met or exceeded
- Strong team acceptance
- Clear ROI (81% cost reduction)
- Risks are manageable

**Next Steps:**
1. Procurement approval for full team (week 1)
2. Training rollout plan (weeks 2-4)
3. Phased deployment (weeks 4-8)
4. Monitor and optimize (ongoing)

**Confidence Level:** High (8/10)
```

## Build vs. Buy Decision Framework

### Decision Matrix

```markdown
## Build vs. Buy Analysis: [Capability]

### Evaluation Criteria

| Factor | Weight | Build | Buy | Winner |
|--------|--------|-------|-----|--------|
| **Time to Market** | 20% | 6 months (4/10) | 1 month (10/10) | Buy |
| **Initial Cost** | 15% | $200K (3/10) | $20K (9/10) | Buy |
| **Ongoing Cost** | 15% | $50K/yr (7/10) | $80K/yr (5/10) | Build |
| **Customization** | 15% | Full (10/10) | Limited (5/10) | Build |
| **Competitive Advantage** | 10% | Differentiator (9/10) | Commodity (3/10) | Build |
| **Expertise Available** | 10% | Need to hire (4/10) | Not needed (9/10) | Buy |
| **Maintenance** | 10% | Our responsibility (5/10) | Vendor handles (9/10) | Buy |
| **Lock-in Risk** | 5% | No lock-in (10/10) | Vendor dependent (4/10) | Build |
| **TOTAL** | **100%** | **6.25/10** | **7.40/10** | **Buy** |

### Recommendation: BUY (off-the-shelf)

**Key Factors:**
- Time to market critical (6 months vs. 1 month)
- Not a competitive differentiator
- Build cost too high ($200K upfront)
- Lack ML expertise in-house

**Build would make sense if:**
- We had ML team already
- This was core competitive advantage
- Off-shelf solutions inadequate
- We had 6+ month timeline
```

### When to Build vs. Buy

**Build Custom When:**
✅ Core competitive differentiator
✅ Unique requirements not met by market
✅ High volume (custom cheaper at scale)
✅ You have ML expertise in-house
✅ Data privacy absolute requirement
✅ Time to market not critical

**Buy Off-the-Shelf When:**
✅ Commodity capability (everyone needs it)
✅ Fast time to market critical
✅ Limited ML expertise
✅ Cost-conscious (buy usually cheaper initially)
✅ Good solutions exist
✅ Want vendor support and updates

**Hybrid Approach:**
- Buy base platform, customize on top
- Use APIs but build abstraction layer
- Open-source model + custom hosting

## Best Practices

### Do's
✅ Define clear evaluation criteria upfront
✅ Weight criteria based on priorities
✅ Test with real use cases, not demos
✅ Involve actual users in evaluation
✅ Run POCs before committing
✅ Consider total cost of ownership (TCO)
✅ Check vendor financials and stability
✅ Plan for multi-provider strategy

### Don'ts
❌ Rely only on vendor demos
❌ Skip POC to save time
❌ Ignore hidden costs (integration, training)
❌ Choose based on hype alone
❌ Lock into long contracts before validation
❌ Forget to evaluate vendor stability
❌ Neglect security and compliance review
❌ Compare only on price

This skill ensures AI tool selection decisions are data-driven, objective, and aligned with business needs - avoiding costly mistakes.
