---
name: proposal-builder
description: Assemble proposals from templates and content library. Use when implementing proposal generation, managing content blocks, or working with proposal templates.
allowed-tools: Read, Grep, Glob
---

# Proposal Builder Skill

## Overview

This skill manages reusable proposal templates, capability blocks, and content library for rapid RFP response assembly.

## Content Library Structure

```typescript
interface ContentLibrary {
  templates: ProposalTemplate[];
  capabilityBlocks: CapabilityBlock[];
  caseStudies: CaseStudy[];
  teamBios: TeamBio[];
  boilerplate: BoilerplateSection[];
}

interface CapabilityBlock {
  id: string;
  name: string;
  category: string;
  content: string;
  keywords: string[];
  lastUpdated: Date;
}

interface CaseStudy {
  id: string;
  title: string;
  client: string;
  industry: string;
  challenge: string;
  approach: string;
  results: string;
  technologies: string[];
  timeline: string;
  teamSize: number;
}

interface TeamBio {
  id: string;
  name: string;
  role: string;
  summary: string;
  expertise: string[];
  certifications: string[];
  yearsExperience: number;
}
```

## Default Capability Blocks

```typescript
const DEFAULT_BLOCKS: CapabilityBlock[] = [
  {
    id: "serverless",
    name: "Serverless Architecture",
    category: "technical",
    keywords: ["serverless", "lambda", "aws", "cloud-native"],
    content: `Our serverless-first approach leverages AWS Lambda, API Gateway, and managed services:

- **Zero infrastructure management**: Focus on business logic
- **Automatic scaling**: Handle traffic spikes seamlessly
- **Pay-per-use pricing**: Cost-efficient compute
- **Built-in high availability**: Multi-AZ by default

We've delivered 20+ serverless production systems for government and enterprise clients.`,
  },
  {
    id: "apis",
    name: "API Development & Integration",
    category: "technical",
    keywords: ["api", "rest", "graphql", "integration"],
    content: `We design and implement modern APIs for seamless integration:

- **RESTful & GraphQL APIs**: Right pattern for each use case
- **OpenAPI documentation**: Complete API contracts
- **OAuth 2.0 & JWT**: Secure authentication
- **Rate limiting & monitoring**: Production-ready from day one

Our APIs serve millions of requests daily across multiple clients.`,
  },
  {
    id: "devsecops",
    name: "DevSecOps & CI/CD",
    category: "technical",
    keywords: ["devops", "ci/cd", "security", "automation"],
    content: `Security-integrated DevOps practices for reliable delivery:

- **Infrastructure as Code**: Terraform, CloudFormation, CDK
- **CI/CD pipelines**: GitHub Actions, GitLab CI, AWS CodePipeline
- **Security scanning**: SAST, DAST, dependency scanning
- **Compliance automation**: FedRAMP, SOC 2 support`,
  },
  {
    id: "cloud_migration",
    name: "Cloud Migration",
    category: "technical",
    keywords: ["migration", "cloud", "modernization"],
    content: `Proven migration methodology minimizes risk:

**Assessment**: Application portfolio analysis, dependency mapping
**Strategy**: 6 Rs evaluation (Rehost, Replatform, Refactor, etc.)
**Execution**: Phased migration with rollback plans
**Optimization**: FinOps practices, performance tuning

Successfully migrated 50+ applications, reducing costs 30-50%.`,
  },
];
```

## Proposal Templates

### Formal RFP Template Sections

| Section | Purpose | Content Type |
|---------|---------|--------------|
| Cover Letter | Personalized introduction | Custom |
| Executive Summary | Value proposition | Custom + boilerplate |
| Technical Approach | Solution architecture | Capability blocks |
| Project Plan | Timeline & milestones | Template |
| Team & Staffing | Organization & bios | Team bios |
| Past Performance | Case studies | Case studies |
| Security & Compliance | Standards met | Boilerplate |
| Pricing | Cost breakdown | Custom |

### Template Placeholders

```
{{CLIENT_NAME}}        - Agency or organization name
{{PROJECT_TITLE}}      - RFP title or project name
{{SUBMISSION_DATE}}    - Proposal submission date
{{VALUE_PROPOSITION}}  - Customized value statement
{{TECHNICAL_APPROACH}} - Assembled capability blocks
{{TEAM_BIOS}}          - Selected team member bios
{{CASE_STUDIES}}       - Selected relevant case studies
{{TIMELINE}}           - Project timeline
{{PRICING_TABLE}}      - Cost breakdown
```

## Convex Implementation

### Content Management

```typescript
// convex/templates.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const listCapabilityBlocks = query({
  args: { category: v.optional(v.string()) },
  handler: async (ctx, args) => {
    let q = ctx.db.query("capabilityBlocks");
    if (args.category) {
      q = q.filter((q) => q.eq(q.field("category"), args.category));
    }
    return await q.collect();
  },
});

export const matchBlocksToRfp = query({
  args: { rfpId: v.id("rfps") },
  handler: async (ctx, args) => {
    const rfp = await ctx.db.get(args.rfpId);
    if (!rfp) return [];

    const blocks = await ctx.db.query("capabilityBlocks").collect();
    const text = `${rfp.title} ${rfp.description}`.toLowerCase();

    // Score blocks by keyword matches
    const scored = blocks.map((block) => {
      const matches = block.keywords.filter((kw) =>
        text.includes(kw.toLowerCase())
      );
      return {
        ...block,
        matchScore: matches.length,
        matchedKeywords: matches,
      };
    });

    return scored
      .filter((b) => b.matchScore > 0)
      .sort((a, b) => b.matchScore - a.matchScore);
  },
});

export const createCapabilityBlock = mutation({
  args: {
    name: v.string(),
    category: v.string(),
    content: v.string(),
    keywords: v.array(v.string()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    return await ctx.db.insert("capabilityBlocks", {
      ...args,
      lastUpdated: Date.now(),
    });
  },
});
```

### Proposal Assembly

```typescript
// convex/proposals.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const assembleProposal = action({
  args: {
    rfpId: v.id("rfps"),
    templateId: v.string(),
    selectedBlocks: v.array(v.string()),
    selectedCaseStudies: v.array(v.string()),
    selectedTeam: v.array(v.string()),
  },
  handler: async (ctx, args) => {
    // Fetch RFP
    const rfp = await ctx.runQuery(internal.rfps.get, { id: args.rfpId });
    if (!rfp) throw new Error("RFP not found");

    // Fetch template
    const template = await ctx.runQuery(internal.templates.getTemplate, {
      id: args.templateId,
    });

    // Fetch selected content
    const blocks = await ctx.runQuery(internal.templates.getBlocksByIds, {
      ids: args.selectedBlocks,
    });
    const caseStudies = await ctx.runQuery(internal.templates.getCaseStudiesByIds, {
      ids: args.selectedCaseStudies,
    });
    const team = await ctx.runQuery(internal.templates.getTeamBiosByIds, {
      ids: args.selectedTeam,
    });

    // Assemble proposal
    let content = template.content;

    // Replace placeholders
    content = content
      .replace(/\{\{CLIENT_NAME\}\}/g, extractClientName(rfp))
      .replace(/\{\{PROJECT_TITLE\}\}/g, rfp.title)
      .replace(/\{\{SUBMISSION_DATE\}\}/g, formatDate(new Date()));

    // Insert capability blocks
    const techSection = blocks.map((b) => `### ${b.name}\n\n${b.content}`).join("\n\n");
    content = content.replace(/\{\{TECHNICAL_APPROACH\}\}/g, techSection);

    // Insert case studies
    const caseSection = caseStudies.map(formatCaseStudy).join("\n\n---\n\n");
    content = content.replace(/\{\{CASE_STUDIES\}\}/g, caseSection);

    // Insert team bios
    const teamSection = team.map(formatTeamBio).join("\n\n");
    content = content.replace(/\{\{TEAM_BIOS\}\}/g, teamSection);

    // Save draft
    await ctx.runMutation(internal.pursuits.saveDraft, {
      rfpId: args.rfpId,
      content,
    });

    return { content, wordCount: countWords(content) };
  },
});

function formatCaseStudy(cs: CaseStudy): string {
  return `### ${cs.title}

**Client:** ${cs.client}
**Industry:** ${cs.industry}

**Challenge:** ${cs.challenge}

**Approach:** ${cs.approach}

**Results:**
${cs.results}

**Technologies:** ${cs.technologies.join(", ")}
**Timeline:** ${cs.timeline}
**Team Size:** ${cs.teamSize}`;
}

function formatTeamBio(bio: TeamBio): string {
  return `#### ${bio.name} - ${bio.role}

${bio.summary}

**Expertise:** ${bio.expertise.join(", ")}
**Certifications:** ${bio.certifications.join(", ")}
**Experience:** ${bio.yearsExperience}+ years`;
}
```

## UI Components

```tsx
// components/ProposalBuilder.tsx
export function ProposalBuilder({ rfpId }: { rfpId: Id<"rfps"> }) {
  const [selectedTemplate, setSelectedTemplate] = useState<string>();
  const [selectedBlocks, setSelectedBlocks] = useState<string[]>([]);
  const [selectedStudies, setSelectedStudies] = useState<string[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<string[]>([]);

  const templates = useQuery(api.templates.list);
  const matchedBlocks = useQuery(api.templates.matchBlocksToRfp, { rfpId });
  const caseStudies = useQuery(api.templates.listCaseStudies);
  const team = useQuery(api.templates.listTeamBios);

  const assemble = useMutation(api.proposals.assembleProposal);

  const handleAssemble = async () => {
    await assemble({
      rfpId,
      templateId: selectedTemplate!,
      selectedBlocks,
      selectedCaseStudies: selectedStudies,
      selectedTeam,
    });
  };

  return (
    <div className="grid grid-cols-3 gap-6 p-6">
      {/* Template Selection */}
      <section className="space-y-4">
        <h3 className="font-semibold">1. Select Template</h3>
        <TemplateSelector
          templates={templates ?? []}
          selected={selectedTemplate}
          onSelect={setSelectedTemplate}
        />
      </section>

      {/* Content Selection */}
      <section className="space-y-4">
        <h3 className="font-semibold">2. Select Content</h3>

        <div>
          <h4 className="text-sm text-muted-foreground mb-2">
            Recommended Capability Blocks
          </h4>
          <BlockSelector
            blocks={matchedBlocks ?? []}
            selected={selectedBlocks}
            onSelect={setSelectedBlocks}
          />
        </div>

        <div>
          <h4 className="text-sm text-muted-foreground mb-2">Case Studies</h4>
          <CaseStudySelector
            studies={caseStudies ?? []}
            selected={selectedStudies}
            onSelect={setSelectedStudies}
          />
        </div>

        <div>
          <h4 className="text-sm text-muted-foreground mb-2">Team Members</h4>
          <TeamSelector
            team={team ?? []}
            selected={selectedTeam}
            onSelect={setSelectedTeam}
          />
        </div>
      </section>

      {/* Actions */}
      <section className="space-y-4">
        <h3 className="font-semibold">3. Generate</h3>
        <button
          onClick={handleAssemble}
          disabled={!selectedTemplate}
          className="w-full px-4 py-2 bg-primary text-primary-foreground rounded disabled:opacity-50"
        >
          Assemble Proposal
        </button>
      </section>
    </div>
  );
}
```

## Seeding Default Content

```typescript
// convex/templates.ts
export const seedDefaults = mutation({
  args: {},
  handler: async (ctx) => {
    // Check if already seeded
    const existing = await ctx.db.query("capabilityBlocks").first();
    if (existing) return { message: "Already seeded" };

    // Seed capability blocks
    for (const block of DEFAULT_BLOCKS) {
      await ctx.db.insert("capabilityBlocks", {
        ...block,
        lastUpdated: Date.now(),
      });
    }

    // Seed sample case study
    await ctx.db.insert("caseStudies", {
      title: "Federal Agency Cloud Migration",
      client: "US Federal Agency",
      industry: "Government",
      challenge: "Legacy on-premises systems causing operational issues",
      approach: "Phased migration to AWS with serverless architecture",
      results: "50% cost reduction, 99.9% uptime, 3x faster deployments",
      technologies: ["AWS", "Lambda", "DynamoDB", "CloudFront"],
      timeline: "6 months",
      teamSize: 5,
    });

    return { message: "Defaults seeded" };
  },
});
```
