---
name: hubitat-run
description: Send commands to Hubitat devices or interact with app instances
argument-hint: "[device_id] [command] or [filepath]"
allowed-tools: Bash, Read, Glob, Grep
---

# Hubitat Run Skill

Send commands to devices or interact with app instances on the Hubitat hub.

## Instructions

Follow these steps exactly:

### Step 1: Read Configuration

Read `.hubitat.json` from the project root to get `hub_ip` and check if `maker_api` credentials are configured (both `app_id` and `token` must be non-null).

### Step 2: Parse Arguments

`$ARGUMENTS` can be one of:

1. **`{device_id} {command}`** — a numeric device ID and a command to send (e.g., `42 on`, `42 off`, `42 setLevel 50`)
2. **`{device_id}`** — just a device ID to show its current status
3. **`{filepath}`** — a `.groovy` filename to discover which devices/apps use it
4. **No arguments** — prompt the user for what they want to do

### Step 3: Smart Discovery (if filepath given)

If the argument looks like a file path (contains `/` or ends in `.groovy`):

1. Read the file and extract the `name` from the `definition()` block
2. Determine if it's an app or driver (based on `apps/` or `drivers/` in path)
3. Query the hub:
   - **Drivers**: `curl -s "http://{hub_ip}/hub2/userDeviceTypes"` → find by name → get `usedBy` list
   - **Apps**: `curl -s "http://{hub_ip}/hub2/userAppTypes"` → find by name → get `usedBy` list
4. Display the list of devices/instances using this code with their IDs and names
5. Ask the user which device they want to interact with

### Step 4: Execute Command

#### If Maker API is configured:

**To send a command:**
```bash
curl -s "http://{hub_ip}/apps/api/{app_id}/devices/{device_id}/{command}?access_token={token}"
```

For commands with arguments (e.g., `setLevel 50`), the format is:
```bash
curl -s "http://{hub_ip}/apps/api/{app_id}/devices/{device_id}/{command}/{value}?access_token={token}"
```

**To get device status:**
```bash
curl -s "http://{hub_ip}/apps/api/{app_id}/devices/{device_id}?access_token={token}"
```

Display the device's current attributes in a readable format.

#### If Maker API is NOT configured:

Maker API is required for sending commands. Tell the user:

1. They need to install "Maker API" on their hub
2. Add the target device(s) to Maker API's allowed devices
3. Update `.hubitat.json` with the `app_id` and `token` from Maker API
4. Provide the direct link to the device in the hub UI: `http://{hub_ip}/device/edit/{device_id}`

Even without Maker API, you can still show device info by querying:
```bash
curl -s "http://{hub_ip}/hub2/devicesList"
```
Find the device by ID and display its current states and attributes.

### Step 5: Report Result

After sending a command:

1. Wait 1 second for the device to process
2. Query the device status again to confirm the state changed
3. Report the result: what command was sent, what the device's new state is

### Step 6: App Instances

For interacting with app instances (if the user specifies an app):

- Provide the configuration link: `http://{hub_ip}/installedapp/configure/{instance_id}`
- Show the app's current status from the hub's app list
