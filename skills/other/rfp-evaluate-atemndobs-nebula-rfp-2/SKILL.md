---
name: rfp-evaluate
description: Evaluate RFP opportunities using the 6-dimension scoring framework. Use when modifying evaluation criteria, adjusting keyword weights, or implementing AI-based evaluation.
allowed-tools: Read, Grep, Glob
---

# RFP Evaluation Skill

## Overview

This skill implements the 6-dimension scoring framework for evaluating RFP opportunities, with both logic-based (keyword matching) and AI-based evaluation modes.

---

## CRITICAL: Execution Order

> **Eligibility Gate is P0 HIGHEST PRIORITY and runs BEFORE scoring.**

```
┌─────────────────────────────────────────────────────────┐
│                 EVALUATION PIPELINE                      │
├─────────────────────────────────────────────────────────┤
│  1. ELIGIBILITY GATE (Hard filters - Phase 2)           │
│     ↓                                                    │
│     Output: ELIGIBLE | PARTNER_REQUIRED | REJECTED       │
│     ↓                                                    │
│  2. SCORING ENGINE (Only if eligible - Phase 3)         │
│     ↓                                                    │
│     Output: 0-6 score + Good Fit determination          │
└─────────────────────────────────────────────────────────┘
```

**Implementation Plan References:**
- Eligibility Gate: `docs/implementation-plan/phase-2-eligibility/`
- Scoring Engine: `docs/implementation-plan/phase-3-scoring/`

---

## 6-Dimension Scoring Framework

| Dimension | Weight | Purpose |
|-----------|--------|---------|
| Technical Relevance | 25% | Tech stack alignment |
| Scope Fit | 20% | Project type match |
| Category Focus | 15% | Industry alignment |
| Client Profile | 15% | Client type match |
| Logistics | 15% | Practical feasibility |
| Skill Alignment | 10% | Team capability match |

## Criterion Configuration

```typescript
interface Criterion {
  id: string;
  name: string;
  weight: number;           // 0-100, sum should = 100
  enabled: boolean;
  keywords: Keyword[];
  minMatches: number;       // Minimum keywords to meet criterion
  systemInstruction?: string; // For AI evaluation
}

interface Keyword {
  value: string;
  enabled: boolean;
  weight?: number;          // Optional keyword importance
}
```

## Default Keywords

### Technical Relevance (25%)
```typescript
const TECHNICAL_KEYWORDS = [
  "aws", "azure", "gcp", "cloud", "serverless", "lambda",
  "kubernetes", "docker", "react", "nextjs", "typescript",
  "node", "api", "rest", "graphql", "microservices",
  "data platform", "analytics", "etl", "ci/cd", "devsecops"
];
```

### Scope Fit (20%)
```typescript
const SCOPE_KEYWORDS = [
  "website redesign", "web application", "portal development",
  "cms implementation", "platform modernization", "digital transformation",
  "cloud migration", "api development", "system integration",
  "data migration", "taxonomy", "information architecture"
];
```

### Category Focus (15%)
```typescript
const CATEGORY_KEYWORDS = [
  "public sector", "federal", "state", "local government",
  "it services", "software development", "digital services",
  "technology", "information technology"
];
```

### Client Profile (15%)
```typescript
const CLIENT_KEYWORDS = [
  "federal agency", "state agency", "municipality",
  "department of", "office of", "bureau of",
  "technology-forward", "agile", "modern"
];
```

### Skill Alignment (10%)
```typescript
const SKILL_KEYWORDS = [
  "frontend developer", "backend developer", "full-stack",
  "cloud architect", "devops engineer", "ux designer",
  "technical lead", "project manager", "qa engineer"
];
```

## Eligibility Gate

Run BEFORE scoring to reject ineligible opportunities:

```typescript
interface EligibilityResult {
  eligible: boolean;
  status: "ok" | "needs_partner" | "reject";
  disqualifiers: string[];
}

const HARD_DISQUALIFIERS = [
  { pattern: /security\s*clearance\s*(required|mandatory)/i, fatal: true },
  { pattern: /on-?site\s*(presence\s*)?(required|mandatory)/i, fatal: true },
  { pattern: /u\.?s\.?\s*(citizen|company|organization)\s*only/i, fatal: false }, // Can partner
];

function checkEligibility(text: string): EligibilityResult {
  const disqualifiers: string[] = [];
  let canPartner = true;

  for (const { pattern, fatal } of HARD_DISQUALIFIERS) {
    if (pattern.test(text)) {
      disqualifiers.push(pattern.source);
      if (fatal) canPartner = false;
    }
  }

  if (disqualifiers.length === 0) {
    return { eligible: true, status: "ok", disqualifiers: [] };
  }

  return {
    eligible: canPartner,
    status: canPartner ? "needs_partner" : "reject",
    disqualifiers,
  };
}
```

## Logic-Based Evaluation

```typescript
interface EvaluationResult {
  score: number;            // 0-100
  isFit: boolean;           // score >= 60
  criteriaResults: CriterionResult[];
  eligibility: EligibilityResult;
  reasoning?: string;
}

interface CriterionResult {
  criterionId: string;
  criterionName: string;
  weight: number;
  met: boolean;
  score: number;
  matchedKeywords: string[];
  details: string;
}

function evaluateLogically(
  rfp: RFP,
  criteria: Criterion[]
): EvaluationResult {
  const text = `${rfp.title} ${rfp.description}`.toLowerCase();
  const results: CriterionResult[] = [];
  let totalScore = 0;
  let totalWeight = 0;

  for (const criterion of criteria) {
    if (!criterion.enabled) continue;

    const enabledKeywords = criterion.keywords
      .filter(kw => kw.enabled)
      .map(kw => kw.value.toLowerCase());

    const matches = enabledKeywords.filter(kw => text.includes(kw));
    const met = matches.length >= criterion.minMatches;
    const score = met ? criterion.weight : 0;

    results.push({
      criterionId: criterion.id,
      criterionName: criterion.name,
      weight: criterion.weight,
      met,
      score,
      matchedKeywords: matches,
      details: met
        ? `Matched ${matches.length} keywords: ${matches.join(", ")}`
        : `Only ${matches.length}/${criterion.minMatches} required matches`,
    });

    totalScore += score;
    totalWeight += criterion.weight;
  }

  const normalizedScore = totalWeight > 0
    ? (totalScore / totalWeight) * 100
    : 0;

  return {
    score: Math.round(normalizedScore),
    isFit: normalizedScore >= 60,
    criteriaResults: results,
    eligibility: checkEligibility(text),
  };
}
```

## AI-Based Evaluation

```typescript
async function evaluateWithAI(
  rfp: RFP,
  criterion: Criterion,
  aiProvider: AIProvider
): Promise<CriterionResult> {
  const prompt = `
Analyze this RFP for ${criterion.name}.

RFP Title: ${rfp.title}
RFP Description: ${rfp.description}

Keywords to consider: ${criterion.keywords.map(k => k.value).join(", ")}

Evaluate if this RFP aligns with these keywords.
Consider both exact matches AND semantic relevance.

Respond with JSON only:
{
  "foundKeywords": ["keyword1", "keyword2"],
  "isMatch": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "One sentence explanation"
}`;

  const systemInstruction = criterion.systemInstruction ??
    "You are an expert RFP analyst for a cloud-native software company.";

  const response = await aiProvider.analyze(prompt, systemInstruction);
  const parsed = JSON.parse(response);

  return {
    criterionId: criterion.id,
    criterionName: criterion.name,
    weight: criterion.weight,
    met: parsed.isMatch,
    score: parsed.isMatch ? criterion.weight : 0,
    matchedKeywords: parsed.foundKeywords,
    details: parsed.reasoning,
  };
}
```

## Chaseability Score

Final composite score with recommendation:

```typescript
interface ChaseabilityScore {
  overall: number;
  recommendation: "pursue" | "maybe" | "skip";
  reasoning: string;
  breakdown: Record<string, number>;
}

function calculateChaseability(
  evaluation: EvaluationResult
): ChaseabilityScore {
  // Apply partner penalty if needed
  const partnerPenalty = evaluation.eligibility.status === "needs_partner" ? 0.85 : 1.0;
  const adjustedScore = evaluation.score * partnerPenalty;

  // Determine recommendation
  let recommendation: "pursue" | "maybe" | "skip";
  if (!evaluation.eligibility.eligible) {
    recommendation = "skip";
  } else if (adjustedScore >= 70) {
    recommendation = "pursue";
  } else if (adjustedScore >= 50) {
    recommendation = "maybe";
  } else {
    recommendation = "skip";
  }

  // Build breakdown
  const breakdown: Record<string, number> = {};
  for (const result of evaluation.criteriaResults) {
    breakdown[result.criterionId] = result.score;
  }

  return {
    overall: Math.round(adjustedScore),
    recommendation,
    reasoning: buildReasoning(evaluation),
    breakdown,
  };
}

function buildReasoning(evaluation: EvaluationResult): string {
  const met = evaluation.criteriaResults.filter(r => r.met);
  const notMet = evaluation.criteriaResults.filter(r => !r.met);

  let reasoning = `Score: ${evaluation.score}%. `;
  reasoning += `Met ${met.length}/${evaluation.criteriaResults.length} criteria. `;

  if (notMet.length > 0) {
    reasoning += `Missing: ${notMet.map(r => r.criterionName).join(", ")}. `;
  }

  if (evaluation.eligibility.status === "needs_partner") {
    reasoning += "Note: Requires US partner for eligibility.";
  } else if (evaluation.eligibility.status === "reject") {
    reasoning += `Disqualified: ${evaluation.eligibility.disqualifiers.join(", ")}`;
  }

  return reasoning;
}
```

## Convex Implementation

```typescript
// convex/evaluations.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const evaluate = mutation({
  args: {
    rfpId: v.id("rfps"),
    evaluationType: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const rfp = await ctx.db.get(args.rfpId);
    if (!rfp) throw new Error("RFP not found");

    // Get criteria configuration
    const criteria = await ctx.db.query("criteria").collect();

    // Run evaluation
    const evaluation = evaluateLogically(rfp, criteria);

    // Save result
    return await ctx.db.insert("evaluations", {
      rfpId: args.rfpId,
      userId: identity.subject,
      evaluationType: args.evaluationType ?? "logic",
      ...evaluation,
      evaluatedAt: Date.now(),
    });
  },
});

export const getByRfp = query({
  args: { rfpId: v.id("rfps") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("evaluations")
      .withIndex("by_rfp", (q) => q.eq("rfpId", args.rfpId))
      .order("desc")
      .first();
  },
});
```

## Score Display Guidelines

| Score Range | Color | Badge Text |
|-------------|-------|------------|
| ≥70% | `text-success` (green) | "Strong Fit" |
| 50-69% | `text-warning` (yellow) | "Potential Fit" |
| <50% | `text-destructive` (red) | "Weak Fit" |

```tsx
function EvaluationBadge({ score }: { score: number }) {
  const variant = score >= 70 ? "success" : score >= 50 ? "warning" : "destructive";
  const label = score >= 70 ? "Strong Fit" : score >= 50 ? "Potential Fit" : "Weak Fit";

  return (
    <span className={`px-2 py-1 rounded text-sm bg-${variant}/20 text-${variant}`}>
      {score}% - {label}
    </span>
  );
}
```
