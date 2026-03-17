---
name: meme-launcher
description: |
  Solana memecoin launch strategy and execution. Use when planning token launches, designing tokenomics, building pre-launch hype, deploying on pump.fun/Raydium, or optimizing launch mechanics. Covers: token creation, bonding curves, liquidity strategy, community building, anti-rug best practices.
tools: Read(pattern:.claude/skills/meme-launcher/**), WebSearch, WebFetch(domain:pump.fun|raydium.io|jup.ag|solscan.io|docs.solana.com), mcp__perplexity-ask__search, TodoWrite
---

# Meme Launcher - Solana Memecoin Launch System

End-to-end memecoin launch planning and execution for Solana. From concept to deployment to moon.

## Activation Triggers

<triggers>
- "Launch a memecoin"
- "Create token for [concept]"
- "Pump.fun launch strategy"
- "Tokenomics for [project]"
- "Pre-launch checklist"
- "How to launch on [platform]"
- "Bonding curve setup"
- "Build hype for [token]"
- Keywords: launch, deploy, tokenomics, pump.fun launch, create token, mint token, bonding curve, pre-launch, liquidity add
</triggers>

## Core Capabilities

### 1. Token Concept Development
- Name/ticker optimization (memorability, searchability)
- Narrative construction (why this token, why now)
- Visual identity guidelines (logo, banner, meme templates)
- Community angle (target demographic, culture fit)

### 2. Tokenomics Design
- Supply architecture (total supply, decimals)
- Distribution strategy (fair launch vs. presale)
- Tax structure (if any) - buy/sell fees
- Burn mechanics and deflationary options
- LP allocation and lock parameters

### 3. Platform Selection
- **Pump.fun**: Bonding curve launches, low barrier, viral potential
- **Raydium**: AMM pools, deeper liquidity, established traders
- **Jupiter**: Launch pad features, routing optimization
- **Custom SPL**: Full control, requires more setup

### 4. Launch Execution
- Contract deployment checklist
- Liquidity provisioning strategy
- Initial price setting
- Sniper protection tactics
- First-hour playbook

### 5. Anti-Rug Implementation
- Mint authority renouncement
- Freeze authority removal
- LP lock procedures
- Transparent team allocation
- Trust signals for buyers

## Launch Platforms Deep Dive

<platforms>
### Pump.fun
- **Best for**: Viral memes, low-effort launches, quick validation
- **Bonding curve**: Auto-AMM, graduates to Raydium at threshold
- **Cost**: ~0.02 SOL creation fee
- **Time to launch**: < 5 minutes
- **Graduation**: 69 SOL collected triggers Raydium migration

### Raydium
- **Best for**: Serious projects, larger liquidity, established presence
- **Pool type**: Concentrated liquidity or standard AMM
- **Cost**: ~2-3 SOL for pool creation
- **Time to launch**: 15-30 minutes
- **Requirements**: Pre-minted token, initial liquidity

### Jupiter LFG
- **Best for**: Curated launches, built-in audience
- **Features**: Voting mechanism, established credibility
- **Cost**: Application-based
- **Time to launch**: Days (approval required)
</platforms>

## Implementation Workflow

### Step 1: Parse Launch Intent
```typescript
interface LaunchConfig {
  concept: string;
  name?: string;
  ticker?: string;
  platform: 'pump.fun' | 'raydium' | 'jupiter' | 'custom';
  supply: number;
  initialLiquidity: number; // in SOL
  launchType: 'fair' | 'presale' | 'stealth';
  antiRugFeatures: string[];
}
```

### Step 2: Concept Validation
1. **Name Check**: Search existing tokens for conflicts
2. **Trend Analysis**: Validate narrative timing
3. **Competition Scan**: Similar tokens, market saturation
4. **Virality Score**: Meme potential assessment

### Step 3: Tokenomics Builder
```
RECOMMENDED TOKENOMICS:

Fair Launch (Pump.fun):
- Supply: 1,000,000,000 (1B)
- Decimals: 6
- Dev allocation: 0% (buy from curve like everyone)
- Tax: 0% (standard for pump.fun)
- LP: Auto-managed by bonding curve

Raydium Launch:
- Supply: 1,000,000,000 (1B)
- Decimals: 9
- Dev/Team: 5-10% (vested/locked)
- Marketing: 5%
- LP: 80-90% of supply
- Initial LP: 10-50 SOL recommended
```

### Step 4: Pre-Launch Checklist
Execute validation before any deployment:
```bash
npx tsx .claude/skills/meme-launcher/scripts/pre-launch-check.ts \
  --name "MOONCAT" \
  --ticker "$MCAT" \
  --platform pump.fun \
  --supply 1000000000
```

### Step 5: Launch Execution
Platform-specific deployment guides in `references/`

## Output Formats

### Launch Plan (Default)
```
TOKEN: $MCAT (MoonCat)
PLATFORM: Pump.fun
STATUS: Ready to Deploy

TOKENOMICS:
- Supply: 1,000,000,000
- Decimals: 6
- Tax: 0%
- LP Lock: Auto (pump.fun)

PRE-LAUNCH CHECKLIST:
[x] Name available (no conflicts)
[x] Ticker unique
[x] Logo prepared (400x400 PNG)
[x] Description written
[x] Social links ready
[ ] Community seeded (min 50 members)
[ ] KOL outreach complete

ANTI-RUG SIGNALS:
[x] Fair launch (no presale)
[x] Dev buys from curve
[x] Mint renounced at creation
[x] No freeze authority

LAUNCH STRATEGY:
1. Deploy at low-activity hour (2-4 AM UTC)
2. Seed initial buys (0.5-1 SOL each x 5 wallets)
3. Post to CT immediately after
4. Telegram announcement at 10 holders
5. Push for graduation at momentum peak

ESTIMATED COSTS:
- Creation: 0.02 SOL
- Initial seed buys: 2.5-5 SOL
- Total: ~3-5 SOL
```

### Quick Deploy (--format quick)
```
$MCAT | Pump.fun | 1B supply | Fair launch
Deploy: pump.fun/create → paste details → confirm
Post-deploy: Announce → Seed → Shill
```

### Full Strategy (--format full)
Complete go-to-market plan including:
- 7-day pre-launch timeline
- Community building playbook
- Influencer outreach templates
- Post-launch maintenance guide

## Tokenomics Templates

<tokenomics_templates>
### Fair Launch (Maximum Trust)
```
Supply: 1B | Tax: 0% | Dev: 0%
Everyone buys equally, dev buys from market
Best for: Viral memes, community-driven
```

### Team Allocation (Project-Focused)
```
Supply: 1B | Tax: 0-1% | Team: 5-10% (locked 3mo)
Team tokens vested, transparent allocation
Best for: Utility roadmap, long-term projects
```

### Marketing-Heavy
```
Supply: 1B | Tax: 2% (1% burn, 1% marketing) | Marketing wallet: 5%
Built-in marketing fund from trading
Best for: KOL campaigns, aggressive growth
```

### Deflationary
```
Supply: 1B | Burn: 1% per tx | LP burn: 50% at launch
Decreasing supply over time
Best for: "Number go up" narrative
```
</tokenomics_templates>

## Platform Deployment Guides

### Pump.fun Launch Steps
```
1. Go to pump.fun/create
2. Upload logo (400x400 recommended)
3. Enter name and ticker
4. Write description (max 500 chars, include narrative)
5. Add social links (Twitter, Telegram, Website)
6. Pay creation fee (~0.02 SOL)
7. IMMEDIATELY after creation:
   - Copy contract address
   - Make first buy (establishes you're in)
   - Post to Twitter with CA
   - Share in Telegram
```

### Raydium Launch Steps
```
1. Create SPL token via spl-token CLI or Solana Tools
2. Renounce mint authority
3. Go to raydium.io/liquidity
4. Create new pool (select token + SOL pair)
5. Set initial price (supply in pool / SOL in pool)
6. Add liquidity (recommend 80%+ of supply)
7. Lock LP tokens (raydium.io/burn or third-party)
8. Announce with LP lock proof
```

## Pre-Launch Validation

<validation_checklist>
**REQUIRED:**
- [ ] Token name doesn't conflict with established projects
- [ ] Ticker is available and memorable (3-5 chars)
- [ ] Logo is original or properly licensed
- [ ] Description is clear and compelling
- [ ] At least one social channel exists

**RECOMMENDED:**
- [ ] Community of 50+ members pre-launch
- [ ] 2-3 KOLs aware/interested
- [ ] Meme templates prepared
- [ ] Website or landing page
- [ ] Launch timing analyzed (avoid major events)

**ANTI-RUG (Non-negotiable for credibility):**
- [ ] Mint authority will be renounced
- [ ] No freeze authority
- [ ] LP will be locked or burned
- [ ] Team allocation (if any) is transparent and locked
- [ ] No hidden functions in contract
</validation_checklist>

## Launch Timing Strategy

<timing>
### Best Times (UTC)
- **Monday-Wednesday 14:00-18:00**: US afternoon, peak CT activity
- **Friday 12:00-16:00**: Weekend anticipation, FOMO builds
- **Sunday 20:00-24:00**: Fresh week positioning

### Avoid
- **Saturday night**: Low attention
- **Major crypto events**: Competition for attention
- **Market dumps**: Fear overrides degen impulses
- **US holidays**: Reduced volume

### Coordination
1. Soft announce 24h before (build anticipation)
2. Final countdown 1h before (urgency)
3. Deploy and immediately post CA
4. First 10 minutes critical (seed momentum)
</timing>

## Post-Launch Checklist

<post_launch>
**First Hour:**
- [ ] Verify contract on Solscan
- [ ] Post CA to all channels
- [ ] Monitor for snipers/bots
- [ ] Engage with early buyers
- [ ] Update Dexscreener info (if Raydium)

**First Day:**
- [ ] Track holder growth
- [ ] Respond to community questions
- [ ] Share milestone updates (holders, MCAP)
- [ ] KOL follow-ups

**First Week:**
- [ ] Daily community engagement
- [ ] Meme contests/airdrops
- [ ] Partnership outreach
- [ ] Roadmap updates (if applicable)
</post_launch>

## Risk Framework

### Launch Risk Assessment
```
LOW RISK (Green light):
- Unique concept, good timing
- Community pre-built
- Clean contract, all anti-rug features
- Multiple social channels active

MEDIUM RISK (Proceed carefully):
- Similar tokens exist
- Small initial community
- Launch timing suboptimal
- Limited marketing budget

HIGH RISK (Reconsider):
- Saturated narrative
- No community traction
- Poor timing (bear market)
- No differentiator
```

## Error Handling

<error_recovery>
- **Name taken**: Generate alternatives, check availability
- **Low initial traction**: Increase seed buys, delay major push
- **Sniper attack**: Document, communicate to community
- **Pump.fun graduation stall**: Rally community for final push
- **FUD spreading**: Address transparently, show proof of anti-rug
</error_recovery>

## Security Considerations

<security>
- Never share deployer wallet private keys
- Use fresh wallet for launches (operational security)
- Verify all contract interactions before signing
- Document everything for transparency
- Prepare proof of LP lock/burn before launch
</security>

## Quality Gates

<validation_rules>
- Never recommend launch without anti-rug features
- Always include LP strategy
- Verify name/ticker availability before finalizing
- Include cost estimates
- Provide post-launch support checklist
</validation_rules>

<see_also>
- references/pump-fun-guide.md - Detailed pump.fun walkthrough
- references/tokenomics-templates.md - Supply/distribution models
- references/launch-marketing-playbook.md - Go-to-market strategies
- scripts/pre-launch-check.ts - Validation CLI
</see_also>
