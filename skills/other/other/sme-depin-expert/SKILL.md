---
name: depin-infrastructure-fetcher
description: |
  <mandatory>MUST BE USED when DePIN projects, tokenomics, or infrastructure deployment mentioned</mandatory>
  <triggers>depin | helium | filecoin | render | akash | hivemapper | "decentralized infrastructure" | "node deployment" | "tokenomics design"</triggers>
  <expertise>BME tokenomics, PoPW consensus, node ROI, hardware requirements, network economics</expertise>
  <outputs>project_analysis, roi_calculations, deployment_guides, tokenomics_models, tech_stack_recommendations</outputs>
  <proactive>USE PROACTIVELY for: investment analysis, network comparison, deployment planning</proactive>
tools: Read(pattern:.claude/skills/depin-*/**), WebSearch, WebFetch(domain:depinscan.io|messari.io|helium.io), mcp__perplexity-ask__search, TodoWrite
---

# DePIN Infrastructure Project Fetcher

Comprehensive DePIN (Decentralized Physical Infrastructure Network) project analysis and information retrieval system for researching, evaluating, and monitoring decentralized infrastructure projects.

## Activation Triggers

<triggers>
- "Tell me about [DePIN project name]"
- "What DePIN projects operate in [location]"
- "Compare DePIN networks for [use case]"
- "Analyze [project] tokenomics"
- "Node requirements for [network]"
- Infrastructure keywords: wireless, storage, compute, sensor, energy
</triggers>

## Core Capabilities

### Project Research
- Fetch real-time project metrics and statistics
- Analyze tokenomics and economic models
- Evaluate network coverage and node distribution
- Compare multiple DePIN projects side-by-side

### Network Categories

<domain_terminology>
- **Wireless Networks**: Helium (IoT/5G), Pollen Mobile (cellular)
- **Storage Networks**: Filecoin, Arweave, Sia
- **Compute Networks**: Render Network, Akash, Flux
- **Sensor Networks**: PlanetWatch (air quality), WeatherXM (weather)
- **Energy Networks**: React Network, Powerledger
- **Mapping/Location**: Hivemapper (dashcams), DIMO (vehicle data)
</domain_terminology>

## Implementation Workflow

### Step 1: Parse Query Intent
```typescript
interface DePINQuery {
  project_name?: string;
  location?: string;
  category?: 'wireless' | 'storage' | 'compute' | 'sensor' | 'energy' | 'mapping';
  metric_type?: 'coverage' | 'nodes' | 'tokenomics' | 'roi';
}
```

### Step 2: Data Retrieval
Execute `scripts/fetch-depin-data.ts` with parsed parameters:
```bash
npx tsx .claude/skills/depin-infrastructure-fetcher/scripts/fetch-depin-data.ts \
  --project "helium" \
  --location "new-zealand" \
  --metrics "coverage,nodes"
```

### Step 3: Format Response
Use project-specific templates from `references/project-templates/`:
- Network statistics summary
- Node deployment requirements
- ROI calculations
- Coverage maps interpretation

## Quality Gates

<validation_rules>
- Data freshness: Max 24 hours old
- Source verification: Only trusted APIs (see references/trusted-sources.md)
- ROI calculations: Include all costs (hardware, electricity, maintenance)
- Coverage data: Verify with multiple sources when available
</validation_rules>

## Output Format

### Project Summary Template
```
PROJECT: [Name]
CATEGORY: [Network Type]
LOCATION: [Coverage Area]
STATUS: [Active Nodes] | [Network Growth]

DESCRIPTION:
[1-2 sentence overview]

KEY METRICS:
- Active Nodes: [count]
- Network Coverage: [area/percentage]
- Token Price: [current]
- Node ROI: [monthly estimate]

DEPLOYMENT:
- Hardware Cost: $[amount]
- Setup Complexity: [Low/Medium/High]
- Maintenance: [requirements]
```

## Error Handling

<error_recovery>
- API timeout (5s): Fall back to cached data with freshness warning
- No results: Suggest alternative projects in same category
- Ambiguous query: Ask clarifying questions (location, use case, budget)
</error_recovery>

## Performance Optimization

- Cache responses for 24 hours using `scripts/cache-manager.ts`
- Batch multiple project queries into single API calls
- Pre-fetch popular projects during idle time

## Security Considerations

<security>
- Never expose API keys in responses
- Sanitize location queries to prevent PII leakage
- Validate all external data against schema
- Rate limit external API calls (10/minute)
</security>

## Success Metrics

Track via `scripts/analytics.ts`:
- Query response time (<2s target)
- Data accuracy (>95% match with official sources)
- User satisfaction (follow-up questions indicate success)

<see_also>
- /docs/META-LEARNINGS/DEPIN-INFRASTRUCTURE.md → DePIN ecosystem overview
- references/api-documentation.md → External API schemas
- references/project-database.json → Known projects catalog
</see_also>