#!/usr/bin/env node
// SOURCE-OF-TRUTH: shared/scripts/story-planning-runtime/cli.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

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
    recordEpic,
    recordPlanSummary,
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
import { PLANNING_PROGRESS_STATUSES } from "../coordinator-runtime/lib/runtime-constants.mjs";

const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
        "project-root": { type: "string", default: process.cwd() },
        "run-id": { type: "string" },
        epic: { type: "string" },
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
        skill: "ln-220",
        runId: values["run-id"],
        identifier: values.epic ? `epic-${values.epic}` : null,
        identifierFlag: "epic",
        listActiveRuns,
        resolveRunId,
        loadRun,
        fail,
    });
}

function applyCheckpointToState(state, phase, payload) {
    const nextState = { ...state };

    if (phase === PHASES.CONTEXT_ASSEMBLY) {
        nextState.context_ready = payload.context_ready === true;
    }
    if (phase === PHASES.RESEARCH) {
        nextState.research_status = payload.research_status || PLANNING_PROGRESS_STATUSES.COMPLETED;
        nextState.research_file = payload.research_file || nextState.research_file;
    }
    if (phase === PHASES.PLAN) {
        nextState.ideal_plan_summary = payload.ideal_plan_summary || payload.plan_summary || payload;
    }
    if (phase === PHASES.ROUTING) {
        nextState.routing_summary = payload.routing_summary || payload;
    }
    if (phase === PHASES.MODE_DETECTION) {
        nextState.epic_group_modes = payload.epic_group_modes || payload.group_modes || {};
    }
    if (phase === PHASES.FINALIZE) {
        nextState.final_result = payload.final_result || nextState.final_result;
        if (payload.template_compliance_passed === true) {
            nextState.template_compliance_passed = true;
        }
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
        if (!values.epic || !values["manifest-file"]) {
            fail("start requires --epic and --manifest-file");
        }
        const manifest = readManifestOrFail(values, readJsonFile);
        const result = startRun(projectRoot, {
            ...manifest,
            epic_id: values.epic,
            identifier: `epic-${values.epic}`,
        });
        output(result);
        process.exit(result.ok ? 0 : 1);
    }

    if (command === "status") {
        const run = loadPlanningStatusRun({
            projectRoot,
            skill: "ln-220",
            runId: values["run-id"],
            identifier: values.epic ? `epic-${values.epic}` : null,
            identifierFlag: "epic",
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

    if (command === "record-epic") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordEpic(projectRoot, runId, payload);
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

    if (command === "record-plan-summary") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordPlanSummary(projectRoot, runId, payload);
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

    fail("Unknown command. Use: start, status, advance, checkpoint, record-epic, record-plan-summary, set-decision, pause, complete");
}

main().catch(error => fail(error.message));
