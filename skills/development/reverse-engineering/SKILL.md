---
name: reverse-engineering
description: Use when reverse-engineering a binary or firmware — static triage + decompilation (Ghidra/IDA/Binary Ninja), dynamic instrumentation (GDB/Frida 17/angr), anti-reversing & packer bypass, OLLVM/VM deobfuscation, UEFI/BIOS RE & Secure Boot research, patch-diffing for n-days
metadata:
  type: offensive
  phase: analysis
  tools: ghidra, ida, binary-ninja, radare2, rizin, gdb-gef, frida, x64dbg, x96dbg, triton, angr, unicorn, capstone, scyllahide, titanhide, novmp, bindiff, diaphora, ghidriff, binwalk, uefitool, chipsec, kaitai-struct
  mitre: TA0042
kill_chain:
  phase: [weaponize, exploit]
  step: [2, 4]
  attck_tactics: [TA0042, TA0002, TA0005]
  attck_techniques: [T1027, T1027.002, T1027.007, T1027.009, T1027.013, T1620, T1140, T1622, T1497, T1497.001, T1497.003, T1542.001, T1542.003, T1592.002, T1203, T1518.001]
depends_on: [recon-osint]
feeds_into: [exploit-development, malware-analysis, vulnerability-analysis, mobile-pentest, windows-mitigations]
inputs: [binary_samples, firmware_images, packed_malware, patched_binaries, pcap_captures, unknown_file_formats]
outputs: [disassembly_report, decompiled_source, vulnerability_details, unpacked_payload, deobfuscated_code, protocol_specs, nday_root_cause, ioc_list]
references:
  - references/static-triage-decompilation.md
  - references/dynamic-instrumentation.md
  - references/anti-reversing-bypass.md
  - references/deobfuscation.md
  - references/firmware-uefi.md
  - references/patch-diffing-protocol.md
scripts:
  - scripts/triage.py
  - scripts/frida_universal.js
  - scripts/antidebug_unhook.py
  - scripts/string_decrypt_emu.py
  - scripts/deflatten_triton.py
  - scripts/uefi_triage.py
  - scripts/patchdiff_fetch.py
  - scripts/proto_infer.py
---

# Reverse Engineering

## When to Activate

- Triaging an unknown compiled binary (ELF/PE/Mach-O) or stripped/obfuscated sample for vulns or capability.
- Decompiling proprietary code and recovering structure/types (incl. AI/MCP-assisted Ghidra/Binary Ninja).
- Unpacking & devirtualizing protected binaries (VMProtect 3.x, Themida, OLLVM control-flow flattening).
- Defeating anti-debugging / anti-VM / anti-Frida so dynamic analysis can proceed.
- Firmware extraction & UEFI/BIOS RE, Secure Boot bypass research, persistent pre-OS implant analysis.
- Patch diffing a Patch-Tuesday/CVE fix to recover root cause and build an n-day trigger.
- Reverse engineering an unknown wire protocol or proprietary file format for fuzzing/parsing.

## Technique Map

| Technique | ATT&CK | CWE | Reference | Script |
|-----------|--------|-----|-----------|--------|
| Binary triage (format/arch/mitigations/strings/imports) | T1592.002, T1518.001 | CWE-1395 | references/static-triage-decompilation.md | scripts/triage.py |
| Headless decompilation (Ghidra 11.4 / r2 / IDA) | T1592.002 | CWE-noinfo | references/static-triage-decompilation.md | scripts/triage.py |
| AI/MCP-assisted RE (Sidekick / GhidrAssistMCP / LLM4Decompile) | T1592.002 | CWE-noinfo | references/static-triage-decompilation.md | - |
| Dynamic debugging (GDB/GEF, x64dbg, conditional bps) | T1622 | CWE-noinfo | references/dynamic-instrumentation.md | - |
| Frida 17 instrumentation + SSL-pin/JNI hooking | T1622, T1562.001 | CWE-noinfo | references/dynamic-instrumentation.md | scripts/frida_universal.js |
| Symbolic / concolic execution (angr, Triton) | T1480.001 | CWE-noinfo | references/dynamic-instrumentation.md | scripts/deflatten_triton.py |
| Anti-debug detection & bypass (PEB/ptrace/HW-bp/timing) | T1622, T1497.001 | CWE-noinfo | references/anti-reversing-bypass.md | scripts/antidebug_unhook.py |
| Anti-VM / sandbox-evasion neutralization | T1497, T1497.003 | CWE-noinfo | references/anti-reversing-bypass.md | scripts/antidebug_unhook.py |
| Packer unpack → OEP dump (UPX/runtime packers) | T1027.002, T1620 | CWE-noinfo | references/anti-reversing-bypass.md | scripts/antidebug_unhook.py |
| String / API-hash deobfuscation (Unicorn emulation) | T1027.013, T1140, T1027.007 | CWE-noinfo | references/deobfuscation.md | scripts/string_decrypt_emu.py |
| OLLVM control-flow-flattening de-flattening | T1027.009, T1027 | CWE-noinfo | references/deobfuscation.md | scripts/deflatten_triton.py |
| VM-protector devirtualization (VMProtect 3.x / Themida) | T1027.009 | CWE-noinfo | references/deobfuscation.md | scripts/deflatten_triton.py |
| Firmware extraction (binwalk/squashfs/QEMU emulation) | T1542.001 | CWE-1263 | references/firmware-uefi.md | scripts/uefi_triage.py |
| UEFI/BIOS RE + Secure Boot bypass research | T1542.001, T1542.003 | CWE-347 | references/firmware-uefi.md | scripts/uefi_triage.py |
| Patch diffing → n-day root cause (BinDiff/Diaphora/ghidriff) | T1203, T1592.002 | CWE-noinfo | references/patch-diffing-protocol.md | scripts/patchdiff_fetch.py |
| Protocol / file-format inference (Netzob/Kaitai) | T1592.002 | CWE-noinfo | references/patch-diffing-protocol.md | scripts/proto_infer.py |

## Quick Start

```bash
# 0. Triage: format, arch, mitigations, packer entropy, strings, imports, capabilities → JSON
python3 scripts/triage.py ./sample -o out/triage.json

# 1. Headless decompile to C (Ghidra 11.4 analyzeHeadless wrapper inside triage.py --decompile)
python3 scripts/triage.py ./sample --decompile --ghidra "$GHIDRA_HOME" -o out/

# 2. If packed/protected → defeat anti-debug, dump OEP (run under x64dbg+ScyllaHide on Windows)
python3 scripts/antidebug_unhook.py --scan ./sample      # enumerate anti-debug primitives first

# 3. Dynamic: attach Frida (Android/Linux/Win), universal SSL-unpin + native trace
frida -U -f com.target.app -l scripts/frida_universal.js --no-pause

# 4. Deobfuscate: emulate string decryptor over all xrefs; de-flatten OLLVM with Triton
python3 scripts/string_decrypt_emu.py ./sample --func 0x401500 --auto-xref -o out/strings.txt
python3 scripts/deflatten_triton.py ./sample --func 0x401abc -o out/cfg.dot

# 5. Firmware: carve + identify + map UEFI DXE/PEI attack surface, scan for PKfail/known hashes
python3 scripts/uefi_triage.py firmware.bin -o out/fw/

# 6. n-day: fetch pre/post-patch Windows binary from winbindex and diff
python3 scripts/patchdiff_fetch.py --pe afd.sys --kb-after KB5050000 -o out/diff/

# 7. Unknown protocol: infer fields/state machine from a pcap, emit Kaitai + Wireshark dissector
python3 scripts/proto_infer.py capture.pcap --port 4444 -o out/proto/
```

## OPSEC & Detection (summary)

| Technique | Telemetry / IOC | Detection (Sigma/EDR) | OPSEC note |
|-----------|-----------------|------------------------|------------|
| Static triage / decompile | None (offline on analyst box) | N/A — runs in lab | Analyze copies in an isolated, snapshotted VM; never on the target |
| Frida / dynamic hooking | `frida-agent.so` in `/proc/self/maps`, port 27042, `gum-js-loop`/`gmain` threads, `ptrace` on target | App-side RASP (Talsec/DeepID), frida-string scans, EDR userland hook tripwires | Rename agent, use gadget+`-l` script mode, embed gadget in APK to dodge port checks |
| Anti-debug bypass | Debug registers DR0-7 set, PEB.BeingDebugged flips, hooked Nt* prologues | Self-integrity checks, KiUserExceptionDispatcher checks, TitanHide-vs-malware arms race | Prefer kernel TitanHide/HyperHide for hardened packers; snapshot before each run |
| Packer/OEP dump | New RWX region, IAT rebuild, written `dump.exe` on disk | EDR RWX-alloc + tail-jump heuristics (lab only) | All in lab; dumped sample is for analysis, not redeployment |
| String/API-hash decrypt (Unicorn) | None on target (offline emulation) | N/A | Pure offline; safe — no sample execution of network/FS code |
| Firmware / SPI flash dump | Hardware: chip-clip on SPI; software: `chipsec`/`flashrom` reads | Boot Guard / measured boot (TPM PCRs), Binarly/CHIPSEC verifiers | Physical/authorized only; flashing back a modded image is destructive & loud |
| Secure Boot bypass research | New unsigned bootloader in ESP, MokList/dbx anomalies, unexpected `bootmgfw` hash | Measured boot PCR[0/2/4/7] drift, `dbx` revocation checks, ESET/Binarly scanners | Lab VMs / disposable hardware; document, never persist a real implant |
| Patch diffing | None on target (fetches public binaries) | N/A | Public Microsoft/distro binaries; n-day PoC stays in lab until disclosure/ROE |
| Protocol inference | Replays captured/crafted packets at the service | IDS on malformed/replayed frames; rate anomalies | Throttle active probes; prefer passive pcap when a live target is in scope |

## Deep Dives

- references/static-triage-decompilation.md — File/arch/mitigation triage, entropy & packer ID, capability detection (capa), Ghidra 11.4 `analyzeHeadless` + PyGhidra, r2/rizin & IDA decompile flows, and the 2025 AI/MCP-assisted layer (Binary Ninja Sidekick, GhidrAssistMCP, LLM4Decompile / SK²Decompile) with verification discipline.
- references/dynamic-instrumentation.md — GDB/GEF & x64dbg workflows, conditional/commands breakpoints, Frida 17 internals (Interceptor/Stalker/Java), universal SSL-unpin + JNI tracing, and angr/Triton symbolic + concolic execution with backward slicing for path/value recovery.
- references/anti-reversing-bypass.md — Anti-debug taxonomy (PEB flags, NtSetInformationThread/ThreadHideFromDebugger, DR0-7 / GetThreadContext, KiUserExceptionDispatcher, NtClose, INT 2D, rdtsc timing, Linux ptrace/TracerPid), anti-VM/al-khaser, ScyllaHide/TitanHide, and runtime-packer OEP dumping.
- references/deobfuscation.md — String & API-hash decryption via Unicorn emulation, OLLVM control-flow-flattening de-flattening (dispatcher recovery, Triton backward slicing à la LummaC2), MBA simplification, and VM-protector devirtualization (NoVmp/VTIL, Titan, Triton lifting) for VMProtect 3.x / Themida.
- references/firmware-uefi.md — binwalk/unblob carving, squashfs/JFFS2 extraction, QEMU+afl emulation, UEFI volume/DXE/PEI parsing (UEFITool/chipsec), SMM callout & NVRAM variable surface, and Secure Boot bypass research with the verified 2024-2025 chain: LogoFAIL (CVE-2023-40238), PKfail (CVE-2024-8105), CVE-2024-7344, BlackLotus/Bootkitty context.
- references/patch-diffing-protocol.md — winbindex binary acquisition, MSU/CAB extraction, BinDiff/Diaphora/ghidriff function-level diffing, LLM-assisted triage (PatchWatch/DiffRays) with hallucination caveats, late-2025 kernel targets (cldflt.sys, win32k, CLFS), plus network/file-format protocol RE (Netzob, Kaitai Struct, BinPRE-style field inference).
