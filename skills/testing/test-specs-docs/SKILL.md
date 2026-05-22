---
name: test-specs-docs
description: Create or update EasyPlatform test specifications in docs/test-specs/{Module}/. Use when asked to create test specs, write test cases, document test scenarios, or generate Given-When-Then specifications. Triggers on "test specs", "test specifications", "test cases", "test scenarios", "QA documentation", "Given-When-Then".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# EasyPlatform Test Specifications Documentation

Generate comprehensive test specifications following EasyPlatform conventions with Given-When-Then format and code evidence.

---

## Output Structure

All test specifications MUST be placed in the correct folder structure:

```
docs/
└── test-specs/
    ├── README.md                     # Master index with format spec
    ├── PRIORITY-INDEX.md             # All tests organized by P0-P3
    ├── INTEGRATION-TESTS.md          # Cross-module test scenarios
    ├── VERIFICATION-REPORT.md        # Test verification status
    └── {Module}/
        └── README.md                 # Module test specifications
```

---

## Module Codes & Naming Convention

### Test Case ID Format

```
TC-[MODULE]-[FEATURE]-[NUM]
```

**Examples:**

- `TC-TXT-SNP-001` = TextSnippet > Snippet > Test 001
- `TC-TXT-TAG-001` = TextSnippet > Tag > Test 001
- `TC-ACC-AUTH-001` = Accounts > Authentication > Test 001

### Module Codes

| Code | Module              | Folder               |
| ---- | ------------------- | -------------------- |
| TAL  | TextSnippet         | `TextSnippet`        |
| GRO  | TextSnippet         | `TextSnippet`        |
| SUR  | TextSnippet         | `TextSnippet`        |
| INS  | TextSnippet         | `TextSnippet`        |
| ACC  | Accounts            | `Accounts`           |
| NOT  | NotificationMessage | `SupportingServices` |
| PAR  | ParserApi           | `SupportingServices` |
| PER  | PermissionProvider  | `SupportingServices` |
| EXA  | ExampleApp          | `SupportingServices` |

### Feature Codes (Common)

| Feature        | Code | Example         |
| -------------- | ---- | --------------- |
| Goal           | GOL  | TC-TXT-GOL-001  |
| CheckIn        | CHK  | TC-TXT-CHK-001  |
| Review         | REV  | TC-TXT-REV-001  |
| Kudos          | KUD  | TC-TXT-KUD-001  |
| Snippet        | SNP  | TC-TXT-SNP-001  |
| Job            | JOB  | TC-TXT-JOB-001  |
| Interview      | INT  | TC-TXT-INT-001  |
| Survey         | SUR  | TC-TXT-SUR-001  |
| Authentication | AUTH | TC-ACC-AUTH-001 |
| User           | USR  | TC-ACC-USR-001  |

---

## Priority Classification

| Priority | Level    | Description                                         | Examples                                   |
| -------- | -------- | --------------------------------------------------- | ------------------------------------------ |
| **P0**   | Critical | Security, authentication, data integrity, financial | Login, password security, data isolation   |
| **P1**   | High     | Core business workflows                             | Create snippet, submit form, update record |
| **P2**   | Medium   | Secondary features                                  | Filters, sorting, notifications, reporting |
| **P3**   | Low      | UI enhancements, non-essential                      | Color themes, tooltips, preferences        |

### Priority Guidelines

- **P0**: If this fails, users cannot work or data is at risk
- **P1**: Core happy-path functionality for business operations
- **P2**: Features that enhance but don't block core workflows
- **P3**: Nice-to-have polish and non-critical features

---

## Phase 1: Context Gathering

### Step 1.1: Identify Target Module

Determine module from:

1. User specifies module/feature
2. Feature domain implies module
3. Search codebase for related code

### Step 1.2: Read Existing Test Specs

Before creating new specs:

```
1. Read docs/test-specs/README.md (format reference)
2. Read docs/test-specs/{Module}/README.md (if exists)
3. Read docs/test-specs/PRIORITY-INDEX.md (avoid duplicate IDs)
4. Identify existing test case IDs to continue numbering
```

### Step 1.3: Code Evidence Gathering

For each test case, gather evidence from:

- **Validation logic**: Command `Validate()` methods
- **Business rules**: Entity methods, domain services
- **Authorization**: Controller `[PlatformAuthorize]` attributes
- **Edge cases**: Conditional logic in handlers

---

## Phase 2: Test Specification Template

### Template: Module Test Specs (README.md)

Reference: `docs/test-specs/TextSnippet/README.md`

````markdown
# {Module} - Comprehensive Test Specifications

**Module**: {Module} ([Description])
**Generated**: {Date}
**Coverage**: [Feature list]

---

## Table of Contents

1. [Feature 1 Test Specs](#1-feature-1-test-specs)
2. [Feature 2 Test Specs](#2-feature-2-test-specs)
   ...

---

## 1. [Feature Name] Test Specs

### 1.1 [Sub-Feature] Tests

#### TC-{MOD}-{FEAT}-001: [Descriptive Test Name]

**Priority**: P0-Critical | P1-High | P2-Medium | P3-Low

**Preconditions**:

- User has `{Policy}` authorization
- Company has active {Feature} subscription
- [Other setup requirements]

**Test Steps** (Given-When-Then):

```gherkin
Given [initial context/state]
  And [additional context if needed]
When [action performed]
  And [additional action if needed]
Then [expected outcome]
  And [additional verification]
```
````

**Acceptance Criteria**:

- ✅ [Expected success behavior]
- ✅ [Another success case]
- ❌ [Expected failure behavior]
- ❌ [Another failure case]

**Test Data**:

```json
{
    "field": "value",
    "required": true
}
```

**Edge Cases**:

- ❌ [Boundary condition 1] → [Expected error]
- ❌ [Boundary condition 2] → [Expected error]
- ✅ [Edge case that should succeed] → Success

**Evidence**:

- **Controller**: `{Module}.Service/Controllers/{Controller}.cs:L{lines}`
    - Authorization: `{Policies}`
    - Endpoint: `{Method} /api/{path}`

- **Command Handler**: `{Module}.Application/UseCaseCommands/{Feature}/{Command}.cs:L{lines}`

<details>
<summary>Code Snippet: [Key Logic Description]</summary>

```csharp
// {File}:L{lines}
[actual code snippet]
```

</details>

**Related Files**:

| Layer    | Type       | File Path                                                                          |
| -------- | ---------- | ---------------------------------------------------------------------------------- |
| Backend  | Controller | `src/Backend/{Module}/{Module}.Service/Controllers/{Controller}.cs`                |
| Backend  | Command    | `src/Backend/{Module}/{Module}.Application/UseCaseCommands/{Feature}/{Command}.cs` |
| Backend  | Entity     | `src/Backend/{Module}/{Module}.Domain/Entities/{Entity}.cs`                        |
| Frontend | Component  | `src/Frontend/apps/playground-text-snippet/src/app/{feature}/{component}.ts`       |

---

#### TC-{MOD}-{FEAT}-002: [Next Test Name]

[Continue with same format...]

---

## Cross-Module Integration Tests

See [INTEGRATION-TESTS.md](../INTEGRATION-TESTS.md) for cross-module scenarios.

---

## Related Documentation

- **Business Features**: [docs/business-features/{Module}/README.md](../../business-features/{Module}/README.md)
- **Backend Patterns**: [docs/claude/backend-patterns.md](../../claude/backend-patterns.md)

---

**Last Updated**: {Date}

````

---

## Test Case Writing Guidelines

### Given-When-Then Best Practices

```gherkin
# GOOD - Specific and actionable
Given user is authenticated with EmployeePolicy role
  And company subscription includes Goal feature
  And goal creation form is displayed
When user fills required fields:
  - Title: "Reduce churn by 15%"
  - GoalType: "Smart"
  - TargetDate: "2025-12-31"
  And user clicks Submit
Then goal is created with status "Draft"
  And success notification is displayed
  And goal appears in dashboard list

# BAD - Vague and unmeasurable
Given user is logged in
When user creates a goal
Then it works
````

### Acceptance Criteria Format

```markdown
**Acceptance Criteria**:

- ✅ Form validates all required fields (Title, GoalType, TargetDate)
- ✅ Backend creates Goal entity in database
- ✅ Goal assigned to current employee as owner
- ✅ Notification event triggered via entity event handler
- ❌ External users cannot create goals (returns validation error)
- ❌ Missing required fields shows validation error
- ❌ Invalid date range shows "Target date must be after start date"
```

### Evidence Requirements

Every test case MUST include:

1. **Controller reference**: File path + line numbers + authorization policies
2. **Handler/Command reference**: File path + line numbers for business logic
3. **Code snippet**: Actual code in `<details>` block for key validation/logic
4. **Related files table**: All relevant source files

---

## Phase 3: Index Updates

After creating/updating test specs:

### Update PRIORITY-INDEX.md

Add new test cases to appropriate priority section:

```markdown
### P0 - Critical

| ID             | Module      | Feature   | Test Name                      |
| -------------- | ----------- | --------- | ------------------------------ |
| TC-TXT-GOL-001 | TextSnippet | Goal      | Create SMART Goal Successfully |
| TC-{NEW-ID}    | {Module}    | {Feature} | {Test Name}                    |
```

### Update Module Section in README.md

Ensure master test-specs README.md links to module:

```markdown
| **[{Module}](./{Module}/README.md)** | {Description} | {Feature list} | P1: {Focus} |
```

---

## Anti-Hallucination Protocols

### EVIDENCE_CHAIN_VALIDATION

- Every test case MUST reference actual source code
- Read validation logic before writing acceptance criteria
- Verify authorization policies from controller attributes
- Never assume behavior without code evidence

### LINE_NUMBER_ACCURACY

- Always verify line numbers are current
- Use Grep to find exact locations
- Include code snippets for complex logic

### TEST_ID_UNIQUENESS

- Read PRIORITY-INDEX.md before assigning new IDs
- Continue numbering sequence within feature
- Never duplicate existing TC-XXX-XXX-NNN IDs

---

## Quality Checklist

- [ ] Test case IDs follow TC-[MODULE]-[FEATURE]-[NUM] format
- [ ] All IDs are unique (verified against PRIORITY-INDEX.md)
- [ ] Priority assigned based on classification guidelines
- [ ] Given-When-Then format used for all test steps
- [ ] Acceptance criteria include both ✅ success and ❌ failure cases
- [ ] Test data examples provided in JSON format
- [ ] Edge cases documented with expected outcomes
- [ ] Code evidence with file paths and line numbers
- [ ] Code snippets in `<details>` blocks for key logic
- [ ] Related files table with all layers (Backend/Frontend)
- [ ] PRIORITY-INDEX.md updated with new test cases
- [ ] Links to business-features docs included

---

## Example: Complete Test Case

````markdown
#### TC-TXT-KUD-001: Send Kudos to Colleague Successfully

**Priority**: P1-High

**Preconditions**:

- User has `EmployeePolicy` authorization
- Company has Kudos feature enabled
- User has remaining quota for current period
- Recipient is an active employee in same company

**Test Steps** (Given-When-Then):

```gherkin
Given user is authenticated with EmployeePolicy role
  And company has Kudos feature enabled
  And user has at least 1 kudos quota remaining
  And target recipient "john.doe@company.com" is active employee
When user selects recipient from employee search
  And user selects kudos type "Teamwork"
  And user enters message "Great collaboration on Project X!"
  And user clicks Send Kudos
Then kudos transaction is created
  And sender quota decremented by 1
  And recipient receives notification
  And kudos appears in company feed
  And confirmation message displayed to sender
```
````

**Acceptance Criteria**:

- ✅ Kudos transaction created with sender, receiver, type, message
- ✅ Sender quota decremented (SendQuotaRemaining - 1)
- ✅ Receiver notification sent via NotificationMessage service
- ✅ Transaction visible in public company feed
- ❌ Sending to self returns "Cannot send kudos to yourself"
- ❌ Zero quota returns "No kudos remaining this period"
- ❌ Sending to inactive employee returns "Recipient not found"
- ❌ Sending to different company returns "Recipient not in your company"

**Test Data**:

```json
{
    "recipientEmployeeId": "emp-12345",
    "kudosType": "Teamwork",
    "message": "Great collaboration on Project X!",
    "isAnonymous": false
}
```

**Edge Cases**:

- ❌ Empty message → Validation error
- ❌ Message > 500 chars → Validation error
- ✅ Message with special characters → Success
- ❌ Invalid kudosType → Validation error

**Evidence**:

- **Controller**: `Growth.Service/Controllers/KudosController.cs:L25-28`
    - Authorization: `EmployeePolicy`, `KudosPolicy`
    - Endpoint: `POST /api/Kudos/send`

- **Command Handler**: `Growth.Application/UseCaseCommands/Kudos/SendKudosCommand.cs:L45-89`

<details>
<summary>Code Snippet: Quota Validation</summary>

```csharp
// SendKudosCommandHandler.cs:L52-58
return await requestSelfValidation
    .AndNotAsync(
        r => kudosRepository.AnyAsync(k =>
            k.SenderId == RequestContext.CurrentEmployeeId()
            && k.SendQuotaRemaining <= 0),
        "No kudos remaining this period"
    );
```

</details>

**Related Files**:

| Layer    | Type       | File Path                                                                                    |
| -------- | ---------- | -------------------------------------------------------------------------------------------- |
| Backend  | Controller | `src/Backend/TextSnippet/Growth.Service/Controllers/KudosController.cs`                      |
| Backend  | Command    | `src/Backend/TextSnippet/Growth.Application/UseCaseCommands/Kudos/SendKudosCommand.cs`       |
| Backend  | Entity     | `src/Backend/TextSnippet/Growth.Domain/Entities/Kudos/KudosTransaction.cs`                   |
| Frontend | Component  | `src/Frontend/apps/playground-text-snippet/src/app/kudos/send-kudos/send-kudos.component.ts` |

```

```

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
