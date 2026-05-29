---
name: kamailio-config
description: |
  Kamailio SIP server configuration and troubleshooting. Use when Claude needs to:
  (1) Edit or create Kamailio configuration files (.cfg)
  (2) Debug SIP routing logic (request_route, failure_route, reply_route)
  (3) Work with Kamailio pseudo-variables ($ru, $fU, $avp, $xavp, $dlg_var)
  (4) Configure modules (tm, dialog, acc, sqlops, jansson, http_client, rr, sl, mqueue, rtimer)
  (5) Understand SIP message flow and transaction handling
  (6) Validate configuration syntax
  Triggers: "kamailio", "SIP routing", "kamailio.cfg", SIP-related pseudo-variables
---

# Kamailio Configuration

## Quick Reference

### Configuration Syntax
```kamailio
#!KAMAILIO                      # Config marker
#!define FLAG_NAME 1            # Preprocessor define

loadmodule "module.so"          # Load module
modparam("module", "param", value)  # Set parameter

request_route { }               # Main routing block
route[NAME] { }                 # Named subroute
failure_route[NAME] { }         # Failure handler
onreply_route[NAME] { }         # Reply handler
branch_route[NAME] { }          # Branch handler
```

### Common Pseudo-Variables
| Variable | Description | R/W |
|----------|-------------|-----|
| `$ru` | Request URI | R/W |
| `$rU` | Request URI username | R/W |
| `$du` | Destination URI | R/W |
| `$fU` | From username | R/W |
| `$si` | Source IP | R |
| `$ci` | Call-ID | R |
| `$rs` | Reply status code | R |
| `$var(x)` | Script variable | R/W |
| `$avp(x)` | AVP (stack, transaction) | R/W |
| `$xavp(r=>f)` | Extended AVP | R/W |
| `$dlg_var(x)` | Dialog variable | R/W |
| `$hdr(X)` | Header value | R |
| `$Ts` | Unix timestamp (cached) | R |
| `$TS` | Unix timestamp (non-cached, real-time) | R |
| `$TV(u)` | Current time microseconds (0-999999) | R |

### Transformations
```kamailio
$(var{s.len})              # String length
$(var{s.int})              # To integer
$(var{s.tolower})          # Lowercase
$(var{s.substr,0,5})       # Substring
$(var{s.select,1,:})       # Split and select
$(var{s.escape.param})     # URL encode
$(uri{uri.user})           # URI username
$(uri{uri.host})           # URI domain
```

### Syntax Validation (Quick Check)

```bash
# Default (validates kamailio/kamailio.cfg)
.claude/skills/kamailio-config/scripts/check-kamailio.sh

# Custom config path
.claude/skills/kamailio-config/scripts/check-kamailio.sh path/to/config.cfg
```

Exit code 0 = valid (PASS), non-zero = syntax error (FAIL).

The script auto-builds Docker image, substitutes env placeholders, and uses `--platform linux/amd64` for Apple Silicon.

### Common Gotchas

#### String concatenation requires `+` operator
You cannot directly concatenate pseudo-variables or literals without `+`. The `.` character is NOT a concatenation operator:
```kamailio
# WRONG - syntax error at column 63
$var(ts) = $(Ts{s.ftime,%Y-%m-%d %H:%M:%S}).$TV(u);

# CORRECT - use + for concatenation
$var(ts) = $(TS{s.ftime,%Y-%m-%d %H:%M:%S}) + "." + $TV(u);
```

#### $Ts vs $TS - cached vs real-time timestamp
`$Ts` is cached at transaction start and doesn't change. Use `$TS` for real-time timestamps:
```kamailio
# WRONG - $Ts cached at transaction start, same value throughout
$var(event_time) = $(Ts{s.ftime,%Y-%m-%d %H:%M:%S}) + "." + $TV(u);

# CORRECT - $TS is non-cached, gives real-time value
$var(event_time) = $(TS{s.ftime,%Y-%m-%d %H:%M:%S}) + "." + $TV(u);
```
Note: strftime doesn't support microseconds, so append `$TV(u)` separately.

#### No `continue` or `break` statements
Kamailio scripting does NOT support `continue` or `break`. Use a validity flag pattern instead:
```kamailio
# WRONG - will cause syntax error
while(condition) {
    if(error) { continue; }  # NOT SUPPORTED
}

# CORRECT - use validity flag
while(condition) {
    $var(valid) = 1;
    if(error) { $var(valid) = 0; }
    if($var(valid) == 1) {
        # process valid items
    }
}
```

#### sql_query vs sql_pvquery
- `sql_query(con, query, res)` - query must be a **constant string**, no PV evaluation
- `sql_pvquery(con, query, res)` - query can contain pseudo-variables that get evaluated

```kamailio
# WRONG - sql_query with dynamic string concatenation
sql_query("rw", "INSERT INTO t VALUES ('" + $var(x) + "')", "res");  # ERROR

# CORRECT - sql_pvquery with embedded PVs
sql_pvquery("rw", "INSERT INTO t VALUES ('$(var(x){s.escape.common})')", "$avp(res)");
```

#### sql_pvquery result parameter
The result parameter must be a pseudo-variable, not a plain string:
```kamailio
# WRONG
sql_pvquery("rw", "INSERT ...", "ra");  # ERROR: invalid result parameter

# CORRECT
sql_pvquery("rw", "INSERT ...", "$avp(res)");
```

#### Docker base image entrypoint
The `ghcr.io/kamailio/kamailio:6.0.1-noble` image has a hardcoded ENTRYPOINT that ignores CMD. Override in Dockerfile:
```dockerfile
# Clear base image entrypoint to use our startup script
ENTRYPOINT []
CMD ["/usr/local/bin/start-kamailio.sh"]
```

#### Variable comparison type conversion errors
Comparing variables with `== $null` or `== ""` can trigger type conversion errors:
```
automatic string to int conversion for "null" failed
```

**Use `defined` keyword and regex matching instead:**
```kamailio
# WRONG - may cause type conversion error
if($dlg_var(trunk_id) != $null && $dlg_var(trunk_id) != "") {
    # use trunk_id
}

# CORRECT - use defined and regex for null-safe comparison
if(defined $dlg_var(trunk_id) && $dlg_var(trunk_id) =~ "^[0-9]+$") {
    # use trunk_id - validated as numeric
}

# For string "null" from JSON parsing
if($var(value) =~ "^null$") {
    $var(value) = "";  # convert to empty
}
```

#### $avp vs $dlg_var scope
- **`$avp(x)`** - Transaction-scoped, cleared after transaction ends. Empty for BYE/re-INVITE.
- **`$dlg_var(x)`** - Dialog-scoped, persists for entire call duration. Use for call-level data.

```kamailio
# In LCR routing - store trunk_id in both
$avp(trunk_id) = $var(selected_trunk);
$dlg_var(trunk_id) = $avp(trunk_id);  # Persist for entire dialog

# In onreply_route/failure_route - use $dlg_var
# $avp(trunk_id) may be empty here for BYE messages
$var(trunk_id_json) = $dlg_var(trunk_id);  # CORRECT
```

#### CANCEL doesn't trigger branch_route
CANCEL requests are handled specially by the transaction module. Adding CANCEL to `t_on_branch()` method list won't work - `t_relay()` for CANCEL just forwards to cancel the existing INVITE transaction without creating new branches.

To capture CANCEL requests, handle them directly in `request_route`:
```kamailio
# In request_route
if (is_method("CANCEL")) {
    if (t_check_trans()) {
        # Capture CANCEL event HERE - before route(RELAY)
        xlog("L_NOTICE", "CANCEL request for callid=$ci\n");
        route(RELAY);
    }
    exit;
}
```

#### jansson_get returns "null" string for JSON null
When parsing JSON with `jansson_get`, a JSON `null` value becomes the string `"null"`:
```kamailio
# JSON: {"trunk_id":null}
jansson_get("trunk_id", $var(json), "$var(trunk_id)");
# $var(trunk_id) now contains string "null", not $null

# Check with regex, not equality
if($var(trunk_id) =~ "^null$") {
    $var(trunk_id) = "";
}
```

#### mqueue uses key for deduplication
The mqueue module's `mq_add(queue, key, value)` uses the key for deduplication - adding items with the same key **overwrites** previous entries instead of adding to the queue:
```kamailio
# WRONG - same callid as key, later events overwrite earlier ones
mq_add("cdr_events", $ci, $var(json1));  # INVITE request
mq_add("cdr_events", $ci, $var(json2));  # 180 response - OVERWRITES!
mq_add("cdr_events", $ci, $var(json3));  # 200 response - OVERWRITES!
# Only json3 remains in queue

# CORRECT - use unique key per event (callid + zero-padded microseconds)
$var(usec_padded) = $(TV(u){s.int}) + 1000000;
mq_add("cdr_events", $ci + "-" + $(var(usec_padded){s.substr,1,6}), $var(json));
```

#### $TV(u) microseconds not zero-padded
`$TV(u)` returns microseconds 0-999999 but does NOT zero-pad the value. This causes sorting issues when used in timestamps or as unique keys:
```kamailio
# WRONG - 69225 vs 100421 sorts incorrectly as strings
$var(event_time) = $(TS{s.ftime,%Y-%m-%d %H:%M:%S}) + "." + $TV(u);

# CORRECT - add 1000000 and take last 6 digits for zero-padding
$var(usec_padded) = $(TV(u){s.int}) + 1000000;
$var(event_time) = $(TS{s.ftime,%Y-%m-%d %H:%M:%S}) + "." + $(var(usec_padded){s.substr,1,6});
# Result: 069225 sorts correctly before 100421
```

## Reference Files

### Core Documentation
- **[pseudovariables.md](references/pseudovariables.md)** - Complete PV reference (all variables)
- **[transformations.md](references/transformations.md)** - All transformation types
- **[routing.md](references/routing.md)** - SIP routing flow explanation
- **[syntax-checking.md](references/syntax-checking.md)** - Config validation with Docker
- **[modules-list.md](references/modules-list.md)** - All available Kamailio modules with links

### Module Documentation (Detailed)
- **[tm.md](references/modules/tm.md)** - Transaction Management
- **[dialog.md](references/modules/dialog.md)** - Dialog tracking
- **[acc.md](references/modules/acc.md)** - Accounting/CDR
- **[sqlops.md](references/modules/sqlops.md)** - SQL operations
- **[jansson.md](references/modules/jansson.md)** - JSON parsing
- **[http_client.md](references/modules/http_client.md)** - HTTP requests
- **[rr.md](references/modules/rr.md)** - Record-Route
- **[sl.md](references/modules/sl.md)** - Stateless replies

## External Resources
- [Module Docs (6.0.x)](https://kamailio.org/docs/modules/6.0.x/)
- [Wiki Cookbooks](https://www.kamailio.org/wikidocs/cookbooks/6.0.x/)
- [GitHub Source](https://github.com/kamailio/kamailio)
- [Docker Image](https://ghcr.io/kamailio/kamailio) - Project uses `6.0.1-noble`
