// SOURCE-OF-TRUTH: shared/scripts/planning-worker-runtime/lib/store.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { resolveWorkerManifestBase, buildWorkerManifestSchema, createWorkerRuntimeStore, createWorkerState } from "../../coordinator-runtime/lib/worker-runtime.mjs";
import {
    opportunityDiscoveryWorkerSummarySchema,
    storyPlanWorkerSummarySchema,
    storyPrioritizationWorkerSummarySchema,
} from "../../coordinator-runtime/lib/schemas.mjs";
import { getWorkerPhases } from "./phases.mjs";

const planningWorkerManifestSchema = buildWorkerManifestSchema("work_item_id", {
    epic_id: { type: "string" },
    input_mode: { type: "string" },
    depth: { type: "string" },
    task_provider: { type: "string" },
    auto_approve: { type: "boolean" },
});

function expectedSummaryKindForSkill(skill) {
    if (skill === "ln-201") {
        return "opportunity-discovery-worker";
    }
    if (skill === "ln-230") {
        return "story-prioritization-worker";
    }
    if (skill === "ln-221" || skill === "ln-222") {
        return "story-plan-worker";
    }
    throw new Error(`Unsupported planning worker skill: ${skill}`);
}

function summarySchemaForSkill(skill) {
    if (skill === "ln-201") {
        return opportunityDiscoveryWorkerSummarySchema;
    }
    if (skill === "ln-230") {
        return storyPrioritizationWorkerSummarySchema;
    }
    if (skill === "ln-221" || skill === "ln-222") {
        return storyPlanWorkerSummarySchema;
    }
    throw new Error(`Unsupported planning worker skill: ${skill}`);
}

const planningWorkerStore = createWorkerRuntimeStore({
    baseRootParts: [".hex-skills", "planning-worker", "runtime"],
    manifestSchema: planningWorkerManifestSchema,
    normalizeManifest(manifestInput, projectRoot) {
        const epicId = manifestInput.epic_id || null;
        const identifier = manifestInput.identifier
            || (manifestInput.skill === "ln-201" ? manifestInput.work_item_id || "discovery" : `epic-${epicId || "unknown"}`);
        return {
            ...resolveWorkerManifestBase(manifestInput, projectRoot, "work_item_id", identifier),
            skill: manifestInput.skill,
            mode: manifestInput.mode || "planning_worker",
            ...(epicId ? { epic_id: epicId } : {}),
            input_mode: manifestInput.input_mode || "ideas",
            depth: manifestInput.depth || "standard",
            task_provider: manifestInput.task_provider || "unknown",
            auto_approve: manifestInput.auto_approve === true,
        };
    },
    defaultState(manifest, runId) {
        const phases = getWorkerPhases(manifest.skill);
        return createWorkerState(manifest, runId, phases[0], {
            epic_id: manifest.epic_id || null,
            summary_kind: expectedSummaryKindForSkill(manifest.skill),
        });
    },
    summarySchema: {
        type: "object",
    },
    summaryLabel: "planning worker summary",
    expectedSummaryKind(manifest) {
        return expectedSummaryKindForSkill(manifest.skill);
    },
    buildArtifactFileName(manifest) {
        return `${manifest.skill}--${manifest.identifier}.json`;
    },
    validateSummary(manifest, summary) {
        const schema = summarySchemaForSkill(manifest.skill);
        const expectedSummaryKind = expectedSummaryKindForSkill(manifest.skill);
        const validation = schema
            && summary.summary_kind === expectedSummaryKind
            ? { ok: true }
            : { ok: false, error: `Worker summary kind must be ${expectedSummaryKind}` };
        if (!validation.ok) {
            return validation;
        }
        if (manifest.skill !== "ln-201" && summary.payload?.epic_id !== manifest.epic_id) {
            return { ok: false, error: `Worker summary epic_id must match manifest epic_id (${manifest.epic_id})` };
        }
        return { ok: true };
    },
    reduceState(state, summary) {
        return {
            ...state,
            summary_kind: summary.summary_kind,
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
    recordSummary,
    resolveRunId,
    runtimePaths,
    saveState,
    startRun,
    updateState,
    readJsonFile,
} = planningWorkerStore;
