---
name: hr-automation
description: "HR workflow automation - recruiting, onboarding, employee management, and offboarding processes"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: hr
tags:
  - hr
  - recruiting
  - onboarding
  - employee
  - automation
department: Human Resources

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: hr-mcp
  tools:
    - greenhouse_api
    - workday_api
    - bamboohr_api

capabilities:
  - recruiting_automation
  - onboarding_workflows
  - employee_management
  - offboarding_processes
  - compliance_tracking

languages:
  - en
  - zh

related_skills:
  - applicant-screening
  - offer-letter
  - job-description
  - slack-workflows
---

# HR Automation

Automate HR workflows including recruiting, onboarding, employee management, and offboarding. Based on n8n's HR workflow templates.

## Overview

This skill covers:
- Recruiting pipeline automation
- Employee onboarding workflows
- Performance review cycles
- Time-off management
- Offboarding processes

---

## Recruiting Automation

### Applicant Pipeline

```yaml
recruiting_pipeline:
  stages:
    - applied
    - screening
    - phone_interview
    - technical_interview
    - onsite_interview
    - offer
    - hired
    
  automations:
    new_application:
      trigger: application_received
      actions:
        - send_confirmation: to_candidate
        - notify_recruiter: slack
        - add_to_tracking: airtable
        - ai_resume_screen: if_enabled
        
    stage_change:
      trigger: candidate_moved
      actions:
        - update_candidate: in_ats
        - notify_team: relevant_interviewers
        - send_email: stage_specific_template
        
    interview_scheduled:
      trigger: calendar_event_created
      actions:
        - send_confirmation: to_candidate
        - send_prep_materials: to_interviewers
        - create_scorecard: in_system
```

### AI Resume Screening

```yaml
ai_screening:
  model: gpt-4
  
  prompt: |
    Review this resume for the {job_title} position.
    
    Job Requirements:
    {job_requirements}
    
    Resume:
    {resume_text}
    
    Evaluate:
    1. Skills match (1-10)
    2. Experience match (1-10)
    3. Key strengths
    4. Potential concerns
    5. Recommended: Yes/No/Maybe
    
  automation:
    - if: score >= 8
      action: advance_to_screening
    - if: score 5-7
      action: flag_for_review
    - if: score < 5
      action: auto_reject + send_rejection
```

### Interview Scheduling

```yaml
interview_scheduling:
  workflow:
    1. candidate_advances:
        trigger: stage_change_to_interview
        
    2. check_availability:
        interviewers: from_hiring_plan
        candidate: request_via_email
        
    3. find_slots:
        algorithm: first_available_matching
        buffer: 15_minutes_between
        
    4. send_invites:
        to: [candidate, interviewers]
        include: [zoom_link, calendar_invite, prep_docs]
        
    5. reminders:
        - 24h_before: all_parties
        - 1h_before: all_parties
        
    6. post_interview:
        - collect_feedback: from_interviewers
        - aggregate_scores
        - trigger_next_stage: if_approved
```

---

## Onboarding Automation

### New Hire Workflow

```yaml
onboarding_workflow:
  trigger: offer_accepted
  duration: 30_days
  
  pre_start:
    day_minus_14:
      - send_welcome_email
      - collect_documents: [id, tax_forms, direct_deposit]
      - order_equipment: laptop, peripherals
      
    day_minus_7:
      - create_accounts: [email, slack, tools]
      - add_to_systems: hris, payroll
      - schedule_orientation
      - assign_buddy
      
    day_minus_1:
      - setup_desk: if_office
      - ship_equipment: if_remote
      - send_first_day_info
      
  first_day:
    morning:
      - welcome_meeting: with_manager
      - it_setup: credentials, tools
      - team_introductions
      
    afternoon:
      - hr_orientation: policies, benefits
      - access_verification
      - buddy_lunch
      
  first_week:
    - daily_checkins: with_manager
    - tool_training: as_needed
    - team_meetings: join_all
    - documentation_review
    
  first_month:
    - weekly_1on1s: with_manager
    - project_assignment
    - goal_setting
    - 30_day_survey
```

### Onboarding Checklist Automation

```yaml
onboarding_checklist:
  employee_tasks:
    - complete_i9: deadline_day_3
    - setup_direct_deposit: deadline_day_7
    - complete_benefits_enrollment: deadline_day_30
    - review_handbook: deadline_day_7
    - complete_training: deadline_day_14
    
  manager_tasks:
    - introduce_to_team: day_1
    - assign_onboarding_buddy: day_1
    - set_30_60_90_goals: week_1
    - schedule_recurring_1on1s: week_1
    - provide_project_context: week_1
    
  it_tasks:
    - create_email: day_minus_1
    - provision_tools: day_minus_1
    - setup_hardware: day_1
    - grant_system_access: day_1
    - security_training: week_1
    
  notifications:
    incomplete_task:
      - remind_owner: at_50%_deadline
      - remind_owner: at_80%_deadline
      - escalate: at_100%_deadline
```

---

## Employee Management

### Time-Off Requests

```yaml
pto_workflow:
  request:
    trigger: employee_submits_request
    fields: [start_date, end_date, type, reason]
    
  approval:
    routing:
      - if: days <= 3
        approver: direct_manager
      - if: days > 3
        approver: [manager, hr]
        
    automation:
      - notify_approver: slack_dm
      - set_deadline: 48_hours
      - if_no_response: escalate
      
  approved:
    actions:
      - update_calendar: block_dates
      - notify_team: upcoming_pto
      - update_hris: deduct_balance
      - send_confirmation: to_employee
      
  denied:
    actions:
      - notify_employee: with_reason
      - log_denial: for_compliance
```

### Performance Reviews

```yaml
performance_review_cycle:
  schedule: quarterly
  
  workflow:
    week_1:
      - launch_cycle: notify_all
      - self_assessment: open
      
    week_2:
      - self_assessment: deadline
      - peer_feedback: open
      
    week_3:
      - peer_feedback: deadline
      - manager_review: open
      
    week_4:
      - manager_review: deadline
      - calibration: hr_and_leadership
      - finalize_ratings
      
    week_5:
      - deliver_reviews: manager_meetings
      - goal_setting: next_quarter
      
  automation:
    reminders:
      - 3_days_before_deadline: gentle
      - 1_day_before: urgent
      - overdue: daily_until_complete
      
    analytics:
      - completion_rates
      - score_distribution
      - feedback_themes
```

---

## Offboarding

### Offboarding Workflow

```yaml
offboarding_workflow:
  trigger: resignation_submitted OR termination
  
  immediate:
    - acknowledge_resignation: to_employee
    - notify_hr: for_processing
    - notify_manager: for_transition_planning
    - notify_it: for_access_review
    
  planning_phase:
    - calculate_final_pay
    - schedule_exit_interview
    - create_transition_plan
    - document_knowledge_transfer
    
  last_week:
    - knowledge_transfer: sessions
    - collect_equipment
    - remove_system_access: scheduled
    - update_team_distribution
    
  last_day:
    - exit_interview: hr
    - return_badge_keys
    - revoke_all_access
    - send_farewell: if_voluntary
    
  post_departure:
    - process_final_paycheck
    - send_benefits_info: cobra
    - archive_files
    - offboarding_survey: 30_days_later
```

### Access Revocation

```yaml
access_revocation:
  immediate_on_termination:
    - email: disable
    - sso: revoke
    - vpn: revoke
    - physical_access: revoke
    - company_credit_cards: cancel
    
  within_24_hours:
    - tool_licenses: remove
    - shared_drives: transfer_ownership
    - code_repositories: remove
    - customer_systems: remove
    
  audit:
    - document_all_revocations
    - verify_no_remaining_access
    - compliance_report
```

---

## Compliance Tracking

### Document Management

```yaml
document_compliance:
  required_documents:
    - i9: deadline_3_days
    - w4: deadline_first_payroll
    - emergency_contact: deadline_7_days
    - direct_deposit: deadline_first_payroll
    - handbook_acknowledgment: deadline_7_days
    - benefits_election: deadline_30_days
    
  tracking:
    - notify_employee: missing_docs
    - notify_hr: compliance_risk
    - escalate: after_deadline
    
  storage:
    - location: secure_hris
    - retention: per_legal_requirements
    - access: hr_only
```

---

## Output Example

**Request**: "Create an employee onboarding checklist automation"

**Output**:

```markdown
# Employee Onboarding Automation

## Trigger
New hire added to HRIS (e.g., BambooHR, Workday)

## Pre-Start Checklist

### Day -14
- [ ] Send welcome email
- [ ] Collect: ID, Tax forms, Banking info
- [ ] Order laptop & equipment

### Day -7
- [ ] Create email account
- [ ] Create Slack account
- [ ] Add to HRIS
- [ ] Schedule orientation
- [ ] Assign buddy

### Day -1
- [ ] Ship/setup equipment
- [ ] Send Day 1 instructions
- [ ] Prepare workspace (if office)

## Day 1 Checklist

### Morning
- [ ] Manager welcome (9am)
- [ ] IT setup (10am)
- [ ] Team introductions

### Afternoon
- [ ] HR orientation (1pm)
- [ ] Buddy lunch
- [ ] Tool walkthroughs

## Notifications

```yaml
overdue_task:
  - 50% deadline: Friendly reminder
  - 80% deadline: Urgent reminder
  - 100% deadline: Escalate to manager
```

## n8n Workflow

```yaml
trigger: New employee in BambooHR
actions:
  - Create accounts (Google, Slack)
  - Add to Notion onboarding tracker
  - Send Slack welcome
  - Schedule calendar events
  - Create task checklist in Asana
```
```

---

*HR Automation Skill - Part of Claude Office Skills*
