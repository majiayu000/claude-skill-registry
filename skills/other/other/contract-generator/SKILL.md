---
name: contract-generator
description: Use when asked to generate legal contracts, agreements, or documents from templates with variable substitution and formatting.
---

# Contract Generator

Generate professional legal contracts and agreements from templates with variable substitution, formatting, and validation.

## Purpose

Contract generation for:
- Employment agreements and NDAs
- Service contracts and SOWs
- Sales and purchase agreements
- Lease and rental contracts
- Partnership and operating agreements

## Features

- **Template System**: Pre-built contract templates
- **Variable Substitution**: Replace placeholders with actual values
- **Conditional Sections**: Include/exclude based on variables
- **Formatting**: Professional DOCX output
- **Validation**: Check for missing required fields
- **Batch Generation**: Create multiple contracts from CSV

## Quick Start

```python
from contract_generator import ContractGenerator

# Generate from template
generator = ContractGenerator()
generator.load_template('templates/nda.docx')
generator.set_variables({
    'party1_name': 'Acme Corp',
    'party2_name': 'John Smith',
    'effective_date': '2024-03-14',
    'jurisdiction': 'California'
})
generator.save('nda_acme_smith.docx')
```

## CLI Usage

```bash
# Generate single contract
python contract_generator.py --template nda.docx --vars vars.json --output contract.docx

# Batch generate from CSV
python contract_generator.py --template nda.docx --csv parties.csv --output-dir contracts/
```

## Limitations

- Templates must be in DOCX format
- Not a substitute for legal review
- Does not provide legal advice
- Complex conditional logic may require custom templates
