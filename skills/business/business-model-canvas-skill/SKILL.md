---
name: "business-model-canvas"
description: "Business model design using Alexander Osterwalder's 9 building blocks. Use when: business model, canvas, value proposition, customer segments, revenue streams, startup planning, analyze business, business strategy."
---

<objective>
Help design and analyze business models using the Business Model Canvas framework - 9 interconnected building blocks that describe how a company creates, delivers, and captures value.
</objective>

<quick_start>
**Generate a canvas:**
```
/business-model canvas for [company/idea]
```

Claude will analyze all 9 blocks:
1. Customer Segments (who are we serving?)
2. Value Propositions (what value do we deliver?)
3. Channels (how do we reach customers?)
4. Customer Relationships (how do we engage?)
5. Revenue Streams (how do we make money?)
6. Key Resources (what do we need?)
7. Key Activities (what must we do?)
8. Key Partnerships (who helps us?)
9. Cost Structure (what does it cost?)
</quick_start>

<the_9_blocks>

## 1. Customer Segments
**Question:** For whom are we creating value? Who are our most important customers?

**Types:**
| Type | Description | Example |
|------|-------------|---------|
| Mass Market | No distinction between segments | Consumer electronics |
| Niche Market | Specific, specialized segment | Luxury goods |
| Segmented | Slightly different needs | Bank retail vs private |
| Diversified | Unrelated segments | Amazon (retail + AWS) |
| Multi-sided | Interdependent segments | Credit cards (merchants + cardholders) |

## 2. Value Propositions
**Question:** What value do we deliver? Which problems do we solve?

**Value Types:**
- **Newness** - New needs customers didn't know they had
- **Performance** - Improving product/service performance
- **Customization** - Tailoring to specific needs
- **Getting the Job Done** - Simply helping get things done
- **Design** - Superior design and aesthetics
- **Brand/Status** - Value from using a specific brand
- **Price** - Offering similar value at lower price
- **Cost Reduction** - Helping customers reduce costs
- **Risk Reduction** - Reducing risks customers incur
- **Accessibility** - Making products available to new segments
- **Convenience/Usability** - Making things easier to use

## 3. Channels
**Question:** How do we reach our customers? Which channels work best?

**Channel Phases:**
1. Awareness - How do we raise awareness?
2. Evaluation - How do we help customers evaluate?
3. Purchase - How do we allow customers to purchase?
4. Delivery - How do we deliver value?
5. After-sales - How do we provide post-purchase support?

**Channel Types:**
| Type | Owned | Partner |
|------|-------|---------|
| Direct | Sales force, web sales, own stores | - |
| Indirect | - | Partner stores, wholesalers |

## 4. Customer Relationships
**Question:** What type of relationship does each segment expect?

**Relationship Types:**
- **Personal Assistance** - Human interaction during/after sale
- **Dedicated Personal Assistance** - Dedicated representative
- **Self-Service** - No direct relationship, all resources provided
- **Automated Services** - Mix of self-service + automation
- **Communities** - User communities for knowledge exchange
- **Co-creation** - Customer involvement in value creation

## 5. Revenue Streams
**Question:** For what value are customers willing to pay? How do they pay?

**Revenue Types:**
| Type | Description | Pricing |
|------|-------------|---------|
| Asset Sale | Selling ownership rights | Fixed/Dynamic |
| Usage Fee | Pay per use of service | Per unit |
| Subscription | Recurring access fee | Monthly/Annual |
| Lending/Leasing | Temporary right to use | Per period |
| Licensing | Intellectual property rights | Per license |
| Brokerage Fees | Intermediation fee | % of transaction |
| Advertising | Fees for advertising | CPM/CPC/CPA |

**Pricing Mechanisms:**
- Fixed: List price, feature-dependent, segment-dependent, volume-dependent
- Dynamic: Negotiation, yield management, real-time market, auctions

## 6. Key Resources
**Question:** What key resources does our value proposition require?

**Resource Categories:**
| Category | Examples |
|----------|----------|
| Physical | Facilities, equipment, vehicles, inventory, materials |
| Intellectual | Brands, patents, copyrights, proprietary knowledge, databases |
| Human | Creative talent, expertise, experience, skills |
| Financial | Cash, credit lines, stock options, guarantees |

## 7. Key Activities
**Question:** What key activities does our value proposition require?

**Activity Categories:**
- **Production** - Designing, making, delivering products (manufacturing)
- **Problem Solving** - Finding solutions to individual problems (consulting)
- **Platform/Network** - Platform development, service provisioning, promotion (tech)

## 8. Key Partnerships
**Question:** Who are our key partners and suppliers?

**Partnership Types:**
| Type | Purpose | Example |
|------|---------|---------|
| Strategic Alliance | Non-competitors | Airlines + Hotels |
| Coopetition | Competitors partnering | Samsung + Apple (components) |
| Joint Venture | New business development | Sony Ericsson |
| Buyer-Supplier | Assured supplies | Car manufacturers + suppliers |

**Partnership Motivations:**
- Optimization and economies of scale
- Reduction of risk and uncertainty
- Acquisition of resources and activities

## 9. Cost Structure
**Question:** What are the most important costs in our business model?

**Cost Focus:**
| Approach | Description | Example |
|----------|-------------|---------|
| Cost-Driven | Minimize costs wherever possible | Budget airlines, Walmart |
| Value-Driven | Focus on value creation | Luxury hotels, premium brands |

**Cost Characteristics:**
- **Fixed Costs** - Same regardless of volume (salaries, rent)
- **Variable Costs** - Vary with production volume (materials)
- **Economies of Scale** - Lower cost per unit with volume
- **Economies of Scope** - Lower cost with broader operations

</the_9_blocks>

<canvas_generation_algorithm>

## Canvas Generation Process

### Step 1: Identify Customer Segments
```
For each potential segment:
  - Define demographics/firmographics
  - Assess market size
  - Evaluate accessibility
  - Score attractiveness (1-10)

Prioritize: Focus on top 2-3 segments
```

### Step 2: Define Value Propositions
```
For each priority segment:
  - List jobs-to-be-done
  - Identify pains to relieve
  - Identify gains to create
  - Match to value types above

Map: segment → value proposition(s)
```

### Step 3: Design Channels
```
For each channel phase:
  - Awareness: [channels]
  - Evaluation: [channels]
  - Purchase: [channels]
  - Delivery: [channels]
  - After-sales: [channels]

Optimize: Cost vs reach vs customer preference
```

### Step 4: Define Customer Relationships
```
For each segment:
  - Determine relationship type
  - Consider acquisition cost
  - Plan retention strategy
  - Define upsell path
```

### Step 5: Establish Revenue Streams
```
For each value proposition:
  - Select revenue type
  - Choose pricing mechanism
  - Estimate willingness to pay
  - Project revenue potential
```

### Step 6: Identify Key Resources
```
For value propositions + channels + relationships:
  - List required physical resources
  - List required intellectual resources
  - List required human resources
  - List required financial resources
```

### Step 7: Define Key Activities
```
For each key resource:
  - Define activities to acquire
  - Define activities to maintain
  - Define activities to leverage

Categorize: Production / Problem Solving / Platform
```

### Step 8: Establish Key Partnerships
```
For each activity not core to business:
  - Evaluate build vs buy vs partner
  - Identify potential partners
  - Define partnership type
  - Establish terms
```

### Step 9: Calculate Cost Structure
```
Sum all costs:
  - Fixed costs (resources, overhead)
  - Variable costs (per unit)
  - Partnership costs

Determine: Cost-driven or Value-driven approach
```

</canvas_generation_algorithm>

<output_format>

## Business Model Canvas Output

### Visual Canvas Layout
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Key Partners    │ Key Activities  │ Value           │ Customer        │ Customer        │
│                 │                 │ Propositions    │ Relationships   │ Segments        │
│ • Partner 1     │ • Activity 1    │                 │                 │                 │
│ • Partner 2     │ • Activity 2    │ • Value 1       │ • Type 1        │ • Segment 1     │
│                 ├─────────────────┤ • Value 2       │ • Type 2        │ • Segment 2     │
│                 │ Key Resources   │                 │                 │                 │
│                 │                 │                 ├─────────────────┤                 │
│                 │ • Resource 1    │                 │ Channels        │                 │
│                 │ • Resource 2    │                 │                 │                 │
│                 │                 │                 │ • Channel 1     │                 │
│                 │                 │                 │ • Channel 2     │                 │
├─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┤
│ Cost Structure                    │ Revenue Streams                                     │
│                                   │                                                     │
│ Fixed: $X                         │ • Stream 1: $Y                                      │
│ Variable: $X per unit             │ • Stream 2: $Z                                      │
└───────────────────────────────────┴─────────────────────────────────────────────────────┘
```

### Table Format
| Block | Content |
|-------|---------|
| **Customer Segments** | [List segments] |
| **Value Propositions** | [List propositions] |
| **Channels** | [List channels by phase] |
| **Customer Relationships** | [List relationship types] |
| **Revenue Streams** | [List streams with pricing] |
| **Key Resources** | [List by category] |
| **Key Activities** | [List activities] |
| **Key Partnerships** | [List partners and purpose] |
| **Cost Structure** | [List costs, approach] |

</output_format>

<validation_questions>

## Canvas Validation Checklist

### Customer Segments
- [ ] Are segments clearly defined and distinct?
- [ ] Is market size quantified?
- [ ] Are they profitable to serve?

### Value Propositions
- [ ] Does it solve a real problem or satisfy a need?
- [ ] Is it differentiated from competitors?
- [ ] Is value clearly articulated?

### Channels
- [ ] Are channels cost-efficient?
- [ ] Do they reach target segments effectively?
- [ ] Are they integrated across phases?

### Customer Relationships
- [ ] Do relationships match segment expectations?
- [ ] Are acquisition costs sustainable?
- [ ] Is there a retention strategy?

### Revenue Streams
- [ ] Are customers willing to pay?
- [ ] Is pricing competitive yet profitable?
- [ ] Are revenue streams diversified?

### Key Resources
- [ ] Are all critical resources identified?
- [ ] Are intellectual assets protected?
- [ ] Is human capital sustainable?

### Key Activities
- [ ] Are activities aligned with value proposition?
- [ ] Are processes documented and scalable?
- [ ] Is quality maintained?

### Key Partnerships
- [ ] Are partnerships strategically valuable?
- [ ] Are dependencies manageable?
- [ ] Are terms favorable?

### Cost Structure
- [ ] Are all costs accounted for?
- [ ] Is the model profitable at scale?
- [ ] Are there cost optimization opportunities?

</validation_questions>

<canvas_metrics>

## Canvas Health Metrics

### Viability Score (0-100)
```
Customer fit:     (segment_clarity + value_alignment) / 2 × 20
Channel efficiency: (reach + cost_efficiency) / 2 × 15
Relationship depth: (retention + satisfaction) / 2 × 15
Revenue potential:  (streams_diversity + pricing_power) / 2 × 20
Cost efficiency:    (margin + scalability) / 2 × 15
Resource strength:  (capabilities + sustainability) / 2 × 15
──────────────────────────────────────────────────────────────
Total:             Sum of above (max 100)
```

### Key Ratios
| Ratio | Formula | Healthy Range |
|-------|---------|---------------|
| CAC | Total acquisition cost / New customers | Industry-dependent |
| LTV:CAC | Lifetime value / Acquisition cost | > 3:1 |
| Gross Margin | (Revenue - COGS) / Revenue | > 50% for SaaS |
| Burn Rate | Monthly cash outflow | < 1/12 of runway |

</canvas_metrics>

<example_session>

## Example: AI-Powered CRM Startup

**User:** Create a business model canvas for an AI-powered CRM for small businesses

### Customer Segments
- **Primary:** Small businesses (10-50 employees) in service industries
- **Secondary:** Solopreneurs and freelancers
- **Characteristics:** Tech-savvy, growth-oriented, limited IT resources

### Value Propositions
- AI automates data entry from emails/calls (saves 5+ hours/week)
- Predictive lead scoring (increases close rate 20%)
- Natural language queries ("Show my hottest leads in Texas")
- Affordable pricing (1/3 of enterprise CRM cost)

### Channels
- **Awareness:** Content marketing, SEO, partner referrals
- **Evaluation:** Free trial, demo videos, ROI calculator
- **Purchase:** Self-service online checkout
- **Delivery:** Cloud SaaS, browser + mobile apps
- **After-sales:** In-app chat, knowledge base, email support

### Customer Relationships
- **Self-service:** Most interactions automated
- **Automated:** AI-powered onboarding, tips, alerts
- **Community:** User forum, template sharing
- **Personal:** High-touch for annual plans (10+ seats)

### Revenue Streams
- **Subscription:** $29/user/month (monthly) or $19/user/month (annual)
- **Premium Features:** AI analytics add-on +$10/user/month
- **Integration Marketplace:** 20% rev share on partner integrations

### Key Resources
- Proprietary AI/ML models (NLP, prediction)
- Cloud infrastructure (AWS/GCP)
- Engineering team (10 FTEs)
- Customer success team (3 FTEs)

### Key Activities
- AI model training and improvement
- Platform development and maintenance
- Customer acquisition and onboarding
- Integration partnerships

### Key Partnerships
- Cloud providers (AWS, GCP) - infrastructure
- Communication platforms (Twilio, email APIs) - integrations
- Accounting software (QuickBooks, Xero) - data sync
- Referral partners (consultants, VARs) - distribution

### Cost Structure
- **Fixed:** Salaries ($800K/yr), office ($50K/yr), tools ($30K/yr)
- **Variable:** Cloud costs ($2/user/month), support ($1/user/month)
- **Approach:** Value-driven (premium AI features justify pricing)

### Canvas Score: 78/100
- Customer fit: 18/20 (strong segment-value match)
- Channel efficiency: 12/15 (need more paid acquisition)
- Relationship depth: 11/15 (automation good, retention TBD)
- Revenue potential: 16/20 (pricing competitive, upsell path clear)
- Cost efficiency: 12/15 (good unit economics)
- Resource strength: 9/15 (AI talent competitive market)

</example_session>

<activation_triggers>
**This skill activates for:**
- "business model canvas"
- "business model for [company]"
- "value proposition for"
- "customer segments"
- "revenue model"
- "startup canvas"
- "analyze this business"
- "9 building blocks"
- "Osterwalder canvas"
</activation_triggers>
