---
name: pursuit-brief
description: Generate 1-page pursuit briefs for qualified RFP opportunities. Use when creating bid/no-bid decision documents or implementing pursuit brief generation features.
allowed-tools: Read, Grep, Glob
---

# Pursuit Brief Skill

## Overview

This skill generates structured 1-page pursuit briefs to support rapid bid/no-bid decisions for RFP opportunities.

## Brief Structure

```typescript
interface PursuitBrief {
  rfpId: string;
  quickFacts: QuickFacts;
  chaseabilityScore: ChaseabilityScore;
  summary: string;
  whyPursue: string[];
  risks: string[];
  eligibility: EligibilityChecklist;
  recommendedTeam: TeamRecommendation;
  winStrategyNotes: string;
}

interface QuickFacts {
  source: string;
  noticeId: string;
  agency: string;
  posted: Date;
  deadline: Date;
  daysRemaining: number;
  estValue: string;
  location: string;
  setAside?: string;
}

interface TeamRecommendation {
  technicalLead: boolean;
  frontendDevs: number;
  backendDevs: number;
  fullStackDevs: number;
  devOps: boolean;
  qa: boolean;
  designer: boolean;
}
```

## Template (Markdown)

```markdown
# Pursuit Brief: {{RFP_TITLE}}

## Quick Facts
| Field | Value |
|-------|-------|
| Source | {{SOURCE}} |
| Notice ID | {{NOTICE_ID}} |
| Agency | {{AGENCY}} |
| Posted | {{POSTED_DATE}} |
| Deadline | {{DEADLINE}} ({{DAYS_REMAINING}} days) |
| Est. Value | {{EST_VALUE}} |
| Location | {{LOCATION}} |
| Set-Aside | {{SET_ASIDE}} |

## Chaseability Score: {{SCORE}}/100

### Score Breakdown
- Technical Relevance: {{TECH_SCORE}}/25
- Scope Fit: {{SCOPE_SCORE}}/20
- Category Focus: {{CATEGORY_SCORE}}/15
- Client Profile: {{CLIENT_SCORE}}/15
- Logistics: {{LOGISTICS_SCORE}}/15
- Skill Alignment: {{SKILL_SCORE}}/10

## Opportunity Summary
{{SUMMARY}}

## Why Pursue
- {{STRENGTH_1}}
- {{STRENGTH_2}}
- {{STRENGTH_3}}

## Risks & Concerns
- {{RISK_1}}
- {{RISK_2}}
- {{RISK_3}}

## Eligibility Status
- [{{US_ORG_STATUS}}] US Organization Requirement
- [{{CLEARANCE_STATUS}}] Security Clearance
- [{{ONSITE_STATUS}}] Onsite Presence

## Recommended Team
| Role | Count |
|------|-------|
| Technical Lead | 1 |
| Frontend Dev | {{FE_COUNT}} |
| Backend Dev | {{BE_COUNT}} |
| Full-Stack Dev | {{FS_COUNT}} |
| DevOps | {{DEVOPS}} |
| QA Engineer | {{QA}} |

## Win Strategy Notes
{{WIN_STRATEGY}}

---

## Decision
- [ ] **PURSUE** - Strong fit, move to capture
- [ ] **MAYBE** - Needs more investigation
- [ ] **SKIP** - Does not meet criteria

**Decision By:** _________________ **Date:** _________
```

## Generation Logic

### Convex Action

```typescript
// convex/pursuits.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const generateBrief = action({
  args: { rfpId: v.id("rfps") },
  handler: async (ctx, args) => {
    // Get RFP and evaluation
    const rfp = await ctx.runQuery(internal.rfps.get, { id: args.rfpId });
    const evaluation = await ctx.runQuery(internal.evaluations.getByRfp, {
      rfpId: args.rfpId,
    });

    if (!rfp) throw new Error("RFP not found");
    if (!evaluation) throw new Error("Evaluate RFP first");

    // Build quick facts
    const quickFacts: QuickFacts = {
      source: rfp.source,
      noticeId: rfp.externalId,
      agency: extractAgency(rfp),
      posted: new Date(rfp.postedDate),
      deadline: new Date(rfp.expiryDate),
      daysRemaining: Math.ceil(
        (rfp.expiryDate - Date.now()) / (1000 * 60 * 60 * 24)
      ),
      estValue: rfp.rawData?.estimatedValue ?? "Not specified",
      location: rfp.location,
      setAside: rfp.setAside,
    };

    // Generate AI sections
    const aiSections = await generateAISections(rfp, evaluation);

    // Infer team needs
    const recommendedTeam = inferTeamNeeds(rfp);

    // Build brief
    const brief: PursuitBrief = {
      rfpId: args.rfpId,
      quickFacts,
      chaseabilityScore: {
        overall: evaluation.score,
        breakdown: buildBreakdown(evaluation),
      },
      summary: aiSections.summary,
      whyPursue: aiSections.strengths,
      risks: aiSections.risks,
      eligibility: {
        usOrg: evaluation.eligibility.status === "ok" ? "✓" : "!",
        clearance: "✓",
        onsite: "✓",
      },
      recommendedTeam,
      winStrategyNotes: aiSections.winStrategy,
    };

    // Save brief to pursuit
    await ctx.runMutation(internal.pursuits.saveBrief, {
      rfpId: args.rfpId,
      brief: JSON.stringify(brief),
    });

    return brief;
  },
});
```

### AI Section Generation

```typescript
async function generateAISections(
  rfp: RFP,
  evaluation: Evaluation
): Promise<{
  summary: string;
  strengths: string[];
  risks: string[];
  winStrategy: string;
}> {
  const prompt = `
Analyze this RFP opportunity for Nebula Logix, a cloud-native software company specializing in serverless architectures, APIs, and workflow systems.

RFP Title: ${rfp.title}
Description: ${rfp.description}
Evaluation Score: ${evaluation.score}/100
Matched Keywords: ${evaluation.criteriaResults
    .flatMap((c) => c.matchedKeywords)
    .join(", ")}

Provide:
1. A 2-3 sentence summary of what the client needs
2. 3 specific reasons why we should pursue this (based on our strengths)
3. 3 potential risks or concerns
4. Initial win strategy notes (how we differentiate, competition considerations)

Respond with JSON only:
{
  "summary": "...",
  "strengths": ["...", "...", "..."],
  "risks": ["...", "...", "..."],
  "winStrategy": "..."
}`;

  const response = await callAIProvider(prompt);
  return JSON.parse(response);
}
```

### Team Inference

```typescript
function inferTeamNeeds(rfp: RFP): TeamRecommendation {
  const text = `${rfp.title} ${rfp.description}`.toLowerCase();

  const needs: TeamRecommendation = {
    technicalLead: true,
    frontendDevs: 0,
    backendDevs: 0,
    fullStackDevs: 0,
    devOps: false,
    qa: false,
    designer: false,
  };

  // Frontend indicators
  if (
    text.includes("frontend") ||
    text.includes("react") ||
    text.includes("user interface") ||
    text.includes("ui/ux")
  ) {
    needs.frontendDevs = 1;
  }

  // Backend indicators
  if (
    text.includes("backend") ||
    text.includes("api") ||
    text.includes("database") ||
    text.includes("server")
  ) {
    needs.backendDevs = 1;
  }

  // Full-stack or general
  if (text.includes("full-stack") || text.includes("full stack")) {
    needs.fullStackDevs = 2;
  }

  // DevOps indicators
  if (
    text.includes("devops") ||
    text.includes("ci/cd") ||
    text.includes("deployment") ||
    text.includes("infrastructure")
  ) {
    needs.devOps = true;
  }

  // QA indicators
  if (
    text.includes("testing") ||
    text.includes("qa") ||
    text.includes("quality assurance")
  ) {
    needs.qa = true;
  }

  // Design indicators
  if (
    text.includes("design") ||
    text.includes("ux") ||
    text.includes("user experience")
  ) {
    needs.designer = true;
  }

  // Default if nothing detected
  if (needs.frontendDevs + needs.backendDevs + needs.fullStackDevs === 0) {
    needs.fullStackDevs = 2;
  }

  return needs;
}
```

## UI Component

```tsx
// components/PursuitBriefView.tsx
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

export function PursuitBriefView({ rfpId }: { rfpId: Id<"rfps"> }) {
  const pursuit = useQuery(api.pursuits.getByRfp, { rfpId });
  const generateBrief = useMutation(api.pursuits.generateBrief);
  const updateDecision = useMutation(api.pursuits.updateDecision);

  const brief = pursuit?.brief ? JSON.parse(pursuit.brief) : null;

  if (!brief) {
    return (
      <div className="p-6 text-center">
        <p className="text-muted-foreground mb-4">
          No pursuit brief generated yet.
        </p>
        <button
          onClick={() => generateBrief({ rfpId })}
          className="px-4 py-2 bg-primary text-primary-foreground rounded"
        >
          Generate Pursuit Brief
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">
        Pursuit Brief: {brief.quickFacts.agency}
      </h1>

      {/* Quick Facts Table */}
      <QuickFactsTable facts={brief.quickFacts} />

      {/* Score Display */}
      <ScoreCard score={brief.chaseabilityScore} />

      {/* Summary */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Summary</h2>
        <p className="text-muted-foreground">{brief.summary}</p>
      </section>

      {/* Why Pursue */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Why Pursue</h2>
        <ul className="list-disc list-inside space-y-1">
          {brief.whyPursue.map((item, i) => (
            <li key={i} className="text-muted-foreground">{item}</li>
          ))}
        </ul>
      </section>

      {/* Risks */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Risks & Concerns</h2>
        <ul className="list-disc list-inside space-y-1">
          {brief.risks.map((item, i) => (
            <li key={i} className="text-muted-foreground">{item}</li>
          ))}
        </ul>
      </section>

      {/* Decision Buttons */}
      <div className="flex gap-4 pt-4 border-t">
        <button
          onClick={() => updateDecision({ rfpId, decision: "pursue" })}
          className="px-6 py-2 bg-success text-white rounded font-medium"
        >
          PURSUE
        </button>
        <button
          onClick={() => updateDecision({ rfpId, decision: "maybe" })}
          className="px-6 py-2 bg-warning text-white rounded font-medium"
        >
          MAYBE
        </button>
        <button
          onClick={() => updateDecision({ rfpId, decision: "skip" })}
          className="px-6 py-2 bg-destructive text-white rounded font-medium"
        >
          SKIP
        </button>
      </div>
    </div>
  );
}
```

## Export Functions

```typescript
export function exportBriefAsMarkdown(brief: PursuitBrief): string {
  return `# Pursuit Brief: ${brief.quickFacts.agency}

## Quick Facts
| Field | Value |
|-------|-------|
| Source | ${brief.quickFacts.source} |
| Notice ID | ${brief.quickFacts.noticeId} |
| Deadline | ${formatDate(brief.quickFacts.deadline)} (${brief.quickFacts.daysRemaining} days) |
| Location | ${brief.quickFacts.location} |

## Chaseability Score: ${brief.chaseabilityScore.overall}/100

## Summary
${brief.summary}

## Why Pursue
${brief.whyPursue.map((s) => `- ${s}`).join("\n")}

## Risks
${brief.risks.map((r) => `- ${r}`).join("\n")}

## Win Strategy
${brief.winStrategyNotes}
`;
}
```
