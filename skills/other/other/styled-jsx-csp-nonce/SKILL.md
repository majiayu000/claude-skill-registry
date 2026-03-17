---
name: styled-jsx-csp-nonce
description: Configure styled-jsx to work with strict CSP using nonces (Next.js/custom Document patterns). Use when CSP blocks inline styles.
argument-hint: "[framework: next/pages/app] [current CSP header] [desired nonce flow]"
allowed-tools: Read, Grep, Glob
---

# styled-jsx CSP Nonce Skill

Enable styled-jsx under strict Content-Security-Policy rules.

## What to do

1. Identify the framework (Next.js pages router, app router, custom SSR).
2. Confirm where the nonce is generated (server) and how it reaches HTML.
3. Ensure:
   - CSP header includes style-src with the same nonce
   - styled-jsx style tags receive the nonce attribute

## Output expectations

- Provide the minimal code changes needed in the appropriate files.
- Include notes on where the nonce originates and how it propagates.
- Avoid insecure CSP suggestions (do not recommend unsafe-inline).
