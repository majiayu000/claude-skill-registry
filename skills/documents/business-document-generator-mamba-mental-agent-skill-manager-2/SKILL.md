---
name: business-document-generator
description: This skill should be used when the user requests to create professional business documents (proposals, business plans, or budgets) from templates. It provides PDF templates and a Python script for generating filled documents from user data.
---

# Business Document Generator

## Overview

Generate professional business documents (Project Proposals, Business Plans, Annual Budgets) from high-quality PDF templates. Use the bundled Python script to fill templates with user-provided data and output polished PDF documents ready for distribution.

## When to Use This Skill

Activate this skill when the user asks to:
- Create a business proposal or project proposal
- Generate a business plan document
- Develop an annual budget plan
- Create any professional business document based on the available templates
- Fill in business templates with specific data

## Available Document Types

This skill supports three types of professional business documents:

1. **Project Proposal** - Professional proposals for client projects
   - Template: `assets/templates/Professional Proposal Template.pdf`
   - Use case: Pitching projects to clients, stakeholders

2. **Business Plan** - Comprehensive business planning documents
   - Template: `assets/templates/Comprehensive Business Plan Template.pdf`
   - Use case: Startup planning, investor presentations, strategic planning

3. **Annual Budget** - Detailed budget planning documents
   - Template: `assets/templates/Annual Budget Plan Template.pdf`
   - Use case: Financial planning, budget proposals, fiscal year planning

## Quick Start Workflow

### Step 1: Understand User Requirements

Gather information from the user about:
- Document type needed (proposal, business plan, or budget)
- Key data to include (company name, client info, dates, etc.)
- Any specific customization needs

### Step 2: Prepare the Data

Create a JSON file with the document data. Reference the data schemas in `references/document_schemas.md` for field requirements.

**Example for Proposal:**
```json
{
  "title": "Digital Transformation Initiative",
  "subtitle": "A Comprehensive Plan for Acme Corporation",
  "client_org": "Acme Corporation",
  "client_contact": "Jane Smith, CTO",
  "company_name": "TechSolutions Inc.",
  "contact_info": "contact@techsolutions.com",
  "date": "November 3, 2025"
}
```

**Note:** Check `assets/examples/` for complete example JSON files:
- `proposal_example.json`
- `business_plan_example.json`
- `budget_example.json`

### Step 3: Install Dependencies (First Time Only)

The generation script requires Python packages. Install them:

```bash
pip install pypdf reportlab
```

### Step 4: Generate the Document

Run the generation script:

```bash
python3 scripts/generate_document.py <document_type> <data_file> \
  --templates-dir assets/templates \
  --output-dir <output_directory>
```

**Parameters:**
- `<document_type>`: One of `proposal`, `business_plan`, or `budget`
- `<data_file>`: Path to JSON file with document data
- `--templates-dir`: Directory containing PDF templates (default: `assets/templates`)
- `--output-dir`: Where to save generated PDFs (default: `output`)
- `--output-filename`: Optional custom filename

**Example:**
```bash
python3 scripts/generate_document.py proposal my_proposal_data.json \
  --templates-dir assets/templates \
  --output-dir ./generated_docs
```

### Step 5: Deliver the Document

The script outputs a PDF file in the specified output directory. Verify the document was generated successfully and inform the user of the file location.

## Detailed Usage Instructions

### Creating a Project Proposal

1. Collect proposal information:
   - Project title and subtitle
   - Client organization and contact
   - Your company name and contact info
   - Project details (problem, solution, timeline, budget)

2. Create a JSON data file with proposal fields (see `references/document_schemas.md`)

3. Run the script:
   ```bash
   python3 scripts/generate_document.py proposal proposal_data.json \
     --templates-dir assets/templates
   ```

4. Output: Professional PDF proposal with cover page and content sections

### Creating a Business Plan

1. Collect business plan information:
   - Company name and legal structure
   - Mission and vision statements
   - Target market details
   - Financial projections

2. Create a JSON data file with business plan fields

3. Run the script:
   ```bash
   python3 scripts/generate_document.py business_plan plan_data.json \
     --templates-dir assets/templates
   ```

4. Output: Comprehensive business plan PDF template

### Creating an Annual Budget

1. Collect budget information:
   - Fiscal year
   - Company name
   - Budget assumptions (inflation, growth targets)
   - Revenue and expense forecasts

2. Create a JSON data file with budget fields

3. Run the script:
   ```bash
   python3 scripts/generate_document.py budget budget_data.json \
     --templates-dir assets/templates
   ```

4. Output: Annual budget plan PDF with tables and projections

## Important Notes

### Script Functionality

The `scripts/generate_document.py` script:
- Reads PDF templates from the assets directory
- Overlays user data on template pages (primarily cover pages)
- Generates a new PDF with filled information
- Preserves the original template structure and formatting

### Current Limitations

The script currently fills in cover page information (titles, names, dates). The template body content serves as a professional framework that users can follow when creating their documents manually or through other PDF editing tools.

### Extending the Script

To fill additional fields beyond the cover page, the script can be enhanced to:
- Parse form fields in PDFs
- Add text overlays on specific coordinates for each page
- Replace placeholder text programmatically

Modify `scripts/generate_document.py` to add more sophisticated PDF manipulation as needed.

## Data Schema Reference

For detailed information about required and optional fields for each document type, consult:
- `references/document_schemas.md` - Complete data structure documentation

## Example Files

Find complete working examples in `assets/examples/`:
- `proposal_example.json` - Sample project proposal data
- `business_plan_example.json` - Sample business plan data
- `budget_example.json` - Sample budget plan data

Use these as starting templates when creating new documents.

## Troubleshooting

**Import errors when running the script:**
- Install required packages: `pip install pypdf reportlab`

**Template not found:**
- Verify `--templates-dir` points to `assets/templates`
- Check that PDF template files exist in the templates directory

**Generated PDF is blank or missing data:**
- Verify JSON data file is properly formatted
- Check that required fields are present (see `references/document_schemas.md`)

**Need to customize templates:**
- Original templates are in `assets/templates/`
- Modify templates using PDF editing software
- Keep original filenames or update `TEMPLATE_MAP` in the script

## Resources

### scripts/

Contains the Python script for document generation:
- `generate_document.py` - Main document generation script with CLI interface

This script can be executed directly without loading into context for token efficiency. It may be read if modifications or debugging are needed.

### references/

Documentation to reference while working:
- `document_schemas.md` - Complete JSON data structure for all document types

### assets/

Files used in the document generation output:
- `templates/` - Professional PDF templates for each document type
  - `Professional Proposal Template.pdf`
  - `Comprehensive Business Plan Template.pdf`
  - `Annual Budget Plan Template.pdf`
- `examples/` - Sample JSON data files demonstrating proper structure
  - `proposal_example.json`
  - `business_plan_example.json`
  - `budget_example.json`

These templates and examples are not loaded into context but referenced during generation.
