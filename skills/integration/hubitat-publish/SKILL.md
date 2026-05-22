---
name: hubitat-publish
description: Publish a driver or app to other Hubitat hubs on the same account
argument-hint: "[driver/app name, filepath, or ID]"
allowed-tools: Bash, Read, Glob, Grep
---

# Hubitat Publish Skill

Publish a driver or app's code to all other Hubitat hubs linked to the same account, and report distribution status.

## Instructions

Follow these steps exactly:

### Step 1: Read Configuration

Read `.hubitat.json` from the project root to get `hub_ip`.

### Step 2: Identify the Code and Type

Check `$ARGUMENTS`:

- **If a numeric ID** — use it directly. You'll need to determine the type (driver or app) by checking both `userDeviceTypes` and `userAppTypes`.
- **If a filepath** — determine the type from the path:
  - Path contains `drivers/` → it's a **driver**
  - Path contains `apps/` → it's an **app**
  - Extract the `name` from the file's `definition()` block and resolve to an ID.
- **If a name** — search both `userDeviceTypes` and `userAppTypes` for a case-insensitive match. Get the `id` and determine the type from which list matched.
- **If no argument** — find the most recently modified `.groovy` file using `ls -t apps/*.groovy drivers/**/*.groovy 2>/dev/null | head -1`, then resolve as above.

To resolve names to IDs:
- **Drivers**: `curl -s "http://{hub_ip}/hub2/userDeviceTypes"`
- **Apps**: `curl -s "http://{hub_ip}/hub2/userAppTypes"`

If no match is found on the hub, report the error and stop.

### Step 3: Publish the Code

Initiate publishing by calling:

```bash
curl -s "http://{hub_ip}/hub/publishCode/{type}/{id}"
```

Where `{type}` is `driver` or `app`.

Report the initial response to the user. The response is JSON like:
```json
{"success":true,"completed":false,"hubs":[{"id":"...","name":"Chalet","status":"Pending"},...]}
```

### Step 4: Check Distribution Status

Poll the publish status endpoint:

```bash
curl -s "http://{hub_ip}/hub/publishCode/status"
```

The response is JSON:
```json
{"success":true,"completed":false,"hubs":[{"id":"...","name":"Chalet","status":"Pending"},{"id":"...","name":"Maison","status":"Done"}]}
```

- If `completed` is `false`, wait 2 seconds and poll again (up to 15 attempts).
- Once `completed` is `true` (or on error/timeout), report the final status.

### Step 5: Report Result

Summarize what happened:

- Name, type (driver/app), and ID that was published
- A markdown table of target hubs with columns: **Hub Name**, **Status**
- Any errors encountered
