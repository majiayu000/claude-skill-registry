---
name: app-crash-report
description: Customer reporting application crashes, missing exercises, broken features, StackBlitz issues, or other technical problems with the course platform.
metadata:
  trigger_phrases:
    - "application crash"
    - "app crashing"
    - "getting errors"
    - "application errors"
    - "missing exercises"
    - "exercises not showing"
    - "broken feature"
    - "StackBlitz"
    - "node modules"
    - "can't see subtitles"
    - "subtitle option missing"
    - "videos not loading"
    - "exercise doesn't work"
    - "code not running"
  related_skills: ["broken-link-404-error", "technical-issue-course-content", "course-content-locked"]
  sample_size: "760"
  routing: "agent"
  category: "technical_support"
  validation: |
    required_phrases: []
    forbidden_patterns:
      - "(?i)refund"
      - "(?i)money back"
    max_length: 500
  created_from_gap_analysis: true
  source_cluster: 27
---
# App Crash / Technical Bug Report

## When to Use

Use this skill when a customer reports:
- Application crashes or errors
- Missing exercises or content
- StackBlitz environment issues
- Node modules / npm errors
- Subtitle problems
- Videos not loading
- Exercises not working

## Response Template

Thank you for reporting this technical issue. We're sorry you're experiencing problems with the platform.

Could you please provide:
1. Which course/workshop you're accessing
2. Your browser and operating system
3. Any error messages you're seeing
4. Steps to reproduce the issue

This will help our team investigate and resolve the problem as quickly as possible.

## Common Issues

- **StackBlitz failures**: Environment crashes, dependency issues
- **Missing exercises**: Content not displaying under episodes
- **Subtitle issues**: Options not appearing on videos
- **npm errors**: node_modules problems in workshops

## Example Requests

1. "I've been getting a lot of application errors in the last couple of days. It happens when you go to the next lesson."
2. "Under each Episode there is text saying 'This module also has exercises for you to practice!' But I don't find them."
3. "I can't see the subtitle option in some of your workshop videos. Is this because I installed the npm packages incorrectly?"
4. "The StackBlitz environment keeps crashing when I try to run the exercises."
5. "Getting node_modules errors when trying to start the workshop. The application keeps crashing."

## Phrases That Work

- "We're sorry you're experiencing..."
- "Could you please provide more details..."
- "Our team will investigate..."
- "Let us know if the issue persists..."
