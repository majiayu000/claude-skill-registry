---
name: creating-gorm-entity
description: Creates GORM entity structs for go-kratos microservices with BaseModel embedding, proper field tags, relationships (one-to-one, one-to-many), indexing strategies, and soft delete support. Use when defining database schema, creating new entities, setting up table relationships, or configuring database constraints.
---

# GORM Entity Creation Skill

## Purpose

Generate GORM entity structs that follow the project's Clean Architecture patterns, with proper field tags, relationships, indexing strategies, and soft delete support.

## Essential Patterns

### 1. BaseModel Pattern

All entities MUST embed `BaseModel` which provides:
- `ID uint64` - Primary key with auto-increment
- `CreatedAt time.Time` - Automatic timestamp
- `UpdatedAt time.Time` - Automatic timestamp
- `DeletedAt gorm.DeletedAt` - Soft delete support with index

```go
type BaseModel struct {
    ID        uint64 `gorm:"primaryKey;autoIncrement"`
    CreatedAt time.Time
    UpdatedAt time.Time
    DeletedAt gorm.DeletedAt `gorm:"index"`
}
```

### 2. Field Ordering Rules

Fields MUST follow this exact order:
1. BaseModel embedding (always first)
2. Foreign keys (e.g., ProjectID, SymbolID)
3. Required business fields (UID, Label, ClassName, etc.)
4. Optional fields
5. Relationship fields (pointer types with gorm tags)

**Example:**
```go
type Symbol struct {
    BaseModel                                    // 1. Base embedding
    ProjectID       uint64      `gorm:"..."     // 2. Foreign key
    UID             string      `gorm:"..."     // 3. Required fields
    Label           string      `gorm:"..."
    ClassName       string      `gorm:"..."
    ComponentTarget string      `gorm:"..."
    Version         uint32      `gorm:"..."
    SymbolData      *SymbolData `gorm:"..."     // 4. Relationship
}
```

### 3. GORM Tag Structure

Tags MUST follow this pattern: \`gorm:"constraint1;constraint2;..." json:"field_name"\`

**Common constraints:**
- \`not null\` - Required field
- \`size:255\` - String length limit
- \`uniqueIndex:idx_name,priority:N\` - Unique composite index
- \`index:idx_name,priority:N\` - Non-unique composite index
- \`foreignKey:FieldName\` - FK relationship
- \`references:ID\` - FK reference
- \`constraint:OnDelete:CASCADE\` - FK cascade delete

**Critical indexing patterns:**
```go
// Composite unique index (project_id + uid)
ProjectID uint64 \`gorm:"not null;uniqueIndex:idx_project_uid,priority:1" json:"project_id"\`
UID       string \`gorm:"not null;size:255;uniqueIndex:idx_project_uid,priority:2" json:"uid"\`

// Multiple indexes on same field
ProjectID uint64 \`gorm:"not null;uniqueIndex:idx_project_uid,priority:1;index:idx_project_id,priority:1;index:idx_symbols_project_deleted_at,priority:1" json:"project_id"\`
```

### 4. Relationship Patterns

**One-to-One with Cascade Delete:**
```go
type Symbol struct {
    BaseModel
    // ... other fields ...
    SymbolData *SymbolData \`gorm:"foreignKey:SymbolID;references:ID;constraint:OnDelete:CASCADE" json:"symbol_data,omitempty"\`
}

type SymbolData struct {
    BaseModel
    SymbolID uint64  \`gorm:"not null;uniqueIndex" json:"symbol_id"\`
    Data     *[]byte \`gorm:"not null;type:longblob" json:"data"\`
}
```

### 5. Table Naming

MUST provide explicit table name method:

```go
func (Symbol) TableName() string {
    return "symbols"  // plural, snake_case
}
```

## Validation Checklist

When creating a GORM entity, verify:

- [ ] BaseModel is embedded as first field
- [ ] All foreign keys come before business fields  
- [ ] Required fields have \`not null\` tag
- [ ] String fields have \`size:N\` constraint
- [ ] Unique combinations use \`uniqueIndex\` with priorities
- [ ] Frequently queried fields are indexed
- [ ] Foreign keys have proper relationship tags
- [ ] Cascade deletes are configured where needed
- [ ] TableName() method returns plural snake_case
- [ ] JSON tags use snake_case naming
- [ ] Pointer types used for optional relationships
- [ ] \`omitempty\` added to optional json fields

## Anti-Patterns

❌ **DON'T:**
- Use \`gorm.Model\` (use \`BaseModel\` instead)
- Forget to index foreign keys
- Use value types for optional relationships
- Mix camelCase and snake_case in json tags
- Omit \`TableName()\` method
- Put relationship fields before business fields

✅ **DO:**
- Always embed \`BaseModel\`
- Index all foreign keys
- Use pointer types for optional relationships
- Use snake_case for all json tags
- Provide explicit \`TableName()\` method
- Follow field ordering rules

