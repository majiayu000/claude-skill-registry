---
name: esp32-workbench-integration
description: >
  Integrates an ESP32 project with the Universal ESP32 Workbench. Adds firmware
  modules (UDP logging, WiFi provisioning, OTA, BLE command handling, strategic
  log messages), updates build config, then writes the Workbench operations,
  Testing, and Appendix chapters into the project's existing FSD.
  Triggers on "integrate workbench", "add workbench", "workbench integration",
  "set up project", "add testing", "add tester".
---

# ESP32 Workbench Integration

This is a procedure. When triggered, read the project's existing FSD, integrate
the firmware with the workbench infrastructure (UDP logging, OTA, BLE command
handling, strategic log messages), then write the operational, testing, and
appendix chapters into the FSD.

**Prerequisite:** The project must already have an FSD with at least a System
Overview and Functional Requirements section. Use the `fsd-writer` skill first
to generate one from a rough description if needed.

The workbench provides the **test infrastructure**. This skill adds both the
**firmware integration** (modules the workbench needs to interact with the
device) and the **FSD documentation** (operational guide, test plan,
troubleshooting).

## FSD Document Structure

This skill operates on FSDs produced by the `fsd-writer` skill, which uses
this canonical numbered structure:

```
# <Project Name> — Functional Specification Document (FSD)
## 1. System Overview                    ← pre-existing (read-only)
## 2. System Architecture                ← pre-existing (read-only)
## 3. Implementation Phases              ← pre-existing (read-only)
## 4. Functional Requirements            ← pre-existing (read-only)
## 5. Risks, Assumptions & Dependencies  ← pre-existing (read-only)
## 6. Interface Specifications           ← pre-existing (read-only)
## 7. Operational Procedures             ← REPLACED by this skill with workbench-specific content
## 8. Verification & Validation          ← REPLACED by this skill with workbench test cases
## 9. Troubleshooting Guide              ← REPLACED by this skill with workbench diagnostics
## 10. Appendix                          ← REPLACED by this skill with logging strategy + constants
```

**Sections 1–6** are written by the `fsd-writer` skill and contain system
overview, architecture, phases, requirements, risks, and interfaces. This skill
reads them to extract features, phases, and constants but does not modify them.

**Sections 7–10** are written (or replaced) by this skill with workbench-specific
operational procedures, test cases, troubleshooting, and appendix content.

Steps 1–7 handle firmware integration. Steps 8–12 write FSD sections 7–10.

## Template Reference

All template code lives in `Universal-ESP32-Workbench/test-firmware/`. When adding modules, copy from these templates and customize project-specific values:

| Module | Template source | Customization |
|--------|----------------|---------------|
| `udp_log.c/.h` | `test-firmware/main/udp_log.c` | None (universal) |
| `wifi_prov.c/.h` | `test-firmware/main/wifi_prov.c` | Change `AP_SSID`. |
| `portal.html` | `test-firmware/main/portal.html` | Change `<title>` and `<h1>` |
| `ota_update.c/.h` | `test-firmware/main/ota_update.c` | Change `OTA_DEFAULT_URL` |
| `ble_nus.c/.h` | `test-firmware/main/ble_nus.c` | Change BLE device name |
| `http_server.c/.h` | `test-firmware/main/http_server.c` | Add project-specific endpoints |
| `nvs_store.c/.h` | `test-firmware/main/nvs_store.c` | Change `NVS_NAMESPACE` |
| `dns_server/` | `test-firmware/components/dns_server/` | None (copy entire dir) |
| `partitions.csv` | `test-firmware/partitions.csv` | None (dual OTA layout) |
| `sdkconfig.defaults` | `test-firmware/sdkconfig.defaults` | Reference for required options |
| `app_main.c` | `test-firmware/main/app_main.c` | Reference for init order only |

## Workbench Compatibility Contract

The workbench is not a passive observer — it actively drives the device through
BLE commands, HTTP relay, captive portal automation, and serial/UDP log parsing.
For this to work, the firmware **must** conform to two contracts:

### Contract 1: Required Log Messages

The workbench skills detect device state by grepping serial and UDP log output
for specific format strings. These are **not optional debug messages** — they are
**required infrastructure**. If a log message is missing or uses a different
format string, the corresponding workbench skill will fail to detect the event.

The firmware must emit these exact strings at the specified locations:

| Pattern | Workbench skill that needs it | Where | Why the workbench needs it |
|---------|-------------------------------|-------|---------------------------|
| `"Init complete"` | serial monitor | End of app_main() | Confirms boot finished; workbench waits for this before proceeding |
| `"alive %lu"` | serial monitor | Heartbeat task | Proves device is running, not hung |
| `"OTA succeeded"` / `"OTA failed"` | OTA skill | OTA task | Confirms OTA result; workbench blocks until one appears |
| `"OTA update requested"` | BLE skill | cmd_handler | Confirms BLE OTA command was received |
| `"WiFi reset requested"` | BLE skill | cmd_handler | Confirms BLE WiFi reset command was received |
| `"WiFi credentials erased"` | WiFi skill | wifi_prov_reset() | Confirms NVS wipe before reboot into AP mode |
| `"INSERT: %.*s"`, `"ENTER"`, `"BACKSPACE x%d"` | UDP log skill | cmd_handler | Verifies BLE text commands are being processed |
| `"UDP logging -> %s:%d"` | logging skill | udp_log_init() | Confirms UDP log channel is active |
| `"No WiFi credentials"` | WiFi skill | wifi_prov_init() | Confirms device will enter AP mode (no stored creds) |
| `"AP mode: SSID='%s'"` | WiFi skill | WiFi AP start | Workbench detects AP name to drive captive portal |
| `"Portal page requested"` | WiFi skill | portal_get_handler() | Confirms workbench HTTP request reached the portal |
| `"Credentials saved"` | WiFi skill | connect_post_handler() | Confirms portal form submission succeeded |
| `"STA mode, connecting to '%s'"` | WiFi skill | start_sta() | Confirms device is attempting WiFi connection |
| `"STA got IP"` | WiFi skill | wifi_event_handler() | Confirms device joined the network; workbench proceeds |
| `"STA disconnect, retry"` | WiFi skill | wifi_event_handler() | Diagnoses WiFi connection failures |
| `"BLE NUS initialized"` | BLE skill | BLE init | Confirms BLE is ready; workbench can start scanning |

Step 5 of the procedure ensures every required pattern exists in the firmware.

### Contract 2: Required Process Flows

The workbench automates device operations by driving specific sequences. The
firmware **must implement these flows exactly as described** — alternative
implementations (e.g., BLE-based provisioning instead of captive portal,
SmartConfig instead of SoftAP) are not compatible with the workbench.

#### WiFi Provisioning Flow (Captive Portal)

The workbench drives this exact sequence:

```
1. Device boots with no WiFi credentials
   → firmware logs "No WiFi credentials"
   → firmware starts SoftAP with configured SSID
   → firmware logs "AP mode: SSID='<SSID>'"

2. Workbench connects to device's SoftAP (via enter-portal)
   → workbench sends HTTP GET to portal page
   → firmware logs "Portal page requested"
   → workbench submits credentials via POST
   → firmware logs "Credentials saved"

3. Device switches to STA mode
   → firmware logs "STA mode, connecting to '<SSID>'"
   → on success: firmware logs "STA got IP"
   → on failure: firmware logs "STA disconnect, retry" (with backoff)
```

The firmware must use: SoftAP → captive portal (HTTP) → NVS credential storage →
STA connect. The `wifi_prov.c` template implements this exactly.

#### WiFi Reset Flow (BLE-triggered)

```
1. Workbench sends CMD_WIFI_RESET via BLE NUS
   → firmware logs "WiFi reset requested"
   → firmware erases WiFi credentials from NVS
   → firmware logs "WiFi credentials erased"
   → firmware reboots
   → device enters AP mode (see provisioning flow above)
```

#### OTA Update Flow

```
1. Workbench uploads firmware binary to its HTTP server
2. Workbench triggers OTA via one of:
   a. BLE: sends CMD_OTA via NUS → firmware logs "OTA update requested"
   b. HTTP relay: POST to device's /ota endpoint
3. Device downloads firmware from workbench URL
   → on success: firmware logs "OTA succeeded", reboots
   → on failure: firmware logs "OTA failed", stays on current firmware
```

The firmware must expose an HTTP `/ota` endpoint that accepts
`{"url": "<firmware-url>"}` and performs esp_https_ota (or esp_http_ota).
The `ota.c` template implements this exactly.

#### BLE Command Protocol (NUS)

```
1. Workbench scans for device by BLE name
2. Workbench connects to device's NUS service
3. Workbench writes binary commands to NUS RX characteristic:
   - Each command starts with a 1-byte opcode
   - Followed by opcode-specific payload
4. Device logs each command execution via UDP/serial
```

The firmware must use NimBLE with Nordic UART Service. The `ble_nus.c` and
`cmd_handler.c` templates implement this exactly.

#### Boot Sequence

The firmware must initialize in this order:
NVS → netif/event loop → UDP log → WiFi provisioning → BLE → heartbeat →
"Init complete"

This order ensures: UDP logging is ready before WiFi events fire, WiFi is up
before BLE (which may trigger WiFi reset), and "Init complete" is the last
message (so the workbench knows init is done).

### Compatibility Validation

In **Step 2** (Parse FSD), after extracting features, the skill must check for
compatibility conflicts:

| Conflict | Detection | Resolution |
|----------|-----------|------------|
| FSD specifies BLE provisioning instead of captive portal | FR mentions "BLE provisioning" or "SmartConfig" | Flag to user: workbench requires captive portal flow |
| FSD specifies MQTT-based OTA instead of HTTP | FR mentions MQTT OTA trigger | Flag to user: workbench requires HTTP `/ota` endpoint |
| FSD specifies custom BLE protocol instead of NUS | Interface spec shows non-NUS UUIDs | Flag to user: workbench requires NUS for BLE commands |
| No WiFi mentioned | Feature checklist NEEDS_WIFI=no | UDP logging and OTA are unavailable; document serial-only workflow |

If the project's architecture conflicts with a required flow, the skill must
**ask the user** whether to adapt the project or document a limited-compatibility
mode.

## Procedure

### Step 1: Identify project

Find the project's FSD path and firmware root directory. Confirm:
- What chip is being used (ESP32, ESP32-S3, etc.)
- Where the firmware source lives (e.g. `main/` directory)
- The project name

### Step 2: Parse FSD — extract features and build checklist

Read the entire FSD (produced by the `fsd-writer` skill). Extract features from
**Section 4 (Functional Requirements)**, phases from **Section 3 (Implementation
Phases)**, interfaces from **Section 6 (Interface Specifications)**, and
architecture details from **Section 2 (System Architecture)**.

Build a feature checklist:

```
NEEDS_WIFI        → if project uses WiFi
NEEDS_BLE         → if project uses BLE
NEEDS_BLE_NUS     → if project uses Nordic UART Service
NEEDS_OTA         → if project supports firmware updates
NEEDS_MQTT        → if project uses MQTT
NEEDS_UDP_LOG     → always yes when NEEDS_WIFI=yes
NEEDS_CMD_HANDLER → if NEEDS_BLE_NUS=yes
OTA_TRIGGER       → ble / http / both
```

Record project-specific values:
- WiFi AP SSID for captive portal (e.g. `"KB-Setup"`)
- BLE device name (e.g. `"iOS-KB"`)
- OTA URL (e.g. `"http://192.168.0.87:8080/firmware/ios-keyboard/ios-keyboard.bin"`)
- NVS namespace
- Any project-specific command opcodes

### Step 3: Audit firmware code

Inventory the project's source files. For each module in the template reference table, check:
- Does the file exist?
- Does it contain the required log patterns?
- Does it match the template's API signatures?

Also check:
- `CMakeLists.txt` — are all sources listed in SRCS? Are all PRIV_REQUIRES present?
- `sdkconfig.defaults` — are required options set?
- `partitions.csv` — does it have OTA slots (if NEEDS_OTA)?
- `app_main.c` — what's the init order? Is "Init complete" the last log?
- `components/dns_server/` — does it exist (if NEEDS_WIFI)?

### Step 4: Add missing modules (Enforce Contract 2)

Follow this decision tree. For each missing module, copy from
`workbench-test/main/` and customize. These templates implement the exact process
flows required by the **Workbench Compatibility Contract** (Contract 2) — WiFi
captive portal, BLE NUS command protocol, OTA via HTTP endpoint, and the
canonical boot sequence:

```
Does the project use WiFi? --NO--> Skip WiFi, UDP, OTA
  |YES
  v
Has udp_log.c? --YES--> Check log message exists
  |NO --> Copy from workbench-test
  v
Has wifi_prov.c? --YES--> Check AP_SSID, check wifi_prov_reset()
  |NO --> Copy from workbench-test, customize AP_SSID
  v
Needs OTA? --NO--> Skip
  |YES
  v
Has ota.c? --YES--> Check OTA_DEFAULT_URL, check log messages
  |NO --> Copy from workbench-test, customize URL
         Ensure partitions.csv has OTA slots
  v
Uses BLE? --NO--> Skip BLE modules
  |YES
  v
Has ble_nus.c? --YES--> Check device name
  |NO --> Copy from workbench-test, customize name
  v
Has cmd_handler.c? --YES--> Check CMD_OTA + CMD_WIFI_RESET exist
  |NO --> Copy from workbench-test, add project-specific opcodes
  v
Has heartbeat task? --YES--> Check "alive" pattern
  |NO --> Add to app_main.c
  v
Has "Init complete"? --YES--> Done
  |NO --> Add to end of app_main()
```

When copying files:
- Read the template source from workbench-test
- Customize project-specific values (AP_SSID, BLE name, OTA URL, NVS namespace)
- Add or remove project-specific opcodes in cmd_handler
- Write the customized file to the project

### Step 5: Enforce Contract 1 — Required Log Messages

Check every required log pattern from the **Workbench Compatibility Contract**
(Contract 1) table. For each missing pattern:
- Add the exact log statement at the correct location
- Use the exact format string — the workbench skills grep for these patterns
- Do not paraphrase, reformat, or localize the strings
- These are infrastructure, not debug aids — they must survive any "clean up
  logging" refactors

### Step 6: Update build config

Update the project's build configuration:

**CMakeLists.txt** — add new source files to SRCS, add any missing PRIV_REQUIRES:
- `nvs_flash`, `esp_wifi`, `esp_netif`, `esp_event` (WiFi)
- `esp_http_server`, `esp_http_client`, `esp_https_ota` (OTA)
- `bt` (BLE)
- `dns_server`, `lwip` (captive portal)
- `esp_app_format`, `app_update` (OTA + status endpoint)
- `json` (OTA HTTP endpoint)
- Add `EMBED_FILES "portal.html"` if wifi_prov uses captive portal

**partitions.csv** — copy from `test-firmware/` (`partitions-4mb.csv` for 4MB flash, `partitions.csv` for 8MB+). See `idf-flash` skill for flash size and partition table rules.

**sdkconfig.defaults** — verify required options are set (NimBLE, partition table, flash size, etc.). See `idf-flash` skill for flash size defaults.

**dns_server component** — copy `workbench-test/components/dns_server/` if project needs captive portal but doesn't have it

### Step 7: Update app_main.c

Ensure the canonical init order:
1. NVS init (with erase-on-corrupt fallback)
2. Boot count increment
3. `esp_netif_init()` + `esp_event_loop_create_default()`
4. `udp_log_init("192.168.0.87", 5555)`
5. Register IP event handler for HTTP server
6. `wifi_prov_init()`
7. `ble_nus_init(cmd_handler_on_rx)`
8. Heartbeat task (`alive_task`)
9. `ESP_LOGI(TAG, "Init complete, running event-driven")`

The exact implementation can vary, but the order must be: NVS → netif → UDP → WiFi → BLE → cmd handler → heartbeat → "Init complete".

### Step 8: Write "7. Operational Procedures" (Workbench Operations)

Replace `## 7. Operational Procedures` in the FSD with workbench-specific
operational content. This section becomes a standalone **operations guide** — how
to interact with the device through the workbench. It contains no test cases.

If the fsd-writer left a generic Section 7, replace it entirely. The workbench
operations are the operational procedures for this project.

#### 8a. Hardware setup

Query the workbench for hardware details:
```bash
curl -s http://192.168.0.87:8080/api/devices | jq .
curl -s http://192.168.0.87:8080/api/info | jq .
```

Record: slot label, TCP port, RFC2217 URL, device state.

**Check for dual-USB hub boards:** If the board occupies two slots (onboard USB hub exposing both JTAG and UART), identify which slot is which:
- Espressif USB-Serial/JTAG (`303a:1001`) → **JTAG slot** (flash here)
- CH340/CP2102 UART bridge (`1a86:55d3` / `10c4:ea60`) → **UART slot** (console output here)

Write a hardware table and a project-specific values table:

```markdown
### Hardware Setup

| What | Where |
|------|-------|
| ESP32 USB | Workbench slot <N>, serial at `rfc2217://192.168.0.87:<PORT>` |
| Workbench host | `192.168.0.87:8080` |
| UDP log sink | `192.168.0.87:5555` |
| OTA firmware URL | `http://192.168.0.87:8080/firmware/<project>/<project>.bin` |

#### Project-Specific Values

| Value | Setting |
|-------|---------|
| WiFi portal SSID | `<SSID>` (device SoftAP name when no credentials stored) |
| Workbench AP SSID | `WB-TestAP` |
| Workbench AP password | `wbtestpass` |
| BLE device name | `<NAME>` |
| NVS namespace | `<NS>` |
| NUS RX characteristic | `6e400002-b5a3-f393-e0a9-e50e24dcca9e` |
```

**Important:** Fill in all actual values from the firmware source — never leave `<placeholder>` in the final FSD.

#### 8b. Flashing

Document the project-specific esptool command for serial flashing via RFC2217. Reference the `esp32-workbench-serial-flashing` skill for download mode, crash-loop recovery, and dual-USB hub details.

#### 8c. WiFi provisioning

WiFi provisioning is a prerequisite for most operations (OTA, UDP logs, HTTP endpoints). Document it as a complete two-phase procedure with filled-in project values.

**Three values are involved — document all three clearly:**

| Value | What it is | Where it's defined |
|-------|-----------|-------------------|
| Device portal SSID | The SoftAP name the device broadcasts when it has no WiFi credentials | `wifi_prov.c` → `AP_SSID` |
| Workbench AP SSID | The WiFi network the workbench creates for the device to join | Passed in `enter-portal` request |
| Workbench AP password | Password for the workbench's AP | Passed in `enter-portal` request |

**Always document both phases:**
1. **Ensure device is in AP mode** — BLE WiFi reset if previously provisioned, skip if freshly flashed
2. **Provision via captive portal** — `enter-portal` with all three values filled in, serial monitor for confirmation

Include the enter-portal failure diagnostic steps (check AP mode, check WiFi scan, check activity log).

#### 8d. BLE commands

Document how to scan, connect, and send each opcode. Write a command reference table:

```markdown
| Opcode | Hex example | Description | Expected log |
|--------|-------------|-------------|--------------|
| `0x01 <count>` | `0103` | Backspace | `"BACKSPACE x3"` |
| ... | ... | ... | ... |
```

Include one example `curl` write command. This is reference material — test cases go in the Testing chapter.

#### 8e. OTA updates

Document the complete OTA workflow:
1. Upload firmware to the workbench (`/api/firmware/upload`)
2. Trigger OTA via BLE (`CMD_OTA` opcode) or via HTTP (`POST /ota` through relay)
3. Monitor result via serial

#### 8f. HTTP endpoints

Document the device's HTTP endpoints and how to reach them via the workbench HTTP relay (`/api/wifi/http`). Typical endpoints: `/status`, `/ota`.

#### 8g. Log monitoring

Document the two log methods (serial monitor and UDP logs) with example commands. This is the "how" — when to use which method goes in the Appendix.

### Step 9: Write "8. Verification & Validation" (Testing)

Replace `## 8. Verification & Validation` in the FSD with workbench test cases.
This section contains **only test cases** — verification tables with pass/fail
criteria. It does not repeat operational procedures from Section 7.

If the fsd-writer left a generic Section 8 with a traceability matrix, preserve
the traceability matrix (Section 8.4) and replace the phase verification tables
(Sections 8.1, 8.2, 8.3) with workbench-specific test procedures.

#### 9a. Phase verification tables

For each implementation phase, write a table:

```markdown
### Phase N Verification

| Step | Feature | Test procedure | Success criteria |
|------|---------|---------------|-----------------|
| 1 | <feature> | <brief description, reference workbench chapter> | <expected output> |
```

**Rules:**
- Every FSD feature must appear in exactly one phase verification table
- Test procedures **reference** operations from Section 7 (Operational Procedures) (e.g., "Provision WiFi (see WiFi Provisioning)") — they don't duplicate curl commands
- Every step must have concrete, observable success criteria — no vague "verify it works"
- Include the hex data for BLE commands inline (e.g., "BLE write `024869`") since that's test-specific

### Step 10: Write "9. Troubleshooting Guide" and "10. Appendix"

Replace `## 9. Troubleshooting Guide` and `## 10. Appendix` in the FSD with
workbench-specific diagnostics and reference material.

#### 10a. Logging strategy

Document when to use each log method:

```markdown
### Logging Strategy

| Situation | Method | Why |
|-----------|--------|-----|
| Verify boot output | Serial monitor | Captures UART before WiFi is up |
| Monitor BLE commands | UDP logs | Non-blocking, works while device runs |
| Capture crash output | Serial monitor | Only UART captures panic handler output |
```

#### 10b. Troubleshooting

Add a failure-to-diagnostic-to-fix mapping table covering likely failure modes:

```markdown
### Troubleshooting

| Test failure | Diagnostic | Fix |
|-------------|-----------|-----|
| Serial monitor shows no output | Check `/api/devices` | Device absent or flapping |
| enter-portal times out | Check serial for AP mode | BLE `CMD_WIFI_RESET` first |
| ... | ... | ... |
```

### Step 11: Build verification

```bash
cd <project-root> && idf.py build
```

Fix any compilation errors. Common issues:
- Missing PRIV_REQUIRES in CMakeLists.txt
- Missing `#include` directives
- Function signature mismatches between header and implementation

### Step 12: Summary report

List what was added/changed:
- New files copied from workbench-test (with customizations noted)
- Modified files (what changed)
- Build result
- Any issues found and fixed

## Completeness Checklist

After completing all steps, verify:

**Firmware integration (Steps 1–7):**
- [ ] Every module needed by the feature checklist exists
- [ ] Every required log pattern is present
- [ ] CMakeLists.txt has all sources and dependencies
- [ ] app_main.c follows the canonical init order
- [ ] "Init complete" is the last log message in app_main()

**Section 7 — Operational Procedures (Step 8):**
- [ ] Hardware table documents all slots (including dual-USB if applicable)
- [ ] All project-specific values are filled in (no `<placeholder>` the AI must guess)
- [ ] WiFi provisioning includes all three values: `portal_ssid`, `ssid`, `password`
- [ ] WiFi provisioning documents both phases (ensure AP mode + provision via portal)
- [ ] BLE command reference table covers every opcode
- [ ] OTA workflow covers upload + both trigger methods (BLE and HTTP)
- [ ] HTTP endpoints documented with relay examples
- [ ] Section 7 works as a standalone operations guide

**Section 8 — Verification & Validation (Step 9):**
- [ ] Every FSD feature appears in a phase verification table
- [ ] Every implementation phase has a verification table
- [ ] Test procedures reference (not duplicate) Section 7
- [ ] Every test step has concrete success criteria

**Sections 9 & 10 — Troubleshooting & Appendix (Step 10):**
- [ ] Logging strategy explains when to use serial monitor vs UDP logs
- [ ] Troubleshooting covers likely failure modes

**Build (Step 11):**
- [ ] Project builds cleanly with `idf.py build`

## Workbench Skills Reference

| Skill | Key endpoints | What it enables |
|-------|-------------|-----------------|
| `esp32-tester-serial` | `GET /api/devices`, `POST /api/serial/reset` | Device discovery, remote flashing (esptool via RFC2217), GPIO download mode, crash-loop recovery |
| `esp32-tester-udplog` | `POST /api/serial/monitor`, `GET /api/udplog` | Serial monitor with pattern matching, UDP log collection, boot/crash capture |
| `esp32-tester-wifi` | `POST /api/enter-portal`, `GET /api/wifi/ap_status`, `GET /api/wifi/scan`, `POST /api/wifi/http`, `GET /api/wifi/events` | Captive portal provisioning, AP control, WiFi on/off testing, HTTP relay, event monitoring |
| `esp32-tester-gpio` | `POST /api/gpio/set`, `GET /api/gpio/status` | Boot mode control, hardware reset, button simulation, GPIO probe |
| `esp32-tester-ota` | `POST /api/firmware/upload`, `GET /api/firmware/list`, `POST /api/wifi/http` | Firmware upload/serve, OTA trigger via HTTP relay |
| `esp32-tester-ble` | `POST /api/ble/scan`, `POST /api/ble/connect`, `POST /api/ble/write`, `POST /api/ble/disconnect` | BLE scan, connect, GATT write, remote BLE testing |
