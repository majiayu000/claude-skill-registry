---
name: compliance-matrix
description: Generate and track compliance matrices for RFP requirements. Use when building requirements tracking features, implementing compliance checklists, or ensuring proposal coverage.
allowed-tools: Read, Grep, Glob
---

# Compliance Matrix Skill

## Overview

This skill generates compliance matrices to track RFP requirements against proposal responses, ensuring complete coverage of all mandatory elements.

## Data Structures

```typescript
interface ComplianceMatrix {
  rfpId: string;
  rfpTitle: string;
  createdAt: Date;
  updatedAt: Date;
  status: "draft" | "in_review" | "complete";
  sections: ComplianceSection[];
  summary: MatrixSummary;
}

interface ComplianceSection {
  id: string;
  name: string;
  requirements: ComplianceRequirement[];
}

interface ComplianceRequirement {
  id: string;
  reference: string;           // RFP section reference
  requirement: string;          // Original requirement text
  type: "mandatory" | "desirable" | "informational";
  category: RequirementCategory;
  responseSection: string;      // Proposal section
  responseText: string;         // Draft response
  evidence: string;             // Supporting evidence
  owner: string;                // Team member responsible
  status: "pending" | "draft" | "review" | "complete" | "n/a";
  notes: string;
}

type RequirementCategory =
  | "technical"
  | "management"
  | "past_performance"
  | "pricing"
  | "certifications"
  | "staffing"
  | "security"
  | "compliance"
  | "other";

interface MatrixSummary {
  totalRequirements: number;
  mandatory: number;
  desirable: number;
  addressed: number;
  pending: number;
  notApplicable: number;
}
```

## Template Output

```markdown
# Compliance Matrix: {{RFP_TITLE}}

**RFP ID:** {{EXTERNAL_ID}}
**Agency:** {{AGENCY}}
**Deadline:** {{DEADLINE}}
**Last Updated:** {{UPDATED_AT}}

## Summary
| Status | Mandatory | Desirable | Total |
|--------|-----------|-----------|-------|
| Complete | {{M_COMPLETE}} | {{D_COMPLETE}} | {{TOTAL_COMPLETE}} |
| Draft | {{M_DRAFT}} | {{D_DRAFT}} | {{TOTAL_DRAFT}} |
| Pending | {{M_PENDING}} | {{D_PENDING}} | {{TOTAL_PENDING}} |
| N/A | {{M_NA}} | {{D_NA}} | {{TOTAL_NA}} |

---

## Section 1: Technical Requirements

| Ref | Requirement | Type | Response | Status | Owner |
|-----|-------------|------|----------|--------|-------|
| 3.1.1 | {{REQ}} | M | {{RESPONSE_SECTION}} | ✅ | {{OWNER}} |

---

## Submission Checklist
- [ ] All mandatory requirements addressed
- [ ] Technical volume complete
- [ ] Past performance complete
- [ ] Pricing complete
- [ ] All forms signed
- [ ] Format requirements met
- [ ] Red team review complete
```

## Requirement Extraction

### Convex Action

```typescript
// convex/compliance.ts
import { action, mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const generateMatrix = action({
  args: { rfpId: v.id("rfps") },
  handler: async (ctx, args) => {
    const rfp = await ctx.runQuery(internal.rfps.get, { id: args.rfpId });
    if (!rfp) throw new Error("RFP not found");

    // Extract requirements using AI
    const requirements = await extractRequirements(rfp);

    // Group into sections
    const sections = groupRequirements(requirements);

    // Create matrix
    const matrix: ComplianceMatrix = {
      rfpId: args.rfpId,
      rfpTitle: rfp.title,
      createdAt: new Date(),
      updatedAt: new Date(),
      status: "draft",
      sections,
      summary: calculateSummary(sections),
    };

    // Save to pursuit
    await ctx.runMutation(internal.pursuits.saveComplianceMatrix, {
      rfpId: args.rfpId,
      matrix: JSON.stringify(matrix),
    });

    return matrix;
  },
});
```

### AI Extraction

```typescript
async function extractRequirements(rfp: RFP): Promise<ComplianceRequirement[]> {
  const prompt = `
Analyze this RFP and extract ALL requirements.

RFP Title: ${rfp.title}
RFP Content: ${rfp.description}

For each requirement, identify:
1. Section reference (use sequential numbering if not available)
2. Exact requirement text
3. Type: mandatory (must/shall/required), desirable (should/may), or informational
4. Category: technical, management, past_performance, pricing, certifications, staffing, security, compliance, other

Respond with JSON array:
[
  {
    "reference": "3.1.1",
    "requirement": "System must support 1000 concurrent users",
    "type": "mandatory",
    "category": "technical"
  }
]`;

  const response = await callAIProvider(prompt);
  const parsed = JSON.parse(response);

  return parsed.map((req: any, index: number) => ({
    id: `req-${index + 1}`,
    reference: req.reference || `${index + 1}`,
    requirement: req.requirement,
    type: req.type,
    category: req.category,
    responseSection: "",
    responseText: "",
    evidence: "",
    owner: "",
    status: "pending" as const,
    notes: "",
  }));
}
```

### Grouping Logic

```typescript
function groupRequirements(
  requirements: ComplianceRequirement[]
): ComplianceSection[] {
  const groups = new Map<string, ComplianceRequirement[]>();

  for (const req of requirements) {
    const existing = groups.get(req.category) || [];
    existing.push(req);
    groups.set(req.category, existing);
  }

  const categoryNames: Record<string, string> = {
    technical: "Technical Requirements",
    management: "Management Requirements",
    past_performance: "Past Performance",
    pricing: "Pricing Requirements",
    certifications: "Certifications & Compliance",
    staffing: "Staffing Requirements",
    security: "Security Requirements",
    compliance: "Regulatory Compliance",
    other: "Other Requirements",
  };

  const order = [
    "technical",
    "management",
    "staffing",
    "past_performance",
    "security",
    "compliance",
    "pricing",
    "certifications",
    "other",
  ];

  return order
    .filter((cat) => groups.has(cat))
    .map((category) => ({
      id: category,
      name: categoryNames[category] || category,
      requirements: groups.get(category)!,
    }));
}
```

## Update Functions

```typescript
// convex/compliance.ts
export const updateRequirement = mutation({
  args: {
    rfpId: v.id("rfps"),
    requirementId: v.string(),
    updates: v.object({
      responseSection: v.optional(v.string()),
      responseText: v.optional(v.string()),
      evidence: v.optional(v.string()),
      owner: v.optional(v.string()),
      status: v.optional(v.string()),
      notes: v.optional(v.string()),
    }),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const pursuit = await ctx.db
      .query("pursuits")
      .withIndex("by_rfp", (q) => q.eq("rfpId", args.rfpId))
      .first();

    if (!pursuit?.complianceMatrix) {
      throw new Error("Compliance matrix not found");
    }

    const matrix: ComplianceMatrix = JSON.parse(pursuit.complianceMatrix);

    // Find and update requirement
    for (const section of matrix.sections) {
      const req = section.requirements.find((r) => r.id === args.requirementId);
      if (req) {
        Object.assign(req, args.updates);
        break;
      }
    }

    // Recalculate summary
    matrix.summary = calculateSummary(matrix.sections);
    matrix.updatedAt = new Date();

    await ctx.db.patch(pursuit._id, {
      complianceMatrix: JSON.stringify(matrix),
      updatedAt: Date.now(),
    });

    return matrix;
  },
});

export const getProgress = query({
  args: { rfpId: v.id("rfps") },
  handler: async (ctx, args) => {
    const pursuit = await ctx.db
      .query("pursuits")
      .withIndex("by_rfp", (q) => q.eq("rfpId", args.rfpId))
      .first();

    if (!pursuit?.complianceMatrix) return null;

    const matrix: ComplianceMatrix = JSON.parse(pursuit.complianceMatrix);

    return {
      summary: matrix.summary,
      byCategory: matrix.sections.map((s) => ({
        category: s.name,
        total: s.requirements.length,
        complete: s.requirements.filter((r) => r.status === "complete").length,
        mandatory: s.requirements.filter((r) => r.type === "mandatory").length,
      })),
      lastUpdated: matrix.updatedAt,
    };
  },
});
```

## UI Components

```tsx
// components/ComplianceMatrixView.tsx
export function ComplianceMatrixView({ rfpId }: { rfpId: Id<"rfps"> }) {
  const progress = useQuery(api.compliance.getProgress, { rfpId });
  const generateMatrix = useMutation(api.compliance.generateMatrix);

  if (progress === undefined) return <LoadingSpinner />;

  if (!progress) {
    return (
      <div className="p-6 text-center">
        <p className="text-muted-foreground mb-4">
          No compliance matrix generated yet.
        </p>
        <button
          onClick={() => generateMatrix({ rfpId })}
          className="px-4 py-2 bg-primary text-primary-foreground rounded"
        >
          Generate Compliance Matrix
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-4 gap-4">
        <SummaryCard
          label="Total"
          value={progress.summary.totalRequirements}
          color="blue"
        />
        <SummaryCard
          label="Complete"
          value={progress.summary.addressed}
          color="green"
        />
        <SummaryCard
          label="Pending"
          value={progress.summary.pending}
          color="yellow"
        />
        <SummaryCard
          label="Mandatory"
          value={progress.summary.mandatory}
          color="red"
        />
      </div>

      {/* Progress by Category */}
      <div className="space-y-2">
        {progress.byCategory.map((cat) => (
          <ProgressBar
            key={cat.category}
            label={cat.category}
            current={cat.complete}
            total={cat.total}
          />
        ))}
      </div>
    </div>
  );
}
```

## Export Formats

```typescript
export function exportToMarkdown(matrix: ComplianceMatrix): string {
  // See template above
}

export function exportToCsv(matrix: ComplianceMatrix): string {
  const headers = [
    "Section",
    "Reference",
    "Requirement",
    "Type",
    "Response Section",
    "Status",
    "Owner",
    "Notes",
  ];

  const rows = matrix.sections.flatMap((section) =>
    section.requirements.map((req) => [
      section.name,
      req.reference,
      `"${req.requirement.replace(/"/g, '""')}"`,
      req.type,
      req.responseSection,
      req.status,
      req.owner,
      `"${req.notes.replace(/"/g, '""')}"`,
    ])
  );

  return [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
}
```

## Status Legend

| Icon | Status | Meaning |
|------|--------|---------|
| ✅ | Complete | Fully addressed with evidence |
| 🔶 | Draft | Response written, needs review |
| ⏳ | Pending | Not yet started |
| ➖ | N/A | Not applicable to this proposal |
