---
name: hubitat-push
description: Push Groovy app or driver code to Hubitat hub and report compile status
argument-hint: "[filepath]"
allowed-tools: Bash, Read, Glob, Grep
---

# Hubitat Push Skill

Push a local Groovy file to the Hubitat hub, compile it, and report the result.

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
- This determines the API endpoints to use:
  - Driver: `/hub2/userDeviceTypes`, `/driver/ajax/code`, `/driver/ajax/update`
  - App: `/hub2/userAppTypes`, `/app/ajax/code`, `/app/ajax/update`

### Step 4: Extract Name from Source

Read the file and extract the `name` value from the `definition()` block. The format looks like:

```groovy
definition(
    name: "My Driver Name",
    namespace: "iamtrep",
    ...
)
```

Extract the name string (the value after `name:`).

### Step 5: Find the Hub ID

Query the hub for the list of user code to find the matching ID:

- **Drivers**: `curl -s "http://{hub_ip}/hub2/userDeviceTypes"`
- **Apps**: `curl -s "http://{hub_ip}/hub2/userAppTypes"`

The response is a JSON array. Find the entry where `name` matches the name extracted in Step 4. Get the `id` field. Also note the `usedBy` field for later.

If no match is found, the code is not yet on the hub. **Use the `/hubitat-install` skill** to create it, then stop (install will handle creation and report the result). Tell the user you are invoking `/hubitat-install`.

### Step 6: Get Current Version

Fetch the current version number (required for the update API):

- **Drivers**: `curl -s "http://{hub_ip}/driver/ajax/code?id={ID}"`
- **Apps**: `curl -s "http://{hub_ip}/app/ajax/code?id={ID}"`

Extract the `version` field from the JSON response.

### Step 7: Push the Code

POST the updated source to the hub:

- **Drivers**: `POST http://{hub_ip}/driver/ajax/update`
- **Apps**: `POST http://{hub_ip}/app/ajax/update`

Use curl with:
```bash
curl -s -X POST "http://{hub_ip}/{type}/ajax/update" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "id={ID}" \
  --data-urlencode "version={VERSION}" \
  --data-urlencode "source@{FILEPATH}"
```

Where `{type}` is `driver` or `app`.

Note: `--data-urlencode "source@{FILEPATH}"` reads and URL-encodes the file contents automatically.

### Step 8: Report Result

Parse the JSON response:

- On success: `{"id":..., "version":..., "status":"success"}`
  - Report: "Successfully pushed {name} to hub (version {new_version})"
- On error: The response will contain error/status details
  - Report the compilation errors clearly so the user can fix them

### Step 9: Show Usage

From the data retrieved in Step 5, show which devices or app instances use this code:

- For drivers: list the devices using this driver (from `usedBy` in the userDeviceTypes response)
- For apps: list the installed instances (from `usedBy` in the userAppTypes response)

Format as a simple list with device/app IDs and names.
