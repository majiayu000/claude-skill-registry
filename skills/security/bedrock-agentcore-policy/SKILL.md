---
name: bedrock-agentcore-policy
description: Amazon Bedrock AgentCore Policy for defining agent boundaries using natural language and Cedar. Deterministic policy enforcement at the Gateway level. Use when setting agent guardrails, access control, tool permissions, or compliance rules.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Amazon Bedrock AgentCore Policy

## Overview

AgentCore Policy provides deterministic enforcement of agent boundaries, separate from the probabilistic nature of prompt engineering. Author policies in natural language that automatically convert to Cedar—AWS's open-source policy language—for real-time enforcement at the Gateway layer.

**Purpose**: Define what agents can and cannot do with deterministic, auditable rules

**Pattern**: Task-based (5 operations)

**Key Principles** (validated by AWS December 2025):
1. **Natural Language Authoring** - Write policies in plain English
2. **Automated Cedar Generation** - System converts to valid Cedar
3. **Real-time Enforcement** - Gateway intercepts every tool call
4. **Automated Reasoning** - Detects overly permissive/restrictive rules
5. **Default Deny** - No permit policy = automatic denial
6. **Forbid Wins** - Forbid always overrides permit

**Quality Targets**:
- Policy generation: < 5 seconds
- Enforcement latency: < 10ms per tool call
- Validation coverage: 100% of tool schemas

---

## When to Use

Use bedrock-agentcore-policy when:

- Setting boundaries for what agents can do
- Implementing role-based access control (RBAC)
- Enforcing compliance rules (e.g., max refund amounts)
- Temporarily disabling problematic tools
- Requiring specific parameters for operations
- Auditing agent actions

**When NOT to Use**:
- Content filtering (use Bedrock Guardrails)
- Rate limiting (use API Gateway)
- Business logic (implement in tools)

---

## Prerequisites

### Required
- AgentCore Gateway configured
- Tools registered as Gateway targets
- IAM permissions for policy operations

### Recommended
- Understanding of Cedar semantics
- Tool schemas documented
- Test scenarios defined

---

## Operations

### Operation 1: Natural Language Policy Authoring

**Time**: 2-5 minutes
**Automation**: 95%
**Purpose**: Create policies from plain English descriptions

**Process**:

1. **Define requirements in natural language**:
```
"Allow all users to read policy details and claim status.
Only allow users with 'senior-adjuster' role to update coverage.
Block all claim filings unless a description is provided."
```

2. **Generate Cedar policy**:
```python
import boto3

control = boto3.client('bedrock-agentcore-control')

# Start policy generation from natural language
response = control.start_policy_generation(
    gatewayId='gateway-xxx',
    naturalLanguagePolicy="""
    Allow all users to get policy and get claim status.
    Only allow principals with the 'senior-adjuster' role to update coverage.
    Block principals from filing claims unless description is provided.
    """,
    policyName='insurance-agent-policy'
)

generation_id = response['policyGenerationId']

# Wait for completion
waiter = control.get_waiter('PolicyGenerationCompleted')
waiter.wait(policyGenerationId=generation_id)

# Get generated Cedar
result = control.get_policy_generation(
    policyGenerationId=generation_id
)

cedar_policy = result['generatedPolicy']
validation_results = result['validationResults']
```

3. **Review generated Cedar**:
```cedar
// Permit read-only actions for everyone
permit(
    principal,
    action in [
        AgentCore::Action::"InsuranceAPI__get_policy",
        AgentCore::Action::"InsuranceAPI__get_claim_status"
    ],
    resource
);

// Permit updates only for specific roles
permit(
    principal,
    action == AgentCore::Action::"InsuranceAPI__update_coverage",
    resource
)
when {
    principal.hasTag("role") &&
    principal.getTag("role") == "senior-adjuster"
};

// Block claims without description
forbid(
    principal,
    action == AgentCore::Action::"InsuranceAPI__file_claim",
    resource
)
unless {
    context.input has description
};
```

---

### Operation 2: Create Policy Directly (Cedar)

**Time**: 5-10 minutes
**Automation**: 80%
**Purpose**: Write Cedar policies with full control

**Cedar Syntax**:
```cedar
// Basic permit
permit(
    principal,
    action == AgentCore::Action::"ToolName__method",
    resource == AgentCore::Gateway::"arn:..."
);

// With conditions
permit(
    principal is AgentCore::OAuthUser,
    action == AgentCore::Action::"RefundAPI__process_refund",
    resource
)
when {
    context.input.amount < 1000
};

// Forbid with unless
forbid(
    principal,
    action == AgentCore::Action::"DeleteAPI__delete_record",
    resource
)
unless {
    principal.hasTag("role") &&
    principal.getTag("role") == "admin"
};
```

**Create policy via boto3**:
```python
response = control.create_policy(
    name='refund-limit-policy',
    description='Limits refunds to under $1000 for non-managers',
    policyContent='''
permit(
    principal,
    action == AgentCore::Action::"RefundToolTarget___refund",
    resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:123456789012:gateway/refund"
)
when {
    context.input.amount < 1000
};

permit(
    principal,
    action == AgentCore::Action::"RefundToolTarget___refund",
    resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:123456789012:gateway/refund"
)
when {
    principal.hasTag("role") &&
    principal.getTag("role") == "manager"
};
'''
)

policy_id = response['policyId']
```

---

### Operation 3: Common Policy Patterns

**Time**: 5-15 minutes
**Automation**: 90%
**Purpose**: Implement standard access control patterns

**Pattern 1: Role-Based Access Control (RBAC)**
```cedar
// Admin-only actions
permit(
    principal,
    action in [
        AgentCore::Action::"AdminAPI__delete_user",
        AgentCore::Action::"AdminAPI__modify_permissions"
    ],
    resource
)
when {
    principal.hasTag("role") &&
    principal.getTag("role") == "admin"
};
```

**Pattern 2: OAuth Scope Validation**
```cedar
// Require specific scope
permit(
    principal is AgentCore::OAuthUser,
    action == AgentCore::Action::"CustomerAPI__read_profile",
    resource
)
when {
    principal.hasTag("scope") &&
    principal.getTag("scope") like "*customer:read*"
};
```

**Pattern 3: Parameter Constraints**
```cedar
// Limit by parameter value
permit(
    principal,
    action == AgentCore::Action::"TransferAPI__transfer_funds",
    resource
)
when {
    context.input has amount &&
    context.input.amount <= 10000
};
```

**Pattern 4: Multi-Condition AND Logic**
```cedar
// All conditions must be true
permit(
    principal,
    action == AgentCore::Action::"InsuranceAPI__update_coverage",
    resource
)
when {
    context.input has coverageType &&
    context.input has newLimit &&
    (context.input.coverageType == "liability" ||
     context.input.coverageType == "collision")
};
```

**Pattern 5: Disable Specific Tool**
```cedar
// Temporarily disable a tool
forbid(
    principal,
    action == AgentCore::Action::"ProblematicAPI__buggy_method",
    resource
);
```

**Pattern 6: User-Specific Permissions**
```cedar
// Grant to specific user
permit(
    principal,
    action == AgentCore::Action::"SpecialAPI__sensitive_action",
    resource
)
when {
    principal.hasTag("username") &&
    principal.getTag("username") == "trusted-user"
};
```

---

### Operation 4: Policy Engine Configuration

**Time**: 5-10 minutes
**Automation**: 85%
**Purpose**: Attach policies to Gateway for enforcement

**Create Policy Engine**:
```python
# Create policy engine to evaluate policies
response = control.create_policy_engine(
    name='insurance-policy-engine',
    description='Enforces insurance agent boundaries',
    gatewayId='gateway-xxx'
)

engine_id = response['policyEngineId']

# Wait for active
waiter = control.get_waiter('PolicyEngineActive')
waiter.wait(policyEngineId=engine_id)
```

**Attach Policy to Engine**:
```python
# Update policy engine with policies
response = control.update_policy_engine(
    policyEngineId=engine_id,
    policyIds=[
        'policy-read-access',
        'policy-role-restrictions',
        'policy-refund-limits'
    ]
)
```

**Test Policy Enforcement**:
```python
# Invoke agent and observe policy enforcement
client = boto3.client('bedrock-agentcore')

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:...',
    runtimeSessionId='test-session',
    payload={
        'prompt': 'Process a refund of $50000',
        'context': {
            'user_id': 'regular-user',
            'role': 'customer-service'  # Not manager
        }
    }
)

# Policy will block this - amount exceeds $1000 for non-managers
# Agent response will indicate the action was denied
```

---

### Operation 5: Policy Validation and Debugging

**Time**: 5-15 minutes
**Automation**: 80%
**Purpose**: Test and troubleshoot policy behavior

**Validation Checks**:
```python
# Get policy validation results
response = control.get_policy_generation(
    policyGenerationId=generation_id
)

for issue in response.get('validationResults', {}).get('issues', []):
    print(f"Issue: {issue['type']}")
    print(f"Message: {issue['message']}")
    print(f"Location: {issue.get('location', 'N/A')}")

# Common issues:
# - Overly permissive (allows more than intended)
# - Overly restrictive (blocks legitimate actions)
# - Unsatisfiable conditions (can never match)
# - Schema mismatch (references non-existent tools)
```

**Debug Policy Decisions**:
```python
# Enable detailed logging
import logging
logging.getLogger('botocore').setLevel(logging.DEBUG)

# Check CloudWatch for policy decisions
# Log group: /aws/bedrock-agentcore/gateway/{gateway-id}
# Look for: PolicyDecision events

# Example log entry:
# {
#   "eventType": "PolicyDecision",
#   "action": "InsuranceAPI__file_claim",
#   "decision": "DENY",
#   "matchedPolicy": "policy-require-description",
#   "reason": "Condition not satisfied: context.input has description"
# }
```

**Test Scenarios**:
```python
def test_policy_scenarios():
    """Test various policy scenarios"""

    test_cases = [
        {
            'name': 'Regular user reads policy',
            'action': 'get_policy',
            'context': {'role': 'user'},
            'expected': 'ALLOW'
        },
        {
            'name': 'Regular user updates coverage',
            'action': 'update_coverage',
            'context': {'role': 'user'},
            'expected': 'DENY'
        },
        {
            'name': 'Senior adjuster updates coverage',
            'action': 'update_coverage',
            'context': {'role': 'senior-adjuster'},
            'expected': 'ALLOW'
        },
        {
            'name': 'Claim without description',
            'action': 'file_claim',
            'context': {'role': 'user'},
            'input': {'amount': 100},  # No description
            'expected': 'DENY'
        },
        {
            'name': 'Claim with description',
            'action': 'file_claim',
            'context': {'role': 'user'},
            'input': {'amount': 100, 'description': 'Car accident'},
            'expected': 'ALLOW'
        }
    ]

    for case in test_cases:
        result = simulate_policy(case)
        assert result == case['expected'], f"Failed: {case['name']}"
```

---

## Cedar Quick Reference

### Principal Types
```cedar
principal                           // Any principal
principal is AgentCore::OAuthUser   // OAuth authenticated user
principal is AgentCore::ApiKeyUser  // API key authenticated
```

### Actions
```cedar
action == AgentCore::Action::"ToolName__method"
action in [Action1, Action2, Action3]
```

### Conditions
```cedar
// Tag checks
principal.hasTag("role")
principal.getTag("role") == "admin"
principal.getTag("scope") like "*read*"

// Context/input checks
context.input has fieldName
context.input.amount < 1000
context.input.type == "premium"

// Logical operators
&&  // AND
||  // OR
!   // NOT
```

### Policy Types
```cedar
permit(...)         // Allow if conditions match
permit(...) when {} // Allow with conditions
forbid(...)         // Deny unconditionally
forbid(...) unless {} // Deny unless conditions match
```

---

## Best Practices

### 1. Start Permissive, Tighten Gradually
```cedar
// Phase 1: Allow all, log actions
permit(principal, action, resource);

// Phase 2: After analysis, add restrictions
permit(principal, action, resource)
when { /* specific conditions */ };
```

### 2. Use Descriptive Policy Names
```python
control.create_policy(
    name='refund-limit-1000-non-managers',  # Good
    # name='policy-1',  # Bad
    ...
)
```

### 3. Document Business Rules
```cedar
// Business Rule: PCI-DSS compliance requires
// credit card operations to be role-restricted
permit(
    principal,
    action == AgentCore::Action::"PaymentAPI__process_card",
    resource
)
when {
    principal.hasTag("role") &&
    principal.getTag("role") in ["payment-admin", "finance"]
};
```

### 4. Layer Policies
```
Policy Stack:
1. Global deny (default)
2. Read-only permits (broad)
3. Write permits (role-specific)
4. Admin permits (highly restricted)
5. Emergency forbids (immediate disable)
```

---

## MCP Server Integration

AgentCore Policy is available as an MCP server for AI-assisted coding environments:

```json
{
  "mcpServers": {
    "bedrock-agentcore-policy": {
      "command": "uvx",
      "args": ["bedrock-agentcore-policy-mcp"],
      "env": {
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

---

## Related Skills

- **bedrock-agentcore**: Core platform and Gateway setup
- **bedrock-agentcore-evaluations**: Test policy effectiveness
- **bedrock-agentcore-deployment**: Deploy policies with agents
- **eks-irsa**: IAM integration for EKS-hosted agents

---

## References

- `references/cedar-syntax.md` - Complete Cedar language guide
- `references/policy-patterns.md` - Common patterns library
- `references/troubleshooting.md` - Policy debugging guide

---

## Sources

- [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Example Policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/example-policies.html)
- [Common Policy Patterns](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-common-patterns.html)
- [Cedar Language](https://www.cedarpolicy.com/)
