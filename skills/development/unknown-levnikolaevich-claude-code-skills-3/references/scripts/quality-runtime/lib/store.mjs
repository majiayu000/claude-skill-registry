// SOURCE-OF-TRUTH: shared/scripts/quality-runtime/lib/store.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { resolve } from "node:path";
import {
    createRuntimeStore,
    readJsonFile,
} from "../../coordinator-runtime/lib/core.mjs";
import {
    qualityWorkerSummarySchema,
} from "../../coordinator-runtime/lib/schemas.mjs";
import { assertSchema } from "../../coordinator-runtime/lib/validate.mjs";
import { PHASES } from "./phases.mjs";

const manifestSchema = {
    type: "object",
    required: ["skill", "identifier", "story_id", "project_root", "created_at"],
    properties: {
        skill: { type: "string" },
        mode: { type: "string" },
        identifier: { type: "string" },
        story_id: { type: "string" },
        fast_track: { type: "boolean" },
        project_root: { type: "string" },
        task_provider: { type: "string" },
        created_at: { type: "string", format: "date-time" },
    },
};

const qualityStore = createRuntimeStore({
    baseRootParts: [".hex-skills", "quality", "runtime"],
    manifestSchema,
    normalizeManifest(manifestInput, projectRoot) {
        return {
            skill: "ln-510",
            mode: manifestInput.mode || "quality_gate",
            identifier: manifestInput.story_id || manifestInput.identifier,
            story_id: manifestInput.story_id || manifestInput.identifier,
            fast_track: manifestInput.fast_track === true,
            task_provider: manifestInput.task_provider || "unknown",
            project_root: resolve(projectRoot || process.cwd()),
            created_at: new Date().toISOString(),
        };
    },
    defaultState(manifest, runId) {
        return {
            run_id: runId,
            skill: manifest.skill,
            mode: manifest.mode,
            identifier: manifest.identifier,
            story_id: manifest.story_id,
            phase: PHASES.CONFIG,
            complete: false,
            paused_reason: null,
            pending_decision: null,
            decisions: [],
            fast_track: manifest.fast_track,
            worker_results: {},
            child_runs: {},
            review_summary: null,
            criteria_summary: null,
            linters_summary: null,
            aggregated_issues: [],
            quality_score: null,
            quality_verdict: null,
            self_check_passed: false,
            final_result: null,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
        };
    },
});

export const {
    checkpointPhase,
    completeRun,
    loadActiveRun,
    listActiveRuns,
    loadRun,
    pauseRun,
    resolveRunId,
    runtimePaths,
    saveState,
    startRun,
    updateState,
} = qualityStore;

export { readJsonFile };

export function recordWorker(projectRoot, runId, summary) {
    const run = loadRun(projectRoot, runId);
    if (!run) {
        return { ok: false, error: "Run not found" };
    }
    const validation = assertSchema(qualityWorkerSummarySchema, summary, "quality worker summary");
    if (!validation.ok) {
        return validation;
    }
    return updateState(projectRoot, runId, state => ({
        ...state,
        worker_results: {
            ...state.worker_results,
            [summary.payload.worker]: summary,
        },
    }));
}
