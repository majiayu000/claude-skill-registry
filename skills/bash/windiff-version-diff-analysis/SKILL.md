---
name: windiff-version-diff-analysis
description: >-
  Generate and analyze a diff between two Windows versions (or two patch levels of
  one version) for security research, using the WinDiff CLI in this repo. Use this
  whenever the user wants to compare Windows builds to find what Microsoft changed
  between versions — new or removed syscalls, new exported/internal kernel routines,
  added structures or struct fields, new security mitigation flags (process/thread
  mitigations, CFG/CET/XFG, Code Integrity / ci.dll, kCET, win32k lockdown), AND any
  other new security-relevant feature or component: new kernel notification/callback
  surface (Ps/Ob/Cm callbacks, ETW providers and the EtwTi threat-intel channel,
  minifilter/altitude hooks), new telemetry, ELAM/AMSI/PPL/anti-tamper changes, and
  brand-new drivers or modules. Frame findings for three audiences — anti-malware /
  EDR developers, anti-cheat developers, and vulnerability researchers. Triggers on
  requests like "diff ntoskrnl between 21H2 and 23H2", "what new syscalls were added
  in 24H2", "what changed in win32k.sys / ci.dll between these builds", "find new
  mitigation flags", "what new ETW providers or kernel callbacks appeared", "what's
  new that matters for EDR / anti-cheat", or "analyze the attack surface added in
  this Windows update". The analysis must interpret the raw diff with Windows
  internals knowledge (Nt/Zw/Ps/Ke/Mm/Ob/Se/Cm/Etw/Ci prefixes, the roles of
  ntoskrnl.exe, ntdll.dll, win32k*.sys, ci.dll, cng.sys) to explain the likely
  intent and security relevance of each change, not just list symbols.
---

# WinDiff Version Diff Analysis

Compare two Windows builds and turn the raw symbol/type/syscall delta into a
security-research report: what was added, what it probably *does*, and why it
matters for attack surface, exploitation, or defense.

This skill runs inside the **WinDiff** repo. It uses `windiff_cli` to generate
the per-binary JSON databases, then diffs and interprets them. The interpretation
is the point — anyone can list new symbols; the value is explaining intent from
Windows internals conventions.

## Workflow

### 1. Pin down scope

Establish, asking the user only if genuinely ambiguous:

- **Two OS versions** as WinDiff triples `version / update / architecture`
  (e.g. `21H2 / BASE / amd64` and `11-24H2 / KB5074105 / amd64`). `update` is
  `BASE` for an RTM image or a `KB...` number for a patch. The path suffix used
  in filenames is `version_update_architecture`, e.g. `11-24H2_KB5074105_amd64`.
- **Binaries** to compare. Default to the security-relevant core when the user is
  vague: `ntoskrnl.exe`, `ntdll.dll`, `win32k.sys`, `win32kbase.sys`,
  `win32kfull.sys`, `ci.dll`, `cng.sys`. See `references/windows-components.md`
  for what each one governs.
- **Focus**: syscalls, mitigation flags, new attack surface, a specific
  component/feature, etc. This steers interpretation, not data generation.

`ci/db_configuration.json` is the canonical list of tracked versions and binaries
— consult it for valid `version`/`update` spellings.

### 2. Generate the databases with windiff_cli

Write a **minimal** config containing only the two OS versions and the chosen
binaries, then run the CLI into a scratch output dir (keep it under the repo's
git-ignored `local/`). Use `scripts/make_config.py` to build the config:

```bash
python3 .claude/skills/windiff-version-diff-analysis/scripts/make_config.py \
  --os "21H2:BASE:amd64" --os "11-24H2:KB5074105:amd64" \
  --binary ntoskrnl.exe --binary ntdll.dll --binary win32k.sys --binary ci.dll \
  > local/windiff_diff_config.json

cd windiff_cli
cargo run --release -- --low-storage-mode \
  ../local/windiff_diff_config.json ../local/windiff_diff_out/
```

This downloads PEs from Winbindex and PDBs from MSDL, so it **needs network
access** and takes minutes per binary. `--low-storage-mode` keeps memory bounded.
If the CLI fails for one OS (a build may be missing from Winbindex), report which
version/update is unavailable and suggest the nearest tracked one from
`ci/db_configuration.json`.

If the user says the databases already exist (e.g. in `windiff_frontend/public/`),
skip generation and point the diff script at that directory instead.

### 3. Diff each binary

`scripts/windiff_diff.py` does the deterministic set/text diff so you never hand-
compute it. Run it per binary; it prints a summary to stderr and structured JSON
to stdout.

```bash
python3 .claude/skills/windiff-version-diff-analysis/scripts/windiff_diff.py \
  local/windiff_diff_out ntoskrnl.exe 21H2_BASE_amd64 11-24H2_KB5074105_amd64 \
  > local/diff_ntoskrnl.json
```

Use `--list` to see available suffixes, `--kinds` to restrict (e.g.
`--kinds syscalls types`). Anonymous `_unnamed_0xNNNN` types are hidden from the
top-level added/removed/modified lists by default (their synthetic ids churn
between builds — noise); pass `--include-anon` only if you specifically need them.

**`resolved_member_changes` — where new mitigation flags actually show up.**
Bitfields like `_EPROCESS::MitigationFlagsValues`, `MitigationFlags2Values`, or
`_KPROCESS` flag words are typed as *anonymous* `_unnamed_0xNNNN` structs, and the
individual bits (e.g. `RedirectionTrustPolicyEnabled : 1`) live inside them. When
Microsoft adds a mitigation, a new bit appears in that anonymous struct — and its
synthetic id churns, so a naive diff would either hide it or show it as noise. The
script resolves this for you: the `types.resolved_member_changes` array follows
each anonymous member back to its named parent (across the id change) and reports
the real per-member delta as `<parent>::<member>` with the added/removed
declarations. **This is the first place to look for new mitigation bits and other
new bitfield flags** — e.g. a new bit under `_EPROCESS::MitigationFlags2Values`, or
a new `_KALPC_MESSAGE::u1::s1` flag. Resolution recurses through nested anonymous
structs/unions, so the `path` may be several `::` levels deep.

**Noise to discount when reading the output:**
- The script already strips `modified` lines that differ only by an anonymous type
  id, and folds genuine anonymous-struct changes into `resolved_member_changes`.
  What remains in `modified` is real: renamed/added named fields, size changes, new
  enum values. Still sanity-check against `resolved_member_changes` for the bits.
- Exports differing only by ordinal/decoration are usually not meaningful.
- Syscall renumbering with no name change is a rebuild artifact (see
  `references/windows-internals.md` §3).

### 4. Interpret with Windows internals knowledge — the core of the analysis

For every meaningful addition, infer **what it is and why it matters**. Do not
just relay names. Read `references/windows-internals.md` for the reasoning toolkit:
API prefixes (`Nt`/`Zw`/`Ps`/`Ke`/`Mm`/`Ob`/`Se`/`Cm`/`Alpc`/`Etw`/`Ci`/`Bcrypt`),
naming patterns for mitigations, the structures where security flags live
(`_PS_MITIGATION_OPTIONS`, `_KPROCESS`/`_EPROCESS` flag bitfields, `_SEP_TOKEN_*`,
CI policy structs), and — equally important — the **non-mitigation** security
surface: kernel notification/callback registration, ETW providers and the
`EtwTi` threat-intelligence channel, ELAM/AMSI, PPL and anti-tamper, minifilter
hooks, and entirely new drivers/modules. Read `references/windows-components.md`
for per-binary roles.

Mitigations are only one of several things worth surfacing. Cast a wide net for
any new security-relevant **feature or component** and frame it for whichever of
these audiences it serves — `references/windows-internals.md` §7 maps the signals:

- **Anti-malware / EDR developers** — new ETW providers/events (especially
  `EtwTi*` / Microsoft-Windows-Threat-Intelligence), new `Ps`/`Ob`/`Cm`
  notification callbacks, AMSI/ELAM, scanning/notification hooks: new visibility
  they can consume, or blind spots Microsoft closed.
- **Anti-cheat developers** — process protection (PPL signers), anti-tamper,
  handle/object hardening, integrity and VBS/HVCI surface, registry/handle
  monitoring: primitives for protecting a game or detecting cheats.
- **Vulnerability researchers** — new syscalls/IOCTLs, new parsing surface, new
  drivers/components, widened structs, callback registration reachable from low
  privilege: fresh attack surface and exploit primitives (added or removed).

For each finding, aim to state: the prefix/component it belongs to, the subsystem
it touches, a concrete hypothesis about the feature/mitigation/component it
implements, the security angle (new attack surface, hardening, telemetry, exploit
primitive added/removed), and **which audience(s) should care and why**. Flag
uncertainty honestly — "likely", "consistent with" — and suggest how a researcher
could confirm (reverse the routine, check public symbols, diff the disassembly).

### 5. Write the report

Use the structure in `references/report-template.md`. Lead with the highest-signal
security findings (new syscalls, mitigation flags, new ETW/callback surface, new
components), not an alphabetical dump. Group related symbols by component and
feature. Every nontrivial item gets an interpretation, not just a name, and a note
on which audience (EDR / anti-cheat / vuln research) it matters to. The report
includes a dedicated section for security-relevant features and components beyond
mitigations so EDR and anti-cheat findings aren't buried.

## Quick reference

- `scripts/make_config.py` — build a minimal WinDiff config for the two versions
- `scripts/windiff_diff.py` — diff one binary across two OS suffixes (JSON + summary)
- `references/windows-internals.md` — prefixes, mitigation structures, how to infer intent
- `references/windows-components.md` — role of each tracked binary
- `references/report-template.md` — the report format
