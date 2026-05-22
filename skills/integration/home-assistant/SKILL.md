---
name: home-assistant
description: This skill should be used when helping with Home Assistant setup, including creating automations, modifying dashboards, checking entity states, debugging automations, and managing the smart home configuration. Use this for queries about HA entities, YAML automation/dashboard generation, or troubleshooting HA issues.
---

# Home Assistant Helper

## Overview

This skill provides tools and workflows for working with Home Assistant installations. It enables querying the live HA instance for entities, services, and configuration data, debugging automations, and generating YAML configurations for automations and dashboards.

**Key Capabilities:**
- Query entities, states, and services from the live HA installation
- Search for similar entities to use as examples
- Check automation states and execution history
- Generate YAML configurations for copy/paste into HA
- Find real examples from the user's setup to inform new configurations

## Core Workflow

When helping with Home Assistant tasks, follow this general approach:

1. **Understand the requirement** - What is the user trying to accomplish?
2. **Discover existing entities** - Use scripts to find relevant entities in their setup
3. **Find similar examples** - Search for existing automations or entities that do something similar
4. **Generate YAML** - Create well-formed YAML that can be copied directly into HA
5. **Explain the configuration** - Describe what the YAML does and how to install it

## Available Scripts

All scripts require the `HA_TOKEN` environment variable to be set, which contains the Home Assistant long-lived access token. The HA instance is available at `http://homeassistant.local:8123`.

**Important:** All scripts now use `uv` with inline PEP 723 dependency declarations and the `homeassistant-api` library for consistent, maintainable code. Dependencies are automatically installed by `uv` on first run.

### Entity Discovery

#### `ha_get_entities.py [domain]`
Retrieve all entities, optionally filtered by domain.

**Usage:**
```bash
uv run scripts/ha_get_entities.py           # All entities
uv run scripts/ha_get_entities.py light     # Just lights
uv run scripts/ha_get_entities.py sensor    # Just sensors
```

**When to use:** To discover what entities are available, especially when building new automations.

#### `ha_get_state.py <entity_id>`
Get the current state and attributes of a specific entity.

**Usage:**
```bash
uv run scripts/ha_get_state.py light.living_room
```

**When to use:** To check current state, available attributes, or confirm an entity exists.

#### `ha_search_similar_entities.py <pattern>`
Search for entities matching a pattern in their entity_id or friendly_name.

**Usage:**
```bash
uv run scripts/ha_search_similar_entities.py "bedroom"
uv run scripts/ha_search_similar_entities.py "motion"
uv run scripts/ha_search_similar_entities.py "temperature"
```

**When to use:** To find entities related to what the user wants to automate. This is especially useful for finding examples before creating new automations.

### Automation Management

#### `ha_get_automations.py [search_term]`
Retrieve all automations, optionally filtered by search term.

**Usage:**
```bash
uv run scripts/ha_get_automations.py              # All automations
uv run scripts/ha_get_automations.py motion       # Automations with 'motion'
uv run scripts/ha_get_automations.py light        # Automations with 'light'
```

**When to use:** To find existing automations that are similar to what the user wants to create. Use these as templates.

### Automation Trace Analysis

#### `ha_list_traces.py [automation_id]`
List automation execution traces with timestamps and status.

**Usage:**
```bash
uv run scripts/ha_list_traces.py                    # All traces
uv run scripts/ha_list_traces.py 1761430536701      # Specific automation traces (using numeric ID)
```

**Important:** Use the numeric automation ID (e.g., `1761430536701`), not the full entity_id (e.g., `automation.bedroom_light`). You can find the numeric ID in the automation's attributes from `ha_get_automations.py` output.

**When to use:** To see recent automation runs, their status, and timing. Use this to identify which run IDs to investigate further.

**Output includes:**
- Run ID (for use with `ha_get_trace.py`)
- Timestamp
- Execution state (stopped, running, etc.)
- Script execution status (finished, failed_single, failed_conditions, etc.)
- Last step executed
- Any errors

#### `ha_get_trace.py <automation_id> <run_id>`
Get detailed step-by-step trace for a specific automation run.

**Usage:**
```bash
uv run scripts/ha_get_trace.py 1761430536701 1ceef6b2b6f63a8745eb5dba3fe12f71
```

**Important:** Use the numeric automation ID (e.g., `1761430536701`), not the full entity_id.

**When to use:** To debug a specific automation run. Shows the complete execution path including:
- Trigger details
- Condition evaluations (pass/fail)
- Actions executed
- Variables at each step
- Timing information
- Error details if failed

**Tip:** Get the run_id from `ha_list_traces.py` output.

#### `ha_trace_summary.py <automation_id>`
Get aggregated statistics for an automation's execution history.

**Usage:**
```bash
uv run scripts/ha_trace_summary.py 1761430536701
```

**Important:** Use the numeric automation ID (e.g., `1761430536701`), not the full entity_id.

**When to use:** To understand automation reliability and performance over time.

**Output includes:**
- Total runs
- Success/failure counts and rates
- Average/min/max execution times
- Common error patterns
- Distribution of where executions complete

### Service Discovery

#### `ha_get_services.py [domain]`
Get all available services with descriptions and field information.

**Usage:**
```bash
uv run scripts/ha_get_services.py              # All services
uv run scripts/ha_get_services.py light        # Just light services
uv run scripts/ha_get_services.py climate      # Just climate services
```

**When to use:** To discover what services are available and what parameters they accept.

### Configuration

#### `ha_get_config.py`
Get Home Assistant configuration including version, location, and components.

**Usage:**
```bash
uv run scripts/ha_get_config.py
```

**When to use:** To understand the HA setup, available integrations, or system information.

#### `ha_get_config_entries.py [domain]`
Get Home Assistant config entries, optionally filtered by domain. This is essential for services that require a `config_entry_id`, such as `telegram_bot.send_message`.

**Usage:**
```bash
uv run scripts/ha_get_config_entries.py              # All config entries
uv run scripts/ha_get_config_entries.py telegram_bot # Just Telegram bots
uv run scripts/ha_get_config_entries.py mqtt         # Just MQTT entries
```

**When to use:** When you need to get config_entry_id for services like Telegram notifications, or to discover what integrations are configured.

### Service Calling

#### `ha_call_service.py <domain> <service> <json_data>`
Call a Home Assistant service (use with caution).

**Usage:**
```bash
uv run scripts/ha_call_service.py light turn_on '{"entity_id": "light.living_room"}'
```

**When to use:** Rarely. Generally only for testing or when the user explicitly asks to control something.

## Typical Workflows

### Creating a New Automation

1. **Understand the goal** - Ask clarifying questions about triggers, conditions, and actions
2. **Find similar entities** - Use `ha_search_similar_entities.py` to find relevant entities
3. **Search for similar automations** - Use `ha_get_automations.py` with search terms to find examples
4. **Review existing automation** - If a similar one exists, examine its structure
5. **Generate YAML** - Create well-formatted YAML with:
   - Descriptive alias
   - Clear description
   - Appropriate triggers
   - Relevant conditions
   - Necessary actions
   - Proper mode (single, restart, queued, parallel)
6. **Provide copy-paste YAML** - Format for easy copying into HA configuration
7. **Explain** - Describe what the automation does and how to add it to HA

### Debugging an Automation

1. **Check automation status** - Use `uv run scripts/ha_get_state.py automation.automation_name` to check:
   - Current state (on/off)
   - Last triggered time
   - Current execution count
   - Automation mode
2. **Review execution history** - Use trace analysis tools (use numeric automation ID from attributes):
   - `uv run scripts/ha_trace_summary.py <numeric_id>` - Get success rate and common issues
   - `uv run scripts/ha_list_traces.py <numeric_id>` - See recent runs
   - `uv run scripts/ha_get_trace.py <numeric_id> <run_id>` - Detailed step-by-step trace
3. **Analyze trace data** - Look for:
   - Which trigger fired
   - Whether conditions passed or failed
   - Which actions executed successfully
   - Where the automation stopped or errored
   - Variable values at each step
4. **Check related entities** - Use `uv run scripts/ha_get_state.py` to verify trigger entities are in expected states
5. **Review the automation configuration** - Use `uv run scripts/ha_get_automations.py` to see the full automation details
6. **Identify the issue** - Based on trace data, state information, and configuration review
7. **Suggest fix** - Provide corrected YAML or configuration changes

**Trace-based Debugging Workflow:**
```bash
# Step 1: Get the automation details to find the numeric ID
uv run scripts/ha_get_automations.py problem_automation

# Step 2: Check if automation has been running and get stats (use numeric ID from step 1)
uv run scripts/ha_trace_summary.py 1761430536701

# Step 3: List recent runs to find failing ones (use numeric ID)
uv run scripts/ha_list_traces.py 1761430536701

# Step 4: Get detailed trace for a specific failed run (use numeric ID)
uv run scripts/ha_get_trace.py 1761430536701 <run_id_from_step_3>

# Step 5: Examine the trace to see exactly where and why it failed
```

### Modifying a Dashboard

1. **Understand desired changes** - What should the dashboard show?
2. **Find relevant entities** - Use entity discovery scripts
3. **Generate Lovelace YAML** - Create dashboard card configuration
4. **Provide copy-paste YAML** - User will manually add to their dashboard
5. **Explain card configuration** - Describe options and customization

### Exploring Entity States

1. **Use search or domain filtering** - Find entities of interest
2. **Check specific states** - Get detailed state information
3. **Report findings** - Present relevant information clearly

### Sending Telegram Notifications

Telegram notifications require using the `telegram_bot.send_message` service with a `config_entry_id` parameter (not the notify service pattern).

**Workflow:**
1. **Get the Telegram bot config_entry_id** - Use `uv run scripts/ha_get_config_entries.py telegram_bot` to find the config entry ID
2. **Use the telegram_bot.send_message service** - Include the config_entry_id in the action data

**Example Automation with Telegram Notification:**
```yaml
alias: Example Telegram Alert
description: Send a Telegram notification when something happens
triggers:
  - entity_id: binary_sensor.front_door
    to: "on"
    trigger: state
conditions: []
actions:
  - action: telegram_bot.send_message
    data:
      message: "Front door opened at {{ now().strftime('%I:%M %p') }}"
      config_entry_id: 01JZE11D7Y6B7C3WCARWVZRYNH  # Get this from ha_get_config_entries.py
mode: single
```

**Note:** The `config_entry_id` is specific to your Telegram bot configuration. Always use `uv run scripts/ha_get_config_entries.py telegram_bot` to get the correct ID for your setup.

## Important Notes

### YAML Output Format

When generating YAML configurations, always:
- Use proper YAML formatting with 2-space indentation
- Include helpful comments where appropriate
- Provide descriptive aliases and descriptions
- Use appropriate trigger platforms (state, time, numeric_state, etc.)
- Include mode settings (single, restart, queued, parallel)
- Format for easy copy-paste into HA

### Manual Installation Required

The user must manually copy/paste generated YAML into Home Assistant. Make this clear and provide instructions:
- For automations: Configuration → Automations & Scenes → Add Automation → Edit in YAML
- For dashboards: Dashboard → Edit Dashboard → Raw Configuration Editor
- For configuration.yaml additions: Edit the file and restart HA

### Browser Automation for Screenshots

If the user asks for screenshots of dashboards or wants to see the current UI state, the Playwright browser automation tools can be used to navigate to the HA instance and capture screenshots. The user will need to handle authentication.

### Service Calls

Be cautious about calling services that change state. Generally only do this when explicitly requested by the user or for testing purposes.

### Entity Naming

All entities follow the pattern `domain.object_id` where common domains include:
- `light` - Lights
- `switch` - Switches
- `sensor` - Sensors (read-only)
- `binary_sensor` - Binary sensors (on/off)
- `climate` - Thermostats
- `automation` - Automations
- `script` - Scripts
- `input_boolean`, `input_number`, `input_select`, `input_text`, `input_datetime` - Helper entities
- `person` - People
- `device_tracker` - Device tracking
- `camera` - Cameras
- `media_player` - Media players
- `cover` - Covers (blinds, garage doors)
- `fan` - Fans
- `lock` - Locks

### Common Trigger Platforms

- `state` - Entity state changes
- `numeric_state` - Numeric value crosses threshold
- `sun` - Sunrise/sunset
- `time` - Specific time
- `time_pattern` - Time pattern (every N minutes)
- `event` - HA event fired
- `webhook` - Webhook trigger
- `zone` - Enter/leave zone
- `device` - Device-specific trigger

### Common Condition Platforms

- `state` - Entity state equals value
- `numeric_state` - Numeric comparison
- `time` - Time window
- `sun` - Before/after sunrise/sunset
- `zone` - Person in zone
- `template` - Template evaluation

### Automation Modes

- `single` - Don't start new run if already running
- `restart` - Restart automation if triggered while running
- `queued` - Queue runs if already running
- `parallel` - Allow multiple simultaneous runs
