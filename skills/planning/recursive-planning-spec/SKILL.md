---
name: recursive-planning-spec
description: Recursively decompose a feature into a complete PlanGraph (Intent→…→InteractionSpec) using Nonterminal Expansion and P1–P13 Completion Proofs. Emit delta-only outputs (manifest + deltas + changed nodes), deterministic task order, no code generation. Designed to converge to 100% without guessing. Includes systematic UI expansion for all user-facing nodes (Screen, NavigationSpec, UIComponentContract, SettingsSpec, TutorialSpec, NotificationSpec, BadgeRule, VisualSpec).
---

# Recursive Planning Spec (Skill)

## What this Skill does
- Builds/updates a **PlanGraph** until every branch reaches **InteractionSpecs** (method × interface × operation × state cluster).
- Enforces **Nonterminal Expansion**: a parent cannot be `Ready` until all required child types exist and pass checklists.
- **Systematically projects UI implications** for all user-facing nodes via the UI Implications Questionnaire, generating Screen, NavigationSpec, UIComponentContract, SettingsSpec, TutorialSpec, NotificationSpec, BadgeRule, and VisualSpec nodes.
- Produces **delta-only** outputs in small shards (manifest, deltas, changed nodes) to fit tight context budgets.
- Blocks guessing with **OpenQuestion**; requires **P1–P13 Completion Proofs** before declaring "done."
- Keeps documentation DRY by referencing node IDs instead of inlining large bodies.
- **Plans for depth, not just breadth**: Captures end-to-end flows, architecture patterns, business logic, cross-cutting concerns, and complete UI/UX alongside individual operations.

## When to use
- Any planning pass that must recurse to terminal leaves and *prove* completeness.
- When previous plans looked "big" but contained stubs, guesses, or missing tests/observability.
- When UI/UX planning needs to be systematic and comprehensive, not ad-hoc.

## Inputs and Outputs (per pass)

**Input JSON**
```json
{
  "feature_id": "feat:<slug>",
  "intent": "<one sentence>",
  "prior_plan_version": "vN",
  "knobs": {
    "budgets": {"pass_kb": 8, "node_kb": 3, "max_interactions_per_pass": 40},
    "weights": {"trace":0.25,"ix_cov":0.25,"check":0.20,"risk":0.15,"closure":0.15},
    "lanes": ["Client","API","Worker","Data","Policy","Observability","QA","Migrations","Design"],
    "semver": {"contracts_default":"minor","breaking_requires":"migration_spec"},
    "refactor_caps": {"max_refactors_per_pass": 3},
    "ui_expansion": {"enabled": true, "require_design_system": true}
  }
}
```

**Output JSON**
```json
{
  "plan_version": "v{K}",
  "deltas": [ /* delta ops only */ ],
  "task_order": [ /* ordered leaves with lanes & deps */ ],
  "top_gaps": [ /* unaccounted highlights */ ],
  "changed_nodes": [ /* ids */ ],
  "manifest": {
    "stats": {"nodes":0,"edges":0,"ready":0,"blocked":0,"ui_nodes":0},
    "hotset": {"changed": ["..."], "deferred": ["..."]}
  },
  "proofs": {
    "P1": true, "P2": true, "P3": true, "P4": true,
    "P5": true, "P6": true, "P7": true, "P8": true, "P9": true,
    "P10": true, "P11": true, "P12": true, "P13": true,
    "details": { /* matrices and lists */ }
  }
}
```

## Guardrails (Sycophancy Avoidance)
- **Verify-First Chaining**: list 3 first-principles risks; convert unresolved items to `OpenQuestion`; only then proceed.
- **Rude Persona Check**: add a blunt 2-line critique: "What breaks? What's missing?"
- **Adversarial Critique Pairing**: after proposing deltas, run a critic pass; merge only resolved items; unresolved → `OpenQuestion`.
- **Abstention Calibration**: if confidence <80% on any node, output `INSUFFICIENT` with targeted questions; block that branch.
- **Ensemble Note**: where designs diverge, list ≥2 options; pick one; record rationale in `node.evidence`.

## UI Projection Enforcement (Critical - Duke's Feedback + v44/v45 Learnings)

**MANDATORY: These rules override all other planning rules when user-facing features are involved.**

### Screen Salvage Pattern (v45 Learning - APPLY BEFORE DELETION)

**Lesson Learned (v45)**: When node type classification identifies misclassified "screens", DO NOT just delete them. Many represent legitimate UI requirements that should be converted to the proper artifact type.

**BEFORE deleting any misclassified screen**, classify what it SHOULD be:

```python
def salvage_misclassified_screen(screen_node):
    """
    Convert misclassified 'Screen' nodes to proper artifact types instead of deleting.

    Lesson: v45 had 169 screens, 148 were misclassified. Salvage analysis found 83.4%
    represented real UI needs (dashboards, settings, components) not standalone screens.
    """

    # Read screen purpose/statement
    purpose = screen_node.stmt.lower()

    # Classification decision tree

    # 1. Is it monitoring/analytics data? → Dashboard panel
    if any(keyword in purpose for keyword in [
        "analytics", "metrics", "monitoring", "observability",
        "logs", "traces", "alerts", "slo"
    ]):
        return convert_to_dashboard_panel(screen_node)
        # Creates: Dashboard node with panel definition
        # Example: screen:analytics → dashboard:admin-observability (panel: "Analytics Overview")

    # 2. Is it configuration/settings? → Settings section
    if any(keyword in purpose for keyword in [
        "config", "settings", "preferences", "feature flag",
        "toggle", "enable", "disable"
    ]):
        return convert_to_settings_section(screen_node)
        # Creates: SettingsSpec node or adds section to existing settings
        # Example: screen:feature-flags-config → settings:app-config (section: "Feature Flags")

    # 3. Is it a UI element within another screen? → Component
    if any(keyword in purpose for keyword in [
        "modal", "drawer", "overlay", "widget", "panel",
        "notification", "toast", "banner", "indicator"
    ]):
        return convert_to_component(screen_node)
        # Creates: UIComponentContract
        # Example: screen:notifications → component:notification-drawer

    # 4. Is it admin/developer-only? → Admin tool
    if any(keyword in purpose for keyword in [
        "admin", "debug", "developer", "internal tool"
    ]):
        return convert_to_admin_tool(screen_node)
        # Creates: AdminDashboard
        # Example: screen:agent-access → admin-dashboard:developer-tools

    # 5. Is it a modal/wizard flow? → UX Flow
    if any(keyword in purpose for keyword in [
        "wizard", "flow", "step", "onboarding", "tutorial"
    ]):
        return convert_to_ux_flow(screen_node)
        # Creates: UXFlow + UIComponentContract (modal)
        # Example: screen:onboarding → uxflow:user-onboarding

    # 6. Pure backend operation? → Delete (no UI)
    if any(keyword in purpose for keyword in [
        "worker processes", "cache stores", "queue", "background job",
        "backend", "internal process"
    ]):
        return delete_no_ui_needed(screen_node)
        # Creates: Nothing (legitimate deletion)
        # Example: screen:queues-workers-worker-processes-job → DELETE

    # 7. Legitimate standalone screen? → Keep
    return {"action": "keep", "node": screen_node}
```

**Salvage Conversion Functions**:

```python
def convert_to_dashboard_panel(screen_node):
    """Convert monitoring/analytics screen to dashboard panel."""

    # Group related screens into dashboards
    if "admin" in screen_node.id or "observability" in screen_node.id:
        dashboard_id = "dashboard:admin-observability"
    elif "analytics" in screen_node.id:
        dashboard_id = "dashboard:analytics"
    else:
        dashboard_id = "dashboard:metrics"

    # Extract metrics from screen purpose
    metrics = extract_metrics_from_purpose(screen_node.stmt)

    return {
        "action": "convert",
        "delete": [screen_node.id],
        "create": [{
            "id": dashboard_id,
            "type": "Dashboard",
            "stmt": f"Dashboard for {screen_node.stmt}",
            "panels": [{
                "name": screen_node.title or screen_node.id,
                "metrics": metrics,
                "source": screen_node.id  # Traceability
            }]
        }],
        "edges": [
            {"from": "scenario:<original>", "to": dashboard_id, "type": "satisfied_by"}
        ]
    }

def convert_to_settings_section(screen_node):
    """Convert configuration screen to settings section."""

    # Group related settings
    settings_id = "settings:app-config"

    # Extract controls from screen purpose
    controls = extract_controls_from_purpose(screen_node.stmt)

    return {
        "action": "convert",
        "delete": [screen_node.id],
        "create_or_update": [{
            "id": settings_id,
            "type": "SettingsSpec",
            "sections": [{
                "name": screen_node.title,
                "controls": controls,
                "source": screen_node.id  # Traceability
            }]
        }],
        "edges": [
            {"from": "scenario:<original>", "to": settings_id, "type": "satisfied_by"}
        ]
    }

def convert_to_component(screen_node):
    """Convert UI element screen to component contract."""

    return {
        "action": "convert",
        "delete": [screen_node.id],
        "create": [{
            "id": screen_node.id.replace("screen:", "component:"),
            "type": "UIComponentContract",
            "stmt": screen_node.stmt,
            "parent_screen": "NEEDS_PARENT",  # Must be resolved
            "needs_review": True,  # Flag for manual review
            "source": screen_node.id  # Traceability
        }],
        "edges": [
            {"from": "NEEDS_PARENT", "to": screen_node.id.replace("screen:", "component:"), "type": "contains"}
        ]
    }
```

**Salvage Statistics (v45 Example)**:

From v45 screen salvage of 169 screens:
- **21 kept as screens** (12.4%) - Legitimate standalone screens
- **14 → 2 dashboards** (8.3%) - Monitoring/analytics consolidated
- **10 → 1 settings** (5.9%) - Configuration consolidated
- **116 → 116 components** (68.6%) - UI elements within screens
- **1 → 1 admin tool** (0.6%) - Developer tools
- **7 deleted** (4.1%) - Pure backend, no UI

**Result**: 83.4% of "wrong" screens salvaged as proper UI artifacts, preserving requirements.

**Critical Rule**: Always run salvage classification BEFORE deletion. Only delete after confirming "DELETE_NO_UI_NEEDED".

---

### Pre-Conditions (Non-Negotiable - MUST Execute BEFORE UI Projection)

**CRITICAL**: Do NOT generate ANY UI nodes until these exist:

1. **Design System Foundation Check**:
   ```python
   if not design_system_exists():
       create_openquestion(
           "Design System Foundation Required",
           "Create StyleGuide, DesignTokens, ComponentLibrary BEFORE generating UI nodes",
           owner="Design Lead",
           due="+7d",
           blocks=["All UI node generation"]
       )
       STOP()  # Do not proceed
       return {"status": "blocked", "reason": "design_system_missing"}
   ```

2. **Create Foundation First** (if missing):
   - `StyleGuide:app` - Brand colors, typography, spacing, layout patterns
   - `DesignTokens:v1` - Color/space/radius/shadow/animation tokens
   - `ComponentLibrary:v1` - 40+ reusable components (Button, Input, Card, Modal, etc.)

3. **Validate Foundation** (must pass):
   - StyleGuide has ≥5 layout patterns defined
   - DesignTokens has ≥50 tokens (colors, spacing, typography)
   - ComponentLibrary has ≥40 components across 6 categories

**Consequence**: If pre-conditions not met, BLOCK all UI projection and create OpenQuestion for user.

**Lesson Learned (v44)**: Generated 968 UI nodes → THEN created design system → 199 nodes blocked. Foundation FIRST prevents this.

### Node Type Classification (BEFORE Generation - Anti-Duplication Gate)

**CRITICAL**: Classify node type BEFORE creating any nodes to prevent misclassification.

```python
def classify_node_type(scenario):
    """Classify scenario BEFORE creating nodes to prevent backend-as-screens."""

    # STOP 1: Backend infrastructure (NOT screens)
    if scenario.lane in ["Worker", "Data", "Queue", "Cache", "CDN", "Observability"]:
        return NodeType.SERVICE  # Backend service, NO UI

    # STOP 2: API endpoints (NOT screens)
    if scenario.involves_http_endpoint() or scenario.is_api_operation():
        return NodeType.API_ENDPOINT  # Contract/API, NO screen

    # STOP 3: Internal operations (NOT user-visible)
    if not scenario.user_visible:
        return NodeType.POLICY_EXCLUSION  # No UI by design

    # CHECK 1: User-facing with route = Screen
    if scenario.user_visible and scenario.has_route():
        return NodeType.SCREEN  # YES, create screen

    # CHECK 2: User-facing without route = Component (modal/overlay)
    if scenario.user_visible and not scenario.has_route():
        return NodeType.COMPONENT  # Modal/overlay, NOT separate screen

    # DEFAULT: Log as unaccounted
    return NodeType.UNKNOWN  # Create OpenQuestion
```

**Classification Decision Tree**:
```
Is lane Worker/Data/Queue/Cache? → SERVICE (no screen)
Is HTTP endpoint/API operation? → API_ENDPOINT (no screen)
Is user_visible = false? → POLICY_EXCLUSION (no UI)
Is user_visible + has_route? → SCREEN (yes, create)
Is user_visible + no route? → COMPONENT (modal, not screen)
Otherwise? → UNKNOWN (OpenQuestion)
```

**Apply Classification BEFORE `project_ui_impacts()`**:
```python
classified_scenarios = {}
for scenario in scenarios:
    node_type = classify_node_type(scenario)
    classified_scenarios[scenario.id] = node_type

    if node_type == NodeType.SERVICE:
        create_service_spec(scenario)  # NOT a screen
    elif node_type == NodeType.API_ENDPOINT:
        create_api_contract(scenario)  # NOT a screen
    elif node_type == NodeType.SCREEN:
        project_ui_for_screen(scenario)  # YES, create UI nodes
    # ... etc
```

**Lesson Learned (v44)**: Generated 169 screens, 84% were backend infrastructure (CDN, queues, analytics). Classification gate would have prevented 142 wrong screens.

### Pattern Detection Phase (BEFORE Individual Generation - Anti-Duplication)

**CRITICAL**: Detect reusable patterns across ALL scenarios BEFORE generating individual nodes.

```python
def detect_ui_patterns(scenarios):
    """Analyze ALL scenarios to find reusable patterns."""

    patterns = {
        "list": [],      # Feed, Bookmarks, Search → List Template
        "detail": [],    # Post Detail, Profile → Detail Template
        "form": [],      # Create/Edit → Form Template
        "settings": [],  # Settings sections → Settings Template
        "dashboard": [], # Analytics → Dashboard Template
    }

    for scenario in scenarios:
        if matches_list_pattern(scenario):
            patterns["list"].append(scenario)
        elif matches_detail_pattern(scenario):
            patterns["detail"].append(scenario)
        # ... etc

    return patterns

def create_templates_from_patterns(patterns):
    """Create reusable layout templates for detected patterns."""

    templates = []

    if len(patterns["list"]) > 3:  # 3+ scenarios match List pattern
        template = create_layout_template(
            "ListTemplate",
            matches=patterns["list"],
            route_pattern="/:collection",  # Parameterized
            components=["Header", "TabBar", "List(Card)"]
        )
        templates.append(template)

    # ... create other templates

    return templates
```

**Pattern Detection → Template Creation → Composition**:
```
Step 1: Analyze 169 scenarios
Step 2: Detect patterns (40 match "List", 30 match "Detail", 20 match "Form")
Step 3: Create 5 layout templates (List, Detail, Form, Settings, Dashboard)
Step 4: Compose screens from templates + route parameters
Result: 12 screens (not 169) with 80% code reuse
```

**Lesson Learned (v44)**: Generated 169 individual screens → THEN found 80% were duplicates. Pattern detection FIRST prevents duplication.

### Composition-First Architecture (NOT Screen-First)

**CRITICAL**: Build screens from composition, NOT individual screen files.

**Wrong Approach (v44)**:
```
❌ Generate screen-bookmarks-list.json
❌ Generate screen-bookmarks-detail.json
❌ Generate screen-bookmarks-edit.json
❌ Generate screen-search-results.json
❌ Generate screen-notifications-list.json
= 169 individual screen files (massive duplication)
```

**Right Approach (Composition)**:
```
✅ Create ListTemplate (reusable)
✅ Create DetailTemplate (reusable)
✅ Create FormTemplate (reusable)
✅ Compose: /bookmarks → ListTemplate + route params
✅ Compose: /search → ListTemplate + route params
✅ Compose: /notifications → ListTemplate + route params
= 3 templates + 12 composed screens (80% reuse)
```

**Composition Formula**:
```
Screen = Template + Components + Route Parameters

Examples:
/feed = ListTemplate + Card + Header
/posts/:id = DetailTemplate + PostComponent + Actions
/posts/:id/edit = FormTemplate + EditorComponent + Validation
```

**Implementation**:
```python
def compose_screen(scenario, template, components):
    """Compose screen from template + components, not individual file."""

    return {
        "id": f"screen:{scenario.slug}",
        "type": "Screen",
        "template": template.id,  # Reference to layout template
        "route": generate_route_with_params(scenario),
        "components": [c.id for c in components],
        "state_machine": inherit_from_template(template),
        "a11y": inherit_from_components(components),
    }
```

**Lesson Learned (v44)**: Screen-first approach created 169 files with 80% duplication. Composition-first achieves same functionality with 12 screens + 5 templates.

### Trigger Detection (Non-Negotiable)
After classification and pattern detection, run `project_ui_impacts()` over classified scenarios:
- `Scenario` with `NodeType.SCREEN` classification
- `Contract(API|Event)` with `user_facing=true` **AND** classification = SCREEN
- `DataModel` with client-visible fields **AND** classification = SCREEN
- **SKIP** all scenarios classified as SERVICE, API_ENDPOINT, or POLICY_EXCLUSION

### UI Questionnaire (13 Required Questions)
For EVERY triggered node, ask and persist answers to `node.evidence.ui_answers`:

1. **Presence**: Is there UI at all? If **NO**, create `Policy:Exclusion-UI` with rationale+owner.
2. **Entry & context**: New screen? Where does it live? Navigation (route, params, back behavior)?
3. **Representation**: Individual item, collection, or both? Sorting/filtering/pagination?
4. **Interaction**: Create/edit/delete/duplicate/import/export/share? Batch? Undo? Validation (client/server)?
5. **Settings**: User/admin/device/tenant setting required? Defaults and migration?
6. **Tutorial**: Tutorial/coach-mark/empty-state needed? Triggers?
7. **Background updates**: Badges, in-app notifications, push/email? Read/unread semantics?
8. **A11y/i18n**: Keyboard/focus/aria/contrast, copy keys, RTL/truncation?
9. **Device/layout**: Web/iOS/Android/desktop; breakpoints; reduced motion?
10. **Privacy/compliance**: PII surfaced? Consent, masking, export restrictions?
11. **Analytics/experiments**: Tracking plan events, success metrics, variants?

### UI Projection (Automatic Node Creation)
Based on answers, ensure (create or link):
- `Screen` + `NavigationSpec` if new screen
- `UXFlow` (loading/empty/error) for ALL user-facing features
- `UIComponentContract` (list/detail/form) based on representation
- `SettingsSpec` when answers.needs_setting = YES
- `TutorialSpec` when answers.needs_tutorial = YES
- `NotificationSpec` + `BadgeRule` when answers.needs_notifications/badge = YES
- `AnalyticsSpec` with tracking events

Wire edges: backend **→ covered_by →** UI nodes; UI **→ depends_on →** backend.

### Quality Gates (Non-Negotiable - Block Until Satisfied)
A backend **leaf** is **UNSCHEDULABLE** until:

1. **UI Projection Gate**: Paired `UXFlow` + `UIComponentContract` exist OR `Policy:Exclusion-UI` with owner+rationale
2. **Navigation Symmetry Gate**: `NavigationSpec` exists if new/changed route implied
3. **Settings Gate**: If answers.needs_setting = YES → `SettingsSpec` must exist
4. **Tutorial Gate**: If answers.needs_tutorial = YES → `TutorialSpec` must exist
5. **Notification Gate**: If answers.needs_notifications = YES → `NotificationSpec` + opt-out preference must exist
6. **A11y/i18n Gate**: WCAG 2.2 checks pass, i18n keys exist or Exclusion with rationale/owner
7. **Design System Gate**: If `StyleGuide`/`DesignTokens`/`ComponentLibrary` missing → emit `OpenQuestion` and **BLOCK** all `VisualSpec` nodes as Ready. All `UIComponentContract` must reference tokens (no raw colors/sizing).
8. **Analytics Gate**: Tracking events defined or explicitly excluded

### Explainability (Mandatory Logging)
For EVERY skipped UI projection, add to `unaccounted[]` array:
```json
{
  "node_id": "...",
  "reason": "ui_impact=unknown | styleguide_missing | answers_incomplete",
  "owner": "...",
  "due": "YYYY-MM-DD",
  "blocker": true|false
}
```

### Determinism & Idempotency
- Re-running `project_ui_impacts()` with unchanged inputs MUST be no-op (hash stable)
- Sort IDs and edge ops lexicographically before emission
- Use consistent timestamps and UUIDs

### Incremental Validation with User Checkpoints (Anti-Waste Gate)

**CRITICAL**: Validate approach with user DURING generation, not after.

```python
def project_ui_with_checkpoints(scenarios):
    """Generate UI in batches with user validation checkpoints."""

    BATCH_SIZE = 20  # Show user every 20 nodes

    all_ui_nodes = []
    for i in range(0, len(scenarios), BATCH_SIZE):
        batch = scenarios[i:i+BATCH_SIZE]

        # Generate batch
        batch_ui_nodes = generate_ui_nodes(batch)

        # CHECKPOINT: Show user the pattern
        show_user_checkpoint(
            batch_number=i//BATCH_SIZE + 1,
            nodes_generated=len(batch_ui_nodes),
            pattern=describe_pattern(batch_ui_nodes),
            sample_nodes=batch_ui_nodes[:5],
            question="Does this pattern look correct? Continue or stop and refactor?"
        )

        # Wait for user approval
        if user_approves():
            all_ui_nodes.extend(batch_ui_nodes)
        else:
            # User spotted issue early - stop and refactor
            analyze_issue(batch_ui_nodes)
            refactor_approach()
            return {"status": "stopped", "reason": "user_feedback", "nodes_generated": i}

    return all_ui_nodes
```

**Checkpoint Message Template**:
```
🚦 Checkpoint #3: Generated 60 UI nodes so far

Pattern Detected: List + Detail + Form (consistent)
Sample Nodes:
  - screen-feed.json (List pattern)
  - screen-post-detail.json (Detail pattern)
  - screen-create-post.json (Form pattern)
  - screen-bookmarks.json (List pattern - DUPLICATE of screen-feed?)
  - screen-search-results.json (List pattern - DUPLICATE of screen-feed?)

⚠️ Potential Issue: Multiple screens using same List pattern - should use route parameters?

Continue generating (60 more nodes)?
[Yes] [No - Stop and refactor]
```

**Benefits**:
- Catch issues after 20 nodes, not 169
- User can course-correct early
- Prevents waste (1,500 hours saved in v44)

**Lesson Learned (v44)**: Generated all 169 screens → THEN user asked "Why so many?". Checkpoint at 20 would have caught duplication early.

### Effort Validation Gate (Unreasonableness Detector)

**CRITICAL**: Calculate and validate effort DURING generation to detect unreasonable plans.

```python
def validate_plan_effort(plan):
    """Calculate effort and warn if unreasonable."""

    effort_metrics = {
        "Screen": 8,              # 8 hours per screen
        "Component": 4,           # 4 hours per component
        "UIComponentContract": 6, # 6 hours per contract
        "UXFlow": 3,              # 3 hours per flow
    }

    total_effort_hours = 0
    for node_type, count in plan.node_counts.items():
        if node_type in effort_metrics:
            total_effort_hours += count * effort_metrics[node_type]

    # Calculate person-months (160 hours/month)
    person_months = total_effort_hours / 160

    # WARN if effort exceeds thresholds
    if total_effort_hours > 500:  # More than 3 months for 1 person
        WARN_USER(f"""
        ⚠️ EFFORT WARNING: Plan Requires {total_effort_hours} hours ({person_months:.1f} person-months)

        Breakdown:
        - {plan.node_counts.get('Screen', 0)} screens × 8h = {plan.node_counts.get('Screen', 0) * 8}h
        - {plan.node_counts.get('Component', 0)} components × 4h = {plan.node_counts.get('Component', 0) * 4}h

        This seems high. Consider:
        - Using layout templates instead of individual screens
        - Route parameters instead of duplicate screens
        - Component composition instead of custom screens

        Continue anyway? [Yes] [No - Refactor for reusability]
        """)

        if user_chooses_refactor():
            suggest_consolidation_strategies(plan)
            return {"status": "blocked", "reason": "high_effort"}

    return {"status": "ok", "effort_hours": total_effort_hours}
```

**Effort Thresholds**:
- **< 200 hours**: ✅ Reasonable (1-2 person-months)
- **200-500 hours**: ⚠️ Warning (2-3 person-months) - suggest optimization
- **> 500 hours**: 🛑 BLOCK (3+ person-months) - require user approval or refactoring

**Consolidation Suggestions**:
```
If effort > 500 hours:
1. Look for duplicate screens → Use route parameters
2. Look for similar screens → Create layout templates
3. Look for repeated components → Extract to ComponentLibrary
4. Look for backend "screens" → Reclassify as Services/APIs
```

**Lesson Learned (v44)**: 169 screens × 8h = 1,592 hours (10 months!) should have been flagged immediately as unreasonable.

### Continuous Validation (Not End-of-Pass Validation)

**CRITICAL**: Validate nodes AS they're generated, not after all generation.

```python
class ContinuousValidator:
    """Validates nodes during generation to catch issues early."""

    def __init__(self):
        self.seen_routes = set()
        self.seen_patterns = {}
        self.backend_as_screen_count = 0

    def validate_during_generation(self, node):
        """Validate node BEFORE adding to plan."""

        issues = []

        # Check 1: Duplicate route
        if node.type == "Screen" and node.route in self.seen_routes:
            issues.append(f"Duplicate route: {node.route} already exists")

        # Check 2: Backend as screen
        if node.type == "Screen" and self.is_backend_operation(node):
            self.backend_as_screen_count += 1
            issues.append(f"Backend operation classified as screen: {node.id}")

        # Check 3: Pattern duplication
        pattern = self.detect_pattern(node)
        if pattern in self.seen_patterns and len(self.seen_patterns[pattern]) > 3:
            issues.append(f"Pattern {pattern} used {len(self.seen_patterns[pattern])}× - consider template")

        # WARN if issues found
        if issues:
            WARN(f"Validation issues for {node.id}:\n" + "\n".join(f"  - {i}" for i in issues))
            ask_user("Continue creating this node or skip?")

        self.seen_routes.add(node.route)
        self.seen_patterns.setdefault(pattern, []).append(node)

        return len(issues) == 0
```

**Usage**:
```python
validator = ContinuousValidator()

for scenario in scenarios:
    proposed_node = generate_ui_node(scenario)

    # Validate BEFORE adding
    if validator.validate_during_generation(proposed_node):
        add_to_plan(proposed_node)
    else:
        log_rejected(proposed_node, validator.issues)
```

**Benefits**:
- Catch duplicate routes immediately (not after 169 screens)
- Catch backend-as-screen immediately (not after 84% are wrong)
- Suggest templates after 3 duplicates (not after 40)

**Lesson Learned (v44)**: Validated after all generation → found 80% duplication. Continuous validation would have caught this at node 10-15.

### Similarity Detection During Generation (Anti-Duplication)

**CRITICAL**: Detect similar nodes AS they're created to prevent duplication.

```python
def create_node_with_deduplication(node):
    """Check for similar nodes BEFORE creating."""

    # Find similar existing nodes
    similar_nodes = find_similar_nodes(node, threshold=0.8)

    if similar_nodes:
        most_similar = similar_nodes[0]
        similarity_score = calculate_similarity(node, most_similar)

        WARN(f"""
        🔍 SIMILARITY DETECTED

        New node: {node.id}
        Similar to: {most_similar.id}
        Similarity: {similarity_score:.0%}

        Options:
        1. Reuse existing node with parameters (recommended)
        2. Create new node anyway
        3. Create template for this pattern (if 3+ similar)

        What would you like to do?
        """)

        action = ask_user_choice(["reuse", "create_new", "create_template"])

        if action == "reuse":
            return add_route_parameter(most_similar, node.route)
        elif action == "create_template":
            return create_template_from_similar([most_similar, node])
        # else: create_new

    # Create node if no similarity or user chose to create anyway
    create_node(node)
```

**Similarity Calculation**:
```python
def calculate_similarity(node1, node2):
    """Calculate similarity between two nodes (0.0-1.0)."""

    score = 0.0

    # Route similarity (without parameters)
    if normalize_route(node1.route) == normalize_route(node2.route):
        score += 0.3

    # Component similarity
    if set(node1.components) == set(node2.components):
        score += 0.3

    # Layout similarity
    if node1.layout_type == node2.layout_type:
        score += 0.2

    # State machine similarity
    if node1.state_machine == node2.state_machine:
        score += 0.2

    return score
```

**Lesson Learned (v44)**: Created `screen-bookmarks-1.json`, `screen-bookmarks-2.json`, `screen-bookmarks-3.json` without detecting similarity until after all were created.

### Per-Pass Checklist (Print After Each Pass)

**BEFORE starting UI projection**:
- [ ] Design system foundation exists (StyleGuide, DesignTokens, ComponentLibrary)?
- [ ] Node type classification run (Screen vs Service vs API)?
- [ ] Pattern detection run (List, Detail, Form patterns identified)?
- [ ] Effort calculated and validated (< 500 hours)?

**DURING UI projection**:
- [ ] User checkpoint after every 20 nodes generated?
- [ ] Continuous validation running (duplicate routes, backend-as-screens)?
- [ ] Similarity detection active (80%+ similar → suggest reuse)?
- [ ] Composition-first approach (templates + parameters, not individual screens)?

**AFTER UI projection**:
- [ ] Did I run the UI questionnaire for every triggered node?
- [ ] For each "YES," did I create required nodes (Screen/Nav/UXFlow/Component/Settings/Tutorial/Notification)?
- [ ] Are paired UI artifacts present before marking backend leaves "Ready"?
- [ ] Do all UI components reference design tokens/components?
- [ ] Do A11y and i18n checks pass, or is there a blocking Exclusion with owner?
- [ ] Did I log reasons in `unaccounted[]` for anything I skipped?
- [ ] Are all 8 quality gates satisfied or blocking reasons documented?
- [ ] Final effort validation: Total hours reasonable for team capacity?

## Recursion Loop (fixpoint)
1. **Frontier** := all nonterminals missing required children or failing checklists.
2. **Architecture-first**: Before expanding operations, plan end-to-end data flows, cross-service communication, and integration patterns.
3. Expand top-down: Intent → Capabilities → Scenarios → Requirements → Contracts(API/Data/Event/Policy) → Components → Operations/Algorithms → ChangeSpecs.
4. **Leaf forcing**: if a ChangeSpec touches ≥1 dependency or behavior varies by state, explode into **InteractionSpecs** (see `FORMS.md`).
5. **Plan depth**: For complex features, create dedicated architecture nodes (DataFlow, ErrorStrategy, BusinessLogic) before individual operations.
6. **UI Projection** (after backend nodes, before validation):
   - For each user-facing node (Contract, Event, DataModel, Policy, Scenario with UI impact), run **UI Implications Questionnaire**
   - Generate Screen, NavigationSpec, UIComponentContract, SettingsSpec, TutorialSpec, NotificationSpec, BadgeRule, VisualSpec nodes
   - Ensure **Design System foundation** (StyleGuide, DesignTokens, ComponentLibrary) exists; block if absent
   - Create **Client-side InteractionSpecs** with UI state clustering (network, theme, device, reduced_motion, permission, empty)
   - Invoke **UI Subagents** in parallel: UIPlanner, NavSmith, FormSmith, SettingsSmith, TeachBot, NotifyBot, DesignSync, A11yBot, CopyBot
7. Validate & gap: run checklists; write `unaccounted`; create **OpenQuestions** (owner+due); keep parent **Blocked**.
8. Back-propagate: induce missing Contracts/Policies/Algorithms; apply semver & migrations for breaking changes.
9. Detect **RefactorSpecs** conservatively (dup retry patterns; star-dependencies; policy gaps; polling → events), capped by `refactor_caps`.
10. Recompute DAG + lanes; recompute completeness; repeat until the frontier is empty.

## Nonterminal Expansion (required children by type)
- **Intent →** Capabilities **+ Architecture** (DataFlow, ErrorStrategy, BusinessLogic for complex features)
- **Capability →** Scenarios {happy, error, edge, permission} **+ Integration** (how it integrates with other capabilities)
- **Scenario(user-facing) →** Screen OR UIComponentContract OR Exclusion(UI) with rationale
- **Scenario(any) →** Requirements {Functional, Non-Functional: perf/a11y/security} + Test(acceptance) **+ EndToEndFlow** (user journey)
- **Requirement →** Contracts {API, Data, Event, Policy} **and** Components; link ≥1 ChangeSpec **+ CrossCutting** (caching, rate limiting)
- **Contract(API) →** endpoints, error taxonomy, idempotency, timeouts, rate limits, versioning, observability, Test(contract)
- **Contract(API/Event, user-facing) →** UXFlow {Loading, Empty, Error, Ready} + NavigationSpec (if new screen) + UIComponentContract + Analytics
- **Contract(Data) →** schema, indices, migration/backfill, retention, region/PII, Test(migration)
- **Component →** Operations/Algorithms **+ Integration** (how it integrates with other components)
- **Operation/Algorithm →** ≥1 **InteractionSpec** **+ ErrorHandling** (circuit breakers, fallbacks, compensation)
- **Screen →** NavigationSpec + UIComponentContract + VisualSpec + Test(E2E-UI)
- **UIComponentContract →** props/state_machine + validation + VisualSpec + Test(component)
- **SettingsSpec →** scope/defaults + Policy mapping + migration
- **TutorialSpec →** triggers + steps + completion
- **NotificationSpec →** channels + templates + throttling + BadgeRule + SettingsSpec(opt-out)
- **VisualSpec →** DesignTokens reference (no raw values)
- **UXFlow →** states {loading, ready, empty, error} + a11y + i18n + Test(E2E)
- **Risk →** mitigation(owner/date)
- **ChangeSpec(simple=false) →** lists its InteractionSpecs **+ Architecture** (data flow, error handling, business logic)

Unknowns → **OpenQuestion**; parent stays **Blocked**.

## InteractionSpec Granularity

### Backend InteractionSpecs
Create one per tuple **(method, interface, operation, state_cluster)**.
State clustering: enumerate influencers (auth_role, token_state, feature_flag, quota, cache hit/miss, data_version, region, network, idempotency, time_window, partial_failure). Keep only factors that change control-flow or externally observable outcomes. Cluster MECE; emit one InteractionSpec per interface×operation×cluster.

### Client-side InteractionSpecs (UI State Clustering)
Beyond backend state clustering, **Client-side InteractionSpecs** also cluster on:
- **network**: online/offline/slow
- **theme**: light/dark/high_contrast
- **device**: mobile/tablet/desktop (form factor, orientation, safe areas)
- **reduced_motion**: true/false
- **permission**: granted/denied/not_requested
- **empty**: true/false (for list/collection views)
- **feature_flag**: enabled/disabled (UI-specific flags)
- **auth_role**: user/admin/guest (UI access patterns)
- **error_type**: recoverable/terminal/partial

Emit one **InteractionSpec(Client)** per meaningful UI state cluster.

**Each InteractionSpec MUST include**: `pre`, `inputs`, `expected_effects`, `error_model` (retriable/non-retriable + compensation), `resilience` (timeout/retry/idempotency), `observability` (logs/metrics/span), `security` (authZ/least-priv/PII), `test` (mocks + Given/When/Then), `depends_on` (Contracts/Policies), `owner`, `est_h`, `status`.

For **Client InteractionSpecs**, also include: `a11y` (keyboard/screen reader/contrast), `i18n` (copy keys/pluralization/RTL), `analytics` (tracking events), `visual_spec_ref` (design tokens).

## UI Implications Questionnaire (Systematic)

For every user-facing node (Contract(API/Event), DataModel, Policy, Scenario with UI), answer:

**A. Discoverability** - Where/how users find this? Entry points? Role/flag gating?

**B. Representation** - Item or collection? List/grid/table? Detail view? Filters/sort?

**C. Interaction** - CRUD? Batch? Inline vs modal? Validation (client/server)?

**D. Navigation** - New screen? Push/modal/replace? Back behavior? Deep links?

**E. Settings** - New setting? Scope (user/tenant/device)? Defaults? Admin controls?

**F. Tutorial** - Guided flow needed? Triggers? Format (coach/checklist/sample)?

**G. Notifications** - Background updates? Badge? Push/email? Opt-out preference?

**H. Context** - Which screen? Cross-links? Contextual actions?

**I. States** - Loading/empty/error? Offline? Permission denied? Feature gated?

**J. A11y/i18n** - Keyboard nav? Screen reader? Color contrast? i18n keys? RTL?

**K. Device** - Web/iOS/Android? Breakpoints? Orientation? Safe areas?

**L. Privacy** - PII surfaced? Consent required? Redaction? Export controls?

**M. Analytics** - Tracking events? Experiment buckets? Success metrics?

Answers drive UI node generation. Missing answers → OpenQuestion.

**Quick mapping from backend changes → UI obligations**:

| Change type                      | Typical UI obligations                                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| New **GET /items**               | `Screen:list`, `UIComponent:list`, `UXFlow:list` (loading/empty/error), filters/sort, analytics events              |
| New **POST /items**              | `Screen:create` or inline form, `UIComponentContract:form`, validation, success/error toasts, navigation on success |
| New **Event item.updated**       | `BadgeRule` for inbox/surface, optimistic updates, toasts, cache invalidation                                       |
| New **Policy scope/limit**       | Guarded `Screen`, "upgrade/paywall" UX, copy, analytics                                                             |
| New **Data field PII/sensitive** | Redaction/masking, consent gating, export/print restrictions                                                        |
| New **Async job**                | Background status indicator, job progress view, inbox entry, retry UI                                               |

## UI Node Types

Add these **UI node types** to the PlanGraph:

- **Screen** (aka Destination) — registered route with purpose and entry points.
- **UXFlow** — stepwise user journey (includes Loading/Empty/Error variants).
- **UIComponentContract** — props/types/state machine for a component or form.
- **NavigationSpec** — route name, params, guards, transitions, back behavior.
- **SettingsSpec** — key/scope/defaults/change events/admin policy.
- **TutorialSpec** — triggers, steps, completion, re-entry rules.
- **NotificationSpec** — channels, template IDs, throttling, preferences linkage.
- **BadgeRule** — increment/decrement sources, reset semantics.
- **VisualSpec** — mapping to style guide tokens, spacing, densities.
- **StyleGuide** / **DesignTokens** / **ComponentLibrary** — design system artifacts (foundational).

**Edges**:
- Backend node (`Contract|Event|DataModel|Policy`) **→ covered_by →** `UXFlow|Screen|UIComponentContract|SettingsSpec|NotificationSpec`
- UI nodes **→ depends_on →** backend/schema/policy versions
- `Screen` **→ gated_by →** `Policy` (roles/flags/plans)
- `NavigationSpec` **→ covered_by →** `Test(Client)` and **measured_by →** analytics events

**UI leaf requirement**: Every UI node yields **InteractionSpec(Client)** per state-cluster.

## UI Subagents (Parallel Execution)

When UI projection is triggered, invoke these specialized subagents **in parallel** for independent UI concerns:

- **UIPlanner** - Runs questionnaire, drafts UXFlow/Screen
- **NavSmith** - NavigationSpec + deep links + tests
- **FormSmith** - UIComponentContracts for forms with validation
- **SettingsSmith** - SettingsSpec + defaults/migrations
- **TeachBot** - TutorialSpec + triggers + completion
- **NotifyBot** - NotificationSpec + BadgeRule + preferences
- **DesignSync** - VisualSpec + DesignTokens enforcement (lint for raw values)
- **A11yBot** - WCAG checks + keyboard nav + screen reader labels
- **CopyBot** - i18n keys + pluralization + RTL hints

These subagents report back to the main planning loop with their generated UI nodes and edges.

## UI Node Templates (copy/paste)

**Screen**
```yaml
id: Screen:<slug>
route: /<path>/{id?}
entry_points: [CTA:..., DeepLink:..., NavItem:...]
guards: {auth_role: [...], plan: [...], feature_flag: [...], unsaved_changes_guard: true}
layout: {type: detail|list|grid|wizard|map, breakpoints: [sm, md, lg]}
depends_on: [Contract:..., DataModel:...]
```

**NavigationSpec**
```yaml
id: NavigationSpec:<from>-><to>
action: push|replace|modal|sheet
params: {id?: string, source?: string}
back_behavior: pop|dismiss|custom
tests:
  - name: deep_link_opens_detail
    given: url:/item/123
    then: route_is:/item/123
```

**UIComponentContract**
```yaml
id: UIComponentContract:<entity>-form
props: {entityId?: string}
state_machine: [Idle -> Editing -> Submitting -> Success|InlineError]
validation: {client_rules:[...], server_rules:[...]}
events: [submit, cancel, delete]
links: {tracking_events:[...], spans:[...]}
```

**SettingsSpec**
```yaml
id: SettingsSpec:<key>
scope: user|tenant|device
default: true|false|value
controls: toggle|select|range
policy: {admin_enforced?: bool, allowed_values?: [...]}
migration: {from_version: vN, fallback: value}
```

**TutorialSpec**
```yaml
id: TutorialSpec:<feature>
triggers: [first_use_of:<screen>, low_adoption_below:<metric>]
steps: [coachmark:<selector>, highlight:<selector>, checklist:<id>]
completion: {event: tutorial_completed, cooldown_days: 90}
```

**NotificationSpec + BadgeRule**
```yaml
id: NotificationSpec:<topic>
channels: [in_app, push, email]
template_ids: {in_app: tpl_..., push: tpl_...}
throttle: {max_per_hour: 2}
preference_link: SettingsSpec:notifications.<topic>

id: BadgeRule:<surface>
increments_on: [Event:<name>|Query:unread_count]
resets_on: [screen_visit:<slug>, action:<name>]
```

**VisualSpec**
```yaml
id: VisualSpec:<component>
tokens: {color.bg: var(--bg-surface), space.x: 16, radius: 12}
modes: {light: true, dark: true, high_contrast: true}
```

## Completion Proofs (CPP) — ALL must be true

### Core Proofs (P1-P9, renumbered)
- **P1 Topology** — Ready nodes exist for: Client/UI, API Gateway, Services, Data Stores, Caches/CDN, Queues/Workers, Auth/Identity, Secrets, Moderation/Policy (if used), Observability, Analytics, Config/Flags, Migrations/Backfills, Rollout.
- **P2 Scenario × Interface × State Coverage Matrix (Backend)** — for every Scenario, enumerate expected backend interactions; require `expected_ix == realized_ix` (zero gaps).
- **P3 Data Lifecycle** — per Data contract: CRUD, retention, PII, region, backup/restore, migration/backfill, indexing.
- **P4 Security/AuthZ** — authN, scopes/roles, least privilege, secrets, CSRF/CORS (web), rate limits/quotas.
- **P5 Tests** — per Scenario (unit+integration+E2E) and per InteractionSpec (mocks + G/W/T).
- **P6 Observability** — logs, metrics, trace spans; dashboards + alerts; rollout metrics.
- **P7 Rollout/Versioning** — contract semver; migrations/backfills precede consumers; flags/canary/rollback.
- **P8 Ordering/Gate** — task DAG has no blocked leaves; all pass Work-Start Gate.
- **P9 Node-Expansion** — all nonterminals have required children and pass checklists; coverage = 1.00.

### UI-Specific Proofs (P2-Client, P6-UX, P11-Design, P13-A11y/i18n)
- **P2-Client: Client Lane Coverage Matrix** — for every user-facing Scenario, coverage matrix for Client lane satisfied: all interactions have corresponding UI nodes (Screen/UXFlow/UIComponentContract) OR documented Exclusion(UI).
- **P6-UX: UXFlow Completeness** — All UXFlow variants (Loading/Empty/Error/Ready) present with tests + a11y/i18n checks.
- **P10 Core Blueprint Coverage** — Architecture patterns, data flows, error strategies documented.
- **P11 Incident Readiness** — Runbooks, alerts, rollback procedures defined.
- **P11-Design: Design System Compliance** — All UI components reference DesignTokens (no raw color/size values); StyleGuide, DesignTokens, ComponentLibrary nodes exist and are Ready.
- **P12 Compliance** — GDPR/CCPA/HIPAA requirements (if applicable) addressed.
- **P13-A11y/i18n: Accessibility & Internationalization** — WCAG 2.1 AA checks pass for all UI nodes; all copy uses i18n keys (no hardcoded strings); RTL layouts validated; keyboard navigation and screen reader support verified.

**Additional UI completeness score components**:
- `% Screens with NavigationSpec`
- `% UIComponentContracts with validation + tests`
- `% UXFlows with tutorial or intentional no-tutorial decision`
- `% Notifications with linked preference`
- `% components referencing tokens (target: 100%)`

## UI Projection Algorithm (Revised with v44 Learnings)

**This algorithm is MANDATORY and MUST run after every delta merge pass.**

**Execution Order** (CRITICAL - follow exact sequence):

```python
def project_ui_impacts_v45(changed_nodes):
    """
    Revised UI projection algorithm incorporating all v44 learnings.
    Execution order: Pre-conditions → Classification → Pattern Detection → Composition → Validation
    """

    # ============================================================
    # PHASE 0: PRE-CONDITIONS (BLOCKING - MUST EXIST BEFORE PROCEEDING)
    # ============================================================

    print("Phase 0: Checking pre-conditions...")

    # 0.1: Check design system foundation
    if not design_system_exists():
        create_openquestion(
            "Design System Foundation Required",
            "Create StyleGuide, DesignTokens, ComponentLibrary BEFORE generating UI nodes",
            owner="Design Lead",
            due="+7d",
            blocks=["All UI node generation"]
        )
        STOP()  # Do not proceed without foundation
        return {"status": "blocked", "reason": "design_system_missing"}

    print("  ✅ Design system foundation exists")

    # ============================================================
    # PHASE 1: NODE TYPE CLASSIFICATION (BEFORE GENERATION)
    # ============================================================

    print("Phase 1: Classifying node types...")

    classified = {
        "SCREEN": [],         # User-facing screens with routes
        "COMPONENT": [],      # Modals/overlays without routes
        "SERVICE": [],        # Backend services (NO UI)
        "API_ENDPOINT": [],   # API contracts (NO UI)
        "EXCLUSION": [],      # No UI by design
        "UNKNOWN": []         # Needs clarification
    }

    for node in changed_nodes:
        node_type = classify_node_type(node)
        classified[node_type.name].append(node)

    # Log classification results
    print(f"  ✅ Classified: {len(classified['SCREEN'])} screens, "
          f"{len(classified['SERVICE'])} services, "
          f"{len(classified['API_ENDPOINT'])} APIs, "
          f"{len(classified['EXCLUSION'])} exclusions")

    # WARN if many backend nodes classified as screens
    if len(classified['SERVICE']) > len(classified['SCREEN']):
        WARN(f"More services ({len(classified['SERVICE'])}) than screens ({len(classified['SCREEN'])}) - verify classification")

    # ============================================================
    # PHASE 2: PATTERN DETECTION (BEFORE INDIVIDUAL GENERATION)
    # ============================================================

    print("Phase 2: Detecting UI patterns...")

    ui_scenarios = classified["SCREEN"]
    patterns = detect_ui_patterns(ui_scenarios)

    # Log pattern detection results
    print(f"  ✅ Patterns detected:")
    for pattern_name, scenarios in patterns.items():
        print(f"    - {pattern_name}: {len(scenarios)} scenarios")

    # ============================================================
    # PHASE 3: TEMPLATE CREATION (FROM PATTERNS)
    # ============================================================

    print("Phase 3: Creating layout templates...")

    templates = create_templates_from_patterns(patterns)

    print(f"  ✅ Created {len(templates)} layout templates")
    for template in templates:
        print(f"    - {template.id}: {len(template.matches)} scenarios")

    # ============================================================
    # PHASE 4: EFFORT VALIDATION (BEFORE COMPOSITION)
    # ============================================================

    print("Phase 4: Validating effort estimate...")

    estimated_nodes = {
        "Screen": len(ui_scenarios),  # May be reduced by composition
        "Template": len(templates),
        "Component": sum(len(t.components) for t in templates),
    }

    effort_result = validate_plan_effort(estimated_nodes)

    if effort_result["status"] == "blocked":
        WARN(f"⚠️ Effort too high: {effort_result['effort_hours']} hours. Suggest consolidation.")
        if user_chooses_refactor():
            # Increase composition, reduce individual screens
            return suggest_consolidation_strategies(patterns, templates)

    print(f"  ✅ Effort estimate: {effort_result['effort_hours']} hours (acceptable)")

    # ============================================================
    # PHASE 5: COMPOSITION (SCREENS FROM TEMPLATES)
    # ============================================================

    print("Phase 5: Composing screens from templates...")

    composed_screens = []
    validator = ContinuousValidator()  # Real-time validation

    BATCH_SIZE = 20  # Checkpoint every 20 nodes

    for i, scenario in enumerate(ui_scenarios):
        # 5.1: Match scenario to template
        template = match_template(scenario, templates)

        # 5.2: Compose screen from template
        screen = compose_screen(scenario, template)

        # 5.3: VALIDATE BEFORE ADDING (continuous validation)
        if not validator.validate_during_generation(screen):
            WARN(f"Validation failed for {screen.id}: {validator.last_issues}")
            ask_user("Continue creating this screen or skip?")

        # 5.4: Check similarity (anti-duplication)
        similar = find_similar_nodes(screen, threshold=0.8)
        if similar:
            WARN(f"Screen {screen.id} is 80% similar to {similar[0].id}")
            ask_user("Reuse existing with parameters or create new?")

        composed_screens.append(screen)

        # 5.5: USER CHECKPOINT every 20 nodes
        if (i + 1) % BATCH_SIZE == 0:
            show_checkpoint(
                batch_number=(i + 1) // BATCH_SIZE,
                nodes_generated=i + 1,
                pattern=describe_pattern(composed_screens[-BATCH_SIZE:]),
                continue_or_stop="Continue generating or stop and refactor?"
            )

            if not user_approves():
                return {"status": "stopped", "reason": "user_feedback", "nodes": i + 1}

    print(f"  ✅ Composed {len(composed_screens)} screens from {len(templates)} templates")

    # ============================================================
    # PHASE 6: UI QUESTIONNAIRE & NODE GENERATION
    # ============================================================

    print("Phase 6: Running UI questionnaire and generating UI nodes...")

    all_ui_nodes = []
    unaccounted = []

    for screen in composed_screens:
        # 6.1: Run 13-question UI questionnaire
        answers = ui_questionnaire(screen)

        # 6.2: Generate UI nodes based on answers
        ui_nodes = []
        ui_nodes.append(screen)  # Screen itself
        ui_nodes.extend(ensure_navigation_spec(screen, answers))
        ui_nodes.extend(ensure_uxflows(screen, answers))
        ui_nodes.extend(ensure_ui_components(screen, answers))

        # 6.3: Conditional nodes
        if answers.needs_setting:
            ui_nodes.extend(ensure_settings_spec(screen, answers))
        if answers.needs_tutorial:
            ui_nodes.extend(ensure_tutorial_spec(screen, answers))
        if answers.needs_notifications or answers.needs_badge:
            ui_nodes.extend(ensure_notification_and_badge(screen, answers))

        # 6.4: Quality checks
        ui_nodes.extend(ensure_a11y_i18n_checks(screen))
        ui_nodes.extend(ensure_analytics_spec(screen, answers))

        all_ui_nodes.extend(ui_nodes)

        # 6.5: Log if UI was skipped
        if not ui_nodes and not has_exclusion(screen):
            unaccounted.append({
                "node_id": screen.id,
                "reason": determine_skip_reason(screen, answers),
                "owner": screen.owner or "Unassigned",
                "due": calculate_due_date(screen),
                "blocker": True
            })

    print(f"  ✅ Generated {len(all_ui_nodes)} UI nodes total")

    # ============================================================
    # PHASE 7: BACKEND NODES (NON-UI)
    # ============================================================

    print("Phase 7: Creating backend nodes (non-UI)...")

    # Create Service specs for backend operations
    for service_node in classified["SERVICE"]:
        create_service_spec(service_node)

    # Create API endpoints for API operations
    for api_node in classified["API_ENDPOINT"]:
        create_api_endpoint(api_node)

    # Create exclusions for no-UI scenarios
    for exclusion_node in classified["EXCLUSION"]:
        ensure_ui_exclusion(exclusion_node)

    print(f"  ✅ Created {len(classified['SERVICE'])} services, "
          f"{len(classified['API_ENDPOINT'])} APIs, "
          f"{len(classified['EXCLUSION'])} exclusions")

    # ============================================================
    # PHASE 8: QUALITY GATES & VALIDATION
    # ============================================================

    print("Phase 8: Applying quality gates...")

    gates_result = apply_ui_gates_and_block_on_failure(all_ui_nodes, unaccounted)

    print(f"  ✅ Gates applied: {len(gates_result['gates_applied'])}")
    print(f"  ⚠️ Blocked nodes: {len(gates_result['blocked_nodes'])}")

    # ============================================================
    # PHASE 9: FINAL EFFORT VALIDATION
    # ============================================================

    print("Phase 9: Final effort validation...")

    actual_nodes = {
        "Screen": len(composed_screens),
        "Template": len(templates),
        "Component": len([n for n in all_ui_nodes if n.type == "UIComponentContract"]),
        "UXFlow": len([n for n in all_ui_nodes if n.type == "UXFlow"]),
    }

    final_effort = validate_plan_effort(actual_nodes)

    print(f"  ✅ Final effort: {final_effort['effort_hours']} hours")
    print(f"  ✅ Composition reuse: {calculate_reuse_percentage(composed_screens, templates):.1f}%")

    # ============================================================
    # RETURN RESULTS
    # ============================================================

    return {
        "status": "complete",
        "classification": {
            "screens": len(classified["SCREEN"]),
            "services": len(classified["SERVICE"]),
            "apis": len(classified["API_ENDPOINT"]),
            "exclusions": len(classified["EXCLUSION"]),
        },
        "patterns_detected": {k: len(v) for k, v in patterns.items()},
        "templates_created": len(templates),
        "screens_composed": len(composed_screens),
        "ui_nodes_generated": len(all_ui_nodes),
        "effort_hours": final_effort["effort_hours"],
        "reuse_percentage": calculate_reuse_percentage(composed_screens, templates),
        "gates_applied": gates_result["gates_applied"],
        "blocked_nodes": gates_result["blocked_nodes"],
        "unaccounted": unaccounted,
    }
```

**Key Improvements from v44**:

1. **Pre-conditions FIRST** → No UI generation without design system
2. **Classification BEFORE generation** → No backend-as-screens
3. **Pattern detection BEFORE individual nodes** → 80% less duplication
4. **Effort validation DURING planning** → Catch unreasonable plans early
5. **Continuous validation** → Catch issues as they happen
6. **User checkpoints every 20 nodes** → Course-correct early
7. **Similarity detection** → Prevent duplicate screens
8. **Composition-first** → Templates + parameters, not individual files

**Result**: 12 screens (not 169), 80% reuse, 77% effort reduction

## UI Lint Rules & Gates (Enforced - Duke's Feedback Section 4)

**These lints are NON-NEGOTIABLE and MUST block execution when violated.**

Add these to existing spec-lint:

1. **UI Projection Rule** (MANDATORY) - Any `user_facing=true` backend node requires:
   - ≥1 `UXFlow` **AND**
   - ≥1 `InteractionSpec(Client)` **AND**
   - ≥1 Client-lane interaction spec
   - **OR** recorded `Policy:Exclusion-UI` with owner+rationale+date
   - **Consequence**: Mark parent as BLOCKED until satisfied

2. **Coverage Matrix (Client)** - For each affected entity: `Entity × Screen × StateCluster(role, network, feature_flag, data_version, cache_hit, permission, offline, empty, error_type)` has ≥1 IX or documented Exclusion.
   - **Consequence**: Add to `unaccounted[]` with owner+due

3. **Navigation Symmetry** (MANDATORY) - If new destination exists:
   - `NavigationSpec` with route/params/guards/back behavior MUST exist
   - Tests for navigation MUST exist
   - **Consequence**: Mark Screen as BLOCKED until NavigationSpec created

4. **Settings/Tutorial/Notification Gates** (MANDATORY) - YES answers create required specs:
   - Settings: `SettingsSpec` + `Policy` mapping + migration default
   - Tutorial: `TutorialSpec` + triggers + completion events
   - Notification: `NotificationSpec` + `BadgeRule` + opt-out preference
   - **Consequence**: Mark parent as BLOCKED; add to `unaccounted[]`

5. **A11y/i18n Gate** (MANDATORY) - All `UXFlow` and `UIComponentContract` nodes MUST pass:
   - WCAG 2.2 Level AA checks (keyboard nav, contrast 4.5:1, labels, roles)
   - i18n keys present (no hardcoded strings)
   - RTL layout validated
   - **OR** `Policy:Exclusion-A11y` with owner+rationale (requires legal review)
   - **Consequence**: Mark as BLOCKED; emit OpenQuestion with A11y owner

6. **Design System Gate** (MANDATORY) - If `StyleGuide`/`DesignTokens`/`ComponentLibrary` absent:
   - Create `OpenQuestion` ("Which design system? Who owns tokens?")
   - BLOCK all `VisualSpec` nodes as Ready
   - All `UIComponentContract` and `VisualSpec` nodes MUST reference tokens
   - Raw CSS values forbidden unless `node.evidence` justifies (requires Design approval)
   - **Consequence**: 199 nodes blocked until design system created (expected)

7. **Explainability Gate** (MANDATORY) - For any failure, `unaccounted[]` includes:
   - Short, actionable reason
   - Owner (person responsible for resolution)
   - Due date (when this must be resolved)
   - **Consequence**: Block release until all `unaccounted[]` items resolved

8. **Work-Start Gate (Amended)** (MANDATORY) - Backend leaf is unschedulable until:
   - Paired `UXFlow` + `UIComponentContract` exist AND are Ready
   - `NavigationSpec` exists AND is Ready (if new screen)
   - A11y/i18n checks pass
   - Analytics events defined or excluded
   - Design tokens referenced (no raw values)
   - **Consequence**: Cannot generate ImplementationTasks until all gates satisfied

**Audit Mechanism**: Run lint checker at end of each pass; print violations; refuse to mark plan "complete" until all lints pass.

## Work-Start Gate (Complete Definition)

A leaf can be scheduled only if:
- **No OpenQuestions** blocking it
- Upstream **Contracts** are `Ready`
- **Migrations** scheduled (if breaking changes)
- **Acceptance checks** defined
- **Owner + estimate** set
- **Rollout flag** set (if applicable)
- **P1–P13 true** for its ancestry
- **If user-facing**: paired `UXFlow/Screen` + `UIComponentContract` + `NavigationSpec` (if new screen) + A11y/i18n checks + Analytics events + `VisualSpec` (referencing tokens)

Do **not** generate ImplementationTasks until the parent ChangeSpec **and** all child InteractionSpecs (both backend and client) are `Ready`.

## Emission Rules (DRY, low duplication)
- Emit **deltas only** + **changed node bodies** within the pass KB budget.
- Reference upstream by **IDs** (and optional hash) instead of inlining; keep large bodies in shards.
- Use `FORMS.md` for canonical templates; `PROOFS.md` for matrices to avoid repeating the same text.

## Examples

**First pass**
```json
{"feature_id":"feat:post-image-upload","intent":"Allow users to attach an image to a post."}
```

**Add missing auth refresh Contract, link to IX**
```json
{"deltas":[
  {"op":"add_node","node":{"id":"contract:auth-refresh","type":"Contract","stmt":"POST /auth/refresh ...","status":"Open"}},
  {"op":"add_edge","from":"contract:auth-refresh","to":"ix:compose.auth.refresh.expired","type":"depends_on"}
]}
```

**Add UI nodes for new POST /items endpoint**
```json
{"deltas":[
  {"op":"add_node","node":{"id":"screen:items-create","type":"Screen","route":"/items/new","entry_points":["CTA:create-item"],"status":"Open"}},
  {"op":"add_node","node":{"id":"nav:items-list->items-create","type":"NavigationSpec","action":"push","status":"Open"}},
  {"op":"add_node","node":{"id":"ui-component:items-form","type":"UIComponentContract","state_machine":"Idle->Editing->Submitting->Success","status":"Open"}},
  {"op":"add_node","node":{"id":"visual:items-form","type":"VisualSpec","tokens":{"color.bg":"var(--bg-surface)"},"status":"Open"}},
  {"op":"add_edge","from":"contract:post-items","to":"screen:items-create","type":"covered_by"},
  {"op":"add_edge","from":"screen:items-create","to":"ui-component:items-form","type":"depends_on"}
]}
```

## Planning Depth Requirements

**Beyond Completeness: Plan for Integration and Depth**

The skill should plan for **depth, not just breadth**. Completeness (all operations, contracts, tests) is necessary but not sufficient. Also plan:

1. **Architecture & Data Flow**
   - End-to-end data flow diagrams (user action → API → service → DB → cache → response)
   - Request/response lifecycle across services
   - Cross-service communication patterns (sync, async, events)

2. **Error Handling & Resilience**
   - Error taxonomy across services (consistent error codes, messages)
   - Circuit breaker patterns and fallback strategies
   - Compensation workflows (sagas) for distributed operations
   - Partial failure handling

3. **Business Logic Deep Dive**
   - State machines for complex flows (payment states, subscription lifecycle)
   - Business rules and workflows (payout, revenue reporting)
   - Algorithm specifications (pathfinding, golden ratio calculations)

4. **Integration Patterns**
   - How features integrate (monetization + content, chat + agent access)
   - Shared concerns (caching, rate limiting) across features
   - Data consistency across services

5. **Cross-Cutting Concerns**
   - Caching strategy (what/when to cache, invalidation)
   - Rate limiting strategy (per user/feature/endpoint)
   - Search strategy (full-text, indexing, ranking)
   - Analytics strategy (event tracking, behavior analytics)

6. **UI/UX Architecture** (NEW)
   - Design system foundation (StyleGuide, DesignTokens, ComponentLibrary)
   - Navigation architecture (screen hierarchy, deep linking strategy)
   - State management strategy (local vs global, optimistic updates)
   - Accessibility architecture (keyboard navigation, screen reader support)
   - Internationalization architecture (copy management, RTL support)
   - Responsive design strategy (breakpoints, device capabilities)

## Meta Dimensions Planning

**Expand view beyond basic dimensions to include indirect interfaces and meta dimensions**

Each planning iteration must expand beyond basic implementation dimensions to include:

1. **Indirect Interface Dimensions**
   - How the item interfaces with other areas of the application that support the action/behavior
   - Cross-feature dependencies and interactions
   - Service boundaries and integration points
   - Data flow through indirect paths

2. **User Experience Meta Dimensions**
   - How users discover and access the feature
   - User mental models and expectations
   - Contextual interactions (where/when/how users engage)
   - Accessibility and internationalization considerations
   - Error recovery from user perspective

3. **System Meta Dimensions**
   - Observability and monitoring touchpoints
   - Security and compliance touchpoints
   - Performance and scalability implications
   - Operational and deployment considerations
   - Maintenance and evolution pathways

4. **Planning Meta Dimensions**
   - How the planning itself should evolve
   - Feedback loops for planning improvements
   - Risk assessment for planning gaps
   - Validation mechanisms for planning completeness

5. **Behavioral Support Dimensions**
   - Supporting infrastructure for the behavior (not just the behavior itself)
   - Background processes that enable the action
   - Data consistency and state management
   - Event propagation and side effects
   - Failure modes and recovery mechanisms

6. **UI/UX Meta Dimensions** (NEW)
   - How UI features integrate with each other (cross-screen workflows)
   - Design system evolution and component reusability
   - Analytics and experimentation infrastructure
   - User education and onboarding flows
   - Settings and preference management
   - Notification and communication strategy

**Guidance**: For every feature/capability, ask:
- "What other areas support this action or behavior?"
- "How does this interface with the user in indirect ways?"
- "What meta-infrastructure enables this feature?"
- "What are the indirect consequences and dependencies?"
- "How does the UI discovery and navigation work?"
- "What supporting UI patterns are needed (settings, tutorials, notifications)?"

For complex features mentioned in goal documents (monetization, chat, pathfinding), create dedicated **Architecture** nodes before expanding to operations. Capture the "how it works together" before the "what exists," including indirect interfaces, meta dimensions, and comprehensive UI/UX architecture.

## Decision Heuristics: "Do we need a tutorial/setting/screen?"

Use these cues to guide questionnaire answers:

- **Tutorial**: Required if flow has ≥3 steps, error rate > threshold, or introduces non-obvious affordances; otherwise add empty-state guidance or contextual help.

- **Setting**: Required if behavior materially affects user risk or noisy channels (notifications), or if admins must enforce policy; otherwise prefer adaptive defaults with inline controls.

- **New screen**: Required if the entity needs **discoverable** list + detail, or if navigation/state sharing across sessions is needed; otherwise consider inline/ephemeral UI (modals, sheets, drawers).

- **Tutorial format**: Coach marks for simple features, checklists for multi-step processes, sample data for creative tools, empty-state learning for first use.

- **Notification channels**: In-app for immediate feedback, push for time-sensitive updates, email for reports/summaries, webhooks for integrations.

## Design System Foundation

**Detection & Enforcement**:

If **StyleGuide/DesignTokens/ComponentLibrary** nodes are missing:
1. Create `StyleGuide:App` (owner: Design)
2. Create `DesignTokens:v1` (colors/typography/spacing/radii/shadows/breakpoints/animations)
3. Create `ComponentLibrary:v1` (Button, Input, List, Card, Modal, Toast, Badge, Tabs, Table, Empty, Skeleton, Avatar, Dropdown, Checkbox, Radio, Switch, Slider, DatePicker, FileUpload, Pagination, Breadcrumb, ProgressBar, Tooltip, Popover, Alert, Banner)

**Lint**: Every `UIComponentContract` and `VisualSpec` **must** reference tokens or components; raw CSS values (colors, sizes, fonts) are forbidden unless justified in `node.evidence`.

**DesignAudit pass** (periodic):
- Crawl `UIComponentContract` → verify token usage
- Flag anti-patterns (raw values, inconsistent spacing, non-standard components)
- Propose refactors to shared components
- Identify component library gaps

See `FORMS.md` for node templates and `PROOFS.md` for Completion Proof details.
