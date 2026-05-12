#!/usr/bin/env node
// SOURCE-OF-TRUTH: shared/scripts/quality-runtime/cli.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { parseArgs } from "node:util";
import {
    checkpointPhase,
    completeRun,
    listActiveRuns,
    loadActiveRun,
    loadRun,
    pauseRun,
    readJsonFile,
    recordWorker,
    resolveRunId,
    runtimePaths,
    saveState,
    startRun,
} from "./lib/store.mjs";
import {
    failJson as fail,
    failResult,
    outputGuardFailure,
    outputInactiveRuntime,
    outputJson as output,
    outputRuntimeState,
    outputRuntimeStatus,
    readManifestOrFail,
    readPayload,
} from "../coordinator-runtime/lib/cli-helpers.mjs";
import { computeResumeAction, validateTransition } from "./lib/guards.mjs";
import { PHASES } from "./lib/phases.mjs";

const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
        "project-root": { type: "string", default: process.cwd() },
        "run-id": { type: "string" },
        story: { type: "string" },
        phase: { type: "string" },
        to: { type: "string" },
        payload: { type: "string" },
        "payload-file": { type: "string" },
        "manifest-file": { type: "string" },
        reason: { type: "string" },
        resolve: { type: "boolean", default: false },
    },
});

function resolveRun(projectRoot) {
    const runId = resolveRunId(projectRoot, "ln-510", values["run-id"], values.story);
    if (!runId) {
        const activeRuns = listActiveRuns(projectRoot, "ln-510");
        if (activeRuns.length > 1 && !values.story) {
            fail("Multiple active ln-510 runs found. Pass --story or --run-id.");
        }
        fail("No active ln-510 run found. Pass --story or --run-id.");
    }
    const run = loadRun(projectRoot, runId);
    if (!run) {
        fail(`Run not found: ${runId}`);
    }
    return { runId, run };
}

function applyCheckpointToState(state, phase, payload) {
    const nextState = { ...state };
    if ([PHASES.CODE_QUALITY, PHASES.CLEANUP, PHASES.REGRESSION, PHASES.LOG_ANALYSIS].includes(phase)
        && payload.child_run?.worker) {
        nextState.child_runs = {
            ...(nextState.child_runs || {}),
            [payload.child_run.worker]: payload.child_run,
        };
    }
    if (phase === PHASES.FINALIZE) {
        nextState.quality_score = payload.quality_score ?? nextState.quality_score;
        nextState.quality_verdict = payload.quality_verdict || nextState.quality_verdict;
        nextState.aggregated_issues = payload.aggregated_issues || nextState.aggregated_issues;
        nextState.final_result = payload.final_result || payload.quality_verdict || nextState.final_result;
    }
    if (phase === PHASES.AGENT_REVIEW) {
        nextState.review_summary = payload.review_summary || payload;
    }
    if (phase === PHASES.CRITERIA) {
        nextState.criteria_summary = payload.criteria_summary || payload;
    }
    if (phase === PHASES.LINTERS) {
        nextState.linters_summary = payload.linters_summary || payload;
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
        if (!values.story || !values["manifest-file"]) {
            fail("start requires --story and --manifest-file");
        }
        const manifest = readManifestOrFail(values, readJsonFile);
        const result = startRun(projectRoot, {
            ...manifest,
            story_id: values.story,
            identifier: values.story,
        });
        output(result);
        process.exit(result.ok ? 0 : 1);
    }

    if (command === "status") {
        if (!values["run-id"] && !values.story) {
            const activeRuns = listActiveRuns(projectRoot, "ln-510");
            if (activeRuns.length > 1) {
                output({ ok: false, error: "Multiple active ln-510 runs found. Pass --story or --run-id." });
                process.exit(1);
            }
        }
        const run = values["run-id"]
            ? loadRun(projectRoot, values["run-id"])
            : loadActiveRun(projectRoot, "ln-510", values.story);
        if (!run) {
            outputInactiveRuntime(output);
            return;
        }
        outputRuntimeStatus(output, projectRoot, run, runtimePaths, computeResumeAction);
        return;
    }

    if (command === "advance") {
        if (!values.to) {
            fail("advance requires --to");
        }
        const { runId, run } = resolveRun(projectRoot);
        if (run.state.phase === PHASES.PAUSED && values.resolve) {
            const resumed = saveState(projectRoot, runId, {
                ...run.state,
                phase: values.to,
                paused_reason: null,
            });
            if (resumed?.ok === false) {
                outputGuardFailure(output, resumed);
            }
            outputRuntimeState(output, run, resumed, { resumed_from: "PAUSED" });
            return;
        }
        const guard = validateTransition(run.manifest, run.state, run.checkpoints, values.to);
        if (!guard.ok) {
            outputGuardFailure(output, guard);
        }
        const nextState = saveState(projectRoot, runId, {
            ...run.state,
            phase: values.to,
            complete: values.to === PHASES.DONE ? true : run.state.complete,
            paused_reason: null,
        });
        if (nextState?.ok === false) {
            outputGuardFailure(output, nextState);
        }
        outputRuntimeState(output, run, nextState);
        return;
    }

    if (command === "checkpoint") {
        if (!values.phase) {
            fail("checkpoint requires --phase");
        }
        const payload = readPayload(values, readJsonFile);
        const { runId, run } = resolveRun(projectRoot);
        const checkpointed = checkpointPhase(projectRoot, runId, values.phase, payload);
        if (!checkpointed.ok) {
            fail(checkpointed.error);
        }
        const nextState = saveState(projectRoot, runId, applyCheckpointToState(run.state, values.phase, payload));
        if (nextState?.ok === false) {
            failResult(nextState);
        }
        outputRuntimeState(output, run, nextState, {
            checkpoint: checkpointed.checkpoints[values.phase],
            history_length: checkpointed.checkpoints._history.length,
        });
        return;
    }

    if (command === "record-worker") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordWorker(projectRoot, runId, payload);
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    if (command === "pause") {
        const { runId } = resolveRun(projectRoot);
        const result = pauseRun(projectRoot, runId, values.reason || "Paused");
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    if (command === "complete") {
        const { runId, run } = resolveRun(projectRoot);
        const guard = validateTransition(run.manifest, run.state, run.checkpoints, PHASES.DONE);
        if (!guard.ok) {
            outputGuardFailure(output, guard);
        }
        const result = completeRun(projectRoot, runId);
        if (!result.ok) {
            failResult(result);
        }
        output(result);
        return;
    }

    fail("Unknown command. Use: start, status, advance, checkpoint, record-worker, pause, complete");
}

main().catch(error => fail(error.message));
