---
name: "data-model-designer"
description: "Design data models for construction projects. Create entity-relationship diagrams, define schemas, and generate database structures."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📐", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Data Model Designer

## Business Case

### Problem Statement
Construction data management challenges:
- Fragmented data across systems
- Inconsistent data structures
- Missing relationships between entities
- Difficult data integration

### Solution
Systematic data model design for construction projects, defining entities, relationships, and schemas for effective data management.

## Technical Implementation

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class DataType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TEXT = "text"
    JSON = "json"


class RelationType(Enum):
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_MANY = "N:M"


class ConstraintType(Enum):
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    UNIQUE = "unique"
    NOT_NULL = "not_null"


@dataclass
class Field:
    name: str
    data_type: DataType
    nullable: bool = True
    default: Any = None
    description: str = ""
    constraints: List[ConstraintType] = field(default_factory=list)


@dataclass
class Entity:
    name: str
    description: str
    fields: List[Field] = field(default_factory=list)
    primary_key: str = "id"


@dataclass
class Relationship:
    name: str
    from_entity: str
    to_entity: str
    relation_type: RelationType
    from_field: str
    to_field: str


class ConstructionDataModel:
    """Design data models for construction projects."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []

    def add_entity(self, entity: Entity):
        """Add entity to model."""
        self.entities[entity.name] = entity

    def add_relationship(self, relationship: Relationship):
        """Add relationship between entities."""
        self.relationships.append(relationship)

    def create_entity(self, name: str, description: str,
                      fields: List[Dict[str, Any]]) -> Entity:
        """Create entity from field definitions."""

        entity_fields = [
            Field(
                name=f['name'],
                data_type=DataType(f.get('type', 'string')),
                nullable=f.get('nullable', True),
                default=f.get('default'),
                description=f.get('description', ''),
                constraints=[ConstraintType(c) for c in f.get('constraints', [])]
            )
            for f in fields
        ]

        entity = Entity(name=name, description=description, fields=entity_fields)
        self.add_entity(entity)
        return entity

    def create_relationship(self, from_entity: str, to_entity: str,
                           relation_type: str = "1:N",
                           from_field: str = None) -> Relationship:
        """Create relationship between entities."""

        rel = Relationship(
            name=f"{from_entity}_{to_entity}",
            from_entity=from_entity,
            to_entity=to_entity,
            relation_type=RelationType(relation_type),
            from_field=from_field or f"{to_entity.lower()}_id",
            to_field="id"
        )
        self.add_relationship(rel)
        return rel

    def generate_sql_schema(self, dialect: str = "postgresql") -> str:
        """Generate SQL DDL statements."""

        sql = []
        type_map = {
            DataType.STRING: "VARCHAR(255)",
            DataType.INTEGER: "INTEGER",
            DataType.FLOAT: "DECIMAL(15,2)",
            DataType.BOOLEAN: "BOOLEAN",
            DataType.DATE: "DATE",
            DataType.DATETIME: "TIMESTAMP",
            DataType.TEXT: "TEXT",
            DataType.JSON: "JSONB" if dialect == "postgresql" else "JSON"
        }

        for name, entity in self.entities.items():
            columns = []
            for fld in entity.fields:
                col = f"    {fld.name} {type_map.get(fld.data_type, 'VARCHAR(255)')}"
                if not fld.nullable:
                    col += " NOT NULL"
                if ConstraintType.PRIMARY_KEY in fld.constraints:
                    col += " PRIMARY KEY"
                columns.append(col)

            sql.append(f"CREATE TABLE {name} (\n" + ",\n".join(columns) + "\n);")

        for rel in self.relationships:
            sql.append(f"""ALTER TABLE {rel.from_entity}
ADD CONSTRAINT fk_{rel.name}
FOREIGN KEY ({rel.from_field}) REFERENCES {rel.to_entity}({rel.to_field});""")

        return "\n\n".join(sql)

    def generate_json_schema(self) -> Dict[str, Any]:
        """Generate JSON Schema representation."""

        schemas = {}
        for name, entity in self.entities.items():
            properties = {}
            required = []

            for fld in entity.fields:
                prop = {"description": fld.description}
                if fld.data_type == DataType.STRING:
                    prop["type"] = "string"
                elif fld.data_type == DataType.INTEGER:
                    prop["type"] = "integer"
                elif fld.data_type == DataType.FLOAT:
                    prop["type"] = "number"
                elif fld.data_type == DataType.BOOLEAN:
                    prop["type"] = "boolean"
                else:
                    prop["type"] = "string"

                properties[fld.name] = prop
                if not fld.nullable:
                    required.append(fld.name)

            schemas[name] = {
                "type": "object",
                "title": entity.description,
                "properties": properties,
                "required": required
            }
        return schemas

    def generate_er_diagram(self) -> str:
        """Generate Mermaid ER diagram."""

        lines = ["erDiagram"]
        for name, entity in self.entities.items():
            for fld in entity.fields[:5]:
                lines.append(f"    {name} {{")
                lines.append(f"        {fld.data_type.value} {fld.name}")
                lines.append("    }")

        for rel in self.relationships:
            rel_symbol = {
                RelationType.ONE_TO_ONE: "||--||",
                RelationType.ONE_TO_MANY: "||--o{",
                RelationType.MANY_TO_MANY: "}o--o{"
            }.get(rel.relation_type, "||--o{")
            lines.append(f"    {rel.from_entity} {rel_symbol} {rel.to_entity} : \"{rel.name}\"")

        return "\n".join(lines)

    def validate_model(self) -> List[str]:
        """Validate data model for issues."""

        issues = []
        for rel in self.relationships:
            if rel.from_entity not in self.entities:
                issues.append(f"Missing entity: {rel.from_entity}")
            if rel.to_entity not in self.entities:
                issues.append(f"Missing entity: {rel.to_entity}")

        for name, entity in self.entities.items():
            has_pk = any(ConstraintType.PRIMARY_KEY in f.constraints for f in entity.fields)
            if not has_pk:
                issues.append(f"Entity '{name}' has no primary key")

        return issues


class ConstructionEntities:
    """Standard construction data entities."""

    @staticmethod
    def project_entity() -> Entity:
        return Entity(
            name="projects",
            description="Construction projects",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("code", DataType.STRING, False, constraints=[ConstraintType.UNIQUE]),
                Field("name", DataType.STRING, False),
                Field("status", DataType.STRING),
                Field("start_date", DataType.DATE),
                Field("end_date", DataType.DATE),
                Field("budget", DataType.FLOAT)
            ]
        )

    @staticmethod
    def activity_entity() -> Entity:
        return Entity(
            name="activities",
            description="Schedule activities",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("project_id", DataType.INTEGER, False),
                Field("wbs_code", DataType.STRING),
                Field("name", DataType.STRING, False),
                Field("start_date", DataType.DATE),
                Field("end_date", DataType.DATE),
                Field("percent_complete", DataType.FLOAT)
            ]
        )

    @staticmethod
    def cost_item_entity() -> Entity:
        return Entity(
            name="cost_items",
            description="Project cost items",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("project_id", DataType.INTEGER, False),
                Field("wbs_code", DataType.STRING),
                Field("description", DataType.STRING),
                Field("budgeted_cost", DataType.FLOAT),
                Field("actual_cost", DataType.FLOAT)
            ]
        )
```

## Quick Start

```python
# Create model
model = ConstructionDataModel("Office Building A")

# Add standard entities
model.add_entity(ConstructionEntities.project_entity())
model.add_entity(ConstructionEntities.activity_entity())
model.add_entity(ConstructionEntities.cost_item_entity())

# Add relationships
model.create_relationship("activities", "projects")
model.create_relationship("cost_items", "projects")

# Generate SQL
sql = model.generate_sql_schema("postgresql")
print(sql)
```

## Common Use Cases

### 1. Custom Entity
```python
model.create_entity(
    name="change_orders",
    description="Project change orders",
    fields=[
        {"name": "id", "type": "integer", "nullable": False, "constraints": ["primary_key"]},
        {"name": "project_id", "type": "integer", "nullable": False},
        {"name": "amount", "type": "float"},
        {"name": "status", "type": "string"}
    ]
)
```

### 2. Generate ER Diagram
```python
er_diagram = model.generate_er_diagram()
print(er_diagram)
```

### 3. Validate Model
```python
issues = model.validate_model()
for issue in issues:
    print(f"Issue: {issue}")
```

## Resources
- **DDC Book**: Chapter 2.5 - Data Models and Standards
- **Website**: https://datadrivenconstruction.io
