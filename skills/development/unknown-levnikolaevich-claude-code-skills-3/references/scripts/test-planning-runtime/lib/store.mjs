// SOURCE-OF-TRUTH: shared/scripts/test-planning-runtime/lib/store.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { resolve } from "node:path";
import {
    createRuntimeStore,
    readJsonFile,
} from "../../coordinator-runtime/lib/core.mjs";
import {
    testPlanningWorkerSummarySchema,
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
        simplified: { type: "boolean" },
        project_root: { type: "string" },
        task_provider: { type: "string" },
        created_at: { type: "string", format: "date-time" },
    },
};

const plannerStore = createRuntimeStore({
    baseRootParts: [".hex-skills", "test-planning", "runtime"],
    manifestSchema,
    normalizeManifest(manifestInput, projectRoot) {
        return {
            skill: "ln-520",
            mode: manifestInput.mode || "test_planning",
            identifier: manifestInput.story_id || manifestInput.identifier,
            story_id: manifestInput.story_id || manifestInput.identifier,
            simplified: manifestInput.simplified === true,
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
            simplified: manifest.simplified,
            worker_results: {},
            child_runs: {},
            research_status: null,
            manual_status: null,
            test_task_id: null,
            test_task_url: null,
            coverage_summary: null,
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
} = plannerStore;

export { readJsonFile };

export function recordWorker(projectRoot, runId, summary) {
    const run = loadRun(projectRoot, runId);
    if (!run) {
        return { ok: false, error: "Run not found" };
    }
    const validation = assertSchema(testPlanningWorkerSummarySchema, summary, "test-planning worker summary");
    if (!validation.ok) {
        return validation;
    }
    return updateState(projectRoot, runId, state => ({
        ...state,
        worker_results: {
            ...state.worker_results,
            [summary.payload.worker]: summary,
        },
        research_status: summary.payload.worker === "ln-521" ? summary.payload.status : state.research_status,
        manual_status: summary.payload.worker === "ln-522" ? summary.payload.status : state.manual_status,
        test_task_id: summary.payload.test_task_id || state.test_task_id,
        test_task_url: summary.payload.test_task_url || state.test_task_url,
        coverage_summary: summary.payload.coverage_summary || state.coverage_summary,
    }));
}
