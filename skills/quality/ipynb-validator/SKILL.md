---
name: ipynb-validator
description: Validate Jupyter notebooks (.ipynb files) for production readiness. Checks smart links consistency, layout structure, transition cells with action cards, numbered part flow, cell ordering, and overall quality. Use when validating notebooks, checking notebook structure, testing smart links, verifying action cards, or preparing notebooks for production deployment. Keywords include ipynb validation, notebook structure, smart links, action cards, transitions, part flow, production ready.
---

# Jupyter Notebook Validator

## Purpose

Comprehensive validation of Jupyter notebooks (.ipynb files) to ensure production readiness. Validates smart links, layout structure, transitions, part flow, and overall quality standards.

## When to Use This Skill

Use this skill when you need to:
- Validate a notebook before production deployment
- Check smart link consistency and resolution
- Verify layout structure and organization
- **Ensure all transition cells have action cards** ⚠️ MOST COMMON ISSUE
- Validate numbered part/section flow
- Check cell ordering and completeness
- Assess overall notebook quality
- Prepare notebooks for client or end-user viewing

## ⚠️ Quick Check: Missing Action Cards

**Before running full validation, manually verify:**

1. Find all transition cells (cells with "Part X:", Progress indicator, and 🔵 dots)
2. Check each has `<!-- action-cards -->` marker
3. Verify 3-6 links follow the marker
4. Ensure links use `(#)` placeholder pattern

**This single check catches 80% of validation failures.**

## Validation Categories

### 1. Smart Links Validation

**What it checks:**
- All smart links (`[text](#)`) have matching headings
- No broken links or orphaned references
- Link text matches heading text (case-insensitive, emoji-agnostic)
- Smart links resolve to valid cells
- Action card links are properly formatted

**Expected pattern:**
```markdown
[Link Text](#) → Finds heading containing "Link Text"
```

**Common issues:**
- Link text doesn't match any heading
- Heading was renamed but link wasn't updated
- Typos in link text
- Missing target heading

### 2. Layout Structure

**What it checks:**
- Clear introduction section (hero, TOC, emergency nav)
- Numbered parts/sections in logical order
- Each part has consistent structure:
  - Transition cell (optional but recommended)
  - Part start cell with full title
  - Content cells
  - Part summary cell
- Conclusion section present
- No gaps or missing sections

**Expected structure:**
```
Introduction (Cells 0-N)
→ Transition (optional)
→ Part 1 (Start → Content → Summary)
→ Transition
→ Part 2 (Start → Content → Summary)
...
→ Conclusion
```

### 3. Transition Cells ⚠️ CRITICAL CHECK

**What it checks:**
- Transition cells exist between major parts
- **Each transition MUST have `<!-- action-cards -->` marker** (REQUIRED)
- Action cards have 3-6 links (enforced)
- Action cards link to upcoming content
- Transition text provides context

**Expected pattern:**
```markdown
### Part X: Section Name
**Progress: X of Y** 🔵🔵🔵⚪⚪⚪
**Reading time: N minutes**

Contextual text explaining what's next...

<!-- action-cards -->

- [Topic 1](#)
- [Topic 2](#)
- [Topic 3](#)
```

**⚠️ COMMON FAILURE: Missing Action Cards Marker**

This is the #1 validation failure. Every transition cell between parts MUST include:
1. The `<!-- action-cards -->` HTML comment marker
2. A markdown list of 3-6 links immediately following
3. Each link using the `(#)` placeholder pattern

**Validation will FAIL if:**
- Transition cell lacks `<!-- action-cards -->` marker
- Fewer than 3 action card links
- Action cards not in proper markdown list format

**When transitions are optional:**
- Part flows naturally from previous summary
- First part (follows introduction)
- Conclusion section

### 4. Part Flow Validation

**What it checks:**
- Parts are numbered sequentially (1, 2, 3, ...)
- No missing or duplicate part numbers
- Part summaries come after part content
- Part titles follow consistent format
- Progress indicators are accurate

**Expected title patterns:**
```markdown
### 🌍 Part 1: Topic Name
### 👥Part 2: By Your Role - Subtopic
### 🎯Part 3: By Your Task - Subtopic
```

**Part structure requirements:**
- First cell: Full title with part number
- Middle cells: Clean titles without part prefix
- Last cell: Summary with "You've Completed Part X"

### 5. Cell Ordering

**What it checks:**
- Cells are in logical sequence
- No content cells after summary
- Summaries appear at end of parts
- Transition cells precede part starts
- No orphaned or misplaced cells
- Reference/utility cells placed appropriately
- Part X completion immediately before Part X+1 transition

**Common ordering issues:**
- Summary before content is complete
- Transition after part start
- Content cells out of sequence
- Missing cells in expected flow
- Reference cells (Resources, Bookmarks, Next Steps) between parts
- Completion cells appearing before part content
- Technical detail cells orphaned outside their parent section

**Example of correct flow:**
```
Part 6 Completion Cell
  ↓ immediately adjacent
Part 7 Transition Cell (with action cards)
  ↓
Part 7 Content Cells
  ↓
Part 7 Completion Cell
  ↓ immediately adjacent
Part 8 Transition Cell
```

### 6. Action Cards Quality

**What it checks:**
- `<!-- action-cards -->` marker present
- Marker followed by markdown list
- 3-6 links per action card section
- Links use `(#)` placeholder
- Link text is descriptive and unique
- No duplicate action card sections in same cell

**Quality criteria:**
- Clear, actionable link text
- Links point to major sections
- Balanced number of options (not too few, not too many)
- Consistent formatting

### 7. Production Readiness

**What it checks:**
- Notebook metadata present (title, description, author, etc.)
- Repository URL configured (for .md links)
- No test or placeholder content
- All code cells are appropriate (if any)
- No broken formatting
- File size is reasonable
- JSON structure is valid

**Metadata requirements:**
```json
{
  "metadata": {
    "title": "Notebook Title",
    "description": "Brief description",
    "author": "Author Name",
    "date": "YYYY-MM-DD",
    "version": "X.Y",
    "repo": "https://github.com/user/repo"
  }
}
```

## Validation Workflow

### Step 1: Load and Parse

1. Read notebook JSON file
2. Validate JSON structure
3. Extract all cells
4. Parse cell sources
5. Identify headings and links

### Step 2: Analyze Structure

1. Identify introduction section
2. Find all parts and their boundaries
3. Locate transition cells
4. Map cell relationships
5. Verify overall organization

### Step 3: Validate Links

1. Extract all smart links
2. Build heading index
3. Match links to headings
4. Report unresolved links
5. Check action card links

### Step 4: Check Transitions (CRITICAL)

**This is the most important validation step for missing action cards.**

1. **Find all transition cells** by pattern matching:
   ```python
   def is_transition_cell(source):
       return (
           re.search(r'###.*Part \d+:', source) and
           'Progress:' in source and
           '🔵' in source and
           'Reading time:' in source
       )
   ```

2. **Verify action card markers** (REQUIRED):
   ```python
   has_action_cards = '<!-- action-cards -->' in source
   if not has_action_cards:
       issues.append({
           'severity': 'ERROR',
           'cell': cell_idx,
           'message': f'Part {part_num} transition missing action cards marker'
       })
   ```

3. **Count links per transition** (must be 3-6):
   ```python
   links = re.findall(r'^\s*- \[([^\]]+)\]\(#\)', source, re.MULTILINE)
   if len(links) < 3:
       issues.append({'severity': 'ERROR', 'message': 'Too few action cards'})
   elif len(links) > 6:
       issues.append({'severity': 'WARN', 'message': 'Too many action cards'})
   ```

4. **Validate link targets** - ensure all action card links resolve

5. **Check contextual text** - verify transition has explanatory text before action cards

### Step 5: Verify Part Flow

1. Extract part numbers
2. Check sequential order
3. Verify part structure
4. Validate summaries
5. Check progress indicators

### Step 6: Assess Quality

1. Check metadata completeness
2. Verify repository configuration
3. Review cell ordering
4. Assess content quality
5. Generate quality score

## Common Issues and Fixes

### Issue 1: Broken Smart Links

**Symptom:** Link text doesn't match any heading

**Fix:**
```markdown
# Before (broken)
[Getting Started](#)  → No heading contains "Getting Started"

# After (fixed)
Heading: ### Getting Started Guide
Link: [Getting Started Guide](#)
```

### Issue 2: Missing Transitions

**Symptom:** Part starts immediately after previous summary

**Fix:**
```markdown
# Add transition cell with action cards
Contextual text...

<!-- action-cards -->
- [Topic 1](#)
- [Topic 2](#)
```

### Issue 3: Incorrect Cell Order

**Symptom:** Summary appears before content, or reference cells between parts

**Fix:**
```python
# Reorder cells in notebook JSON
# Example: Move completion cell from index 64 to index 72

cells = notebook['cells']
completion_cell = cells.pop(64)  # Remove from wrong position
cells.insert(72, completion_cell)  # Insert at correct position
```

**Common scenarios:**
- Completion cell before part content → Move to end of part
- Reference cells between parts → Move to end of notebook (before final wrap-up)
- Technical cells outside their section → Move into proper section

### Issue 4: Missing Action Cards

**Symptom:** Transition cell has no `<!-- action-cards -->` marker

**Critical Issue:** This is one of the most common validation failures. Every transition cell between parts MUST have action cards to guide readers.

**Detection Pattern:**
```python
# Identifies transition cells by:
# 1. Contains "Part X:" heading
# 2. Has progress indicator (Progress: X of Y)
# 3. Has progress dots (🔵🔵...)
# 4. Has reading time estimate

# Then checks for:
# - <!-- action-cards --> marker (REQUIRED)
# - 3-6 markdown links after marker
# - Links use (#) placeholder pattern
```

**Fix:**
```markdown
# Before (FAILS validation):
### Part 7: Universal Patterns
**Progress: 7 of 8** 🔵🔵🔵🔵🔵🔵🔵⚪
**Reading time: 2 minutes**

These patterns work everywhere...

# After (PASSES validation):
### Part 7: Universal Patterns
**Progress: 7 of 8** 🔵🔵🔵🔵🔵🔵🔵⚪
**Reading time: 2 minutes**

These patterns work everywhere...

<!-- action-cards -->

- [Beyond EDS](#)
- [Universal Patterns](#)
- [Apply Anywhere](#)
```

**Why this matters:**
- Action cards provide visual navigation
- Helps readers preview upcoming content
- Maintains consistent user experience
- Critical for educational notebooks

### Issue 5: Part Number Gaps

**Symptom:** Parts numbered 1, 2, 4 (missing 3)

**Fix:** Renumber parts sequentially or add missing part

## Testing the Notebook

### Manual Testing

1. Open in VS Code with Jupyter extension
2. Click through all smart links
3. Verify action cards display correctly
4. Check part flow and navigation
5. Test in ipynb-viewer block

### Automated Validation

Use the `/validate-notebook` command:
```bash
/validate-notebook notebook-name.ipynb
```

Output includes:
- Smart link validation results
- Structure analysis
- Transition checks
- Part flow verification
- Overall quality score
- Detailed issue report

## Production Checklist

Before deploying to production:

- [ ] All smart links resolve correctly
- [ ] Structure is complete and logical
- [ ] Transitions have action cards
- [ ] Parts flow sequentially
- [ ] Cells are properly ordered
- [ ] Metadata is complete
- [ ] Repository URL is set
- [ ] No test/placeholder content
- [ ] Formatting is correct
- [ ] File size is reasonable
- [ ] Tested in ipynb-viewer
- [ ] Action cards display correctly
- [ ] Navigation works smoothly
- [ ] Content is final and approved

## Quality Scoring

The validator assigns scores (0-100) in each category:

**Smart Links (0-100):**
- 100: All links resolve perfectly
- 75-99: Minor issues or warnings
- 50-74: Some broken links
- 0-49: Many broken links

**Structure (0-100):**
- 100: Perfect organization
- 75-99: Minor structural issues
- 50-74: Missing sections or gaps
- 0-49: Poor organization

**Transitions (0-100):**
- 100: All transitions present with action cards
- 75-99: Missing some action cards
- 50-74: Some transitions missing
- 0-49: Few or no transitions

**Part Flow (0-100):**
- 100: Perfect sequential flow
- 75-99: Minor numbering issues
- 50-74: Gaps or duplicates
- 0-49: Major flow problems

**Overall (0-100):**
- 90-100: Production ready
- 75-89: Minor fixes needed
- 60-74: Moderate issues
- 0-59: Major rework required

## Best Practices

### For Smart Links

✅ Use descriptive, unique link text
✅ Keep link text consistent with headings
✅ Test all links before deployment
✅ Use emojis in headings (they're ignored in matching)

❌ Don't use generic link text like "Click here"
❌ Don't hardcode cell IDs like `#cell-5`
❌ Don't create circular link references

### For Cell Ordering

✅ Validate cell order with structural checks:
```python
# Check adjacency between key sections
part_completion_idx < part_transition_idx + 1  # Must be adjacent
part_transition_idx < next_part_start_idx  # Proper sequence
```

✅ Place reference/utility cells strategically:
- Resources & Quick Reference → End of notebook
- Essential Bookmarks → End of notebook
- Troubleshooting → End of notebook
- "What's Next" → End of notebook

✅ Keep technical detail cells within their parent section:
- Code examples belong in "How This Works" section
- Implementation details stay with their topic
- Don't orphan detail cells between major parts

❌ Don't place utility cells between parts
❌ Don't split sections with unrelated content
❌ Don't place completion cells before content

### For Transitions

✅ Provide contextual text explaining what's next
✅ Include 3-6 action cards per transition
✅ Link to major upcoming sections
✅ Use consistent formatting

❌ Don't skip transitions between major parts
❌ Don't have too many action cards (> 6)
❌ Don't have too few action cards (< 3)

### For Part Flow

✅ Number parts sequentially
✅ Use consistent title format
✅ Place summaries at end of parts
✅ Keep part structure uniform

❌ Don't skip part numbers
❌ Don't change title format mid-notebook
❌ Don't place summaries before content

## Related Files

- `.claude/commands/validate-notebook.md` - Command implementation
- `blocks/ipynb-viewer/README.md` - Viewer documentation
- `docs/for-ai/explaining-educational-notebooks.md` - Notebook creation guide
- `docs/for-ai/explaining-presentation-notebooks.md` - Presentation notebooks

## Validation Output Format

The validator produces a detailed report:

```
NOTEBOOK VALIDATION REPORT: notebook-name.ipynb
================================================================

SUMMARY:
  Total Cells: 66
  Smart Links: 51 (51 valid, 0 broken)
  Parts: 7 (sequential)
  Transitions: 6 (all with action cards)
  Overall Score: 95/100 ✅ PRODUCTION READY

SMART LINKS: ✅ PASS
  ✓ All 51 smart links resolve correctly
  ✓ No broken or orphaned links
  ✓ Action card links validated

STRUCTURE: ✅ PASS
  ✓ Clear introduction section (8 cells)
  ✓ 7 parts with consistent structure
  ✓ Conclusion section present
  ✓ No gaps or missing sections

TRANSITIONS: ✅ PASS
  ✓ 6 transition cells with action cards
  ✓ Part 6 flows naturally (no transition needed)
  ✓ All action cards have 3-6 links
  ✓ Contextual text present

PART FLOW: ✅ PASS
  ✓ Parts numbered 1-7 sequentially
  ✓ No gaps or duplicates
  ✓ Summaries at end of each part
  ✓ Consistent title format

CELL ORDERING: ✅ PASS
  ✓ All cells in logical sequence
  ✓ Summaries after content
  ✓ Transitions before parts
  ✓ No orphaned cells

PRODUCTION READINESS: ✅ PASS
  ✓ Metadata complete
  ✓ Repository URL set
  ✓ No test content
  ✓ Valid JSON structure
  ✓ Appropriate file size

RECOMMENDATIONS:
  • Notebook is ready for production deployment
  • All validation checks passed
  • Quality score: 95/100
```

---

**Note:** This validator is designed for educational and navigation notebooks. Testing notebooks (test.ipynb) may have different structure requirements and are validated separately.
