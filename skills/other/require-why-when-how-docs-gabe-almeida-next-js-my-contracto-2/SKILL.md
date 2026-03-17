---
name: require-why-when-how-docs
description: Require comprehensive WHY/WHEN/HOW documentation for all functions. Apply when writing functions, classes, or complex logic to explain purpose, usage context, and implementation approach.
---

# WHY/WHEN/HOW Documentation Requirements

**CRITICAL: EVERY function, class, and complex logic block MUST have comprehensive documentation.**

This is NON-NEGOTIABLE. Code without proper documentation will be rejected.

## Why This Exists

Undocumented code:
- Forces readers to reverse-engineer intent
- Makes onboarding painful
- Leads to bugs from misunderstanding
- Becomes unmaintainable over time

**Good documentation explains the reasoning (WHY), context (WHEN), and approach (HOW).**

## When to Apply

Document EVERY:
- Public function/method
- Private function with complex logic
- Class or component
- Complex algorithm or business rule
- Non-obvious code patterns

## How It Works

### Required Format

```typescript
/**
 * WHY: [Why does this exist? What problem does it solve? Business reason?]
 * WHEN: [When should this be called? What triggers it? What conditions?]
 * HOW: [How does it work? Algorithm? Steps? Approach?]
 *
 * @param {Type} paramName - Description
 * @returns {Type} Description
 * @throws {ErrorType} When and why
 *
 * @example
 * // Usage example showing typical use case
 * const result = functionName(param1, param2);
 *
 * @see relatedFunction - Link to related functionality
 */
```

### The Three Required Sections

#### 1. WHY (Purpose & Business Context)

Answers:
- Why does this code exist?
- What problem does it solve?
- What's the business/product reason?
- What would break without it?

**Example:**
```typescript
/**
 * WHY: Users need to authenticate to access protected resources. This validates
 *      credentials and generates a JWT token for subsequent authenticated requests.
 *      Without this, anyone could access user data.
 */
```

#### 2. WHEN (Usage Context & Triggers)

Answers:
- When should this be called?
- What triggers this function?
- Under what conditions should it run?
- What preconditions must be met?

**Example:**
```typescript
/**
 * WHEN: Called by POST /auth/login endpoint when user submits login form.
 *       Should ONLY be called after rate limiting checks pass.
 *       Requires valid email and non-empty password.
 */
```

#### 3. HOW (Implementation Approach)

Answers:
- How does it work?
- What's the algorithm/approach?
- What are the main steps?
- What side effects occur?

**Example:**
```typescript
/**
 * HOW:
 *   1. Validates email format
 *   2. Finds user in database by email
 *   3. Compares provided password with stored bcrypt hash
 *   4. If match, generates JWT with user ID and role
 *   5. Returns token with 24-hour expiration
 *   Side effects: Updates last_login timestamp in database
 */
```

## Complete Examples

### Example 1: Service Function

```typescript
/**
 * WHY: Users need to authenticate to access protected resources. This validates
 *      credentials and generates a JWT token for subsequent authenticated requests.
 *
 * WHEN: Called by the POST /auth/login endpoint when a user submits login form.
 *       Should ONLY be called after rate limiting checks pass.
 *
 * HOW:
 *   1. Validates email format
 *   2. Finds user in database by email
 *   3. Compares provided password with stored bcrypt hash
 *   4. If match, generates JWT with user ID and role
 *   5. Returns token with 24-hour expiration
 *   Side effects: Updates last_login timestamp
 *
 * @param {string} email - User's email address
 * @param {string} password - Plain text password (will be hashed for comparison)
 * @returns {Promise<AuthToken>} JWT token and user info
 * @throws {UnauthorizedError} When credentials are invalid
 * @throws {ValidationError} When email format is invalid
 *
 * @example
 * const token = await authService.login('user@example.com', 'password123');
 * // Returns: { token: 'jwt...', user: { id, email, role } }
 *
 * @see TokenService.generateToken - Handles JWT creation
 * @see UserRepository.updateLastLogin - Updates login timestamp
 */
async login(email: string, password: string): Promise<AuthToken> {
  // Implementation
}
```

### Example 2: Complex Utility Function

```typescript
/**
 * WHY: Phone numbers need consistent formatting for storage and comparison.
 *      Users enter phone numbers in many formats (with/without country code,
 *      with spaces, dashes, parentheses) but we need E.164 format for Twilio.
 *
 * WHEN: Called before saving phone numbers to database or sending to Twilio API.
 *       Use this anytime you receive phone input from users.
 *
 * HOW:
 *   1. Remove all non-digit characters (spaces, dashes, parentheses)
 *   2. If starts with +1, keep it
 *   3. If starts with 1, add +
 *   4. If 10 digits with no prefix, add +1
 *   5. Validate final format is E.164 (+1XXXXXXXXXX)
 *   6. Return formatted or throw if invalid
 *
 * @param {string} phone - Phone number in any common format
 * @returns {string} E.164 formatted phone number (+1XXXXXXXXXX)
 * @throws {ValidationError} When phone number cannot be normalized
 *
 * @example
 * normalizePhoneNumber('(555) 123-4567')  // Returns: '+15551234567'
 * normalizePhoneNumber('555-123-4567')    // Returns: '+15551234567'
 * normalizePhoneNumber('+1 555 123 4567') // Returns: '+15551234567'
 *
 * @see validatePhoneNumber - Validates format without normalization
 */
function normalizePhoneNumber(phone: string): string {
  // Implementation
}
```

### Example 3: React Component

```typescript
/**
 * WHY: Workflow system requires agents to select phone numbers for outbound calls.
 *      This dropdown shows available phone numbers from the contact group associated
 *      with the workflow, preventing manual entry errors and ensuring valid numbers.
 *
 * WHEN: Use in workflow builder when step type is "outbound_call".
 *       Dropdown populates with phone numbers from workflow's contact group.
 *       If workflow has no contact group, dropdown is disabled with helper text.
 *
 * HOW:
 *   1. Loads workflow from context
 *   2. Fetches contact group associated with workflow
 *   3. Gets all phone numbers from contacts in that group
 *   4. Formats numbers as dropdown options (name + number)
 *   5. Handles selection and updates step config
 *   6. Shows loading/error/empty states appropriately
 *
 * @param {object} props - Component props
 * @param {string} props.workflowId - ID of workflow being edited
 * @param {string} props.stepId - ID of step being configured
 * @param {Function} props.onChange - Callback when number selected
 * @returns {JSX.Element} Phone number dropdown component
 *
 * @example
 * <PhoneNumberDropdown
 *   workflowId="wf_123"
 *   stepId="step_456"
 *   onChange={(phoneNumber) => console.log('Selected:', phoneNumber)}
 * />
 *
 * @see WorkflowContext - Provides workflow data
 * @see useContactGroup - Hook for fetching contact group
 */
export function PhoneNumberDropdown({ workflowId, stepId, onChange }: Props) {
  // Implementation
}
```

### Example 4: Complex Algorithm

```typescript
/**
 * WHY: Race conditions occur when agents mark status as "available" while
 *      system is assigning them a call. This leads to double-assignments
 *      where agent gets 2+ calls simultaneously. This debouncer prevents
 *      rapid status changes during critical assignment window.
 *
 * WHEN: Called whenever agent status changes (via UI button or realtime update).
 *       Waits 2 seconds before applying status to allow assignment to complete.
 *       If another status change arrives during wait, restarts timer.
 *
 * HOW:
 *   1. When status change requested, cancel any pending timers
 *   2. Start new 2-second timer with new status value
 *   3. If timer completes without interruption, apply status
 *   4. If new status arrives during timer, cancel and restart
 *   5. Special case: "on_call" status applies immediately (no debounce)
 *      because it indicates active call state that must be immediate
 *
 * @param {AgentStatus} newStatus - Status to apply
 * @param {Function} callback - Called when debounced status should apply
 * @param {number} delay - Debounce delay in ms (default 2000)
 * @returns {Function} Cleanup function to cancel pending timer
 *
 * @example
 * const cleanup = debounceStatusChange(
 *   'available',
 *   (status) => updateAgentStatus(status),
 *   2000
 * );
 * // If another change comes in 1 second, first change is cancelled
 *
 * @see AgentStatusContext - Manages agent status state
 * @see handleWorkflowAssignment - Where race condition originally occurred
 */
function debounceStatusChange(
  newStatus: AgentStatus,
  callback: (status: AgentStatus) => void,
  delay: number = 2000
): () => void {
  // Implementation
}
```

## Documentation Levels

### Level 1: Simple Functions (Still need WHY/WHEN/HOW!)

Even simple functions need all three sections, just shorter:

```typescript
/**
 * WHY: Consistent uppercase formatting for display names
 * WHEN: Use when formatting names for UI display
 * HOW: Converts to uppercase using String.toUpperCase()
 *
 * @param {string} name - Name to format
 * @returns {string} Uppercase name
 */
function formatName(name: string): string {
  return name.toUpperCase();
}
```

### Level 2: Complex Functions (Detailed WHY/WHEN/HOW)

Complex functions need detailed step-by-step HOW:

```typescript
/**
 * WHY: Workflow execution engine needs to determine next step based on
 *      current step outcome and branching logic. Supports conditional
 *      flows, parallel branches, and loop-backs.
 *
 * WHEN: Called after each workflow step completes.
 *       Requires step outcome (success/failure) and step config.
 *       Returns next step ID or null if workflow should end.
 *
 * HOW:
 *   1. Check if current step has conditional branches
 *   2. If yes, evaluate condition against step outcome
 *   3. If condition true, follow "then" branch
 *   4. If condition false, follow "else" branch
 *   5. If no conditions, check if parallel step exists
 *   6. If yes, check if all parallel steps completed
 *   7. If not all complete, return null (wait for others)
 *   8. If all complete, proceed to next step
 *   9. Check if next step is loop-back (revisits previous step)
 *   10. If yes, increment loop counter and check max iterations
 *   11. Return next step ID or null if end reached
 *
 * @param {WorkflowStep} currentStep - Step that just completed
 * @param {StepOutcome} outcome - Result of step execution
 * @param {WorkflowState} state - Current workflow state
 * @returns {string | null} Next step ID or null to end workflow
 *
 * @see WorkflowExecutor - Orchestrates workflow execution
 * @see evaluateCondition - Evaluates branch conditions
 */
```

## When Documentation is Missing

If you encounter undocumented code:

1. **Flag it**: "⚠️ This function lacks WHY/WHEN/HOW documentation"
2. **Don't proceed**: Ask for clarification before editing
3. **Document as you understand it**: Add docs based on your analysis
4. **Mark uncertainty**: Use `// TODO: Verify this understanding` if unsure

## Enforcement

The code-quality-auditor will:
- ✅ Check for WHY/WHEN/HOW sections
- ✅ Reject functions without documentation
- ✅ Verify documentation is comprehensive (not just placeholders)
- ✅ Check that documentation matches implementation

## Quick Checklist

- [ ] Every function has documentation
- [ ] Documentation includes WHY section
- [ ] Documentation includes WHEN section
- [ ] Documentation includes HOW section
- [ ] Complex HOW sections have numbered steps
- [ ] Examples provided for public APIs
- [ ] Parameters and returns documented
- [ ] Throws documented if applicable
