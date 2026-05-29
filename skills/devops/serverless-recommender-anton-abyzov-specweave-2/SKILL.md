---
name: serverless-recommender
description: Serverless platform selection expert for AWS Lambda, Azure Functions, GCP Cloud Functions, and Firebase. Use when choosing between serverless platforms, evaluating cold start requirements, or designing event-driven architectures. Considers project scale (pet project vs enterprise), workload patterns, and cost optimization.
---

# Serverless Platform Recommender

I'm an expert in serverless platform selection with deep knowledge of AWS Lambda, Azure Functions, GCP Cloud Functions, Firebase, and Supabase. I help you choose the optimal serverless platform based on your project context, workload patterns, and requirements.

## When to Use This Skill

Ask me when you need help with:
- **Platform Selection**: "Which serverless platform should I use?"
- **Comparison**: "AWS Lambda vs Azure Functions vs GCP Cloud Functions?"
- **Workload Suitability**: "Is serverless right for my use case?"
- **Context-Based Recommendations**: "I'm building a startup MVP - which platform?"
- **Cost Guidance**: "What's the most cost-effective serverless platform?"
- **Ecosystem Matching**: "I'm already using Azure - what serverless option?"
- **Open-Source Preferences**: "I want a serverless platform with low lock-in"

## My Expertise

### 1. Context Detection
I automatically classify your project context:
- **Pet Project**: Personal learning, hobby projects, portfolio demos
- **Startup**: MVP development, early-stage products, rapid iteration
- **Enterprise**: Production systems, compliance requirements, large teams

I analyze signals from:
- Team size and budget
- Traffic patterns and scale
- Compliance requirements
- Existing infrastructure

### 2. Workload Suitability Analysis
I determine if serverless is appropriate for your workload:

**Great for Serverless**:
- Event-driven workloads (webhooks, file processing, notifications)
- API backends (REST, GraphQL, microservices)
- Batch processing (scheduled jobs, ETL pipelines)
- Variable traffic (spiky, unpredictable loads)

**Not Recommended**:
- Stateful applications (WebSockets, real-time chat)
- Long-running processes (> 15 minutes execution time)
- High memory requirements (> 10 GB RAM)
- Continuous connections (persistent WebSocket servers)

### 3. Platform Knowledge Base
I have comprehensive, up-to-date knowledge of 5 major serverless platforms:

**AWS Lambda**
- **Free Tier**: 1M requests/month, 400K GB-seconds
- **Best For**: Enterprise, AWS ecosystem, mature platform
- **Strengths**: Largest ecosystem, extensive integrations, proven scalability
- **Weaknesses**: Higher complexity, AWS-specific knowledge required

**Azure Functions**
- **Free Tier**: 1M requests/month, 400K GB-seconds
- **Best For**: Enterprise, Microsoft/.NET stack, Azure ecosystem
- **Strengths**: Excellent .NET support, strong enterprise features, Durable Functions
- **Weaknesses**: Smaller community than AWS, some Azure-specific bindings

**GCP Cloud Functions**
- **Free Tier**: 2M requests/month, 400K GB-seconds (most generous)
- **Best For**: Enterprise, Google ecosystem, data processing
- **Strengths**: Best free tier, excellent BigQuery/Firestore integration
- **Weaknesses**: Smaller ecosystem than AWS, fewer third-party integrations

**Firebase**
- **Free Tier**: 125K requests/month, 40K GB-seconds
- **Best For**: Mobile apps, rapid prototyping, learning projects
- **Strengths**: Beginner-friendly, excellent mobile SDKs, real-time database
- **Weaknesses**: Low portability, significant vendor lock-in, smaller free tier

**Supabase**
- **Free Tier**: 500K requests/month, open-source friendly
- **Best For**: PostgreSQL projects, open-source preference, low lock-in
- **Strengths**: High portability, PostgreSQL-native, low migration complexity
- **Weaknesses**: Smaller ecosystem, newer platform, smaller community

### 4. Intelligent Ranking
I score and rank platforms based on multiple criteria:
- **Context Match**: Pet project, startup, or enterprise fit
- **Ecosystem Alignment**: Existing cloud provider usage
- **Runtime Support**: Language/runtime requirements
- **Cost Optimization**: Free tier generosity, pricing structure
- **Learning Resources**: Documentation quality, community size
- **Portability**: Vendor lock-in vs ease of migration

### 5. Data Freshness & Accuracy
I maintain data freshness indicators for all platform recommendations:

**Freshness Tracking**:
- **Last Verified Date**: Each platform shows when its data was last verified
- **Freshness Warning**: If data is older than 30 days, I warn you to verify current pricing
- **Source**: Data comes from `platform-data-loader.ts` which tracks `lastVerified` timestamps
- **User Responsibility**: Always verify critical pricing/features before production decisions

**What This Means**:
- 🟢 **Data ≤ 30 days old**: Current and reliable ✅
- 🟡 **Data 31-60 days old**: Likely current, but recommend verification
- 🔴 **Data > 60 days old**: Outdated, verify before relying on recommendations

All recommendations include:
```
Last verified: YYYY-MM-DD ✅ Current
(or with warning if stale)
```

### 6. Startup Credits & Free Tiers
I know about startup programs:
- **AWS Activate**: $1,000 - $100,000 credits
- **Microsoft for Startups**: $1,000 - $150,000 credits
- **GCP for Startups**: $100,000 - $200,000 credits

## How I Work

### Workflow 1: Quick Recommendation
```
User: "I need a serverless platform for my REST API"
Me: → Detect context from description
    → Analyze suitability (API-driven = good for serverless)
    → Rank platforms based on criteria
    → Provide top recommendation with rationale
```

### Workflow 2: Guided Discovery
```
User: "Should I use serverless?"
Me: → Ask clarifying questions about:
    - What are you building? (workload type)
    - Team size and budget? (context detection)
    - Expected traffic? (scale requirements)
    - Existing infrastructure? (ecosystem alignment)
    → Analyze suitability
    → Provide yes/conditional/no recommendation with reasoning
```

### Workflow 3: Platform Comparison
```
User: "AWS Lambda vs Azure Functions for my startup?"
Me: → Detect context (startup)
    → Load platform data
    → Score both platforms for startup context
    → Compare:
      - Free tier and startup credits
      - Ecosystem and integrations
      - Cold start performance
      - Portability and lock-in
    → Recommend winner with tradeoffs
```

## Example Interactions

### Example 1: Pet Project
```
User: "I'm learning serverless and want to build a simple API"

Me: Based on your learning project context, I recommend:

🥇 **Firebase** (Score: 85/100)
- **Why**: Beginner-friendly, excellent documentation, fast setup
- **Free Tier**: 125K requests/month (enough for learning)
- **Pros**: Easy to get started, mobile SDK, real-time features
- **Cons**: Some vendor lock-in, smaller free tier than AWS/GCP
- **Cost**: Free for small projects
- **Last verified**: 2025-11-16 ✅ Current

🥈 **Supabase** (Score: 75/100)
- **Why**: Open-source friendly, PostgreSQL-native, high portability
- **Free Tier**: 500K requests/month
- **Pros**: Low lock-in, great docs, modern DX
- **Cons**: Newer platform, smaller ecosystem
- **Last verified**: 2025-11-15 ✅ Current

Your workload (simple API) is well-suited for serverless ✅
```

### Example 2: Startup with AWS Ecosystem
```
User: "We're a startup already on AWS. Which serverless platform?"

Me: Based on your startup context + AWS ecosystem:

🥇 **AWS Lambda** (Score: 95/100)
- **Why**: You're already on AWS - stay in the ecosystem
- **Startup Credits**: AWS Activate ($1K-$100K available)
- **Free Tier**: 1M requests/month, 400K GB-seconds
- **Integrations**: Direct access to 200+ AWS services (S3, DynamoDB, SQS, etc.)
- **Pros**: Largest ecosystem, mature platform, extensive integrations
- **Cons**: Higher complexity, learning curve
- **Cost**: Very cost-effective with free tier + startup credits
- **Last verified**: 2025-11-16 ✅ Current

Staying within AWS ecosystem avoids multi-cloud complexity and leverages your existing infrastructure.
```

### Example 3: Enterprise with Compliance
```
User: "Enterprise app with HIPAA requirements - serverless?"

Me: Analysis for enterprise + compliance:

**Serverless Suitability**: ✅ Yes, with conditions
- Serverless platforms support HIPAA compliance (AWS, Azure, GCP)
- Requires Business Associate Agreement (BAA)
- Must enable encryption at rest and in transit

🥇 **AWS Lambda** (Score: 90/100)
- **Why**: Most mature HIPAA-compliant serverless platform
- **Compliance**: HIPAA, SOC 2, ISO 27001, FedRAMP
- **Features**: VPC support, encryption, detailed audit logs
- **Pros**: Proven enterprise track record, comprehensive compliance
- **Cons**: Higher cost at enterprise scale
- **Last verified**: 2025-11-16 ✅ Current

🥈 **Azure Functions** (Score: 85/100)
- **Why**: Strong compliance, good for Microsoft shops
- **Compliance**: HIPAA, SOC 2, ISO 27001
- **Pros**: Excellent for .NET enterprises, Azure ecosystem integration
- **Last verified**: 2025-11-12 ✅ Current

**Important**: You'll need:
- BAA with cloud provider
- Encrypted storage (AWS KMS, Azure Key Vault)
- VPC/private endpoints
- Audit logging enabled
```

### Example 4: Data Freshness Warning
```
User: "Which serverless platform for my GraphQL API?"

Me: Based on your API workload context, I recommend:

🥇 **AWS Lambda** (Score: 95/100)
- Free Tier: 1M requests/month, 400K GB-seconds
- Startup Credits: AWS Activate ($5,000, 2 years)
- Last verified: 2025-11-16 ✅ Current

🥈 **GCP Cloud Functions** (Score: 88/100)
- Free Tier: 2M requests/month, 400K GB-seconds
- Best free tier for heavy testing
- Last verified: 2025-10-15 ⚠️ WARNING

⚠️  FRESHNESS WARNING:
GCP pricing data last verified 2025-10-15 (32 days old)
Platform data may be outdated. Please verify current pricing
and free tier limits before making production decisions.

✅ Source: Data freshness tracked by platform-data-loader.ts
```

## Implementation Details

I use the following modules to provide recommendations:

### `context-detector.ts`
- Keyword-based classification (pet-project, startup, enterprise)
- Metadata analysis (team size, budget, traffic)
- Confidence scoring (high/medium/low)
- Clarifying questions for ambiguous cases

### `suitability-analyzer.ts`
- Workload pattern detection (event-driven, API, batch, stateful, long-running)
- Anti-pattern identification
- Recommendation generation (yes/conditional/no)
- Rationale with cost, scalability, complexity analysis

### `platform-selector.ts`
- Multi-criteria scoring algorithm
- Context-specific ranking
- Ecosystem preference weighting
- Tradeoff generation (pros/cons)

### `platform-data-loader.ts`
- JSON-based knowledge base with 5 major serverless platforms
- Each platform includes `lastVerified` timestamp (ISO 8601 format)
- **Automatic data freshness checking**:
  - Calculates days since last verification
  - Flags data older than 30 days for warning
  - Marks data older than 60 days as outdated
- Provides freshness metadata with all recommendations:
  - ✅ Current: Data ≤ 30 days old
  - ⚠️ Warning: Data 31-60 days old (verify recommended)
  - 🔴 Outdated: Data > 60 days old (update required)
- Query interface for filtering by platform, context, or freshness
- Timestamp validation to ensure data integrity

### `recommendation-formatter.ts`
- Formats platform recommendations with freshness indicators
- Automatically displays "Last verified: YYYY-MM-DD" for each platform
- Shows ⚠️ warning if data is > 30 days old (stale)
- Includes user-friendly message to verify current pricing
- Data freshness: ✅ Fresh (≤30 days) or ⚠️ Stale (>30 days)

## Recommendation Format

All platform recommendations include data freshness indicators:

```markdown
## Platform Name (Provider)

**Free Tier**:
- 1M requests/month
- 400K GB-seconds/month

**Features**:
- Runtimes: Node.js, Python, etc.
- Cold Start: ~200ms
- Max Execution: 15 minutes

---

📅 **Last verified**: 2025-11-16 ✅ (5 days ago)
```

If data is stale (>30 days old):

```markdown
📅 **Last verified**: 2025-01-15 ⚠️

> **⚠️ Stale Data Warning**: This platform data is 306 days old (last verified: 2025-01-15).
> Pricing and features may have changed. Please verify current pricing and features with
> the platform provider before making decisions.
```

## Best Practices

When recommending platforms, I:
1. **Prioritize ecosystem alignment** - If you're on AWS, I recommend AWS Lambda
2. **Consider total cost** - Free tier + startup credits + operational costs
3. **Warn about anti-patterns** - Stateful apps, long-running processes
4. **Explain tradeoffs** - No platform is perfect, I show pros/cons
5. **Account for learning curve** - Firebase for beginners, AWS for experienced teams
6. **Respect portability preferences** - Open-source users → Supabase
7. **Track data freshness** - All recommendations include verification timestamps
8. **Warn about stale data** - I alert you if pricing/features are older than 30 days
9. **Encourage verification** - For production decisions, always verify current data

## Keywords That Activate This Skill
- Serverless recommendations
- Platform selection, platform comparison
- AWS Lambda vs Azure Functions vs GCP Cloud Functions
- Firebase vs Supabase
- Serverless architecture, serverless patterns
- Should I use serverless, is serverless right
- Which serverless platform, best serverless platform
- Serverless cost, serverless pricing
- Serverless free tier
- Lambda vs Functions vs Cloud Functions
- Cloud functions comparison
- Serverless for startups, serverless for enterprise
- Serverless learning, serverless tutorial

## Future Enhancements (Planned)

- **Cost Estimation**: Calculate monthly costs based on traffic (T-017)
- **IaC Generation**: Generate Terraform templates for selected platform (T-009-T-014)
- **Multi-platform comparison**: Side-by-side comparison tables
- **Learning paths**: Curated resources for each platform (T-021)
- **Security best practices**: Platform-specific security guidance (T-022)

---

**Remember**: I base all recommendations on your specific context, workload patterns, and requirements. There's no one-size-fits-all answer - the best platform depends on your situation!

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/serverless-recommender.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

