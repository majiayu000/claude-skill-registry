---
name: mcp-hass
description: The skill for control Home Assistant smart home devices and query states using MCP protocol.
---

# Home Assistant
Control Home Assistant smart home and query states using MCP protocol.

## Prerequisites
Enable MCP server in Home Assistant:
- Browse to your Home Assistant instance.
- Go to Settings > Devices & services.
- In the bottom right corner, select the [+ Add Integration](https://my.home-assistant.io/redirect/config_flow_start?domain=mcp) button.
- From the list, select Model Context Protocol.
- Follow the instructions on screen to complete the setup.

## Config
When prompted that the MCP server does not exist, remind the user to configure the `HASS_BASE_URL` and `HASS_ACCESS_TOKEN` environment variables by executing the following command to add the configuration:
```shell
npx -y mcporter config add home-assistant \
  --transport http \
  --url "${HASS_BASE_URL:-http://homeassistant.local:8123}/api/mcp" \
  --header "Authorization=Bearer \${HASS_ACCESS_TOKEN}"
```

## Usage
```shell
# Get states
npx -y mcporter call home-assistant.GetLiveContext

# Turn on the device
npx -y mcporter call home-assistant.HassTurnOn(name: "Bedroom Light")
npx -y mcporter call home-assistant.HassTurnOn(name: "Light", area: "Bedroom")

# Turn off the device
npx -y mcporter call home-assistant.HassTurnOff(name: "Bedroom Light")
npx -y mcporter call home-assistant.HassTurnOff(area: "Bedroom", domain: ["light"])

# Control light
# brightness: The percentage of the light, where 0 is off and 100 is fully lit.
# color: Name of color
npx -y mcporter call home-assistant.HassLightSet(name: "Bedroom Light", brightness: 50)

# Control fan
# percentage: The percentage of the fan, where 0 is off and 100 is full speed.
npx -y mcporter call home-assistant.HassFanSetSpeed(name: "Fan", area: "Bedroom", percentage: 80)
```

Execute the following command to learn about specific usage methods:
- `npx -y mcporter list home-assistant --schema --all-parameters`

## About `mcporter`
- To improve compatibility, use `npx -y mcporter` instead of `mcporter` when executing commands.
- https://github.com/steipete/mcporter/raw/refs/heads/main/docs/call-syntax.md
- https://github.com/steipete/mcporter/raw/refs/heads/main/docs/cli-reference.md
