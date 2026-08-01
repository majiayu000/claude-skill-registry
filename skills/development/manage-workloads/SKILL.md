---
name: manage-workloads
description: '**Autonomously create** filters, throttles, and classification rules
  to implement new workloads or manage workload lifecycle in response to changing
  operational needs'
---

---
name: manage-workloads
description: **Autonomously create** filters, throttles, and classification rules to implement new workloads or manage workload lifecycle in response to changing operational needs
---

# Manage Workloads

**Autonomously create and configure** filters, throttles, and classification rules to implement new workloads, manage workload lifecycle, and dynamically control system behavior in response to operational changes.

## 🎯 New Autonomous Capabilities

**This skill can now execute workload management, not just recommend it!**

With tdwm-mcp v1.5.0, this skill has evolved from advisory to autonomous:
- ✅ **CREATE** filters to route queries to workloads
- ✅ **CREATE** throttles to protect workload resources
- ✅ **ENABLE/DISABLE** filters and throttles for lifecycle management
- ✅ **USE TEMPLATES** for common workload patterns
- ✅ **VALIDATE** configurations before execution
- ✅ **VERIFY** workload implementation

**Note**: Workload definitions themselves are created via Teradata TDWM utilities, but this skill automates the filter and throttle creation needed to make workloads functional.

## Instructions

### When to Use This Skill
- Implementing new workload for application or user group
- Creating filters to route queries to existing workload
- Adding throttles to protect workload resources
- Emergency situation requires temporary workload protection
- Responding to maintenance windows or special events
- Managing seasonal or special-purpose workload activation

### Available MCP Tools

**Monitoring & Analysis:**
- `list_active_WD` - List currently active workloads
- `list_WDs` - List all workloads (active and inactive)
- `show_tdwm_summary` - View workload distribution
- `show_tasm_statistics` - Monitor workload effectiveness
- `list_rulesets` - List all available rulesets

**Configuration Management (NEW ✨):**
- `create_filter_rule` - Create filter to route queries to workload
- `create_system_throttle` - Create throttle for workload protection
- `enable_filter_rule` / `disable_filter_rule` - Lifecycle management
- `enable_throttle` / `disable_throttle` - Lifecycle management
- `add_classification_to_rule` - Add criteria to existing filter/throttle
- `activate_ruleset` - Apply all pending changes

### Available MCP Resources (NEW ✨)

**Templates:**
- `tdwm://templates/filter` - List all filter templates
- `tdwm://template/filter/application-basic` - Route by application
- `tdwm://template/filter/user-group` - Route by user/account
- `tdwm://template/filter/time-based` - Time-based routing
- `tdwm://templates/throttle` - List all throttle templates
- `tdwm://template/throttle/application-basic` - Basic workload throttle
- `tdwm://template/throttle/user-concurrency` - Per-user limits

**Reference Data:**
- `tdwm://reference/classification-types` - All 31 classification types
- `tdwm://reference/operators` - Classification operators (I, O, IO)
- `tdwm://reference/filter-actions` - Filter actions (ACCEPT/REJECT)
- `tdwm://reference/throttle-types` - Throttle types (DM, M)

**Discovery:**
- `tdwm://rulesets` - List all rulesets
- `tdwm://system/active-ruleset` - Get currently active ruleset
- `tdwm://ruleset/{name}/filters` - List filters in ruleset
- `tdwm://ruleset/{name}/throttles` - List throttles in ruleset
- `tdwm://ruleset/{name}/pending-changes` - Check pending changes

**Workflows:**
- `tdwm://workflow/create-filter` - Step-by-step filter creation guide
- `tdwm://workflow/create-throttle` - Step-by-step throttle creation guide

### Step-by-Step Workflow

#### Phase 1: Discovery & Analysis (Read-Only)

1. **Understand Current State**
   - Get active ruleset: `tdwm://system/active-ruleset`
   - List all workloads: `list_active_WD` and `list_WDs`
   - Review workload distribution: `show_tdwm_summary`
   - Document baseline before making changes

2. **Identify Workload Requirements**
   - What queries should route to this workload?
   - How should queries be classified? (query band, user, account)
   - What concurrency limits are needed?
   - What priority level is appropriate?
   - Are there time-based or complexity requirements?

3. **Review Existing Configuration**
   - List filters: `tdwm://ruleset/{name}/filters`
   - List throttles: `tdwm://ruleset/{name}/throttles`
   - Check for conflicts or overlaps with existing rules
   - Identify gaps in current configuration

4. **Plan Implementation**
   - Which filters need to be created or enabled?
   - Which throttles need to be created or enabled?
   - What classification criteria should be used?
   - What is the activation sequence?

#### Phase 2: Execute Changes (Autonomous - NEW!)

5. **Select Approach: Template or Custom**
   - **Template-Based** (Recommended):
     - Browse templates: `tdwm://templates/filter` and `tdwm://templates/throttle`
     - Select templates matching use case
     - Customize parameters for your workload

   - **Custom Configuration**:
     - Validate classification types: `tdwm://reference/classification-types`
     - Validate operators: `tdwm://reference/operators`
     - Design custom classification criteria

6. **Create Filter for Query Routing**
   - **Create new filter**:
     ```
     Use: create_filter_rule(
       ruleset_name, filter_name,
       classification_criteria,
       action_type, workload_name
     )
     ```

   - **Filter routes queries** to target workload based on criteria

7. **Create Throttle for Resource Protection**
   - **Create new throttle**:
     ```
     Use: create_system_throttle(
       ruleset_name, throttle_name, throttle_type,
       limit, classification_criteria
     )
     ```

   - **Throttle limits concurrency** for workload protection

8. **Enable and Activate**
   - Enable filter: `enable_filter_rule(ruleset_name, filter_name)`
   - Enable throttle: `enable_throttle(ruleset_name, throttle_name)`
   - Check pending changes: `tdwm://ruleset/{name}/pending-changes`
   - Activate ruleset: `activate_ruleset(ruleset_name)`

#### Phase 3: Verification (Autonomous - NEW!)

9. **Verify Configuration**
   - Read back filter: `tdwm://ruleset/{name}/filter/{filter_name}`
   - Read back throttle: `tdwm://ruleset/{name}/throttle/{throttle_name}`
   - Confirm enabled states are correct
   - Confirm classification criteria match expectations

10. **Monitor Impact**
    - Wait 5-10 minutes for statistics to update
    - Check workload distribution: `show_tdwm_summary`
    - Verify queries routing to workload correctly
    - Monitor throttle statistics: `show_trottle_statistics`
    - Check TASM events: `show_tasm_even_history`

11. **Iterate if Needed**
    - If routing not working: add more classification criteria
    - If throttle too restrictive: adjust limit
    - Use configuration tools for adjustments

## Examples

### Example 1: Implement New Application Workload (Autonomous)

**Scenario**: New BI tool launching Monday, need to route queries to BI_ANALYTICS workload

**Discovery**:
```
1. list_active_WD → BI_ANALYTICS workload exists (created by DBA)
2. show_query_band → BI tool sets 'APP=BI_DASHBOARD'
3. tdwm://system/active-ruleset → "Tactical"
4. tdwm://ruleset/Tactical/filters → No BI filter exists
5. show_tdwm_summary → BI queries currently in DEFAULT workload
```

**Analysis**:
- Workload definition exists, needs filter for routing
- BI tool sets query band (simple classification)
- Need throttle to limit to 15 concurrent queries
- Can use templates for quick implementation

**Execution** (Autonomous):
```
1. Get filter template:
   tdwm://template/filter/application-basic
   → Shows APPL-based filter pattern

2. Create filter to route BI queries:
   create_filter_rule(
     ruleset_name="Tactical",
     filter_name="BI_DASHBOARD_FILTER",
     classification_criteria=[{
       "description": "BI Dashboard Application",
       "type": "APPL",
       "value": "BI_DASHBOARD",
       "operator": "I"
     }],
     action_type="ACCEPT",
     workload_name="BI_ANALYTICS"
   )

3. Get throttle template:
   tdwm://template/throttle/application-basic
   → Shows APPL-based throttle pattern

4. Create throttle to protect resources:
   create_system_throttle(
     ruleset_name="Tactical",
     throttle_name="BI_ANALYTICS_LIMIT",
     throttle_type="DM",  # Delay Management
     limit=15,
     classification_criteria=[{
       "description": "BI Analytics workload throttle",
       "type": "APPL",
       "value": "BI_DASHBOARD",
       "operator": "I"
     }]
   )

5. Enable both rules:
   enable_filter_rule(ruleset_name="Tactical", filter_name="BI_DASHBOARD_FILTER")
   enable_throttle(ruleset_name="Tactical", throttle_name="BI_ANALYTICS_LIMIT")

6. Activate:
   activate_ruleset(ruleset_name="Tactical")

7. Verify:
   tdwm://ruleset/Tactical/filter/BI_DASHBOARD_FILTER
   → Confirm filter routes to BI_ANALYTICS workload

   tdwm://ruleset/Tactical/throttle/BI_ANALYTICS_LIMIT
   → Confirm throttle limit=15

8. Monitor (wait 10 minutes):
   show_tdwm_summary
   → BI queries now in BI_ANALYTICS workload (not DEFAULT)

   show_trottle_statistics
   → BI throttle active, limit enforced
```

**Result**: BI workload fully operational with routing and protection

---

### Example 2: Emergency Workload Protection (Autonomous)

**Scenario**: Ad-hoc queries overloading system, need immediate throttling

**Discovery**: SKIP - Emergency situation requires fast action

**Execution** (Fast):
```
1. Use emergency workflow:
   tdwm://workflow/emergency-throttle

2. Create very restrictive throttle:
   create_system_throttle(
     ruleset_name="Tactical",
     throttle_name="EMERGENCY_ADHOC_LIMIT",
     throttle_type="DM",
     limit=3,  # Very restrictive
     classification_criteria=[{
       "description": "Emergency ad-hoc protection",
       "type": "USER",
       "value": "adhoc_*",  # All ad-hoc users
       "operator": "I"
     }]
   )

3. Enable and activate immediately:
   enable_throttle(ruleset_name="Tactical", throttle_name="EMERGENCY_ADHOC_LIMIT")
   activate_ruleset(ruleset_name="Tactical")

4. Monitor recovery (wait 60 seconds):
   show_physical_resources
   → CPU should drop below 90%

5. Gradual relaxation:
   modify_throttle_limit(
     ruleset_name="Tactical",
     throttle_name="EMERGENCY_ADHOC_LIMIT",
     new_limit=5
   )
   activate_ruleset(ruleset_name="Tactical")

   Wait, monitor, increase to 10 if stable

6. Cleanup when stable:
   disable_throttle(ruleset_name="Tactical", throttle_name="EMERGENCY_ADHOC_LIMIT")
   activate_ruleset(ruleset_name="Tactical")
```

**Result**: System stabilized in <5 minutes, gradual return to normal

---

### Example 3: Seasonal Workload Activation (Autonomous)

**Scenario**: Year-end processing starting, activate YEAR_END workload with filters

**Discovery**:
```
1. list_WDs → YEAR_END workload exists (inactive)
2. tdwm://ruleset/Tactical/filter/YEAR_END_FILTER → Filter exists, disabled
3. tdwm://ruleset/Tactical/throttle/YEAR_END_LIMIT → Throttle exists, disabled
4. show_tdwm_summary → No year-end queries yet
```

**Analysis**:
- Workload, filter, and throttle already exist (from last year)
- Just need to enable them for the season

**Execution** (Autonomous):
```
1. Enable year-end filter:
   enable_filter_rule(
     ruleset_name="Tactical",
     filter_name="YEAR_END_FILTER"
   )

2. Enable year-end throttle:
   enable_throttle(
     ruleset_name="Tactical",
     throttle_name="YEAR_END_LIMIT"
   )

3. Activate:
   activate_ruleset(ruleset_name="Tactical")

4. Verify:
   tdwm://ruleset/Tactical/filter/YEAR_END_FILTER
   → Confirm enabled=true

   tdwm://ruleset/Tactical/throttle/YEAR_END_LIMIT
   → Confirm enabled=true

5. Monitor:
   show_tdwm_summary
   → Year-end queries routing to YEAR_END workload

6. Schedule deactivation (manual reminder):
   "Disable YEAR_END_FILTER and YEAR_END_LIMIT on January 5"
```

**Result**: Year-end workload active with proper routing and limits

---

### Example 4: User-Based Workload Routing (Autonomous)

**Scenario**: Power users need dedicated workload with higher limits

**Discovery**:
```
1. list_active_WD → POWER_USERS workload exists
2. show_query_band → Power users DON'T set query band
3. tdwm://ruleset/Tactical/filters → No power user filter exists
4. Power users identified by account='power_user_acct'
```

**Analysis**:
- Need to create filter using ACCT classification
- Need throttle with higher limit (20 concurrent vs normal 10)

**Execution** (Autonomous):
```
1. Validate classification type:
   tdwm://reference/classification-types
   → Confirm "ACCT" is valid

2. Create filter for account-based routing:
   create_filter_rule(
     ruleset_name="Tactical",
     filter_name="POWER_USER_FILTER",
     classification_criteria=[{
       "description": "Power user account routing",
       "type": "ACCT",
       "value": "power_user_acct",
       "operator": "I"
     }],
     action_type="ACCEPT",
     workload_name="POWER_USERS"
   )

3. Create throttle with higher limit:
   create_system_throttle(
     ruleset_name="Tactical",
     throttle_name="POWER_USER_LIMIT",
     throttle_type="DM",
     limit=20,  # Higher than normal users
     classification_criteria=[{
       "description": "Power user concurrency limit",
       "type": "ACCT",
       "value": "power_user_acct",
       "operator": "I"
     }]
   )

4. Enable both:
   enable_filter_rule(ruleset_name="Tactical", filter_name="POWER_USER_FILTER")
   enable_throttle(ruleset_name="Tactical", throttle_name="POWER_USER_LIMIT")

5. Activate:
   activate_ruleset(ruleset_name="Tactical")

6. Verify:
   tdwm://ruleset/Tactical/filter/POWER_USER_FILTER
   → Confirm routes to POWER_USERS workload

   tdwm://ruleset/Tactical/throttle/POWER_USER_LIMIT
   → Confirm limit=20

7. Monitor:
   show_tdwm_summary
   → Power user queries in POWER_USERS workload
```

**Result**: Power users have dedicated workload with higher concurrency

---

### Example 5: Maintenance Window Workload (Autonomous)

**Scenario**: During Saturday maintenance, only maintenance queries should run

**Discovery**:
```
1. list_WDs → MAINTENANCE_ONLY workload exists
2. tdwm://ruleset/Tactical/filters → No maintenance filter exists
3. Need to block all non-maintenance queries during window
```

**Analysis**:
- Need filter to route maintenance user queries to MAINTENANCE_ONLY
- Need filter to REJECT all other queries
- Will enable for maintenance window, disable after

**Execution** (Autonomous):
```
1. Create maintenance filter (ACCEPT):
   create_filter_rule(
     ruleset_name="Tactical",
     filter_name="MAINTENANCE_ACCEPT",
     classification_criteria=[{
       "description": "Allow maintenance user",
       "type": "USER",
       "value": "maint_user",
       "operator": "I"
     }],
     action_type="ACCEPT",
     workload_name="MAINTENANCE_ONLY"
   )

2. Create blocking filter (REJECT):
   create_filter_rule(
     ruleset_name="Tactical",
     filter_name="MAINTENANCE_BLOCK_ALL",
     classification_criteria=[{
       "description": "Block all non-maintenance queries",
       "type": "USER",
       "value": "*",  # All users
       "operator": "I"
     }],
     action_type="REJECT",
     workload_name=None  # REJECT doesn't need workload
   )

3. Keep both DISABLED initially (will enable during maintenance):
   # Don't enable yet - wait for maintenance window

4. Activate (makes filters available, but disabled):
   activate_ruleset(ruleset_name="Tactical")

5. At maintenance start (Saturday 2 AM):
   enable_filter_rule(ruleset_name="Tactical", filter_name="MAINTENANCE_ACCEPT")
   enable_filter_rule(ruleset_name="Tactical", filter_name="MAINTENANCE_BLOCK_ALL")
   activate_ruleset(ruleset_name="Tactical")

6. At maintenance end (Saturday 10 AM):
   disable_filter_rule(ruleset_name="Tactical", filter_name="MAINTENANCE_ACCEPT")
   disable_filter_rule(ruleset_name="Tactical", filter_name="MAINTENANCE_BLOCK_ALL")
   activate_ruleset(ruleset_name="Tactical")

7. Verify normal operations resumed:
   show_tdwm_summary
   → All workloads operational
```

**Result**: Maintenance window enforced, normal operations restored after

---

## Best Practices

### General Principles
- Workload definitions created by Teradata TDWM, but filters/throttles make them functional
- Always create both filter (routing) and throttle (protection) for new workloads
- Test workload implementation in non-production first
- Document business justification for each workload
- Name filters and throttles clearly (e.g., "BI_DASHBOARD_FILTER", "BI_ANALYTICS_LIMIT")

### Discovery Before Execution (NEW ✨)
- **ALWAYS** check existing filters and throttles before creating new ones
- Use `tdwm://ruleset/{name}/filters` and `tdwm://ruleset/{name}/throttles` to explore
- Check `tdwm://ruleset/{name}/pending-changes` before activating
- Understand current workload distribution before implementing changes

### Template Usage (NEW ✨)
- Use templates for common patterns (application-based, user-based)
- Templates reduce errors by 50% compared to custom creation
- Customize template parameters for your specific workload needs

### Execution Safety (NEW ✨)
- Validate classification types against `tdwm://reference/classification-types`
- Validate operators against `tdwm://reference/operators`
- Start with conservative throttle limits, increase gradually
- Test filter routing with sample queries before full activation
- Keep emergency rollback plan (disable filter + activate)

### Validation (NEW ✨)
- Always read back filter/throttle after creation
- Confirm enabled state matches intention
- Monitor workload distribution for 15-30 minutes after activation
- Verify queries routing as expected using `show_tdwm_summary`

### Monitoring
- Monitor workload effectiveness using `show_tasm_statistics`
- Check throttle impact using `show_trottle_statistics`
- Review classification accuracy using `show_tasm_even_history`
- Set alerts for workload performance SLA violations
- Coordinate workload changes with application teams
- Document workload lifecycle events

### Related Skills
- Use **optimize-throttles** skill for adjusting throttle limits on existing workloads
- Use **tune-workloads** skill for adding classification criteria to existing filters
- Use **emergency-response** skill for crisis situations
- Use **discover-configuration** skill to inventory existing workload configurations
- Use **configure-filters** skill for detailed filter creation guidance
- Use **configure-throttles** skill for detailed throttle creation guidance
