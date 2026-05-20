---
name: investigating-hms-internals
description: |
  Investigates HEC-HMS internals through decompiled Java classes. Provides JythonHms
  API reference, CLI options, version-specific differences (3.x vs 4.x), and guides
  on-demand decompilation for new discoveries. Use when debugging HMS behavior,
  discovering undocumented features, understanding version differences, validating
  automation approaches, or investigating HMS API capabilities. Includes complete
  JythonHms method reference, Python 2 vs 3 syntax differences, and decompilation
  tooling. Complements hms_doc_query (official docs) with internal implementation details.

  Trigger keywords: decompile, HMS internals, JythonHms API, HMS version differences,
  CLI options, undocumented, HMS jar, HMS classes, debugging HMS, HMS source code,
  HMS 3.x support, Python 2 vs 3, HMS methods, HMS parameters.
---

# Investigating HMS Internals

**Purpose**: Understand HEC-HMS internal implementation through decompiled Java classes to support hms-commander development and debugging.

---

## Quick Start

### Check JythonHms Method
```
Q: "Does HMS support SetTimeWindow()?"
A: See hms_agents/hms_decompiler/knowledge/JYTHON_HMS_API.md
```

### Check Version Compatibility
```
Q: "Does HMS 3.3 support Jython?"
A: See hms_agents/hms_decompiler/knowledge/HMS_3x_SUPPORT.md
→ YES! Discovered via decompilation
```

### Decompile New Class
```
cd hms_agents/hms_decompiler/tools
decompile.bat "C:\...\hms.jar" "hms.model.ClassName" output
```

---

## Primary Sources

### Production Agent
**Location**: `hms_agents/hms_decompiler/`

**Quick access**:
- `QUICK_START.md` - 5-minute guide
- `AGENT.md` - Comprehensive documentation
- `knowledge/` - Curated API references
- `reference/` - Key decompiled classes
- `tools/` - Decompilation utilities (cfr.jar)
- `examples/` - Usage workflows

**This agent is self-contained** with all necessary reference data and tools.

---

## When to Use This Skill

### ✅ Use When

1. **Checking API Existence**
   - "Does JythonHms have method X?"
   - "What parameters does SetLossRateValue accept?"
   - "Is there a method to set time window?"

2. **Version Compatibility**
   - "Does HMS 3.x support Jython?"
   - "What's different between HMS 3.x and 4.x?"
   - "Will this API work in HMS 3.5?"

3. **Understanding Behavior**
   - "Why does this HMS call fail?"
   - "What error codes does HMS use?"
   - "How does HMS execute scripts?"

4. **Discovering Features**
   - "Are there undocumented JythonHms methods?"
   - "What CLI flags does HMS support?"
   - "Does HMS have an RMI command server?"

5. **Validating Automation**
   - "Can I automate optimization via Jython?"
   - "How should I structure my script?"
   - "What's the correct method signature?"

### ❌ Don't Use When

1. **Official Documentation Query**
   - Use **hms_doc_query** agent instead
   - hms_doc_query searches User's Manual, Technical Reference

2. **hms-commander API Questions**
   - Read hms-commander docstrings
   - Check examples/ notebooks
   - See hms-commander documentation

3. **Project File Parsing**
   - Use **parsing-basin-models** skill
   - Use HmsBasin, HmsMet, HmsControl classes

---

## Knowledge Files

### 1. JYTHON_HMS_API.md

**Location**: `hms_agents/hms_decompiler/knowledge/JYTHON_HMS_API.md`

**Contains**:
- Complete JythonHms method reference (HMS 4.x)
- Method signatures, parameters, exceptions
- Examples and usage notes
- Internal implementation details
- Deprecated/removed methods

**Example lookup**:
```
Q: "What parameters does SetLossRateValue accept?"
A: SetLossRateValue(elementName, parameterName, value)
   - elementName (String): Subbasin name
   - parameterName (String): e.g., "Curve Number"
   - value (double): Parameter value
```

### 2. HMS_3x_SUPPORT.md

**Location**: `hms_agents/hms_decompiler/knowledge/HMS_3x_SUPPORT.md`

**Contains**:
- HMS 3.x Jython support discovery (✅ YES!)
- Python 2 vs 3 syntax differences
- API method availability (3.x vs 4.x)
- Example scripts for both versions
- Test results from hms-commander

**Key finding**:
```
HMS 3.3+ supports Jython scripting (undocumented)!
Requires Python 2 syntax: print "text" (not print("text"))
Use Compute() instead of ComputeRun()
```

### 3. HMS_CLI_OPTIONS.md

**Location**: `hms_agents/hms_decompiler/knowledge/HMS_CLI_OPTIONS.md`

**Contains**:
- Complete CLI arguments discovered via decompilation
- `-script`, `-lite`, `-debug`, `-info`, `CommandServer`
- Version compatibility (which flags in which HMS versions)
- Usage examples

**Example**:
```
Q: "How do I run HMS without GUI?"
A: HEC-HMS.cmd -lite -script path/to/script.py
```

---

## Reference Classes

**Location**: `hms_agents/hms_decompiler/reference/`

### HMS 3.3
- `HMS_3.3/hms/Hms.java` - Entry point, CLI parsing
- `HMS_3.3/hms/model/JythonHms.java` - Scripting API (3.x)
- `HMS_3.3/hec/map/hms/*.java` - GIS support

### HMS 4.13
- `HMS_4.13/hms/Hms.java` - Entry point, CLI parsing
- `HMS_4.13/hms/model/JythonHms.java` - Scripting API (4.x)
- `HMS_4.13/hms/command/HmsCommandServerImpl.java` - RMI server

**Use**: Review implementation details for specific methods

---

## Tools

### CFR Decompiler

**Location**: `hms_agents/hms_decompiler/tools/cfr.jar`

**Usage**:
```batch
cd hms_agents/hms_decompiler/tools
java -jar cfr.jar "C:\Program Files\HEC\HEC-HMS\4.13\java\hms.jar" --classfilter "hms.model.ClassName" --outputdir output
```

**Options**:
- `--classfilter <pattern>` - Filter classes to decompile
- `--outputdir <dir>` - Output directory for decompiled classes

---

## Common Use Cases

### Use Case 1: Query JythonHms API

**Example**: Check if `SetTimeWindow()` exists

**Steps**:
1. Open `knowledge/JYTHON_HMS_API.md`
2. Search for "SetTimeWindow"
3. Result: ✅ Found

**See**: `examples/query_jython_api.md`

### Use Case 2: Check Version Compatibility

**Example**: Verify HMS 3.3 supports Jython

**Steps**:
1. Open `knowledge/HMS_3x_SUPPORT.md`
2. Review "Supported Versions"
3. Result: ✅ HMS 3.3+ supports Jython (Python 2 syntax required)

**See**: `examples/version_compatibility.md`

### Use Case 3: Decompile New Class

**Example**: Investigate how optimization works

**Steps**:
1. Check if already in agent reference/
2. If not, use tools/cfr.jar to decompile
3. Review decompiled source
4. Document findings if high-value

**See**: `examples/decompile_new_class.md`

---

## Integration with hms-commander

### How This Skill Supports Development

**HmsJython.py implementation**:
- Uses JythonHms API reference from JYTHON_HMS_API.md
- Implements python2_compatible flag based on HMS_3x_SUPPORT.md
- Method signatures validated against decompiled source

**HmsCmdr.py execution**:
- CLI options discovered from HMS_CLI_OPTIONS.md
- Version detection patterns from decompiled Hms.java
- Direct Java invocation (bypasses batch file bugs)

**Error handling**:
- Error codes from decompiled source
- Exception handling patterns from JythonHms.java

---

## On-Demand Decompilation

The agent provides tools for decompiling any HMS class as needed:

**Included**:
- CFR decompiler (tools/cfr.jar)
- Essential reference classes (reference/)
- Curated knowledge files (knowledge/)

**For New Classes**:
1. Use cfr.jar to decompile the class
2. Analyze the decompiled source
3. Add to agent reference/ if high-value
4. Document findings in knowledge/ if commonly needed

**This agent contains all necessary tools** for HMS internal investigation.

---

## Examples

### Example 1: query_jython_api.md
**Demonstrates**: Checking if JythonHms method exists and understanding parameters

**Workflow**:
1. Open JYTHON_HMS_API.md
2. Search for method
3. Review signature and parameters
4. Check hms-commander integration status

### Example 2: version_compatibility.md
**Demonstrates**: Understanding HMS 3.x vs 4.x differences

**Key findings**:
- HMS 3.x DOES support Jython (Python 2)
- API differences (Compute vs ComputeRun)
- Architecture (32-bit vs 64-bit)

### Example 3: decompile_new_class.md
**Demonstrates**: Complete workflow from question to decompilation to documentation

**Steps**:
1. Identify target class
2. Check if already decompiled
3. Decompile using tools
4. Analyze findings
5. Document in library

---

## Skill Workflow

### Standard Investigation Flow

```
User Question
    ↓
Check Agent Knowledge
    ├─ JYTHON_HMS_API.md → Found? → Answer
    ├─ HMS_3x_SUPPORT.md → Found? → Answer
    └─ HMS_CLI_OPTIONS.md → Found? → Answer
    ↓ (Not Found)
Check Library INDEX.md
    ├─ Class listed? → Read decompiled source → Answer
    └─ Not listed? → Decompile on-demand → Document → Answer
```

### Adding New Knowledge

```
Decompile Class (tools/cfr.jar)
    ↓
Analyze Source
    ↓
High-Value Finding?
    ├─ YES → Add to agent reference/
    └─ NO → Keep in local output/
    ↓
Update AGENT.md if commonly needed
    ↓
Document in knowledge/ if API-relevant
```

---

## Limitations

### What This Skill CAN Do
- ✅ Provide JythonHms API reference
- ✅ Show version differences (3.x vs 4.x)
- ✅ List CLI options
- ✅ Decompile any HMS class on-demand using included tools
- ✅ Explain HMS internal behavior

### What This Skill CANNOT Do
- ❌ Replace official HMS documentation (use hms_doc_query)
- ❌ Modify HMS source code
- ❌ Guarantee 100% decompilation accuracy
- ❌ Explain "why" design decisions were made (only "how" implementation works)

---

## Related Skills & Agents

### hms_doc_query Agent
**Purpose**: Search official HMS documentation

**Complementary use**:
- hms_doc_query → What's documented
- investigating-hms-internals → How it works internally

### update_3_to_4 Agent
**Purpose**: Migrate HMS projects from 3.x to 4.x

**Uses**: HMS_3x_SUPPORT.md for version differences

### managing-hms-versions Skill
**Purpose**: Detect and work with multiple HMS versions

**Uses**: Version detection patterns from decompilation

---

## Quality Checklist

Before answering user questions:

- [ ] Checked agent `knowledge/` files first
- [ ] If not found, checked agent `reference/` classes
- [ ] Decompiled on-demand using tools/cfr.jar if necessary
- [ ] Documented findings in agent if high-value
- [ ] Pointed to primary sources (not duplicated content)
- [ ] Clarified limitations of decompiled code

---

## Quick Reference

**Common questions → Files**:

| Question | File |
|----------|------|
| "What JythonHms methods exist?" | knowledge/JYTHON_HMS_API.md |
| "Does HMS 3.x support Jython?" | knowledge/HMS_3x_SUPPORT.md |
| "What CLI options are available?" | knowledge/HMS_CLI_OPTIONS.md |
| "How do I decompile a class?" | Use tools/cfr.jar directly |
| "What classes are available?" | reference/ directory + on-demand decompilation |

---

**Status**: Production skill
**Version**: 1.0
**Created**: 2025-12-12
**Agent**: hms_decompiler
