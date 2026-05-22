---
name: sf-omnistudio
description: |
  Comprehensive OmniStudio / Salesforce Industries development skill covering
  OmniScripts, FlexCards, Integration Procedures, Data Mappers (DataRaptors),
  namespace detection, dependency mapping, and migration patterns.
  TRIGGER when: user works with OmniStudio components, asks about OmniScripts,
  FlexCards, Integration Procedures, Data Mappers, DataRaptors, namespace
  detection, or Vlocity-to-Core migration.
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org with OmniStudio or Industries Cloud license.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, omnistudio, omniscript, flexcard, integration-procedure, datamapper, dataraptor, industries
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# OmniStudio Development Guide

You are a Salesforce OmniStudio specialist. Build, review, and troubleshoot all OmniStudio components: OmniScripts, FlexCards, Integration Procedures, and Data Mappers.

## OmniStudio Overview

OmniStudio is Salesforce Industries' declarative development framework for building guided digital experiences without code. It provides four primary component types that work together:

| Component | Purpose | Analogy |
|-----------|---------|---------|
| **OmniScript** | Multi-step guided wizard for user interaction | Screen Flow |
| **FlexCard** | At-a-glance UI card displaying data | Lightning Component |
| **Integration Procedure** | Server-side process orchestration | Apex Service Layer |
| **Data Mapper** | Data extraction, transformation, and loading | SOQL + DML abstraction |

**Component dependency chain** (build bottom-up):

```
Data Mapper --> Integration Procedure --> OmniScript --> FlexCard
   (data)        (orchestration)          (wizard)      (display)
```

Data Mappers read/write Salesforce data. Integration Procedures orchestrate Data Mappers, Apex, and HTTP calls. OmniScripts present guided UIs that invoke Integration Procedures. FlexCards display summary data and can launch OmniScripts.

## Namespace Guide

OmniStudio exists in three namespace variants. You MUST detect the namespace before querying any component metadata.

| Namespace | Package | Industry |
|-----------|---------|----------|
| **Core** (no prefix) | OmniStudio managed package / Industries Cloud | All industries (Spring '22+) |
| **vlocity_cmt** | Vlocity CMT | Communications, Media, Energy |
| **vlocity_ins** | Vlocity INS | Insurance, Health |

### Namespace Detection

Try querying a known object from each namespace. An `INVALID_TYPE` error means that variant isn't installed; a valid response (even `totalSize: 0`) confirms it.

| Namespace | Test Query | Object to Probe |
|-----------|-----------|-----------------|
| Core | `sf data query -q "SELECT Id FROM OmniProcess LIMIT 1" -o <org>` | `OmniProcess` |
| vlocity_cmt | `sf data query -q "SELECT Id FROM vlocity_cmt__OmniScript__c LIMIT 1" -o <org>` | `vlocity_cmt__OmniScript__c` |
| vlocity_ins | `sf data query -q "SELECT Id FROM vlocity_ins__OmniScript__c LIMIT 1" -o <org>` | `vlocity_ins__OmniScript__c` |

Start with Core (the modern path) and fall back to Vlocity variants if it fails.

### Object Name Mapping

| Concept | Core | vlocity_cmt | vlocity_ins |
|---------|------|-------------|-------------|
| OmniScript / IP | `OmniProcess` | `vlocity_cmt__OmniScript__c` | `vlocity_ins__OmniScript__c` |
| Elements | `OmniProcessElement` | `vlocity_cmt__Element__c` | `vlocity_ins__Element__c` |
| FlexCard | `OmniUiCard` | `vlocity_cmt__VlocityUITemplate__c` | `vlocity_ins__VlocityUITemplate__c` |
| Data Mapper | `OmniDataTransform` | `vlocity_cmt__DRBundle__c` | `vlocity_ins__DRBundle__c` |
| Data Mapper Item | `OmniDataTransformItem` | `vlocity_cmt__DRMapItem__c` | `vlocity_ins__DRMapItem__c` |

See [references/omnistudio-reference.md](references/omnistudio-reference.md) for the complete field-level mapping.

## OmniScripts

OmniScripts are multi-step, interactive guided experiences (wizards). They collect user input, call server-side logic, and present results -- all declaratively.

### Identification

Every OmniScript is uniquely identified by a **Type / SubType / Language** triplet (e.g., `ServiceRequest / NewCase / English`). Multiple versions can exist; only one is active per triplet.

In Core namespace, OmniScripts are stored in `OmniProcess` with `IsIntegrationProcedure = false`.

### Element Types

**Containers**: Step, Conditional Block, Loop Block, Edit Block

**Inputs**: Text, Text Area, Number, Date, Date/Time, Checkbox, Radio, Select, Multi-select, Type Ahead, File, Currency, Email, Telephone, URL, Signature, Password, Range, Time

**Display**: Text Block, Headline, Aggregate, Disclosure, Image, Chart

**Actions**: DataRaptor Extract Action, DataRaptor Load Action, Integration Procedure Action, Remote Action, Navigate Action, Email Action, DocuSign Envelope Action

**Logic**: Set Values, Validation, Formula, Submit Action

### Element Hierarchy

Elements use `Level` and `Order` fields to form a tree. Level 0 = Steps (pages in the wizard). Level 1+ = elements within steps. `Order` determines sequence within a level.

### Data Flow

OmniScripts maintain a single JSON data structure passed through all steps. Elements read from and write to this shared JSON using merge field syntax (`%fieldName%`). Action elements map input/output between the JSON and server calls.

### LWC-Enabled OmniScripts

LWC OmniScripts render using Lightning Web Components instead of Aura. Key differences:
- Use `omnistudio-omniscript` base component
- Custom elements must extend `OmniscriptBaseMixin`
- CSS styling uses SLDS tokens instead of Aura-specific classes
- Event model differs (LWC custom events vs Aura events)
- Cannot embed Aura components inside LWC OmniScripts

### OmniScript Best Practices

- Limit to 7-10 input elements per Step for usability
- Add validation on all required inputs
- Configure error handling on every action element (`showError`, `errorMessage`)
- Use conditional visibility (`show` expressions) to hide irrelevant fields
- Fire data-loading actions on step entry, not on OmniScript load
- Never embed OmniScript A in B if B embeds A (circular embedding causes infinite loops)
- Never hardcode Salesforce record IDs in PropertySetConfig

## FlexCards

FlexCards are declarative UI cards that display at-a-glance information with data from Integration Procedures, SOQL, or REST sources.

### Data Sources

FlexCards bind to data sources configured in the `DataSourceConfig` JSON field on `OmniUiCard`. Core namespace splits what Vlocity stored in a single `Definition` blob into separate `DataSourceConfig` and `PropertySetConfig` fields.

| Source Type | `dataSource.type` Value | Use Case |
|-------------|------------------------|----------|
| Integration Procedure | `IntegrationProcedures` (must be plural) | Primary pattern for live data |
| SOQL | `SOQL` | Direct queries (prefer IP for abstraction) |
| Apex Remote | `ApexRemote` | Custom Apex class invocation |
| REST | `REST` | External API via Named Credential |

Data sources pass context via input parameters (e.g., `{recordId}`) and map response fields to card elements using `{fieldName}` merge syntax.

### Layout Types

| Layout | Use Case |
|--------|----------|
| Single Card | Record summary display |
| Card List | Repeating cards from array data |
| Tabbed Card | Multiple views as tabs |
| Flyout Card | Expandable detail panel |

### Actions and Child Cards

FlexCards can launch OmniScripts via action buttons, passing context data as input. Cards can embed other FlexCards as child cards (limit nesting to 2 levels for performance). LWC FlexCards follow the same patterns but render as Lightning Web Components.

### FlexCard Best Practices

- Always configure empty-state messaging when data source returns no records
- Use SLDS design tokens for styling (no hardcoded colors)
- Add `aria-label` on all interactive elements for accessibility
- Limit child card nesting to 2 levels
- Verify all referenced Integration Procedures are active before deployment

## Integration Procedures

Integration Procedures (IPs) are server-side orchestrations that combine Data Mapper actions, Apex calls, HTTP callouts, and conditional logic into declarative multi-step operations.

### Identification

IPs use a **Type / SubType** pair as their key (e.g., `AccountOnboarding / Standard`). In Core namespace, IPs are stored in `OmniProcess` with `IsIntegrationProcedure = true`.

### Action Types

| Element Type | Purpose | Key PropertySet Fields |
|-------------|---------|----------------------|
| DataRaptor Extract Action | Read Salesforce data | `bundle` (Data Mapper name) |
| DataRaptor Load Action | Write Salesforce data | `bundle` |
| DataRaptor Transform Action | In-memory data reshaping | `bundle` |
| Remote Action | Call Apex class method | `remoteClass`, `remoteMethod` |
| Integration Procedure Action | Call nested IP | `ipMethod` (Type_SubType format) |
| HTTP Action | External API callout | `path`, `method`, `httpUrl` |
| Matrix Action | Decision table lookup | `matrixName` |
| Email Action | Send email | `emailTemplateId` |
| Conditional Block | Branching logic | condition expression |
| Loop Block | Iterate over collections | loop source path |
| Set Values | Assign variables | key-value pairs |

### Response Mapping

Each element's output is namespaced under its element name in the response JSON. Reference upstream outputs in downstream inputs using `%elementName:keyPath%` syntax.

### Caching

IPs support platform cache for read-heavy orchestrations. Set `cacheType` and `cacheTTL` in the procedure's PropertySet. Never cache procedures that perform DML -- cached results bypass actual data operations.

### Integration Procedure Best Practices

- Deploy all referenced Data Mappers before deploying the IP
- Set LIMIT on all DataRaptor Extract actions to avoid governor limits
- Wrap DataRaptor Load actions in error handling (try/catch or conditional checks)
- Never create circular IP call chains (A calls B calls A)
- Use parallel execution for independent elements
- Never hardcode Salesforce IDs or API credentials in PropertySetConfig
- Use Named Credentials for external API authentication

## Data Mappers / DataRaptors

Data Mappers (formerly DataRaptors) provide declarative data access for OmniStudio. They handle Extract, Transform, and Load operations against Salesforce objects.

### Types

| Type | Purpose | Reads Data | Writes Data | Naming Prefix |
|------|---------|-----------|-------------|---------------|
| **Extract** | Query records with relationship support | Yes (SOQL) | No | `DR_Extract_` |
| **Turbo Extract** | High-volume compiled queries (10x faster) | Yes (compiled) | No | `DR_TurboExtract_` |
| **Transform** | In-memory data reshaping (JSON-to-JSON) | No | No | `DR_Transform_` |
| **Load** | Insert, update, upsert, or delete records | No | Yes (DML) | `DR_Load_` |

### Metadata Structure

Data Mappers are stored as `OmniDataTransform` records (parent) with `OmniDataTransformItem` records (field mappings). Watch out: the child-to-parent lookup field uses the unabbreviated spelling `OmniDataTransformationId` — developers often mistakenly try `OmniDataTransformId`, which doesn't exist.

### Turbo Extract Limitations

Turbo Extract does NOT support: formula fields, related lists, aggregate queries, polymorphic fields. Fall back to standard Extract for these cases.

### Data Mapper Best Practices

- Always specify explicit field lists (no wildcards)
- Add LIMIT and filter conditions on all Extract queries
- Validate field-level security before deploying Load Data Mappers
- Use upsert keys to prevent duplicate records on Load
- Activate Data Mappers after deployment (inactive ones are not callable)
- Name using `DR_[Type]_[Object]_[Purpose]` convention in PascalCase

## Dependency Mapping

OmniStudio components form a directed dependency graph. Trace dependencies to understand impact before modifying any component.

### Dependency Sources

| Component | Where Dependencies Live | What to Parse |
|-----------|------------------------|---------------|
| OmniScript | `PropertySetConfig` on `OmniProcessElement` | `bundle` (Data Mapper), `ipMethod` (IP), `omniScriptKey` (nested OS) |
| Integration Procedure | `PropertySetConfig` on `OmniProcessElement` | `bundle`, `remoteClass`, `integrationProcedureKey`, `httpUrl` |
| FlexCard | `DataSourceConfig` on `OmniUiCard` | `dataSource.value.ipMethod` (IP), `dataSource.value.className` (Apex) |
| Data Mapper | `InputObjectName` / `OutputObjectName` on `OmniDataTransformItem` | Source and target sObjects |

### Dependency Queries (Core Namespace)

```bash
# OmniScript/IP elements with config
sf data query -q "SELECT Id, OmniProcessId, Name, Type, PropertySetConfig FROM OmniProcessElement WHERE OmniProcessId = '<id>'" -o <org> --json

# FlexCard data sources
sf data query -q "SELECT Id, Name, DataSourceConfig FROM OmniUiCard WHERE IsActive = true" -o <org> --json

# Data Mapper object references
sf data query -q "SELECT Id, OmniDataTransformationId, InputObjectName, OutputObjectName FROM OmniDataTransformItem" -o <org> --json
```

### Impact Analysis

When modifying a component, trace all dependents upstream:
1. Changing a Data Mapper? Find all IPs and OmniScripts referencing its `bundle` name
2. Changing an IP? Find all OmniScripts with matching `ipMethod` and FlexCards with matching data source
3. Changing an OmniScript? Find all FlexCards with launch actions targeting it
4. Check both active and inactive components -- inactive ones may become active later

## Migration Patterns

### Vlocity to OmniStudio Core Migration

When migrating from Vlocity (vlocity_cmt or vlocity_ins) to OmniStudio Core:

1. **Inventory**: Catalog all components in the source namespace using analysis queries
2. **Namespace conversion**: Map all object and field API names from Vlocity to Core equivalents (see Namespace Guide above)
3. **Export**: Extract component definitions as JSON from source org
4. **Transform**: Convert namespace-prefixed field references in PropertySetConfig, DataSourceConfig, and element configurations
5. **Deploy order**: Data Mappers first, then Integration Procedures, then OmniScripts, then FlexCards
6. **Validate**: Run each component in the target org, verifying data flow end-to-end
7. **Decommission**: Deactivate Vlocity components only after Core equivalents are verified

Key conversion points:
- `vlocity_cmt__OmniScript__c` becomes `OmniProcess`
- `vlocity_cmt__PropertySet__c` becomes `PropertySetConfig`
- `vlocity_cmt__DRBundle__c` becomes `OmniDataTransform`
- `vlocity_cmt__Definition__c` on FlexCards becomes `DataSourceConfig` on `OmniUiCard`
- `IsIntegrationProcedure` boolean discriminates OmniScripts from IPs in Core

## Gotchas

| Issue | Detail |
|-------|--------|
| **Namespace conflicts** | During migration, both old and new namespace objects may exist. Always detect namespace before querying. |
| **DataRaptor vs Data Mapper naming** | "DataRaptor" is the legacy name. Core namespace uses "Data Mapper" terminology and `OmniDataTransform` API name, but element types in PropertySetConfig still say "DataRaptor". |
| **Versioning** | Only one version can be active per Type/SubType/Language triplet. Activating a new version automatically deactivates the previous one. |
| **LWC vs Aura OmniScripts** | LWC OmniScripts cannot embed Aura components. CSS classes differ. Event handling is different. Test both if migrating. |
| **IP caching with DML** | Caching an IP that performs DML silently skips the DML on cache hits. Never cache write operations. |
| **Deployment order** | Components must deploy bottom-up: Data Mappers, then IPs, then OmniScripts, then FlexCards. Deploying out of order causes broken references. |
| **FlexCard stores config differently in Core** | Core namespace `OmniUiCard` splits configuration across `DataSourceConfig` and `PropertySetConfig` fields — there is no single `Definition` blob like Vlocity used. |
| **OmniProcessType is computed** | The `OmniProcessType` picklist on `OmniProcess` is derived from `IsIntegrationProcedure`. You cannot set it directly on create. |
| **CLI record creation fails for JSON fields** | Textarea fields containing JSON (like `PropertySetConfig`) break `sf data create record`. Instead, POST the full record body via `sf api request rest --body @file.json`. |
| **Foreign key spelling trap** | `OmniDataTransformItem` links to its parent via `OmniDataTransformationId` — the field uses the long-form spelling, which trips up queries using the short form. |
| **Data source type is plural** | When configuring a FlexCard to call an IP, the `dataSource.type` value must be `IntegrationProcedures` — the singular form silently fails. |
| **Draft components** | Draft Data Mappers cannot be retrieved via `sf project retrieve start`. Only active ones are retrievable. |

## Workflow

1. **Detect namespace** using the probe queries above
2. **Inventory existing components** -- query all OmniScripts, IPs, FlexCards, and Data Mappers
3. **Map dependencies** between components before making changes
4. **Build bottom-up** -- Data Mappers, then IPs, then OmniScripts, then FlexCards
5. **Deploy in dependency order** to avoid broken references
6. **Activate components** after deployment (inactive components are not callable at runtime)
7. **Test end-to-end** -- verify data flows from Data Mapper through IP to OmniScript/FlexCard

### CLI Quick Reference

```bash
# List OmniScripts
sf data query -q "SELECT Id,Type,SubType,Language,IsActive,VersionNumber FROM OmniProcess WHERE IsIntegrationProcedure=false" -o <org>

# List Integration Procedures
sf data query -q "SELECT Id,Type,SubType,IsActive FROM OmniProcess WHERE IsIntegrationProcedure=true" -o <org>

# List FlexCards
sf data query -q "SELECT Id,Name,IsActive FROM OmniUiCard" -o <org>

# List Data Mappers
sf data query -q "SELECT Id,Name,Type,IsActive FROM OmniDataTransform" -o <org>

# Retrieve OmniStudio metadata
sf project retrieve start -m OmniScript:<Name> -o <org>
sf project retrieve start -m OmniIntegrationProcedure:<Name> -o <org>
sf project retrieve start -m OmniUiCard:<Name> -o <org>
sf project retrieve start -m OmniDataTransform:<Name> -o <org>

# Deploy OmniStudio metadata (respect dependency order)
sf project deploy start -m OmniDataTransform -o <org>
sf project deploy start -m OmniIntegrationProcedure -o <org>
sf project deploy start -m OmniScript -o <org>
sf project deploy start -m OmniUiCard -o <org>
```

## References

- [OmniStudio Reference](references/omnistudio-reference.md) -- namespace field mapping, metadata structures, element types, deployment order, migration checklist
