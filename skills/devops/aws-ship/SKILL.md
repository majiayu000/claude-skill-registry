---
name: aws-ship
description: AWS shipping gate for Lambda, ECS, EKS, App Runner, API Gateway, CloudFront, IAM, Secrets Manager, SSM, networking, and rollout safety. Use when releasing to AWS and you want a provider-specific read on identity mistakes, env drift, networking traps, scaling surprises, or rollback realism.
user-invocable: true
argument-hint: "[Lambda, ECS service, EKS deploy, API Gateway change, or AWS release]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- IAM mistakes ship outages with extra ceremony.
- If the secret path or region is wrong, your health checks are theater.
- A deploy without rollback reality is just confidence cosplay.
- AWS will let you misconfigure five things before the first request arrives.

## What to interrogate

### 1. Release surface

State what is shipping:
- Lambda or Lambda@Edge
- ECS or Fargate service
- EKS workload
- API Gateway, ALB, or CloudFront
- App Runner or Elastic Beanstalk
- IAM, secrets, env config, network, or data-plane change

### 2. Identity and config realism

Check:
- IAM role and policy assumptions
- secret and parameter paths
- region/account/environment drift
- environment variable completeness
- S3, queue, database, and event-source permissions

### 3. Network and runtime risk

Review:
- VPC and subnet assumptions
- security groups and egress needs
- cold start or startup behavior
- timeout, memory, concurrency, and autoscaling settings
- health check and readiness realism

### 4. Rollout and rollback

Ask:
- is this canary, weighted, blue/green, or instant?
- can traffic shift back cleanly?
- do migrations, queue consumers, or config changes make rollback fake?
- what fails first under partial rollout?

## Output format

### AWS release surface

What actually changes in the platform.

### Platform blockers

IAM, secret, network, scaling, or runtime blockers.

### Rollout risk

What breaks during deploy, traffic shift, scale-up, or rollback.

### Mitigation and rollback plan

Concrete safer rollout steps.

### Verdict

- **Safe to release**
- **Fix before release**
- **AWS release red flag**
