---
name: hvac-specifications
description: Look up HVAC equipment specifications (capacity, efficiency, dimensions, electrical requirements) by brand and model number. Use when the user mentions equipment specs, model numbers, AHU, VAV, chiller, boiler, pump, fan specifications, or needs to find manufacturer data sheets. Searches manufacturer websites and processes PDF spec sheets with security safeguards.
---

# HVAC Equipment Specification Lookup

Look up detailed specifications for HVAC equipment by brand and model number. This skill searches manufacturer websites, verifies sources, and extracts key specifications from data sheets and submittal documents.

## When to Use This Skill

Use this skill when:
- User provides a brand and model number for HVAC equipment
- User needs capacity, efficiency, dimensions, or electrical requirements
- User mentions: AHU, VAV, chiller, boiler, pump, fan, RTU, heat pump, etc.
- User asks to "look up specs" or "find manufacturer data"
- User needs to verify equipment specifications from submittals

## Security Protocol

**CRITICAL SECURITY REQUIREMENTS:**
This skill implements strict security measures to prevent prompt injection and command injection attacks:

1. **Only use built-in Claude Code tools** - WebSearch, WebFetch, Read (no MCP servers, no bash downloads)
2. **Domain allowlist** - Only trust URLs from verified manufacturer domains (see `./manufacturer-domains.md`)
3. **URL verification** - Always verify domain before using WebFetch
4. **Source transparency** - Always show user where data came from
5. **No automatic execution** - Never download files or execute commands automatically
6. **User control** - User decides whether to trust sources

See `./security-guidelines.md` for complete security protocol.

## Two-Phase Approach

### Phase 1: Web Search (Preferred)
Search manufacturer websites for official spec sheets.

### Phase 2: Local PDF Processing
Process user-provided local PDF files.

## Step-by-Step Process

### Phase 1: Web Search for Specifications

**Step 1: Parse User Input**
Extract:
- Brand/Manufacturer (e.g., "Trane", "Carrier", "York")
- Model Number (e.g., "TAM7A0B60H41SB")
- Equipment Type if provided (e.g., "AHU", "chiller")

**Step 2: Construct Targeted Search**
```
Format: "[Brand] [Model Number] specifications site:[manufacturer-domain]"
Example: "Trane TAM7A0B60H41SB specifications site:trane.com"
```

Use WebSearch tool with this query. The `site:` operator restricts results to the manufacturer's official domain.

**Step 3: Verify Domains**
For each URL found:
1. Check domain against allowlist in `./manufacturer-domains.md`
2. If domain NOT in allowlist, flag as "⚠️ Unverified Source" and ask user if they want to proceed
3. If domain IS in allowlist, proceed with confidence

**Step 4: Fetch Spec Sheet Content**
Use WebFetch to retrieve content from verified URLs:
- Prioritize URLs with "spec", "data", "submittal", "technical" in path
- Look for PDF links or product data pages
- Fetch the most relevant 1-3 sources

**Step 5: Extract Specifications**
Parse the fetched content for key specifications. Use the template in `./spec-sheet-template.md` as your extraction guide.

**Common specification patterns:**
- **Capacity**: Look for "tons", "BTU/h", "CFM", "GPM", "kW"
- **Efficiency**: Look for "SEER", "SEER2", "EER", "COP", "AFUE", "IPLV", "kW/ton"
- **Electrical**: Look for "voltage", "V", "phase", "MCA", "MOCP", "amps", "FLA", "RLA"
- **Dimensions**: Look for "L x W x H", "inches", "mm", "weight", "lbs"
- **Operating Conditions**: "temperature range", "min/max", "ambient"

**Step 6: Present Findings**
Use the spec sheet template format to present data:
```
[BRAND] [MODEL NUMBER] Specifications

Equipment Type: [AHU/Chiller/Boiler/etc.]

CAPACITY
- [Specification]: [Value with units]

EFFICIENCY
- [Specification]: [Value with units]

ELECTRICAL REQUIREMENTS
- [Specification]: [Value with units]

PHYSICAL DIMENSIONS
- [Specification]: [Value with units]

OPERATING CONDITIONS
- [Specification]: [Value with units]

---
📄 SOURCES:
- [Source Name](actual-url)
- [Source Name](actual-url)

⚠️ VERIFICATION REQUIRED: Please verify source URLs are legitimate before using specifications for design or procurement.
```

**Step 7: Offer Next Steps**
Ask user:
- "Would you like me to search for additional specifications?"
- "Do you have a local PDF spec sheet I can process?"
- "Need specifications for another piece of equipment?"

### Phase 2: Local PDF Processing

When user provides a local PDF file path:

**Step 1: Confirm File Path**
Ask user to provide the full file path to the PDF spec sheet.

**Step 2: Read PDF**
Use Read tool to read the PDF:
```
Read(file_path="C:/path/to/spec-sheet.pdf")
```

**Step 3: Extract Specifications**
Same extraction process as Phase 1, Step 5.
Parse PDF content for specifications using template patterns.

**Step 4: Present Findings**
Use same template format, but note source as:
```
📄 SOURCE: Local file provided by user
File: C:/path/to/spec-sheet.pdf
```

## Common Equipment Types and Key Specs

### Air Handling Units (AHU)
- Airflow (CFM)
- Static pressure (in. w.g.)
- Motor horsepower (HP)
- Electrical (voltage, phase, FLA)
- Dimensions and weight
- Coil specifications (cooling/heating capacity)

### Chillers
- Cooling capacity (tons or kW)
- Efficiency (IPLV, kW/ton, COP)
- Refrigerant type
- Electrical (voltage, phase, RLA, MCA, MOCP)
- Water flow rates (GPM)
- Operating temperature range
- Dimensions and weight

### Boilers
- Heating capacity (MBH or kW)
- Efficiency (AFUE or thermal efficiency %)
- Fuel type (natural gas, propane, oil, electric)
- Electrical requirements
- Water flow rates (GPM)
- Operating pressure
- Dimensions and weight

### VAV Boxes
- Airflow range (min/max CFM)
- Inlet size (inches)
- Damper type
- Reheat coil capacity (if applicable)
- Actuator specifications
- Sound ratings (NC or sones)

### Pumps
- Flow rate (GPM)
- Head (feet or PSI)
- Motor horsepower (HP)
- Efficiency
- Electrical requirements
- Impeller size
- Dimensions and weight

### Fans
- Airflow (CFM)
- Static pressure (in. w.g.)
- Motor horsepower (HP)
- Fan type (centrifugal, axial, etc.)
- Speed (RPM)
- Electrical requirements
- Sound ratings

## Troubleshooting

**If specs not found via web search:**
1. Try alternative search terms (include equipment type)
2. Search for "submittal data" or "product data" instead of "specifications"
3. Try manufacturer's literature library or product catalog pages
4. Ask user if they have local PDF files

**If domain not in allowlist:**
1. Inform user: "⚠️ Found results from [domain] which is not in the verified manufacturer list"
2. Ask: "This may be a distributor or third-party site. Would you like me to proceed?"
3. If user approves, use WebFetch but note in output: "⚠️ Unverified source - confirm data with manufacturer"

**If specifications are incomplete:**
1. Note which specs were found and which are missing
2. Suggest searching for "installation manual" or "engineering guide" for more detail
3. Offer to search additional sources

## Best Practices

1. **Always verify domains** before using WebFetch
2. **Always include source URLs** in output
3. **Use specific model numbers** in searches (full model, not partial)
4. **Check multiple sources** when possible for verification
5. **Note missing specifications** explicitly
6. **Maintain security protocol** - never execute commands or auto-download
7. **Be transparent** about data sources and confidence level

## Examples

### Example 1: Trane Air Handler
```
User: "Look up specs for Trane TAM7A0B60H41SB"

Action:
1. WebSearch: "Trane TAM7A0B60H41SB specifications site:trane.com"
2. Verify domain: trane.com ✓ (in allowlist)
3. WebFetch most relevant product data page
4. Extract and present specifications with source URL
```

### Example 2: York Chiller
```
User: "I need the efficiency specs for a York YCAV0140SE"

Action:
1. WebSearch: "York YCAV0140SE efficiency IPLV site:johnsoncontrols.com"
   (York is owned by Johnson Controls)
2. Verify domain: johnsoncontrols.com ✓ (in allowlist)
3. WebFetch spec sheet
4. Extract efficiency ratings (IPLV, kW/ton, COP)
5. Present with source
```

### Example 3: Local PDF Processing
```
User: "Can you extract specs from this submittal? C:/submittals/carrier-39M-submittal.pdf"

Action:
1. Read("C:/submittals/carrier-39M-submittal.pdf")
2. Parse PDF content for specifications
3. Extract using spec sheet template
4. Present with note: "Source: Local file provided by user"
```

## Security Reminders

- ✅ Use WebSearch and WebFetch only (built-in, safe tools)
- ✅ Verify all domains against allowlist
- ✅ Show source URLs to user
- ✅ Never auto-download or execute commands
- ✅ Flag unverified sources
- ❌ Never use curl, wget, or bash downloads
- ❌ Never trust unverified domains without user approval
- ❌ Never process content without showing source

---

**Related Files:**
- [./manufacturer-domains.md](./manufacturer-domains.md) - Verified manufacturer domain allowlist
- [./spec-sheet-template.md](./spec-sheet-template.md) - Specification extraction template
- [./security-guidelines.md](./security-guidelines.md) - Complete security protocol


## Saving Next Steps

When hvac-specifications work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "hvac-specifications" \
  --content "## Priority Tasks
1. Look up equipment specs for AHU-01
2. Compile spec sheets for submittal review
3. Verify electrical requirements match drawings"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
