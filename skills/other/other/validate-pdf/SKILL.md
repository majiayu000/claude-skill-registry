---
description: Generate and validate PDF structure (30 days + shopping lists + macros)
handoffs:
  - label: Fix PDF Generation
    agent: pdf-designer
    prompt: Fix the PDF generation issues identified
    send: false
---

## User Input

```text
$ARGUMENTS
```

Options: meal plan JSON file path or use test fixture

## Task

Generate a PDF from meal plan data and validate structure, file size, and visual layout.

### Steps

1. **Load Test Meal Plan**:
   ```bash
   cd backend

   # Use test fixture or provided file
   MEAL_PLAN_FILE="${ARGUMENTS:-tests/fixtures/test_meal_plan_weight_loss.json}"

   python -c "
   import json
   with open('${MEAL_PLAN_FILE}') as f:
       meal_plan = json.load(f)
   print(f'✅ Meal plan loaded: {len(meal_plan[\"days\"])} days')
   "
   ```

2. **Generate PDF**:
   ```bash
   python -c "
   from src.services.pdf_generator import generate_pdf
   import json

   with open('${MEAL_PLAN_FILE}') as f:
       meal_plan = json.load(f)

   pdf_path = generate_pdf(meal_plan, 'test_output.pdf')
   print(f'✅ PDF generated: {pdf_path}')
   "
   ```

3. **Validate File**:
   ```bash
   # Check file exists and has content
   if [ -f "test_output.pdf" ]; then
       FILE_SIZE=$(stat -f%z "test_output.pdf" 2>/dev/null || stat -c%s "test_output.pdf")
       echo "✅ PDF file created: ${FILE_SIZE} bytes"

       # Expected size: 400-600 KB
       if [ $FILE_SIZE -lt 400000 ]; then
           echo "⚠️ File size too small (< 400KB)"
       elif [ $FILE_SIZE -gt 600000 ]; then
           echo "⚠️ File size too large (> 600KB)"
       else
           echo "✅ File size in expected range (400-600KB)"
       fi
   else
       echo "❌ PDF file not generated"
   fi
   ```

4. **Validate PDF Structure**:
   ```bash
   python -c "
   from PyPDF2 import PdfReader

   reader = PdfReader('test_output.pdf')
   num_pages = len(reader.pages)

   print(f'📄 Total Pages: {num_pages}')

   # Expected: Cover + 30 days + 4 shopping lists = ~35 pages
   if num_pages < 30:
       print('❌ Too few pages (expected ~35)')
   elif num_pages > 50:
       print('⚠️ Too many pages (expected ~35)')
   else:
       print('✅ Page count looks good')

   # Check first page text
   first_page = reader.pages[0].extract_text()
   if 'Keto Meal Plan' in first_page:
       print('✅ Cover page detected')
   else:
       print('⚠️ Cover page may be missing')
   "
   ```

5. **Visual Validation** (open PDF):
   ```bash
   # Open PDF for manual inspection
   if command -v open &> /dev/null; then
       open test_output.pdf
   elif command -v xdg-open &> /dev/null; then
       xdg-open test_output.pdf
   else
       echo "PDF saved to: $(pwd)/test_output.pdf"
   fi
   ```

6. **Check Required Elements**:
   - ✅ Cover page with green theme (#22c55e)
   - ✅ 30 daily meal plans with breakfast, lunch, dinner
   - ✅ Macronutrient breakdown per meal
   - ✅ 4 weekly shopping lists
   - ✅ Ingredient quantities
   - ✅ Prep times (<30 min per meal)

7. **Output Summary**:
   ```
   ✅ PDF Validation Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Source: tests/fixtures/test_meal_plan_weight_loss.json

   Generation:
   ✅ PDF created successfully
   ⏱️  Generation time: 3.2s (target: <20s)

   File Properties:
   ✅ File size: 487 KB (target: 400-600KB)
   ✅ Pages: 36 (expected: ~35)
   ✅ PDF format valid

   Structure Check:
   ✅ Cover page present
   ✅ 30 daily meal plans
   ✅ 4 weekly shopping lists
   ✅ Macronutrient tables included

   Visual Check:
   📂 PDF opened for manual review
   → Verify: Green theme, readability, layout

   Recommendation: ✅ PDF meets quality standards
   ```

## Example Usage

```bash
/validate-pdf                                        # Use default test fixture
/validate-pdf tests/fixtures/test_meal_plan_muscle_gain.json
```

## Exit Criteria

- PDF generated from meal plan data
- File size within 400-600KB range
- Structure validated (pages, cover, meals, shopping lists)
- PDF opened for visual inspection
