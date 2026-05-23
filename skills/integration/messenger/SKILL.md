---
name: messenger
description: Guidance for Facebook Messenger Platform integrations: app setup, webhooks, messaging, and operational safety.
---

# Messenger Integration Guide

## Goal
Provide a practical baseline for integrating Facebook Messenger: app setup, webhooks, messaging flows, and safe operations.

## Use when
- You need a Messenger bot for notifications or support.
- You need to describe webhook validation and event handling.
- You want a security/rate-limit checklist.

## Do not use when
- The request involves policy violations or spam.

## Core topics
- App and Page setup, tokens, permissions.
- Webhook verification and signature checks.
- Message types: text, templates, attachments.
- Ops: rate limits, retries, logging.

## Required inputs
- App/Page ownership and use case.
- Deployment model and environment.
- Access control and compliance constraints.

## Expected output
- A clear integration plan with a technical checklist.

## Notes
- Never expose Page access tokens.
- Validate webhooks and handle retries safely.
