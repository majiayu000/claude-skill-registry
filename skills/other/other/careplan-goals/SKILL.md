---
name: careplan-goals
description: Generate CarePlan, Goal, and ServiceRequest resources with proper status, intent, categories, targets, and linked conditions. Use when user mentions care plan, goals, service request, referral, orders, lab orders, imaging orders, or care coordination.
keywords: [careplan, care plan, goal, service request, referral, order, lab order, imaging, physical therapy, counseling, care coordination, target, HbA1c target, blood pressure target]
resource_types: [CarePlan, Goal, ServiceRequest]
always: false
---

# Care Plans, Goals, and Service Requests

## Care Plan
- Status: draft, active, on-hold, revoked, completed, entered-in-error.
- Intent: proposal, plan, order, option.
- Categories: assess-plan, longitudinal, encounter-specific.
- Include CarePlan.activity with detail (scheduled procedures, medication reviews, referrals).
- Link to Conditions via CarePlan.addresses[].
- Link to Goals via CarePlan.goal[].

## Goals
- lifecycleStatus: proposed, planned, accepted, active, on-hold, completed, cancelled.
- achievementStatus: in-progress, improving, worsening, no-change, achieved, not-achieved.
- Include target with detailQuantity, dueDate:
  * HbA1c < 7.0%, BP < 140/90, LDL < 100, BMI < 30, weight loss X lbs by date.
- Priority: high-priority, medium-priority, low-priority.

## Service Requests
- Status: draft, active, completed, revoked, entered-in-error.
- Intent: order, plan, proposal, directive, reflex-order, filler-order.
- Categories: laboratory, imaging, procedure, referral, counseling.
- Priority: routine, urgent, asap, stat.
- Common orders: Lab panels, imaging (X-ray, CT, MRI), specialist referrals,
  physical therapy, dietary counseling.

