---
name: running-coach-index
description: Reference catalog for all running coach AI skills, shared TypeScript contracts, safety guardrails, and telemetry conventions. Use when working with any running coach feature to understand data schemas, safety patterns, or integration points.
metadata:
  short-description: Catalog of AI skills, contracts, telemetry, and guardrails for Run-Smart.
  agent: cursor
---

## Purpose
Defines the shared conventions, contracts, safety posture, and telemetry used by all Run-Smart AI skills. This index allows Cursor Agent to discover available skills and the rules they follow.

## When Cursor should use this skill
- Before invoking any Run-Smart skill to understand shared schemas, safety guidance, and telemetry
- When onboarding a new skill to ensure compliance with common contracts
- When working with running coach features and need to understand data schemas or safety patterns
- When user asks about available AI capabilities or skill documentation

## Invocation guidance
1. Load shared references in `running-coach-index/references/` (contracts, telemetry, conventions, smoke-tests)
2. Select the appropriate skill directory based on the user's need (plan generation, adjustment, insights, etc.)
3. Validate request/response payloads against the schemas in `contracts.md` and skill-specific schemas
4. Always follow safety guardrails and emit SafetyFlags when thresholds are crossed
5. Log telemetry events via `v0/lib/analytics.ts` for monitoring and improvement

## Shared components
- **Contracts:** `running-coach-index/references/contracts.md` - TypeScript interfaces for all data structures
- **Telemetry:** `running-coach-index/references/telemetry.md` - Standard event logging patterns
- **Conventions:** `running-coach-index/references/conventions.md` - Naming, formatting, and design patterns
- **Smoke tests:** `running-coach-index/references/smoke-tests.md` - Quick validation scenarios

## Available Skills Catalog

### Planning & Generation
- **plan-generator** - Generates 14-21 day personalized training plans with safe load progression
- **plan-adjuster** - Recomputes upcoming workouts based on recent runs and feedback
- **conversational-goal-discovery** - Chat-based goal classification with constraint clarification

### Pre-Run Assessment
- **readiness-check** - Pre-run safety gate evaluating readiness (proceed/modify/skip decisions)
- **workout-explainer** - Translates planned workouts into execution cues and purpose explanations

### Post-Run Analysis
- **post-run-debrief** - Converts run telemetry into structured reflections with confidence scores
- **run-insights-recovery** - Analyzes completed runs for effort assessment and recovery recommendations

### Safety & Monitoring
- **load-anomaly-guard** - Detects unsafe training load spikes (>20-30% week-over-week)
- **adherence-coach** - Identifies missed sessions and proposes plan reshuffles with motivational support

### Advanced Features
- **race-strategy-builder** - Generates race-day pacing and fueling strategies
- **route-builder** - Generates route specifications with distance and elevation constraints

## Safety & guardrails

### Universal Safety Rules
1. **No Medical Diagnosis**: Never provide medical advice, diagnosis, or treatment recommendations
2. **Conservative Under Uncertainty**: When data is missing or uncertain, prefer safer, more conservative options
3. **Pain/Injury Signals**: If user reports pain, dizziness, chest discomfort, or severe symptoms:
   - Recommend stopping activity immediately
   - Advise consulting a qualified healthcare professional
   - Emit `SafetyFlag` with severity `high`
4. **Load Management**: Enforce hard caps on training load increases:
   - Weekly volume: max +20-30% increase
   - Long run: max +10-15% increase
   - Use `plan-complexity-engine.ts` for deterministic caps
5. **SafetyFlag Emission**: Emit structured `SafetyFlag` objects when:
   - Load thresholds exceeded
   - Critical data missing
   - Injury signals detected
   - Heat/weather risks present
   - Model confidence low (<50%)

### Data Handling
- Redact PII before logging telemetry
- Validate all inputs against schemas
- Handle missing data gracefully with appropriate defaults
- Never assume user state - always verify from database

### Model Behavior
- Prefer deterministic rules over probabilistic when safety is involved
- Fall back to template-based plans if AI generation fails
- Log all fallbacks and failures for monitoring
- Maintain consistent tone: supportive, evidence-based, non-alarmist

## Integration points

### API Routes
- **Chat**: `v0/app/api/chat/route.ts` - Conversational AI interactions
- **Plan Generation**: `v0/app/api/generate-plan/route.ts` - Training plan creation
- **Adjustments**: Background jobs (plan adjustment logic)
- **Insights**: Post-run screens (run analysis and recovery)

### Core Libraries
- **Enhanced AI Coach**: `v0/lib/enhanced-ai-coach.ts` - Skill orchestration and routing
- **Plan Generator**: `v0/lib/planGenerator.ts` - Plan creation logic
- **Plan Templates**: `v0/lib/plan-templates.ts` - Fallback templates
- **Recovery Engine**: `v0/lib/recoveryEngine.ts` - Recovery score calculations
- **Periodization**: `v0/lib/periodization.ts` - Training load management
- **Plan Complexity**: `v0/lib/plan-complexity-engine.ts` - Safety caps and thresholds

### Data Layer
- **Database**: `v0/lib/db.ts` - Dexie IndexedDB schema
- **DB Utils**: `v0/lib/dbUtils.ts` - Common database operations
- **Analytics**: `v0/lib/analytics.ts` - PostHog event tracking
- **Monitoring**: `v0/lib/backendMonitoring.ts` - Performance and error tracking

### UI Components
- **Today Screen**: Main dashboard with readiness check
- **Plan Screen**: Training calendar and workout details
- **Record Screen**: GPS tracking and run recording
- **Chat Screen**: Conversational AI interface
- **Profile Screen**: User settings and history

## Telemetry events (standard)

All skills should emit these standard events via `v0/lib/analytics.ts`:

- `ai_skill_invoked` - Every skill invocation with context
- `ai_plan_generated` - Training plan creation
- `ai_adjustment_applied` - Plan modifications
- `ai_insight_created` - Run analysis
- `ai_safety_flag_raised` - Safety warnings
- `ai_user_feedback` - User ratings and comments

See `references/telemetry.md` for detailed event schemas.

## Development workflow

### Adding a New Skill
1. Create skill directory: `.cursor/skills/skill-name/`
2. Write `SKILL.md` with metadata, description, and guidance
3. Create `references/` subdirectory
4. Add JSON schemas: `input-schema.json`, `output-schema.json`
5. Document examples in `examples.md`
6. Document edge cases in `edge-cases.md`
7. Update this index to include the new skill
8. Add integration code in relevant API routes/libraries
9. Add tests for the skill
10. Update CURSOR.md with skill description

### Testing Skills
- Use smoke tests from `references/smoke-tests.md`
- Verify safety guardrails with edge case inputs
- Test fallback behavior when data is missing
- Validate telemetry event emission
- Check SafetyFlag generation for risky scenarios

### Monitoring Skills
- Check `v0/lib/backendMonitoring.ts` for error rates
- Review PostHog analytics for usage patterns
- Monitor SafetyFlag frequency and severity
- Track user feedback ratings
- Analyze model latency and performance

## Version History
- **v1.0** (2026-01-23): Initial Cursor Agent skills system with 12 core skills
