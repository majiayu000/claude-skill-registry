---
name: pathling-python
description: Comprehensive cheat sheet for using the Pathling Python API. Use this skill when working with FHIR data in Python, running SQL on FHIR queries, using terminology functions, encoding FHIR resources, or any other Pathling Python operations. Trigger keywords include "pathling", "pathling python", "fhir encoding", "sql on fhir python", "terminology functions", "member_of", "translate", "subsumes", "PathlingContext".
---

# Pathling Python API cheat sheet

You are an expert in using the Pathling Python API for working with FHIR data in Python applications and data science workflows.

## Installation

Prerequisites:

- Python 3.9+ with pip

```bash
pip install pathling
```

## Core concepts

### PathlingContext

The main entry point for all Pathling operations. It manages the Spark session and provides access to data reading, encoding, and terminology functions.

**Creating a basic context:**

```python
from pathling import PathlingContext

pc = PathlingContext.create()
```

**Creating a context with terminology server authentication:**

```python
pc = PathlingContext.create(
    terminology_server_url='https://ontology.nhs.uk/production1/fhir',
    token_endpoint='https://ontology.nhs.uk/authorisation/auth/realms/nhs-digital-terminology/protocol/openid-connect/token',
    client_id='[client ID]',
    client_secret='[client secret]'
)
```

**Creating a context with caching:**

```python
pc = PathlingContext.create(
    terminology_server_url="http://localhost:8081/fhir",
    terminology_verbose_request_logging=True,
    cache_override_expiry=2_628_000,
    cache_storage_type="disk",
    cache_storage_path=".local/tx-cache"
)
```

**Accessing the Spark session:**

```python
pc.spark  # Access the underlying Spark session
pc.spark.sparkContext.setLogLevel("DEBUG")  # Set log level
```

## Reading FHIR data

### Reading NDJSON files

NDJSON is a common format for bulk FHIR data, with one JSON resource per line.

```python
# Read each line from the NDJSON into a row within a Spark data set.
ndjson_dir = '/some/path/ndjson/'
json_resources = pc.spark.read.text(ndjson_dir)

# Convert the data set of strings into a structured FHIR data set.
patients = pc.encode(json_resources, 'Patient')

# Do some stuff.
patients.select('id', 'gender', 'birthDate').show()
```

**Using the DataSource API:**

```python
data = pc.read.ndjson("/some/file/location")
```

### Reading FHIR Bundles

FHIR Bundles contain collections of related resources.

```python
# Read each Bundle into a row within a Spark data set.
bundles_dir = '/some/path/bundles/'
bundles = pc.spark.read.text(bundles_dir, wholetext=True)

# Convert the data set of strings into a structured FHIR data set.
patients = pc.encode_bundle(bundles, 'Patient')

# XML Bundles can be encoded using input type.
# patients = pc.encode_bundle(bundles, 'Patient', inputType=MimeType.FHIR_XML)

# Do some stuff.
patients.select('id', 'gender', 'birthDate').show()
```

### Reading from Delta tables

```python
# Read from previously persisted Delta tables.
data = pc.read.tables()

# Get available resource types.
data.resource_types()

# Read a specific resource.
patients = data.read('Patient')
patients.count()
```

## SQL on FHIR views

SQL on FHIR views project FHIR data into easy-to-use tabular forms.

### Basic view with simple columns

```python
result = data.view(
    resource="Patient",
    select=[
        {"column": [{"path": "getResourceKey()", "name": "patient_id"}]},
        {
            "forEach": "address",
            "column": [
                {"path": "line.join('\\n')", "name": "street"},
                {"path": "use", "name": "use"},
                {"path": "city", "name": "city"},
                {"path": "postalCode", "name": "zip"},
            ],
        },
    ],
)

display(result)
```

### View with where clause

```python
view_ds = datasource.view(
    resource='Patient',
    select=[
        {
            'column': [
                {'path': 'id', 'name': 'id'},
                {'path': 'gender', 'name': 'gender'},
                {'path': "telecom.where(system='phone').value ", 'name': 'phone_numbers', 'collection': True},
            ]
        }
    ],
    where=[
        {'path': "gender = 'male'"},
    ]
)

view_ds.show()
```

### Nested forEach with forEachOrNull

```python
view_ds = datasource.view(
    resource='Patient',
    select=[
        {
            'forEach': 'name',
            'column': [
                {'path': 'use', 'name': 'name_use'},
                {'path': 'family', 'name': 'family_name'},
            ],
            'select': [
                {
                    'forEachOrNull': 'given',
                    'column': [
                        {'path': '$this', 'name': 'given_name'},
                    ],
                }
            ]
        },
    ]
)

view_ds.show()
```

## Terminology functions

Terminology functions require a FHIR terminology server to be configured.

### Helper functions for creating Coding structs

**to_coding:**

```python
from pathling import to_coding

# Convert a column containing codes into a Coding struct.
coding_column = to_coding(df.CODE, 'http://snomed.info/sct')

# With version.
coding_column = to_coding(df.CODE, 'http://snomed.info/sct', version='http://snomed.info/sct/32506021000036107/version/20250831')
```

**to_snomed_coding:**

```python
from pathling import to_snomed_coding

# Shorthand for SNOMED CT codes.
coding_column = to_snomed_coding(df.CODE)
coding_column = to_snomed_coding(df.CODE, version='http://snomed.info/sct/32506021000036107/version/20250831')
```

**to_loinc_coding:**

```python
from pathling.functions import to_loinc_coding

# Shorthand for LOINC codes.
coding_column = to_loinc_coding(df.CODE)
```

**Coding class:**

```python
from pathling import Coding

# Create a Coding object.
coding = Coding('http://snomed.info/sct', '232208008')

# Create a SNOMED Coding using the factory method.
snomed_coding = Coding.of_snomed('232208008')

# Convert to a Spark literal column.
coding_literal = coding.to_literal()
```

**to_ecl_value_set:**

```python
from pathling import to_ecl_value_set

# Convert a SNOMED CT ECL expression into a FHIR ValueSet URI.
viral_infection_ecl = """
<< 64572001|Disease| : (
  << 370135005|Pathological process| = << 441862004|Infectious process|,
  << 246075003|Causative agent| = << 49872002|Virus|
)
"""
value_set_uri = to_ecl_value_set(viral_infection_ecl)
```

### member_of - Value set membership

Test if a code is a member of a value set.

```python
from pathling import member_of, to_snomed_coding, to_ecl_value_set

# Using an ECL expression.
result = csv.select(
    "CODE",
    "DESCRIPTION",
    member_of(
        to_snomed_coding(csv.CODE),
        to_ecl_value_set("<< 64572001")  # Viral disease
    ).alias("VIRAL_INFECTION")
)
result.show()

# Using a predefined value set.
result = csv.select(
    "CODE",
    "DESCRIPTION",
    member_of(
        to_coding(csv.CODE, 'http://loinc.org'),
        'http://hl7.org/fhir/ValueSet/observation-vitalsignresult'
    ).alias("IS_VITAL_SIGN")
)
```

**Alternative syntax using PathlingContext:**

```python
result = transformed_df.withColumn(
    "Viral Infection",
    pc.snomed.member_of(col("primary_diagnosis_concept"), "<< 64572001")
)
```

### translate - Concept translation

Translate codes from one code system to another.

```python
from pathling import translate, to_coding

# Translate SNOMED CT codes to Read CTV3.
result = pc.translate(
    csv,
    to_coding(csv.CODE, 'http://snomed.info/sct'),
    'http://snomed.info/sct/900000000000207008?fhir_cm=900000000000497000',
    output_column_name='READ_CODE'
)

# Extract just the code from the Coding struct.
result = result.withColumn('READ_CODE', result.READ_CODE.code)
result.select('CODE', 'DESCRIPTION', 'READ_CODE').show()
```

### subsumes and subsumed_by - Subsumption testing

Test if one code is equal to or a subtype of another code.

```python
from pathling import subsumes, to_snomed_coding, Coding

# Test if codes are subsumed by a specific code.
# 232208008 |Ear, nose and throat disorder|
left_coding = Coding('http://snomed.info/sct', '232208008')
right_coding_column = to_snomed_coding(csv.CODE)

result = pc.subsumes(
    csv,
    'IS_ENT',
    left_coding=left_coding,
    right_coding_column=right_coding_column
)

result.select('CODE', 'DESCRIPTION', 'IS_ENT').show()
```

**Using subsumed_by (reverse order):**

```python
from pathling import subsumed_by

# Test if a code is subsumed by codes in a column.
result = pc.subsumed_by(
    csv,
    'IS_SUBTYPE',
    left_coding_column=to_snomed_coding(csv.CODE),
    right_coding=Coding('http://snomed.info/sct', '232208008')
)
```

### property_of - Retrieve code properties

Retrieve properties associated with codes in terminologies.

```python
from pathling import property_of, to_snomed_coding, PropertyType

# Get the parent codes for each code in the dataset.
parents = csv.withColumn(
    "PARENTS",
    property_of(to_snomed_coding(csv.CODE), "parent", PropertyType.CODE)
)

# Split each parent code into a separate row.
exploded_parents = parents.selectExpr(
    "CODE", "DESCRIPTION", "explode_outer(PARENTS) AS PARENT"
)
```

**PropertyType values:**

- `PropertyType.CODE` - Returns an array of codes.
- `PropertyType.STRING` - Returns an array of strings.
- `PropertyType.INTEGER` - Returns an array of integers.
- `PropertyType.BOOLEAN` - Returns an array of booleans.
- `PropertyType.DATETIME` - Returns an array of timestamps.
- `PropertyType.DECIMAL` - Returns an array of decimals.

### display - Get preferred display term

Retrieve the preferred display term for codes.

```python
from pathling import display, to_snomed_coding

# Get the display term for parent codes.
with_displays = exploded_parents.withColumn(
    "PARENT_DISPLAY",
    display(to_snomed_coding(exploded_parents.PARENT))
)

with_displays.show()
```

**Alternative syntax using PathlingContext:**

```python
transformed_df = source_df.withColumn(
    "Primary Diagnosis Term",
    pc.snomed.display(col("primary_diagnosis_concept"))
)
```

### designation - Get alternative display terms

Retrieve alternative display terms (synonyms, translations, etc.).

```python
from pathling import designation, to_snomed_coding, Coding

# Get the synonyms for each code in the dataset.
# 900000000000013009 is the SNOMED CT "Synonym" designation use.
synonyms = csv.withColumn(
    "SYNONYMS",
    designation(
        to_snomed_coding(csv.CODE),
        Coding.of_snomed("900000000000013009")
    )
)

# Split each synonym into a separate row.
exploded_synonyms = synonyms.selectExpr(
    "CODE", "DESCRIPTION", "explode_outer(SYNONYMS) AS SYNONYM"
)

exploded_synonyms.show()
```

## Common patterns

### Grouping and categorising with SNOMED CT

```python
from pathling import PathlingContext, to_snomed_coding, to_ecl_value_set, member_of
from pyspark.sql.functions import col, when

pc = PathlingContext.create()

# Define value sets using ECL.
viral_infection_ecl = "<< 64572001"  # Viral disease
musculoskeletal_injury_ecl = "<< 263534002"  # Injury of musculoskeletal system
mental_health_ecl = "<< 40733004 |Mental state finding|"

# Add membership columns for each category.
categorised_df = df.withColumn(
    "Viral Infection",
    member_of(to_snomed_coding(col("diagnosis_code")), to_ecl_value_set(viral_infection_ecl))
).withColumn(
    "Musculoskeletal Injury",
    member_of(to_snomed_coding(col("diagnosis_code")), to_ecl_value_set(musculoskeletal_injury_ecl))
).withColumn(
    "Mental Health Problem",
    member_of(to_snomed_coding(col("diagnosis_code")), to_ecl_value_set(mental_health_ecl))
)

# Create mutually exclusive categories with hierarchy.
mutually_exclusive_df = categorised_df.withColumn(
    "Category",
    when(col("Viral Infection"), "Viral Infection")
    .when(~col("Viral Infection") & col("Musculoskeletal Injury"), "Musculoskeletal Injury")
    .when(~col("Viral Infection") & ~col("Musculoskeletal Injury") & col("Mental Health Problem"), "Mental Health Problem")
    .otherwise("Other")
)
```

### Enriching data with terminology information

```python
from pathling import display, property_of, to_snomed_coding, PropertyType

# Add display terms to codes.
enriched_df = df.withColumn(
    "diagnosis_display",
    display(to_snomed_coding(df.diagnosis_code))
)

# Add parent codes.
with_parents = enriched_df.withColumn(
    "parent_codes",
    property_of(to_snomed_coding(df.diagnosis_code), "parent", PropertyType.CODE)
)
```

### Converting Spark DataFrames to Pandas

After creating a view or running terminology functions, you can convert the result to a Pandas DataFrame for use in Python data science tools.

```python
# Convert to Pandas.
pandas_df = result.toPandas()

# Use with plotting libraries.
import plotly.express as px

fig = px.bar(pandas_df, x="category", y="count")
fig.show()
```

## Configuration options

### PathlingContext.create() parameters

- `terminology_server_url` - URL of the FHIR terminology server.
- `token_endpoint` - OAuth2 token endpoint for authentication.
- `client_id` - OAuth2 client ID.
- `client_secret` - OAuth2 client secret.
- `terminology_verbose_request_logging` - Enable verbose logging of terminology requests.
- `cache_override_expiry` - Cache expiry time in seconds.
- `cache_storage_type` - Cache storage type (`"memory"` or `"disk"`).
- `cache_storage_path` - Path for disk-based cache.

### Spark configuration

When running your own Spark cluster, configure Pathling as a Spark package:

```
spark.jars.packages au.csiro.pathling:library-api:[version]
```

## MimeType and Version enums

```python
from pathling import MimeType, Version

# MimeType values.
MimeType.FHIR_JSON  # application/fhir+json
MimeType.FHIR_XML   # application/fhir+xml

# Version values.
Version.R4  # FHIR R4
```

## Databricks installation

Install both packages:

1. `pathling` PyPI package
2. `au.csiro.pathling:library-api` Maven package

Enable Java 21 support in Advanced Options > Spark > Environment Variables:

```bash
JNAME=zulu21-ca-amd64
```

## Common gotchas

1. **Always create Coding structs when using terminology functions** - Use `to_coding()`, `to_snomed_coding()`, or the `Coding` class to convert code columns into the proper struct format.

2. **ECL expressions need to be converted to value set URIs** - Use `to_ecl_value_set()` to convert ECL expressions before passing them to `member_of()`.

3. **Terminology functions return new columns** - Use `.withColumn()` or `.select()` to add terminology function results to your DataFrame.

4. **Resource encoding requires the correct resource type** - Make sure to specify the correct FHIR resource type when using `encode()` or `encode_bundle()`.

5. **SQL on FHIR views use FHIRPath syntax** - The `path` elements in view definitions use FHIRPath expressions, not SQL or Python syntax.

6. **PathlingContext manages the Spark session** - Access the Spark session via `pc.spark`, don't create a separate one.

## Best practices

1. **Use DataSource API for reading data** - Prefer `pc.read.ndjson()` or `pc.read.tables()` over manual encoding.

2. **Cache terminology results** - Configure terminology caching to avoid repeated requests to the terminology server.

3. **Use appropriate terminology server** - For Australian FHIR content, use the Australian terminology server.

4. **Batch terminology operations** - Process data in batches to improve performance of terminology operations.

5. **Use SQL on FHIR views for complex projections** - Views provide a declarative way to flatten and transform FHIR data.

6. **Profile your Spark jobs** - Use Spark's monitoring tools to identify performance bottlenecks.

7. **Set appropriate log levels** - Use `pc.spark.sparkContext.setLogLevel()` to control logging verbosity.
