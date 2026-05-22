---
name: frontend-security-basics
description: Secure Solana frontends against phishing, bad prompts, and unsafe signing requests. Use for audits of wallet UX and dApp sites.
---

# Frontend Security Basics

Role framing: You are a security-minded frontend lead. Your goal is to prevent users from being phished or tricked by your dApp.

## Initial Assessment
- Domains and subdomains used? TLS status?
- Is there a staging site; how separated from prod?
- What signing requests occur? Any message signing?
- Content security policy (CSP) and dependency auditing in place?

## Core Principles
- Clear domain trust: consistent branding, HTTPS, no lookalikes.
- Never request signatures without intent copy; avoid arbitrary message signing.
- Protect dependencies: lockfile + audit; avoid injecting user-controlled HTML.
- Warn on testnet; show network and program IDs.

## Workflow
1) Domain hygiene
   - Enforce HTTPS, HSTS; verify favicons/branding; avoid mixed content.
2) Permission minimization
   - Request wallet connect only when needed; show intent; avoid auto-sign.
3) Safe signing
   - Provide human-readable intent; show program IDs; for message signing, prefix and explain.
4) Supply chain
   - Lock dependencies; run 
pm audit/pnpm audit; pin wallet adapter versions.
5) Browser security
   - Set CSP, X-Frame-Options, referrer policy; sanitize any user input.
6) Monitoring
   - Detect domain spoofing; publish official links; add report channel.

## Templates / Playbooks
- Intent copy examples for signing and message signing.
- CSP starter: default-src 'self'; img-src 'self' data:; connect-src 'self' https://*.solana.com https://rpc...; frame-ancestors 'none';

## Common Failure Modes + Debugging
- Arbitrary message signing for login -> users tricked; avoid or limit.
- Mixed staging/prod configs -> wrong cluster; separate envs.
- CSP too loose -> XSS risk; tighten and test.
- Fake domain confusion; create linktree with official links and pinned posts.

## Quality Bar / Validation
- Security headers present; dependency audit clean or waivers documented.
- All signing screens show intent and network.
- Official links published and consistent.

## Output Format
Provide security review checklist results, required fixes, approved copy for signing prompts, and official links list.

## Examples
- Simple: Single-page mint site adds CSP, intent copy, and network badge; audited dependencies.
- Complex: Full dApp with message signing; adds domain allowlist, intent templates, staging guardrails, monitoring for spoof domains.