---
name: changelog-root
description: Update the repository root ChangeLog and keep the root release version metadata in sync. Use when updating the root version or syncing subsystem/package version lists in ChangeLog; touches ChangeLog at repo root and the release version in rebar.config. If you are not sure which changelog-* skill to read, read this first.
---

# Changelog Root

## Overview

Update the root ChangeLog entry and keep the root release version and version lists consistent.

## Versioning

1. Identify the change type (patch, minor, major). Ask if unclear.
2. Read the top entry in `ChangeLog` and note whether it is `UNRELEASED`.
3. Find the latest released version from the first dated entry.
4. Compute the target version from the latest released version and the change type:
   - Patch: fixes, docs, or internal changes without new features.
   - Minor: new features or notable behavior changes.
   - Major: breaking changes.
5. Apply one of these states:
   - No `UNRELEASED` entry: insert a new `UNRELEASED` entry at the top with the target version.
   - `UNRELEASED` exists but target version is higher: update the `* VERSION:` line to the target version.
   - `UNRELEASED` exists and target version is the same or lower: keep the `* VERSION:` line unchanged.
6. Never downgrade an existing `UNRELEASED` version.
7. Update `rebar.config` at `{release, {qrpc, "X.Y.Z"}, ...}` to match the `UNRELEASED` version.
8. Do not replace `UNRELEASED` with a date; only do that at release time.

## Scope and Forbidden Reads

Only edit the repository root `ChangeLog`. Do not open or modify any other ChangeLog files in the repo. It is forbidden to read `apps/*/ChangeLog` or `config/pkgsrc/files/*/*/ChangeLog` for this task unless you edited them or asked to do so.

## Subsystem Versioning

Refresh `* SUBSYSTEM VERSIONS:` from `apps/*/src/*.app.src` (`vsn` values) if you edited them or asked to do so. Keep the existing order and formatting. Do not read new ChangeLog files just for this. If you are not sure what to do, skip this section.

## Package Versioning

Refresh `* PACKAGE VERSIONS:` from `config/pkgsrc/files/meta-pkgs/*/Makefile` (`DISTNAME` versions) if you edited those meta-pkg files or were asked to do so. Keep the existing order and formatting. Do not add versions for non-meta packages; their ChangeLogs (example: `config/pkgsrc/files/audio/voicevox_core/ChangeLog`) do not affect the root ChangeLog. Do not read new ChangeLog files just for this. If you are not sure what to do, skip this section.

## Change Description

Append the new change line(s) under the version lists in the `UNRELEASED` entry.

## Formatting Rules

Use the existing ChangeLog formatting:
- Use a header line like `UNRELEASED  ts-klassen  <qrpc@su-shiki.com>` or `YYYY-MM-DD  ts-klassen  <qrpc@su-shiki.com>`.
- Keep a blank line after the header.
- Use tabs for indentation and `*` bullets, matching the file.
- Use 2 new lines in between entries.

## Example Requests

- "Update ChangeLog"
- "Update ChangeLog as minor update"
- "Update the root ChangeLog and rebar.config release version to 0.2.0."

## Example scenario

### No UNRELEASED

current file:

```
2025-12-25  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.1.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Initial setup.
```

updated file:

```
UNRELEASED  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.2.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Added some feature.


2025-12-25  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.1.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Initial setup.
```

### UNRELEASED 0.1.1 to 0.2.0

current file:

```
UNRELEASED  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.1.1
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Fixed some bug.


2025-12-25  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.1.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Initial setup.
```

updated file:

```
UNRELEASED  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.2.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Fixed some bug.
	Added some feature.


2025-12-25  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.1.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Initial setup.
```

### append to UNRELEASED

current file:

```
UNRELEASED  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.2.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Added some feature.


2025-12-25  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.1.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Initial setup.
```

updated file:

```
UNRELEASED  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.2.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Added some feature.
	Added more feature.


2025-12-25  ts-klassen  <qrpc@su-shiki.com>

	* VERSION: 0.1.0
	* SUBSYSTEM VERSIONS:
		* qrpc: 0.1.0
		* q_tut: 0.3.0
		* q_vvx: 0.1.0
	* PACKAGE VERSIONS:
		* qrpc-devel: 0.1.0
		* qrpc-prod: 0.1.0
	Initial setup.
```

## Related skills

- changelog-pkg
  - If you edited a file under ./config/pkgsrc, read this too if you haven't.
- changelog-app
  - If you edited a file under ./apps, read this too if you haven't.
