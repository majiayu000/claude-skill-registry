---
name: risks-and-considerations
description: "Use when reviewing planning documents for security, performance, and scalability risks."
user-invocable: false
---

# Risks and Considerations

## Purpose

To ensure a systematic review of potential risks, edge cases, and important technical considerations for planning documents, particularly for GitHub Issues and new Claude Code Skills. This practice aids in proactive problem identification, robust planning, and the creation of more resilient and well-thought-out features and guidelines.

## Analysis Checklist

When drafting or reviewing a planning document, you must perform an analysis covering the following areas:

1.  **Security Implications**:
    - Could this change introduce vulnerabilities (e.g., XSS, CSRF, data leaks)?
    - Does it properly handle authentication and authorization?
    - Are user inputs validated and sanitized?

2.  **Performance Considerations**:
    - Could this change negatively impact system performance (e.g., increase page load time, database query time, function execution time)?
    - Are there opportunities for optimization (e.g., caching, code splitting, parallel execution, efficient algorithms)?

3.  **Scalability Concerns**:
    - Is the proposed solution designed to handle growth in users, data, and traffic?
    - Could any part of the design become a bottleneck at scale?
    - If you take one of the underlying variables in the assumptions of the business logic to the extreme, does the solution start to break down?

4.  **Cross-Browser/Platform Compatibility**:
    - Will the proposed changes work consistently across all supported browsers and platforms (web, desktop, mobile)?
    - Are there any known platform-specific issues to address?

5.  **Data Privacy Implications**:
    - Does this change handle user data responsibly?
    - Are there any GDPR or other privacy regulation concerns to address?

## Articulating Findings

After performing the analysis, you should articulate your findings clearly and actionably within the conversation or even directly on the planning document as a dedicated "Warnings & Considerations" section to highlight potential risks, suggest mitigation strategies, and note important technical details that must be handled during implementation.
