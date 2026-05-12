// SOURCE-OF-TRUTH: shared/scripts/story-gate-runtime/lib/store.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { resolve } from "node:path";
import {
    createRuntimeStore,
    readJsonFile,
} from "../../coordinator-runtime/lib/core.mjs";
import {
    pipelineStageCoordinatorSummarySchema,
    qualitySummarySchema,
    testSummarySchema,
} from "../../coordinator-runtime/lib/schemas.mjs";
import { writeRuntimeArtifactJson } from "../../coordinator-runtime/lib/artifacts.mjs";
import { assertSchema } from "../../coordinator-runtime/lib/validate.mjs";
import { PHASES } from "./phases.mjs";

const gateManifestSchema = {
    type: "object",
    required: ["skill", "identifier", "story_id", "project_root", "created_at"],
    properties: {
        skill: { type: "string" },
        mode: { type: "string" },
        identifier: { type: "string" },
        story_id: { type: "string" },
        task_provider: { type: "string" },
        project_root: { type: "string" },
        worktree_dir: { type: "string" },
        branch: { type: "string" },
        fast_track_policy: { type: "object" },
        nfr_policy: { type: "object" },
        test_task_policy: { type: "object" },
        created_at: { type: "string", format: "date-time" },
    },
};

const gateStore = createRuntimeStore({
    baseRootParts: [".hex-skills", "story-gate", "runtime"],
    manifestSchema: gateManifestSchema,
    normalizeManifest(manifestInput, projectRoot) {
        return {
            skill: "ln-500",
            mode: manifestInput.mode || "story_gate",
            identifier: manifestInput.story_id || manifestInput.identifier,
            story_id: manifestInput.story_id || manifestInput.identifier,
            task_provider: manifestInput.task_provider || "unknown",
            project_root: resolve(projectRoot || process.cwd()),
            worktree_dir: manifestInput.worktree_dir || null,
            branch: manifestInput.branch || null,
            fast_track_policy: manifestInput.fast_track_policy || {},
            nfr_policy: manifestInput.nfr_policy || {},
            test_task_policy: manifestInput.test_task_policy || {},
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
            fast_track: false,
            quality_summary: null,
            child_runs: {},
            test_task_id: null,
            test_task_status: null,
            test_planner_invoked: false,
            quality_score: null,
            nfr_validation: {},
            fix_tasks_created: [],
            branch_finalized: false,
            story_final_status: null,
            stage_summary: null,
            self_check_passed: false,
            final_result: null,
            worktree_dir: manifest.worktree_dir,
            branch: manifest.branch,
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
} = gateStore;

export function recordQuality(projectRoot, runId, qualitySummary) {
    const run = loadRun(projectRoot, runId);
    if (!run) {
        return { ok: false, error: "Run not found" };
    }
    const validation = assertSchema(qualitySummarySchema, qualitySummary, "quality summary");
    if (!validation.ok) {
        return validation;
    }
    return updateState(projectRoot, runId, state => ({
        ...state,
        quality_summary: qualitySummary,
        quality_score: qualitySummary.quality_score ?? state.quality_score,
    }));
}

export function recordTestStatus(projectRoot, runId, testSummary) {
    const run = loadRun(projectRoot, runId);
    if (!run) {
        return { ok: false, error: "Run not found" };
    }
    const validation = assertSchema(testSummarySchema, testSummary, "test summary");
    if (!validation.ok) {
        return validation;
    }
    return updateState(projectRoot, runId, state => ({
        ...state,
        test_task_id: testSummary.test_task_id || state.test_task_id,
        test_task_status: testSummary.status || state.test_task_status,
        test_planner_invoked: state.test_planner_invoked || Boolean(testSummary.planner_invoked),
    }));
}

export function recordStageSummary(projectRoot, runId, summary) {
    const run = loadRun(projectRoot, runId);
    if (!run) {
        return { ok: false, error: "Run not found" };
    }
    if (summary?.run_id !== runId) {
        return { ok: false, error: `Stage summary run_id must match runtime run_id (${runId})` };
    }
    const validation = assertSchema(pipelineStageCoordinatorSummarySchema, summary, "pipeline stage coordinator summary");
    if (!validation.ok) {
        return validation;
    }
    return updateState(projectRoot, runId, state => {
        const artifactIdentifier = `${summary.identifier}-stage-${summary.payload.stage}`;
        const artifactPath = writeRuntimeArtifactJson(projectRoot, runId, summary.summary_kind, artifactIdentifier, summary);
        return {
            ...state,
            stage_summary: {
                ...summary,
                payload: {
                    ...summary.payload,
                    artifact_path: artifactPath,
                },
            },
        };
    });
}

export {
    readJsonFile,
};
