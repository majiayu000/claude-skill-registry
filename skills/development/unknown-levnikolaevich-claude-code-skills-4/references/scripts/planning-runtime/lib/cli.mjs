// SOURCE-OF-TRUTH: shared/scripts/planning-runtime/lib/cli.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import {
    outputGuardFailure,
    outputInactiveRuntime,
    outputRuntimeState,
    outputRuntimeStatus,
} from "../../coordinator-runtime/lib/cli-helpers.mjs";

export function resolvePlanningRunOrFail({
    projectRoot,
    skill,
    runId,
    identifier,
    identifierFlag,
    listActiveRuns,
    resolveRunId,
    loadRun,
    fail,
}) {
    const resolvedRunId = resolveRunId(projectRoot, skill, runId, identifier);
    if (!resolvedRunId) {
        const activeRuns = listActiveRuns(projectRoot, skill);
        if (activeRuns.length > 1 && !identifier) {
            fail(`Multiple active ${skill} runs found. Pass --${identifierFlag} or --run-id.`);
        }
        fail(`No active ${skill} run found. Pass --${identifierFlag} or --run-id.`);
    }
    const run = loadRun(projectRoot, resolvedRunId);
    if (!run) {
        fail(`Run not found: ${resolvedRunId}`);
    }
    return { runId: resolvedRunId, run };
}

export function loadPlanningStatusRun({
    projectRoot,
    skill,
    runId,
    identifier,
    identifierFlag,
    listActiveRuns,
    loadRun,
    loadActiveRun,
    output,
}) {
    if (!runId && !identifier) {
        const activeRuns = listActiveRuns(projectRoot, skill);
        if (activeRuns.length > 1) {
            outputGuardFailure(output, { error: `Multiple active ${skill} runs found. Pass --${identifierFlag} or --run-id.` });
        }
    }
    return runId
        ? loadRun(projectRoot, runId)
        : loadActiveRun(projectRoot, skill, identifier);
}

export function outputPlanningStatus(projectRoot, run, runtimePaths, computeResumeAction, output) {
    outputRuntimeStatus(output, projectRoot, run, runtimePaths, computeResumeAction);
}

export function advancePlanningRun(projectRoot, runId, run, toPhase, validateTransition, saveState, donePhase, output) {
    const guard = validateTransition(run.manifest, run.state, run.checkpoints, toPhase);
    if (!guard.ok) {
        outputGuardFailure(output, guard);
    }
    const nextState = saveState(projectRoot, runId, {
        ...run.state,
        phase: toPhase,
        complete: toPhase === donePhase ? true : run.state.complete,
        paused_reason: null,
    });
    if (nextState?.ok === false) {
        outputGuardFailure(output, nextState);
    }
    outputRuntimeState(output, run, nextState);
}

export function checkpointPlanningRun(projectRoot, runId, run, phase, payload, checkpointPhase, saveState, applyCheckpointToState, fail, output) {
    const checkpointed = checkpointPhase(projectRoot, runId, phase, payload);
    if (!checkpointed.ok) {
        fail(checkpointed.error);
    }
    const nextState = saveState(projectRoot, runId, applyCheckpointToState(run.state, phase, payload));
    if (nextState?.ok === false) {
        fail(nextState.error);
    }
    outputRuntimeState(output, run, nextState, {
        checkpoint: checkpointed.checkpoints[phase],
        history_length: checkpointed.checkpoints._history.length,
    });
}

export function pausePlanningRun(projectRoot, runId, payload, reason, pauseRun, setPendingDecision, fail, output) {
    const result = Object.keys(payload).length > 0
        ? setPendingDecision(projectRoot, runId, payload, reason || "Decision required")
        : pauseRun(projectRoot, runId, reason || "Paused");
    if (!result.ok) {
        fail(result.error);
    }
    output(result);
}

export function completePlanningRun(projectRoot, runId, run, validateTransition, completeRun, donePhase, fail, output) {
    const guard = validateTransition(run.manifest, run.state, run.checkpoints, donePhase);
    if (!guard.ok) {
        outputGuardFailure(output, guard);
    }
    const result = completeRun(projectRoot, runId);
    if (!result.ok) {
        fail(result.error);
    }
    output(result);
}

export {
    outputInactiveRuntime,
};
