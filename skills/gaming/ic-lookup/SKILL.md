---
name: ic-lookup
description: Look up Stationeers device properties and IC10 instruction syntax. Use when user asks about logic values, device pins, prefab hashes, or IC10 command syntax.
---

# IC10 Lookup

Quick reference lookup for IC10 instructions and device properties.

## Workflow

1. **Parallel Lookup**
   Spawn these agents simultaneously based on query type:
   - `instruction-researcher` - For IC10 instruction syntax
   - `device-researcher` - For device logic types and properties

## Instructions

When the user asks about IC10 syntax or device properties:

1. Determine query type:
   - **Instruction query**: "How do I use [instruction]?", "What's the syntax for...?"
   - **Device query**: "What logic values does [device] have?", "How do I read from...?"
   - **Both**: When question involves using specific instructions with specific devices

2. Launch appropriate researcher(s):
   - For instructions: `instruction-researcher`
   - For devices: `device-researcher`
   - For combined questions: Both in parallel

3. Present results clearly:
   - Instruction syntax with examples
   - Device logic types (readable/writable)
   - Practical IC10 code snippet

4. If the lookup involves batch operations:
   - Include the prefab hash
   - Show lb/sb syntax example

## Quick Reference Cheat Sheet

### Common Instructions
- `l r0 device LogicType` - Read from device
- `s device LogicType value` - Write to device
- `lb r0 hash LogicType mode` - Batch read (0=avg, 1=sum, 2=min, 3=max)
- `sb hash LogicType value` - Batch write

### Common Logic Types
- `On`, `Power`, `Open`, `Lock` - Boolean states
- `Temperature`, `Pressure` - Float values
- `Setting`, `Mode` - Configurable values

## Example Triggers

- "How do I use lb?"
- "What's the syntax for select?"
- "What logic values does the gas sensor have?"
- "What's the prefab hash for..."
- "How do I read temperature?"
- "What can I set on a vent?"
