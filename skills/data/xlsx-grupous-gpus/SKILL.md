---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. Provides intelligent header detection and semantic column mapping for robust data import."
license: Proprietary. LICENSE.txt has complete terms
---

# Intelligence Capabilities (New)

When working with imperfect input files (e.g., user uploads, legacy system exports), apply the following intelligent processing strategies.

## 1. Intelligent Header Detection
**Full Guide**: [header-detection.md](intelligence/header-detection.md)

Never assume the first row is the header. Use the following heuristics:
- **Semantic Analysis**: Look for row content matching known keywords using Levenshtein distance (e.g., "Telefome" ≈ "Telefone").
- **Data Pattern Analysis**: The header is typically the last text-heavy row before data-heavy rows (dates, emails, CPFs).
- **Context**: Headers have high density (few empty cells) and are often below metadata rows (titles, dates).

## 2. Semantic Column Mapping
**Full Guide**: [column-mapping.md](intelligence/column-mapping.md)

Map source columns to target fields using specific scoring:
- **Semantic (40%)**: Normalization + Synonyms (e.g., "Zap" -> "Phone").
- **Pattern (30%)**: Data validation samples (e.g., column has `\d{11}` -> "CPF").
- **Context (30%)**: Position and frequency of occurrence.

## 3. Real-World Examples
**See**: [examples.md](intelligence/examples.md) for handling:
- Metadata headers (Reports with titles)
- Ambiguous columns (Date formats)
- Unknown columns

---

# Requirements for Outputs

## All Excel files

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards
Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Number Formatting Standards

#### Required Format Rules
- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

### Formula Construction Rules

#### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

#### Formula Error Prevention
- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

#### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

# XLSX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.

## Important Requirements

**LibreOffice Required for Formula Recalculation**: You can assume LibreOffice is installed for recalculating formula values using the `recalc.py` script. The script automatically configures LibreOffice on first run

## Reading and analyzing data

### Data analysis with pandas
For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Excel File Workflows

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.

### ❌ WRONG - Hardcoding Calculated Values
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### ✅ CORRECT - Using Excel Formulas
```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

This applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.

## Common Workflow
1. **Choose tool**: pandas for data, openpyxl for formulas/formatting
2. **Create/Load**: Create new workbook or load existing file
3. **Modify**: Add/edit data, formulas, and formatting
4. **Save**: Write to file
5. **Recalculate formulas (MANDATORY IF USING FORMULAS)**: Use the recalc.py script
   ```bash
   python recalc.py output.xlsx
   ```
6. **Verify and fix any errors**:
   - The script returns JSON with error details
   - If `status` is `errors_found`, check `error_summary` for specific error types and locations
   - Fix the identified errors and recalculate again
   - Common errors to fix:
     - `#REF!`: Invalid cell references
     - `#DIV/0!`: Division by zero
     - `#VALUE!`: Wrong data type in formula
     - `#NAME?`: Unrecognized formula name

### Creating new Excel files

```python
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editing existing Excel files

```python
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## Recalculating formulas

Excel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `recalc.py` script to recalculate formulas:

```bash
python recalc.py <excel_file> [timeout_seconds]
```

Example:
```bash
python recalc.py output.xlsx 30
```

The script:
- Automatically sets up LibreOffice macro on first run
- Recalculates all formulas in all sheets
- Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.)
- Returns JSON with detailed error locations and counts
- Works on both Linux and macOS

## Formula Verification Checklist

Quick checks to ensure formulas work correctly:

### Essential Verification
- [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model
- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK)
- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)

### Common Pitfalls
- [ ] **NaN handling**: Check for null values with `pd.notna()`
- [ ] **Far-right columns**: FY data often in columns 50+
- [ ] **Multiple matches**: Search all occurrences, not just first
- [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!)
- [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!)
- [ ] **Cross-sheet references**: Use correct format (Sheet1!A1) for linking sheets

### Formula Testing Strategy
- [ ] **Start small**: Test formulas on 2-3 cells before applying broadly
- [ ] **Verify dependencies**: Check all cells referenced in formulas exist
- [ ] **Test edge cases**: Include zero, negative, and very large values

### Interpreting recalc.py Output
The script returns JSON with error details:
```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## Best Practices

### Library Selection
- **pandas**: Best for data analysis, bulk operations, and simple data export
- **openpyxl**: Best for complex formatting, formulas, and Excel-specific features

### Working with openpyxl
- Cell indices are 1-based (row=1, column=1 refers to cell A1)
- Use `data_only=True` to read calculated values: `load_workbook('file.xlsx', data_only=True)`
- **Warning**: If opened with `data_only=True` and saved, formulas are replaced with values and permanently lost
- For large files: Use `read_only=True` for reading or `write_only=True` for writing
- Formulas are preserved but not evaluated - use recalc.py to update values

### Working with pandas
- Specify data types to avoid inference issues: `pd.read_excel('file.xlsx', dtype={'id': str})`
- For large files, read specific columns: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- Handle dates properly: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## Code Style Guidelines
**IMPORTANT**: When generating Python code for Excel operations:
- Write minimal, concise Python code without unnecessary comments
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

**For Excel files themselves**:
- Add comments to cells with complex formulas or important assumptions
- Document data sources for hardcoded values
- Include notes for key calculations and model sections

---

# Intelligent Spreadsheet Import and Analysis

## Overview

When importing or analyzing spreadsheets, especially for data import workflows, intelligent detection and mapping capabilities are essential for handling real-world spreadsheets that may have:
- Non-standard layouts (metadata rows, empty rows, merged cells)
- Varied column naming (synonyms, abbreviations, typos)
- Multiple data types requiring pattern recognition
- Contextual relationships between columns

This section provides advanced techniques for intelligent header detection, column mapping, and data pattern analysis.

---

## Intelligent Header Detection

### Overview

Header detection is the process of identifying which row in a spreadsheet contains the column names. Real-world spreadsheets often have:
- Title rows or metadata at the top
- Empty separator rows
- Multi-line headers (merged cells)
- Headers that don't start at row 1

### Detection Strategy: Multi-Factor Analysis

Use a combination of semantic analysis, pattern recognition, and contextual clues to identify headers with high confidence.

#### 1. Semantic Analysis

**String Similarity Algorithms**

Use similarity metrics to compare row cells against known header keywords. Implement Levenshtein distance, Jaro-Winkler similarity, and normalization functions to handle:
- Accent removal (á → a)
- Case insensitivity
- Whitespace normalization
- Synonym matching

**Synonym Recognition**

Maintain a knowledge base of header synonyms and variations in multiple languages (Portuguese, English) and handle:
- Regional variations ("celular" vs "móvel")
- Common typos ("E-mail" vs "Email")
- Abbreviations ("Tel" = "Telefone")
- Context-dependent names ("Cliente" = "Nome" in CRM context)

#### 2. Pattern-Based Data Type Detection

Analyze sample data values (first 5-10 rows) to infer column types:
- **CPF**: 11 digits, format XXX.XXX.XXX-XX
- **Email**: Contains @ and valid domain
- **Phone**: 10-11 digits, Brazilian formats
- **Date**: Multiple formats (DD/MM/YYYY, MM/DD/YYYY, Excel serial)
- **Monetary**: R$, points, commas (Brazilian format)
- **CEP**: 8 digits, format XXXXX-XXX

Use pattern matching with regex and validation functions to detect types with confidence scores.

#### 3. Contextual Analysis

Consider multiple contextual factors:
- **Position**: Headers usually in first 5 rows
- **Density**: Headers have many filled cells
- **Consistency**: Headers are text, data rows vary in type
- **Structure**: Headers have similar length/format

### Multi-Factor Scoring

Calculate header likelihood score using:
- Text ratio (30%): Headers are usually text, not numbers
- Keyword matches (40%): Match against known header keywords
- Fill ratio (20%): Headers usually have many filled cells
- Position bonus (10%): Headers usually in first rows

### Thresholds and Confidence Levels

- **Confidence ≥ 0.8**: High confidence - use automatically
- **Confidence 0.6-0.8**: Medium confidence - show to user for confirmation
- **Confidence < 0.6**: Low confidence - require user selection

### Handling Edge Cases

- **Multiple Header Rows**: Detect merged cells spanning multiple rows
- **Empty Rows**: Skip empty separator rows before data
- **Metadata Rows**: Identify and skip title/metadata rows at top

---

## Intelligent Column Mapping

### Overview

Column mapping matches spreadsheet column names to system fields. Real-world spreadsheets use varied naming that requires intelligent matching.

### Multi-Factor Scoring System

Use weighted scoring to determine best mapping:

- **Semantic Similarity (40%)**: String similarity and synonym matching
- **Data Pattern Match (30%)**: Type inferred from actual values
- **Position Context (15%)**: Expected position of field
- **Frequency/Common Name (15%)**: Most common names get priority

### Expanded Knowledge Base

Maintain comprehensive synonym mappings including:
- Portuguese and English variations
- Regional differences
- Common typos and abbreviations
- Context-dependent synonyms

**Example Knowledge Base Structure:**

```python
# Comprehensive header knowledge base for student/CRM imports
EXPANDED_HEADER_KNOWLEDGE = {
    # Name variations (regional, typos, languages)
    'name': [
        # Portuguese standard
        'nome', 'nome completo', 'aluno', 'cliente', 'pessoa',
        'nome do aluno', 'nome do cliente', 'razao social', 'razão social',
        # English
        'name', 'full name', 'client name', 'student name', 'person', 'fullname',
        # Abbreviations
        'nm', 'nome compl', 'nome compl.',
        # Common typos
        'nme', 'nomee', 'nom', 'nomes',
        # Context variations
        'cadastro', 'registro', 'identificação'
    ],

    # Email variations
    'email': [
        # Portuguese
        'email', 'e-mail', 'correio eletrônico', 'correio eletronico',
        'correio', 'endereço de email', 'endereco de email', 'endereço email',
        # English
        'mail', 'e-mail address', 'email address', 'mail address',
        # Abbreviations
        'e-mail', 'mail addr', 'email addr',
        # Common typos
        'emial', 'emal', 'eail', 'emai',
        # Variations
        'correio eletrônico', 'correio eletr.'
    ],

    # Phone variations
    'phone': [
        # Portuguese
        'telefone', 'celular', 'whatsapp', 'contato', 'telefone celular',
        'telefone fixo', 'fone', 'tel', 'telefone residencial',
        # English
        'phone', 'mobile', 'cell phone', 'telephone', 'contact number',
        'mobile phone', 'cell',
        # Regional
        'móvel', 'movel', 'cel',
        # Abbreviations
        'tel', 'fone', 'cel', 'whats', 'wpp',
        # Common typos
        'telefne', 'telefonee', 'celularr'
    ],

    # CPF variations
    'cpf': [
        'cpf', 'documento', 'documento cpf', 'cpf/cnpj', 'cpf cnpj',
        'identificação', 'identificacao', 'id', 'rg', 'documento de identidade',
        'doc', 'document', 'identifier', 'cpf cnpj', 'documento único',
        'documento unico', 'cpf documento', 'número cpf', 'numero cpf'
    ],

    # Address variations
    'address': [
        'endereço', 'endereco', 'rua', 'logradouro', 'street', 'address',
        'endereço completo', 'endereco completo', 'full address', 'endereço residencial',
        'endereco residencial', 'logradouro completo', 'rua endereço'
    ],

    'addressNumber': [
        'número', 'numero', 'nº', 'n°', 'num', 'número do endereço',
        'numero do endereco', 'address number', 'house number', 'nro'
    ],

    'complement': [
        'complemento', 'complement', 'apto', 'apartamento', 'bloco',
        'bloco apto', 'andar', 'sala', 'complemento endereço'
    ],

    'neighborhood': [
        'bairro', 'neighborhood', 'distrito', 'bairro residencial',
        'bairro endereço', 'zona', 'região', 'regiao'
    ],

    'city': [
        'cidade', 'municipio', 'município', 'city', 'municipality',
        'munic', 'cid', 'município de residência', 'cidade residência'
    ],

    'state': [
        'estado', 'uf', 'state', 'province', 'est', 'uf estado',
        'estado uf', 'unidade federativa', 'estado brasileiro'
    ],

    'zipCode': [
        'cep', 'código postal', 'codigo postal', 'zip', 'postal code',
        'cep código', 'postal', 'cep código postal', 'zip code',
        'código postal cep'
    ],

    'country': [
        'país', 'pais', 'country', 'nacionalidade', 'país de origem',
        'pais de origem', 'country of origin'
    ],

    # Professional fields
    'profession': [
        'profissão', 'profissao', 'graduação', 'graduacao', 'formação',
        'formacao', 'profession', 'graduation', 'formation', 'curso',
        'área de atuação', 'area de atuacao', 'especialidade', 'especialização'
    ],

    'hasClinic': [
        'tem clínica', 'tem clinica', 'possui clínica', 'possui clinica',
        'tem estabelecimento', 'has clinic', 'own clinic', 'clinic owner',
        'clínica própria', 'clinica propria'
    ],

    'clinicName': [
        'nome clínica', 'nome clinica', 'clínica nome', 'clinica nome',
        'nome estabelecimento', 'nome do estabelecimento', 'clinic name',
        'estabelecimento', 'nome da clínica'
    ],

    'clinicCity': [
        'cidade clínica', 'cidade clinica', 'cidade estabelecimento',
        'município clínica', 'municipio clinica', 'clinic city',
        'cidade da clínica'
    ],

    # Status and dates
    'status': [
        'status', 'situação', 'situacao', 'estado', 'condição', 'condicao',
        'status aluno', 'situação aluno', 'status do aluno'
    ],

    'birthDate': [
        'data nasc', 'data de nascimento', 'nascimento', 'data nascimento',
        'data nasc.', 'birth date', 'date of birth', 'dob', 'data nascimento aluno',
        'nasc', 'data nascimento aluno'
    ],

    'saleDate': [
        'data da venda', 'data venda', 'data de venda', 'venda data',
        'data contrato', 'data do contrato', 'sale date', 'contract date',
        'data assinatura', 'data de assinatura'
    ],

    'startDate': [
        'data início', 'data inicio', 'data_inicio', 'start date',
        'inicio', 'data de início', 'data de inicio', 'data início curso',
        'início curso', 'inicio curso'
    ],

    # Sales and marketing
    'salesperson': [
        'vendedor', 'vendedora', 'vendedor responsável', 'vendedor responsavel',
        'salesperson', 'seller', 'vendedor da venda', 'responsável venda',
        'responsavel venda'
    ],

    'leadSource': [
        'origem lead', 'origem', 'fonte', 'lead source', 'source',
        'origem do lead', 'fonte do lead', 'como conheceu', 'origem cliente',
        'canal', 'canal de origem', 'fonte de origem'
    ],

    'cohort': [
        'turma', 'cohort', 'turma curso', 'turma do curso', 'grupo',
        'turma aluno', 'classe', 'batch', 'lote'
    ],

    # Financial fields
    'totalValue': [
        'valor total', 'valortotal', 'valor_total', 'total', 'amount',
        'valor', 'preço', 'preco', 'price', 'total value', 'total amount',
        'valor do curso', 'valor curso', 'valor contrato', 'valor total curso',
        'montante', 'valor pago', 'valor investido'
    ],

    'installments': [
        'parcelas', 'número de parcelas', 'numero de parcelas',
        'qtd parcelas', 'quantidade de parcelas', 'installments',
        'parc', 'qtd parc', 'número parcelas', 'numero parcelas',
        'total parcelas', 'qtd de parcelas', 'quantidade parcelas'
    ],

    'installmentValue': [
        'valor parcela', 'valor_parcela', 'valorparcela', 'installment value',
        'valor da parcela', 'valor de parcela', 'parcela valor',
        'valor mensal', 'mensalidade', 'valor por parcela'
    ],

    'paymentStatus': [
        'status pagamento', 'status_pagamento', 'payment status',
        'pagamento', 'status de pagamento', 'situação pagamento',
        'situacao pagamento', 'payment', 'status pag', 'situação pag',
        'condição pagamento', 'condicao pagamento'
    ],

    'paidInstallments': [
        'parcelas pagas', 'parcelas_pagas', 'paid installments',
        'parcelas quitadas', 'parcelas pagas total', 'qtd parcelas pagas',
        'quantidade parcelas pagas', 'parcelas já pagas', 'parcelas ja pagas'
    ],

    # Professional ID
    'professionalId': [
        'registro', 'registro profissional', 'coren', 'cro', 'crm', 'crf',
        'número registro', 'numero registro', 'registro número',
        'professional id', 'professional registration', 'número conselho',
        'numero conselho', 'conselho profissional', 'registro conselho'
    ],

    # Contract status
    'contractStatus': [
        'status contrato', 'status do contrato', 'situação contrato',
        'situacao contrato', 'contract status', 'status do contrato',
        'condição contrato', 'condicao contrato', 'estado contrato'
    ]
}

def find_best_match(column_header: str, knowledge_base: Dict[str, List[str]]) -> List[Tuple[str, float]]:
    """
    Find best matching schema fields for a column header.
    Returns list of (field_name, confidence_score) tuples sorted by score.
    """
    normalized_header = normalize_header(column_header)
    matches = []

    for field_name, synonyms in knowledge_base.items():
        best_score = 0.0

        for synonym in synonyms:
            normalized_synonym = normalize_header(synonym)

            # Exact match
            if normalized_header == normalized_synonym:
                best_score = 1.0
                break
            # Contains match
            elif normalized_synonym in normalized_header or normalized_header in normalized_synonym:
                best_score = max(best_score, 0.9)
            else:
                # Similarity match
                similarity = jaro_winkler_similarity(normalized_header, normalized_synonym)
                if similarity > 0.7:
                    best_score = max(best_score, similarity * 0.85)

        if best_score > 0.5:  # Only include reasonable matches
            matches.append((field_name, best_score))

    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches
```

### Intelligent Suggestions

When confidence is low (< 70%), provide multiple mapping options:
- Show top 3-5 suggestions ordered by score
- Include reasoning for each suggestion
- Highlight pattern mismatches (e.g., column named "ID" but contains CPF values)

---

## Data Pattern Analysis

### Overview

Pattern analysis identifies data types and formats by examining actual values, not just column names. This is crucial for:
- Validating mappings
- Detecting errors
- Normalizing data formats
- Providing user feedback

### Pattern Recognition

Define comprehensive patterns for common data types:
- **CPF**: Brazilian tax ID with validation algorithm
- **Email**: Standard email format validation
- **Phone (Brazilian)**: 10-11 digits with formatting
- **Date**: Multiple format support (DD/MM/YYYY, Excel serial)
- **Monetary (Brazilian)**: R$ format with comma decimal separator
- **CEP**: Brazilian postal code (8 digits)
- **UF**: Brazilian state abbreviations (2 letters)

### Validation and Normalization

For each pattern type:
- **Regex matching**: Initial pattern detection
- **Validator function**: Domain-specific validation (e.g., CPF check digits)
- **Normalizer function**: Convert to standard format
- **Formatter function**: Display in user-friendly format

### Pattern Detection Process

1. Sample first 10-20 rows of data
2. Test each value against pattern regexes
3. Run validator functions for matched patterns
4. Calculate match ratio and confidence
5. Return best match with confidence score

---

## Integration with Existing Code

### Integration with xlsx-helper.ts

Enhance `detectHeaderRow()` function in `src/lib/xlsx-helper.ts`:

**Current Implementation:**
```typescript
// Current basic implementation
export function detectHeaderRow(rows: unknown[][], maxRowsToScan = 15): HeaderDetectionResult {
  // Basic keyword matching and scoring
}
```

**Enhanced Implementation:**
```typescript
// Enhanced with multi-factor analysis
export function detectHeaderRowEnhanced(
  rows: unknown[][],
  maxRowsToScan = 15
): HeaderDetectionResult {
  const candidates: Array<{
    rowIndex: number;
    score: number;
    headers: string[];
  }> = [];

  // Factor 1: Text ratio (headers are usually text)
  const calculateTextRatio = (row: unknown[]): number => {
    const textCells = row.filter(
      cell => cell && !String(cell).trim().match(/^\d+([.,]\d+)?$/)
    );
    return textCells.length / Math.max(row.length, 1);
  };

  // Factor 2: Keyword matches
  const countKeywordMatches = (row: unknown[]): number => {
    const normalizedRow = row.map(cell =>
      normalizeHeader(String(cell || ''))
    );
    return normalizedRow.filter(cell =>
      HEADER_KEYWORDS.some(kw => cell.includes(kw) || kw.includes(cell))
    ).length;
  };

  // Factor 3: Fill ratio
  const calculateFillRatio = (row: unknown[]): number => {
    const nonEmpty = row.filter(cell => cell && String(cell).trim());
    return nonEmpty.length / Math.max(row.length, 1);
  };

  // Factor 4: Pattern consistency (compare with next row)
  const checkPatternConsistency = (
    row: unknown[],
    nextRow: unknown[],
    index: number
  ): number => {
    if (index + 1 >= rows.length) return 0;

    const rowTypes = row.map(cell => typeof cell);
    const nextTypes = nextRow.map(cell => typeof cell);

    // Headers should have different types than data
    const typeOverlap = rowTypes.filter((t, i) => t === nextTypes[i]).length;
    return typeOverlap < rowTypes.length / 2 ? 5 : 0;
  };

  // Calculate scores for each candidate row
  for (let i = 0; i < Math.min(rows.length, maxRowsToScan); i++) {
    const row = rows[i];
    if (!row || row.length === 0) continue;

    let score = 0;

    // Factor 1: Text ratio (30 points max)
    score += calculateTextRatio(row) * 30;

    // Factor 2: Keyword matches (40 points max)
    score += Math.min(countKeywordMatches(row) * 10, 40);

    // Factor 3: Fill ratio (20 points max)
    score += calculateFillRatio(row) * 20;

    // Factor 4: Position bonus (10 points)
    if (i < 5) score += 10;

    // Factor 5: Pattern consistency (5 points)
    score += checkPatternConsistency(row, rows[i + 1] || [], i);

    const headers = row
      .map(h => String(h ?? '').trim())
      .filter(Boolean);

    if (headers.length >= 2) {
      candidates.push({
        rowIndex: i,
        score,
        headers,
      });
    }
  }

  if (candidates.length === 0) {
    return {
      headerRowIndex: 0,
      confidence: 0,
      headers: rows[0]?.map(h => String(h ?? '').trim()).filter(Boolean) || [],
      candidates: [],
    };
  }

  candidates.sort((a, b) => b.score - a.score);
  const best = candidates[0];

  // Calculate confidence
  let confidence: number;
  if (candidates.length === 1) {
    confidence = Math.min(best.score / 100, 1);
  } else {
    const scoreDiff = best.score - candidates[1].score;
    const relativeConfidence = scoreDiff / Math.max(best.score, 1);
    const absoluteConfidence = best.score / 100;
    confidence = Math.min((relativeConfidence + absoluteConfidence) / 2, 1);
  }

  return {
    headerRowIndex: best.rowIndex,
    confidence: Math.round(confidence * 100) / 100,
    headers: best.headers,
    candidates: candidates.slice(0, 5),
  };
}

// Helper function for header normalization
function normalizeHeader(header: string): string {
  return header
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove accents
    .trim()
    .replace(/\s+/g, ' ');
}
```

### Integration with csv-validator.ts

Enhance `mapCSVHeaders()` function:

**Current Implementation:**
```typescript
// Current static mapping
export function mapCSVHeaders(headers: string[]): Record<string, string> {
  const mapping: Record<string, string> = {};
  for (const header of headers) {
    const normalized = header.trim().toLowerCase();
    if (HEADER_MAP[normalized]) {
      mapping[header] = HEADER_MAP[normalized];
    }
  }
  return mapping;
}
```

**Enhanced Implementation:**
```typescript
// Enhanced with pattern analysis and fuzzy matching
export interface ColumnMappingResult {
  mapping: Record<string, string>;
  confidence: Record<string, number>;
  suggestions: Record<string, Array<{ field: string; score: number; reason: string }>>;
}

export function mapCSVHeadersIntelligent(
  headers: string[],
  sampleRows: Record<string, unknown>[],
  maxSuggestions = 3
): ColumnMappingResult {
  const mapping: Record<string, string> = {};
  const confidence: Record<string, number> = {};
  const suggestions: Record<string, Array<{ field: string; score: number; reason: string }>> = {};

  for (const header of headers) {
    // Get column data
    const columnData = sampleRows
      .map(row => row[header])
      .filter(v => v !== undefined && v !== null)
      .slice(0, 10); // Sample first 10 rows

    // Detect pattern
    const pattern = detectColumnPattern(columnData);

    // Find best matches
    const matches = findBestSchemaMatches(header, pattern, headers.indexOf(header));

    if (matches.length > 0 && matches[0].score >= 0.5) {
      mapping[header] = matches[0].field;
      confidence[header] = matches[0].score;
    }

    // Store suggestions for low confidence matches
    if (matches.length > 0 && matches[0].score < 0.7) {
      suggestions[header] = matches.slice(0, maxSuggestions).map(m => ({
        field: m.field,
        score: m.score,
        reason: m.reason,
      }));
    }
  }

  return { mapping, confidence, suggestions };
}

// Pattern detection function
function detectColumnPattern(values: unknown[]): {
  type: string;
  confidence: number;
  matchRatio: number;
} {
  if (values.length === 0) {
    return { type: 'empty', confidence: 0, matchRatio: 0 };
  }

  // CPF pattern
  const cpfPattern = /^\d{3}[.\-]?\d{3}[.\-]?\d{3}[.\-]?\d{2}$/;
  const cpfMatches = values.filter(v => cpfPattern.test(String(v).replace(/\s/g, '')));
  if (cpfMatches.length / values.length > 0.7) {
    return {
      type: 'cpf',
      confidence: cpfMatches.length / values.length,
      matchRatio: cpfMatches.length / values.length,
    };
  }

  // Email pattern
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const emailMatches = values.filter(v => emailPattern.test(String(v).toLowerCase()));
  if (emailMatches.length / values.length > 0.7) {
    return {
      type: 'email',
      confidence: emailMatches.length / values.length,
      matchRatio: emailMatches.length / values.length,
    };
  }

  // Phone pattern (Brazilian)
  const phonePattern = /^[\d\s\(\)\-\+]{10,15}$/;
  const phoneMatches = values.filter(v => {
    const digits = String(v).replace(/\D/g, '');
    return phonePattern.test(String(v)) && digits.length >= 10 && digits.length <= 11;
  });
  if (phoneMatches.length / values.length > 0.7) {
    return {
      type: 'phone',
      confidence: phoneMatches.length / values.length,
      matchRatio: phoneMatches.length / values.length,
    };
  }

  return { type: 'text', confidence: 0.3, matchRatio: 0 };
}

// Find best schema matches with scoring
function findBestSchemaMatches(
  header: string,
  pattern: { type: string; confidence: number },
  columnIndex: number
): Array<{ field: string; score: number; reason: string }> {
  const normalizedHeader = normalizeHeader(header);
  const matches: Array<{ field: string; score: number; reason: string }> = [];

  // Check against expanded knowledge base
  for (const [field, synonyms] of Object.entries(EXPANDED_HEADER_KNOWLEDGE)) {
    let semanticScore = 0;
    let reason = '';

    // Check synonyms
    for (const synonym of synonyms) {
      const normalizedSynonym = normalizeHeader(synonym);

      if (normalizedHeader === normalizedSynonym) {
        semanticScore = 1.0;
        reason = `Exact match with '${synonym}'`;
        break;
      } else if (normalizedSynonym.includes(normalizedHeader) ||
                 normalizedHeader.includes(normalizedSynonym)) {
        semanticScore = Math.max(semanticScore, 0.9);
        reason = `Contains keyword '${synonym}'`;
      } else {
        // Fuzzy match
        const similarity = jaroWinklerSimilarity(normalizedHeader, normalizedSynonym);
        if (similarity > 0.7) {
          semanticScore = Math.max(semanticScore, similarity * 0.85);
          reason = `Similar to '${synonym}' (${Math.round(similarity * 100)}% similarity)`;
        }
      }
    }

    // Pattern match bonus
    const patternScore = getPatternMatchScore(field, pattern.type);
    const totalScore = semanticScore * 0.4 + patternScore * 0.3 +
                       getPositionScore(field, columnIndex) * 0.15 +
                       getFrequencyScore(field, normalizedHeader) * 0.15;

    if (totalScore >= 0.3) {
      matches.push({
        field,
        score: totalScore,
        reason: reason || `Pattern matches: ${pattern.type}`,
      });
    }
  }

  return matches.sort((a, b) => b.score - a.score);
}

// Jaro-Winkler similarity (simplified)
function jaroWinklerSimilarity(s1: string, s2: string): number {
  // Use a library like 'string-similarity' in production
  // Simplified version here
  if (s1 === s2) return 1.0;
  if (s1.length === 0 || s2.length === 0) return 0.0;

  // Simple character overlap
  const longer = s1.length > s2.length ? s1 : s2;
  const shorter = s1.length > s2.length ? s2 : s1;
  const matches = shorter.split('').filter(c => longer.includes(c)).length;

  return matches / Math.max(s1.length, s2.length);
}
```

### Recommended Enhancements

1. **Add pattern detection**: Create `detectColumnPattern()` function in `xlsx-helper.ts`
2. **Expand knowledge base**: Add all synonyms from `EXPANDED_HEADER_KNOWLEDGE` to `HEADER_MAP` in `csv-validator.ts`
3. **Add validation feedback**: Show pattern detection results in UI components
4. **Highlight mismatches**: Alert when header name doesn't match data pattern
5. **Add confidence indicators**: Display confidence scores in mapping UI
6. **Store user corrections**: Learn from user mappings to improve future suggestions

---

## Practical Examples

### Example 1: Detecting Header in Spreadsheet with Metadata

**Spreadsheet Structure:**
```
Row 0: "Relatório de Alunos - 2024"
Row 1: (empty)
Row 2: "Nome" | "E-mail" | "Telefone" | "CPF"
Row 3: "João Silva" | "joao@email.com" | "11999999999" | "123.456.789-00"
Row 4: "Maria Santos" | "maria@email.com" | "21988888888" | "987.654.321-00"
```

**Detection Process:**

```python
rows = [
    ["Relatório de Alunos - 2024"],
    [],
    ["Nome", "E-mail", "Telefone", "CPF"],
    ["João Silva", "joao@email.com", "11999999999", "123.456.789-00"],
    ["Maria Santos", "maria@email.com", "21988888888", "987.654.321-00"]
]

result = detect_header_row(rows, max_rows_to_scan=15)

# Result:
# {
#   'header_row_index': 2,
#   'confidence': 0.85,
#   'headers': ['Nome', 'E-mail', 'Telefone', 'CPF'],
#   'candidates': [
#     {'row_index': 2, 'score': 85.0, 'headers': ['Nome', 'E-mail', 'Telefone', 'CPF']},
#     {'row_index': 0, 'score': 15.0, 'headers': ['Relatório de Alunos - 2024']}
#   ]
# }
```

**Scoring Breakdown for Row 2:**
- Text ratio: 100% (all cells are text) → 30 points
- Keyword matches: 4 matches (nome, email, telefone, cpf) → 40 points
- Fill ratio: 100% (all cells filled) → 20 points
- Position bonus: Row 2 (< 5) → 10 points
- **Total: 100 points → Confidence: 0.85**

**Mappings with Pattern Analysis:**

```python
# Analyze each column
mappings = map_columns_intelligently(
    headers=['Nome', 'E-mail', 'Telefone', 'CPF'],
    rows=rows,
    header_row_index=2
)

# Results:
# {
#   'Nome': ('name', 0.95),      # Exact keyword match + text pattern
#   'E-mail': ('email', 0.90),   # Synonym match + email pattern
#   'Telefone': ('phone', 0.92), # Keyword match + phone pattern
#   'CPF': ('cpf', 0.88)         # Keyword match + CPF pattern
# }
```

### Example 2: Ambiguous Column Name

**Column:** "Contato"

**Sample Data:**
```
"Contato"
"11999999999"
"21988888888"
"(11) 3333-4444"
```

**Analysis Process:**

```python
column_header = "Contato"
column_data = ["11999999999", "21988888888", "(11) 3333-4444"]
column_index = 2

# Step 1: Semantic analysis
semantic_score = find_synonym_match("Contato", "phone")
# Result: 0.85 (contato ≈ telefone/phone)

# Step 2: Pattern detection
pattern = detect_data_pattern(column_data)
# Result: {'type': 'phone', 'confidence': 0.90, 'format': 'brazilian'}

# Step 3: Position context
position_score = 0.70  # Column 2, expected phone position 2

# Step 4: Calculate total score
total_score = (
    semantic_score * 0.40 +      # 0.85 * 0.40 = 0.34
    pattern['confidence'] * 0.30 + # 0.90 * 0.30 = 0.27
    position_score * 0.15 +       # 0.70 * 0.15 = 0.105
    0.6 * 0.15                    # Frequency score = 0.09
)
# Total: 0.805 → Map to 'phone' with 80.5% confidence
```

**Result:** Map to `phone` (0.82 total score)

**Alternative Scenario - If pattern was emails:**

```python
column_data = ["joao@email.com", "maria@email.com", "pedro@email.com"]
pattern = detect_data_pattern(column_data)
# Result: {'type': 'email', 'confidence': 0.95}

# Semantic score for email: 0.60 (contato can mean contact/email)
total_score = 0.60 * 0.40 + 0.95 * 0.30 + 0.70 * 0.15 + 0.4 * 0.15
# Total: 0.72 → Map to 'email' with 72% confidence
```

### Example 3: Type Detection by Pattern (Header Name Mismatch)

**Column:** "ID"
**Values:**
```
"ID"
"123.456.789-00"
"987.654.321-00"
"111.222.333-44"
```

**Analysis:**

```python
column_header = "ID"
column_data = ["123.456.789-00", "987.654.321-00", "111.222.333-44"]

# Step 1: Header name suggests numeric ID
# But pattern analysis reveals CPF format
pattern = detect_data_pattern(column_data)
# Result: {
#   'type': 'cpf',
#   'confidence': 0.95,
#   'match_ratio': 1.0,
#   'format': 'brazilian_tax_id'
# }

# Step 2: Validate CPF format
for value in column_data:
    is_valid = validate_cpf(value)
    # All values pass CPF validation

# Step 3: Mapping decision
# Header name: "ID" → suggests 'id' field (numeric)
# But pattern: CPF → suggests 'cpf' field
# Pattern confidence (0.95) > Semantic confidence (0.30)
# Decision: Map to 'cpf' based on pattern evidence
```

**Result:** Map to `cpf` (0.95 confidence), not numeric `id`

**User Feedback:**
```
⚠️ Column "ID" appears to contain CPF values (confidence: 95%)
   Suggested mapping: CPF
   Reason: Data pattern matches CPF format, not numeric ID
```

### Example 4: Low Confidence - Multiple Suggestions

**Column:** "Dados"

**Sample Data:**
```
"Dados"
"João Silva"
"Maria Santos"
"Pedro Oliveira"
```

**Analysis:**

```python
column_header = "Dados"
column_data = ["João Silva", "Maria Santos", "Pedro Oliveira"]
column_index = 0

# Pattern detection
pattern = detect_data_pattern(column_data)
# Result: {'type': 'text', 'confidence': 0.5}

# Find all potential matches
matches = find_best_match("Dados", EXPANDED_HEADER_KNOWLEDGE)
# Results:
# [
#   ('name', 0.45),   # Position suggests name, text pattern
#   ('email', 0.35),  # Could be email if pattern matched
#   ('phone', 0.25),  # Low match
# ]

# Generate suggestions with reasoning
suggestions = [
    {
        'field': 'name',
        'score': 0.45,
        'confidence': 'medium',
        'reasons': [
            'Position suggests name field (first column)',
            'Text pattern matches name format',
            'Values appear to be full names'
        ]
    },
    {
        'field': 'email',
        'score': 0.35,
        'confidence': 'low',
        'reasons': [
            'Could be email if pattern matched',
            'Position sometimes used for email'
        ]
    },
    {
        'field': '_skip',
        'score': 0.30,
        'confidence': 'low',
        'reasons': [
            'Unclear mapping - consider skipping',
            'May be metadata or notes column'
        ]
    }
]
```

**UI Action:** Show dropdown with suggestions for user selection

**TypeScript Implementation:**

```typescript
// In mapping UI component
const suggestions = getMappingSuggestions("Dados", columnData, 0);

// Display in UI
<Select value={mapping["Dados"]} onValueChange={handleChange}>
  <SelectTrigger>
    <SelectValue placeholder="Select mapping..." />
  </SelectTrigger>
  <SelectContent>
    {suggestions.map(suggestion => (
      <SelectItem key={suggestion.field} value={suggestion.field}>
        {suggestion.field} ({Math.round(suggestion.score * 100)}% confidence)
        <div className="text-xs text-muted-foreground">
          {suggestion.reasons[0]}
        </div>
      </SelectItem>
    ))}
  </SelectContent>
</Select>
```

### Example 5: Regional Variations

**Column:** "Móvel" (Portuguese for mobile/phone)

**Sample Data:**
```
"Móvel"
"11999999999"
"21988888888"
"11987654321"
```

**Analysis:**

```python
column_header = "Móvel"
column_data = ["11999999999", "21988888888", "11987654321"]

# Step 1: Semantic analysis with accent handling
normalized_header = normalize_header("Móvel")  # "movel"
synonyms = EXPANDED_HEADER_KNOWLEDGE['phone']
# ['telefone', 'celular', 'móvel', 'movel', 'whatsapp', ...]

# Check synonym chain: móvel → movel → celular → telefone → phone
semantic_score = 0.88  # Strong match through synonym chain

# Step 2: Pattern detection
pattern = detect_data_pattern(column_data)
# Result: {'type': 'phone', 'confidence': 0.92, 'format': 'brazilian'}

# Step 3: Total score
total_score = 0.88 * 0.40 + 0.92 * 0.30 + 0.70 * 0.15 + 0.8 * 0.15
# Total: 0.90 → Map to 'phone' with 90% confidence
```

**Result:** Map to `phone` (0.90 confidence)

**Key Learning:** Accent normalization is crucial for Portuguese text matching.

### Example 6: Handling Multiple Data Blocks

**Spreadsheet Structure:**
```
Row 0: "Relatório de Vendas - Q1 2024"
Row 1: (empty)
Row 2: "Nome" | "Email" | "Telefone"
Row 3: "João" | "joao@..." | "11999..."
Row 4: "Maria" | "maria@..." | "21988..."
Row 5: (empty)
Row 6: "Resumo" | "Total" | "Média"
Row 7: "Vendas" | "15000" | "7500"
```

**Detection Strategy:**

```python
# First pass: Detect main data header
result1 = detect_header_row(rows[:10])
# Detects row 2 as header (confidence: 0.85)

# Second pass: Detect summary section
result2 = detect_header_row(rows[5:10])
# Detects row 6 as summary header (confidence: 0.75)

# Handle separately
main_data = extract_data_with_headers(rows, result1.header_row_index)
summary_data = extract_data_with_headers(rows[5:], result2.header_row_index)
```

### Example 7: Merged Cells / Multi-line Headers

**Spreadsheet Structure:**
```
Row 0: "Dados Pessoais" (merged across columns A-D)
Row 1: "Nome" | "Email" | "Telefone" | "CPF"
Row 2: "João" | "joao@..." | "11999..." | "123..."
```

**Detection:**

```python
# Detect multi-line header
def detect_multiline_header(rows, start_row):
    # Check if next row also looks like header
    current_row = rows[start_row]
    next_row = rows[start_row + 1] if start_row + 1 < len(rows) else []

    # If both rows are mostly text and similar structure
    if is_header_like(current_row) and is_header_like(next_row):
        return start_row + 1  # Header spans 2 rows

    return start_row

# Result: Header spans rows 0-1, data starts at row 2
header_row_index = 1  # Use second row as actual column headers
```

### Example 8: Error Detection and Validation

**Column:** "CPF"
**Values:**
```
"CPF"
"123.456.789-00"  ✓ Valid
"987.654.321-00"  ✓ Valid
"111.111.111-11"  ✗ Invalid (all same digits)
"123.456.789"     ✗ Invalid (missing check digits)
```

**Validation Process:**

```python
column_data = [
    "123.456.789-00",
    "987.654.321-00",
    "111.111.111-11",
    "123.456.789"
]

validation_results = []
for i, value in enumerate(column_data):
    is_valid, normalized, error = validate_and_normalize_value(value, 'cpf')
    validation_results.append({
        'row': i + 2,  # +2 for header row and 0-index
        'value': value,
        'valid': is_valid,
        'normalized': normalized,
        'error': error
    })

# Results:
# [
#   {'row': 2, 'valid': True, 'normalized': '12345678900', 'error': None},
#   {'row': 3, 'valid': True, 'normalized': '98765432100', 'error': None},
#   {'row': 4, 'valid': False, 'normalized': None, 'error': 'CPF with all same digits'},
#   {'row': 5, 'valid': False, 'normalized': None, 'error': 'CPF missing check digits'}
# ]

# User feedback:
# ⚠️ Row 4: Invalid CPF - all same digits
# ⚠️ Row 5: Invalid CPF - missing check digits
```

### Example 9: Learning from User Corrections

**Scenario:** User corrects mapping "Contato" → `email` instead of suggested `phone`

**Learning System:**

```typescript
// Store user correction
interface UserCorrection {
  columnHeader: string;
  suggestedField: string;
  userSelectedField: string;
  columnData: unknown[];
  timestamp: number;
}

// Learn from correction
function learnFromCorrection(correction: UserCorrection) {
  // Analyze why user chose different field
  const pattern = detectColumnPattern(correction.columnData);

  // If pattern matches user's choice better, update knowledge base
  if (pattern.type === 'email' && correction.userSelectedField === 'email') {
    // Add "contato" as email synonym in specific contexts
    updateKnowledgeBase('email', {
      context: 'when_pattern_is_email',
      synonyms: [...existingSynonyms, 'contato']
    });
  }

  // Track for future suggestions
  trackCorrection(correction);
}
```

**Future Improvement:** Next time "Contato" with email pattern appears, suggest `email` first.

---

## Best Practices Summary

1. **Always use multi-factor analysis** - Don't rely on single method
2. **Sample data for pattern detection** - Use first 10-20 rows, not all data
3. **Provide fallbacks** - When confidence is low, show suggestions
4. **Validate patterns** - Use domain-specific validators (CPF, CEP, etc.)
5. **Normalize early** - Clean and normalize data during detection
6. **User feedback** - Show confidence scores and reasoning
7. **Learn from corrections** - Track user corrections to improve future mappings
8. **Handle edge cases** - Empty rows, merged cells, multiple data blocks

---

## Performance Considerations

- **Limit scanning**: Only scan first 15 rows for headers
- **Sample data**: Use first 10-20 rows for pattern detection
- **Cache results**: Store detection results to avoid re-computation
- **Lazy evaluation**: Only analyze columns that need mapping
- **Parallel processing**: Analyze multiple columns simultaneously if possible