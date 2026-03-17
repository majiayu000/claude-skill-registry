---
name: watch-connectivity
description: WatchConnectivity patterns + dual-target sync flows; also complications/widgets pointers.
allowed-tools: Read, Grep, Glob, Edit, Write
---

Load:
- @docs/watch/README.md
- @docs/watch/watchconnectivity.md
- @docs/watch/background-execution.md

Output:
- Message schema (keys, payload types, versioning)
- iOS WCSession manager + watch WCSession manager skeletons
- Failure handling strategy (not reachable, delays)
- Minimal tests for encoding/decoding
