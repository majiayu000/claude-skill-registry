---
name: data-sourcing
description: Optimize provider selection, routing, and credit usage across 150+ enrichment sources for company/contact intelligence.
---

# Data Sourcing & Provider Optimization Skill

## When to Use

- Selecting provider stacks for email, phone, company, or intent enrichment
- Building or tuning waterfall sequences to improve success rates
- Auditing credit consumption or provider performance
- Designing enrichment logic for GTM ops, RevOps, or data engineering teams

## Framework

You are an expert at selecting and optimizing data providers from 150+ available options to maximize data quality while minimizing credit costs. Use this layered framework to keep enrichment predictable and efficient.

### Core Principles

1. **Quality-Cost Balance**: Optimize for highest data quality within budget constraints
2. **Smart Routing**: Route requests to providers based on input type and success probability
3. **Waterfall Logic**: Use sequential provider attempts for maximum success
4. **Caching Strategy**: Leverage cached data to reduce redundant API calls
5. **Bulk Optimization**: Process similar requests together for volume discounts

### Provider Selection Matrix

#### For Email Discovery

**Best Input Scenarios:**
- **Have LinkedIn URL**: ContactOut → RocketReach → Apollo
- **Have Name + Company**: Apollo → Hunter → RocketReach → FindyMail
- **Have Domain Only**: Hunter → Apollo → Clearbit
- **Have Email (need validation)**: ZeroBounce → NeverBounce → Debounce

**Quality Tiers:**
- **Premium** (90%+ success): ZoomInfo, BetterContact waterfall
- **Standard** (75%+ success): Apollo, Hunter, RocketReach
- **Budget** (60%+ success): Snov.io, Prospeo, ContactOut

#### For Company Intelligence

**Data Type Priority:**
- **Basic Firmographics**: Clearbit (fastest) → Ocean.io → Apollo
- **Financial Data**: Crunchbase → PitchBook → Dealroom
- **Technology Stack**: BuiltWith → HG Insights → Clearbit
- **Intent Signals**: B2D AI → ZoomInfo Intent → 6sense
- **News & Social**: Google News → Social platforms → Owler

**Industry Specialization:**
- **Startups**: Crunchbase, Dealroom, AngelList
- **Enterprise**: ZoomInfo, D&B, HG Insights
- **E-commerce**: Store Leads, BuiltWith, Shopify data
- **Healthcare**: Definitive Healthcare + compliance providers
- **Financial Services**: PitchBook, S&P Capital IQ

### Credit Optimization Strategies

#### Cost Tiers
```
Tier 0 (Free): Native operations, cached data, manual inputs
Tier 1 (0.5 credits): Validation, verification, basic lookups
Tier 2 (1-2 credits): Standard enrichments (Apollo, Hunter, Clearbit)
Tier 3 (2-3 credits): Premium data (ZoomInfo, technographics, intent)
Tier 4 (3-5 credits): Enterprise intelligence (PitchBook, custom AI)
Tier 5 (5-10 credits): Specialized services (video generation, deep AI research)
```

#### Optimization Tactics

**1. Cache Everything**
- Email: 30-day cache
- Company: 90-day cache
- Intent: 7-day cache
- Static data: Indefinite cache

**2. Batch Processing**
```python
# Process in batches for volume discounts
if record_count > 1000:
    use_provider("apollo_bulk")  # 10-30% discount
elif record_count > 100:
    use_parallel_processing()
else:
    use_standard_processing()
```

**3. Smart Waterfalls**
```python
waterfall_sequence = [
    {"provider": "cache", "credits": 0},
    {"provider": "apollo", "credits": 1.5, "stop_if_success": True},
    {"provider": "hunter", "credits": 1.2, "stop_if_success": True},
    {"provider": "bettercontact", "credits": 3, "stop_if_success": True},
    {"provider": "ai_research", "credits": 5, "last_resort": True}
]
```

### Provider-Specific Optimizations

#### Apollo.io
- **Strengths**: US B2B, LinkedIn data, phone numbers
- **Weaknesses**: International coverage, personal emails
- **Tips**: Use bulk API for 10%+ discount, batch similar companies

#### ZoomInfo
- **Strengths**: Enterprise data, org charts, intent signals
- **Weaknesses**: Expensive, SMB coverage
- **Tips**: Reserve for high-value accounts, negotiate enterprise deals

#### Hunter
- **Strengths**: Domain searches, email patterns, API reliability
- **Weaknesses**: Phone numbers, detailed contact info
- **Tips**: Best for initial domain exploration, use pattern detection

#### Clearbit
- **Strengths**: Real-time API, company data, speed
- **Weaknesses**: Email discovery rates, phone numbers
- **Tips**: Great for instant enrichment, combine with others for contacts

#### BuiltWith
- **Strengths**: Technology detection, historical data, e-commerce
- **Weaknesses**: Contact information, company financials
- **Tips**: Filter accounts by technology before enrichment

### Waterfall Strategies

#### Maximum Success Waterfall
```yaml
Priority: Success rate over cost
Sequence:
  1. BetterContact (aggregates 10+ sources)
  2. ZoomInfo (if enterprise)
  3. Apollo + Hunter + RocketReach
  4. AI web research
Expected Success: 95%+
Average Cost: 8-12 credits
```

#### Balanced Waterfall
```yaml
Priority: Good success with reasonable cost
Sequence:
  1. Apollo.io
  2. Hunter (if domain match)
  3. RocketReach (if name match)
  4. Stop or continue based on confidence
Expected Success: 80%
Average Cost: 3-5 credits
```

#### Budget Waterfall
```yaml
Priority: Minimize cost
Sequence:
  1. Cache check
  2. Hunter (domain only)
  3. Free sources (Google, LinkedIn public)
  4. Stop at first result
Expected Success: 60%
Average Cost: 1-2 credits
```

### Quality Scoring Framework

```python
def calculate_data_quality_score(data, sources):
    score = 0
    
    # Multi-source validation (30 points)
    if len(sources) > 1:
        score += min(len(sources) * 10, 30)
    
    # Data completeness (30 points)
    required_fields = ["email", "phone", "title", "company"]
    score += sum(10 for field in required_fields if data.get(field))
    
    # Verification status (20 points)
    if data.get("email_verified"):
        score += 10
    if data.get("phone_verified"):
        score += 10
    
    # Recency (20 points)
    days_old = get_data_age(data)
    if days_old < 30:
        score += 20
    elif days_old < 90:
        score += 10
    
    return score
```

### Industry-Specific Provider Selection

#### SaaS/Technology
- Primary: Apollo, Clearbit, BuiltWith
- Secondary: ZoomInfo, HG Insights
- Intent: G2, TrustRadius, 6sense

#### Financial Services
- Primary: PitchBook, ZoomInfo
- Compliance: LexisNexis, D&B
- News: Bloomberg, Reuters

#### Healthcare
- Primary: Definitive Healthcare
- Compliance: NPPES, state boards
- Standard: ZoomInfo with healthcare filters

#### E-commerce
- Primary: Store Leads, BuiltWith
- Platform-specific: Shopify, Amazon seller data
- Standard: Clearbit with e-commerce signals

### Troubleshooting Common Issues

#### Low Email Discovery Rate
- Check email patterns with Hunter
- Try personal email providers
- Use AI research for executives
- Consider LinkedIn outreach instead

#### High Credit Usage
- Audit waterfall sequences
- Increase cache TTL
- Negotiate volume deals
- Use native operations first

#### Poor Data Quality
- Add verification steps
- Cross-reference multiple sources
- Set minimum confidence thresholds
- Implement human review for critical data

### Advanced Techniques

#### Hybrid Enrichment
```python
# Combine AI and traditional providers
def hybrid_enrichment(company):
    # Fast, cheap base data
    base = clearbit_lookup(company)
    
    # AI for missing pieces
    if not base.get("description"):
        base["description"] = ai_generate_description(company)
    
    # Premium for high-value
    if is_enterprise_account(base):
        base.update(zoominfo_enrich(company))
    
    return base
```

#### Progressive Enrichment
```python
# Enrich in stages based on engagement
def progressive_enrichment(lead):
    # Stage 1: Basic (on import)
    if lead.stage == "new":
        return basic_enrichment(lead)  # 1-2 credits
    
    # Stage 2: Engaged (opened email)
    elif lead.stage == "engaged":
        return standard_enrichment(lead)  # 3-5 credits
    
    # Stage 3: Qualified (booked meeting)
    elif lead.stage == "qualified":
        return comprehensive_enrichment(lead)  # 10+ credits
```

## Templates
- **Provider Cheat Sheet**: See `references/provider_cheat_sheet.md` for provider selection.
- **Cost Calculator**: See `scripts/cost_calculator.py` for estimating credit usage.
- **Integration Code Templates**:
```javascript
// JavaScript/Node.js template
const enrichContact = async (name, company) => {
  // Check cache first
  const cached = await checkCache(name, company);
  if (cached) return cached;
  
  // Try providers in sequence
  const providers = ['apollo', 'hunter', 'rocketreach'];
  
  for (const provider of providers) {
    try {
      const result = await callProvider(provider, {name, company});
      if (result.email) {
        await saveToCache(result);
        return result;
      }
    } catch (error) {
      console.log(`${provider} failed, trying next...`);
    }
  }
  
  // Fallback to AI research
  return await aiResearch(name, company);
};
```

---

## Tips

- **Pre-build waterfalls per motion** so GTM teams can call a single orchestration command rather than juggling providers.
- **Instrument cache hit rates**; alert RevOps when cache effectiveness drops below target to avoid spike in credits.
- **Rotate premium providers** each quarter to negotiate better volume discounts and diversify coverage gaps.
- **Pair enrichment with QA hooks** (e.g., verification APIs, sampling) before syncing into CRM to prevent bad data cascades.

---

*Progressive disclosure: Load full provider details and code examples only when actively optimizing enrichment workflows*
