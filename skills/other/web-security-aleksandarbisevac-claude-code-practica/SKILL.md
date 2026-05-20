---
name: web-security
description: Enforce web security and avoid security vulnerabilities
---

# Web Security

We treat **web security as a core requirement**, not an afterthought.
Assume hostile input and untrusted environments by default.

## Core Principles

- **NEVER** trust user input
- **ALWAYS** validate and sanitize data at boundaries
- Prefer secure defaults over configurability

## XSS & Injection

- **AVOID** `dangerouslySetInnerHTML` and raw HTML injection
- Escape and encode dynamic content properly
- Never interpolate untrusted data into HTML, CSS, or JS contexts
- Ensure SQL injection protection

## Authentication & Authorization

- Do not store secrets or tokens in insecure locations
- **AVOID** localStorage for sensitive credentials when possible
- Use HTTP-only, secure cookies where applicable
- Always enforce authorization on the server

## Browser Security APIs

- Respect CORS, CSP, and browser security boundaries
- Use Content Security Policy to restrict script and resource execution
- Avoid inline scripts and styles when CSP is enabled

## Data Handling

- Minimize data exposure
- Do not log sensitive information

## Dependencies & Supply Chain

- Avoid unnecessary packages
- Treat third-party code as untrusted input

## General Principles

- Simplicity reduces attack surface
- If unsure, choose the more restrictive option
