---
name: querying-hms-documentation
description: |
  Queries official HEC-HMS documentation to answer technical questions. Provides access to
  User's Manual, Technical Reference Manual, Release Notes, and community resources.
  Use when seeking official documentation on HMS methods, parameters, file formats,
  version features, or workflow guidance. Complements investigating-hms-internals (decompiled
  source code) with authoritative documentation.

  Trigger keywords: HMS documentation, User's Manual, Technical Reference, loss methods,
  transform methods, routing methods, HMS parameters, file formats, release notes,
  HMS version features, method parameters, official HMS, USACE documentation.
---

# Querying HMS Documentation

**Purpose**: Answer technical questions using official HEC-HMS documentation from the U.S. Army Corps of Engineers (USACE) Hydrologic Engineering Center.

---

## Quick Start

### Query Method Parameters
```
Q: "What parameters does SCS Curve Number require?"
A: See hms_agents/hms_doc_query/AGENT.md → query_documentation("SCS Curve Number parameters", focus_area="loss_methods")
```

### Check File Format
```
Q: "How are subbasins defined in .basin files?"
A: See hms_agents/hms_doc_query/AGENT.md → query_documentation("subbasin definition", focus_area="file_formats")
```

### Version Features
```
Q: "What was added in HMS 4.11?"
A: See hms_agents/hms_doc_query/AGENT.md → search_release_notes("4.11")
```

---

## Primary Sources

### Production Agent
**Location**: `hms_agents/hms_doc_query/`

**Quick access**:
- `QUICK_START.md` - 5-minute guide
- `AGENT.md` - Comprehensive documentation
- `doc_query.py` - Query implementation

**This agent queries official documentation** via web requests to HEC documentation servers.

---

## Documentation Sources

### Official USACE Documentation

| Source | URL | Coverage |
|--------|-----|----------|
| User's Manual | https://www.hec.usace.army.mil/confluence/hmsdocs/hmsum/latest/ | UI, workflows, methods |
| Technical Reference | https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/latest/ | Method algorithms, equations |
| Release Notes | https://www.hec.usace.army.mil/software/hec-hms/downloads.aspx | Version changes, features |
| Downloads | https://www.hec.usace.army.mil/software/hec-hms/downloads.aspx | Installation, examples |

### Community Resources

| Source | URL | Coverage |
|--------|-----|----------|
| The RAS Solution Forum | https://therassolution.kleinschmidtgroup.com/ | Professional Q&A |
| Hydro School Forums | https://hydroschool.org/forums/ | Tutorials, modeling |
| Reddit r/HECRAS | https://www.reddit.com/r/HECRAS/ | Quick questions |

---

## When to Use This Skill

### Use When

1. **Method Documentation**
   - "What parameters does Clark Unit Hydrograph require?"
   - "How does Green-Ampt loss method work?"
   - "What's the difference between ModClark and Clark?"

2. **File Format Questions**
   - "What is the structure of a .control file?"
   - "How are gages defined in .gage files?"
   - "What DSS pathname format does HMS use?"

3. **Version-Specific Features**
   - "Is gridded soil moisture available in HMS 4.10?"
   - "What new features were added in HMS 4.11?"
   - "When was the EAP transform introduced?"

4. **Workflow Guidance**
   - "How do I set up gridded precipitation?"
   - "How do I configure a reservoir routing model?"
   - "What's the workflow for calibration?"

5. **Troubleshooting**
   - "What does WARNING 10020 mean?"
   - "Why am I getting NullPointerException?"
   - "How do I fix 'Project not found' errors?"

### Don't Use When

1. **Internal Implementation Details**
   - Use **investigating-hms-internals** skill instead
   - investigating-hms-internals has decompiled source code

2. **JythonHms API Reference**
   - Use **investigating-hms-internals** skill
   - Decompiled JythonHms.java has complete method signatures

3. **Undocumented Features**
   - Official docs won't cover undocumented behavior
   - Use investigating-hms-internals for source code analysis

4. **hms-commander API Questions**
   - Read hms-commander docstrings directly
   - Check examples/ notebooks

---

## Query Functions

### query_documentation()
Main function to query HMS documentation.

**Parameters**:
- `question` (str): The technical question
- `focus_area` (str): Narrow search
  - "loss_methods", "transform_methods", "routing_methods"
  - "file_formats", "workflows", "release_notes"
  - "installation", "troubleshooting"
- `hms_version` (str): Target version (e.g., "4.11")

### get_method_parameters()
Get parameter details for specific HMS method.

**Parameters**:
- `method_type` (str): "loss", "transform", "baseflow", "routing"
- `method_name` (str): Name of the method

### search_release_notes()
Search HMS release notes.

**Parameters**:
- `query` (str): Search query
- `version` (str): Specific version to search

### validate_method_name()
Check if method name is valid in HMS.

**Parameters**:
- `method_name` (str): Method name to validate
- `method_type` (str): "loss", "transform", etc.

---

## Common Questions

### Loss Methods
| Question | Focus Area |
|----------|------------|
| "What are SCS Curve Number parameters?" | loss_methods |
| "How does Deficit-Constant differ from Initial-Constant?" | loss_methods |
| "What is Green-Ampt infiltration?" | loss_methods |

### Transform Methods
| Question | Focus Area |
|----------|------------|
| "Clark Unit Hydrograph parameters?" | transform_methods |
| "How to calculate Time of Concentration?" | transform_methods |
| "What's the difference between Clark and ModClark?" | transform_methods |

### Routing Methods
| Question | Focus Area |
|----------|------------|
| "Muskingum-Cunge parameters?" | routing_methods |
| "How does kinematic wave routing work?" | routing_methods |
| "Modified Puls vs Muskingum?" | routing_methods |

### File Formats
| Question | Focus Area |
|----------|------------|
| "Structure of .basin file?" | file_formats |
| "DSS pathname format for HMS?" | file_formats |
| "How are time series stored?" | file_formats |

---

## Known Limitations

### Image/Screenshot Support
**IMPORTANT**: HMS documentation relies heavily on screenshots and diagrams.

- WebFetch retrieves TEXT content from documentation pages
- Images are REFERENCED but NOT RENDERED
- Agent cannot describe UI screenshots or visual diagrams
- Agent CAN identify when images exist and reference captions

**Workaround**: Agent provides URLs for manual viewing when visual content is needed.

### Other Limitations
- Cannot access local HMS installation help files
- PDF manuals require direct URLs
- Community forums have varying quality
- Version differences may not be clearly documented

---

## Complementary Skills

### investigating-hms-internals
**Purpose**: Decompiled source code analysis

**Complementary use**:
| Question Type | Use This Skill |
|---------------|----------------|
| "What does the documentation say about X?" | querying-hms-documentation |
| "How does HMS actually implement X?" | investigating-hms-internals |
| "What parameters are documented for X?" | querying-hms-documentation |
| "What is the JythonHms method signature for X?" | investigating-hms-internals |

### Related Skills
- **parsing-basin-models** - Working with basin files
- **executing-hms-runs** - Running simulations
- **managing-hms-versions** - Version detection and handling

---

## Integration with hms-commander

This skill supports hms-commander development by providing:

1. **Method Validation**: Verify method names and parameters before use
2. **File Format Guidance**: Understand file structures when parsing
3. **Version Compatibility**: Check feature availability across versions
4. **Troubleshooting Context**: Interpret error messages

**Example workflow**:
```python
# 1. Query documentation for method parameters
# Use hms_doc_query to verify "Deficit and Constant" parameters

# 2. Set parameters with confidence
from hms_commander import HmsBasin
HmsBasin.set_loss_parameters(
    "model.basin", "Sub1",
    method="Deficit and Constant",
    initial_deficit=0.5,
    maximum_deficit=1.0,
    constant_rate=0.2,
    impervious_percent=10
)
```

---

## Skill Workflow

### Standard Query Flow

```
User Question
    |
    v
Identify Focus Area
    |-- loss_methods, transform_methods, routing_methods
    |-- file_formats, workflows, release_notes
    |-- installation, troubleshooting
    |
    v
Query Documentation (hms_doc_query)
    |
    v
Return Answer + Source URLs
    |
    v
Provide URL for Visual Content (if needed)
```

### When to Escalate to Code Analysis

```
Documentation Query
    |
    v
Answer Found? --> YES --> Return Answer
    |
    NO
    |
    v
Undocumented Feature?
    |
    v
Use investigating-hms-internals
    |
    v
Decompile and Analyze Source
```

---

## Quality Checklist

Before answering user questions:

- [ ] Identified appropriate focus area
- [ ] Queried correct documentation source
- [ ] Provided source URLs for verification
- [ ] Noted when visual content exists but cannot be shown
- [ ] Suggested investigating-hms-internals for undocumented features
- [ ] Pointed to primary sources (not duplicated content)

---

## Quick Reference

**Common questions -> Focus areas**:

| Question Type | Focus Area |
|---------------|------------|
| Method parameters | loss_methods, transform_methods, routing_methods |
| File structure | file_formats |
| Version features | release_notes |
| How-to guides | workflows |
| Error messages | troubleshooting |
| Setup/install | installation |

**Agent location**: `hms_agents/hms_doc_query/`

**Documentation URLs**:
- User's Manual: https://www.hec.usace.army.mil/confluence/hmsdocs/hmsum/latest/
- Technical Reference: https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/latest/

---

**Status**: Production skill
**Version**: 1.0
**Created**: 2025-12-17
**Agent**: hms_doc_query
