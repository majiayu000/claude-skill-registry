---
name: content-feedback
description: Customer providing feedback about course content including suggestions for improvements, typo corrections, error reports in exercises or solutions, and feature requests for content.
metadata:
  trigger_phrases:
    - "feedback"
    - "suggestion"
    - "typo"
    - "error in"
    - "mistake in"
    - "correction"
    - "improvement"
    - "small note"
    - "solution incorrect"
    - "exercise wrong"
    - "content issue"
    - "you might want to fix"
    - "noticed an error"
  related_skills: ["ui-ux-feedback", "broken-link-404-error", "outdated-course-content"]
  sample_size: "586"
  routing: "agent"
  category: "feedback"
  validation: |
    required_phrases: []
    forbidden_patterns:
      - "(?i)refund"
      - "(?i)money back"
    max_length: 400
  created_from_gap_analysis: true
  source_cluster: 9
---
# Course Content Feedback

## When to Use

Use this skill when a customer:
- Reports typos or errors in content
- Suggests improvements to exercises
- Points out incorrect solutions
- Provides constructive feedback on course material
- Reports broken images or links in content

## Response Template

Thank you so much for taking the time to share this feedback! We really appreciate community members helping us improve the course content.

I've logged your feedback and our content team will review it. Corrections and improvements are regularly incorporated into course updates.

Thanks for helping make the course better for everyone!

## Feedback Types

- **Typos**: Text errors in lessons or exercises
- **Broken images**: Missing or broken visual content
- **Exercise errors**: Problems with exercise code or instructions
- **Solution bugs**: Incorrect or incomplete solutions
- **Content suggestions**: Ideas for improvements

## Example Requests

1. "Nice videos, just a small note: you don't need to use a normal function to use generics in JSX, you can define arrow functions too."
2. "Exercise 72.5 for reusable type guard provides an example of inferred type predicates but the solution itself is still showing that the value type is not inferred."
3. "I found broken images on this page: https://www.totaltypescript.com/books/total-typescript-essentials/"
4. "There's a typo in the first sentence of this automated email. Just an FYI."
5. "The assertion function example in the utility folder section has an issue with the type definitions."

## Phrases That Work

- "Thank you for taking the time..."
- "We really appreciate community members..."
- "I've logged your feedback..."
- "Thanks for helping make the course better..."
