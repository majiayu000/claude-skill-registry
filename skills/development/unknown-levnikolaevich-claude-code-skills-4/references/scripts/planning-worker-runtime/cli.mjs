#!/usr/bin/env node
// SOURCE-OF-TRUTH: shared/scripts/planning-worker-runtime/cli.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { parseArgs } from "node:util";
import {
    checkpointPhase,
    completeRun,
    listActiveRuns,
    loadActiveRun,
    loadRun,
    pauseRun,
    readJsonFile,
    recordSummary,
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

const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
        "project-root": { type: "string", default: process.cwd() },
        skill: { type: "string" },
        "run-id": { type: "string" },
        identifier: { type: "string" },
        epic: { type: "string" },
        "summary-artifact-path": { type: "string" },
        phase: { type: "string" },
        to: { type: "string" },
        payload: { type: "string" },
        "payload-file": { type: "string" },
        "manifest-file": { type: "string" },
        reason: { type: "string" },
        resolve: { type: "boolean", default: false },
    },
});

function requireSkill() {
    if (!values.skill) {
        fail("Command requires --skill");
    }
    return values.skill;
}

function resolveIdentifier() {
    if (values.identifier) {
        return values.identifier;
    }
    if (values.epic) {
        return `epic-${values.epic}`;
    }
    return null;
}

function resolveRun(projectRoot) {
    const skill = requireSkill();
    const identifier = resolveIdentifier();
    const runId = resolveRunId(projectRoot, skill, values["run-id"], identifier);
    if (!runId) {
        const activeRuns = listActiveRuns(projectRoot, skill);
        if (activeRuns.length > 1 && !identifier) {
            fail(`Multiple active ${skill} runs found. Pass --identifier or --run-id.`);
        }
        fail(`No active ${skill} run found. Pass --identifier or --run-id.`);
    }
    const run = loadRun(projectRoot, runId);
    if (!run) {
        fail(`Run not found: ${runId}`);
    }
    return { runId, run };
}

function applyCheckpointToState(state, phase, payload) {
    const nextState = { ...state };
    if (phase.endsWith("SELF_CHECK")) {
        nextState.self_check_passed = payload.pass === true;
        nextState.final_result = payload.final_result || nextState.final_result;
    }
    return nextState;
}

async function main() {
    const command = positionals[0];
    const projectRoot = values["project-root"];

    if (command === "start") {
        requireSkill();
        const identifier = resolveIdentifier();
        if (!identifier || !values["manifest-file"]) {
            fail("start requires --skill, --identifier or --epic, and --manifest-file");
        }
        if (Boolean(values["run-id"]) !== Boolean(values["summary-artifact-path"])) {
            fail("start requires both --run-id and --summary-artifact-path when either is provided");
        }
        const manifest = readManifestOrFail(values, readJsonFile);
        const result = startRun(projectRoot, {
            ...manifest,
            skill: values.skill,
            identifier,
            work_item_id: identifier,
            ...((manifest.epic_id || values.epic) ? { epic_id: manifest.epic_id || values.epic } : {}),
            run_id: values["run-id"],
            summary_artifact_path: values["summary-artifact-path"] || null,
        });
        output(result);
        process.exit(result.ok ? 0 : 1);
    }

    if (command === "status") {
        const skill = requireSkill();
        const identifier = resolveIdentifier();
        if (!values["run-id"] && !identifier) {
            const activeRuns = listActiveRuns(projectRoot, skill);
            if (activeRuns.length > 1) {
                output({ ok: false, error: `Multiple active ${skill} runs found. Pass --identifier or --run-id.` });
                process.exit(1);
            }
        }
        const run = values["run-id"]
            ? loadRun(projectRoot, values["run-id"])
            : loadActiveRun(projectRoot, skill, identifier);
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
        if (run.state.phase === "PAUSED" && values.resolve) {
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
            complete: values.to === "DONE" ? true : run.state.complete,
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

    if (command === "record-summary") {
        const payload = readPayload(values, readJsonFile);
        const { runId } = resolveRun(projectRoot);
        const result = recordSummary(projectRoot, runId, payload);
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
        const guard = validateTransition(run.manifest, run.state, run.checkpoints, "DONE");
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

    fail("Unknown command. Use: start, status, advance, checkpoint, record-summary, pause, complete");
}

main().catch(error => fail(error.message));
