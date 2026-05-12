// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/schemas.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import {
    OPTIMIZATION_CYCLE_STATUS_LIST,
    REVIEW_AGENT_STATUS_LIST,
    RUNTIME_HISTORY_EVENT_TYPE_LIST,
    STORY_GATE_VERDICT_LIST,
    STORY_EXECUTION_GROUP_STATUS_LIST,
    WORKER_SUMMARY_STATUS_LIST,
} from "./runtime-constants.mjs";

function stringArraySchema() {
    return {
        type: "array",
        items: { type: "string" },
    };
}

function nullableStringSchema() {
    return { type: ["string", "null"] };
}

function nonNegativeIntegerSchema() {
    return { type: "integer", minimum: 0 };
}

function dateTimeSchema() {
    return { type: "string", format: "date-time" };
}

function baseDecisionRecordSchema() {
    return {
        type: "object",
        required: ["kind", "selected_choice", "answered_at"],
        additionalProperties: false,
        properties: {
            kind: { type: "string", minLength: 1 },
            selected_choice: { type: "string", minLength: 1 },
            answered_at: dateTimeSchema(),
            context: { type: "object" },
        },
    };
}

export function buildRuntimeStateSchema(extraProperties = {}, extraRequired = []) {
    return {
        type: "object",
        required: [
            "run_id",
            "skill",
            "identifier",
            "phase",
            "complete",
            "paused_reason",
            "pending_decision",
            "decisions",
            "final_result",
            "created_at",
            "updated_at",
            ...extraRequired,
        ],
        properties: {
            run_id: { type: "string", minLength: 1 },
            skill: { type: "string", minLength: 1 },
            mode: { type: ["string", "null"] },
            identifier: { type: "string", minLength: 1 },
            phase: { type: "string", minLength: 1 },
            complete: { type: "boolean" },
            paused_reason: nullableStringSchema(),
            pending_decision: { type: ["object", "null"] },
            decisions: {
                type: "array",
                items: baseDecisionRecordSchema(),
            },
            final_result: { type: ["string", "null"] },
            created_at: dateTimeSchema(),
            updated_at: dateTimeSchema(),
            ...extraProperties,
        },
    };
}

export const activePointerSchema = {
    type: "object",
    required: ["skill", "identifier", "run_id", "updated_at"],
    additionalProperties: false,
    properties: {
        skill: { type: "string", minLength: 1 },
        identifier: { type: "string", minLength: 1 },
        run_id: { type: "string", minLength: 1 },
        updated_at: dateTimeSchema(),
    },
};

export const runtimeCheckpointEntrySchema = {
    type: "object",
    required: ["sequence", "phase", "created_at", "payload"],
    additionalProperties: false,
    properties: {
        sequence: { type: "integer", minimum: 1 },
        phase: { type: "string", minLength: 1 },
        created_at: dateTimeSchema(),
        payload: { type: "object" },
    },
};

export const runtimeCheckpointHistorySchema = {
    type: "object",
    required: ["_history", "_next_sequence"],
    properties: {
        _history: {
            type: "array",
            items: runtimeCheckpointEntrySchema,
        },
        _next_sequence: { type: "integer", minimum: 1 },
    },
};

export const runtimeHistoryEventSchema = {
    type: "object",
    required: ["sequence", "event_type", "created_at"],
    properties: {
        sequence: { type: "integer", minimum: 1 },
        event_type: {
            type: "string",
            enum: RUNTIME_HISTORY_EVENT_TYPE_LIST,
        },
        created_at: dateTimeSchema(),
        run_id: { type: "string" },
    },
};

export const runtimeStatusResponseSchema = {
    type: "object",
    required: ["ok", "active", "runtime"],
    properties: {
        ok: { type: "boolean" },
        active: { type: "boolean" },
        runtime: {
            type: ["object", "null"],
            properties: {
                skill: { type: "string" },
                identifier: { type: "string" },
                run_id: { type: "string" },
                phase: { type: "string" },
                complete: { type: "boolean" },
            },
        },
        manifest: { type: "object" },
        state: { type: "object" },
        checkpoints: { type: "object" },
        paths: { type: "object" },
        resume_action: { type: ["string", "null"] },
        error: { type: "string" },
        validation_errors: { type: "array" },
    },
};

export function buildSummaryEnvelopeSchema(payloadSchema) {
    return {
        type: "object",
        required: ["schema_version", "summary_kind", "run_id", "identifier", "producer_skill", "produced_at", "payload"],
        additionalProperties: false,
        properties: {
            schema_version: { type: "string", minLength: 1 },
            summary_kind: { type: "string", minLength: 1 },
            run_id: { type: "string", minLength: 1 },
            identifier: { type: "string", minLength: 1 },
            producer_skill: { type: "string", minLength: 1 },
            produced_at: dateTimeSchema(),
            payload: payloadSchema || { type: "object" },
        },
    };
}

export const pendingDecisionSchema = {
    type: "object",
    required: ["kind", "question", "choices", "default_choice", "resume_to_phase", "blocking"],
    additionalProperties: false,
    properties: {
        kind: { type: "string", minLength: 1 },
        question: { type: "string", minLength: 1 },
        choices: {
            ...stringArraySchema(),
            minItems: 1,
        },
        default_choice: { type: "string", minLength: 1 },
        context: { type: "object" },
        resume_to_phase: { type: "string", minLength: 1 },
        blocking: { type: "boolean" },
    },
};

export const environmentWorkerPayloadSchema = {
    type: "object",
    required: ["status"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        targets: stringArraySchema(),
        changes: stringArraySchema(),
        warnings: stringArraySchema(),
        detail: { type: "string" },
    },
};

export const opportunityDiscoveryWorkerPayloadSchema = {
    type: "object",
    required: ["input_mode", "ideas_analyzed", "survivors_count", "killed_count", "warnings"],
    additionalProperties: false,
    properties: {
        input_mode: { type: "string", minLength: 1 },
        ideas_analyzed: { type: "integer" },
        generated_ideas: { type: "integer" },
        survivors_count: { type: "integer" },
        killed_count: { type: "integer" },
        top_recommendation: nullableStringSchema(),
        report_path: nullableStringSchema(),
        warnings: stringArraySchema(),
        artifact_path: nullableStringSchema(),
    },
};

export const storyPlanWorkerPayloadSchema = {
    type: "object",
    required: ["mode", "epic_id", "stories_created", "stories_updated", "stories_canceled", "story_urls", "warnings", "kanban_updated"],
    additionalProperties: false,
    properties: {
        mode: { type: "string" },
        epic_id: { type: "string" },
        stories_planned: { type: "integer" },
        stories_created: { type: "integer" },
        stories_updated: { type: "integer" },
        stories_canceled: { type: "integer" },
        story_urls: stringArraySchema(),
        warnings: stringArraySchema(),
        kanban_updated: { type: "boolean" },
        research_path_used: { type: "string" },
    },
};

export const storyPlanCoordinatorPayloadSchema = {
    type: "object",
    required: ["mode", "epic_id", "stories_created", "stories_updated", "stories_canceled", "story_urls", "warnings", "kanban_updated"],
    additionalProperties: false,
    properties: {
        mode: { type: "string" },
        epic_id: { type: "string" },
        stories_planned: { type: "integer" },
        stories_created: { type: "integer" },
        stories_updated: { type: "integer" },
        stories_canceled: { type: "integer" },
        story_urls: stringArraySchema(),
        warnings: stringArraySchema(),
        kanban_updated: { type: "boolean" },
        research_path_used: { type: "string" },
        worker_runs_completed: { type: "integer" },
        artifact_path: nullableStringSchema(),
    },
};

export const taskPlanWorkerPayloadSchema = {
    type: "object",
    required: ["mode", "story_id", "task_type", "tasks_created", "tasks_updated", "tasks_canceled", "task_urls", "warnings", "kanban_updated"],
    additionalProperties: false,
    properties: {
        mode: { type: "string" },
        story_id: { type: "string" },
        task_type: { type: "string" },
        tasks_created: { type: "integer" },
        tasks_updated: { type: "integer" },
        tasks_canceled: { type: "integer" },
        task_urls: stringArraySchema(),
        dry_warnings_count: { type: "integer" },
        warnings: stringArraySchema(),
        kanban_updated: { type: "boolean" },
    },
};

export const qualityWorkerPayloadSchema = {
    type: "object",
    required: ["worker", "status", "verdict", "issues", "warnings"],
    additionalProperties: false,
    properties: {
        worker: { type: "string", minLength: 1 },
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        verdict: { type: "string", minLength: 1 },
        score: { type: "number" },
        issues: stringArraySchema(),
        warnings: stringArraySchema(),
        artifact_path: nullableStringSchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const taskStatusWorkerPayloadSchema = {
    type: "object",
    required: ["worker", "status", "from_status", "to_status", "warnings"],
    additionalProperties: false,
    properties: {
        worker: { type: "string", minLength: 1 },
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        from_status: { type: "string", minLength: 1 },
        to_status: { type: "string", minLength: 1 },
        result: nullableStringSchema(),
        tests_run: stringArraySchema(),
        files_changed: stringArraySchema(),
        issues: stringArraySchema(),
        score: { type: ["number", "null"] },
        comment_path: nullableStringSchema(),
        error: nullableStringSchema(),
        warnings: stringArraySchema(),
        artifact_path: nullableStringSchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const testPlanningWorkerPayloadSchema = {
    type: "object",
    required: ["worker", "status", "warnings"],
    additionalProperties: false,
    properties: {
        worker: { type: "string", minLength: 1 },
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        warnings: stringArraySchema(),
        research_comment_path: nullableStringSchema(),
        manual_result_path: nullableStringSchema(),
        test_task_id: nullableStringSchema(),
        test_task_url: nullableStringSchema(),
        coverage_summary: nullableStringSchema(),
        planned_scenarios: stringArraySchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const storyPrioritizationWorkerPayloadSchema = {
    type: "object",
    required: ["epic_id", "stories_analyzed", "priority_distribution", "prioritization_path", "warnings"],
    additionalProperties: false,
    properties: {
        epic_id: { type: "string", minLength: 1 },
        depth: { type: "string" },
        stories_analyzed: { type: "integer" },
        priority_distribution: {
            type: "object",
            required: ["p0", "p1", "p2", "p3"],
            additionalProperties: false,
            properties: {
                p0: nonNegativeIntegerSchema(),
                p1: nonNegativeIntegerSchema(),
                p2: nonNegativeIntegerSchema(),
                p3: nonNegativeIntegerSchema(),
            },
        },
        top_story_ids: stringArraySchema(),
        prioritization_path: { type: "string", minLength: 1 },
        warnings: stringArraySchema(),
        artifact_path: nullableStringSchema(),
    },
};

export const docsGenerationWorkerPayloadSchema = {
    type: "object",
    required: ["worker", "status", "created_files", "skipped_files", "quality_inputs", "validation_status", "warnings"],
    additionalProperties: false,
    properties: {
        worker: { type: "string", minLength: 1 },
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        created_files: stringArraySchema(),
        skipped_files: stringArraySchema(),
        quality_inputs: {
            type: "object",
            additionalProperties: true,
        },
        validation_status: { type: "string", minLength: 1 },
        warnings: stringArraySchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const epicPlanCoordinatorPayloadSchema = {
    type: "object",
    required: ["mode", "scope_identifier", "epics_created", "epics_updated", "epics_canceled", "epic_urls", "warnings", "kanban_updated"],
    additionalProperties: false,
    properties: {
        mode: { type: "string" },
        scope_identifier: { type: "string", minLength: 1 },
        epics_created: { type: "integer" },
        epics_updated: { type: "integer" },
        epics_canceled: { type: "integer" },
        epic_urls: stringArraySchema(),
        warnings: stringArraySchema(),
        kanban_updated: { type: "boolean" },
        infrastructure_epic_included: { type: "boolean" },
        artifact_path: nullableStringSchema(),
    },
};

export const scopeDecompositionPayloadSchema = {
    type: "object",
    required: ["scope_identifier", "epic_runs_completed", "story_runs_completed", "warnings"],
    additionalProperties: false,
    properties: {
        scope_identifier: { type: "string", minLength: 1 },
        epic_runs_completed: { type: "integer" },
        story_runs_completed: { type: "integer" },
        prioritization_runs_completed: { type: "integer" },
        warnings: stringArraySchema(),
        final_result: { type: "string" },
        artifact_path: nullableStringSchema(),
    },
};

export const pipelineStageCoordinatorPayloadSchema = {
    type: "object",
    required: ["stage", "story_id", "status", "final_result", "story_status", "warnings"],
    additionalProperties: false,
    properties: {
        stage: { type: "integer", minimum: 0, maximum: 3 },
        story_id: { type: "string", minLength: 1 },
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        final_result: { type: "string", minLength: 1 },
        story_status: { type: "string", minLength: 1 },
        verdict: nullableStringSchema(),
        readiness_score: { type: ["number", "null"] },
        quality_score: { type: ["number", "null"] },
        warnings: stringArraySchema(),
        artifact_path: nullableStringSchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const auditSeverityCountsSchema = {
    type: "object",
    required: ["critical", "high", "medium", "low"],
    additionalProperties: false,
    properties: {
        critical: nonNegativeIntegerSchema(),
        high: nonNegativeIntegerSchema(),
        medium: nonNegativeIntegerSchema(),
        low: nonNegativeIntegerSchema(),
    },
};

export const auditWorkerPayloadSchema = {
    type: "object",
    required: ["status", "category", "report_path", "score", "issues_total", "severity_counts", "warnings"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        category: { type: "string", minLength: 1 },
        report_path: { type: "string", minLength: 1 },
        score: { type: "number" },
        issues_total: nonNegativeIntegerSchema(),
        severity_counts: auditSeverityCountsSchema,
        warnings: stringArraySchema(),
        diagnostic_scores: {
            type: "object",
            additionalProperties: { type: "number" },
        },
        domain_name: nullableStringSchema(),
        scan_scope: nullableStringSchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const auditCoordinatorPayloadSchema = {
    type: "object",
    required: ["status", "final_result", "report_path", "worker_count", "issues_total", "severity_counts", "warnings"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        final_result: { type: "string", minLength: 1 },
        report_path: { type: "string", minLength: 1 },
        results_log_path: nullableStringSchema(),
        overall_score: { type: ["number", "null"] },
        worker_count: nonNegativeIntegerSchema(),
        issues_total: nonNegativeIntegerSchema(),
        severity_counts: auditSeverityCountsSchema,
        warnings: stringArraySchema(),
        artifact_path: nullableStringSchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const evaluationWorkerPayloadSchema = {
    type: "object",
    required: ["status", "worker", "operation", "warnings"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        worker: { type: "string", minLength: 1 },
        operation: { type: "string", minLength: 1 },
        verdict: nullableStringSchema(),
        findings: {
            type: "array",
            items: {
                type: "object",
                additionalProperties: true,
            },
        },
        metrics: {
            type: "object",
            additionalProperties: true,
        },
        decisions: {
            type: "array",
            items: {
                type: "object",
                additionalProperties: true,
            },
        },
        report_path: nullableStringSchema(),
        artifact_path: nullableStringSchema(),
        warnings: stringArraySchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const evaluationCoordinatorPayloadSchema = {
    type: "object",
    required: ["status", "final_result", "report_path", "worker_count", "issues_total", "severity_counts", "warnings", "cleanup_verified"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        final_result: { type: "string", minLength: 1 },
        report_path: { type: "string", minLength: 1 },
        results_log_path: nullableStringSchema(),
        overall_score: { type: ["number", "null"] },
        worker_count: nonNegativeIntegerSchema(),
        agent_count: nonNegativeIntegerSchema(),
        issues_total: nonNegativeIntegerSchema(),
        severity_counts: auditSeverityCountsSchema,
        warnings: stringArraySchema(),
        cleanup_verified: { type: "boolean" },
        research_completed: { type: "boolean" },
        artifact_path: nullableStringSchema(),
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const optimizationWorkerPayloadSchema = {
    type: "object",
    required: ["status", "worker"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        worker: { type: "string", minLength: 1 },
        cycle: { type: "integer", minimum: 1 },
        phase_context: nullableStringSchema(),
        artifact_path: nullableStringSchema(),
        branch: { type: "string" },
        baseline: { type: "object" },
        performance_map: { type: "object" },
        wrong_tool_indicators: stringArraySchema(),
        e2e_test: { type: "object" },
        instrumented_files: stringArraySchema(),
        industry_benchmark: { type: "object" },
        target_metrics: { type: "object" },
        hypotheses: stringArraySchema(),
        local_codebase_findings: stringArraySchema(),
        verdict: { type: "string" },
        corrections_applied: stringArraySchema(),
        concerns: stringArraySchema(),
        final: { type: "object" },
        total_improvement_pct: { type: "number" },
        target_met: { type: "boolean" },
        strike_result: { type: "string" },
        hypotheses_applied: stringArraySchema(),
        hypotheses_removed: stringArraySchema(),
        recorded_at: dateTimeSchema(),
    },
};

export const optimizationCoordinatorPayloadSchema = {
    type: "object",
    required: ["status", "final_result", "cycle_count", "report_ready", "execution_mode"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        final_result: { type: "string", minLength: 1 },
        cycle_count: nonNegativeIntegerSchema(),
        stop_reason: nullableStringSchema(),
        report_ready: { type: "boolean" },
        execution_mode: { type: "string", minLength: 1 },
        target_metric: { type: ["object", "null"] },
        total_improvement_pct: { type: ["number", "null"] },
        target_met: { type: ["boolean", "null"] },
        summary_artifact_path: nullableStringSchema(),
        report_path: nullableStringSchema(),
    },
};

export const dependencyWorkerPayloadSchema = {
    type: "object",
    required: ["status", "worker", "package_manager"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        worker: { type: "string", minLength: 1 },
        package_manager: { type: "string", minLength: 1 },
        branch: nullableStringSchema(),
        upgrades: {
            type: "array",
            items: {
                type: "object",
                required: ["package", "from", "to"],
                additionalProperties: false,
                properties: {
                    package: { type: "string", minLength: 1 },
                    from: { type: "string", minLength: 1 },
                    to: { type: "string", minLength: 1 },
                    breaking: { type: "boolean" },
                },
            },
        },
        warnings: stringArraySchema(),
        errors: stringArraySchema(),
        tests_passed: { type: "boolean" },
        build_passed: { type: "boolean" },
        artifact_path: nullableStringSchema(),
    },
};

export const dependencyCoordinatorPayloadSchema = {
    type: "object",
    required: ["status", "final_result", "worker_count", "upgraded_packages", "verification_passed", "report_ready"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        final_result: { type: "string", minLength: 1 },
        worker_count: nonNegativeIntegerSchema(),
        upgraded_packages: nonNegativeIntegerSchema(),
        failed_workers: nonNegativeIntegerSchema(),
        verification_passed: { type: "boolean" },
        report_ready: { type: "boolean" },
        report_path: nullableStringSchema(),
        artifact_path: nullableStringSchema(),
    },
};

export const modernizationWorkerPayloadSchema = {
    type: "object",
    required: ["status", "worker"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        worker: { type: "string", minLength: 1 },
        branch: nullableStringSchema(),
        changes_applied: nonNegativeIntegerSchema(),
        changes_discarded: nonNegativeIntegerSchema(),
        tests_passed: { type: "boolean" },
        build_passed: { type: "boolean" },
        modules_replaced: nonNegativeIntegerSchema(),
        loc_removed: nonNegativeIntegerSchema(),
        bundle_reduction_bytes: nonNegativeIntegerSchema(),
        warnings: stringArraySchema(),
        errors: stringArraySchema(),
        artifact_path: nullableStringSchema(),
    },
};

export const modernizationCoordinatorPayloadSchema = {
    type: "object",
    required: ["status", "final_result", "worker_count", "verification_passed", "report_ready"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        final_result: { type: "string", minLength: 1 },
        worker_count: nonNegativeIntegerSchema(),
        verification_passed: { type: "boolean" },
        report_ready: { type: "boolean" },
        modules_replaced: nonNegativeIntegerSchema(),
        loc_removed: nonNegativeIntegerSchema(),
        bundle_reduction_bytes: nonNegativeIntegerSchema(),
        report_path: nullableStringSchema(),
        artifact_path: nullableStringSchema(),
    },
};

export const benchmarkWorkerPayloadSchema = {
    type: "object",
    required: ["status", "worker", "scenarios_total", "scenarios_passed", "scenarios_failed", "activation_valid", "validity_verdict", "warnings"],
    additionalProperties: false,
    properties: {
        status: { type: "string", enum: WORKER_SUMMARY_STATUS_LIST },
        worker: { type: "string", minLength: 1 },
        scenarios_total: nonNegativeIntegerSchema(),
        scenarios_passed: nonNegativeIntegerSchema(),
        scenarios_failed: nonNegativeIntegerSchema(),
        activation_valid: { type: "boolean" },
        validity_verdict: { type: "string", minLength: 1 },
        report_path: nullableStringSchema(),
        artifact_path: nullableStringSchema(),
        scenario_ids: stringArraySchema(),
        warnings: stringArraySchema(),
        metrics: {
            type: "object",
            additionalProperties: true,
        },
        metadata: {
            type: "object",
            additionalProperties: true,
        },
    },
};

export const environmentWorkerSummarySchema = buildSummaryEnvelopeSchema(environmentWorkerPayloadSchema);
export const opportunityDiscoveryWorkerSummarySchema = buildSummaryEnvelopeSchema(opportunityDiscoveryWorkerPayloadSchema);
export const storyPlanWorkerSummarySchema = buildSummaryEnvelopeSchema(storyPlanWorkerPayloadSchema);
export const storyPlanCoordinatorSummarySchema = buildSummaryEnvelopeSchema(storyPlanCoordinatorPayloadSchema);
export const taskPlanWorkerSummarySchema = buildSummaryEnvelopeSchema(taskPlanWorkerPayloadSchema);
export const qualityWorkerSummarySchema = buildSummaryEnvelopeSchema(qualityWorkerPayloadSchema);
export const taskStatusWorkerSummarySchema = buildSummaryEnvelopeSchema(taskStatusWorkerPayloadSchema);
export const testPlanningWorkerSummarySchema = buildSummaryEnvelopeSchema(testPlanningWorkerPayloadSchema);
export const storyPrioritizationWorkerSummarySchema = buildSummaryEnvelopeSchema(storyPrioritizationWorkerPayloadSchema);
export const docsGenerationWorkerSummarySchema = buildSummaryEnvelopeSchema(docsGenerationWorkerPayloadSchema);
export const epicPlanCoordinatorSummarySchema = buildSummaryEnvelopeSchema(epicPlanCoordinatorPayloadSchema);
export const scopeDecompositionSummarySchema = buildSummaryEnvelopeSchema(scopeDecompositionPayloadSchema);
export const auditWorkerSummarySchema = buildSummaryEnvelopeSchema(auditWorkerPayloadSchema);
export const auditCoordinatorSummarySchema = buildSummaryEnvelopeSchema(auditCoordinatorPayloadSchema);
export const evaluationWorkerSummarySchema = buildSummaryEnvelopeSchema(evaluationWorkerPayloadSchema);
export const evaluationCoordinatorSummarySchema = buildSummaryEnvelopeSchema(evaluationCoordinatorPayloadSchema);
export const pipelineStageCoordinatorSummarySchema = buildSummaryEnvelopeSchema(pipelineStageCoordinatorPayloadSchema);
export const optimizationWorkerSummarySchema = buildSummaryEnvelopeSchema(optimizationWorkerPayloadSchema);
export const optimizationCoordinatorSummarySchema = buildSummaryEnvelopeSchema(optimizationCoordinatorPayloadSchema);
export const dependencyWorkerSummarySchema = buildSummaryEnvelopeSchema(dependencyWorkerPayloadSchema);
export const dependencyCoordinatorSummarySchema = buildSummaryEnvelopeSchema(dependencyCoordinatorPayloadSchema);
export const modernizationWorkerSummarySchema = buildSummaryEnvelopeSchema(modernizationWorkerPayloadSchema);
export const modernizationCoordinatorSummarySchema = buildSummaryEnvelopeSchema(modernizationCoordinatorPayloadSchema);
export const benchmarkWorkerSummarySchema = buildSummaryEnvelopeSchema(benchmarkWorkerPayloadSchema);

export const environmentStateSchema = {
    type: "object",
    required: ["scanned_at", "agents"],
    properties: {
        scanned_at: { type: "string", format: "date-time" },
        agents: {
            type: "object",
            required: ["claude", "codex"],
            properties: {
                claude: {
                    type: "object",
                    required: ["available"],
                    properties: {
                        available: { type: "boolean" },
                        disabled: { type: "boolean" },
                        version: { type: "string" },
                        detail: { type: "string" },
                    },
                },
                codex: {
                    type: "object",
                    required: ["available"],
                    properties: {
                        available: { type: "boolean" },
                        disabled: { type: "boolean" },
                        version: { type: "string" },
                        config_aligned: { type: "boolean" },
                        servers_aligned: { type: "integer" },
                        marketplace_plugins: stringArraySchema(),
                        alignment_actions: stringArraySchema(),
                        detail: { type: "string" },
                    },
                }
            },
        },
        task_management: {
            type: "object",
            properties: {
                provider: { type: "string", enum: ["linear", "file", "github"] },
                status: { type: "string" },
                fallback: { type: "string", enum: ["file"] },
                linear: {
                    type: "object",
                    properties: {
                        team_id: { type: "string" },
                    },
                },
                github: {
                    type: "object",
                    properties: {
                        repository: { type: "string" },
                        project_number: { type: "integer" },
                    },
                },
            },
        },
        research: {
            type: "object",
            properties: {
                provider: { type: "string" },
                fallback_chain: stringArraySchema(),
                status: { type: "string" },
            },
        },
        claude_md: {
            type: "object",
            properties: {
                exists: { type: "boolean" },
                has_compact_instructions: { type: "boolean" },
                has_mcp_preferences: { type: "boolean" },
                has_date_stamp: { type: "boolean" },
                line_count: { type: "integer" },
                has_timestamps: { type: "boolean" },
            },
        },
        assessment: {
            type: "object",
            properties: {
                assessed_at: { type: "string", format: "date-time" },
                all_green: { type: "boolean" },
                score: { type: "string" },
                warnings: stringArraySchema(),
                info: stringArraySchema(),
                workers_run: stringArraySchema(),
                workers_skipped: stringArraySchema(),
            },
        },
        hooks: {
            type: "object",
            properties: {
                mode: {
                    type: "string",
                    enum: ["blocking", "advisory"],
                },
            },
        },
        ide_extension: {
            type: "object",
            properties: {
                cursor: ideExtensionEntrySchema(),
                vscode: ideExtensionEntrySchema(),
            },
        },
    },
};

function ideExtensionEntrySchema() {
    return {
        type: "object",
        properties: {
            installed: { type: "boolean" },
            extension_version: { type: "string" },
            settings_path: { type: "string" },
            initial_permission_mode: {
                type: "string",
                enum: ["default", "acceptEdits", "plan", "bypassPermissions"],
            },
            allow_dangerously_skip_permissions: { type: "boolean" },
            effective_state: {
                type: "string",
                enum: [
                    "default-prompt",
                    "accept-edits",
                    "plan-only",
                    "bypass-active",
                    "bypass-blocked",
                    "no-ide",
                ],
            },
            conflict_with_project_default_mode: {
                type: "string",
                enum: ["aligned", "override", "n/a"],
            },
            last_modified_by_skill: { type: "string" },
        },
    };
}

export const reviewAgentRecordSchema = {
    type: "object",
    required: ["name"],
    additionalProperties: false,
    properties: {
        name: { type: "string", minLength: 1 },
        status: { type: "string", enum: REVIEW_AGENT_STATUS_LIST },
        prompt_file: nullableStringSchema(),
        result_file: nullableStringSchema(),
        log_file: nullableStringSchema(),
        metadata_file: nullableStringSchema(),
        pid: { type: ["integer", "null"] },
        session_id: nullableStringSchema(),
        started_at: { type: ["string", "null"], format: "date-time" },
        finished_at: { type: ["string", "null"], format: "date-time" },
        exit_code: { type: ["integer", "null"] },
        error: nullableStringSchema(),
    },
};

export const storyGroupRecordSchema = {
    type: "object",
    required: ["group_id"],
    additionalProperties: false,
    properties: {
        group_id: { type: "string", minLength: 1 },
        task_ids: stringArraySchema(),
        status: { type: "string", enum: STORY_EXECUTION_GROUP_STATUS_LIST },
        result: { type: "string" },
        completed_at: dateTimeSchema(),
        inflight_workers: { type: "object" },
    },
};

export const qualitySummarySchema = {
    type: "object",
    required: ["story_id", "verdict"],
    additionalProperties: false,
    properties: {
        story_id: { type: "string", minLength: 1 },
        verdict: { type: "string", enum: STORY_GATE_VERDICT_LIST },
        quality_score: { type: "number" },
        issues: stringArraySchema(),
        fast_track: { type: "boolean" },
        agent_review_summary: { type: "object" },
        regression_status: { type: "string" },
    },
};

export const testSummarySchema = {
    type: "object",
    required: ["story_id", "status"],
    additionalProperties: false,
    properties: {
        story_id: { type: "string", minLength: 1 },
        mode: { type: "string" },
        test_task_id: { type: "string" },
        status: { type: "string", minLength: 1 },
        planned_scenarios: stringArraySchema(),
        coverage_summary: { type: "string" },
        planner_invoked: { type: "boolean" },
        error: { type: "string" },
    },
};

export const optimizationWorkerResultSchema = optimizationWorkerPayloadSchema;

export const optimizationCycleSchema = {
    type: "object",
    required: ["cycle"],
    additionalProperties: false,
    properties: {
        cycle: { type: "integer", minimum: 1 },
        status: { type: "string", enum: OPTIMIZATION_CYCLE_STATUS_LIST },
        next_cycle: { type: "integer" },
        stop_reason: { type: "string" },
        final_result: { type: "string" },
        recorded_at: dateTimeSchema(),
    },
};

// ── Blueprint verification (ln-401 task executor) ──────────────────────────

export const blueprintCheckpointPayloadSchema = {
    type: "object",
    required: ["blueprint"],
    properties: {
        blueprint: {
            type: "object",
            required: ["change_order"],
            properties: {
                change_order: {
                    type: "array",
                    items: {
                        type: "object",
                        required: ["file", "action"],
                        properties: {
                            file: { type: "string", minLength: 1 },
                            action: { type: "string", enum: ["create", "modify"] },
                            reason: { type: "string" },
                        },
                    },
                    minItems: 1,
                },
            },
        },
    },
};

export const blueprintStatusSchema = {
    type: "object",
    required: ["planned_count", "completed", "skipped", "added", "completion_pct"],
    properties: {
        planned_count: { type: "integer", minimum: 0 },
        completed: stringArraySchema(),
        skipped: {
            type: "array",
            items: {
                type: "object",
                required: ["file", "justification"],
                properties: {
                    file: { type: "string", minLength: 1 },
                    justification: { type: "string", minLength: 1 },
                },
            },
        },
        added: {
            type: "array",
            items: {
                type: "object",
                required: ["file", "justification"],
                properties: {
                    file: { type: "string", minLength: 1 },
                    justification: { type: "string", minLength: 1 },
                },
            },
        },
        completion_pct: { type: "number", minimum: 0, maximum: 100 },
    },
};
