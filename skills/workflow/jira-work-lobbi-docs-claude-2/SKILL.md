---
name: jira:work
description: Start working on a Jira issue with optimized tiered orchestration. Begins with intelligent question-gathering to ensure complete understanding before implementation.
version: 5.1.0
qualityGatesIntegration: code-quality-orchestrator
agentOrchestration: true
executionTiers: [FAST, STANDARD, FULL]
minSubAgents: 3
maxSubAgents: 12
caching: true
parallelExecution: maximized
questionGathering: mandatory
---

# Jira Work Orchestration v5.1 (Optimized)

High-performance workflow with **intelligent question-gathering**, **tiered execution**, **caching**, and **maximum parallelization**.

**Key Features in v5.1:**
- ❓ **Question-First Protocol** - Ask all clarifying questions BEFORE starting
- ⚡ **3 Execution Tiers:** FAST (3-4 agents) | STANDARD (6-8) | FULL (10-12)
- 🚀 **40% Faster:** Parallel phase execution where possible
- 💾 **Caching Layer:** Memoized Jira/Confluence lookups
- 🎯 **Smart Gates:** 5 gates → 3 parallel gate groups
- 🔀 **Early Exit:** Skip unnecessary phases for trivial changes

---

## PHASE 0: Question-Gathering (MANDATORY)

**Before ANY work begins, Claude MUST gather sufficient context by asking questions.**

```
QUESTION-GATHERING PROTOCOL:
═════════════════════════════════════════════════════════════════════════
  ┌─────────────────────────────────────────────────────────────────────┐
  │  STEP 1: Initial Analysis (~30 seconds)                             │
  │  ─────────────────────────────────────────                          │
  │  • Parse Jira issue description                                     │
  │  • Identify ambiguous requirements                                  │
  │  • Detect missing technical details                                 │
  │  • Check for undefined acceptance criteria                          │
  └─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │  STEP 2: Generate Question Categories                               │
  │  ────────────────────────────────────                               │
  │                                                                      │
  │  📋 REQUIREMENTS QUESTIONS                                          │
  │     • What is the expected behavior?                                │
  │     • What are the acceptance criteria?                             │
  │     • Are there edge cases to consider?                             │
  │     • What should happen on errors?                                 │
  │                                                                      │
  │  🔧 TECHNICAL QUESTIONS                                             │
  │     • Which components/files are affected?                          │
  │     • Are there existing patterns to follow?                        │
  │     • What dependencies are involved?                               │
  │     • Are there performance requirements?                           │
  │                                                                      │
  │  🎨 DESIGN QUESTIONS                                                │
  │     • UI/UX requirements (if applicable)?                           │
  │     • API contract expectations?                                    │
  │     • Database schema changes needed?                               │
  │                                                                      │
  │  ⚠️ RISK QUESTIONS                                                  │
  │     • Rollback strategy if something goes wrong?                    │
  │     • Testing requirements?                                         │
  │     • Security considerations?                                      │
  │                                                                      │
  │  🔗 DEPENDENCY QUESTIONS                                            │
  │     • Are there blocking issues?                                    │
  │     • External team dependencies?                                   │
  │     • Timeline constraints?                                         │
  └─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │  STEP 3: Present Questions & Wait for Answers                       │
  │  ────────────────────────────────────────────                       │
  │  • Present grouped questions clearly                                │
  │  • Wait for user responses                                          │
  │  • Ask follow-up questions if needed                                │
  │  • Confirm understanding before proceeding                          │
  └─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │  STEP 4: Confirmation                                               │
  │  ────────────────────                                               │
  │  "Based on your answers, here's my understanding:                   │
  │   [Summary of requirements]                                         │
  │                                                                      │
  │   Is this correct? Should I proceed with implementation?"           │
  └─────────────────────────────────────────────────────────────────────┘
═════════════════════════════════════════════════════════════════════════
```

### Question Categories by Tier

| Tier | Min Questions | Focus Areas |
|------|---------------|-------------|
| **FAST** | 1-2 | Confirmation only ("Just updating X, correct?") |
| **STANDARD** | 3-5 | Requirements, affected files, testing approach |
| **FULL** | 5-10 | Full technical spec, architecture, security, rollback |

### Intelligent Question Generation

```typescript
interface QuestionContext {
  issueKey: string;
  issueType: string;
  description: string;
  acceptanceCriteria: string[];
  labels: string[];
  components: string[];
}

function generateQuestions(context: QuestionContext): Question[] {
  const questions: Question[] = [];

  // Requirements gaps
  if (!context.acceptanceCriteria?.length) {
    questions.push({
      category: 'requirements',
      priority: 'high',
      question: 'What are the acceptance criteria for this issue?'
    });
  }

  // Technical ambiguity
  if (context.description.includes('should') || context.description.includes('might')) {
    questions.push({
      category: 'technical',
      priority: 'medium',
      question: 'The description mentions "should/might" - is this optional or required behavior?'
    });
  }

  // Error handling
  if (context.issueType === 'Story' && !context.description.includes('error')) {
    questions.push({
      category: 'requirements',
      priority: 'medium',
      question: 'How should the system handle error cases?'
    });
  }

  // Testing strategy
  if (!context.labels.includes('tested') && !context.labels.includes('no-tests')) {
    questions.push({
      category: 'technical',
      priority: 'low',
      question: 'What level of test coverage is expected?'
    });
  }

  // Security implications
  if (detectSecurityKeywords(context.description)) {
    questions.push({
      category: 'security',
      priority: 'high',
      question: 'Are there specific security requirements or compliance needs?'
    });
  }

  return questions;
}

// Example question output
const exampleQuestions = `
Before I start working on ${issueKey}, I have a few questions:

**Requirements:**
1. The description mentions "user authentication" - should this support both email/password and OAuth, or just one?
2. What should happen if a user's session expires mid-action?

**Technical:**
3. Should I follow the existing auth patterns in src/auth/, or is there a new approach you prefer?
4. Are there specific performance requirements (e.g., max auth latency)?

**Testing:**
5. Should I add integration tests with the OAuth provider, or mock those?

Please answer these questions and I'll proceed with implementation.
`;
```

### Skip Conditions (FAST tier only)

Questions can be skipped when ALL of these are true:
- Issue type is: Bug, Sub-task, or Documentation
- Description is very specific (< 50 words)
- Acceptance criteria are clearly defined
- Files to change are explicitly mentioned
- No security implications detected

```typescript
function shouldSkipQuestions(context: QuestionContext): boolean {
  const skipTypes = ['Bug', 'Sub-task', 'Documentation', 'Task'];
  const hasSpecificDescription = context.description.split(' ').length < 50;
  const hasClearAC = context.acceptanceCriteria.length >= 2;
  const hasFilesMentioned = /\.(ts|js|py|go|java|rb)/.test(context.description);
  const noSecurityImplications = !detectSecurityKeywords(context.description);

  return (
    skipTypes.includes(context.issueType) &&
    hasSpecificDescription &&
    hasClearAC &&
    hasFilesMentioned &&
    noSecurityImplications
  );
}
```

---

## Quick Start

```
/jira:work <issue-key> [--tier=auto|fast|standard|full] [--skip-questions]
```

**Note:** `--skip-questions` is only available for FAST tier and trivial changes.

### Tier Auto-Selection Logic
```
FAST:     docs-only | config | typo | readme | 1-2 files
STANDARD: bug-fix | minor-feature | refactor | 3-10 files
FULL:     major-feature | architectural | security | 10+ files
```

---

## Optimized Architecture (v5.1)

```
┌─────────────────────────────────────────────────────────────────────────┐
│           JIRA WORK ORCHESTRATOR v5.1 - QUESTION-FIRST EXECUTION         │
│                    ⚡ Optimized for Speed ⚡                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ TIER SELECTOR (runs first, ~500ms)                              │    │
│  │  Analyze: issue type, labels, files, complexity → select tier   │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                              │                                          │
│            ┌─────────────────┼─────────────────┐                       │
│            ▼                 ▼                 ▼                       │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐                  │
│     │   FAST   │      │ STANDARD │      │   FULL   │                  │
│     │ 3-4 agnt │      │ 6-8 agnt │      │10-12 agnt│                  │
│     │ ~2 min   │      │ ~5 min   │      │ ~10 min  │                  │
│     └──────────┘      └──────────┘      └──────────┘                  │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════   │
│                                                                          │
│                        PARALLEL EXECUTION LANES                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ LANE 1: CODE PATH          │ LANE 2: CONTEXT (cached)            │  │
│  │ ─────────────────          │ ─────────────────────               │  │
│  │ [EXPLORE]──▶[PLAN]──▶     │ [JIRA]──▶[CONFLUENCE]               │  │
│  │      │           │         │    │          │                     │  │
│  │      ▼           ▼         │    ▼          ▼                     │  │
│  │    [CODE]──▶[TEST+QG]     │ [CACHE]    [CACHE]                  │  │
│  │         \       /          │                                      │  │
│  │          ▼     ▼           │                                      │  │
│  │         [COMMIT]           │                                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════   │
│                                                                          │
│  GATE GROUPS (Parallel)                                                  │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐               │
│  │   GROUP 1     │ │   GROUP 2     │ │   GROUP 3     │               │
│  │ LINT+FORMAT   │ │ SECURITY+DEPS │ │ COVERAGE+CMPLX│               │
│  │   (haiku)     │ │   (haiku)     │ │   (sonnet)    │               │
│  └───────────────┘ └───────────────┘ └───────────────┘               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tiered Execution Modes

### FAST Mode (3-4 agents, ~2 min)
**Use for:** Docs, configs, typos, README, 1-2 file changes

```typescript
// Single consolidated agent for FAST mode
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `FAST MODE: Complete ${issueKey} end-to-end:
    1. Quick context from Jira (cached if available)
    2. Make the simple change
    3. Run lint + format (auto-fix)
    4. Commit and push

    Skip: Full exploration, coverage check, complexity analysis
    Output: { completed: true, files: [], commitSha: string }`
});

// Parallel: Basic quality check
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: "Lint check only: npx eslint --fix && npx prettier --write"
});
```

**Early Exit Conditions:**
- No code changes (docs only) → Skip all quality gates
- Config-only changes → Skip coverage, complexity
- README/typo → Skip everything except commit

---

### STANDARD Mode (6-8 agents, ~5 min)
**Use for:** Bug fixes, minor features, refactors, 3-10 files

```
PARALLEL EXECUTION GRAPH:
═════════════════════════════════════════════════════════════
  ┌─────────────────────────────────────────────────────────┐
  │  WAVE 1 (Parallel Launch - 3 agents)                    │
  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐   │
  │  │  EXPLORE  │  │   JIRA    │  │  CONFLUENCE CACHE │   │
  │  │  (haiku)  │  │  (cached) │  │     (cached)      │   │
  │  └─────┬─────┘  └─────┬─────┘  └─────────┬─────────┘   │
  │        └──────────────┼──────────────────┘              │
  │                       ▼                                  │
  │  ┌─────────────────────────────────────────────────────┐ │
  │  │  WAVE 2: PLAN+CODE (1 consolidated agent)           │ │
  │  │  - Receive context from Wave 1                      │ │
  │  │  - Plan inline (no separate planning agent)         │ │
  │  │  - Execute code changes                             │ │
  │  └─────────────────────────────────────────────────────┘ │
  │                       ▼                                  │
  │  ┌─────────────────────────────────────────────────────┐ │
  │  │  WAVE 3: TEST + QUALITY (3 parallel gate groups)    │ │
  │  │  ┌─────────┐  ┌─────────────┐  ┌─────────────────┐ │ │
  │  │  │LINT+FMT │  │SECURITY+DEPS│  │COVERAGE+COMPLEX │ │ │
  │  │  │ (haiku) │  │   (haiku)   │  │    (sonnet)     │ │ │
  │  │  └─────────┘  └─────────────┘  └─────────────────┘ │ │
  │  └─────────────────────────────────────────────────────┘ │
  │                       ▼                                  │
  │  ┌─────────────────────────────────────────────────────┐ │
  │  │  WAVE 4: COMMIT (1 agent, includes PR)              │ │
  │  └─────────────────────────────────────────────────────┘ │
  └─────────────────────────────────────────────────────────┘
═════════════════════════════════════════════════════════════
```

```typescript
// WAVE 1: Parallel context gathering (with cache)
const [exploreResult, jiraContext, confluenceContext] = await Promise.all([
  Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: `Quick codebase analysis for ${issueKey}:
      - Identify affected files (Glob/Grep)
      - Find test files
      - Map immediate dependencies`
  }),
  getCached('jira', issueKey) || Task({
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: `Fetch and cache Jira issue ${issueKey}`
  }),
  getCached('confluence', issueKey) || Task({
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: "Search Confluence for related docs (cache result)"
  })
]);

// WAVE 2: Consolidated Plan+Code (single agent, inline planning)
const codeResult = await Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `Implement ${issueKey} with inline planning:
    Context: ${JSON.stringify({ exploreResult, jiraContext })}

    1. [INLINE PLAN] Quick design decisions (no separate agent)
    2. [CODE] Implement changes following plan
    3. Output: { files: [], plan: string, summary: string }`
});

// WAVE 3: 3 Gate Groups in Parallel (consolidates 5 gates)
const [lintGate, securityGate, coverageGate] = await Promise.all([
  // Group 1: Lint + Format (combines Static Analysis)
  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: `GATE GROUP 1 - LINT+FORMAT:
      - ESLint with --fix
      - Prettier with --write
      Output: { passed: boolean, issues: [], autoFixed: number }`
  }),

  // Group 2: Security + Dependencies (combines 2 gates)
  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: `GATE GROUP 2 - SECURITY+DEPS:
      - gitleaks (secrets)
      - npm audit (vulnerabilities)
      - Check for outdated critical deps
      Output: { passed: boolean, vulns: [], outdated: [] }`
  }),

  // Group 3: Coverage + Complexity (requires more analysis)
  Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    prompt: `GATE GROUP 3 - COVERAGE+COMPLEXITY:
      - Run tests with coverage (threshold: 80%)
      - Check cyclomatic complexity (max: 10)
      - Identify complex functions
      Output: { passed: boolean, coverage: number, complexity: [] }`
  })
]);

// WAVE 4: Commit + PR (single agent)
await Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `Complete ${issueKey}:
    Quality: ${JSON.stringify({ lintGate, securityGate, coverageGate })}
    1. Commit with smart message
    2. Push to feature branch
    3. Create PR with quality report
    4. Link to Jira
    Output: { commitSha, prUrl, jiraLinked }`
});
```

---

### FULL Mode (10-12 agents, ~10 min)
**Use for:** Major features, architectural changes, security-critical

```
FULL MODE EXECUTION:
═════════════════════════════════════════════════════════════
  WAVE 1: Deep Analysis (4 parallel agents)
  ├── EXPLORE: Deep codebase analysis
  ├── JIRA: Full issue context + linked issues
  ├── CONFLUENCE: Architecture docs, ADRs
  └── SECURITY-PRE: Pre-implementation security review

  WAVE 2: Architecture Planning (2 agents)
  ├── PLAN: Detailed implementation plan with DAG
  └── TEST-PLAN: Test strategy and scenarios

  WAVE 3: Implementation (2-4 agents based on subtasks)
  └── CODE: Parallel subtask execution

  WAVE 4: Comprehensive Quality (3 gate groups + deep security)
  ├── LINT+FORMAT
  ├── SECURITY+DEPS (with SAST)
  ├── COVERAGE+COMPLEXITY
  └── DEEP-SECURITY: Full vulnerability analysis

  WAVE 5: Finalization (2 agents)
  ├── COMMIT: Smart commit + PR
  └── DOCUMENT: Confluence tech doc generation
═════════════════════════════════════════════════════════════
```

---

## Caching Layer (New in v5.0)

```typescript
interface WorkflowCache {
  jira: Map<string, JiraIssue>;      // TTL: 5 minutes
  confluence: Map<string, Page[]>;    // TTL: 10 minutes
  fileAnalysis: Map<string, Analysis>; // TTL: until file modified
  gateResults: Map<string, GateResult>; // TTL: until code changed
}

// Cache-aware fetch pattern
async function getCached<T>(type: keyof WorkflowCache, key: string): Promise<T | null> {
  const cache = workflowCache[type];
  const entry = cache.get(key);

  if (entry && !isExpired(entry)) {
    return entry.value;
  }
  return null; // Cache miss - will fetch fresh
}

// Pre-warm cache at session start
async function prewarmCache(issueKey: string): Promise<void> {
  // Parallel cache warming (runs during tier selection)
  await Promise.all([
    fetchAndCache('jira', issueKey),
    fetchAndCache('confluence', getProjectKey(issueKey))
  ]);
}
```

**Cache Benefits:**
- Same issue re-run: **50% faster** (Jira/Confluence cached)
- Same session multiple issues: **30% faster** (shared project context)
- File unchanged: **Skip redundant analysis**

---

## Early Exit Optimization

```typescript
// Tier determines which gates can be skipped
const earlyExitRules = {
  FAST: {
    skip: ['coverage', 'complexity', 'deepSecurity', 'confluence-doc'],
    require: ['lint']
  },
  STANDARD: {
    skip: ['deepSecurity', 'confluence-doc'],
    require: ['lint', 'security', 'coverage']
  },
  FULL: {
    skip: [],
    require: ['all']
  }
};

// File-type based skips
const fileTypeSkips = {
  'docs': ['coverage', 'complexity'],  // .md, .txt, .rst
  'config': ['coverage'],               // .json, .yaml, .toml
  'test': ['complexity']                // *.test.*, *.spec.*
};

// Apply early exit logic
function shouldSkipGate(gate: string, tier: Tier, files: string[]): boolean {
  // Check tier rules
  if (earlyExitRules[tier].skip.includes(gate)) return true;

  // Check file-type rules
  const fileTypes = detectFileTypes(files);
  if (fileTypes.every(ft => fileTypeSkips[ft]?.includes(gate))) return true;

  return false;
}
```

---

## Failure Recovery & Context Optimization (v5.0)

**Purpose:** Prevent wasted context when agents struggle to find answers or searches fail.

### Search Timeout Limits

```typescript
const SEARCH_LIMITS = {
  // Maximum attempts before giving up
  maxSearchAttempts: 3,

  // Time limits per search type
  timeouts: {
    glob: 5000,        // 5 seconds
    grep: 10000,       // 10 seconds
    explore: 30000,    // 30 seconds
    jiraFetch: 10000,  // 10 seconds
    confluence: 15000  // 15 seconds
  },

  // Context budget per phase (tokens)
  contextBudget: {
    EXPLORE: 5000,
    PLAN: 3000,
    CODE: 15000,
    TEST: 5000,
    QUALITY: 3000,
    FIX: 8000,
    COMMIT: 2000
  }
};
```

### Negative Caching (Failed Search Memoization)

```typescript
interface NegativeCache {
  failedSearches: Map<string, {
    query: string;
    timestamp: number;
    reason: string;
    ttl: number;  // Don't retry for this duration
  }>;
}

// Prevent repeating failed searches
async function searchWithNegativeCache(query: string, searchFn: () => Promise<any>): Promise<any> {
  const cacheKey = hashQuery(query);
  const cached = negativeCache.get(cacheKey);

  if (cached && !isExpired(cached)) {
    // Return early with fallback instead of re-trying
    return {
      found: false,
      reason: cached.reason,
      suggestion: 'Try alternative search pattern'
    };
  }

  try {
    const result = await withTimeout(searchFn(), SEARCH_LIMITS.timeouts.grep);
    return result;
  } catch (error) {
    // Cache the failure to prevent retry storms
    negativeCache.set(cacheKey, {
      query,
      timestamp: Date.now(),
      reason: error.message,
      ttl: 5 * 60 * 1000  // Don't retry for 5 minutes
    });
    throw error;
  }
}
```

### Context Checkpointing

```typescript
interface PhaseCheckpoint {
  phase: string;
  issueKey: string;
  timestamp: string;
  artifacts: {
    filesIdentified: string[];
    planSummary?: string;
    codeChanges?: string[];
    testResults?: any;
    qualityScore?: number;
  };
  contextUsed: number;  // Tokens consumed
  canResume: boolean;
}

// Checkpoint after each phase to prevent re-work
async function checkpointPhase(phase: string, result: any): Promise<void> {
  const checkpoint: PhaseCheckpoint = {
    phase,
    issueKey: currentIssue,
    timestamp: new Date().toISOString(),
    artifacts: extractArtifacts(result),
    contextUsed: estimateTokens(result),
    canResume: true
  };

  // Save to session storage (survives agent restarts)
  await sessionStorage.set(`checkpoint:${currentIssue}:${phase}`, checkpoint);
}

// Resume from last checkpoint if context was lost
async function resumeFromCheckpoint(issueKey: string): Promise<PhaseCheckpoint | null> {
  const phases = ['COMMIT', 'FIX', 'QUALITY', 'TEST', 'CODE', 'PLAN', 'EXPLORE'];

  for (const phase of phases) {
    const checkpoint = await sessionStorage.get(`checkpoint:${issueKey}:${phase}`);
    if (checkpoint?.canResume) {
      return checkpoint;  // Resume from most recent valid checkpoint
    }
  }
  return null;
}
```

### Escalation Patterns

```
STRUGGLE DETECTION & ESCALATION:
═════════════════════════════════════════════════════════════════════════
  ┌─────────────────────────────────────────────────────────────────────┐
  │  LEVEL 1: Agent Self-Recovery (automatic)                          │
  │  ─────────────────────────────────────────                          │
  │  • 3 search attempts with query refinement                          │
  │  • Broaden search pattern on failure                                │
  │  • Try alternative file patterns                                    │
  │  • Timeout: 30 seconds total                                        │
  └───────────────────────────┬─────────────────────────────────────────┘
                              │ (if still failing)
                              ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │  LEVEL 2: Strategy Pivot (automatic)                               │
  │  ─────────────────────────────────                                  │
  │  • Switch from Grep to Glob (or vice versa)                         │
  │  • Use Task(Explore) agent for deeper search                        │
  │  • Check registry for known patterns                                │
  │  • Consult project structure cache                                  │
  └───────────────────────────┬─────────────────────────────────────────┘
                              │ (if still failing)
                              ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │  LEVEL 3: Graceful Degradation (automatic)                         │
  │  ─────────────────────────────────────────                          │
  │  • Proceed with partial context                                     │
  │  • Log what's missing for manual review                             │
  │  • Mark result as "low confidence"                                  │
  │  • Add TODO comments for missing context                            │
  └───────────────────────────┬─────────────────────────────────────────┘
                              │ (if critical blocker)
                              ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │  LEVEL 4: Human Escalation (requires intervention)                 │
  │  ───────────────────────────────────────────────                    │
  │  • Pause workflow with clear status                                 │
  │  • Present what was tried and what failed                           │
  │  • Request specific information needed                              │
  │  • Checkpoint state for resume after input                          │
  └─────────────────────────────────────────────────────────────────────┘
═════════════════════════════════════════════════════════════════════════
```

### Retry Budget & Circuit Breaker

```typescript
interface RetryBudget {
  maxRetries: number;
  currentRetries: number;
  backoffMs: number[];
  circuitOpen: boolean;
  lastFailure?: Date;
}

const retryBudgets: Record<string, RetryBudget> = {
  jiraApi: { maxRetries: 3, currentRetries: 0, backoffMs: [1000, 2000, 4000], circuitOpen: false },
  confluence: { maxRetries: 2, currentRetries: 0, backoffMs: [2000, 5000], circuitOpen: false },
  githubApi: { maxRetries: 3, currentRetries: 0, backoffMs: [1000, 2000, 4000], circuitOpen: false },
  codeSearch: { maxRetries: 3, currentRetries: 0, backoffMs: [500, 1000, 2000], circuitOpen: false }
};

// Circuit breaker pattern
async function withCircuitBreaker<T>(
  service: string,
  operation: () => Promise<T>
): Promise<T | null> {
  const budget = retryBudgets[service];

  // Check if circuit is open (too many recent failures)
  if (budget.circuitOpen) {
    const timeSinceFailure = Date.now() - (budget.lastFailure?.getTime() || 0);
    if (timeSinceFailure < 60000) {  // 1 minute cooldown
      return null;  // Skip this service, use fallback
    }
    budget.circuitOpen = false;  // Reset circuit
  }

  for (let attempt = 0; attempt < budget.maxRetries; attempt++) {
    try {
      const result = await operation();
      budget.currentRetries = 0;  // Reset on success
      return result;
    } catch (error) {
      budget.currentRetries++;
      budget.lastFailure = new Date();

      if (attempt < budget.maxRetries - 1) {
        await sleep(budget.backoffMs[attempt]);
      }
    }
  }

  // Open circuit after exhausting retries
  budget.circuitOpen = true;
  return null;
}
```

### Fallback Strategies

```typescript
const FALLBACK_STRATEGIES = {
  // When Jira API fails
  jiraUnavailable: {
    action: 'useLocalContext',
    steps: [
      'Parse issue key from branch name',
      'Extract context from commit messages',
      'Use cached issue data if available',
      'Proceed with minimal context, mark as draft'
    ]
  },

  // When Confluence search fails
  confluenceUnavailable: {
    action: 'skipDocumentation',
    steps: [
      'Skip Confluence search in EXPLORE',
      'Skip doc generation in COMMIT',
      'Add TODO for manual documentation',
      'Continue with code-only workflow'
    ]
  },

  // When codebase search fails
  searchFailed: {
    action: 'broaden',
    steps: [
      'Try parent directory',
      'Use simpler glob pattern (*.ts instead of **/*.service.ts)',
      'Search by keyword instead of path',
      'Fall back to git log for file history'
    ]
  },

  // When quality gates timeout
  gateTimeout: {
    action: 'partialCheck',
    steps: [
      'Run only fast gates (lint, format)',
      'Skip slow gates (coverage, complexity)',
      'Mark PR as "needs-full-review"',
      'Schedule async quality check'
    ]
  }
};

// Apply fallback when primary strategy fails
async function withFallback<T>(
  primary: () => Promise<T>,
  fallbackKey: keyof typeof FALLBACK_STRATEGIES,
  fallbackFn: () => Promise<T>
): Promise<{ result: T; usedFallback: boolean }> {
  try {
    const result = await withTimeout(primary(), 30000);
    return { result, usedFallback: false };
  } catch (error) {
    console.log(`Primary failed, using fallback: ${fallbackKey}`);
    const result = await fallbackFn();
    return { result, usedFallback: true };
  }
}
```

### Context Budget Enforcement

```typescript
// Track context usage per phase
class ContextBudgetTracker {
  private usage: Map<string, number> = new Map();
  private readonly totalBudget = 100000;  // tokens

  consume(phase: string, tokens: number): boolean {
    const current = this.usage.get(phase) || 0;
    const phaseBudget = SEARCH_LIMITS.contextBudget[phase];

    if (current + tokens > phaseBudget) {
      console.warn(`Phase ${phase} exceeding budget: ${current + tokens}/${phaseBudget}`);
      return false;  // Deny consumption
    }

    this.usage.set(phase, current + tokens);
    return true;
  }

  getRemaining(): number {
    const used = Array.from(this.usage.values()).reduce((a, b) => a + b, 0);
    return this.totalBudget - used;
  }

  shouldCheckpoint(): boolean {
    return this.getRemaining() < 25000;  // 25% remaining
  }

  shouldCompress(): boolean {
    return this.getRemaining() < 10000;  // 10% remaining
  }
}

// Enforce budget during agent execution
const budgetTracker = new ContextBudgetTracker();

async function executeWithBudget(phase: string, operation: () => Promise<any>): Promise<any> {
  if (budgetTracker.shouldCheckpoint()) {
    await checkpointPhase(phase, { partial: true });
  }

  if (budgetTracker.shouldCompress()) {
    await compressContext();  // Summarize and discard old messages
  }

  const result = await operation();
  budgetTracker.consume(phase, estimateTokens(result));
  return result;
}
```

### Summary: Mitigation Quick Reference

| Problem | Detection | Mitigation |
|---------|-----------|------------|
| Search taking too long | Timeout after 30s | Broaden pattern, try alternatives |
| Same search failing repeatedly | Negative cache hit | Skip with fallback, don't retry |
| Context running out | Budget tracker | Checkpoint + compress |
| API consistently failing | Circuit breaker open | Use cached data or skip |
| Agent stuck in loop | Retry count > 3 | Escalate to human |
| Phase incomplete | Missing artifacts | Resume from checkpoint |
| Low confidence result | Fallback was used | Mark for review, add TODOs |

---

## Subagent Communication Protocol

### Message Format
```typescript
interface AgentMessage {
  id: string;
  from: string;        // Agent identifier
  to: string;          // Target agent or "orchestrator"
  phase: string;       // Current workflow phase
  type: "result" | "request" | "error" | "status";
  payload: any;
  timestamp: string;
}
```

### Result Handoff Pattern
```typescript
// Phase N agent completes and reports
const phaseResult = {
  phase: "CODE",
  status: "complete",
  artifacts: {
    filesModified: ["src/api/handler.ts", "src/utils/parser.ts"],
    linesAdded: 245,
    linesRemoved: 12
  },
  nextPhaseInput: {
    filesToTest: ["src/api/handler.ts"],
    coverageTargets: ["handler", "parser"]
  }
};

// Orchestrator receives and forwards to Phase N+1
orchestrator.handoff("TEST", phaseResult.nextPhaseInput);
```

### Error Escalation
```typescript
// Agent encounters blocking error
if (error.severity === "critical") {
  return {
    type: "error",
    escalate: true,
    message: "Security vulnerability detected - blocking commit",
    requiresHumanReview: true
  };
}
```

---

## Agent Registry (Optimized v5.0)

### FAST Mode (3-4 agents)
| Wave | Agent | Model | Purpose |
|------|-------|-------|---------|
| 1 | fast-implementer | haiku | End-to-end: fetch→code→commit |
| 1 | lint-gate | haiku | Quick lint + format (parallel) |
| 2* | fix-agent | sonnet | Only if lint fails |

### STANDARD Mode (6-8 agents)
| Wave | Agent | Model | Purpose |
|------|-------|-------|---------|
| 1 | explore-agent | haiku | Codebase analysis |
| 1 | jira-fetch | haiku | Issue context (cached) |
| 1 | confluence-fetch | haiku | Docs search (cached) |
| 2 | plan-code-agent | sonnet | Consolidated plan + implement |
| 3 | lint-format-gate | haiku | Gate Group 1 |
| 3 | security-deps-gate | haiku | Gate Group 2 |
| 3 | coverage-complex-gate | sonnet | Gate Group 3 |
| 4 | commit-pr-agent | sonnet | Commit + PR + Jira link |

### FULL Mode (10-12 agents)
| Wave | Agent | Model | Purpose |
|------|-------|-------|---------|
| 1 | deep-explore | sonnet | Comprehensive codebase analysis |
| 1 | jira-full | haiku | Issue + linked issues |
| 1 | confluence-arch | sonnet | Architecture docs, ADRs |
| 1 | security-pre | sonnet | Pre-implementation security review |
| 2 | architect-planner | opus | Detailed implementation plan |
| 2 | test-strategist | sonnet | Test planning and scenarios |
| 3 | code-agent (x2-4) | sonnet | Parallel subtask implementation |
| 4 | gate-group-1 | haiku | Lint + Format |
| 4 | gate-group-2 | haiku | Security + Dependencies |
| 4 | gate-group-3 | sonnet | Coverage + Complexity |
| 4 | deep-security | sonnet | Full SAST analysis |
| 5 | commit-pr-agent | sonnet | Smart commit + comprehensive PR |
| 5 | confluence-doc | sonnet | Generate tech documentation |

---

## Performance Comparison

```
┌────────────────────────────────────────────────────────────────┐
│              v4.2 vs v5.0 PERFORMANCE COMPARISON               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AGENT COUNT REDUCTION                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ v4.2: 13-18 agents (all tasks)                           │  │
│  │ v5.0: 3-4 (FAST) | 6-8 (STANDARD) | 10-12 (FULL)        │  │
│  │                                                           │  │
│  │ Average reduction: 40% fewer agents                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  EXECUTION TIME                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         v4.2          │         v5.0                   │    │
│  ├───────────────────────┼────────────────────────────────┤    │
│  │ Simple bug: ~8 min    │ FAST: ~2 min (-75%)           │    │
│  │ Feature: ~12 min      │ STANDARD: ~5 min (-58%)       │    │
│  │ Major: ~15 min        │ FULL: ~10 min (-33%)          │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  GATE CONSOLIDATION                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ v4.2: 5 separate gates (5 agents)                        │  │
│  │ v5.0: 3 gate groups (3 agents, parallel)                 │  │
│  │                                                           │  │
│  │ Group 1: Static Analysis + Formatting                    │  │
│  │ Group 2: Security Scanner + Dependency Health            │  │
│  │ Group 3: Test Coverage + Complexity Analyzer             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  CACHING BENEFITS                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Same issue re-run: 50% faster                            │  │
│  │ Same session/project: 30% faster                         │  │
│  │ Unchanged files: Skip redundant analysis                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  COST REDUCTION (API calls)                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ FAST mode: ~70% fewer API calls                          │  │
│  │ STANDARD mode: ~45% fewer API calls                      │  │
│  │ haiku preference: Lower cost per agent                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

**Total Agents per Run (v5.0):**
- FAST: 3-4 agents
- STANDARD: 6-8 agents
- FULL: 10-12 agents

**v4.2 Comparison:** Was 13-18 agents for ALL task types

## Jira Integration

This command automatically:
- Transitions issue to "In Progress"
- Adds progress comments
- Logs work time
- Creates smart commits
- Links PRs to issues

---

## Confluence Integration (Advanced)

The workflow integrates with Confluence for documentation:

### Auto-Generated Documentation

```typescript
// After successful commit, generate Confluence page
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `Create Confluence documentation for ${issueKey}:
    1. Generate technical design document
    2. Document API changes (if any)
    3. Create/update runbook entries
    4. Add architecture diagrams (mermaid)

    Use mcp__MCP_DOCKER__confluence_create_page`
});
```

### Confluence Features Used

| Feature | Purpose | Trigger |
|---------|---------|---------|
| **Page Creation** | Auto-create tech docs | After COMMIT phase |
| **Page Update** | Update existing docs | If page exists |
| **Search** | Find related docs in EXPLORE | mcp__MCP_DOCKER__confluence_search |
| **Attachment** | Quality reports, diagrams | After QUALITY phase |
| **Labels** | Categorize documentation | Auto-tagged |
| **Macro Insertion** | Jira issue embed, code blocks | Tech docs |

### Documentation Templates

```typescript
// Technical Design Document Template
const techDocTemplate = {
  title: `[${issueKey}] Technical Design - ${summary}`,
  space: projectSpace,
  labels: ["tech-doc", "auto-generated", projectKey],
  sections: [
    "Overview", "Problem Statement", "Solution Architecture",
    "API Changes", "Database Changes", "Testing Strategy",
    "Quality Metrics", "Deployment Notes"
  ]
};
```

### Confluence Search in EXPLORE Phase

```typescript
// Search for related documentation
Task({
  subagent_type: "Explore",
  model: "haiku",
  prompt: `Search Confluence for context:
    Use mcp__MCP_DOCKER__confluence_search with query "${issueKey} OR ${component}"
    1. Find related architecture docs
    2. Locate existing runbooks
    3. Check for similar implementations
    4. Gather ADRs (Architecture Decision Records)`
});
```

---

## GitHub Integration (Advanced)

The workflow integrates deeply with GitHub:

### Branch Strategy

```typescript
// Create feature branch with Jira issue key
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `Create feature branch:
    git checkout -b feature/${issueKey.toLowerCase()}-${slugify(summary)}
    git push -u origin feature/${issueKey}-description`
});
```

### Pull Request Features

```typescript
// Create PR with full quality integration
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `Create comprehensive PR for ${issueKey}:

    1. Create PR: gh pr create --title "${issueKey}: ${summary}"
    2. Add quality report to description
    3. Add labels: gh pr edit --add-label "quality-passed"
    4. Request reviewers: gh pr edit --add-reviewer "@team/code-owners"
    5. Link to Jira in description
    6. Post status check via gh api`
});
```

### GitHub Features Used

| Feature | Purpose | Command |
|---------|---------|---------|
| **Branch Creation** | Feature branches | git checkout -b |
| **PR Creation** | With quality report | gh pr create |
| **Status Checks** | Quality gate status | gh api /statuses |
| **Labels** | Categorize PRs | gh pr edit --add-label |
| **Reviewers** | Auto-assign | gh pr edit --add-reviewer |
| **Projects** | Track in board | gh project item-add |
| **Actions** | Trigger workflows | gh workflow run |
| **Releases** | Auto-generate notes | gh release create |

### GitHub Actions Integration

```typescript
// Trigger quality workflow on PR
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `Trigger GitHub Actions workflow:
    gh workflow run quality-gates.yml \\
      --ref feature/${issueKey} \\
      -f issue_key=${issueKey}`
});
```

### PR Description with Quality Report

```markdown
## Summary
${summary}

**Jira Issue:** [${issueKey}](https://jira.company.com/browse/${issueKey})

## Quality Report
| Gate | Score | Status |
|------|-------|--------|
| Static Analysis | ${staticScore} | ${staticStatus} |
| Test Coverage | ${coverage}% | ${coverageStatus} |
| Security | ${securityScore} | ${securityStatus} |
| Complexity | ${complexityScore} | ${complexityStatus} |
| Dependencies | ${depsScore} | ${depsStatus} |

**Overall:** ${qualityScore}/100 (Grade: ${grade})

## Confluence Docs
- [Technical Design](${confluenceLink})
```

### GitHub Commit Status API

```typescript
// Post quality results as commit status
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `Update GitHub commit status:
    gh api --method POST /repos/{owner}/{repo}/statuses/{sha} \\
      -f state="${allPassed ? 'success' : 'failure'}" \\
      -f description="Quality Score: ${qualityScore}/100" \\
      -f context="quality-gates/curator"`
});
```

---

## Full Workflow Integration Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         JIRA WORK ORCHESTRATOR v4.2.0                        │
│              Integrated with Confluence, GitHub, and Curator                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────┐                                                               │
│  │   JIRA    │◀──────────────────────────────────────────────────────────┐  │
│  │  Arbiter  │                                                            │  │
│  └─────┬─────┘                                                            │  │
│        │                                                                   │  │
│        ▼                                                                   │  │
│  ┌───────────────────────────────────────────────────────────────────┐   │  │
│  │  PHASE 1: EXPLORE                                                  │   │  │
│  │  ┌──────────┐    ┌──────────────┐    ┌──────────────┐            │   │  │
│  │  │ Jira API │    │  Confluence  │    │   Codebase   │            │   │  │
│  │  │  Fetch   │    │   Search     │    │   Analysis   │            │   │  │
│  │  └──────────┘    └──────────────┘    └──────────────┘            │   │  │
│  └───────────────────────────────────────────────────────────────────┘   │  │
│        │                                                                   │  │
│        ▼                                                                   │  │
│  ┌───────────────────────────────────────────────────────────────────┐   │  │
│  │  PHASE 2-4: PLAN → CODE → TEST                                    │   │  │
│  └───────────────────────────────────────────────────────────────────┘   │  │
│        │                                                                   │  │
│        ▼                                                                   │  │
│  ┌───────────────────────────────────────────────────────────────────┐   │  │
│  │  PHASE 5: QUALITY GATES (Curator)                                 │   │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐         │   │  │
│  │  │ Static │ │Coverage│ │Security│ │Complex │ │  Deps  │         │   │  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘         │   │  │
│  └───────────────────────────────────────────────────────────────────┘   │  │
│        │                                                                   │  │
│        ▼                                                                   │  │
│  ┌───────────────────────────────────────────────────────────────────┐   │  │
│  │  PHASE 6-7: FIX → COMMIT                                          │   │  │
│  │  ┌──────────────┐    ┌───────────────────────────────────────┐   │   │  │
│  │  │  Auto-Fix    │    │          GitHub Integration           │   │   │  │
│  │  │   Agent      │───▶│  Branch → Commit → PR → Status Check  │   │   │  │
│  │  └──────────────┘    └───────────────────────────────────────┘   │   │  │
│  └───────────────────────────────────────────────────────────────────┘   │  │
│        │                                                                   │  │
│        ▼                                                                   │  │
│  ┌───────────────────────────────────────────────────────────────────┐   │  │
│  │  POST-COMMIT: Documentation                                        │───┘  │
│  │  ┌──────────────────┐    ┌──────────────────┐                     │      │
│  │  │    Confluence    │    │      Jira        │                     │      │
│  │  │  - Tech Docs     │    │  - Comment       │                     │      │
│  │  │  - Runbooks      │    │  - Link PR       │                     │      │
│  │  └──────────────────┘    └──────────────────┘                     │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Related Commands

### Jira Commands
- `/jira:status` - Check current work session status
- `/jira:sync` - Sync changes with Jira
- `/jira:pr` - Create pull request
- `/jira:commit` - Create smart commit

### Confluence Commands
- `/confluence-publish` - Publish tech doc to Confluence
- `/atlassian-sync` - Sync with Jira/Confluence

### GitHub Commands
- Create PR with quality report via gh cli
- Update commit status via gh api
- Trigger workflows via gh workflow run

### Quality Gate Commands (from Curator)
- `/quality-check` - Run all 5 quality gates
- `/quality-fix` - Auto-fix issues where possible
- `/coverage-check` - Check test coverage (80% min)
- `/security-scan` - Run security vulnerability scan
- `/complexity-audit` - Check code complexity
- `/dependency-audit` - Check dependency health

## Quality Gate Thresholds

| Gate | Metric | Threshold |
|------|--------|-----------|
| Static Analysis | Errors | 0 |
| Test Coverage | Line Coverage | ≥ 80% |
| Security Scanner | Critical/High CVEs | 0 |
| Complexity | Cyclomatic | ≤ 10 |
| Complexity | Cognitive | ≤ 15 |
| Dependencies | Critical Vulns | 0 |
