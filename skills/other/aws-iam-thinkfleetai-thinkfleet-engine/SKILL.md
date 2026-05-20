---
name: aws-iam
description: "Manage AWS IAM users, roles, policies, and access keys."
metadata: {"thinkfleetbot":{"emoji":"🔐","requires":{"bins":["aws","jq"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS IAM

Manage identity and access management.

## List users

```bash
aws iam list-users --query 'Users[].{Name:UserName,Created:CreateDate,LastUsed:PasswordLastUsed}' --output table
```

## List roles

```bash
aws iam list-roles --query 'Roles[].{Name:RoleName,Created:CreateDate,Path:Path}' --output table | head -30
```

## Get role details

```bash
aws iam get-role --role-name my-role | jq '{RoleName: .Role.RoleName, Arn: .Role.Arn, AssumeRolePolicy: .Role.AssumeRolePolicyDocument}'
```

## List attached policies (role)

```bash
aws iam list-attached-role-policies --role-name my-role --query 'AttachedPolicies[].{Name:PolicyName,Arn:PolicyArn}' --output table
```

## List inline policies (role)

```bash
aws iam list-role-policies --role-name my-role --output table
```

## Get policy document

```bash
aws iam get-policy-version --policy-arn arn:aws:iam::123456789:policy/my-policy \
  --version-id v1 | jq '.PolicyVersion.Document'
```

## List access keys

```bash
aws iam list-access-keys --user-name my-user --query 'AccessKeyMetadata[].{KeyId:AccessKeyId,Status:Status,Created:CreateDate}' --output table
```

## Get account summary

```bash
aws iam get-account-summary | jq '.SummaryMap | {Users, Roles, Policies, Groups, MFADevices: .MFADevicesInUse}'
```

## Simulate policy

```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:role/my-role \
  --action-names s3:GetObject s3:PutObject \
  --resource-arns "arn:aws:s3:::my-bucket/*" \
  --query 'EvaluationResults[].{Action:EvalActionName,Decision:EvalDecision}' --output table
```

## Notes

- IAM is global (not region-specific).
- Use `simulate-principal-policy` to test permissions without making real calls.
- Never create or rotate access keys without user confirmation.
