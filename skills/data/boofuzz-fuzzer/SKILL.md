---
name: boofuzz
description: Protocol fuzzer script development using boofuzz framework. Use when creating network protocol fuzzers, defining protocol PDUs (Protocol Data Units), writing mutation-based fuzzing scripts, or contributing to the boofuzz project. Covers binary protocol definitions, session management, crash detection, and reporting findings.
---

# boofuzz Protocol Fuzzer Development

## Protocol Definition Hierarchy

```
Session → Request (message) → Block (chunk) → Primitive (element)
```

Prefer the object-oriented style over static functions for new code:

```python
from boofuzz import Request, Block, String, Byte, Static, Group, Size

req = Request("Protocol-Message", children=(
    Block("Header", children=(
        Byte("opcode", default_value=0x01),
        Size("length", block_name="Payload", length=2),
    )),
    Block("Payload", children=(
        String("data", default_value="test"),
    )),
))
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Request | Protocol-Action format | `"iSCSI-Login-Request"`, `"MQTT-CONNECT"` |
| Block | Protocol terminology | `"BHS"`, `"Data-Segment"`, `"Fixed-Header"` |
| Primitive | Spec field names | `"opcode"`, `"data_segment_length"`, `"client_id"` |

Always provide `name=` parameter for debugging and logging.

## Essential Primitives

```python
# Fixed values (not fuzzed)
Static("magic", default_value=b"\x00\x01")

# Fuzzable bytes/strings
Byte("flags", default_value=0x00)
Bytes("payload", default_value=b"\x00" * 16, size=16)
String("username", default_value="admin")

# Length fields (auto-calculated)
Size("length", block_name="body", length=4, endian=BIG_ENDIAN)

# Opcodes/enums
Group("command", values=[b"\x01", b"\x02", b"\x03"])

# Checksums
Checksum("crc", block_name="data", algorithm="crc32")
```

## Binary Protocol Pattern

For protocols with fixed headers (iSCSI, MQTT, etc.):

```python
from boofuzz import (
    Request, Block, Byte, Bytes, Size, Static, Group,
    BIG_ENDIAN, LITTLE_ENDIAN
)

def define_pdu():
    return Request("Protocol-PDU", children=(
        Block("fixed_header", children=(
            Byte("type", default_value=0x10),
            # Variable length encoding if needed
        )),
        Block("variable_header", children=(
            Size("length", block_name="payload", length=2, endian=BIG_ENDIAN),
            Bytes("session_id", default_value=b"\x00" * 4, size=4),
        )),
        Block("payload", children=(
            String("data", default_value=""),
        )),
    ))
```

## Session Setup

```python
from boofuzz import Session, Target, TCPSocketConnection

session = Session(
    target=Target(
        connection=TCPSocketConnection(host="192.168.1.100", port=3260)
    ),
    web_port=26000,           # Web UI
    keep_web_open=True,
    crash_threshold_element=3, # Failures before restart
)

# Register requests
session.connect(s_get("login"))
session.connect(s_get("login"), s_get("command"))  # login → command

# Run
session.fuzz()
```

## Callbacks for Stateful Protocols

```python
def pre_send_callback(target, fuzz_data_logger, session, sock):
    """Execute before each test case - establish session state."""
    # Send valid login, store session token, etc.
    pass

def post_test_case_callback(target, fuzz_data_logger, session, sock):
    """Execute after each test case - check for anomalies."""
    pass

session = Session(
    target=target,
    pre_send_callbacks=[pre_send_callback],
    post_test_case_callbacks=[post_test_case_callback],
)
```

## Code Style (for contributions)

Format with Black before committing:

```bash
pip install black
black your_fuzzer.py
```

Run full checks:

```bash
pip install tox
tox
```

Use `# fmt: off` / `# fmt: on` sparingly for protocol byte layouts.

## File Organisation

| Directory | Purpose |
|-----------|---------|
| `/examples/` | Complete runnable scripts with CLI |
| `/request_definitions/` | Reusable protocol modules (no `main()`) |

For standalone fuzzers, target `/examples/`.

## Script Structure

```python
#!/usr/bin/env python3
"""
Protocol Name Fuzzer

Brief description of target and approach.
Protocol reference: [RFC/spec URL]
"""

from boofuzz import (...)
import argparse

# Constants from spec
PROTO_PORT = 1234
OPCODE_FOO = 0x01

def define_message_type():
    """Define Protocol Message PDU per RFC section X.Y."""
    # ...

def main():
    parser = argparse.ArgumentParser(description="Protocol Fuzzer")
    parser.add_argument("-t", "--target", required=True, help="Target host")
    parser.add_argument("-p", "--port", type=int, default=PROTO_PORT)
    args = parser.parse_args()
    
    session = Session(...)
    # Register messages
    session.fuzz()

if __name__ == "__main__":
    main()
```

## Monitoring Targets

Build targets with AddressSanitizer for memory bug detection:

```bash
# Example for C projects
export CFLAGS="-fsanitize=address -g"
export LDFLAGS="-fsanitize=address"
./configure && make
```

Monitor during fuzzing:

```bash
# ASAN output
grep -E "AddressSanitizer|ERROR|SUMMARY" target.log

# Process crashes
dmesg -w | grep -i segfault
```

## Results Analysis

Results stored in `./boofuzz-results/*.db` (SQLite):

```bash
# Web UI
boo open boofuzz-results/run-YYYY-MM-DD_HH-MM-SS.db
```

Query crashes:

```python
import sqlite3
conn = sqlite3.connect('boofuzz-results/run-*.db')
cursor = conn.cursor()
cursor.execute("""
    SELECT name, type, timestamp FROM cases 
    WHERE type LIKE '%fail%' OR type LIKE '%crash%'
""")
```

## Reporting Findings

See `references/disclosure.md` for vulnerability disclosure templates and responsible reporting guidelines.

## Quick Reference

Common pitfalls:
- Missing `name=` on primitives makes debugging difficult
- Forgetting `endian=BIG_ENDIAN` for network protocols
- Not handling stateful protocols (login before commands)
- Size fields referencing non-existent block names
