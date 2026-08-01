---
name: manage-generate-subskill-md
description: Skill from boringdata/kurt-demo
---

# Generate Extraction Subskill Subskill

**Purpose:** Generate extraction subskill from template for custom rule type
**Parent Skill:** writing-rules-skill
**Operation:** Management

---

## Context Received from Parent Skill

- `$REGISTRY_PATH` - `rules/rules-config.yaml`
- `$SUBSKILLS_DIR` - `.claude/skills/writing-rules-skill/subskills/`
- `$ARGUMENTS` - Should contain rule type name

---

## Workflow

### Step 1: Parse Arguments

```bash
rule_type="$1"

if [ -z "$rule_type" ]; then
  error "Rule type name required"
  echo "Usage: writing-rules-skill generate-subskill <rule-type>"
  echo "Example: writing-rules-skill generate-subskill verticals"
  echo ""
  echo "To see available types: writing-rules-skill list"
  exit 1
fi
```

### Step 2: Load and Validate Rule Type

```bash
# Load rules-config.yaml
registry_file="rules/rules-config.yaml"

if [ ! -f "$registry_file" ]; then
  error "Rules registry not found"
  exit 1
fi

# Check if rule type exists
if ! rule_type_exists "$rule_type"; then
  error "Rule type '$rule_type' not found in registry"
  echo ""
  echo "Available rule types:"
  list_rule_types
  echo ""
  echo "To add a new type: writing-rules-skill add"
  exit 1
fi

# Load rule type configuration
config=$(get_rule_type_config "$rule_type")
```

### Step 3: Validate Rule Type is Custom

```bash
is_built_in=$(echo "$config" | get_field "built_in")

if [ "$is_built_in" = "true" ]; then
  error "Cannot generate subskill for built-in type '$rule_type'"
  echo ""
  echo "Built-in types (style, structure, persona, publisher) already have extraction subskills."
  echo ""
  echo "This command is only for custom rule types."
  exit 1
fi
```

### Step 4: Check if Subskill Already Exists

```bash
subskill_name=$(echo "$config" | get_field "extraction.subskill")
subskill_path=".claude/skills/writing-rules-skill/subskills/$subskill_name"

if [ -f "$subskill_path" ]; then
  echo "⚠️  Subskill already exists: $subskill_name"
  echo ""
  echo "File: $subskill_path"
  echo ""
  echo "Options:"
  echo "  a) View existing subskill"
  echo "  b) Regenerate (overwrites existing)"
  echo "  c) Cancel"
  echo ""
  read -p "Choose: " choice

  case "$choice" in
    a)
      cat "$subskill_path"
      exit 0
      ;;
    b)
      echo "Regenerating subskill..."
      # Continue to generation
      ;;
    c)
      echo "Operation canceled"
      exit 0
      ;;
    *)
      error "Invalid choice"
      exit 1
      ;;
  esac
fi
```

### Step 5: Load Template

```bash
template_file=".claude/skills/writing-rules-skill/subskills/_template.md"

if [ ! -f "$template_file" ]; then
  error "Template file not found: $template_file"
  echo ""
  echo "The subskill template is missing. This is a system file that should exist."
  echo "Check your Kurt installation."
  exit 1
fi

# Read template content
template_content=$(cat "$template_file")
```

### Step 6: Extract Configuration Values

From the rule type config, extract:

```bash
# Basic info
name=$(echo "$config" | get_field "name")
description=$(echo "$config" | get_field "description")
directory=$(echo "$config" | get_field "directory")

# Extraction config
discovery_modes=$(echo "$config" | get_field "extraction.discovery_modes" | join_array ", ")
sample_size=$(echo "$config" | get_field "extraction.sample_size")
instructions=$(echo "$config" | get_field "extraction.instructions")

# What it extracts/governs
extracts=$(echo "$config" | get_field "extracts" | format_list)
governs=$(echo "$config" | get_field "governs" | format_list)
source_patterns=$(echo "$config" | get_field "source_patterns" | format_list)

# Validation
check_for=$(echo "$config" | get_field "validation.check_for" | format_list)
```

### Step 7: Replace Template Placeholders

Replace all placeholders in template:

```bash
# Simple replacements
output=$(echo "$template_content" \
  | sed "s/{{RULE_TYPE}}/$rule_type/g" \
  | sed "s/{{NAME}}/$name/g" \
  | sed "s/{{DESCRIPTION}}/$description/g" \
  | sed "s/{{DIRECTORY}}/$directory/g" \
  | sed "s/{{DISCOVERY_MODES}}/$discovery_modes/g" \
  | sed "s/{{SAMPLE_SIZE}}/$sample_size/g" \
  | sed "s/{{INSTRUCTIONS}}/$instructions/g"
)

# List replacements (more complex)
output=$(replace_list_placeholder "$output" "{{EXTRACTS}}" "$extracts")
output=$(replace_list_placeholder "$output" "{{GOVERNS}}" "$governs")
output=$(replace_list_placeholder "$output" "{{SOURCE_PATTERNS}}" "$source_patterns")
output=$(replace_list_placeholder "$output" "{{CHECK_FOR}}" "$check_for")
```

### Step 8: Generate Discovery Pattern Examples

Based on source_patterns and discovery_modes, generate example bash code for auto-discovery:

```bash
# For each discovery mode, create a discovery pattern section

discovery_section=""
for mode in $discovery_modes; do
  discovery_section+="
### ${mode^}
\`\`\`bash
# Discover ${mode}-related content
# Based on source patterns: $source_patterns
# Look for: [generate URL patterns based on mode]
# Sample size: $sample_size

${mode}_content=\$(kurt content list --url-contains /${mode} --status FETCHED)
# Sample $sample_size documents
sample=\$(echo \"\$${mode}_content\" | head -${sample_size%%[^0-9]*})
\`\`\`
"
done

# Replace {{DISCOVERY_PATTERNS}} placeholder
output=$(echo "$output" | replace_placeholder "{{DISCOVERY_PATTERNS}}" "$discovery_section")
```

### Step 9: Write Generated Subskill

```bash
output_file=".claude/skills/writing-rules-skill/subskills/extract-$rule_type.md"

# Write to file
echo "$output" > "$output_file"

# Verify file was created
if [ ! -f "$output_file" ]; then
  error "Failed to create subskill file"
  exit 1
fi
```

### Step 10: Display Success Message

```
✅ Extraction subskill generated

Created: extract-{{rule_type}}.md
Location: .claude/skills/writing-rules-skill/subskills/

The subskill has been generated from the template with your
rule type's configuration.

───────────────────────────────────────────────────────

What was generated:
  • Auto-discovery patterns for: {{discovery_modes}}
  • Extraction workflow for {{name}}
  • Instructions: "{{instructions}}"
  • Sample size: {{sample_size}}

───────────────────────────────────────────────────────

Next steps:

1. Review the generated subskill:
   View file: .claude/skills/writing-rules-skill/subskills/extract-{{rule_type}}.md

2. Customize if needed:
   • Adjust discovery patterns
   • Refine extraction logic
   • Add specific validations

3. Extract your first rule:
   writing-rules-skill {{rule_type}} --type {{first_mode}} --auto-discover

4. Validate everything works:
   writing-rules-skill validate

═══════════════════════════════════════════════════════
```

### Step 11: Offer to Show File

```
Would you like to view the generated subskill? (y/n) _
```

**If yes:**
```bash
cat "$output_file" | less
```

---

## Template Variable Reference

The template uses these placeholders:

**Basic Info:**
- `{{RULE_TYPE}}` - Rule type slug (e.g., "verticals")
- `{{NAME}}` - Display name (e.g., "Industry Verticals")
- `{{DESCRIPTION}}` - Description text
- `{{DIRECTORY}}` - Directory name in rules/

**Extraction Config:**
- `{{DISCOVERY_MODES}}` - Comma-separated list of modes
- `{{SAMPLE_SIZE}}` - Number of documents to analyze
- `{{INSTRUCTIONS}}` - LLM extraction instructions

**Lists (formatted as markdown bullets):**
- `{{EXTRACTS}}` - What this rule type extracts
- `{{GOVERNS}}` - What this rule type governs
- `{{SOURCE_PATTERNS}}` - Document types to analyze
- `{{CHECK_FOR}}` - Validation checks

**Generated Content:**
- `{{DISCOVERY_PATTERNS}}` - Auto-generated discovery bash code

---

## Example Output

For rule type "verticals":

```markdown
# Extract Verticals Subskill

**Purpose:** Extract Industry-specific messaging, terminology, and compliance
**Parent Skill:** writing-rules-skill
**Output:** verticals files in `rules/verticals/`

---

## What This Rule Type Extracts

- **industry_terminology** - Industry-specific language and jargon
- **compliance_considerations** - Regulatory requirements
- **vertical_pain_points** - Industry-specific challenges
- **success_metrics** - KPIs relevant to the vertical

## What This Rule Type Governs

- **industry_language** - Use of industry-specific terminology
- **regulatory_compliance** - Adherence to compliance requirements
- **vertical_positioning** - How to position in the vertical

---

## Auto-Discovery Patterns

### Healthcare
```bash
# Discover healthcare-related content
healthcare_content=$(kurt content list --url-contains /healthcare --status FETCHED)
# Sample 3-5 documents
```

### Finance
```bash
# Discover finance-related content
finance_content=$(kurt content list --url-contains /finance --status FETCHED)
# Sample 3-5 documents
```

[...continues with full extraction workflow...]
```

---

## Error Handling

**If template is malformed:**
```
Error: Template file is malformed

Manual intervention required. Check _template.md for syntax errors.
```

**If file write fails:**
```
Error: Could not write subskill file

Check permissions on .claude/skills/writing-rules-skill/subskills/ directory.
```

---

*This subskill automates the creation of extraction workflows for custom rule types, making it easy to extend the rules framework.*
