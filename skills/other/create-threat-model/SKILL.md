---
name: create-threat-model
description: Perform STRIDE threat modeling for a system or component when the user asks to threat model, analyze security risks, or identify attack vectors
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[system or component to threat model]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: security, threat-model, design
---

# Create Threat Model

## Overview

Generate a STRIDE-based threat model (Microsoft) for a system or component. Identifies trust boundaries from architecture docs, analyzes each boundary for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege threats, and recommends mitigations for each identified threat.

## Workflow

1. **Read architecture context** -- Scan `.chalk/docs/engineering/` for architecture docs, API designs, data models, and infrastructure descriptions. Check `.chalk/docs/product/` for PRDs that describe the feature's intended behavior. You need to understand the system before modeling threats against it.

2. **Parse the target system** -- Extract from `$ARGUMENTS` the system, service, or component to threat model. If unspecified, ask the user to name the scope -- threat modeling the entire system at once is too broad to be useful.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/engineering/` to find the highest numbered file. The next number is `highest + 1`.

4. **Identify trust boundaries** -- Map the boundaries where data or control crosses between different trust levels: client/server, service/service, internal/external, user/admin, authenticated/unauthenticated. Each boundary is a potential attack surface.

5. **Apply STRIDE at each boundary** -- For each trust boundary, analyze:
   - **Spoofing**: Can an attacker impersonate a legitimate entity?
   - **Tampering**: Can data be modified in transit or at rest?
   - **Repudiation**: Can a user deny performing an action without detection?
   - **Information Disclosure**: Can sensitive data leak to unauthorized parties?
   - **Denial of Service**: Can the system be made unavailable?
   - **Elevation of Privilege**: Can a user gain unauthorized access levels?

6. **Rate and prioritize** -- For each threat, assess likelihood (low/medium/high) and impact (low/medium/high). Prioritize by risk = likelihood x impact.

7. **Recommend mitigations** -- For each threat rated medium or higher, provide a specific, actionable mitigation. Reference existing controls from the architecture docs where applicable.

8. **Write the file** -- Save to `.chalk/docs/engineering/<n>_threat_model_<system-slug>.md`.

9. **Confirm** -- Share the file path and highlight the top 3 highest-risk threats that need immediate attention.

## Output

- **File**: `.chalk/docs/engineering/<n>_threat_model_<system-slug>.md`
- **Format**: Plain markdown with trust boundary diagram (text-based), STRIDE analysis table, and prioritized mitigations
- **First line**: `# Threat Model: <System Name>`

## Anti-patterns

- **Boilerplate threats without system context** -- "SQL injection is a risk" is generic. Tie every threat to a specific trust boundary and data flow in the actual system.
- **No mitigations** -- A list of threats without mitigations is an anxiety generator, not a security tool. Every medium+ threat needs an actionable mitigation.
- **Scope too broad** -- Threat modeling "the application" produces shallow results. Scope to a specific component, service, or data flow for actionable depth.
- **Missing trust boundaries** -- If you only analyze the client-server boundary, you miss service-to-service, database access, third-party integrations, and admin interfaces. Map all boundaries.
- **One-time artifact** -- Note that threat models should be updated when the architecture changes. Flag sections that are most likely to become stale.
