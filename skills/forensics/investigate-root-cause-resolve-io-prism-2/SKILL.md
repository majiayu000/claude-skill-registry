---
name: investigate-root-cause
description: Use for root cause analysis of bugs or issues. Systematically investigates problems to identify underlying causes.
version: 1.0.0
---
<!-- Powered by Prism Coreâ„¢ -->

# investigate-root-cause

Deep investigation to find the root cause of a validated customer issue using code analysis and debugging.

## When to Use

- After validating that a customer issue is reproducible
- When Playwright validation shows consistent failure
- When error messages need tracing to source code
- Before creating fix specifications for Dev agent

## Quick Start

1. Review validation evidence (errors, screenshots, logs)
2. Search codebase for error signatures
3. Trace through call paths and data flow
4. Identify affected components
5. Document root cause and affected areas

## Purpose

After validating that a customer issue is reproducible, investigate the codebase to identify the exact cause, affected components, and potential fixes.

## SEQUENTIAL Task Execution

### 1. Review Validation Evidence
```yaml
evidence_review:
  - Console errors from Playwright validation
  - Network failures and API responses  
  - Screenshots showing the issue state
  - Timing data (performance issues)
  - Stack traces if available
```

### 2. Search for Error Signatures
Use grep/search tools to find related code:
```yaml
search_patterns:
  error_messages:
    - Search for exact error text from console
    - Look for exception messages
    - Find logging statements near the error
  
  component_search:
    - Identify UI component from screenshots
    - Search for element IDs/classes
    - Find event handlers for user actions
  
  api_endpoints:
    - Locate controller/endpoint from network logs
    - Find service methods being called
    - Trace database queries involved
```

### 3. Analyze Code Flow
```yaml
code_analysis:
  entry_point:
    - Start from user action (button click, form submit)
    - Trace through event handlers
    - Follow API calls
  
  data_flow:
    - Track data from input to processing
    - Identify transformations
    - Find validation points
  
  error_points:
    - Locate try/catch blocks
    - Find error handling logic
    - Identify missing error cases
```

### 4. Check Recent Changes
```yaml
change_investigation:
  git_history:
    - Check commits to affected files (last 30 days)
    - Review PRs that touched this area
    - Look for related deployments
  
  dependency_updates:
    - Package updates that might affect behavior
    - API version changes
    - Database schema modifications
```

### 5. Root Cause Identification

#### Common Root Cause Patterns

**Race Conditions:**
```csharp
// PROBLEM: Not waiting for async operation
public async Task ProcessPayment()
{
    StartPaymentProcess(); // Missing await!
    return RedirectToSuccess(); // Happens before payment completes
}
```

**Null Reference:**
```csharp
// PROBLEM: Not checking for null
var user = await GetUser(id);
var email = user.Email; // Crashes if user is null
```

**Timeout Issues:**
```csharp
// PROBLEM: Default timeout too short
var client = new HttpClient(); // 100 second default
var response = await client.GetAsync(slowEndpoint); // Times out
```

**State Management:**
```javascript
// PROBLEM: State not updating correctly
setState(newState); // Async operation
doSomethingWithState(state); // Uses old state
```

### 6. Document Findings
```yaml
root_cause_report:
  issue_summary: "Payment spinner runs indefinitely"
  
  root_cause:
    description: "Async payment process not awaited"
    file: "PaymentController.cs"
    line: 145
    method: "ProcessPayment"
    
  code_snippet: |
    // Line 145 - Missing await
    StartPaymentProcess(payment);
    return RedirectToAction("Success");
    
  why_it_fails:
    - "StartPaymentProcess is async but not awaited"
    - "Redirect happens immediately"
    - "Frontend polls for completion that never comes"
    
  when_introduced:
    commit: "abc123def"
    date: "2024-01-10"
    pr: "#4567"
    author: "developer@example.com"
```

### 7. Impact Analysis
```yaml
impact_assessment:
  direct_impact:
    - Files that need modification
    - Methods that need updates
    - Tests that will be affected
  
  side_effects:
    - Other features using same code
    - Performance implications
    - Security considerations
  
  risk_level:
    low: "Isolated change, well-tested area"
    medium: "Affects shared components"
    high: "Core system change, multiple dependencies"
```

### 8. Investigation Queries

#### Find Error Patterns
```bash
# Search for error message
grep -r "spinner" --include="*.cs" --include="*.js"

# Find recent changes to payment flow
git log -p --since="30 days ago" -- "*Payment*"

# Locate async issues
grep -r "StartPayment" --include="*.cs" | grep -v "await"
```

#### Analyze Dependencies
```bash
# Check package versions
cat package.json | grep -A2 -B2 "react"

# Find API calls
grep -r "fetch.*payment" --include="*.js"
```

## Success Criteria
- [ ] Root cause identified with specific code location
- [ ] Understanding of why the issue occurs
- [ ] Timeline of when issue was introduced
- [ ] Impact assessment completed
- [ ] Fix approach identified

## Output
- Root cause analysis document
- Affected code locations
- Recommended fix approach
- Risk assessment for changes
