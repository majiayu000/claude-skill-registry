---
name: programming-advisor
description: Evaluate existing solutions (libraries, SaaS, open source) before custom development to avoid reinventing the wheel. Use when considering building new features, asking "should I build or use existing", or need build vs buy cost analysis with token estimates.
license: MIT
metadata:
  version: 1.0.0
  model: claude-opus-4-5
---

# Programming Advisor - "Reinventing the Wheel" Detector

## Triggers

| Trigger Phrase | Action |
|----------------|--------|
| "should I build X or use a library" | Search existing solutions, provide comparison |
| "find existing solutions for X" | Web search, categorize findings |
| "is there a package for X" | Search npm/pip/cargo/etc |
| "build vs buy for X" | Generate cost comparison table |
| "check if X exists before building" | Run full wheel detection workflow |

## Core Philosophy

Before writing a single line of code, determine if the wheel already exists. Vibe coding burns tokens, time, and creates maintenance burden. Existing solutions often provide better quality, security patches, and community support.

## Workflow

### Step 1: Capture Intent

Extract from user request:

- **What**: Core functionality needed
- **Why**: Use case / problem being solved
- **Constraints**: Language, platform, budget, licensing requirements

### Step 2: Search for Existing Solutions

Search strategy (use web_search):

1. `"{functionality} library {language}"`
2. `"{functionality} open source"`
3. `"{functionality} SaaS tool"`
4. `"best {functionality} solution 2024"`
5. `"{functionality} npm/pip/cargo package"` (based on ecosystem)

Categorize findings:

- **Libraries/Packages**: npm, pip, cargo, etc. (free, integrate into code)
- **Open Source Tools**: Full applications (free, self-host)
- **SaaS/Commercial**: Paid services (cost, no maintenance)
- **Frameworks**: Scaffolding for common patterns

### Step 3: Estimate Vibe Coding Cost

Use the token estimation reference: [references/token-estimates.md](references/token-estimates.md)

Factors to estimate:

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Lines of Code | <200 | 200-1000 | >1000 |
| Token Burn (est.) | 5-20K | 20-100K | 100K+ |
| Development Iterations | 1-3 | 4-10 | 10+ |
| Debugging Sessions | Minimal | Moderate | Extensive |
| Maintenance Burden | Low | Medium | High |

### Step 4: Generate Comparison Table

Always present a decision table:

```markdown
| Option | Type | Cost | Setup Time | Maintenance | Token Burn | Verdict |
|--------|------|------|------------|-------------|------------|---------|
| [Solution A] | Library | Free | 5 min | Updates only | 0 | ✅ Recommended |
| [Solution B] | SaaS | $X/mo | Instant | None | 0 | ⚡ Fastest |
| Vibe Code | Custom | Free | X hrs | You own it | ~XK tokens | 🔧 Full control |
```

### Step 5: Buy vs Build Evaluation Framework

#### When to Build

- [ ] Software is core to business differentiation
- [ ] Competitive advantage requires 100% control
- [ ] Vendor solutions insufficient for requirements
- [ ] Team has capacity without additional investment
- [ ] Long-term total cost of ownership favors build

#### When to Buy

- [ ] Time to value critical (weeks not months)
- [ ] Standard capability, not differentiating
- [ ] Vendor efficiencies reduce total cost
- [ ] Team should focus on higher-impact projects
- [ ] Acceptable vendor lock-in trade-off

#### Evaluation Matrix

| Factor | Build | Buy | Weight | Score |
|--------|-------|-----|--------|-------|
| Core competency | [Evidence] | [Evidence] | 30% | [Weighted score] |
| Time to value | [Evidence] | [Evidence] | 25% | [Weighted score] |
| Total cost (5 years) | [Evidence] | [Evidence] | 20% | [Weighted score] |
| Customization needs | [Evidence] | [Evidence] | 15% | [Weighted score] |
| Team expertise | [Evidence] | [Evidence] | 10% | [Weighted score] |
| **Total Score** | | | **100%** | [Sum] |

#### Hidden Costs Analysis

**Build Hidden Costs**:

- Maintenance burden (20-40% of build cost annually)
- Opportunity cost (what else could team build?)
- Expertise acquisition/retention
- Testing and security validation
- Documentation and knowledge transfer

**Buy Hidden Costs**:

- Integration complexity (API changes, data mapping)
- Vendor lock-in (switching cost estimation)
- Customization limitations (workarounds needed?)
- Ongoing licensing (per-user, per-transaction costs)
- Vendor stability risk (acquisition, discontinuation)

#### Core vs Context Assessment

Use Geoffrey Moore's framework to prioritize investment:

| Capability | Type | Rationale | Strategy |
|------------|------|-----------|----------|
| [Capability 1] | Core | [Differentiates business] | Build, own, invest |
| [Capability 2] | Context | [Necessary but commodity] | Buy, outsource |

**Key Insight**: Building context is a distraction from core. Buy context, build core.

#### Lindy Effect Consideration

Evaluate technology maturity:

- **Build**: Are you creating novel solution in unstable space? (High risk)
- **Buy**: Is vendor solution based on Lindy survivor tech? (Lower risk)

#### Buy vs Build Recommendation Template

```markdown
## Buy vs Build Recommendation: [Capability]

**Verdict**: [BUILD | BUY | HYBRID]

### Core Rationale
[Primary reason in 2-3 sentences]

### Evaluation Scores
- Build score: [X/100]
- Buy score: [Y/100]

### Core vs Context
[Core/Context classification with justification]

### Hidden Costs Accepted
**If Build**: [Maintenance burden, opportunity cost, expertise]
**If Buy**: [Lock-in level, integration complexity, licensing]

### Decision Confidence
[High | Medium | Low] - [Why]

### Review Trigger
Revisit if: [Conditions that would change this decision]
```

### Step 6: Recommendation Framework (Quick Reference)

Recommend **existing solutions** when:

- Mature library exists with >1K GitHub stars
- SaaS solves it for <$20/mo
- Common problem with well-tested solutions
- Security-sensitive (auth, crypto, payments)

Recommend **vibe coding** when:

- Highly specific business logic
- Simple glue code (<50 lines)
- Learning exercise (explicitly stated)
- No good existing solution found
- Integration requirements are unusual

### Step 7: If Vibe Coding Proceeds

If user chooses to build after seeing alternatives:

1. Acknowledge the valid reasons
2. Suggest existing code as reference/inspiration
3. Recommend libraries for sub-components
4. Provide a hybrid approach when possible

### Step 8: Integration Planning (When User Accepts Recommendation)

When the user accepts a recommended solution, provide a complete integration plan:

#### 8.1 Detect Project Context

Before generating the plan, analyze the user's project:

- **Package manager**: Check for `package.json` (npm/yarn/pnpm), `requirements.txt`/`pyproject.toml` (pip/poetry), `Cargo.toml` (cargo), `go.mod` (go)
- **Framework**: Identify React, Vue, Next.js, Rails, Django, FastAPI, etc.
- **Existing dependencies**: Check for conflicts or complementary packages
- **Project structure**: Understand where new code should live (src/, lib/, app/, etc.)
- **Code style**: Match existing patterns (TypeScript vs JS, ESM vs CJS, etc.)

#### 8.2 Generate Installation Commands

Provide ready-to-run commands for the detected package manager:

```bash
# npm
npm install <package>

# yarn
yarn add <package>

# pnpm
pnpm add <package>

# pip
pip install <package>

# poetry
poetry add <package>
```

#### 8.3 Provide Integration Steps

Create a numbered action plan:

1. **Install dependencies** - Exact commands
2. **Create/update config files** - If the library needs configuration
3. **Add to existing code** - Where to import and initialize
4. **Create new files** - With suggested file paths matching project structure
5. **Update related files** - Any existing files that need modification

#### 8.4 Generate Starter Code

Provide code scaffolding that:

- Matches the user's detected code style (TypeScript/JavaScript, etc.)
- Uses their existing patterns and conventions
- Includes necessary imports
- Shows basic usage with comments
- Handles common edge cases

#### 8.5 Warn About Potential Issues

Flag any concerns:

- **Dependency conflicts**: "Note: This requires React 18+, you have React 17"
- **Breaking changes**: "This library had major changes in v3, examples are for v3"
- **Peer dependencies**: "You'll also need to install X"
- **Config requirements**: "Requires adding to your tsconfig/babel/webpack config"

### Step 9: Cost Analysis (For Significant Decisions)

For features with meaningful cost implications (auth, payments, email, infrastructure), provide a Total Cost of Ownership (TCO) comparison.

#### 9.1 When to Include Cost Analysis

Include cost table when:

- SaaS options have monthly fees > $10
- DIY token estimate > 50K tokens
- User asks about costs or "is it worth it"
- Comparing multiple paid services
- Security-sensitive features (auth, payments)

#### 9.2 Cost Calculation

Use the pricing reference: [references/pricing-data.md](references/pricing-data.md)

**Formula:**

```text
Year N Cost = Setup Cost + (Monthly × 12 × N) + (Maintenance × N)

Where:
- Setup Cost (DIY) = Token Estimate × $0.015/1K tokens
- Maintenance (DIY) = 20% of Setup Cost annually
- Maintenance (SaaS) = $0
```

#### 9.3 Cost Table Format

```markdown
## 💰 Cost Analysis

| Option | Setup | Monthly | Year 1 | Year 3 | Notes |
|--------|-------|---------|--------|--------|-------|
| [SaaS A] | 10min | $25 | $300 | $900 | Free tier: 10K MAU |
| [SaaS B] | 15min | $35 | $420 | $1,260 | More features |
| [Free/OSS] | 1hr | $0 | $0 | $0 | Self-host required |
| DIY | Xhrs | $0 | ~$Y | ~$Z | + maintenance burden |

💡 **Break-even:** [When DIY becomes cheaper, if ever]
⚠️ **Hidden costs:** [Security audits, compliance, on-call burden]
```

#### 9.4 Hidden Costs to Surface

Always mention relevant hidden costs:

- **Security audits**: $5K-50K for custom auth systems
- **Compliance**: SOC2, GDPR, PCI implementation time
- **On-call burden**: DIY = you're the support team
- **Opportunity cost**: Time not spent on core product
- **Technical debt**: Custom code needs maintenance forever

#### 9.5 Red Flags to Call Out

Warn users when they say:

- "It's just a simple auth system" → Auth is never simple
- "We can build it in a weekend" → You can't, securely
- "We'll add security later" → Security debt is expensive
- "It's cheaper long-term" → Usually false under 10K users

## Response Template

```markdown
## 🔍 Existing Solutions Found

I found [N] existing solutions before we write custom code:

### Libraries/Packages
- **[Name]**: [one-line description] | [stars/downloads] | [link]

### Open Source Tools  
- **[Name]**: [one-line description] | [stars] | [link]

### SaaS Options
- **[Name]**: [one-line description] | [pricing] | [link]

## 📊 Build vs Buy Comparison

| Option | Type | Cost | Setup | Maintenance | Est. Tokens |
|--------|------|------|-------|-------------|-------------|
| ... | ... | ... | ... | ... | ... |

## 💰 Cost Analysis (for significant decisions)

| Option | Setup | Monthly | Year 1 | Year 3 | Notes |
|--------|-------|---------|--------|--------|-------|
| ... | ... | ... | ... | ... | ... |

💡 **Break-even:** [analysis]
⚠️ **Hidden costs:** [security, compliance, maintenance]

## 💡 Recommendation

[Clear recommendation with reasoning]

## 🔧 If You Still Want to Build

[Only if user wants custom solution - suggest hybrid approach]
```

### Integration Plan Template (When User Accepts)

When the user says "let's use [recommended solution]" or "how do I add this?", respond with:

```markdown
## 🚀 Integration Plan: [Solution Name]

### Your Project Context
- **Detected**: [framework], [package manager], [language]
- **Project structure**: [src/app/lib layout]

### Step 1: Install Dependencies

\`\`\`bash
[exact install command for their package manager]
\`\`\`

### Step 2: Configuration (if needed)

[Any config file changes needed]

### Step 3: Create New Files

📁 `[suggested/file/path.ts]`
\`\`\`typescript
[starter code matching their project style]
\`\`\`

### Step 4: Update Existing Files

📝 `[existing/file/to/modify.ts]`
\`\`\`typescript
// Add this import
import { X } from '[package]'

// Use it like this
[integration code]
\`\`\`

### ⚠️ Notes
- [Any warnings about versions, conflicts, or requirements]

### 📚 Resources
- [Official docs link]
- [Relevant examples]
```

## Anti-Patterns to Flag

Alert users when they're about to reinvent:

- Authentication systems → "Use Auth0, Clerk, Supabase Auth"
- State management → "Consider Zustand, Redux Toolkit, Jotai"
- Form validation → "Check out Zod, Yup, React Hook Form"
- API clients → "Look at Axios, ky, ofetch"
- Date handling → "Use date-fns, dayjs, Luxon"
- CLI tools → "Consider Commander, yargs, oclif"
- PDF generation → "Use pdf-lib, jsPDF, Puppeteer"
- Email sending → "Check Resend, SendGrid, Nodemailer"
- Cron jobs → "Use node-cron, Bull, Agenda"
- Database ORMs → "Consider Prisma, Drizzle, TypeORM"

## Quick Reference: Common Token Burns

| Task Complexity | Typical Token Burn | Time Equivalent |
|-----------------|-------------------|-----------------|
| Simple script (<100 LOC) | 5-15K | 30min-1hr |
| Utility module (100-500 LOC) | 15-50K | 2-4hrs |
| Feature component (500-2K LOC) | 50-150K | 1-2 days |
| Full application | 150K-500K+ | Days-weeks |

See [references/token-estimates.md](references/token-estimates.md) for detailed breakdowns.

See [references/common-solutions.md](references/common-solutions.md) for exhaustive list of commonly reinvented wheels.

See [references/integration-patterns.md](references/integration-patterns.md) for project detection and starter code patterns.

See [references/pricing-data.md](references/pricing-data.md) for SaaS pricing and cost calculation data.
