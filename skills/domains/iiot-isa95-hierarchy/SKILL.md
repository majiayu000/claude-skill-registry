---
name: iiot-isa95-hierarchy
description: ISA-95 equipment hierarchy for IIoT asset modeling. Enterprise → Site → Area → Line → Cell → Equipment → Sensor.
triggers:
  - "ISA-95"
  - "ISA-88"
  - "equipment hierarchy"
  - "asset hierarchy"
  - "plant model"
  - "production line"
  - "work center"
  - "control module"
---

# IIoT ISA-95 Hierarchy

## Overview

ISA-95 (IEC 62264) defines the standard equipment hierarchy for manufacturing. This skill provides guidance for modeling IIoT assets following these industry standards.

## Hierarchy Levels

### Equipment Hierarchy (Physical Assets)

```
Enterprise
└── Site
    └── Area
        └── Production Line (Work Center)
            └── Work Cell (Work Unit)
                └── Equipment Module
                    └── Control Module (Sensor/Actuator)
```

### Automation Levels (Data Flow / ISA-95 Pyramid)

| Level | Name | Systems | Data Flow |
|-------|------|---------|-----------|
| L4 | Business Planning | ERP, BI | Strategic planning, finance |
| L3 | Manufacturing Operations | MES, MOM | Production scheduling, quality |
| L2 | Supervisory Control | SCADA, HMI | Real-time monitoring, alarms |
| L1 | Automation Control | PLC, DCS | Process control logic |
| L0 | Physical Process | Sensors, Actuators | Physical measurements |

## TMNL Schema Mapping

| ISA-95 Term | TMNL Schema | Graph Label | File Location |
|-------------|-------------|-------------|---------------|
| Site/Area | `Plant` | `:plant` | `docker/iiot-db/init.sql:53` |
| Production Line | `Line` | `:line` | `docker/iiot-db/init.sql:62` |
| Work Cell | `Machine` | `:machine` | `docker/iiot-db/init.sql:76` |
| Control Module | `Sensor` | `:sensor` | `docker/iiot-db/init.sql:92` |

## Decision Tree: Asset Classification

```
Modeling a physical asset?
│
├─ Facility/Building scope?
│  ├─ Multiple facilities?
│  │  └─ Use: Enterprise (extend schema if needed)
│  └─ Single facility?
│     └─ Use: Plant (ISA-95 Site/Area)
│
├─ Production sequence scope?
│  ├─ Multiple sequential steps?
│  │  └─ Use: Line (ISA-95 Work Center)
│  └─ Single processing area?
│     └─ Use: Area (optional sub-plant zone)
│
├─ Single equipment/machine?
│  ├─ Multiple coordinated units?
│  │  └─ Use: Work Cell (group of machines)
│  └─ Individual machine?
│     └─ Use: Machine (ISA-95 Equipment Module)
│
└─ Measurement/control point?
   ├─ Sensor (reads values)?
   │  └─ Use: Sensor (ISA-95 Control Module)
   └─ Actuator (writes values)?
      └─ Use: Actuator (ISA-95 Control Module)
```

## Graph Relationships (Apache AGE)

### Standard Edge Types

| Relationship | From | To | Meaning |
|--------------|------|-----|---------|
| `[:contains]` | Plant | Line | Facility contains production line |
| `[:contains]` | Line | Machine | Line contains equipment |
| `[:monitors]` | Sensor | Machine | Sensor monitors equipment |
| `[:controls]` | Actuator | Machine | Actuator controls equipment |
| `[:triggered_by]` | Alarm | Sensor | Alarm triggered by sensor reading |
| `[:caused]` | Alarm | Alarm | Alarm causality chain |

### Creating Hierarchy in Cypher

```sql
-- Create plant (ISA-95 Site)
SELECT * FROM cypher('iiot', $$
    CREATE (:plant {
        id: 'PLANT-A',
        name: 'Chicago Assembly',
        location: 'Chicago, IL',
        timezone: 'America/Chicago'
    })
$$) AS (v agtype);

-- Create line (ISA-95 Work Center)
SELECT * FROM cypher('iiot', $$
    CREATE (:line {
        id: 'LINE-001',
        name: 'Body Assembly',
        plant_id: 'PLANT-A',
        capacity: 60  -- units per hour
    })
$$) AS (v agtype);

-- Create relationship
SELECT * FROM cypher('iiot', $$
    MATCH (p:plant {id: 'PLANT-A'}), (l:line {id: 'LINE-001'})
    CREATE (p)-[:contains]->(l)
$$) AS (e agtype);

-- Create machine (ISA-95 Equipment Module)
SELECT * FROM cypher('iiot', $$
    CREATE (:machine {
        id: 'MCH-001',
        name: 'Welding Robot Alpha',
        model: 'FANUC R-2000iC/210F',
        line_id: 'LINE-001',
        commissioned_date: '2023-01-15'
    })
$$) AS (v agtype);

-- Create sensor (ISA-95 Control Module)
SELECT * FROM cypher('iiot', $$
    CREATE (:sensor {
        device_id: 'TMP-001',
        type: 'temperature',
        unit: 'celsius',
        machine_id: 'MCH-001',
        sample_rate_ms: 1000,
        threshold_high: 30,
        threshold_critical: 35
    })
$$) AS (v agtype);
```

### Querying Hierarchy

```sql
-- Get full path from sensor to enterprise
SELECT * FROM cypher('iiot', $$
    MATCH path = (s:sensor {device_id: 'TMP-001'})-[:monitors]->
                 (m:machine)<-[:contains]-
                 (l:line)<-[:contains]-
                 (p:plant)
    RETURN s.device_id, m.name, l.name, p.name
$$) AS (sensor agtype, machine agtype, line agtype, plant agtype);

-- Find all sensors on a specific machine
SELECT * FROM cypher('iiot', $$
    MATCH (m:machine {id: 'MCH-001'})<-[:monitors]-(s:sensor)
    RETURN s.device_id, s.type, s.unit
$$) AS (device_id agtype, type agtype, unit agtype);

-- Get all equipment in a plant (recursive)
SELECT * FROM cypher('iiot', $$
    MATCH (p:plant {id: 'PLANT-A'})-[:contains*]->(asset)
    RETURN labels(asset)[0] AS asset_type, asset.id AS id, asset.name AS name
$$) AS (asset_type agtype, id agtype, name agtype);
```

## Extended Hierarchy (Optional)

For enterprise-scale deployments, extend the schema with additional levels:

```typescript
// src/lib/iiot/schemas/assets.ts

import { Schema } from 'effect'

// Branded identifiers
export const EnterpriseId = Schema.String.pipe(Schema.brand('EnterpriseId'))
export const SiteId = Schema.String.pipe(Schema.brand('SiteId'))
export const AreaId = Schema.String.pipe(Schema.brand('AreaId'))
export const PlantId = Schema.String.pipe(Schema.brand('PlantId'))
export const LineId = Schema.String.pipe(Schema.brand('LineId'))
export const MachineId = Schema.String.pipe(Schema.brand('MachineId'))
export const DeviceId = Schema.String.pipe(Schema.brand('DeviceId'))

// Enterprise (multi-site corporation)
export const Enterprise = Schema.TaggedStruct('Enterprise', {
  id: EnterpriseId,
  name: Schema.NonEmptyString,
  industry: Schema.optional(Schema.String),
})

// Site (physical location)
export const Site = Schema.TaggedStruct('Site', {
  id: SiteId,
  name: Schema.NonEmptyString,
  enterpriseId: EnterpriseId,
  location: Schema.optional(Schema.String),
  timezone: Schema.optional(Schema.String),
})

// Area (sub-plant zone)
export const Area = Schema.TaggedStruct('Area', {
  id: AreaId,
  name: Schema.NonEmptyString,
  siteId: SiteId,
  type: Schema.optional(Schema.Literal('production', 'warehouse', 'maintenance')),
})

// Plant (our current top-level)
export const Plant = Schema.TaggedStruct('Plant', {
  id: PlantId,
  name: Schema.NonEmptyString,
  areaId: Schema.optional(AreaId),  // Optional if using simplified hierarchy
  location: Schema.optional(Schema.String),
})

// Line (production line)
export const Line = Schema.TaggedStruct('Line', {
  id: LineId,
  name: Schema.NonEmptyString,
  plantId: PlantId,
  capacity: Schema.optional(Schema.Number),
})

// Machine (equipment)
export const Machine = Schema.TaggedStruct('Machine', {
  id: MachineId,
  name: Schema.NonEmptyString,
  model: Schema.optional(Schema.String),
  lineId: LineId,
  commissionedDate: Schema.optional(Schema.DateFromString),
})

// Sensor type enumeration
export const SensorType = Schema.Literal(
  'temperature',
  'vibration',
  'humidity',
  'pressure',
  'speed',
  'current',
  'voltage',
  'flow',
  'level'
)

// Sensor (control module)
export const Sensor = Schema.TaggedStruct('Sensor', {
  deviceId: DeviceId,
  type: SensorType,
  unit: Schema.NonEmptyString,
  machineId: MachineId,
  sampleRateMs: Schema.optional(Schema.Number),
  thresholdHigh: Schema.optional(Schema.Number),
  thresholdCritical: Schema.optional(Schema.Number),
})
```

## ISA-88 Integration (Batch Manufacturing)

For batch processes, ISA-88 provides additional concepts:

| ISA-88 Term | Description | Use Case |
|-------------|-------------|----------|
| Process Cell | Logical grouping for batch | Chemical reactors |
| Unit | Equipment that performs batch | Mixing tank |
| Equipment Module | Functional group within unit | Agitator, heater |
| Control Module | Single device | Temperature sensor |
| Recipe | Procedure definition | Batch instructions |
| Phase | Recipe step | Heat, Mix, Cool |

These map to the same physical hierarchy but add procedural concepts for batch control.

## Best Practices

### Naming Conventions

| Asset Type | Pattern | Example |
|------------|---------|---------|
| Plant | `PLANT-{CODE}` | `PLANT-A`, `PLANT-CHI` |
| Line | `LINE-{NNN}` | `LINE-001`, `LINE-042` |
| Machine | `MCH-{NNN}` | `MCH-001`, `MCH-123` |
| Sensor | `{TYPE}-{NNN}` | `TMP-001`, `VIB-002` |
| Alarm | `ALM-{UUID}` | `ALM-abc123...` |

### Sensor Type Prefixes

| Prefix | Type | Unit |
|--------|------|------|
| `TMP` | Temperature | celsius, fahrenheit |
| `VIB` | Vibration | mm/s, g |
| `HUM` | Humidity | percent |
| `PRS` | Pressure | bar, psi |
| `SPD` | Speed | m/min, rpm |
| `CUR` | Current | amps |
| `VLT` | Voltage | volts |
| `FLW` | Flow | L/min, gal/hr |
| `LVL` | Level | percent, meters |

## Related Skills

- `/iiot-unified-namespace` - Topic hierarchy and data flow
- `/nex-effect-services` - Effect-TS service patterns
- `/effect-schema-mastery` - Schema definition patterns

## References

- [ISA-95 Standard](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard)
- [ISA-88 Standard](https://www.isa.org/standards-and-publications/isa-standards/isa-88-standard)
- [IEC 62264 (ISA-95 international)](https://www.iec.ch/iec62264)
