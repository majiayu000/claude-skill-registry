---
name: skill-builder-medical
description: Specialized guide for creating Claude Code skills for Dr. Sophia AI medical system. Includes healthcare integration patterns (FHIR/REST/EHR), medical compliance validation (HIPAA/PBS/TGA), botanical design integration, Railway deployment patterns, and proven examples from our 7 production skills. Use when creating skills specifically for Dr. Sophia AI, medical integration skills, healthcare compliance skills, EHR workflows, or adapting our proven skill patterns.
---

# Dr. Sophia AI Medical Skill Builder

## Overview

Specialized guide for creating Claude Code skills for Dr. Sophia AI medical system. Built on skill-builder-generic foundation, adds healthcare-specific patterns, compliance validation, and references our 7 proven production skills.

## When to Use This Skill

- Creating skills for Dr. Sophia AI
- Medical integration skills (FHIR/REST/EHR)
- Healthcare compliance skills
- Adapting our proven patterns
- Medical testing frameworks

## Quick Start

For universal skill patterns, use skill-builder-generic first.

This medical builder adds Dr. Sophia AI specifics:
- HIPAA compliance
- Botanical design integration
- Railway deployment patterns
- MediRecords FHIR/REST APIs
- Our 7 proven skills as templates

## Healthcare Integration Patterns

### Pattern 1: Medical API Integration
See: medirecords-integration skill (our proven example)
- Two-phase FHIR/REST workflow
- API credentials handling
- SOAP notes formatting

### Pattern 2: Design System Skills
See: botanical-design skill
- Botanical color palette (#00B368 spectrum)
- Typography (Livvic/Onest fonts)
- Component templates

### Pattern 3: Deployment Skills
See: deployment-guide, railway-troubleshooting
- Railway-specific workflows
- Environment-aware builds
- Docker cache handling

### Pattern 4: Testing Skills
See: saudi-patient-testing
- Patient test frameworks
- Data separation principle
- Safety validation

## Our 7 Skills as Examples

All in: .claude/skills/
1. botanical-design - Design system pattern
2. medirecords-integration - API integration
3. deployment-guide - Deployment workflow
4. modal-patterns - React UI
5. railway-troubleshooting - Debugging
6. wearables-setup - OAuth integration
7. saudi-patient-testing - Testing framework

## Medical-Specific Requirements

**HIPAA Compliance:**
- No PHI in examples (use placeholders)
- Template credentials (never real)
- Sanitize logs

**Botanical Brand:**
- Use #00B368 green spectrum
- Livvic/Onest fonts
- Reference botanical-design skill

**Railway Deployment:**
- Environment-aware (dev/prod)
- Frontend: npm run build required
- Backend: auto-deploy from source

---

**Version:** 1.0
**Built On:** skill-builder-generic
**Examples:** 7 proven Dr. Sophia AI skills
**Last Updated:** October 25, 2025
