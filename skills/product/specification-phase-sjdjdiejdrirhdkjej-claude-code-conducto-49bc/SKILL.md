---
name: specification-phase
description: Provides standard operating procedures for the /specify phase including feature classification (HAS_UI, IS_IMPROVEMENT, HAS_METRICS, HAS_DEPLOYMENT_IMPACT), research depth determination, clarification strategy (max 3, informed guesses for defaults), and roadmap integration. Use when executing /specify command, classifying features, generating structured specs, or determining research depth for planning phase. (project)
---

<objective>
Transform natural language feature requests into structured specifications that enable planning and implementation through systematic classification, informed guess strategy, and minimal clarification approach.

This skill orchestrates the /specify phase, producing spec.md with measurable success criteria, classification flags for downstream workflows, and maximum 3 clarifications using informed guess heuristics for technical defaults.

**Core responsibilities**:

- Parse and normalize feature input to slug format (kebab-case, no filler words)
- Check roadmap integration to reuse existing context
- Load project documentation context (docs/project/) to prevent hallucination
- Classify feature with 4 flags (HAS_UI, IS_IMPROVEMENT, HAS_METRICS, HAS_DEPLOYMENT_IMPACT)
- Determine research depth based on complexity (FLAG_COUNT: 0→minimal, 1→standard, ≥2→full)
- Apply informed guess strategy for non-critical technical decisions
- Generate ≤3 clarifications (only scope/security critical)
- Write measurable success criteria (quantifiable, user-facing)

Inputs: User's feature description, existing roadmap entries, project docs (if exists), codebase context
Outputs: specs/NNN-slug/spec.md, NOTES.md, state.yaml, updated roadmap (if FROM_ROADMAP=true)
Expected duration: 10-15 minutes
</objective>

<quick_start>
Execute /specify workflow in 9 steps:

1. **Parse and normalize input** - Generate slug (remove filler words: "add", "create", "we want to"), assign feature number (NNN)
2. **Check roadmap integration** - Search roadmap for slug match, reuse context if found (saves ~10 minutes)
3. **Load project documentation** - Extract tech stack, API patterns, existing entities from docs/project/ (prevents hallucination)
4. **Classify feature** - Set HAS_UI, IS_IMPROVEMENT, HAS_METRICS, HAS_DEPLOYMENT_IMPACT flags using decision tree
5. **Determine research depth** - FLAG_COUNT → minimal (0), standard (1), full (≥2)
6. **Apply informed guess strategy** - Use defaults for performance (<500ms), rate limits (100/min), auth (OAuth2), retention (90d logs)
7. **Generate clarifications** - Max 3 critical clarifications (scope > security > UX > technical priority matrix)
8. **Write success criteria** - Measurable, quantifiable, user-facing outcomes (not tech-specific)
9. **Generate artifacts and commit** - Create spec.md, NOTES.md, state.yaml, update roadmap

Key principle: Use informed guesses for non-critical decisions, document assumptions, limit clarifications to ≤3.
</quick_start>

<prerequisites>
<environment_checks>
Before executing /specify phase:
- [ ] Git working tree clean (no uncommitted changes)
- [ ] Not on main branch (create feature branch: `feature/NNN-slug`)
- [ ] Required templates exist in `.spec-flow/templates/`
- [ ] If project docs exist, docs/project/ directory accessible
</environment_checks>

<knowledge_requirements>
Required understanding before execution:

- **Classification decision tree**: UI keywords vs backend-only exclusions, improvement = baseline + target, metrics = user tracking, deployment = env vars/migrations/breaking changes
- **Informed guess heuristics**: Performance (<500ms), retention (90d logs, 365d analytics), rate limits (100/min), auth (OAuth2), error handling (user-friendly + error ID)
- **Clarification prioritization matrix**: Critical (scope, security, breaking changes) > High (UX) > Medium (performance SLA, tech stack) > Low (error messages, rate limits)
- **Slug generation rules**: Remove filler words, lowercase kebab-case, 50 char limit, fuzzy match roadmap

See [reference.md](reference.md) for complete decision trees and heuristics.
</knowledge_requirements>

<warnings>
- **Over-clarification**: >3 clarifications indicates missing informed guesses (check reference.md for defaults)
- **Wrong classification**: Backend workers/APIs with HAS_UI=true wastes time generating UI artifacts
- **Roadmap mismatch**: Filler words in slug prevent roadmap match ("add-student-dashboard" vs "student-dashboard")
- **Vague success criteria**: "Works correctly", "is fast", "looks good" are not measurable - use quantifiable metrics
</warnings>
</prerequisites>

<workflow>
<step number="1">
**Parse and Normalize Input**

Extract feature description and generate clean slug.

**Slug Generation Rules**:

```bash
# Remove filler words and normalize
echo "$ARGUMENTS" |
  sed 's/\bwe want to\b//gi; s/\bI want to\b//gi' |
  sed 's/\badd\b//gi; s/\bcreate\b//gi; s/\bimplement\b//gi' |
  sed 's/\bget our\b//gi; s/\bto a\b//gi; s/\bwith\b//gi' |
  tr '[:upper:]' '[:lower:]' |
  sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' |
  cut -c1-50
```

**Example**:

- Input: "We want to add student progress dashboard"
- Slug: `student-progress-dashboard` ✅
- Number: 042
- Directory: `specs/042-student-progress-dashboard/`

**Quality Check**: Slug is concise, descriptive, no filler words, matches roadmap format.

See [reference.md § Slug Generation Rules](reference.md#slug-generation-rules) for detailed normalization logic.
</step>

<step number="2">
**Check Roadmap Integration**

Search roadmap for existing entry to reuse context.

**Detection Logic**:

```bash
SLUG="student-progress-dashboard"
if grep -qi "^### ${SLUG}" .spec-flow/memory/roadmap.md; then
  FROM_ROADMAP=true
  # Extract requirements, area, role, impact/effort scores
  # Move entry from "Backlog"/"Next" to "In Progress"
  # Add branch and spec links
fi
```

**Benefits**:

- Saves ~10 minutes (requirements already documented)
- Automatic status tracking (roadmap updates)
- Context reuse (user already vetted scope)

**Quality Check**: If roadmap match found, extracted requirements appear in spec.md.

See [reference.md § Roadmap Integration](reference.md#roadmap-integration) for fuzzy matching logic.
</step>

<step number="3">
**Load Project Documentation Context**

Extract architecture constraints from `docs/project/` to prevent hallucination.

**Detection**:

```bash
if [ -d "docs/project" ]; then
  HAS_PROJECT_DOCS=true
  # Extract tech stack, API patterns, entities
else
  echo "ℹ️  No project documentation (run /init-project recommended)"
  HAS_PROJECT_DOCS=false
fi
```

**Extraction**:

```bash
# Extract constraints from project docs
FRONTEND=$(grep -A 1 "| Frontend" docs/project/tech-stack.md | tail -1)
DATABASE=$(grep -A 1 "| Database" docs/project/tech-stack.md | tail -1)
API_STYLE=$(grep -A 1 "## API Style" docs/project/api-strategy.md | tail -1)
ENTITIES=$(grep -oP '[A-Z_]+(?= \{)' docs/project/data-architecture.md)
```

**Document in NOTES.md**:

```markdown
## Project Documentation Context

**Tech Stack Constraints** (from tech-stack.md):

- Frontend: Next.js 14
- Database: PostgreSQL

**Spec Requirements**:

- ✅ MUST use documented tech stack
- ✅ MUST follow API patterns from api-strategy.md
- ✅ MUST check for duplicate entities before proposing new ones
- ❌ MUST NOT hallucinate MongoDB if PostgreSQL is documented
```

**Quality Check**: NOTES.md includes project context section with constraints.

**Skip if**: No docs/project/ directory exists (warn user but don't block).
</step>

<step number="4">
**Classify Feature**

Set classification flags using decision tree.

**Classification Logic**:

**HAS_UI** (user-facing screens/components):

```
UI keywords: screen, page, dashboard, form, modal, component, frontend, interface
  → BUT NOT backend-only: API, endpoint, service, worker, cron, job, migration, health check
  → HAS_UI = true

Example: "Add student dashboard" → HAS_UI = true ✅
Example: "Add background worker" → HAS_UI = false ✅ (backend-only)
```

**IS_IMPROVEMENT** (optimization with measurable baseline):

```
Improvement keywords: improve, optimize, enhance, speed up, reduce time
  AND baseline: existing, current, slow, faster, better
  → IS_IMPROVEMENT = true

Example: "Improve search performance from 3.2s to <500ms" → IS_IMPROVEMENT = true ✅
Example: "Make search faster" → IS_IMPROVEMENT = false ❌ (no baseline)
```

**HAS_METRICS** (user behavior tracking):

```
Metrics keywords: track user, measure user, engagement, retention, conversion, analytics, A/B test
  → HAS_METRICS = true

Example: "Track dashboard engagement" → HAS_METRICS = true ✅
```

**HAS_DEPLOYMENT_IMPACT** (env vars, migrations, breaking changes):

```
Deployment keywords: migration, schema change, env variable, breaking change, docker, platform change
  → HAS_DEPLOYMENT_IMPACT = true

Example: "OAuth authentication (needs env vars)" → HAS_DEPLOYMENT_IMPACT = true ✅
```

**Quality Check**: Classification matches feature intent. No UI artifacts for backend workers.

See [reference.md § Classification Decision Tree](reference.md#classification-decision-tree) for complete logic.
</step>

<step number="5">
**Determine Research Depth**

Select research depth based on complexity (FLAG_COUNT).

**Research Depth Guidelines**:

| FLAG_COUNT | Depth    | Tools | Use Cases                                       |
| ---------- | -------- | ----- | ----------------------------------------------- |
| 0          | Minimal  | 1-2   | Simple backend endpoint, config change          |
| 1          | Standard | 3-5   | Single-aspect feature (UI-only or backend-only) |
| ≥2         | Full     | 5-8   | Complex multi-aspect feature                    |

**Minimal Research** (FLAG_COUNT = 0):

1. Constitution check (alignment with mission/values)
2. Grep for similar patterns

**Standard Research** (FLAG_COUNT = 1):
1-2. Minimal research 3. UI inventory scan (if HAS_UI=true) 4. Performance budgets check 5. Similar spec search

**Full Research** (FLAG_COUNT ≥ 2):
1-5. Standard research 6. Design inspirations (if HAS_UI=true) 7. Web search for novel patterns 8. Integration points analysis

**Quality Check**: Research depth matches complexity. Don't over-research simple features.

See [reference.md § Research Depth Guidelines](reference.md#research-depth-guidelines) for tool selection logic.
</step>

<step number="6">
**Apply Informed Guess Strategy**

Use defaults for non-critical technical decisions.

**Use Informed Guesses For** (do NOT clarify):

- **Performance targets**: API <500ms (95th percentile), Frontend FCP <1.5s, TTI <3.0s
- **Data retention**: User data indefinite (with deletion option), Logs 90 days, Analytics 365 days
- **Error handling**: User-friendly messages + error ID (ERR-XXXX), logging to error-log.md
- **Rate limiting**: 100 requests/minute per user, 1000/minute per IP
- **Authentication**: OAuth2 for users, JWT for APIs, MFA optional (users), required (admins)
- **Integration patterns**: RESTful API (unless GraphQL needed), JSON format, offset/limit pagination

**Document Assumptions in spec.md**:

```markdown
## Performance Targets (Assumed)

- API endpoints: <500ms (95th percentile)
- Frontend FCP: <1.5s, TTI: <3.0s
- Lighthouse: Performance ≥85, Accessibility ≥95

_Assumption: Standard web application performance expectations applied._
```

**Do NOT Use Informed Guesses For**:

- Scope-defining decisions (feature boundary, user roles)
- Security/privacy critical choices (encryption, PII handling)
- Breaking changes (API response format changes)
- No reasonable default exists (business logic decisions)

**Quality Check**: No clarifications for decisions with industry-standard defaults.

See [reference.md § Informed Guess Heuristics](reference.md#informed-guess-heuristics) for complete defaults catalog.
</step>

<step number="7">
**Generate Clarifications (Max 3)**

Identify ambiguities that cannot be reasonably assumed.

**Clarification Prioritization Matrix**:

| Category         | Priority | Ask?             | Example                                                   |
| ---------------- | -------- | ---------------- | --------------------------------------------------------- |
| Scope boundary   | Critical | ✅ Always        | "Does this include admin features or only user features?" |
| Security/Privacy | Critical | ✅ Always        | "Should PII be encrypted at rest?"                        |
| Breaking changes | Critical | ✅ Always        | "Is it okay to change the API response format?"           |
| User experience  | High     | ✅ If ambiguous  | "Should this be a modal or new page?"                     |
| Performance SLA  | Medium   | ❌ Use defaults  | "What's the target response time?" → Assume <500ms        |
| Technical stack  | Medium   | ❌ Defer to plan | "Which database?" → Planning-phase decision               |
| Error messages   | Low      | ❌ Use standard  | "What error message?" → Standard pattern                  |
| Rate limits      | Low      | ❌ Use defaults  | "How many requests?" → 100/min default                    |

**Limit: Maximum 3 clarifications total**

**Process**:

1. Identify all ambiguities
2. Rank by category priority
3. Keep top 3 most critical
4. Make informed guesses for remaining
5. Document assumptions clearly

**Good Clarifications**:

```markdown
[NEEDS CLARIFICATION: Should dashboard show all students or only assigned classes?]
[NEEDS CLARIFICATION: Should parents have access to this dashboard?]
```

**Bad Clarifications** (have defaults):

```markdown
❌ [NEEDS CLARIFICATION: What's the target response time?] → Use 500ms default
❌ [NEEDS CLARIFICATION: Which database to use?] → Planning-phase decision
❌ [NEEDS CLARIFICATION: What error message format?] → Use standard pattern
```

**Quality Check**: ≤3 clarifications total, all are scope/security/UX critical.

See [reference.md § Clarification Prioritization Matrix](reference.md#clarification-prioritization-matrix) for complete ranking system.
</step>

<step number="8">
**Write Success Criteria**

Define measurable, quantifiable, user-facing outcomes.

**Good Criteria Format**:

```markdown
## Success Criteria

- User can complete registration in <3 minutes (measured via PostHog funnel)
- API response time <500ms for 95th percentile (measured via Datadog APM)
- Lighthouse accessibility score ≥95 (measured via CI Lighthouse check)
- 95% of user searches return results in <1 second
```

**Criteria Requirements**:

- **Measurable**: Can be validated objectively
- **Quantifiable**: Has specific numeric target
- **User-facing**: Focuses on outcomes, not implementation
- **Measurement method**: Specifies how to validate (tool, metric)

**Bad Criteria to Avoid**:

```markdown
❌ System works correctly (not measurable)
❌ API is fast (not quantifiable)
❌ UI looks good (subjective)
❌ React components render efficiently (technology-specific, not outcome-focused)
```

**Quality Check**: Every criterion is measurable, quantifiable, and outcome-focused.
</step>

<step number="9">
**Generate Artifacts and Commit**

Create specification artifacts and commit to git.

**Artifacts**:

1. `specs/NNN-slug/spec.md` - Structured specification with classification flags, requirements, assumptions, clarifications (≤3), success criteria
2. `specs/NNN-slug/NOTES.md` - Implementation decisions and project context
3. `specs/NNN-slug/visuals/README.md` - Visual artifacts directory (if HAS_UI=true)
4. `specs/NNN-slug/state.yaml` - Phase state tracking (currentPhase: specification, status: completed)
5. Updated roadmap (if FROM_ROADMAP=true) - Move entry to "In Progress", add branch/spec links

**Validation Checks**:

- [ ] Requirements checklist complete (if exists)
- [ ] Clarifications ≤3
- [ ] Classification flags match feature description
- [ ] Success criteria are measurable
- [ ] Roadmap updated (if FROM_ROADMAP=true)

**Commit Message**:

```bash
git add specs/NNN-slug/
git commit -m "feat: add spec for <feature-name>

Generated specification with classification:
- HAS_UI: <true/false>
- IS_IMPROVEMENT: <true/false>
- HAS_METRICS: <true/false>
- HAS_DEPLOYMENT_IMPACT: <true/false>

Clarifications: N
Research depth: <minimal/standard/full>"
```

**Quality Check**: All artifacts created, spec committed, roadmap updated, state.yaml initialized.
</step>
</workflow>

<validation>
<phase_checklist>
**Pre-phase checks**:
- [ ] Git working tree clean
- [ ] Not on main branch
- [ ] Required templates exist

**During phase**:

- [ ] Slug normalized (no filler words, lowercase kebab-case)
- [ ] Roadmap checked for existing entry
- [ ] Project docs loaded (if exist)
- [ ] Classification flags validated (no conflicting keywords)
- [ ] Research depth appropriate for complexity (FLAG_COUNT-based)
- [ ] Clarifications ≤3 (use informed guesses for rest)
- [ ] Success criteria measurable and quantifiable
- [ ] Assumptions documented clearly

**Post-phase validation**:

- [ ] spec.md committed with proper message
- [ ] NOTES.md initialized
- [ ] Roadmap updated (if FROM_ROADMAP=true)
- [ ] visuals/ created (if HAS_UI=true)
- [ ] state.yaml initialized
      </phase_checklist>

<quality_standards>
**Specification quality targets**:

- Clarifications: ≤3 per spec
- Classification accuracy: ≥90%
- Success criteria: 100% measurable
- Time to spec: ≤15 minutes
- Rework rate: <5%

**What makes a good spec**:

- Clear scope boundaries (what's in, what's out)
- Measurable success criteria (with measurement methods)
- Reasonable assumptions documented
- Minimal clarifications (only critical scope/security)
- Correct classification (matches feature intent)
- Context reuse (from roadmap when available)

**What makes a bad spec**:

- > 5 clarifications (over-clarifying technical defaults)
- Vague success criteria ("works correctly", "is fast")
- Technology-specific criteria (couples to implementation)
- Wrong classification (UI flag for backend-only)
- Missing roadmap integration (duplicates planning work)
  </quality_standards>
  </validation>

<anti_patterns>
<pitfall name="over_clarification">
**Impact**: Delays planning phase, frustrates users

**Scenario**:

```
Spec with 7 clarifications (limit: 3):
- [NEEDS CLARIFICATION: What format? CSV or JSON?] → Use JSON default
- [NEEDS CLARIFICATION: Rate limiting strategy?] → Use 100/min default
- [NEEDS CLARIFICATION: Maximum file size?] → Use 50MB default
```

**Prevention**:

- Use industry-standard defaults (see reference.md § Informed Guess Heuristics)
- Only mark critical scope/security decisions as NEEDS CLARIFICATION
- Document assumptions in spec.md "Assumptions" section
- Prioritize by impact: scope > security > UX > technical

**If encountered**: Reduce to 3 most critical, convert others to documented assumptions.
</pitfall>

<pitfall name="wrong_classification">
**Impact**: Creates unnecessary UI artifacts, wastes time

**Scenario**:

```
Feature: "Add background worker to process uploads"
Classified: HAS_UI=true (WRONG - no user-facing UI)
Result: Generated screens.yaml for backend-only feature
```

**Root cause**: Keyword "process" triggered false positive without checking for backend-only keywords

**Prevention**:

1. Check for backend-only keywords: worker, cron, job, migration, health check, API, endpoint, service
2. Require BOTH UI keyword AND absence of backend-only keywords
3. Use classification decision tree (see reference.md § Classification Decision Tree)
   </pitfall>

<pitfall name="roadmap_slug_mismatch">
**Impact**: Misses context reuse opportunity, duplicates planning work

**Scenario**:

```
User input: "We want to add Student Progress Dashboard"
Generated slug: "add-student-progress-dashboard" (BAD - includes "add")
Roadmap entry: "### student-progress-dashboard" (slug without "add")
Result: No match found, created fresh spec instead of reusing roadmap context
```

**Prevention**:

1. Remove filler words during slug generation: "add", "create", "we want to"
2. Normalize to lowercase kebab-case consistently
3. Offer fuzzy matches if exact match not found
   </pitfall>

<pitfall name="too_many_research_tools">
**Impact**: Wastes time, exceeds token budget

**Scenario**:

```bash
# 15 research tools for simple backend endpoint (WRONG)
Glob *.py, Glob *.ts, Glob *.tsx, Grep "database", Grep "model"...
```

**Prevention**:

- Use research depth guidelines: FLAG_COUNT = 0 → 1-2 tools only
- For simple features: Constitution check + pattern search is sufficient
- Reserve full research (5-8 tools) for complex multi-aspect features

**Correct approach**:

```bash
# 2 research tools for simple backend endpoint (CORRECT)
grep "similar endpoint" specs/*/spec.md
grep "BaseModel" api/app/models/*.py
```

</pitfall>

<pitfall name="vague_success_criteria">
**Impact**: Cannot validate implementation, leads to scope creep

**Bad examples**:

```markdown
❌ System works correctly (not measurable)
❌ API is fast (not quantifiable)
❌ UI looks good (subjective)
```

**Good examples**:

```markdown
✅ User can complete registration in <3 minutes (measured via PostHog funnel)
✅ API response time <500ms for 95th percentile (measured via Datadog APM)
✅ Lighthouse accessibility score ≥95 (measured via CI Lighthouse check)
```

**Prevention**: Every criterion must answer: "How do we measure this objectively?"
</pitfall>

<pitfall name="technology_specific_criteria">
**Impact**: Couples spec to implementation details, reduces flexibility

**Bad examples**:

```markdown
❌ React components render efficiently
❌ Redis cache hit rate >80%
❌ PostgreSQL queries use proper indexes
```

**Good examples** (outcome-focused):

```markdown
✅ Page load time <1.5s (First Contentful Paint)
✅ 95% of user searches return results in <1 second
✅ Database queries complete in <100ms average
```

**Prevention**: Focus on user-facing outcomes, not implementation mechanisms.
</pitfall>
</anti_patterns>

<best_practices>
<informed_guess_strategy>
**When to use**:

- Non-critical technical decisions
- Industry standards exist
- Default won't impact scope or security

**When NOT to use**:

- Scope-defining decisions
- Security/privacy critical choices
- No reasonable default exists

**Approach**:

1. Check if decision has reasonable default (see reference.md § Informed Guess Heuristics)
2. Document assumption clearly in spec
3. Note that user can override if needed

**Example**:

```markdown
## Performance Targets (Assumed)

- API response time: <500ms (95th percentile)
- Frontend FCP: <1.5s
- Database queries: <100ms

**Assumptions**:

- Standard web app performance expectations applied
- If requirements differ, specify in "Performance Requirements" section
```

**Result**: Reduces clarifications from 5-7 to 0-2, saves ~10 minutes
</informed_guess_strategy>

<roadmap_integration>
**When to use**:

- Feature name matches roadmap entry
- Roadmap uses consistent slug format

**Approach**:

1. Normalize user input to slug format
2. Search roadmap for exact match
3. If found: Extract requirements, area, role, impact/effort
4. Move to "In Progress" section automatically
5. Add branch and spec links

**Result**: Saves ~10 minutes, requirements already vetted, automatic status tracking
</roadmap_integration>

<classification_decision_tree>
**Best practice**: Follow decision tree systematically (see reference.md § Classification Decision Tree)

**Process**:

1. Check UI keywords → Set HAS_UI (but verify no backend-only exclusions)
2. Check improvement keywords + baseline → Set IS_IMPROVEMENT
3. Check metrics keywords → Set HAS_METRICS
4. Check deployment keywords → Set HAS_DEPLOYMENT_IMPACT

**Result**: 90%+ classification accuracy, correct artifacts generated
</classification_decision_tree>
</best_practices>

<success_criteria>
Specification phase complete when:

- [ ] All pre-phase checks passed
- [ ] All 9 execution steps completed
- [ ] All post-phase validations passed
- [ ] Spec committed to git
- [ ] state.yaml shows `currentPhase: specification` and `status: completed`

Ready to proceed when:

- If clarifications >0 → Run `/clarify`
- If clarifications = 0 → Run `/plan`
  </success_criteria>

<troubleshooting>
**Issue**: Too many clarifications (>3)
**Solution**: Review reference.md § Informed Guess Heuristics for defaults, convert non-critical questions to assumptions

**Issue**: Classification seems wrong
**Solution**: Re-check decision tree, verify no backend-only keywords for HAS_UI=true

**Issue**: Roadmap entry exists but wasn't matched
**Solution**: Check slug normalization, offer fuzzy matches, update roadmap slug format

**Issue**: Success criteria are vague
**Solution**: Add quantifiable metrics and measurement methods, focus on user-facing outcomes

**Issue**: Research depth excessive for simple feature
**Solution**: Follow FLAG_COUNT guidelines (0→minimal, 1→standard, ≥2→full)

**Issue**: Project context missing/incomplete
**Solution**: Run /init-project to generate docs/project/, or manually create tech-stack.md and api-strategy.md
</troubleshooting>

<reference_guides>
For detailed documentation:

**Classification & Defaults**: [reference.md](reference.md)

- Classification decision tree (HAS_UI, IS_IMPROVEMENT, HAS_METRICS, HAS_DEPLOYMENT_IMPACT)
- Informed guess heuristics (performance, retention, auth, rate limits)
- Clarification prioritization matrix (scope > security > UX > technical)
- Slug generation rules (normalization, filler word removal)

**Real-World Examples**: [examples.md](examples.md)

- Good specs (0-2 clarifications) vs bad specs (>5 clarifications)
- Side-by-side comparisons with analysis
- Progressive learning patterns (features 1-5, 6-15, 16+)
- Classification accuracy examples

**Execution Details**: reference.md § Research Depth Guidelines, Common Mistakes to Avoid

Next phase after /specify:

- If clarifications >0 → `/clarify` (reduces ambiguity via targeted questions)
- If clarifications = 0 → `/plan` (generates design artifacts from spec)
  </reference_guides>
