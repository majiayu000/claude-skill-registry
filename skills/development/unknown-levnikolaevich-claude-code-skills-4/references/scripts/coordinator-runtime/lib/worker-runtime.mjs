// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/worker-runtime.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { randomUUID } from "node:crypto";
import { resolve } from "node:path";
import { createRuntimeStore, readJsonFile } from "./core.mjs";
import { runtimeArtifactPathForFile, writeRuntimeArtifactJsonToPath } from "./artifacts.mjs";
import { assertSchema } from "./validate.mjs";

function safeSegment(value) {
    return String(value || "default")
        .trim()
        .replace(/[^a-zA-Z0-9._-]+/g, "-")
        .replace(/^-+|-+$/g, "")
        .toLowerCase() || "default";
}

function defaultWorkerRunId(skill, identifier) {
    return `${safeSegment(skill)}-${safeSegment(identifier)}-${Date.now()}-${randomUUID().slice(0, 8)}`;
}

export function buildWorkerManifestSchema(identifierField, extraProperties = {}, extraRequired = []) {
    return {
        type: "object",
        required: ["skill", "identifier", "project_root", "created_at", ...extraRequired],
        properties: {
            skill: { type: "string", minLength: 1 },
            mode: { type: "string" },
            identifier: { type: "string", minLength: 1 },
            [identifierField]: { type: "string", minLength: 1 },
            project_root: { type: "string" },
            summary_artifact_path: { type: ["string", "null"] },
            created_at: { type: "string", format: "date-time" },
            ...extraProperties,
        },
    };
}

export function createWorkerState(manifest, runId, phase, extraState = {}) {
    return {
        run_id: runId,
        skill: manifest.skill,
        mode: manifest.mode || null,
        identifier: manifest.identifier,
        phase,
        complete: false,
        paused_reason: null,
        pending_decision: null,
        decisions: [],
        final_result: null,
        self_check_passed: false,
        summary_recorded: false,
        summary_artifact_path: manifest.summary_artifact_path || null,
        summary_written_at: null,
        summary: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ...extraState,
    };
}

export function createWorkerRuntimeStore({
    baseRootParts,
    manifestSchema,
    normalizeManifest,
    defaultState,
    summarySchema,
    summaryLabel,
    expectedSummaryKind,
    buildArtifactFileName,
    validateSummary,
    reduceState,
}) {
    const store = createRuntimeStore({
        baseRootParts,
        manifestSchema,
        normalizeManifest,
        defaultState,
        buildRunId(skill, identifier, manifestInput) {
            return manifestInput.run_id || defaultWorkerRunId(skill, identifier);
        },
    });

    function recordSummary(projectRoot, runId, summary) {
        const run = store.loadRun(projectRoot, runId);
        if (!run) {
            return { ok: false, error: "Run not found" };
        }
        const validation = assertSchema(summarySchema, summary, summaryLabel);
        if (!validation.ok) {
            return validation;
        }
        if (summary.run_id !== runId) {
            return { ok: false, error: `Worker summary run_id must match runtime run_id (${runId})` };
        }
        if (summary.identifier !== run.manifest.identifier) {
            return { ok: false, error: `Worker summary identifier must match runtime identifier (${run.manifest.identifier})` };
        }
        if (summary.producer_skill !== run.manifest.skill) {
            return { ok: false, error: `Worker summary producer_skill must match runtime skill (${run.manifest.skill})` };
        }
        const resolvedExpectedSummaryKind = typeof expectedSummaryKind === "function"
            ? expectedSummaryKind(run.manifest, summary)
            : expectedSummaryKind;
        if (resolvedExpectedSummaryKind && summary.summary_kind !== resolvedExpectedSummaryKind) {
            return { ok: false, error: `Worker summary kind must be ${resolvedExpectedSummaryKind}` };
        }
        if (summary.payload && typeof summary.payload === "object" && Object.prototype.hasOwnProperty.call(summary.payload, "worker")
            && summary.payload.worker !== run.manifest.skill) {
            return { ok: false, error: `Worker summary payload.worker must match runtime skill (${run.manifest.skill})` };
        }
        if (typeof validateSummary === "function") {
            const summaryValidation = validateSummary(run.manifest, summary);
            if (summaryValidation?.ok === false) {
                return summaryValidation;
            }
        }
        const artifactPath = run.manifest.summary_artifact_path
            ? writeRuntimeArtifactJsonToPath(projectRoot, run.manifest.summary_artifact_path, summary)
            : writeRuntimeArtifactJsonToPath(
                projectRoot,
                runtimeArtifactPathForFile(projectRoot, runId, expectedSummaryKind, buildArtifactFileName(run.manifest, summary)),
                summary,
            );
        const updated = store.updateState(projectRoot, runId, state => {
            const nextState = {
                ...state,
                summary_recorded: true,
                summary_artifact_path: artifactPath,
                summary_written_at: new Date().toISOString(),
                summary,
            };
            if (typeof reduceState === "function") {
                return reduceState(nextState, summary);
            }
            return nextState;
        });
        if (!updated.ok) {
            return updated;
        }
        return {
            ok: true,
            artifact_path: artifactPath,
            state: updated.state,
        };
    }

    return {
        ...store,
        recordSummary,
        readJsonFile,
    };
}

export function resolveWorkerManifestBase(manifestInput, projectRoot, identifierField, identifierValue) {
    return {
        ...manifestInput,
        identifier: identifierValue,
        [identifierField]: identifierValue,
        project_root: resolve(projectRoot || process.cwd()),
        summary_artifact_path: manifestInput.summary_artifact_path || null,
        created_at: new Date().toISOString(),
    };
}
