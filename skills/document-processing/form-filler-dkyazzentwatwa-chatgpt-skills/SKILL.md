---
name: form-filler
description: Fill PDF forms programmatically with data from JSON, CSV, or dictionaries. Support for text fields, checkboxes, and dropdowns. Batch filling available.
---

# Form Filler

Fill PDF forms programmatically with structured data.

## Features

- **Field Detection**: Auto-detect form fields
- **Multiple Field Types**: Text, checkbox, dropdown, radio
- **Data Sources**: JSON, CSV, dictionary input
- **Batch Filling**: Fill multiple forms from data file
- **Field Mapping**: Map data keys to field names
- **Flatten Option**: Convert to non-editable PDF
- **Form Info**: List all fields and their types

## Quick Start

```python
from form_filler import FormFiller

filler = FormFiller()

# Load form
filler.load("application_form.pdf")

# Fill fields
filler.fill({
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2024-01-15",
    "agree": True  # Checkbox
})

# Save filled form
filler.save("filled_form.pdf")
```

## CLI Usage

```bash
# Fill from JSON data
python form_filler.py --input form.pdf --data data.json --output filled.pdf

# List form fields
python form_filler.py --input form.pdf --list-fields

# Fill from CSV (batch)
python form_filler.py --input form.pdf --batch data.csv --output-dir filled/

# Flatten filled form
python form_filler.py --input form.pdf --data data.json --flatten --output filled.pdf

# With field mapping
python form_filler.py --input form.pdf --data data.json --mapping mapping.json -o filled.pdf
```

## API Reference

### FormFiller Class

```python
class FormFiller:
    def __init__(self)

    # Loading
    def load(self, filepath: str) -> 'FormFiller'

    # Field Operations
    def list_fields(self) -> List[Dict]
    def get_field_info(self, field_name: str) -> Dict
    def get_field_value(self, field_name: str) -> Any

    # Filling
    def fill(self, data: Dict) -> 'FormFiller'
    def fill_field(self, name: str, value: Any) -> 'FormFiller'
    def fill_from_json(self, filepath: str) -> 'FormFiller'
    def fill_from_csv_row(self, row: Dict) -> 'FormFiller'

    # Field Mapping
    def set_mapping(self, mapping: Dict[str, str]) -> 'FormFiller'

    # Output
    def save(self, filepath: str, flatten: bool = False) -> str
    def flatten(self) -> 'FormFiller'

    # Batch Processing
    def batch_fill(self, input_form: str, data_file: str,
                  output_dir: str) -> List[str]
```

## Field Types

### Text Fields
```python
filler.fill({
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Main St"
})
```

### Checkboxes
```python
filler.fill({
    "agree_terms": True,
    "subscribe": False
})
```

### Radio Buttons
```python
filler.fill({
    "gender": "male",  # Value of selected option
    "payment_method": "credit_card"
})
```

### Dropdowns
```python
filler.fill({
    "country": "USA",
    "state": "California"
})
```

## Field Discovery

```python
fields = filler.list_fields()
# Returns:
# [
#     {"name": "first_name", "type": "text", "required": True},
#     {"name": "agree_terms", "type": "checkbox", "value": False},
#     {"name": "country", "type": "dropdown", "options": ["USA", "Canada", "UK"]}
# ]
```

## Field Mapping

Map data keys to form field names:

```python
filler.set_mapping({
    "fname": "first_name",     # data key -> form field
    "lname": "last_name",
    "addr": "address_line_1"
})

filler.fill({
    "fname": "John",           # Uses mapping
    "lname": "Doe"
})
```

## Batch Filling

### From CSV
```python
# CSV format:
# first_name,last_name,email
# John,Doe,john@example.com
# Jane,Smith,jane@example.com

filler.batch_fill(
    input_form="application.pdf",
    data_file="applicants.csv",
    output_dir="filled_forms/"
)
# Creates: filled_forms/application_0.pdf, application_1.pdf, ...
```

### From JSON Array
```python
# JSON format:
# [
#     {"first_name": "John", "last_name": "Doe"},
#     {"first_name": "Jane", "last_name": "Smith"}
# ]

filler.batch_fill(
    input_form="form.pdf",
    data_file="data.json",
    output_dir="output/"
)
```

## Dependencies

- PyMuPDF>=1.23.0
- pillow>=10.0.0
- pandas>=2.0.0
