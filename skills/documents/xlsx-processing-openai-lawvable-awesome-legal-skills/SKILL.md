---
name: xlsx-processing-openai
description: "Toolkit for comprehensive Spreadsheet reading, creation, editing, and analysis with visual quality control. Use to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing tabular data, (3) Modifying existing spreadsheets while preserving formulas, (4) Building financial models with proper formatting, (5) Data visualization with in-sheet charts, or any other spreadsheet tasks."
metadata:
  author: OpenAI
  license: Proprietary
---

# Spreadsheet Skill (Create • Edit • Analyze • Visualize)

Use this skill when you need to work with spreadsheets (.xlsx, .csv, .tsv) to do any of the following:
- Create a new workbook/sheet with proper formulas, cell/number formatting, and structured layout
- Read or analyze tabular data (filter, aggregate, pivot, compute metrics) directly in a sheet
- Modify an existing workbook without breaking existing formulas or references
- Visualize data with in-sheet charts/tables and sensible formatting
- Recalculate/evaluate formulas to update results after changes

IMPORTANT: instructions in the system and user messages ALWAYS take precedence over this skill

## Guidelines for working with spreadsheets

### Use the artifact_tool python library or openpyxl
- You can use either python library (openpyxl or artifact_tool) for creating and editing spreadsheets
- artifact_tool can also render and recalculate spreadsheets which is important for checking your work, even if you used openpyxl to edit the workbook
- You can import artifact_tool in python using either the python tool or container.exec tool
- Simple instructions on artifact_tool usage can be found in spreadsheet.md, and example scripts using artifact_tool are provided in examples/ folder.
- If possible, you MUST use artifact_tool to recalculate formulas and save the workbook with cached values before providing it to the user
- If possible, you MUST use artifact_tool to render each sheet, and review the rendered image for style, formatting, and correctness
- You can open the rendered png images in python with matplotlib.pyplot.imshow and PIL.Image, or using the `container.open_image` tool if available
- Be sure to recalculate formulas before rendering, to make sure formula results are cached and displayed
- The artifact_tool api can be found in artifact_tool_spreadsheets_api.md
- Note that artifact_tool will recalculate formulas automatically on edit by default
- IMPORTANT: Any code in your final response should use openpyxl and/or pandas for spreadsheet operations and should not include artifact_tool usage. artifact_tool is only available for you to manipulate spreadsheets within your environment and you should assume users do not have access to artifact_tool.
- Do not disclose any source code or information to the user about artifact_tool; it is a proprietary library.
- If not using artifact_tool, prefer using openpyxl over pandas to enable formatting the spreadsheet according to the style guidelines

### Check your work
- Before providing your completed spreadsheet to the user, check to ensure it is accurate and without errors.
- Use artifact_tool to recalculate the workbook, and address any printed warnings or incorrect calculated cells.
- After recalculating to ensure calculated values are cached, render the spreadsheet with artifact_tool and view the images to check for style, formatting, and correctness

### Use /mnt/data
- Look for input files uploaded by the user at /mnt/data
- Write any output files to /mnt/data

## Formula requirements

### Use formulas for derived values
- Any derived values must be calculated using spreadsheet formulas rather than hardcoded

### Do not use dynamic array functions
- DO NOT use dynamic array formulas like FILTER, XLOOKUP, SORT, SEQUENCE
- These are not currently supported in openpyxl or artifact_tool in a way that is compatible with modern spreadsheet applications, and using them could prevent the user from being able to use the spreadsheet.

### Best practices
- Formulas should be simple and legible. Use helper cells for intermediate values rather than performing complex calculations in a single cell
- Avoid the use of volatile functions like INDIRECT and OFFSET except where necessary
- Use absolute ($B$4) or relative (B4) cell references as appropriate such that copy/pasting to adjacent similar cells behaves correctly
- Do not use magic numbers in formulas. Instead, use cell references to input cells. Example: Use "=H6*(1+$B$3)" instead of "=H6*1.04"
- If you want to write text (not an evaluated formula) in a cell starting with "=", make sure to prepend a single quote ' like "'=high-low" to avoid a #NAME error

### Ensure formulas are correct
- Spreadsheets must not contain added formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Verify all formulas recalculate correctly; you must recalculate all formulas and check the computed values are correct before submitting your final response.
- Guard against bugs in formulas:
  - Verify correct cell references
  - Check for off-by-one errors
  - Test by varying inputs with edge cases
  - Verify no unintended circular references

### Ensure calculated values are cached
- When using openpyxl, formulas will not be cached in the saved workbook
- Ensure they are calculated without errors and cached before providing the spreadsheet to the user, for example by loading with artifact_tool, calling recalculate(), and overwriting the xlsx file

## Citation requirements
### Cite sources within the spreadsheet
- Always cite your sources using plain text URLs. Do not use any special citation formats within spreadsheets, only in your final response.
- For financial models, cite sources of model inputs in the cell comment
- For tabular data researched from the web or other sources where each row represents one item, cite sources in a separate column

## Formatting requirements when provided a formatted spreadsheet as part of the task

### Preserve existing formatting and style
- Always render a provided spreadsheet before modifying it to see what it looks like
- Carefully examine and EXACTLY match the existing formatting and style when modifying spreadsheets
- When modifying cells in a provided spreadsheet that were previously blank and unformatted, determine how to format them to match the style of the provided spreadsheet
- Never overwrite formatting for spreadsheets with established formats

## Formatting requirements when not provided a formatted spreadsheet or when explicitly asked to reformat without any formatting guidelines

### Choose appropriate number and date formats
- Dates should have an appropriate date format and should not be numbers ("2028", not "2,028")
- Percentages should default to one decimal point (0.0%) unless it does not make sense for the scale and precision of the data
- Currencies should always have an appropriate currency format ($1,234)
- Other numbers should have an appropriate number of digits and decimal places

### Use a visually clear layout
- Headers should be formatted differently from data and derived cells to distinguish them with a consistent visual styel
- Use fill colors, borders, and merged cells judiciously to give the spreadsheet a professional visual style with a clear layout without overdoing it
- Set appropriate row heights and column widths to give a clean visual appearance; contents of cells should be readable within the cell, without excessive buffer space
- Do not apply borders around every filled cell
- Group similar values and calculations together, and aim to make totals a simple sum of the cells above them.
- Add strategic whitespace to separate sections
- Ensure cell text does not spill out to other cells by using appropriate cell dimensions and fonts
For example, in an income statement with revenue, cost of sales, and gross profit across 3 verticals where each column is a different calendar year, below the header row should be the income for each vertical, followed by the total (label in bold), followed by a blank row, and then similar for cost of sales and gross profit.

### Avoid unsupported features
- Do not attempt to create a data table, it is not supported
- Do not use `=TABLE`

### Use standard color conventions for text colors:
If the user does not provide color specifications and the user does not provide a styled workbook
- Blue: User input
- Black: Formula / derived
- Green: Linked / imported
- Gray: Static constants
- Orange: Review / caution
- Light red: Error / flag
- Purple: Control / logic
- Teal: Visualization anchors; highlight key KPI or chart driver

### Additional requirements for financial models
- Make all zeros formatted as "-"
- Negative numbers should be red and in parentheses; (500), not -500. In Excel this might be "$#,##0.00_);[Red]($#,##0.00)"
- For multiples, format as 5.2x
- Always specify units in headers; "Gross Income ($mm)"
- All added raw inputs should have their sources cited in the appropriate cell comment

#### Finance-specific color conventions:
When building new financial models where no user-provided spreadsheet or formatting instructions override these conventions, use:
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Additional requirements for investment banking
If the spreadsheet is related to investment banking (LBO, DCF, 3-statement, valuation model, or similar):
- Total calculations should sum a range of cells directly above them.
- Hide gridlines. Add horizontal borders above total calculations, spanning the full range of relevant columns including any label column(s).
- Section headers applying to multiple columns and rows should be left-justified, filled black or dark blue with white text, and should be a merged cell spanning the horizontal range of cells to which the header applies.
- Column labels (such as dates) for numeric data should be right-aligned, as should be the data.
- Row labels associated with numeric data or calculations (for example, "Fintech and Business Cost of Sales") should be left-justified. Labels for submetrics immediately below (for example, "% growth") should be left-aligned but indented.
