---
name: aws-cloudformation-iam
description: Provides AWS CloudFormation patterns for IAM roles, policies, managed policies, permission boundaries, and trust relationships. Use when modeling least-privilege access, cross-account assumptions, service roles, or reusable IAM stacks that other CloudFormation templates consume.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation IAM Security

## Overview

Use this skill to model IAM with CloudFormation in a way that stays secure, auditable, and maintainable.

The most important design concerns are:
- separating trust policies from permission policies
- preferring roles over long-lived users wherever possible
- keeping least-privilege boundaries readable and reusable

Do not treat `SKILL.md` as a full IAM encyclopedia. Use the bundled references for larger policy examples and service-specific variants.

## When to Use

Use this skill when:
- creating IAM roles for Lambda, ECS, EC2, Step Functions, or other AWS services
- defining inline policies, managed policies, and permission boundaries in CloudFormation
- modeling cross-account assume-role access with constrained trust policies
- exporting IAM role ARNs or managed policy ARNs to downstream stacks
- reviewing wildcard permissions, boundary drift, or role replacement risk
- creating small reusable IAM stacks for platform or application teams

Typical trigger phrases include `cloudformation iam`, `iam role template`, `assume role policy`, `permission boundary`, `cross account role`, and `least privilege cloudformation`.

## Instructions

### 1. Prefer roles, then define the trust boundary first

Start by deciding who or what needs to assume the role:
- AWS service principal such as Lambda or ECS tasks
- a user or role in another AWS account
- a federated identity provider or workload identity flow

Write the trust policy first so the principal and assumption conditions are explicit before you add permissions.

### 2. Add the smallest permission set that supports the workload

Grant only the actions and resources the workload needs:
- use inline policies for highly local role-specific access
- use managed policies when the same access pattern is shared across multiple principals
- scope resources tightly and use conditions where possible

Keep permission documents readable; break up very large policies instead of hiding complexity in one giant statement.

### 3. Use permission boundaries and naming conventions intentionally

Permission boundaries help platform teams constrain delegated role creation.

Apply them when:
- teams create or extend roles in their own stacks
- you need guardrails around privileged services such as IAM, KMS, or Organizations
- you want to separate maximum allowed permissions from application-specific policies

Name roles and policies consistently so stack outputs and audits remain easy to trace.

### 4. Model cross-account access carefully

For cross-account roles:
- trust only the exact source account, role, or principal type that needs access
- add conditions such as `sts:ExternalId` when appropriate
- keep the permission policy separate from the trust policy so audits stay clear
- export only the ARNs or names that consuming accounts actually need

### 5. Validate the effective behavior, not just the template

Before rollout:
- validate the template and review change sets
- inspect trust relationships for unintended principals
- review wildcard actions and resources
- test assume-role behavior from the real caller when possible
- confirm policy attachment, boundary application, and stack outputs match the intended security model

## Examples

### Example 1: Service role for Lambda with tightly scoped permissions

```yaml
Resources:
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: DynamoDbWritePolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                Resource: !GetAtt OrdersTable.Arn
```

### Example 2: Cross-account role with an external ID condition

```yaml
Resources:
  PartnerReadRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: arn:aws:iam::123456789012:role/partner-reader
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                sts:ExternalId: partner-contract-001
```

Keep the trust relationship narrow and pair it with a separate read-only permission policy.

## Best Practices

- Prefer IAM roles over long-lived IAM users for application and automation access.
- Separate trust policies from permission policies when reviewing or refactoring templates.
- Use permission boundaries when delegating role creation to other teams.
- Scope resources, actions, and conditions as tightly as the workload allows.
- Export stable ARNs and names only when another stack truly consumes them.
- Keep expanded policy libraries and edge cases in `references/` instead of bloating the root skill.

## Constraints and Warnings

- Overly broad wildcards in IAM are easy to deploy and hard to notice later.
- Named IAM resources can be hard to replace safely once other systems depend on them.
- IAM changes may appear successful in CloudFormation before eventual consistency settles across AWS services.
- Some Identity Center or organization-wide access patterns need complementary tooling outside a single CloudFormation stack.
- Misconfigured trust policies are often a bigger risk than missing permissions.

## References

- `references/examples.md`
- `references/reference.md`

## Related Skills

- `aws-cloudformation-security`
- `aws-cloudformation-ec2`
- `aws-cloudformation-ecs`
- `aws-cloudformation-lambda`
