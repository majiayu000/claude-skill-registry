export const KNOWN_STAGES = [
  "exploration",
  "diagnosis",
  "execution",
  "verification",
  "reusable-workflow",
  "action",
] as const;

export const KNOWN_TASK_TYPES = [
  "debugging",
  "implementation",
  "code-review",
  "refactoring",
  "architecture",
  "planning",
  "documentation",
  "testing",
  "exploration",
  "other",
] as const;

export const KNOWN_FLAGS = [
  "missing-context",
  "no-constraints",
  "no-verification",
  "no-output-format",
  "missing-input-boundaries",
  "privacy-risk",
  "safety-risk",
] as const;

export const KNOWN_TIP_KINDS = [
  "clarify-goal",
  "add-context-evidence",
  "add-expected-actual",
  "add-error-output",
  "name-file-or-function",
  "add-scope-boundary",
  "add-output-format",
  "add-verification-command",
  "redact-sensitive-data",
  "add-safety-check",
  "state-decision-criteria",
] as const;

export type Stage = (typeof KNOWN_STAGES)[number];
export type TaskType = (typeof KNOWN_TASK_TYPES)[number];
export type PromptFlag = (typeof KNOWN_FLAGS)[number];
export type TipKind = (typeof KNOWN_TIP_KINDS)[number];

export interface CoachingNote {
  habit: string;
  why: string;
  practice: string;
}

export const TIP_COACHING: Record<TipKind, CoachingNote> = {
  "clarify-goal": {
    habit: "Name the exact outcome you want before adding details.",
    why: "A clear goal keeps the agent from optimizing for the wrong task.",
    practice: "For the next three prompts, start with `Goal:` in one sentence.",
  },
  "add-context-evidence": {
    habit: "Add the evidence that makes the problem diagnosable.",
    why: "Evidence is the difference between guessing and narrowing the cause.",
    practice: "For the next three diagnosis prompts, include what changed and what you observed.",
  },
  "add-expected-actual": {
    habit: "Add expected behavior and actual behavior before asking for a fix.",
    why: "Expected vs. actual gives the agent a concrete gap to explain.",
    practice: "For the next three debugging prompts, include `Expected:` and `Actual:`.",
  },
  "add-error-output": {
    habit: "Paste the exact error output or failing assertion when it is safe.",
    why: "Exact errors reduce broad searching and false root causes.",
    practice: "For the next three debugging prompts, include the smallest useful error excerpt.",
  },
  "name-file-or-function": {
    habit: "Name the file, function, command, or diff the agent should focus on.",
    why: "Input boundaries keep the agent from searching or editing more than needed.",
    practice: "For the next three code prompts, include at least one file path or command.",
  },
  "add-scope-boundary": {
    habit: "Add one boundary such as no new dependencies, minimal diff, or no API changes.",
    why: "Boundaries protect the parts of the codebase you do not want redesigned.",
    practice: "For the next three implementation prompts, include one `Do not...` line.",
  },
  "add-output-format": {
    habit: "Ask for the response shape that will make the answer easiest to review.",
    why: "A return format turns useful work into something you can scan and act on.",
    practice: "For the next three prompts, include a short `Return:` list.",
  },
  "add-verification-command": {
    habit: "End with the command, test, or edge case that proves the work.",
    why: "Verification turns a request into a checkable engineering task.",
    practice: "For the next three execution prompts, end with `Verify with...`.",
  },
  "redact-sensitive-data": {
    habit: "Replace secrets, personal data, and private URLs with labeled placeholders.",
    why: "Privacy issues matter more than prompt structure because they can expose sensitive data.",
    practice: "For the next three prompts with logs or credentials, redact first.",
  },
  "add-safety-check": {
    habit: "Add confirmation, rollback, or dry-run steps before risky operations.",
    why: "Clear prompts can still be unsafe when they ask for destructive or broad changes.",
    practice: "For the next three risky operations, include a dry run or rollback note.",
  },
  "state-decision-criteria": {
    habit: "State the criteria the agent should use to compare options.",
    why: "Decision criteria make planning advice easier to judge instead of just plausible.",
    practice: "For the next three planning prompts, list two or three criteria up front.",
  },
};

const DEFAULT_PRIORITY: TipKind[] = [
  "redact-sensitive-data",
  "add-safety-check",
  "clarify-goal",
  "name-file-or-function",
  "add-context-evidence",
  "add-scope-boundary",
  "add-verification-command",
  "add-output-format",
];

const STAGE_PRIORITIES: Record<Stage, TipKind[]> = {
  exploration: [
    "redact-sensitive-data",
    "add-safety-check",
    "clarify-goal",
    "state-decision-criteria",
    "add-context-evidence",
  ],
  diagnosis: [
    "redact-sensitive-data",
    "add-safety-check",
    "clarify-goal",
    "add-expected-actual",
    "add-error-output",
    "add-context-evidence",
    "name-file-or-function",
  ],
  execution: [
    "redact-sensitive-data",
    "add-safety-check",
    "name-file-or-function",
    "add-context-evidence",
    "add-expected-actual",
    "add-scope-boundary",
    "add-verification-command",
    "add-output-format",
  ],
  verification: [
    "redact-sensitive-data",
    "add-safety-check",
    "name-file-or-function",
    "clarify-goal",
    "add-verification-command",
    "add-output-format",
  ],
  "reusable-workflow": [
    "redact-sensitive-data",
    "add-safety-check",
    "state-decision-criteria",
    "add-context-evidence",
    "add-scope-boundary",
    "add-output-format",
    "add-verification-command",
  ],
  action: [
    "redact-sensitive-data",
    "add-safety-check",
    "clarify-goal",
  ],
};

const TASK_PRIORITIES: Partial<Record<TaskType, TipKind[]>> = {
  debugging: [
    "redact-sensitive-data",
    "add-safety-check",
    "add-expected-actual",
    "add-error-output",
    "name-file-or-function",
    "add-verification-command",
    "add-output-format",
  ],
  implementation: [
    "redact-sensitive-data",
    "add-safety-check",
    "name-file-or-function",
    "add-context-evidence",
    "add-scope-boundary",
    "add-verification-command",
    "add-output-format",
  ],
  "code-review": [
    "redact-sensitive-data",
    "add-safety-check",
    "name-file-or-function",
    "state-decision-criteria",
    "add-output-format",
    "add-verification-command",
  ],
  refactoring: [
    "redact-sensitive-data",
    "add-safety-check",
    "name-file-or-function",
    "add-scope-boundary",
    "add-verification-command",
    "add-output-format",
  ],
  planning: [
    "redact-sensitive-data",
    "add-safety-check",
    "state-decision-criteria",
    "clarify-goal",
    "add-context-evidence",
    "add-output-format",
  ],
  testing: [
    "redact-sensitive-data",
    "name-file-or-function",
    "add-verification-command",
    "add-expected-actual",
    "add-output-format",
  ],
  documentation: [
    "redact-sensitive-data",
    "clarify-goal",
    "state-decision-criteria",
    "add-context-evidence",
    "add-output-format",
  ],
};

const FLAG_TIP_DEFAULTS: Record<PromptFlag, TipKind> = {
  "missing-context": "add-context-evidence",
  "no-constraints": "add-scope-boundary",
  "no-verification": "add-verification-command",
  "no-output-format": "add-output-format",
  "missing-input-boundaries": "name-file-or-function",
  "privacy-risk": "redact-sensitive-data",
  "safety-risk": "add-safety-check",
};

const TIP_KIND_FLAGS: Partial<Record<TipKind, PromptFlag>> = {
  "add-context-evidence": "missing-context",
  "add-expected-actual": "missing-context",
  "add-error-output": "missing-context",
  "name-file-or-function": "missing-input-boundaries",
  "add-scope-boundary": "no-constraints",
  "add-output-format": "no-output-format",
  "add-verification-command": "no-verification",
  "redact-sensitive-data": "privacy-risk",
  "add-safety-check": "safety-risk",
};

export function normalizeStage(value: string | undefined): Stage | null {
  const normalized = (value ?? "").trim().toLowerCase().replace(/\s+/g, "-");
  return (KNOWN_STAGES as readonly string[]).includes(normalized) ? (normalized as Stage) : null;
}

export function normalizeTaskType(value: string | undefined): TaskType {
  const normalized = (value ?? "").trim().toLowerCase();
  return (KNOWN_TASK_TYPES as readonly string[]).includes(normalized) ? (normalized as TaskType) : "other";
}

export function normalizeTipKind(value: string | undefined): TipKind | null {
  const normalized = (value ?? "").trim().toLowerCase();
  return (KNOWN_TIP_KINDS as readonly string[]).includes(normalized) ? (normalized as TipKind) : null;
}

export function normalizeFlags(flags: string[]): PromptFlag[] {
  return flags.filter((flag): flag is PromptFlag => (KNOWN_FLAGS as readonly string[]).includes(flag));
}

export function priorityFor(stage: string | undefined, taskType: string | undefined): TipKind[] {
  const stagePriority = normalizeStage(stage) ? STAGE_PRIORITIES[normalizeStage(stage)!] : DEFAULT_PRIORITY;
  const taskPriority = TASK_PRIORITIES[normalizeTaskType(taskType)] ?? [];
  return [...new Set([...taskPriority, ...stagePriority, ...DEFAULT_PRIORITY])];
}

export function tipKindForFlag(flag: PromptFlag, taskType: string | undefined): TipKind {
  if (flag === "missing-context" && normalizeTaskType(taskType) === "debugging") {
    return "add-expected-actual";
  }
  return FLAG_TIP_DEFAULTS[flag];
}

export function flagForTipKind(tipKind: TipKind): PromptFlag | null {
  return TIP_KIND_FLAGS[tipKind] ?? null;
}

export function selectTipKind(
  flags: string[],
  stage: string | undefined,
  taskType: string | undefined
): TipKind | null {
  const candidates = normalizeFlags(flags).map((flag) => tipKindForFlag(flag, taskType));
  if (candidates.length === 0) return null;

  const priority = priorityFor(stage, taskType);
  return candidates.sort((a, b) => priority.indexOf(a) - priority.indexOf(b))[0] ?? candidates[0];
}

export function inferTipKindFromText(text: string): TipKind | null {
  const value = text.toLowerCase();
  if (/\b(redact|placeholder|sanitize|secret|token|password|credential|private url|personal data|email)\b/.test(value)) {
    return "redact-sensitive-data";
  }
  if (/\b(confirm|rollback|dry[- ]run|destructive|force[- ]push|delete|safety)\b/.test(value)) {
    return "add-safety-check";
  }
  if (/\b(expected|actual)\b/.test(value)) {
    return "add-expected-actual";
  }
  if (/\b(error|stack trace|traceback|exception|failing assertion|failure output|log output|exact output)\b/.test(value)) {
    return "add-error-output";
  }
  if (/\b(test command|build command|verify|verification|edge case|prove|check|validate|run tests?)\b/.test(value)) {
    return "add-verification-command";
  }
  if (/\b(file|function|method|class|line|diff|branch|repo|repository|path|command|focus)\b/.test(value)) {
    return "name-file-or-function";
  }
  if (/\b(constraint|boundary|do not|don't|dependency|minimal diff|public api)\b/.test(value)) {
    return "add-scope-boundary";
  }
  if (/\b(return|format|structure|findings first|summary|response shape|answer shape)\b/.test(value)) {
    return "add-output-format";
  }
  if (/\b(criteria|tradeoff|compare|decision|audience|option|pros?|cons?)\b/.test(value)) {
    return "state-decision-criteria";
  }
  if (/\b(goal|outcome|intent|action|complete sentence|specific concern|specific ask|what you want)\b/.test(value)) {
    return "clarify-goal";
  }
  if (/\b(context|evidence|recent change|background|repro|reproduction|symptom|observation|what changed)\b/.test(value)) {
    return "add-context-evidence";
  }
  return null;
}
