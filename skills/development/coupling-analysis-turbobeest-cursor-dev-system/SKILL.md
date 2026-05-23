---
activation_code: COUPLING_ANALYSIS_V1
phase: 5.2
prerequisites:
  - tasks.json
outputs:
  - .signals/coupling-analyzed.json
optional: true
description: |
  OPTIONAL: Analyzes TaskMaster subtasks to determine if they are tightly coupled
  (share code/models) or loosely coupled (independent modules). This analysis provides
  RECOMMENDATIONS for implementation order only - it does NOT affect proposal creation.

  All proposals are created 1-per-subtask regardless of coupling. Coupling analysis
  only recommends whether to implement proposals sequentially (tight coupling) or in
  parallel (loose coupling) to avoid merge conflicts.

  Activation trigger: [ACTIVATE:COUPLING_ANALYSIS_V1] (optional)
---

# Coupling Analysis Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:COUPLING_ANALYSIS_V1]
```

This occurs when:
- tasks.json is created (automatic transition from Phase 5)
- User runs 'task-master show' command
- User asks about task coupling or parallelization
- Preparing for Phase 6 (OpenSpec generation)

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-5-task-2` for coupling analysis:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 5 2
cd ./worktrees/phase-5-task-2

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# Coupling analysis with worktree validation
```

### Worktree Safety Measures
1. **Read-only analysis**: No modifications to source code during analysis
2. **Isolated output**: Coupling results stored within worktree boundaries
3. **Merge validation**: Results merged to main only after validation
4. **Contamination prevention**: No cross-worktree analysis dependencies

## What This Skill Does (OPTIONAL - Informational Only)

Automatically analyzes subtask structure to provide **implementation order recommendations**:
- **Tightly Coupled** → Implement proposals sequentially (prevent merge conflicts)
- **Loosely Coupled** → Implement proposals in parallel (safe for 3-4x speedup)
- Clear rationale with file paths and shared resource analysis
- **IMPORTANT**: Does NOT affect proposal creation (always 1 proposal per subtask)
- **IMPORTANT**: Only provides implementation hints for Phase 7
- **NEW**: Worktree-based isolation for safe analysis

### 1. Analyzes Subtask Structure
Examines:
- Task title and description
- Subtask descriptions (if any)
- File paths mentioned
- Architecture components
- Dependencies between subtasks
- Shared resources (models, utilities, services)

### 2. Determines Coupling Type (For Implementation Order)

**ALL subtasks get 1 proposal each. Coupling only affects implementation order:**

#### TIGHTLY COUPLED
```
Subtasks share significant code/data structures
→ Proposals: ONE per subtask (standard)
→ Implementation Recommendation: Sequential
→ Reason: Prevent merge conflicts on shared code
```

**Indicators:**
- Share same model/class (e.g., User, Product, Order)
- Modify same files
- Use same database tables
- Share utility functions
- Sequential dependencies (2.1 → 2.2 → 2.3)
- Common business logic

**Example:**
- Master Task: User Authentication (3 subtasks)
- All modify `User.ts` model
- Create 3 proposals, implement sequentially (avoid conflicts)

#### LOOSELY COUPLED
```
Subtasks are independent modules
→ Proposals: ONE per subtask (standard)
→ Implementation Recommendation: Parallel
→ Reason: Safe to implement simultaneously (3-4x speedup)
```

**Indicators:**
- Touch completely different files
- No shared models/classes
- Independent test suites
- No dependencies between subtasks
- Different architecture components
- Can be tested in isolation

**Example:**
- Master Task: API Endpoints (3 subtasks)
- Each touches different controller file
- Create 3 proposals, implement in parallel (safe speedup)

### 3. Provides Recommendation

**Output Format:**
```
COUPLING ANALYSIS: Task #[X] - [Title]
==================================================

SUBTASKS: [count]
├─ [X.1]: [title]
├─ [X.2]: [title]
└─ [X.3]: [title]

SHARED RESOURCES:
[List shared models, files, utilities]
OR
[None - completely independent]

COUPLING TYPE: [TIGHTLY COUPLED / LOOSELY COUPLED / NO SUBTASKS]

RATIONALE:
[1-2 sentence explanation of why]

PROPOSAL CREATION (Standard):
├─ OpenSpec Proposals: ONE per subtask (always)
└─ Proposal Name(s): [suggest names]

RECOMMENDED IMPLEMENTATION ORDER:
├─ Strategy: [Sequential / Parallel]
├─ Reason: [Prevent conflicts / Safe speedup]
└─ Estimated Time: [time estimate]

IMPLEMENTATION IMPACT:
├─ Sequential: [X] minutes total
└─ Parallel (if loosely coupled): [Y] minutes total
```

## Analysis Decision Tree

```
START: Analyze Task #X
│
├─ Has subtasks?
│  ├─ NO → "NO SUBTASKS" → One proposal
│  └─ YES → Continue
│
├─ Check: Same model/class mentioned?
│  ├─ YES → "TIGHTLY COUPLED" → One proposal
│  └─ NO → Continue
│
├─ Check: Same files modified?
│  ├─ YES → "TIGHTLY COUPLED" → One proposal
│  └─ NO → Continue
│
├─ Check: Sequential dependencies?
│  ├─ YES → "TIGHTLY COUPLED" → One proposal
│  └─ NO → Continue
│
├─ Check: Share utilities/services?
│  ├─ YES → "TIGHTLY COUPLED" → One proposal
│  └─ NO → Continue
│
└─ All checks passed
   → "LOOSELY COUPLED" → One proposal per subtask
```

## Pattern Recognition

### Pattern 1: CRUD Operations on Same Entity
```
Task: Implement User Management
├─ 3.1: Create user endpoint
├─ 3.2: Update user endpoint
├─ 3.3: Delete user endpoint
└─ 3.4: Get user endpoint

Analysis: All share User model
Result: TIGHTLY COUPLED
Proposal: One proposal "user-management" with 4 requirements
```

### Pattern 2: Authentication Features
```
Task: User Authentication
├─ 3.1: Create user model
├─ 3.2: Registration endpoint
├─ 3.3: Login endpoint
└─ 3.4: JWT middleware

Analysis: All depend on User model created in 3.1
Result: TIGHTLY COUPLED
Proposal: One proposal "user-authentication"
```

### Pattern 3: Independent API Refactors
```
Task: Refactor API Endpoints
├─ 5.1: Refactor users endpoint (src/api/users.js)
├─ 5.2: Refactor products endpoint (src/api/products.js)
└─ 5.3: Refactor orders endpoint (src/api/orders.js)

Analysis: Different files, no shared code
Result: LOOSELY COUPLED
Proposals: 
  - refactor-users-endpoint
  - refactor-products-endpoint
  - refactor-orders-endpoint
```

### Pattern 4: Independent Service Integrations
```
Task: External Service Integrations
├─ 7.1: Stripe payment integration
├─ 7.2: SendGrid email integration
├─ 7.3: Twilio SMS integration

Analysis: Completely independent services
Result: LOOSELY COUPLED
Proposals:
  - stripe-payment-integration
  - sendgrid-email-integration
  - twilio-sms-integration
```

### Pattern 5: UI Components with Shared State
```
Task: Shopping Cart UI
├─ 4.1: Cart display component
├─ 4.2: Add to cart button
├─ 4.3: Remove from cart button
└─ 4.4: Cart state management

Analysis: All share CartState, CartContext
Result: TIGHTLY COUPLED
Proposal: One proposal "shopping-cart-ui"
```

## File Path Analysis

**Extract file paths from task descriptions:**

### Tightly Coupled Example:
```
Subtasks mention:
- src/models/User.js (shared)
- src/services/auth.service.js (uses User)
- src/controllers/auth.controller.js (uses User)
- src/middleware/auth.middleware.js (uses User)

Result: TIGHTLY COUPLED (all need User model)
```

### Loosely Coupled Example:
```
Subtasks mention:
- src/api/users.js (independent)
- src/api/products.js (independent)
- src/api/orders.js (independent)

Result: LOOSELY COUPLED (no overlap)
```

## Parallelization Benefit Calculator

**When LOOSELY COUPLED:**
```
Sequential Time = Subtask1_Time + Subtask2_Time + Subtask3_Time
Parallel Time = MAX(Subtask1_Time, Subtask2_Time, Subtask3_Time)

Example:
├─ Subtask 1: 30 minutes
├─ Subtask 2: 30 minutes
└─ Subtask 3: 30 minutes

Sequential: 90 minutes
Parallel: 30 minutes (3x faster!)
```

**Include in analysis output:**
```
PARALLELIZATION BENEFIT:
├─ Sequential: 90 minutes
├─ Parallel: 30 minutes
└─ Speedup: 3x faster
```

## Edge Cases

### Edge Case 1: Mixed Coupling
```
Task: User Profile Features
├─ 6.1: Profile CRUD (uses User model)
├─ 6.2: Avatar upload (uses User model)
├─ 6.3: Email preferences (independent settings)
└─ 6.4: Notification preferences (independent settings)

Analysis: Subtasks 6.1-6.2 tightly coupled, 6.3-6.4 loosely coupled

Recommendation:
├─ Split task into two groups
├─ Group A (6.1-6.2): One proposal "user-profile-core"
└─ Group B (6.3-6.4): Separate proposals or combined "user-preferences"

Alternative: Keep as one proposal with 4 requirements
(Preference: Keep together if ≤4 subtasks)
```

### Edge Case 2: Ambiguous Task
```
Task: Implement Dashboard
├─ 8.1: Create dashboard component
├─ 8.2: Add charts
├─ 8.3: Add data tables

Analysis: Unclear if components share state

Recommendation:
├─ Default to TIGHTLY COUPLED (safer)
├─ Reason: UI components often share context/state
└─ Can refactor later if truly independent
```

### Edge Case 3: No Subtask Descriptions
```
Task: Complex Feature
├─ 10.1: [No description]
├─ 10.2: [No description]
└─ 10.3: [No description]

Analysis: Cannot determine coupling from titles alone

Recommendation:
├─ Request more details from TaskMaster
├─ Run: task-master show 10.1, 10.2, 10.3
├─ If still unclear: Default to TIGHTLY COUPLED
└─ Reason: Prefer cohesion over premature splitting
```

## Output Examples

### Example 1: Tightly Coupled
```
COUPLING ANALYSIS: Task #3 - User Authentication
==================================================

SUBTASKS: 4
├─ 3.1: Create user data model with password hashing
├─ 3.2: Implement registration endpoint with validation
├─ 3.3: Implement login endpoint with JWT generation
└─ 3.4: Create JWT validation middleware

SHARED RESOURCES:
├─ User model (src/models/User.js)
├─ AuthService (src/services/auth.service.js)
├─ JWT utilities (src/utils/jwt.utils.js)
└─ Database: users table

COUPLING TYPE: TIGHTLY COUPLED

RATIONALE:
All subtasks depend on the User model created in 3.1 and share
authentication utilities. Sequential implementation ensures consistency
in password hashing, JWT generation, and validation logic.

RECOMMENDED STRATEGY:
├─ OpenSpec Proposals: ONE proposal covering all subtasks
├─ Proposal Name: user-authentication
├─ Implementation: Sequential (maintain coherence)
└─ Estimated Time: 60-90 minutes total

PROPOSAL STRUCTURE:
user-authentication.md
├─ Requirement 1: User Data Model (TM 3.1)
├─ Requirement 2: Registration Endpoint (TM 3.2)
├─ Requirement 3: Login Endpoint (TM 3.3)
└─ Requirement 4: JWT Middleware (TM 3.4)
```

### Example 2: Loosely Coupled
```
COUPLING ANALYSIS: Task #5 - Refactor API Endpoints
==================================================

SUBTASKS: 3
├─ 5.1: Refactor users endpoint (src/api/users.js)
├─ 5.2: Refactor products endpoint (src/api/products.js)
└─ 5.3: Refactor orders endpoint (src/api/orders.js)

SHARED RESOURCES:
None - each subtask touches completely different files

COUPLING TYPE: LOOSELY COUPLED

RATIONALE:
Each subtask refactors a different API endpoint in a separate file
with no shared dependencies. They can be developed, tested, and
merged independently with zero conflicts.

RECOMMENDED STRATEGY:
├─ OpenSpec Proposals: THREE proposals (one per subtask)
├─ Proposal Names:
│  ├─ refactor-users-endpoint (TM 5.1)
│  ├─ refactor-products-endpoint (TM 5.2)
│  └─ refactor-orders-endpoint (TM 5.3)
├─ Implementation: PARALLEL (3x speedup!)
└─ Estimated Time: 30 minutes parallel (vs 90 sequential)

PARALLELIZATION BENEFIT:
├─ Sequential: 90 minutes (30 min × 3)
├─ Parallel: 30 minutes (3 simultaneous work streams)
└─ Speedup: 3x faster!

IMPLEMENTATION APPROACH:
Use Prompt 3C (Parallel Implementation):
├─ Create 3 git worktrees
├─ Launch 3 Claude Code instances
└─ Implement simultaneously
```

### Example 3: No Subtasks
```
COUPLING ANALYSIS: Task #2 - Configure Testing Framework
==================================================

SUBTASKS: None (single atomic task)

COUPLING TYPE: NO SUBTASKS

RATIONALE:
Single atomic task with no decomposition needed.

RECOMMENDED STRATEGY:
├─ OpenSpec Proposals: ONE proposal (or skip OpenSpec)
├─ Proposal Name: testing-framework-setup (optional)
├─ Implementation: Direct implementation
└─ Estimated Time: 15-20 minutes

NOTE: For simple setup tasks, OpenSpec proposal may be optional.
Task description and acceptance criteria may be sufficient.
```

## Integration with Phase 6 Workflow

**Phase 6 Step 1 Enhancement:**

```bash
# Original workflow:
task-master show 3

# With Coupling Analysis Skill active:
task-master show 3
# ↓ Skill automatically activates
# ↓ Analyzes task structure
# ↓ Provides coupling analysis

COUPLING ANALYSIS: Task #3 - [Title]
[Complete analysis as shown above]

# User receives recommendation immediately
# Can proceed with confidence to Step 2
```

## Common Mistakes to Avoid

### ❌ Mistake 1: Over-Splitting Tightly Coupled Tasks
```
Problem: Creating separate proposals for subtasks that share User model
Result: Inconsistent implementation, duplicate code, merge conflicts

Correct: One proposal with multiple requirements
```

### ❌ Mistake 2: Under-Splitting Loosely Coupled Tasks
```
Problem: One large proposal for completely independent refactors
Result: Sequential implementation, 3x slower, missed parallelization

Correct: Separate proposals, parallel implementation
```

### ❌ Mistake 3: Ignoring File Paths
```
Problem: Not reading file paths in task descriptions
Result: Wrong coupling decision

Correct: Extract and analyze file paths as primary indicator
```

### ❌ Mistake 4: Defaulting to "One Proposal Always"
```
Problem: Never recommending loosely coupled strategy
Result: Never leveraging parallelization benefits

Correct: Actively look for parallelization opportunities
```

## Confidence Levels

**Output confidence indicator:**

```
CONFIDENCE: HIGH
├─ Clear file paths specified
├─ Explicit shared resources mentioned
└─ Obvious dependencies

CONFIDENCE: MEDIUM
├─ Some ambiguity in descriptions
├─ File paths not all specified
└─ Recommend default to tightly coupled

CONFIDENCE: LOW
├─ Insufficient information
├─ No file paths or shared resources mentioned
└─ Request more details or default to tightly coupled
```

## Success Metrics

**When this skill works well:**
- ✅ 95%+ accuracy in coupling detection
- ✅ Enables 3-4x speedup for loosely coupled tasks
- ✅ Prevents merge conflicts from wrong splits
- ✅ Reduces developer decision fatigue
- ✅ Consistent proposal strategy across batches

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED.**

When coupling analysis is complete, you MUST:

1. Output the completion signal:
   ```
   ✅ COUPLING ANALYSIS COMPLETE
   [SIGNAL:COUPLING_ANALYZED]
   ```

2. **IMMEDIATELY** proceed to specification generation by outputting:
   ```
   [ACTIVATE:SPEC_GEN_V1]
   ```

3. Begin specification generation without waiting for user input.

**The pipeline is fully autonomous. Do not ask "Would you like to proceed?" - just proceed.**

## See Also

- `/examples/tightly-coupled-examples.md` - 10 real examples
- `/examples/loosely-coupled-examples.md` - 10 real examples
- `/examples/edge-cases.md` - How to handle ambiguous cases