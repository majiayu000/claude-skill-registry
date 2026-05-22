---
name: react-state-flows
description: Complex multi-step operations in React. Use when implementing flows with multiple async steps, state machine patterns, or debugging flow ordering issues. Works for both React web and React Native.
---

# Complex State Flows

## Problem Statement

Multi-step operations with dependencies between steps are prone to ordering bugs, missing preconditions, and untested edge cases. Even without a formal state machine library, thinking in states and transitions prevents bugs.

---

## Pattern: State Machine Thinking

**Problem:** Complex flows have implicit states that aren't modeled, leading to invalid transitions.

**Example - Checkout flow states:**

```
IDLE → VALIDATING → PROCESSING_PAYMENT → CONFIRMING → COMPLETE
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
 * CHECKOUT FLOW
 *
 * State: IDLE
 * Precondition: cart exists with items
 * Action: validateCart
 * Postcondition: cart validated, prices confirmed
 *
 * State: VALIDATING
 * Precondition: cart validated
 * Action: processPayment
 * Postcondition: payment authorized
 *
 * State: PROCESSING_PAYMENT
 * Precondition: payment authorized
 * Action: confirmOrder
 * Postcondition: order created, confirmation number assigned
 *
 * ... continue for each state
 */
```

---

## Pattern: Explicit Flow Implementation

**Problem:** Flow logic scattered across multiple functions, hard to verify ordering.

```typescript
// WRONG - implicit flow, easy to miss steps or misordering
async function checkout(cartId: string) {
  validateCart(cartId);              // Missing await!
  await processPayment(cartId);
  await confirmOrder(cartId);
}

// CORRECT - explicit flow with validation
async function checkout(cartId: string) {
  const flowId = `checkout-${Date.now()}`;
  logger.info(`[${flowId}] Starting checkout flow`, { cartId });

  // Step 1: Validate cart
  await validateCart(cartId);
  const cart = useStore.getState().cart;
  if (!cart.validated) {
    throw new Error(`[${flowId}] Cart validation failed`);
  }
  logger.debug(`[${flowId}] Cart validated`);

  // Step 2: Process payment
  await processPayment(cartId);
  const payment = useStore.getState().payment;
  if (!payment.authorized) {
    throw new Error(`[${flowId}] Payment authorization failed`);
  }
  logger.debug(`[${flowId}] Payment processed`);

  // Step 3: Confirm order
  await confirmOrder(cartId);
  logger.info(`[${flowId}] Checkout flow completed`);
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

interface CheckoutContext {
  cartId: string;
  flowId: string;
}

const checkoutSteps: FlowStep<CheckoutContext>[] = [
  {
    name: 'validateCart',
    execute: async (ctx) => {
      await validateCart(ctx.cartId);
    },
    validate: (ctx) => {
      const cart = useStore.getState().cart;
      if (!cart.validated) {
        throw new Error(`[${ctx.flowId}] Cart not validated`);
      }
    },
  },
  {
    name: 'processPayment',
    execute: async (ctx) => {
      await processPayment(ctx.cartId);
    },
    validate: (ctx) => {
      const payment = useStore.getState().payment;
      if (!payment.authorized) {
        throw new Error(`[${ctx.flowId}] Payment not authorized`);
      }
    },
  },
  {
    name: 'confirmOrder',
    execute: async (ctx) => {
      await confirmOrder(ctx.cartId);
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
await executeFlow(checkoutSteps, { cartId, flowId }, 'checkout');
```

---

## Pattern: Flow State Tracking

**Problem:** Components need to know current flow state for UI feedback.

```typescript
type CheckoutFlowState =
  | { status: 'idle' }
  | { status: 'loading'; step: string }
  | { status: 'ready' }
  | { status: 'processing'; step: string }
  | { status: 'complete'; orderId: string }
  | { status: 'error'; message: string; step: string };

const useCheckoutStore = create<{
  flowState: CheckoutFlowState;
  setFlowState: (state: CheckoutFlowState) => void;
}>((set) => ({
  flowState: { status: 'idle' },
  setFlowState: (flowState) => set({ flowState }),
}));

async function checkout(cartId: string) {
  const { setFlowState } = useCheckoutStore.getState();

  try {
    setFlowState({ status: 'processing', step: 'validating' });
    await validateCart(cartId);

    setFlowState({ status: 'processing', step: 'payment' });
    await processPayment(cartId);

    setFlowState({ status: 'processing', step: 'confirming' });
    const order = await confirmOrder(cartId);

    setFlowState({ status: 'complete', orderId: order.id });
  } catch (error) {
    setFlowState({
      status: 'error',
      message: error.message,
      step: useCheckoutStore.getState().flowState.step,
    });
  }
}

// Component usage
function CheckoutScreen() {
  const flowState = useCheckoutStore((s) => s.flowState);

  if (flowState.status === 'processing') {
    return <Loading step={flowState.step} />;
  }

  if (flowState.status === 'error') {
    return <Error message={flowState.message} step={flowState.step} />;
  }

  if (flowState.status === 'complete') {
    return <Confirmation orderId={flowState.orderId} />;
  }

  // ... render based on state
}
```

---

## Pattern: Integration Testing Flows

**Problem:** Unit tests for individual functions don't catch flow-level bugs.

```typescript
describe('Checkout Flow', () => {
  beforeEach(() => {
    useCheckoutStore.getState()._reset();
  });

  it('completes full checkout flow', async () => {
    const cartId = 'test-cart';
    const store = useCheckoutStore;

    // Setup: Add items to cart
    store.getState().addItem({ id: 'item-1', price: 100 });

    // Execute full flow
    await store.getState().checkout(cartId);

    // Verify final state
    expect(store.getState().flowState.status).toBe('complete');
    expect(store.getState().flowState.orderId).toBeDefined();
  });

  it('handles payment failure gracefully', async () => {
    // Mock payment to fail
    mockPaymentApi.mockRejectedValueOnce(new Error('Card declined'));

    await expect(
      store.getState().checkout(cartId)
    ).rejects.toThrow('Card declined');

    expect(store.getState().flowState.status).toBe('error');
    expect(store.getState().flowState.step).toBe('payment');
  });
});
```

---

## Pattern: Flow Documentation

Document complex flows with diagrams for team understanding:

```markdown
## Checkout Flow

### Happy Path

```
┌─────────┐     ┌──────────────┐     ┌─────────────────┐     ┌─────────────┐
│  Start  │────▶│ Validate Cart│────▶│ Process Payment │────▶│ Confirm     │
└─────────┘     └──────────────┘     └─────────────────┘     └─────────────┘
                       │                     │                      │
                       ▼                     ▼                      ▼
                 Postcondition:        Postcondition:          Postcondition:
                 cart.validated        payment.authorized      order.created
                                                                    │
                                                                    ▼
                                                              ┌──────────┐
                                                              │ Complete │
                                                              └──────────┘
```

### Error States

Any step can fail → transition to ERROR state with step context.
From ERROR: user can retry or exit.
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
