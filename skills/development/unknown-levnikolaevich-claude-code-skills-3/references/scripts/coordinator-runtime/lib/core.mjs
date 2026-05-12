// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/core.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { randomUUID } from "node:crypto";
import {
    appendFileSync,
    existsSync,
    mkdirSync,
    readdirSync,
    readFileSync,
    renameSync,
    unlinkSync,
    writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import {
    activePointerSchema,
    buildRuntimeStateSchema,
    runtimeCheckpointEntrySchema,
    runtimeCheckpointHistorySchema,
    runtimeHistoryEventSchema,
} from "./schemas.mjs";
import { assertSchema } from "./validate.mjs";
import { updateLoopHealthMap } from "./loop-health.mjs";

const LOCK_FILE = ".lock";
const HISTORY_FILE = "history.jsonl";

function resolveParts(projectRoot, parts) {
    return join(resolve(projectRoot || process.cwd()), ...(parts || []));
}

function safeReadJson(filePath) {
    try {
        return JSON.parse(readFileSync(filePath, "utf8"));
    } catch {
        return null;
    }
}

function safeIdentifier(value) {
    return String(value || "default")
        .trim()
        .replace(/[^a-zA-Z0-9_-]+/g, "-")
        .replace(/^-+|-+$/g, "")
        .toLowerCase() || "default";
}

function atomicWrite(filePath, data) {
    mkdirSync(dirname(filePath), { recursive: true });
    const tmpPath = `${filePath}.tmp-${process.pid}`;
    try {
        writeFileSync(tmpPath, JSON.stringify(data, null, 2) + "\n", "utf8");
        renameSync(tmpPath, filePath);
    } catch (error) {
        try {
            unlinkSync(tmpPath);
        } catch {
            // Best-effort cleanup only.
        }
        throw error;
    }
}

function defaultRunId(skill, identifier) {
    const safeSkill = safeIdentifier(skill || "runtime");
    const safeRunIdentifier = safeIdentifier(identifier || "run");
    return `${safeSkill}-${safeRunIdentifier}-${Date.now()}-${randomUUID().slice(0, 8)}`;
}

function normalizeCheckpoints(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
        return { _history: [], _next_sequence: 1 };
    }
    if (Array.isArray(raw._history)) {
        return {
            ...raw,
            _history: raw._history,
            _next_sequence: Number(raw._next_sequence || (raw._history.length + 1)),
        };
    }
    const history = Object.entries(raw)
        .filter(([key, value]) => !key.startsWith("_") && value && typeof value === "object")
        .map(([phase, entry], index) => ({
            sequence: Number(entry.sequence || (index + 1)),
            phase,
            created_at: entry.created_at || new Date().toISOString(),
            payload: entry.payload || {},
        }));
    return {
        ...raw,
        _history: history,
        _next_sequence: history.length + 1,
    };
}

function appendCheckpoint(checkpoints, phase, payload) {
    const next = normalizeCheckpoints(checkpoints);
    const entry = {
        sequence: next._next_sequence,
        phase,
        created_at: new Date().toISOString(),
        payload: payload || {},
    };
    const entryValidation = assertSchema(runtimeCheckpointEntrySchema, entry, "checkpoint entry");
    if (!entryValidation.ok) {
        throw new Error(entryValidation.error);
    }
    const nextCheckpoints = {
        ...next,
        [phase]: entry,
        _history: [...next._history, entry],
        _next_sequence: entry.sequence + 1,
    };
    const checkpointsValidation = assertSchema(runtimeCheckpointHistorySchema, nextCheckpoints, "checkpoint history");
    if (!checkpointsValidation.ok) {
        throw new Error(checkpointsValidation.error);
    }
    return nextCheckpoints;
}

function acquireLock(dir) {
    const lockPath = join(dir, LOCK_FILE);
    mkdirSync(dir, { recursive: true });
    if (existsSync(lockPath)) {
        const existing = safeReadJson(lockPath);
        if (existing?.pid) {
            try {
                process.kill(existing.pid, 0);
                return { ok: false, error: `Runtime already running (PID ${existing.pid})` };
            } catch {
                // Stale lock.
            }
        }
    }
    atomicWrite(lockPath, { pid: process.pid, started_at: new Date().toISOString() });
    return { ok: true };
}

function releaseLock(dir) {
    try {
        unlinkSync(join(dir, LOCK_FILE));
    } catch {
        // Best-effort cleanup only.
    }
}

function withLock(dir, action) {
    const lock = acquireLock(dir);
    if (!lock.ok) {
        return lock;
    }
    try {
        return action();
    } finally {
        releaseLock(dir);
    }
}

function readHistory(filePath) {
    if (!existsSync(filePath)) {
        return [];
    }
    const content = readFileSync(filePath, "utf8");
    return content
        .split(/\r?\n/u)
        .map(line => line.trim())
        .filter(Boolean)
        .map(line => {
            try {
                return JSON.parse(line);
            } catch {
                return null;
            }
        })
        .filter(Boolean);
}

function appendHistoryEvent(filePath, eventType, payload) {
    mkdirSync(dirname(filePath), { recursive: true });
    const events = readHistory(filePath);
    const nextEvent = {
        sequence: events.length + 1,
        event_type: eventType,
        created_at: new Date().toISOString(),
        ...payload,
    };
    const validation = assertSchema(runtimeHistoryEventSchema, nextEvent, "runtime history event");
    if (!validation.ok) {
        throw new Error(validation.error);
    }
    appendFileSync(filePath, `${JSON.stringify(nextEvent)}\n`, "utf8");
    return nextEvent;
}

function rebuildFromHistory(events, fallback) {
    let manifest = fallback?.manifest || null;
    let state = fallback?.state || null;
    let checkpoints = normalizeCheckpoints(fallback?.checkpoints || {});

    for (const event of events) {
        switch (event.event_type) {
            case "RUN_STARTED":
                manifest = event.manifest || manifest;
                state = event.state || state;
                checkpoints = normalizeCheckpoints(event.checkpoints || checkpoints);
                break;
            case "STATE_SAVED":
            case "RUN_PAUSED":
            case "RUN_COMPLETED":
            case "LOOP_HEALTH_RECORDED":
                state = event.state || state;
                break;
            case "CHECKPOINT_RECORDED":
                checkpoints = appendCheckpoint(checkpoints, event.phase, event.payload || {});
                break;
            default:
                break;
        }
    }

    if (!manifest || !state) {
        return null;
    }

    return { manifest, state, checkpoints, history: events };
}

export function readJsonFile(filePath) {
    return safeReadJson(filePath);
}

export function resolveTrackedPath(projectRoot, filePath) {
    if (!filePath) {
        return null;
    }
    return resolve(projectRoot || process.cwd(), filePath);
}

export function fileExists(filePath) {
    return existsSync(filePath);
}

export function createRuntimeStore(config) {
    const baseRootParts = config.baseRootParts;
    const activeRootParts = config.activeRootParts || baseRootParts;
    const stateSchema = config.stateSchema || buildRuntimeStateSchema();
    const runsSubdir = Object.prototype.hasOwnProperty.call(config, "runsSubdir")
        ? config.runsSubdir
        : "runs";

    function baseRoot(projectRoot) {
        return resolveParts(projectRoot, baseRootParts);
    }

    function activeRoot(projectRoot) {
        return resolveParts(projectRoot, activeRootParts);
    }

    function runsDir(projectRoot) {
        return runsSubdir ? join(baseRoot(projectRoot), runsSubdir) : baseRoot(projectRoot);
    }

    function runDir(projectRoot, runId) {
        return join(runsDir(projectRoot), runId);
    }

    function manifestPath(projectRoot, runId) {
        return join(runDir(projectRoot, runId), "manifest.json");
    }

    function statePath(projectRoot, runId) {
        return join(runDir(projectRoot, runId), "state.json");
    }

    function checkpointsPath(projectRoot, runId) {
        return join(runDir(projectRoot, runId), "checkpoints.json");
    }

    function historyPath(projectRoot, runId) {
        return join(runDir(projectRoot, runId), HISTORY_FILE);
    }

    function activeDir(projectRoot, skill) {
        return join(activeRoot(projectRoot), "active", safeIdentifier(skill));
    }

    function activePath(projectRoot, skill, identifier) {
        return join(activeDir(projectRoot, skill), `${safeIdentifier(identifier)}.json`);
    }

    function listActiveRuns(projectRoot, skill) {
        const dir = activeDir(projectRoot, skill);
        if (!existsSync(dir)) {
            return [];
        }
        return readdirSync(dir)
            .filter(name => name.endsWith(".json"))
            .map(name => safeReadJson(join(dir, name)))
            .filter(pointer => pointer?.run_id);
    }

    function loadRun(projectRoot, runId) {
        const manifest = safeReadJson(manifestPath(projectRoot, runId));
        const state = safeReadJson(statePath(projectRoot, runId));
        const checkpoints = normalizeCheckpoints(safeReadJson(checkpointsPath(projectRoot, runId)));
        const history = readHistory(historyPath(projectRoot, runId));
        if (history.length > 0) {
            return rebuildFromHistory(history, { manifest, state, checkpoints });
        }
        if (!manifest || !state) {
            return null;
        }
        return { manifest, state, checkpoints, history: [] };
    }

    function loadActiveRun(projectRoot, skill, identifier) {
        const pointer = identifier
            ? safeReadJson(activePath(projectRoot, skill, identifier))
            : (() => {
                const activeRuns = listActiveRuns(projectRoot, skill);
                return activeRuns.length === 1 ? activeRuns[0] : null;
            })();
        if (!pointer?.run_id) {
            return null;
        }
        return loadRun(projectRoot, pointer.run_id);
    }

    function saveActive(projectRoot, skill, identifier, runId) {
        const pointer = {
            skill,
            identifier,
            run_id: runId,
            updated_at: new Date().toISOString(),
        };
        const validation = assertSchema(activePointerSchema, pointer, "active runtime pointer");
        if (!validation.ok) {
            throw new Error(validation.error);
        }
        atomicWrite(activePath(projectRoot, skill, identifier), pointer);
    }

    function clearActive(projectRoot, skill, identifier, runId) {
        const filePath = activePath(projectRoot, skill, identifier);
        const pointer = safeReadJson(filePath);
        if (pointer?.run_id && pointer.run_id !== runId) {
            return;
        }
        try {
            unlinkSync(filePath);
        } catch {
            // Best-effort cleanup only.
        }
    }

    function startRun(projectRoot, manifestInput) {
        const manifest = config.normalizeManifest(manifestInput, projectRoot);
        if (!manifest.skill || !manifest.identifier) {
            return { ok: false, error: "Manifest normalization must set skill and identifier" };
        }
        if (config.manifestSchema) {
            const validation = assertSchema(config.manifestSchema, manifest, `${manifest.skill} manifest`);
            if (!validation.ok) {
                return validation;
            }
        }

        const activeRun = loadActiveRun(projectRoot, manifest.skill, manifest.identifier);
        if (activeRun && !activeRun.state.complete) {
            return { ok: false, recovery: true, run: activeRun };
        }

        const runId = (config.buildRunId || defaultRunId)(manifest.skill, manifest.identifier, manifestInput);
        const state = config.defaultState(manifest, runId);
        const stateValidation = assertSchema(stateSchema, state, `${manifest.skill} state`);
        if (!stateValidation.ok) {
            return stateValidation;
        }
        const checkpoints = normalizeCheckpoints({});
        const checkpointsValidation = assertSchema(runtimeCheckpointHistorySchema, checkpoints, `${manifest.skill} checkpoints`);
        if (!checkpointsValidation.ok) {
            return checkpointsValidation;
        }
        const result = withLock(baseRoot(projectRoot), () => {
            atomicWrite(manifestPath(projectRoot, runId), manifest);
            atomicWrite(statePath(projectRoot, runId), state);
            atomicWrite(checkpointsPath(projectRoot, runId), checkpoints);
            appendHistoryEvent(historyPath(projectRoot, runId), "RUN_STARTED", {
                run_id: runId,
                manifest,
                state,
                checkpoints,
            });
            saveActive(projectRoot, manifest.skill, manifest.identifier, runId);
            return { ok: true, run_id: runId, manifest, state, checkpoints };
        });
        return result;
    }

    function saveState(projectRoot, runId, state, eventType = "STATE_SAVED") {
        const nextState = {
            ...state,
            updated_at: new Date().toISOString(),
        };
        const validation = assertSchema(stateSchema, nextState, "runtime state");
        if (!validation.ok) {
            return validation;
        }
        const result = withLock(baseRoot(projectRoot), () => {
            const run = loadRun(projectRoot, runId);
            if (!run) {
                return { ok: false, error: "Run not found" };
            }
            atomicWrite(statePath(projectRoot, runId), nextState);
            appendHistoryEvent(historyPath(projectRoot, runId), eventType, {
                run_id: runId,
                state: nextState,
            });
            if (!nextState.complete) {
                saveActive(projectRoot, nextState.skill, nextState.identifier, runId);
            }
            return { ok: true, state: nextState };
        });
        return result.ok === false ? result : result.state;
    }

    function checkpointPhase(projectRoot, runId, phase, payload) {
        const run = loadRun(projectRoot, runId);
        if (!run) {
            return { ok: false, error: "Run not found" };
        }
        const nextCheckpoints = appendCheckpoint(run.checkpoints, phase, payload);
        return withLock(baseRoot(projectRoot), () => {
            atomicWrite(checkpointsPath(projectRoot, runId), nextCheckpoints);
            appendHistoryEvent(historyPath(projectRoot, runId), "CHECKPOINT_RECORDED", {
                run_id: runId,
                phase,
                payload: payload || {},
            });
            return { ok: true, checkpoints: nextCheckpoints };
        });
    }

    function updateState(projectRoot, runId, updater, options = {}) {
        const run = loadRun(projectRoot, runId);
        if (!run) {
            return { ok: false, error: "Run not found" };
        }
        const nextState = typeof updater === "function" ? updater(run.state, run) : updater;
        const saved = saveState(projectRoot, runId, nextState, options.eventType || "STATE_SAVED");
        if (saved?.ok === false) {
            return saved;
        }
        return { ok: true, state: saved };
    }

    function pauseRun(projectRoot, runId, reason) {
        return updateState(projectRoot, runId, state => ({
            ...state,
            phase: "PAUSED",
            paused_reason: reason || "Paused",
            pending_decision: null,
        }), { eventType: "RUN_PAUSED" });
    }

    function recordLoopHealth(projectRoot, runId, scopeKey, signal, options = {}) {
        let recordedEntry = null;
        let pauseRecommendation = null;
        const result = updateState(projectRoot, runId, state => {
            const updated = updateLoopHealthMap(state.loop_health || {}, scopeKey, signal, options.policy || {});
            recordedEntry = updated.entry;
            pauseRecommendation = updated.pause;
            const pauseState = options.pauseOnRecommendation !== false && updated.pause.pause
                ? {
                    phase: "PAUSED",
                    paused_reason: updated.pause.reason || "Loop health pause",
                    pending_decision: null,
                }
                : {};
            return {
                ...state,
                ...pauseState,
                loop_health: updated.map,
            };
        }, { eventType: "LOOP_HEALTH_RECORDED" });
        if (!result.ok) {
            return result;
        }
        return {
            ok: true,
            state: result.state,
            loop_health: recordedEntry,
            pause: pauseRecommendation,
        };
    }

    function completeRun(projectRoot, runId) {
        const run = loadRun(projectRoot, runId);
        if (!run) {
            return { ok: false, error: "Run not found" };
        }
        const result = updateState(projectRoot, runId, state => ({
            ...state,
            phase: "DONE",
            complete: true,
            paused_reason: null,
            pending_decision: null,
        }), { eventType: "RUN_COMPLETED" });
        if (!result.ok) {
            return result;
        }
        clearActive(projectRoot, run.state.skill, run.state.identifier, runId);
        return result;
    }

    function resolveRunId(projectRoot, skill, runId, identifier) {
        if (runId) {
            return runId;
        }
        if (identifier) {
            const pointer = safeReadJson(activePath(projectRoot, skill, identifier));
            return pointer?.run_id || null;
        }
        const activeRuns = listActiveRuns(projectRoot, skill);
        if (activeRuns.length !== 1) {
            return null;
        }
        return activeRuns[0].run_id;
    }

    function runtimePaths(projectRoot, runId, skill, identifier) {
        const resolvedRunId = resolveRunId(projectRoot, skill, runId, identifier);
        if (!resolvedRunId) {
            return null;
        }
        return {
            root: baseRoot(projectRoot),
            run_dir: runDir(projectRoot, resolvedRunId),
            manifest: manifestPath(projectRoot, resolvedRunId),
            state: statePath(projectRoot, resolvedRunId),
            checkpoints: checkpointsPath(projectRoot, resolvedRunId),
            history: historyPath(projectRoot, resolvedRunId),
            active: identifier ? activePath(projectRoot, skill, identifier) : activeDir(projectRoot, skill),
        };
    }

    return {
        baseRoot,
        runtimePaths,
        loadRun,
        loadActiveRun,
        listActiveRuns,
        startRun,
        saveState,
        checkpointPhase,
        updateState,
        recordLoopHealth,
        pauseRun,
        completeRun,
        clearActiveRun(projectRoot, skill, identifier, runId) {
            clearActive(projectRoot, skill, identifier, runId);
        },
        resolveRunId,
        readHistory(projectRoot, runId) {
            return readHistory(historyPath(projectRoot, runId));
        },
    };
}
