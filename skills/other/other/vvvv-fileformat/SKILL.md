---
name: vvvv-fileformat
description: "Describes the .vl XML file format used by vvvv gamma — document structure, element hierarchy, ID system (base62 GUIDs), NodeReference/Choice patterns, Pins, Pads (IOBoxes), Links, ProcessDefinition/Fragment lifecycle, regions (If/ForEach/Cache), type definitions, TypeAnnotations, and property serialization. Use when generating, parsing, or modifying .vl files programmatically, or when understanding the structure of vvvv patches at the XML level."
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Kopffarben 
  version: "1.0"
---

# VL File Format (.vl)

## Overview

A `.vl` file is an XML document encoding a visual dataflow program for vvvv gamma. Key elements:

- **Document** — root element, contains dependencies and one top-level Patch
- **Patch** — container for visual elements (Nodes, Pads, Links, Canvases)
- **Node** — operation calls, type definitions, or regions
- **Pin** — input/output on a Node (defined at definition site)
- **Pad** — visual data element (IOBox) for displaying/editing values
- **Link** — connects two endpoints by referencing their IDs
- **Canvas** — visual grouping container (no logical scope)
- **ProcessDefinition** — lifecycle definition (Create, Update) via Fragments
- **Slot** — state field within a type definition

## XML Root and Namespaces

```xml
<?xml version="1.0" encoding="utf-8"?>
<Document xmlns:p="property" xmlns:r="reflection" Id="C2vqbtoStWoOI1eKIKZBBM"
          LanguageVersion="2024.6.0" Version="0.128">
  <!-- dependencies and patch -->
</Document>
```

| Prefix | URI | Purpose |
|--------|-----|---------|
| `p` | `property` | **Required.** Complex properties as child elements (`<p:NodeReference>`) |
| `r` | `reflection` | Optional. Only when using `r:IsNull="true"` for explicit null values |

Root attributes: `Id` (base62 GUID), `LanguageVersion` (e.g. `"2024.6.0"`), `Version` (always `"0.128"`).

## ID System

Every element has a unique `Id` — a **22-character base62-encoded GUID** using `[0-9A-Za-z]`. All IDs must be unique within the document. Generate via `GUIDEncoders.GuidTobase62(Guid.NewGuid())`.

Link `Ids` attribute: comma-separated `"sourceId,sinkId"` (output first, input second).

## Element Hierarchy

```
Document
├── NugetDependency (0..n)
├── DocumentDependency (0..n)
├── PlatformDependency (0..n)
└── Patch (exactly 1, top-level)
    ├── Canvas (DefaultCategory, CanvasType="FullCategory")
    └── Node (Name="Application")
        └── Patch (inner)
            ├── Canvas (CanvasType="Group")
            │   ├── Node (operation calls)
            │   ├── Pad (IOBoxes)
            │   └── ...
            ├── Patch (Name="Create")
            ├── Patch (Name="Update")
            ├── ProcessDefinition
            │   ├── Fragment → Create patch
            │   └── Fragment → Update patch
            └── Link (0..n)
```

**Critical**: Dependencies are direct children of `Document`, NOT inside `Patch`.

## Dependencies

```xml
<NugetDependency Id="..." Location="VL.CoreLib" Version="2024.6.0" />
<DocumentDependency Id="..." Location="./MyOtherFile.vl" />
<PlatformDependency Id="..." Location="VL.Core.dll" />
```

Almost every document needs `VL.CoreLib`. Use `IsForward="true"` to re-export types to consumers.

## NodeReference System (Choices)

The `<p:NodeReference>` property defines what a Node IS. It contains `<Choice>` elements that identify the target symbol.

### Operation Call

```xml
<p:NodeReference LastCategoryFullName="Primitive.Math" LastDependency="CoreLibBasics.vl">
  <Choice Kind="NodeFlag" Name="Node" Fixed="true" />
  <Choice Kind="OperationCallFlag" Name="+" />
</p:NodeReference>
```

- First Choice: `Kind="NodeFlag"` with `Fixed="true"` (shape indicator)
- Second Choice: `ProcessAppFlag` (stateful) or `OperationCallFlag` (stateless)

### Type Definitions

```xml
<!-- Process -->
<Choice Kind="ContainerDefinition" Name="Process" />
<CategoryReference Kind="Category" Name="Primitive" />

<!-- Class / Record / Interface / Forward -->
<Choice Kind="ClassDefinition" Name="Class" />
<Choice Kind="RecordDefinition" Name="Record" />
<Choice Kind="InterfaceDefinition" Name="Interface" />
<Choice Kind="ForwardDefinition" Name="Forward" />
```

### Regions

```xml
<Choice Kind="StatefulRegion" Name="Region (Stateful)" Fixed="true" />
<CategoryReference Kind="Category" Name="Primitive" />
<Choice Kind="ApplicationStatefulRegion" Name="If" />  <!-- or ForEach, Cache -->
```

Regions use `StatefulRegion` as the FIRST Choice (not `NodeFlag`). Use `ApplicationStatefulRegion` for If/ForEach or `ProcessStatefulRegion` for Cache.

## Node Element

```xml
<Node Name="MyNode" Bounds="300,200,65,19" Id="...">
  <p:NodeReference>...</p:NodeReference>
  <Pin Id="..." Name="Input" Kind="InputPin" />
  <Pin Id="..." Name="Output" Kind="OutputPin" />
</Node>
```

Key attributes: `Id`, `Name`, `Bounds` (`"X,Y"` or `"X,Y,W,H"`), `Summary`, `Tags`.

## Pin Element

```xml
<Pin Id="..." Name="Value" Kind="InputPin" DefaultValue="42" />
<Pin Id="..." Name="Result" Kind="OutputPin" />
```

Kind values: `InputPin`, `OutputPin`, `StateInputPin`, `StateOutputPin`, `ApplyPin`.

Visibility: `Visible` (default), `Optional`, `OnCreateDefault`, `Hidden`.

## Pad Element (IOBox)

```xml
<Pad Id="..." Bounds="200,160,80,20" ShowValueBox="true" isIOBox="true" Value="3.14"
     Comment="My Value">
  <p:TypeAnnotation LastCategoryFullName="Primitive" LastDependency="CoreLibBasics.vl">
    <Choice Kind="TypeFlag" Name="Float32" />
  </p:TypeAnnotation>
</Pad>
```

Note the lowercase `i` in `isIOBox`. Common types: `Boolean`, `Int32`, `Float32`, `Float64`, `String`, `Vector2`, `Vector3`.

### Comment Pad

```xml
<Pad Id="..." Bounds="100,100,400,25" ShowValueBox="true" isIOBox="true"
     Value="Title text here">
  <p:TypeAnnotation><Choice Kind="TypeFlag" Name="String" /></p:TypeAnnotation>
  <p:ValueBoxSettings>
    <p:fontsize p:Type="Int32">14</p:fontsize>
    <p:stringtype p:Assembly="VL.Core" p:Type="VL.Core.StringType">Comment</p:stringtype>
  </p:ValueBoxSettings>
</Pad>
```

## Link Element

```xml
<Link Id="..." Ids="outputPinId,inputPinId" />
```

`Ids` format: `"sourceId,sinkId"` — output first, input second. Use `IsFeedback="true"` for feedback loops, `IsHidden="true"` for reference links.

## ProcessDefinition and Fragments

```xml
<Patch Id="innerPatchId">
  <Canvas Id="..." CanvasType="Group" />
  <Patch Id="createId" Name="Create" />
  <Patch Id="updateId" Name="Update" />
  <ProcessDefinition Id="...">
    <Fragment Id="..." Patch="createId" Enabled="true" />
    <Fragment Id="..." Patch="updateId" Enabled="true" />
  </ProcessDefinition>
</Patch>
```

Fragment `Patch` attribute references a sibling `<Patch>` element's `Id`.

## Regions

Regions use 4-value Bounds (`"X,Y,W,H"`) and have ControlPoints at borders:

```xml
<Node Bounds="100,200,400,300" Id="...">
  <p:NodeReference LastCategoryFullName="Primitive" LastDependency="Builtin">
    <Choice Kind="StatefulRegion" Name="Region (Stateful)" Fixed="true" />
    <CategoryReference Kind="Category" Name="Primitive" />
    <Choice Kind="ApplicationStatefulRegion" Name="If" />
  </p:NodeReference>
  <Patch Id="...">
    <Canvas Id="..." CanvasType="Group"><!-- content --></Canvas>
    <Patch Id="thenId" Name="Then" />
    <Fragment Id="..." Patch="thenId" Enabled="true" />
  </Patch>
  <ControlPoint Id="..." Bounds="150,200" Alignment="Top" />
  <ControlPoint Id="..." Bounds="150,500" Alignment="Bottom" />
</Node>
```

Region patch names: If uses `Then`/`Else`, ForEach uses `Create`/`Update`/`Dispose`, Cache uses `Create`/`Update`.

## TypeAnnotation

```xml
<!-- Simple type -->
<p:TypeAnnotation>
  <Choice Kind="TypeFlag" Name="Float32" />
</p:TypeAnnotation>

<!-- Generic type: Spread<RGBA> -->
<p:TypeAnnotation LastCategoryFullName="Collections" LastDependency="VL.Collections.vl">
  <Choice Kind="TypeFlag" Name="Spread" />
  <p:TypeArguments>
    <TypeReference LastCategoryFullName="Color" LastDependency="CoreLibBasics.vl">
      <Choice Kind="TypeFlag" Name="RGBA" />
    </TypeReference>
  </p:TypeArguments>
</p:TypeAnnotation>
```

## Slot Element (State Fields)

```xml
<Slot Id="..." Name="MyField">
  <p:TypeAnnotation><Choice Kind="TypeFlag" Name="Float32" /></p:TypeAnnotation>
  <p:Value>0.5</p:Value>
</Slot>
```

## Complete Minimal Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<Document xmlns:p="property" Id="A1b2C3d4E5f6G7h8I9j0Kl"
          LanguageVersion="2024.6.0" Version="0.128">
  <NugetDependency Id="B2c3D4e5F6g7H8i9J0k1Lm" Location="VL.CoreLib"
                   Version="2024.6.0" />
  <Patch Id="C3d4E5f6G7h8I9j0K1l2Mn">
    <Canvas Id="D4e5F6g7H8i9J0k1L2m3No" DefaultCategory="Main"
            BordersChecked="false" CanvasType="FullCategory" />
    <Node Name="Application" Bounds="100,100" Id="E5f6G7h8I9j0K1l2M3n4Op">
      <p:NodeReference>
        <Choice Kind="ContainerDefinition" Name="Process" />
        <CategoryReference Kind="Category" Name="Primitive" />
      </p:NodeReference>
      <Patch Id="F6g7H8i9J0k1L2m3N4o5Pq">
        <Canvas Id="G7h8I9j0K1l2M3n4O5p6Qr" CanvasType="Group" />
        <Patch Id="H8i9J0k1L2m3N4o5P6q7Rs" Name="Create" />
        <Patch Id="I9j0K1l2M3n4O5p6Q7r8St" Name="Update" />
        <ProcessDefinition Id="J0k1L2m3N4o5P6q7R8s9Tu">
          <Fragment Id="K1l2M3n4O5p6Q7r8S9t0Uv"
                   Patch="H8i9J0k1L2m3N4o5P6q7Rs" Enabled="true" />
          <Fragment Id="L2m3N4o5P6q7R8s9T0u1Vw"
                   Patch="I9j0K1l2M3n4O5p6Q7r8St" Enabled="true" />
        </ProcessDefinition>
      </Patch>
    </Node>
  </Patch>
</Document>
```

## Validation Rules

1. All IDs must be unique (22-char base62 GUIDs)
2. `xmlns:p="property"` must be on `Document`
3. `Version="0.128"` always required
4. Fragment `Patch` must reference existing sibling Patch IDs
5. Link `Ids`: exactly `"sourceId,sinkId"` — output first
6. `CanvasType="FullCategory"` only for root canvas
7. Every document needs `VL.CoreLib` dependency
8. Application node is the entry point (Name="Application", ContainerDefinition)
9. Element names are case-sensitive (`Patch` not `patch`)
10. `isIOBox` uses lowercase `i`
11. Dependencies are children of `Document`, not `Patch`

## Common Mistakes

- Forgetting `xmlns:p="property"` namespace declaration
- Putting dependencies inside `Patch` instead of `Document`
- Reversed Link direction (first ID must be source/output)
- Missing ProcessDefinition for process/class type definitions
- Wrong Bounds format (use commas, no spaces: `"100,200,65,19"`)
- Using `IsIOBox` instead of `isIOBox`

For the complete element reference with all attributes, Choice kinds, and serialization details, see [format-reference.md](format-reference.md).
For layout conventions, spacing, positioning, and visual organization best practices, see [best-practices.md](best-practices.md).
