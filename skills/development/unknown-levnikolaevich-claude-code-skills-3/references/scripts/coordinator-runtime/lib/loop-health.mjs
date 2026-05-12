// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/loop-health.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

export const LOOP_HEALTH_FAILURE_CLASSES = Object.freeze({
    NONE: "none",
    TIMEOUT_IDLE: "timeout_idle",
    TIMEOUT_PRODUCTIVE: "timeout_productive",
    PERMISSION_DENIAL: "permission_denial",
    TOOL_MISSING: "tool_missing",
    AUTH_MISSING: "auth_missing",
    RATE_LIMITED: "rate_limited",
    ASKED_QUESTION: "asked_question",
    AGENT_ERROR: "agent_error",
    UNKNOWN: "unknown",
});

export const DEFAULT_LOOP_HEALTH_POLICY = Object.freeze({
    no_progress_limit: 3,
    same_error_limit: 3,
    immediate_pause_failure_classes: Object.freeze([
        LOOP_HEALTH_FAILURE_CLASSES.PERMISSION_DENIAL,
        LOOP_HEALTH_FAILURE_CLASSES.TOOL_MISSING,
        LOOP_HEALTH_FAILURE_CLASSES.AUTH_MISSING,
    ]),
    defer_failure_classes: Object.freeze([
        LOOP_HEALTH_FAILURE_CLASSES.RATE_LIMITED,
    ]),
});

const FAILURE_CLASS_SET = new Set(Object.values(LOOP_HEALTH_FAILURE_CLASSES));

function asText(value) {
    if (value == null) return "";
    if (typeof value === "string") return value;
    try {
        return JSON.stringify(value);
    } catch {
        return String(value);
    }
}

export function normalizeErrorSignature(text) {
    return asText(text)
        .toLowerCase()
        .replace(/\r\n/g, "\n")
        .replace(/[a-z]:[\\/][^\s)'"`]+/gi, "<path>")
        .replace(/\/(?:[^/\s)'"`]+\/)+[^/\s)'"`]+/g, "<path>")
        .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, "<uuid>")
        .replace(/\b\d{4}-\d{2}-\d{2}t\d{2}:\d{2}:\d{2}(?:\.\d+)?z\b/g, "<timestamp>")
        .replace(/\b\d+\b/g, "<num>")
        .replace(/\s+/g, " ")
        .trim()
        .slice(0, 240);
}

function hasProgressSignal(input = {}) {
    const signals = input.progress_signals || {};
    return Boolean(
        input.progress_detected
        || input.artifact_delta
        || input.checkpoint_delta
        || input.status_delta
        || input.files_changed_delta
        || input.scenario_improved
        || input.metric_improved
        || input.new_evidence
        || signals.output_written
        || signals.log_written
        || signals.session_captured
    );
}

function classifyFromText(text) {
    const normalized = normalizeErrorSignature(text);
    if (!normalized) return LOOP_HEALTH_FAILURE_CLASSES.NONE;
    if (/\b(rate limit|rate_limited|too many requests|quota|429)\b/.test(normalized)) {
        return LOOP_HEALTH_FAILURE_CLASSES.RATE_LIMITED;
    }
    if (/\b(permission denied|not allowed|access denied|operation not permitted|blocked by permissions)\b/.test(normalized)) {
        return LOOP_HEALTH_FAILURE_CLASSES.PERMISSION_DENIAL;
    }
    if (/\b(command not found|not found in path|enoent|tool missing|required tool)\b/.test(normalized)) {
        return LOOP_HEALTH_FAILURE_CLASSES.TOOL_MISSING;
    }
    if (/\b(auth|authentication|unauthorized|login required|api key|token missing|credentials)\b/.test(normalized)) {
        return LOOP_HEALTH_FAILURE_CLASSES.AUTH_MISSING;
    }
    if (/\?\s*$|should i|do you want|please confirm|need clarification/.test(normalized)) {
        return LOOP_HEALTH_FAILURE_CLASSES.ASKED_QUESTION;
    }
    return LOOP_HEALTH_FAILURE_CLASSES.UNKNOWN;
}

export function classifyLoopSignal(input = {}) {
    const combinedText = [
        input.error,
        input.stderr,
        input.stdout,
        input.response,
        input.message,
        input.evidence_key,
    ].map(asText).filter(Boolean).join("\n");

    let failureClass = input.failure_class || null;
    if (!FAILURE_CLASS_SET.has(failureClass)) {
        failureClass = classifyFromText(combinedText);
    }

    const progressDetected = hasProgressSignal(input);
    const errorSignature = normalizeErrorSignature(input.error_signature || combinedText || failureClass);

    return {
        failure_class: failureClass,
        progress_detected: progressDetected,
        error_signature: errorSignature || null,
        evidence_key: input.evidence_key || errorSignature || failureClass,
        reason: input.reason || null,
        progress_signals: {
            output_written: Boolean(input.progress_signals?.output_written),
            log_written: Boolean(input.progress_signals?.log_written),
            session_captured: Boolean(input.progress_signals?.session_captured),
        },
        recorded_at: new Date().toISOString(),
    };
}

export function shouldPause(loopHealth = {}) {
    return {
        pause: Boolean(loopHealth.pause_recommended),
        reason: loopHealth.pause_reason || null,
        category: loopHealth.pause_category || null,
    };
}

export function updateLoopHealth(previous = {}, signalInput = {}, policyInput = {}) {
    const policy = {
        ...DEFAULT_LOOP_HEALTH_POLICY,
        ...policyInput,
    };
    const signal = signalInput.failure_class && signalInput.error_signature !== undefined
        ? signalInput
        : classifyLoopSignal(signalInput);

    const immediateSet = new Set(policy.immediate_pause_failure_classes || []);
    const deferSet = new Set(policy.defer_failure_classes || []);
    const previousSignature = previous.last_error_signature || null;
    const sameError = Boolean(signal.error_signature && signal.error_signature === previousSignature);

    const noProgressCount = signal.progress_detected
        ? 0
        : Number(previous.no_progress_count || 0) + 1;
    const sameErrorCount = signal.progress_detected
        ? 0
        : (sameError ? Number(previous.same_error_count || 0) + 1 : 1);

    let pauseRecommended = false;
    let pauseCategory = null;
    let pauseReason = null;

    if (immediateSet.has(signal.failure_class)) {
        pauseRecommended = true;
        pauseCategory = signal.failure_class;
        pauseReason = `Immediate blocker: ${signal.failure_class}`;
    } else if (deferSet.has(signal.failure_class)) {
        pauseRecommended = true;
        pauseCategory = signal.failure_class;
        pauseReason = "Rate limited; defer retry without counting as domain failure";
    } else if (sameErrorCount >= policy.same_error_limit) {
        pauseRecommended = true;
        pauseCategory = "same_error";
        pauseReason = `Same error repeated ${sameErrorCount} times without progress`;
    } else if (noProgressCount >= policy.no_progress_limit) {
        pauseRecommended = true;
        pauseCategory = "no_progress";
        pauseReason = `No progress recorded for ${noProgressCount} attempts`;
    }

    return {
        attempts: Number(previous.attempts || 0) + 1,
        no_progress_count: noProgressCount,
        same_error_count: sameErrorCount,
        last_failure_class: signal.failure_class,
        last_error_signature: signal.error_signature,
        last_evidence_key: signal.evidence_key || null,
        last_progress_detected: signal.progress_detected,
        last_signal_at: signal.recorded_at || new Date().toISOString(),
        pause_recommended: pauseRecommended,
        pause_category: pauseCategory,
        pause_reason: pauseReason,
        history: [
            ...(previous.history || []).slice(-9),
            signal,
        ],
    };
}

export function updateLoopHealthMap(previousMap = {}, scopeKey, signalInput = {}, policyInput = {}) {
    const key = String(scopeKey || "default");
    const nextEntry = updateLoopHealth(previousMap[key] || {}, signalInput, policyInput);
    return {
        map: {
            ...previousMap,
            [key]: nextEntry,
        },
        entry: nextEntry,
        pause: shouldPause(nextEntry),
    };
}
