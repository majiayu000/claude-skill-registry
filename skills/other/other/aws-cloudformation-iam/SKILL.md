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

- Creating IAM roles for Lambda, ECS, EC2, Step Functions, or other AWS services
- Defining inline policies, managed policies, and permission boundaries in CloudFormation
- Modeling cross-account assume-role access with constrained trust policies
- Exporting IAM role ARNs or managed policy ARNs to downstream stacks
- Reviewing wildcard permissions, boundary drift, or role replacement risk
- Creating reusable IAM stacks for platform or application teams

## Instructions

### 1. Define the trust boundary first

Identify who or what assumes the role (service principal, cross-account principal, or federated identity), then write the trust policy with explicit principals and conditions before adding permissions.

### 2. Grant the minimum permission set

Use inline policies for role-specific access; use managed policies for shared patterns across principals. Scope actions and resources tightly, and use conditions where possible.

### 3. Apply permission boundaries for delegated role creation

Use permission boundaries when teams create or extend roles in their own stacks, when guardrails are needed around privileged services (IAM, KMS, Organizations), or to separate maximum allowed permissions from application-specific policies.

Name roles and policies consistently so stack outputs and audits remain easy to trace.

### 4. Model cross-account access

For cross-account roles: trust only the exact source account or principal, add `sts:ExternalId` conditions when appropriate, keep permission and trust policies separate, and export only the ARNs that consuming accounts need.

### 5. Validate the template and policy behavior

Before rollout, use these commands to verify the template and IAM behavior:

```bash
# Validate CloudFormation template syntax
aws cloudformation validate-template --template-body file://template.yaml

# Preview changes before applying
aws cloudformation create-change-set \
  --stack-name <stack-name> \
  --template-body file://template.yaml \
  --change-set-type CREATE

# Simulate whether a principal can perform specific actions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/LambdaExecutionRole \
  --action-names dynamodb:GetItem dynamodb:PutItem

# Check for wildcards in IAM policies within the template
aws cloudformation list-stack-resources --stack-name <stack-name>
```

After deployment, confirm policy attachments and stack outputs match the intended security model.

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
