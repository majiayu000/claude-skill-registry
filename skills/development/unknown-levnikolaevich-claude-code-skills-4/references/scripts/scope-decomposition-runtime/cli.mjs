#!/usr/bin/env node
// SOURCE-OF-TRUTH: shared/scripts/scope-decomposition-runtime/cli.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { parseArgs } from "node:util";
import {
    checkpointPhase,
    completeRun,
    listActiveRuns,
    loadActiveRun,
    loadRun,
    pauseRun,
    readJsonFile,
    recordDecision,
    recordEpicSummary,
    recordPrioritizationSummary,
    recordScopeSummary,
    recordStorySummary,
    resolveRunId,
    runtimePaths,
    saveState,
    setPendingDecision,
    startRun,
} from "./lib/store.mjs";
import {
    failJson as fail,
    failResult,
    outputJson as output,
    readManifestOrFail,
    readPayload,
} from "../coordinator-runtime/lib/cli-helpers.mjs";
import { computeResumeAction, validateTransition } from "./lib/guards.mjs";
import { PHASES } from "./lib/phases.mjs";
import {
    advancePlanningRun,
    checkpointPlanningRun,
    completePlanningRun,
    loadPlanningStatusRun,
    outputInactiveRuntime,
    outputPlanningStatus,
    pausePlanningRun,
    resolvePlanningRunOrFail,
} from "../planning-runtime/lib/cli.mjs";

const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
        "project-root": { type: "string", default: process.cwd() },
        "run-id": { type: "string" },
        identifier: { type: "string" },
        phase: { type: "string" },
        to: { type: "string" },
        payload: { type: "string" },
        "payload-file": { type: "string" },
        "manifest-file": { type: "string" },
        reason: { type: "string" },
    },
});

function resolveRun(projectRoot) {
    return resolvePlanningRunOrFail({
        projectRoot,
        skill: "ln-200",
        runId: values["run-id"],
        identifier: values.identifier || "scope",
        identifierFlag: "identifier",
        listActiveRuns,
        resolveRunId,
        loadRun,
        fail,
    });
}

function applyCheckpointToState(state, phase, payload) {
    const nextState = { ...state };
    if (phase === PHASES.DISCOVERY) {
        nextState.discovery_summary = payload.discovery_summary || payload;
    }
    if (phase === PHASES.PRIORITIZATION_LOOP) {
        if (typeof payload.prioritization_enabled === "boolean") {
            nextState.prioritization_enabled = payload.prioritization_enabled;
        }
        if (Array.isArray(payload.expected_prioritization_epics)) {
            nextState.expected_prioritization_epics = payload.expected_prioritization_epics;
        } else if (payload.prioritization_enabled === true && (!nextState.expected_prioritization_epics || nextState.expected_prioritization_epics.length === 0)) {
            nextState.expected_prioritization_epics = Object.keys(nextState.story_summaries || {});
        }
        if (payload.prioritization_summaries && typeof payload.prioritization_summaries === "object") {
            nextState.prioritization_summaries = {
                ...(nextState.prioritization_summaries || {}),
                ...payload.prioritization_summaries,
            };
        }
    }
    if (phase === PHASES.FINALIZE) {
        nextState.final_result = payload.final_result || nextState.final_result;
    }
    if (phase === PHASES.SELF_CHECK) {
        nextState.self_check_passed = payload.pass === true;
        nextState.final_result = payload.final_result || nextState.final_result;
    }
    return nextState;
}

async function main() {
    const command = positionals[0];
    const projectRoot = values["project-root"];

    if (command === "start") {
        if (!values["manifest-file"]) {
            fail("start requires --manifest-file");
        }
        const manifest = readManifestOrFail(values, readJsonFile);
        const result = startRun(projectRoot, {
            ...manifest,
            identifier: values.identifier || manifest.identifier || "scope",
        });
        output(result);
        process.exit(result.ok ? 0 : 1);
    }

    if (command === "status") {
        const run = loadPlanningStatusRun({
            projectRoot,
            skill: "ln-200",
            runId: values["run-id"],
            identifier: values.identifier || "scope",
            identifierFlag: "identifier",
            listActiveRuns,
            loadRun,
            loadActiveRun,
            output,
        });
        if (!run) {
            outputInactiveRuntime(output);
            return;
        }
        outputPlanningStatus(projectRoot, run, runtimePaths, computeResumeAction, output);
        return;
    }

    if (command === "advance") {
        if (!values.to) {
            fail("advance requires --to");
        }
        const { runId, run } = resolveRun(projectRoot);
        advancePlanningRun(projectRoot, runId, run, values.to, validateTransition, saveState, PHASES.DONE, output);
        return;
    }

    if (command === "checkpoint") {
        if (!values.phase) {
            fail("checkpoint requires --phase");
        }
        const payload = readPayload(values, readJsonFile);
        const { runId, run } = resolveRun(projectRoot);
        checkpointPlanningRun(projectRoot, runId, run, values.phase, payload, checkpointPhase, saveState, applyCheckpointToState, fail, output);
        return;
    }

    if (command === "record-epic-summary") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordEpicSummary(projectRoot, runId, payload);
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    if (command === "record-story-summary") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordStorySummary(projectRoot, runId, payload);
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    if (command === "set-decision") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordDecision(projectRoot, runId, payload);
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    if (command === "record-prioritization-summary") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordPrioritizationSummary(projectRoot, runId, payload);
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    if (command === "record-scope-summary") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordScopeSummary(projectRoot, runId, payload);
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    if (command === "pause") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        pausePlanningRun(projectRoot, runId, payload, values.reason, pauseRun, setPendingDecision, fail, output);
        return;
    }

    if (command === "complete") {
        const { runId, run } = resolveRun(projectRoot);
        completePlanningRun(projectRoot, runId, run, validateTransition, completeRun, PHASES.DONE, fail, output);
        return;
    }

    fail("Unknown command. Use: start, status, advance, checkpoint, record-epic-summary, record-story-summary, record-prioritization-summary, record-scope-summary, set-decision, pause, complete");
}

main().catch(error => fail(error.message));
