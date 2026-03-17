---
name: home-automation
cluster: iot
description: "Integrate smart homes with Home Assistant, HomeKit, Google Home, Matter."
tags: ["iot","home"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "home-automation iot"
---

# home-automation

## Purpose
This skill integrates smart home systems using Home Assistant, HomeKit, Google Home, and Matter protocols, allowing the AI to control IoT devices programmatically for automation tasks.

## When to Use
Use this skill for automating home environments, such as controlling lights, thermostats, or security systems via IoT platforms. Apply it in scenarios like smart home apps, voice assistant integrations, or custom scripts for daily routines (e.g., turning off lights at bedtime).

## Key Capabilities
- Connect to Home Assistant via REST API for device state management.
- Integrate with HomeKit using the HAP protocol for Apple ecosystem devices.
- Use Google Home APIs for controlling compatible smart devices.
- Handle Matter devices through bridge APIs for cross-platform compatibility.
- Specifics: Home Assistant API endpoint for states is `GET /api/states`; HomeKit requires Bonjour discovery; Google Home uses OAuth 2.0 with scopes like `https://www.googleapis.com/auth/homeautomation`; Matter involves IP-based commissioning.

## Usage Patterns
To use this skill, first initialize it with authentication. Import via `skill.use('home-automation')`, then call methods like `skill.connect(service, key)`. For sequential tasks, chain calls: connect, query state, execute action. Always handle async operations with promises or callbacks. Config format: JSON objects, e.g., `{"service": "home-assistant", "api_url": "http://localhost:8123"}`.

## Common Commands/API
- CLI: Run `openclaw home-automation connect --service home-assistant --api-url http://localhost:8123 --key $HOME_ASSISTANT_API_KEY` to establish a connection.
- API: Use `POST /api/services` for Home Assistant actions; example endpoint for Google Home: `GET https://homegraph.googleapis.com/v1/devices`.
- Code snippets:
  ```skill
  skill.use('home-automation')
  skill.connect('home-assistant', { apiUrl: 'http://localhost:8123', key: process.env.HOME_ASSISTANT_API_KEY })
  ```
  ```skill
  const state = await skill.call('getState', { entity: 'light.living_room' })
  console.log(state)
  ```
  ```skill
  skill.execute('turnOn', { device: 'light.kitchen', service: 'homekit' })
  ```
  Use env vars for keys: `$HOME_ASSISTANT_API_KEY` for Home Assistant, `$GOOGLE_HOME_TOKEN` for Google Home.

## Integration Notes
Authenticate using env vars (e.g., `$HOME_ASSISTANT_API_KEY`) before operations. For HomeKit, ensure devices are paired via the Home app; use HAP-NodeJS library for custom integrations. Google Home requires OAuth flow—redirect to `https://accounts.google.com/o/oauth2/v2/auth`. Matter integration needs a compatible bridge; config format: YAML like `matter: { bridge_ip: '192.168.1.100', port: 5540 }`. Avoid mixing protocols in one call; use wrappers for error-free transitions between services.

## Error Handling
Check for HTTP errors (e.g., 401 Unauthorized) by wrapping calls in try-catch blocks. For authentication failures, retry with refreshed tokens. Common errors: API rate limits (e.g., Home Assistant returns 429); handle with exponential backoff. Code snippet:
```skill
try {
  await skill.call('getState', { entity: 'light.living_room' })
} catch (error) {
  if (error.code === 401) console.error('Reauthenticate with $HOME_ASSISTANT_API_KEY')
  else throw error
}
```
Log detailed responses and use skill-specific error codes for debugging.

## Concrete Usage Examples
1. Automate lights based on time: Use `skill.connect('home-assistant', { key: process.env.HOME_ASSISTANT_API_KEY })`, then `skill.execute('turnOff', { entity: 'light.all' })` in a scheduled script to turn off all lights at 11 PM.
2. Integrate with Google Home for temperature control: Call `skill.use('home-automation').connect('google-home', { token: process.env.GOOGLE_HOME_TOKEN })`, followed by `skill.call('setThermostat', { deviceId: 'thermostat.living_room', temperature: 72 })` to adjust the thermostat.

## Graph Relationships
- Cluster: Connected to 'iot' cluster for broader IoT integrations.
- Tags: Links to skills with 'iot' and 'home' tags, such as device-control or smart-security skills.
- Relationships: This skill depends on authentication services; it integrates with external APIs like Home Assistant's REST endpoints and Google Home's OAuth flows.
