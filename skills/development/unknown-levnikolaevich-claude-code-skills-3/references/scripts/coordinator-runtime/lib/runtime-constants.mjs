// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/runtime-constants.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

export const TERMINAL_RUNTIME_PHASES = Object.freeze({
    PAUSED: "PAUSED",
    DONE: "DONE",
});

export const RUNTIME_HISTORY_EVENT_TYPES = Object.freeze({
    RUN_STARTED: "RUN_STARTED",
    STATE_SAVED: "STATE_SAVED",
    RUN_PAUSED: "RUN_PAUSED",
    RUN_COMPLETED: "RUN_COMPLETED",
    CHECKPOINT_RECORDED: "CHECKPOINT_RECORDED",
    LOOP_HEALTH_RECORDED: "LOOP_HEALTH_RECORDED",
});

export const RUNTIME_HISTORY_EVENT_TYPE_LIST = Object.freeze(Object.values(RUNTIME_HISTORY_EVENT_TYPES));

export const WORKER_SUMMARY_STATUSES = Object.freeze({
    COMPLETED: "completed",
    SKIPPED: "skipped",
    ERROR: "error",
});

export const WORKER_SUMMARY_STATUS_LIST = Object.freeze(Object.values(WORKER_SUMMARY_STATUSES));

export const REVIEW_AGENT_STATUSES = Object.freeze({
    SKIPPED: "skipped",
    LAUNCHED: "launched",
    RESULT_READY: "result_ready",
    DEAD: "dead",
    FAILED: "failed",
});

export const REVIEW_AGENT_STATUS_LIST = Object.freeze(Object.values(REVIEW_AGENT_STATUSES));
export const REVIEW_RESOLVED_AGENT_STATUS_LIST = Object.freeze([
    REVIEW_AGENT_STATUSES.RESULT_READY,
    REVIEW_AGENT_STATUSES.DEAD,
    REVIEW_AGENT_STATUSES.FAILED,
    REVIEW_AGENT_STATUSES.SKIPPED,
]);
export const REVIEW_RESOLVED_AGENT_STATUS_SET = new Set(REVIEW_RESOLVED_AGENT_STATUS_LIST);

export const PLANNING_PROGRESS_STATUSES = Object.freeze({
    COMPLETED: "completed",
});

export const OPTIMIZATION_GATE_VERDICTS = Object.freeze({
    PROCEED: "PROCEED",
    CONCERNS: "CONCERNS",
    WAIVED: "WAIVED",
    BLOCK: "BLOCK",
});

export const OPTIMIZATION_GATE_VERDICT_LIST = Object.freeze(Object.values(OPTIMIZATION_GATE_VERDICTS));

export const OPTIMIZATION_VALIDATION_VERDICTS = Object.freeze({
    GO: "GO",
    GO_WITH_CONCERNS: "GO_WITH_CONCERNS",
    WAIVED: "WAIVED",
    NO_GO: "NO_GO",
});

export const OPTIMIZATION_EXECUTION_ALLOWED_VERDICT_LIST = Object.freeze([
    OPTIMIZATION_VALIDATION_VERDICTS.GO,
    OPTIMIZATION_VALIDATION_VERDICTS.GO_WITH_CONCERNS,
    OPTIMIZATION_VALIDATION_VERDICTS.WAIVED,
]);

export const OPTIMIZATION_CHECKPOINT_STATUSES = Object.freeze({
    COMPLETED: "completed",
    SKIPPED_BY_MODE: "skipped_by_mode",
});

export const OPTIMIZATION_CYCLE_STATUSES = Object.freeze({
    COMPLETED: "completed",
});

export const OPTIMIZATION_CYCLE_STATUS_LIST = Object.freeze(Object.values(OPTIMIZATION_CYCLE_STATUSES));

export const STORY_GATE_VERDICTS = Object.freeze({
    PASS: "PASS",
    CONCERNS: "CONCERNS",
    WAIVED: "WAIVED",
    FAIL: "FAIL",
});

export const STORY_GATE_VERDICT_LIST = Object.freeze(Object.values(STORY_GATE_VERDICTS));

export const STORY_GATE_FINALIZATION_STATUSES = Object.freeze({
    SKIPPED_BY_VERDICT: "skipped_by_verdict",
});

export const TASK_BOARD_STATUSES = Object.freeze({
    BACKLOG: "Backlog",
    TODO: "Todo",
    IN_PROGRESS: "In Progress",
    TO_REVIEW: "To Review",
    TO_REWORK: "To Rework",
    DONE: "Done",
    SKIPPED: "SKIPPED",
    VERIFIED: "VERIFIED",
});

export const STORY_GATE_COMPLETED_TEST_STATUS_LIST = Object.freeze([
    TASK_BOARD_STATUSES.DONE,
    TASK_BOARD_STATUSES.SKIPPED,
    TASK_BOARD_STATUSES.VERIFIED,
]);

export const STORY_GATE_PRE_VERIFICATION_ALLOWED_TEST_STATUS_LIST = Object.freeze([
    TASK_BOARD_STATUSES.DONE,
    TASK_BOARD_STATUSES.SKIPPED,
]);

export const STORY_EXECUTION_GROUP_STATUSES = Object.freeze({
    COMPLETED: "completed",
});

export const STORY_EXECUTION_GROUP_STATUS_LIST = Object.freeze(Object.values(STORY_EXECUTION_GROUP_STATUSES));

export const ENVIRONMENT_SETUP_FINAL_RESULTS = Object.freeze({
    READY: "READY",
    DRY_RUN_PLAN: "DRY_RUN_PLAN",
});

export const STORY_EXECUTION_FINAL_RESULTS = Object.freeze({
    READY_FOR_GATE: "READY_FOR_GATE",
});
