---
name: curriculum-validate-cc
description: Validate IMS Common Cartridge 1.3 packages against spec, check manifest schema, verify file references, validate QTI assessments, and ensure LMS compatibility. Use when validating CC packages before delivery. Activates on "validate Common Cartridge", "check CC package", "verify IMS CC", or "CC validation".
---

# Common Cartridge Validation

Validate IMS Common Cartridge 1.3 packages for specification compliance, structural integrity, and LMS compatibility before delivery.

## When to Use

- Validate CC package before delivery to customer
- Check package after creation
- Verify package will import successfully
- Debug CC import failures
- Quality assurance for CC packages
- Pre-import validation

## Required Inputs

- **CC Package**: .imscc file (ZIP format)
- **Validation Level**: quick, standard, thorough
- **Target LMS** (optional): Canvas, Moodle, Blackboard for platform-specific checks

## Validation Checks

### Level 1: Structure Validation (Quick, 1-2 minutes)

**File Structure:**
- ✓ Package is valid ZIP file
- ✓ imsmanifest.xml exists at root
- ✓ imsmanifest.xml is valid XML
- ✓ No OS-specific files (.DS_Store, Thumbs.db, __MACOSX)
- ✓ No hidden files or directories

**File References:**
- ✓ All files in manifest exist in package
- ✓ No orphaned files (files not referenced in manifest)
- ✓ File paths use forward slashes (not backslashes)
- ✓ File names don't contain special characters

### Level 2: Schema Validation (Standard, 3-5 minutes)

**Manifest Schema:**
- ✓ Valid against IMS CC 1.3 XSD schema
- ✓ Required elements present (metadata, organizations, resources)
- ✓ Namespace declarations correct
- ✓ Schema version specified (1.3.0)
- ✓ Identifier attributes unique

**Metadata:**
- ✓ Schema type: "IMS Common Cartridge"
- ✓ Schema version: "1.3.0"
- ✓ LOM metadata structure valid
- ✓ Title, description present
- ✓ Copyright information included

**Organizations:**
- ✓ At least one organization defined
- ✓ Default organization specified
- ✓ Structure is "rooted-hierarchy"
- ✓ All item identifiers unique
- ✓ All identifierref values reference existing resources

**Resources:**
- ✓ All resource identifiers unique
- ✓ Resource types valid for CC 1.3
- ✓ href attributes point to existing files
- ✓ Dependencies reference existing resources

### Level 3: Content Validation (Thorough, 5-10 minutes)

**QTI Assessments:**
- ✓ Assessment metadata valid (assessment_meta.xml)
- ✓ QTI 2.1 XML valid against schema
- ✓ Item types supported
- ✓ Response processing defined
- ✓ Scoring configured
- ✓ Feedback present (optional but recommended)

**LTI Tools:**
- ✓ LTI configuration XML valid
- ✓ Launch URL present and valid format
- ✓ Secure launch URL (HTTPS) present
- ✓ Vendor information included
- ✓ Privacy level specified
- ✓ Platform extensions valid

**Discussion Topics:**
- ✓ Discussion XML valid against schema
- ✓ Title and text present
- ✓ Discussion type valid (threaded, side_comment)
- ✓ Grading configuration valid (if graded)

**Web Links:**
- ✓ Web link XML valid
- ✓ URL present and valid format
- ✓ Target specified

**Web Content:**
- ✓ HTML files are valid HTML5
- ✓ No broken internal links
- ✓ Images referenced exist
- ✓ CSS files valid
- ✓ JavaScript files don't have syntax errors

### Level 4: Accessibility Validation (Thorough)

**WCAG 2.1 AA Compliance:**
- ✓ All images have alt text
- ✓ Color contrast ratios meet AA standards
- ✓ Headings use semantic HTML (h1, h2, etc.)
- ✓ Links have descriptive text
- ✓ Forms have labels
- ✓ Tables have headers
- ✓ No keyboard traps
- ✓ ARIA labels where appropriate

### Level 5: LMS-Specific Validation (Optional)

**Canvas-Specific:**
- ✓ course-settings.xml valid against Canvas schema
- ✓ Assignment groups configured
- ✓ Module requirements valid
- ✓ LTI tool placements valid

**Moodle-Specific:**
- ✓ Activity types supported
- ✓ Grading scales compatible
- ✓ Resource types recognized

**Blackboard-Specific:**
- ✓ Content types compatible
- ✓ Assessment types supported

## Workflow

### 1. Extract Package

```bash
# Extract .imscc to temporary directory
unzip course.imscc -d /tmp/cc-validate-XXXXX

# Verify structure
ls -la /tmp/cc-validate-XXXXX/
```

**Expected structure:**
```
course/
├── imsmanifest.xml         # Required at root
├── course-settings.xml     # Optional
├── lessons/
├── assessments/
├── discussions/
├── lti-tools/
├── resources/
└── web-links/
```

### 2. Validate Manifest Schema

```bash
# Validate against IMS CC 1.3 XSD
xmllint --noout --schema imscc_v1p3_imscp_v1p2.xsd imsmanifest.xml

# Check for well-formed XML
xmllint --noout imsmanifest.xml
```

**Common Schema Errors:**
- Missing namespace declarations
- Invalid element nesting
- Required attributes missing
- Invalid resource types

### 3. Validate File References

```python
# Pseudocode for reference validation
manifest = parse_xml("imsmanifest.xml")

# Get all file references from manifest
referenced_files = []
for resource in manifest.resources:
    referenced_files.append(resource.href)
    for file in resource.files:
        referenced_files.append(file.href)

# Check all references exist
for file_path in referenced_files:
    if not exists(file_path):
        error(f"Missing file: {file_path}")

# Check for orphaned files
package_files = list_all_files()
for file in package_files:
    if file not in referenced_files and file != "imsmanifest.xml":
        warning(f"Orphaned file (not in manifest): {file}")
```

### 4. Validate QTI Assessments

```bash
# For each QTI assessment
for assessment in assessments/*; do
    # Validate assessment metadata
    xmllint --noout --schema assessment_meta.xsd $assessment/assessment_meta.xml

    # Validate QTI 2.1 XML
    xmllint --noout --schema qtiasiv2p1.xsd $assessment/assessment.xml

    # Check item types
    check_qti_item_types $assessment/assessment.xml
done
```

**QTI Validation Checks:**
- Item types: choice, text_entry, matching, ordering
- Response processing exists
- Correct response defined
- Point values specified
- Feedback present

### 5. Validate LTI Tools

```bash
# For each LTI tool
for tool in lti-tools/*; do
    # Validate LTI XML
    xmllint --noout --schema blti_v1p0.xsd $tool

    # Check required fields
    check_lti_fields $tool
done
```

**LTI Validation Checks:**
- Launch URL present
- Launch URL uses HTTPS (recommended)
- Title present
- Vendor information complete
- Privacy level specified
- Platform extensions valid

### 6. Generate Validation Report

```
Common Cartridge Validation Report
===================================

Package: bio-101-2025.imscc
Validation Date: 2025-11-06T13:30:00Z
Validation Level: Thorough

SUMMARY
-------
Overall Status: PASS ✓
Total Checks: 87
Passed: 85
Warnings: 2
Errors: 0

DETAILED RESULTS
----------------

[✓] Structure Validation (12 checks)
  ✓ Package is valid ZIP
  ✓ imsmanifest.xml exists at root
  ✓ imsmanifest.xml is valid XML
  ✓ No OS-specific files
  ✓ All referenced files exist
  ✓ No orphaned files
  ... (6 more)

[✓] Schema Validation (25 checks)
  ✓ Valid against IMS CC 1.3 XSD
  ✓ Required elements present
  ✓ Namespace declarations correct
  ✓ All identifiers unique
  ... (21 more)

[✓] QTI Assessment Validation (18 checks)
  ✓ 3 assessments found
  ✓ All assessment metadata valid
  ✓ All QTI 2.1 XML valid
  ✓ Response processing defined
  ✓ Scoring configured
  ... (13 more)

[⚠] Accessibility Validation (15 checks)
  ✓ All images have alt text
  ✓ Color contrast ratios meet AA
  ⚠ 2 links have non-descriptive text ("click here")
  ⚠ 1 video missing captions
  ... (11 more)

[✓] LTI Tool Validation (8 checks)
  ✓ 2 LTI tools configured
  ✓ All launch URLs valid
  ✓ All use HTTPS
  ✓ Vendor information complete
  ... (4 more)

WARNINGS (2)
------------
1. lessons/lesson-1-2.html: Link text "click here" is not descriptive (line 42)
2. resources/videos/cell-division.mp4: Video missing caption track

RECOMMENDATIONS
---------------
1. Update link text to be descriptive ("View cell diagram" instead of "click here")
2. Add WebVTT caption file for video: resources/videos/cell-division.vtt
3. Consider adding more feedback to QTI questions (optional)

PACKAGE DETAILS
---------------
Course ID: bio-101-2025
Course Title: Introduction to Biology
Lessons: 8
Assessments: 3 (QTI 2.1)
Discussion Topics: 2
LTI Tools: 2
Resources: 47 files (images, videos, PDFs)

Package Size: 14.2 MB
Extracted Size: 15.8 MB

IMPORT COMPATIBILITY
--------------------
Canvas: ✓ Compatible
Moodle: ✓ Compatible
Blackboard: ✓ Compatible
D2L Brightspace: ✓ Compatible
Schoology: ✓ Compatible

NEXT STEPS
----------
1. ✓ Package is ready for delivery
2. Address 2 accessibility warnings (optional but recommended)
3. Test import in target LMS before final delivery
4. Generate import instructions for customer

Report generated by: curriculum.validate-cc v1.0.0
```

## CLI Interface

```bash
# Quick validation (structure only)
/curriculum.validate-cc --package course.imscc --level quick

# Standard validation (structure + schema)
/curriculum.validate-cc --package course.imscc --level standard

# Thorough validation (all checks)
/curriculum.validate-cc --package course.imscc --level thorough

# With target LMS checks
/curriculum.validate-cc --package course.imscc --level thorough --target-lms canvas

# Generate detailed report
/curriculum.validate-cc --package course.imscc --level thorough --report-file validation-report.txt

# JSON output for automation
/curriculum.validate-cc --package course.imscc --level thorough --format json --output validation.json

# Validate multiple packages
/curriculum.validate-cc --packages "*.imscc" --level standard

# Help
/curriculum.validate-cc --help
```

## Output Formats

### Text Report (Default)

Human-readable validation report with:
- Summary section (pass/fail, counts)
- Detailed results by validation category
- Warnings and errors with line numbers
- Recommendations for fixes
- Import compatibility matrix

### JSON Output

```json
{
  "package": "bio-101-2025.imscc",
  "validation_date": "2025-11-06T13:30:00Z",
  "level": "thorough",
  "summary": {
    "status": "pass",
    "total_checks": 87,
    "passed": 85,
    "warnings": 2,
    "errors": 0
  },
  "structure_validation": {
    "status": "pass",
    "checks": 12,
    "passed": 12
  },
  "schema_validation": {
    "status": "pass",
    "checks": 25,
    "passed": 25
  },
  "qti_validation": {
    "status": "pass",
    "checks": 18,
    "passed": 18,
    "assessments": 3
  },
  "accessibility_validation": {
    "status": "warning",
    "checks": 15,
    "passed": 13,
    "warnings": 2,
    "issues": [
      {
        "type": "warning",
        "file": "lessons/lesson-1-2.html",
        "line": 42,
        "message": "Link text 'click here' is not descriptive",
        "recommendation": "Use descriptive text like 'View cell diagram'"
      },
      {
        "type": "warning",
        "file": "resources/videos/cell-division.mp4",
        "message": "Video missing caption track",
        "recommendation": "Add WebVTT caption file"
      }
    ]
  },
  "lti_validation": {
    "status": "pass",
    "checks": 8,
    "passed": 8,
    "tools": 2
  },
  "compatibility": {
    "canvas": true,
    "moodle": true,
    "blackboard": true,
    "d2l_brightspace": true,
    "schoology": true
  }
}
```

### XML Output

```xml
<validation-report>
  <package>bio-101-2025.imscc</package>
  <summary status="pass">
    <total-checks>87</total-checks>
    <passed>85</passed>
    <warnings>2</warnings>
    <errors>0</errors>
  </summary>
  <structure-validation status="pass"/>
  <schema-validation status="pass"/>
  <qti-validation status="pass"/>
  <accessibility-validation status="warning">
    <issue type="warning" file="lessons/lesson-1-2.html" line="42">
      Link text 'click here' is not descriptive
    </issue>
  </accessibility-validation>
  <lti-validation status="pass"/>
</validation-report>
```

## Common Issues and Fixes

### Issue 1: Invalid Manifest Schema

**Error:**
```
Element '{http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1}manifest':
Missing child element(s). Expected is ( {http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1}organizations ).
```

**Cause:** Missing required `<organizations>` element

**Fix:**
```xml
<manifest>
  <metadata>...</metadata>
  <organizations>
    <organization identifier="org-1" structure="rooted-hierarchy">
      <item identifier="root">
        <title>Course Title</title>
      </item>
    </organization>
  </organizations>
  <resources>...</resources>
</manifest>
```

### Issue 2: Orphaned Files

**Warning:**
```
Orphaned file (not in manifest): resources/images/unused-diagram.png
```

**Cause:** File exists in package but not referenced in manifest

**Fix Options:**
1. Add file to manifest if needed
2. Remove file from package if unused
3. Add to resource dependencies

### Issue 3: Broken File References

**Error:**
```
Missing file: lessons/lesson-5.html (referenced in manifest)
```

**Cause:** Manifest references file that doesn't exist

**Fix:**
- Add the missing file to package
- Or remove reference from manifest
- Check file path spelling (case-sensitive)

### Issue 4: Invalid QTI

**Error:**
```
QTI validation failed: assessments/quiz-1/assessment.xml
Element 'correctResponse': This element is not expected.
```

**Cause:** QTI XML doesn't conform to QTI 2.1 schema

**Fix:**
- Validate QTI against schema
- Use curriculum.export-qti skill to generate valid QTI
- Check IMS QTI 2.1 specification

### Issue 5: LTI Launch URL Issues

**Error:**
```
LTI tool 'Virtual Lab' has HTTP launch URL (HTTPS recommended)
```

**Cause:** LTI tool uses insecure HTTP URL

**Fix:**
```xml
<blti:launch_url>http://example.com/launch</blti:launch_url>
<!-- Change to: -->
<blti:secure_launch_url>https://example.com/launch</blti:secure_launch_url>
```

## Integration with Other Tools

**Before Validation:**
1. Package created with curriculum.package-common-cartridge

**After Validation:**
2. If validation passes → deliver to customer
3. If validation fails → fix issues and re-validate
4. For LMS testing → use cc-validator agent

**Workflow:**
```bash
# 1. Create package
/curriculum.package-common-cartridge --materials "curriculum/" --output "course.imscc"

# 2. Validate package
/curriculum.validate-cc --package "course.imscc" --level thorough

# 3. If pass, test in LMS
/agent.cc-validator --action "test" --package "course.imscc" --lms-targets "canvas,moodle"

# 4. If all tests pass, deliver
cp course.imscc published/bio-101-2025.imscc
```

## Best Practices

### When to Validate

✅ **Always validate:**
- Before delivering to customer
- After package creation
- After fixing validation errors
- Before testing in LMS

✅ **Quick validation good for:**
- During iterative development
- Quick sanity checks
- CI/CD pipelines

✅ **Thorough validation good for:**
- Final QA before delivery
- Customer-facing packages
- High-stakes courses

### Validation Levels

| Level | Time | Use Case |
|-------|------|----------|
| **Quick** | 1-2 min | Development, CI/CD |
| **Standard** | 3-5 min | Pre-testing validation |
| **Thorough** | 5-10 min | Final QA, delivery |

### Handling Warnings

**Accessibility Warnings:**
- High priority - impacts users with disabilities
- Fix before delivery when possible
- Document if cannot fix

**Orphaned Files:**
- Medium priority - wastes storage
- Remove unused files
- Low impact on functionality

**Missing Feedback:**
- Low priority - optional but helpful
- Add feedback when time permits
- Improves learning experience

## Exit Codes

- **0**: Validation passed (no errors)
- **1**: Validation failed (errors found)
- **2**: Validation passed with warnings
- **3**: Invalid package format (not .imscc)
- **4**: Cannot extract package (corrupted ZIP)
- **5**: Missing imsmanifest.xml

## Performance

**Typical Validation Times:**

| Package Size | Quick | Standard | Thorough |
|--------------|-------|----------|----------|
| Small (<5 MB, 5-10 lessons) | 30 sec | 1-2 min | 3-5 min |
| Medium (5-20 MB, 10-30 lessons) | 1 min | 3-5 min | 5-10 min |
| Large (20-100 MB, 30+ lessons) | 2-3 min | 5-10 min | 10-20 min |

## References

- [IMS CC 1.3 Specification](https://www.imsglobal.org/cc/ccv1p3/imscc_profilev1p3-html/)
- [IMS QTI 2.1 Specification](https://www.imsglobal.org/question/qtiv2p1/imsqti_infov2p1.html)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Canvas CC Extensions](https://canvas.instructure.com/doc/api/file.common_cartridge.html)

## See Also

- **curriculum.package-common-cartridge** - Create CC packages
- **curriculum.export-qti** - Generate QTI 2.1 assessments
- **cc-validator agent** - Automated LMS testing
- **PRODUCTION_GUIDE.md** - Complete CC workflows
