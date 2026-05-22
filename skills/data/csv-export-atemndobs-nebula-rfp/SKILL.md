---
name: csv-export
description: Export RFP data, evaluations, and pursuits in CSV and other formats. Use when implementing data export features, building reports, or extracting data for analysis.
allowed-tools: Read, Grep, Glob
---

# CSV Export Skill

## Overview

This skill implements data export functionality for RFPs, evaluations, and pursuit pipelines in multiple formats.

## Export Types

### RFP List Export

```typescript
interface RfpExportRow {
  id: string;
  externalId: string;
  source: string;
  title: string;
  description: string;
  location: string;
  category: string;
  postedDate: string;
  expiryDate: string;
  daysRemaining: number;
  url: string;
  // Evaluation
  score: number | null;
  isFit: boolean | null;
  eligibilityStatus: string | null;
  // Pursuit
  pursuitStatus: string | null;
  decision: string | null;
}
```

### Evaluation Export

```typescript
interface EvaluationExportRow {
  rfpId: string;
  rfpTitle: string;
  evaluatedAt: string;
  overallScore: number;
  isFit: boolean;
  eligibilityStatus: string;
  // Per-criterion (dynamic columns)
  [criterionName_score: string]: number;
  [criterionName_met: string]: boolean;
  [criterionName_keywords: string]: string;
  reasoning: string;
}
```

### Pursuit Pipeline Export

```typescript
interface PursuitExportRow {
  rfpId: string;
  rfpTitle: string;
  source: string;
  deadline: string;
  daysRemaining: number;
  status: string;
  decision: string;
  decisionBy: string;
  decisionDate: string;
  score: number;
  teamMembers: string;
  notes: string;
}
```

## CSV Generation

```typescript
// services/csvExport.ts

type ExportableValue = string | number | boolean | null | undefined;
type ExportRow = Record<string, ExportableValue>;

export function generateCsv(
  data: ExportRow[],
  options?: {
    headers?: string[];
    delimiter?: string;
    includeHeaders?: boolean;
  }
): string {
  if (data.length === 0) return "";

  const delimiter = options?.delimiter ?? ",";
  const includeHeaders = options?.includeHeaders ?? true;
  const headers = options?.headers ?? Object.keys(data[0]);

  const rows: string[] = [];

  // Header row
  if (includeHeaders) {
    rows.push(headers.map(escapeForCsv).join(delimiter));
  }

  // Data rows
  for (const row of data) {
    const values = headers.map((header) =>
      escapeForCsv(formatValue(row[header]))
    );
    rows.push(values.join(delimiter));
  }

  return rows.join("\n");
}

function escapeForCsv(value: string): string {
  if (value.includes(",") || value.includes('"') || value.includes("\n")) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

function formatValue(value: ExportableValue): string {
  if (value === null || value === undefined) return "";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (typeof value === "number") return value.toString();
  return String(value);
}

export function downloadCsv(csv: string, filename: string): void {
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
```

## Convex Export Queries

```typescript
// convex/exports.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const exportRfps = query({
  args: {
    source: v.optional(v.string()),
    showOnlyFit: v.optional(v.boolean()),
    limit: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    let q = ctx.db.query("rfps");

    if (args.source) {
      q = q.withIndex("by_source", (q) => q.eq("source", args.source));
    }

    const rfps = await q.take(args.limit ?? 500);

    // Join with evaluations and pursuits
    const exportData = await Promise.all(
      rfps.map(async (rfp) => {
        const evaluation = await ctx.db
          .query("evaluations")
          .withIndex("by_rfp", (q) => q.eq("rfpId", rfp._id))
          .order("desc")
          .first();

        const pursuit = await ctx.db
          .query("pursuits")
          .withIndex("by_rfp", (q) => q.eq("rfpId", rfp._id))
          .first();

        // Filter by fit if requested
        if (args.showOnlyFit && !evaluation?.isFit) {
          return null;
        }

        return {
          id: rfp._id,
          externalId: rfp.externalId,
          source: rfp.source,
          title: rfp.title,
          description: truncate(rfp.description, 500),
          location: rfp.location,
          category: rfp.category,
          postedDate: formatDate(rfp.postedDate),
          expiryDate: formatDate(rfp.expiryDate),
          daysRemaining: calculateDaysRemaining(rfp.expiryDate),
          url: rfp.url,
          score: evaluation?.score ?? null,
          isFit: evaluation?.isFit ?? null,
          eligibilityStatus: evaluation?.eligibility?.status ?? null,
          pursuitStatus: pursuit?.status ?? null,
          decision: pursuit?.decision ?? null,
        };
      })
    );

    return exportData.filter(Boolean);
  },
});

export const exportEvaluations = query({
  args: {
    startDate: v.optional(v.number()),
    endDate: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    let evaluations = await ctx.db.query("evaluations").collect();

    // Date filter
    if (args.startDate || args.endDate) {
      evaluations = evaluations.filter((e) => {
        if (args.startDate && e.evaluatedAt < args.startDate) return false;
        if (args.endDate && e.evaluatedAt > args.endDate) return false;
        return true;
      });
    }

    return Promise.all(
      evaluations.map(async (eval_) => {
        const rfp = await ctx.db.get(eval_.rfpId);

        // Flatten criteria results
        const criteriaData: Record<string, any> = {};
        for (const result of eval_.criteriaResults) {
          const key = result.criterionName.toLowerCase().replace(/\s+/g, "_");
          criteriaData[`${key}_score`] = result.score;
          criteriaData[`${key}_met`] = result.met;
          criteriaData[`${key}_keywords`] = result.matchedKeywords.join("; ");
        }

        return {
          rfpId: eval_.rfpId,
          rfpTitle: rfp?.title ?? "Unknown",
          evaluatedAt: formatDateTime(eval_.evaluatedAt),
          overallScore: eval_.score,
          isFit: eval_.isFit,
          eligibilityStatus: eval_.eligibility.status,
          ...criteriaData,
          reasoning: eval_.reasoning ?? "",
        };
      })
    );
  },
});

export const exportPursuits = query({
  args: {
    status: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    let q = ctx.db.query("pursuits");

    if (args.status) {
      q = q.filter((q) => q.eq(q.field("status"), args.status));
    }

    const pursuits = await q.collect();

    return Promise.all(
      pursuits.map(async (pursuit) => {
        const rfp = await ctx.db.get(pursuit.rfpId);
        const evaluation = await ctx.db
          .query("evaluations")
          .withIndex("by_rfp", (q) => q.eq("rfpId", pursuit.rfpId))
          .first();

        return {
          rfpId: pursuit.rfpId,
          rfpTitle: rfp?.title ?? "Unknown",
          source: rfp?.source ?? "Unknown",
          deadline: rfp ? formatDate(rfp.expiryDate) : "",
          daysRemaining: rfp ? calculateDaysRemaining(rfp.expiryDate) : null,
          status: pursuit.status,
          decision: pursuit.decision ?? "",
          decisionBy: pursuit.decisionBy ?? "",
          decisionDate: pursuit.decisionAt ? formatDate(pursuit.decisionAt) : "",
          score: evaluation?.score ?? null,
          teamMembers: pursuit.teamMembers?.join("; ") ?? "",
          notes: pursuit.notes ?? "",
        };
      })
    );
  },
});

// Helpers
function formatDate(timestamp: number): string {
  return new Date(timestamp).toISOString().split("T")[0];
}

function formatDateTime(timestamp: number): string {
  return new Date(timestamp).toISOString();
}

function calculateDaysRemaining(expiryDate: number): number {
  return Math.ceil((expiryDate - Date.now()) / (1000 * 60 * 60 * 24));
}

function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + "...";
}
```

## React Components

```tsx
// components/ExportButton.tsx
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";
import { generateCsv, downloadCsv } from "../services/csvExport";

interface ExportButtonProps {
  exportType: "rfps" | "evaluations" | "pursuits";
  filters?: Record<string, any>;
  filename?: string;
}

export function ExportButton({ exportType, filters, filename }: ExportButtonProps) {
  const [isExporting, setIsExporting] = useState(false);

  // Get query based on type
  const queryFn =
    exportType === "rfps"
      ? api.exports.exportRfps
      : exportType === "evaluations"
        ? api.exports.exportEvaluations
        : api.exports.exportPursuits;

  const data = useQuery(queryFn, filters ?? {});

  const handleExport = () => {
    if (!data) return;

    setIsExporting(true);
    try {
      const csv = generateCsv(data);
      const defaultFilename = `${exportType}-${formatDateForFilename(new Date())}.csv`;
      downloadCsv(csv, filename ?? defaultFilename);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={isExporting || !data}
      className="flex items-center gap-2 px-4 py-2 bg-secondary text-secondary-foreground rounded hover:bg-secondary/80 disabled:opacity-50"
    >
      <DownloadIcon className="w-4 h-4" />
      {isExporting ? "Exporting..." : "Export CSV"}
    </button>
  );
}
```

### Export Panel

```tsx
// components/ExportPanel.tsx
export function ExportPanel() {
  const [exportType, setExportType] = useState<"rfps" | "evaluations" | "pursuits">("rfps");
  const [filters, setFilters] = useState({
    source: "",
    showOnlyFit: false,
    status: "",
  });

  return (
    <div className="p-6 bg-card rounded-lg space-y-4">
      <h2 className="text-xl font-semibold">Export Data</h2>

      {/* Export Type */}
      <div>
        <label className="block text-sm text-muted-foreground mb-2">
          Export Type
        </label>
        <select
          value={exportType}
          onChange={(e) => setExportType(e.target.value as any)}
          className="w-full p-2 bg-background border rounded"
        >
          <option value="rfps">RFP List</option>
          <option value="evaluations">Evaluation Details</option>
          <option value="pursuits">Pursuit Pipeline</option>
        </select>
      </div>

      {/* Filters */}
      {exportType === "rfps" && (
        <div className="space-y-2">
          <select
            value={filters.source}
            onChange={(e) => setFilters({ ...filters, source: e.target.value })}
            className="w-full p-2 bg-background border rounded"
          >
            <option value="">All Sources</option>
            <option value="sam.gov">SAM.gov</option>
            <option value="emma">Maryland eMMA</option>
            <option value="rfpmart">RFPMart</option>
          </select>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={filters.showOnlyFit}
              onChange={(e) =>
                setFilters({ ...filters, showOnlyFit: e.target.checked })
              }
            />
            <span className="text-sm">Show only fit opportunities</span>
          </label>
        </div>
      )}

      <ExportButton exportType={exportType} filters={filters} />

      <p className="text-xs text-muted-foreground">
        Exports include all visible columns. Dates are in ISO 8601 format.
      </p>
    </div>
  );
}
```

## JSON Export Alternative

```typescript
export function downloadJson(data: any, filename: string): void {
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
```

## Selected Items Export

```tsx
// components/SelectionExport.tsx
export function SelectionExport({
  selectedIds,
}: {
  selectedIds: Id<"rfps">[];
}) {
  const exportSelected = async () => {
    const data = await convex.query(api.exports.exportRfps, {
      rfpIds: selectedIds,
    });
    const csv = generateCsv(data);
    downloadCsv(csv, `selected-rfps-${formatDate(new Date())}.csv`);
  };

  return (
    <button
      onClick={exportSelected}
      disabled={selectedIds.length === 0}
      className="px-4 py-2 bg-primary text-primary-foreground rounded disabled:opacity-50"
    >
      Export {selectedIds.length} Selected
    </button>
  );
}
```
