---
name: hubitat-app-device
description: Add or remove devices from a Hubitat app instance (e.g., Maker API)
argument-hint: "add|remove|list {device_id} [{installed_app_id}]"
allowed-tools: Bash, Read, Glob, Grep
---

# Hubitat App Device Skill

Add or remove devices from an installed app's device input. Primary use case: managing Maker API's device list for automated testing.

## How It Works

A single POST to `/installedapp/update/json` with `_action_update=Done` saves the app configuration. The `settings[{deviceInput}]` field contains the comma-separated list of device IDs — include the new device for add, exclude it for remove. All other settings must be echoed back with their type metadata.

## Instructions

### Step 1: Read Configuration

Read `.hubitat.json` from the project root to get `hub_ip` and `maker_api.app_id`.

### Step 2: Parse Arguments

Parse `$ARGUMENTS`:

- **`add {device_id}`** — add device to Maker API (uses `maker_api.app_id`)
- **`remove {device_id}`** — remove device from Maker API
- **`add {device_id} {installed_app_id}`** — add device to a specific app instance
- **`remove {device_id} {installed_app_id}`** — remove device from a specific app instance
- **`list [{installed_app_id}]`** — show devices currently in the app

If no installed app ID is given, default to `maker_api.app_id` from the config.

### Step 3: Fetch App Configuration

```bash
curl -s "http://{hub_ip}/installedapp/configure/json/{installedAppId}"
```

From the JSON response, extract:

1. **`app.version`** — config version (usually `1`)
2. **`app.label`** — the app's display label
3. **`configPage.name`** — page name (usually `mainPage`)
4. **`configPage.sections[].input[]`** — all input definitions (each has `name`, `type`, `multiple`)
5. **`configPage.sections[].body[]`** — body elements; find any with `element: "label"` (these are label inputs)
6. **`settings`** — current values for all inputs
7. **Device input** — the input whose `type` starts with `capability.` (e.g., `pickedDevices` with type `capability.*`)

The `settings` value for a device input is either:
- A **map** like `{"12": "Device Name", "14": "Other"}` — keys are device IDs
- **null** — no devices selected

### Step 4: For "list" — Display and Stop

Show the app name, device input name, and a table of current device IDs and names. Then stop.

### Step 5: Validate

- **add**: confirm device ID is not already in the device list. If it is, report "already present" and stop.
- **remove**: confirm device ID IS in the device list. If not, report "not found" and stop.

### Step 6: Build and Send the POST

Use Python (`python3`) with `urllib.request` and `urllib.parse`.

Build form fields as a **list of tuples** (preserves order, allows empty-string keys):

#### Fixed header fields

| Field | Value |
|-------|-------|
| `_action_update` | `Done` |
| `formAction` | `update` |
| `id` | installed app ID (string) |
| `version` | `app.version` (string) |
| `appTypeId` | empty string |
| `appTypeName` | empty string |
| `currentPage` | page name from config |
| `pageBreadcrumbs` | `%5B%5D` |

#### Label inputs

For each body element with `element: "label"`:

| Field | Value |
|-------|-------|
| `{name}.type` | `text` |
| `{name}` | value from `app.label` (NOT from `settings`) |

#### Regular inputs

For each input from `configPage.sections[].input[]`, in order:

| Field | Value |
|-------|-------|
| `{name}.type` | the input's `type` |
| `{name}.multiple` | `true` or `false` (lowercase string) |

Then, if the input is a **bool** type:

| Field | Value |
|-------|-------|
| `checkbox[{name}]` | `on` |

Then, if this is the **device input** (type starts with `capability.`):

| Field | Value |
|-------|-------|
| `settings[{name}]` | comma-separated device IDs (see below) |
| `deviceList` | the input name |
| (empty string `""`) | empty string |

Otherwise (non-device inputs):

| Field | Value |
|-------|-------|
| `settings[{name}]` | current value (see conversion rules below) |

#### Device ID list for `settings[{deviceInput}]`

- **add**: existing device IDs + the new device ID, comma-separated
- **remove**: existing device IDs minus the removed device ID, comma-separated

#### Fixed footer fields

| Field | Value |
|-------|-------|
| `referrer` | `http://{hub_ip}/installedapp/list` |
| `url` | `http://{hub_ip}/installedapp/configure/{id}/{pageName}` |
| `_cancellable` | `false` |

#### Settings Value Conversion

When reading `settings` values for the form body:
- **String** (`"true"`, `"false"`, `"some text"`) → use as-is
- **null** → `[]` (the string `[]`)
- **Map** (device inputs) → comma-separated keys

#### Send the POST

```python
body = urllib.parse.urlencode(fields)
req = urllib.request.Request(
    f"http://{hub_ip}/installedapp/update/json",
    data=body.encode(),
    headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
)
resp = urllib.request.urlopen(req)
```

Expected success response: `{"status":"success","location":"/installedapp/list"}`

### Step 7: Verify

Fetch the config again and check `settings.{deviceInputName}` to confirm:
- **add**: the new device ID is now a key in the map
- **remove**: the device ID is no longer a key in the map

### Step 8: Report Result

Summarize:
- Action performed (added/removed)
- Device ID, device name, and the app name
- Updated device list (ID and name table)
