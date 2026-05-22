---
name: schema-analyzer
description: >
  Analyze MongoDB collection schemas, infer data types, detect inconsistencies,
  and recommend schema design improvements. Use when the user asks about database
  structure, data modeling, schema validation, or wants to understand their
  MongoDB collections.
---

# MongoDB Schema Analyzer

You analyze MongoDB schemas to understand data structure, detect problems, and recommend improvements.

## Analysis Process

1. **Sample documents**: Fetch 100 random documents from the collection
2. **Infer types**: Detect field types, nesting depth, array contents
3. **Check consistency**: Find fields that vary in type or presence
4. **Assess design**: Evaluate embedding vs referencing choices
5. **Recommend**: Suggest schema validation rules, indexes, and restructuring

## Schema Discovery Script

Run this to analyze a collection's schema:

```bash
mongosh "$MONGODB_URI" --quiet --eval "
  const coll = '<COLLECTION>';
  const sample = db.getCollection(coll).aggregate([{ \$sample: { size: 100 } }]).toArray();

  const schema = {};
  sample.forEach(doc => {
    function analyze(obj, prefix) {
      Object.entries(obj).forEach(([key, val]) => {
        const path = prefix ? prefix + '.' + key : key;
        const type = Array.isArray(val) ? 'array' : typeof val;
        if (!schema[path]) schema[path] = { types: {}, count: 0 };
        schema[path].types[type] = (schema[path].types[type] || 0) + 1;
        schema[path].count++;
        if (type === 'object' && val !== null) analyze(val, path);
      });
    }
    analyze(doc, '');
  });

  Object.entries(schema)
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([path, info]) => {
      const types = Object.entries(info.types).map(([t, c]) => t + '(' + c + ')').join(', ');
      print(path + '  |  ' + types + '  |  present in ' + info.count + '/100 docs');
    });
"
```

## Schema Validation

Recommend JSON Schema validation rules when appropriate:

```javascript
db.runCommand({
  collMod: "collection",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email", "createdAt"],
      properties: {
        name: { bsonType: "string", description: "must be a string" },
        email: { bsonType: "string", pattern: "^.+@.+$" },
        age: { bsonType: "int", minimum: 0, maximum: 150 },
        createdAt: { bsonType: "date" }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "warn"
})
```

## Schema Design Guidelines

### When to Embed (denormalize)
- Data is read together frequently
- Child documents are bounded in number
- One-to-few relationships
- Data doesn't change independently

### When to Reference (normalize)
- Data is large or unbounded
- Many-to-many relationships
- Data is read independently
- Documents would exceed 16MB limit

### Anti-patterns to Flag
- Arrays that grow without bound (unbounded arrays)
- Deeply nested documents (>3 levels)
- Storing large blobs in documents
- Inconsistent field types across documents
- Missing indexes on frequently queried fields
- Using `$where` or JavaScript expressions in queries
