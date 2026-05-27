---
name: create-semantic-type-detector
description: Define semantic type detectors in detectors.js to auto-detect column data meaning
---

# Create a Semantic Type Detector

Help the user define semantic type detectors that automatically identify the meaning of column data in Datagrok.

## Usage
```
/create-semantic-type-detector [semantic-type-name]
```

## Instructions

### 1. Scaffold a detector

From the package directory:
```shell
grok add detector <semantic-type-name>
```

This adds a template detector function to `detectors.js`.

### 2. Understand the detectors.js file

Detectors live in `detectors.js` at the package root (not inside `src/`). This file is loaded separately from the main webpack bundle. Define a class that extends `DG.Package`:

```javascript
class <PackageName>PackageDetectors extends DG.Package {

  //tags: semTypeDetector
  //input: column col
  //output: string semType
  detectMyType(col) {
    // Detection logic
    // Return semantic type string or null
  }
}
```

### 3. Write the detection function

The function must:
- Be tagged with `semTypeDetector`
- Accept a single `column` input
- Return a `string` (the semantic type name) or `null`
- Set `col.semType` when a match is found

**Simple name-based detection:**
```javascript
//tags: semTypeDetector
//input: column col
//output: string semType
detectNucleotides(col) {
  if (col.name.startsWith('nuc')) {
    col.semType = 'nucleotides';
    return col.semType;
  }
  return null;
}
```

**Type and statistics-based detection:**
```javascript
//tags: semTypeDetector
//input: column col
//output: string semType
detectMagnitude(col) {
  if ((col.type === DG.TYPE.FLOAT || col.type === DG.TYPE.INT) &&
    (0 < col.min && col.max < 10) && col.name.toLowerCase() === 'magnitude') {
    col.semType = 'Magnitude';
    return col.semType;
  }
  return null;
}
```

**Sampling categories for large datasets:**
```javascript
//tags: semTypeDetector
//input: column col
//output: string semType
detectMyFormat(col) {
  if (DG.Detector.sampleCategories(col, (s) => /^[A-Z]{3}-\d{4}$/.test(s)))  {
    col.semType = 'MyFormat';
    return col.semType;
  }
  return null;
}
```

### 4. Detection best practices

- **Keep detectors lightweight.** They run every time a table is opened. Use simple checks: `col.type`, `col.name`, regex on column name.
- **Use column statistics** when needed: `col.min`, `col.max`, `col.stats.missingValueCount`, etc.
- **Use `DG.Detector.sampleCategories()`** for string columns with many unique values -- it checks a random subset instead of all values.
- **Handle empty values.** Never match empty strings or nulls. They should not trigger a semantic type assignment.
- **A column can have only one semantic type.** If multiple detectors match, the result depends on execution order.
- **Set units if applicable:** `col.meta.units = 'pdb';` for subtypes within the same semantic type.

### 5. Testing detectors

Detectors have automatic tests in Datagrok. Control test behavior with meta tags:

```javascript
//tags: semTypeDetector
//input: column col
//output: string semType
//meta.testData: my_test_data.csv
//meta.testDataColumnName: MyColumn
detectMyType(col) { /* ... */ }
```

- `//meta.testData:` -- specify a CSV file in the package for testing
- `//meta.testDataColumnName:` -- specify which column in the test data should match
- `//meta.skipTest:` -- skip the auto-test with a reason (e.g., `//meta.skipTest: #2596, needs fix`)

### 6. Use detectors with info panels

Once a detector assigns a semantic type, info panels with matching `{semType: MyType}` will automatically appear:

```typescript
// In src/package.ts
//name: MyTypePanel
//tags: panel, widgets
//input: string value {semType: MyType}
//output: widget result
export function myTypePanel(value: string) {
  return new DG.Widget(ui.divText('Detected: ' + value));
}
```

### 7. Build and publish

```shell
npm run build
grok publish dev
```

Test by opening a table with data that should trigger your detector. Check that columns get the expected semantic type.

## Behavior

- Ask for the semantic type name and what data pattern it represents if not specified.
- Always place detector functions in `detectors.js` at the package root, not in `src/`.
- The class name must follow the pattern `<PackageName>PackageDetectors extends DG.Package`.
- Remind the user that `detectors.js` is loaded separately from webpack -- do not use imports that require bundling.
- Warn about empty value handling: regex patterns should not match empty strings.
- Suggest `DG.Detector.sampleCategories()` for string columns to avoid performance issues.
- Follow Datagrok coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else-if on new line.
