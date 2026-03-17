---
name: hubitat-install
description: Create, install, and configure a Hubitat app or driver from a local Groovy file
argument-hint: "[filepath]"
allowed-tools: Bash, Read, Glob, Grep
---

# Hubitat Install Skill

Create a new app or driver on the hub from a local Groovy file, install an instance, and open configuration.

## Instructions

Follow these steps exactly:

### Step 1: Read Configuration

Read `.hubitat.json` from the project root to get `hub_ip`.

### Step 2: Identify the File

- If `$ARGUMENTS` contains a filepath, use that file.
- Otherwise, find the most recently modified `.groovy` file using: `ls -t apps/*.groovy drivers/**/*.groovy 2>/dev/null | head -1`
- Confirm the file exists and read its contents.

### Step 3: Determine Type (App vs Driver)

- If the file path contains `apps/` → it's an **app**
- If the file path contains `drivers/` → it's a **driver**

### Step 4: Extract Name from Source

Read the file and extract the `name` value from the `definition()` block.

### Step 5: Check if Already Exists

Query the hub to see if this code already exists:

- **Apps**: `curl -s "http://{hub_ip}/hub2/userAppTypes"`
- **Drivers**: `curl -s "http://{hub_ip}/hub2/userDeviceTypes"`

Search for a matching `name`. If found, report the existing ID and ask the user whether to:
1. Skip creation and just install a new instance of the existing app/driver
2. Abort

### Step 6: Create on Hub (if new)

Create the app or driver code on the hub:

```bash
python3 -c "
import json
with open('{FILEPATH}') as f:
    source = f.read()
payload = json.dumps({'source': source, 'version': 1})
with open('/tmp/hubitat_payload.json', 'w') as f:
    f.write(payload)
"
curl -s -X POST "http://{hub_ip}/{type}/saveOrUpdateJson" \
  -H "Content-Type: application/json" \
  -d @/tmp/hubitat_payload.json
```

Where `{type}` is `app` or `driver`.

Expected response: `{"success":true, "message":"", "id":..., "version":1}`

If `success` is false, report the error and stop.

### Step 7: Install Instance (Apps only)

For apps, create an installed instance:

```bash
curl -s "http://{hub_ip}/installedapp/create/{appTypeId}"
```

Parse the response to get the installed app ID.

Then report the configuration link:
```
http://{hub_ip}/installedapp/configure/{installedAppId}
```

For drivers, there is no instance to install — the driver becomes available for device assignment. Report that the driver is now available and link to the device creation page:
```
http://{hub_ip}/device/create
```

### Step 8: Report Result

Summarize what was done:
- App/driver name and hub ID
- Whether it was newly created or already existed
- For apps: the installed instance ID and configuration link
- For drivers: that it's available for device assignment
