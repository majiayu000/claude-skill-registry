---
name: rn-state-flows
description: Complex multi-step operations in React Native. Use when implementing flows with multiple async steps, state machine patterns, or debugging flow ordering issues.
---

# Complex State Flows

## Problem Statement

Multi-step operations with dependencies between steps are prone to ordering bugs, missing preconditions, and untested edge cases. Even without a formal state machine library, thinking in states and transitions prevents bugs.

---

## Pattern: State Machine Thinking

**Problem:** Complex flows have implicit states that aren't modeled, leading to invalid transitions.

**Example - Retake flow states:**

```
IDLE → LOADING_COMPLETED → ENABLING_RETAKE → CLEARING_ANSWERS → READY → ANSWERING → MERGING → SUBMITTING → COMPLETE
                                                                                                              ↓
                                                                                                           ERROR
```

**Each transition should have:**

1. **Preconditions** - What must be true before this step
2. **Action** - What happens during this step
3. **Postconditions** - What must be true after this step
4. **Error handling** - What to do if this step fails

```typescript
// Document the flow explicitly
/*
 * RETAKE FLOW
 * 
 * State: IDLE
 * Precondition: assessment exists
 * Action: loadCompletedAssessmentAnswers
 * Postcondition: completedAssessmentAnswers populated
 * 
 * State: LOADING_COMPLETED
 * Precondition: completedAssessmentAnswers loaded
 * Action: enableSkillAreaRetake
 * Postcondition: skillArea in retakeAreas set
 * 
 * State: ENABLING_RETAKE
 * Precondition: skillArea in retakeAreas
 * Action: clearSkillAreaAnswers
 * Postcondition: existing answers for skillArea removed
 * 
 * ... continue for each state
 */
```

---

## Pattern: Explicit Flow Implementation

**Problem:** Flow logic scattered across multiple functions, hard to verify ordering.

```typescript
// WRONG - implicit flow, easy to miss steps or misordering
async function startRetake(assessmentId: string, skillArea: string) {
  loadCompletedAssessmentAnswers(assessmentId); // Missing await!
  await enableSkillAreaRetake(skillArea);
  await clearSkillAreaAnswers(skillArea);
}

// CORRECT - explicit flow with validation
async function startRetake(assessmentId: string, skillArea: string) {
  const flowId = `retake-${Date.now()}`;
  logger.info(`[${flowId}] Starting retake flow`, { assessmentId, skillArea });
  
  // Step 1: Load completed answers
  await loadCompletedAssessmentAnswers(assessmentId);
  const completedAnswers = useStore.getState().completedAssessmentAnswers;
  if (Object.keys(completedAnswers).length === 0) {
    throw new Error(`[${flowId}] Failed to load completed answers`);
  }
  logger.debug(`[${flowId}] Loaded ${Object.keys(completedAnswers).length} answers`);
  
  // Step 2: Enable retake for skill area
  await enableSkillAreaRetake(skillArea);
  const retakeAreas = useStore.getState().retakeAreas;
  if (!retakeAreas.has(skillArea)) {
    throw new Error(`[${flowId}] Failed to enable retake for ${skillArea}`);
  }
  logger.debug(`[${flowId}] Enabled retake for ${skillArea}`);
  
  // Step 3: Clear existing answers
  await clearSkillAreaAnswers(skillArea);
  logger.debug(`[${flowId}] Cleared answers for ${skillArea}`);
  
  logger.info(`[${flowId}] Retake flow completed`);
}
```

---

## Pattern: Flow Object

**Problem:** Long async functions with many steps become unwieldy.

```typescript
interface FlowStep<TContext> {
  name: string;
  execute: (context: TContext) => Promise<void>;
  validate?: (context: TContext) => void;  // Postcondition check
}

interface RetakeContext {
  assessmentId: string;
  skillArea: string;
  flowId: string;
}

const retakeSteps: FlowStep<RetakeContext>[] = [
  {
    name: 'loadCompletedAnswers',
    execute: async (ctx) => {
      await loadCompletedAssessmentAnswers(ctx.assessmentId);
    },
    validate: (ctx) => {
      const answers = useStore.getState().completedAssessmentAnswers;
      if (Object.keys(answers).length === 0) {
        throw new Error(`[${ctx.flowId}] No completed answers loaded`);
      }
    },
  },
  {
    name: 'enableRetake',
    execute: async (ctx) => {
      await enableSkillAreaRetake(ctx.skillArea);
    },
    validate: (ctx) => {
      const retakeAreas = useStore.getState().retakeAreas;
      if (!retakeAreas.has(ctx.skillArea)) {
        throw new Error(`[${ctx.flowId}] Retake not enabled for ${ctx.skillArea}`);
      }
    },
  },
  {
    name: 'clearAnswers',
    execute: async (ctx) => {
      await clearSkillAreaAnswers(ctx.skillArea);
    },
  },
];

async function executeFlow<TContext>(
  steps: FlowStep<TContext>[],
  context: TContext,
  flowName: string
) {
  const flowId = `${flowName}-${Date.now()}`;
  logger.info(`[${flowId}] Starting flow`, context);
  
  for (const step of steps) {
    logger.debug(`[${flowId}] Executing: ${step.name}`);
    try {
      await step.execute(context);
      if (step.validate) {
        step.validate(context);
      }
      logger.debug(`[${flowId}] Completed: ${step.name}`);
    } catch (error) {
      logger.error(`[${flowId}] Failed at: ${step.name}`, { error: error.message });
      throw error;
    }
  }
  
  logger.info(`[${flowId}] Flow completed`);
}

// Usage
await executeFlow(retakeSteps, { assessmentId, skillArea, flowId }, 'retake');
```

---

## Pattern: Flow State Tracking

**Problem:** Components need to know current flow state for UI feedback.

```typescript
type RetakeFlowState =
  | { status: 'idle' }
  | { status: 'loading'; step: string }
  | { status: 'ready' }
  | { status: 'answering'; answeredCount: number }
  | { status: 'submitting' }
  | { status: 'complete' }
  | { status: 'error'; message: string; step: string };

const useRetakeStore = create<{
  flowState: RetakeFlowState;
  setFlowState: (state: RetakeFlowState) => void;
}>((set) => ({
  flowState: { status: 'idle' },
  setFlowState: (flowState) => set({ flowState }),
}));

async function startRetake(assessmentId: string, skillArea: string) {
  const { setFlowState } = useRetakeStore.getState();
  
  try {
    setFlowState({ status: 'loading', step: 'loadingAnswers' });
    await loadCompletedAssessmentAnswers(assessmentId);
    
    setFlowState({ status: 'loading', step: 'enablingRetake' });
    await enableSkillAreaRetake(skillArea);
    
    setFlowState({ status: 'loading', step: 'clearingAnswers' });
    await clearSkillAreaAnswers(skillArea);
    
    setFlowState({ status: 'ready' });
  } catch (error) {
    setFlowState({ 
      status: 'error', 
      message: error.message,
      step: useRetakeStore.getState().flowState.step,
    });
  }
}

// Component usage
function RetakeScreen() {
  const flowState = useRetakeStore((s) => s.flowState);
  
  if (flowState.status === 'loading') {
    return <Loading step={flowState.step} />;
  }
  
  if (flowState.status === 'error') {
    return <Error message={flowState.message} step={flowState.step} />;
  }
  
  // ... render based on state
}
```

---

## Pattern: Integration Testing Flows

**Problem:** Unit tests for individual functions don't catch flow-level bugs.

```typescript
describe('Retake Flow', () => {
  beforeEach(() => {
    useAssessmentStore.getState()._reset();
  });

  it('persists answers through complete retake flow', async () => {
    const assessmentId = 'test-assessment';
    const skillArea = 'fundamentals';
    const store = useAssessmentStore;
    
    // Setup: Simulate existing completed assessment
    store.getState().setCompletedAnswers(assessmentId, mockCompletedAnswers);
    
    // Execute full flow
    await store.getState().loadCompletedAssessmentAnswers(assessmentId);
    
    // Verify postcondition
    expect(Object.keys(store.getState().completedAssessmentAnswers).length)
      .toBeGreaterThan(0);
    
    await store.getState().enableSkillAreaRetake(skillArea);
    
    // Verify postcondition
    expect(store.getState().retakeAreas.has(skillArea)).toBe(true);
    
    await store.getState().clearSkillAreaAnswers(skillArea);
    
    // Simulate user answering
    await store.getState().saveAnswer('q1', 4);
    
    // THE CRITICAL CHECK - does the answer persist?
    expect(store.getState().userAnswers['q1']).toBe(4);
    
    // Complete flow
    await store.getState().submitRetake(assessmentId);
    
    // Verify final state
    expect(store.getState().flowState.status).toBe('complete');
  });

  it('handles error at each step', async () => {
    // Test error handling at step 1
    mockApi.loadAnswers.mockRejectedValueOnce(new Error('Network error'));
    
    await expect(
      store.getState().startRetake(assessmentId, skillArea)
    ).rejects.toThrow('Network error');
    
    expect(store.getState().flowState.status).toBe('error');
    expect(store.getState().flowState.step).toBe('loadingAnswers');
  });
});
```

---

## Pattern: Flow Documentation

Document complex flows with diagrams for team understanding:

```markdown
## Retake Flow

### Happy Path

```
┌─────────┐     ┌──────────────┐     ┌───────────────┐     ┌───────────────┐
│  Start  │────▶│ Load Answers │────▶│ Enable Retake │────▶│ Clear Answers │
└─────────┘     └──────────────┘     └───────────────┘     └───────────────┘
                       │                     │                     │
                       ▼                     ▼                     ▼
                 Postcondition:        Postcondition:         Postcondition:
                 answers.length > 0    retakeAreas.has(x)    cleared for area

                                                                   │
                                                                   ▼
┌──────────┐     ┌─────────┐     ┌───────────────┐     ┌──────────────────┐
│ Complete │◀────│ Merge   │◀────│ User Answers  │◀────│ Ready for Input  │
└──────────┘     └─────────┘     └───────────────┘     └──────────────────┘
```

### Error States

Any step can fail → transition to ERROR state with step context.
From ERROR: user can retry (back to IDLE) or exit.
```

---

## Checklist: Designing Complex Flows

Before implementing:

- [ ] Sketch state diagram (even on paper)
- [ ] Identify all states, including error states
- [ ] Document preconditions for each transition
- [ ] Document postconditions to verify
- [ ] Plan how to surface state to UI

During implementation:

- [ ] Verify preconditions before each step
- [ ] Validate postconditions after each step
- [ ] Log state transitions with flow ID
- [ ] Handle errors at each step with context
- [ ] Surface flow state for UI feedback

After implementation:

- [ ] Integration test for happy path
- [ ] Integration test for error at each step
- [ ] Verify logs are sufficient for debugging
- [ ] Document flow for team

---

## When to Use XState

Consider XState when:

- Flow has > 6 states
- Complex branching/parallel states
- Need visualization/debugging tools
- State machine is shared across team

For simpler flows, explicit steps with validation (as shown above) are often sufficient and more readable.
