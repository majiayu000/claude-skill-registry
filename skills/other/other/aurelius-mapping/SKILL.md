---
name: aurelius-mapping
description: Map Delphi classes to a relational database using TMS Aurelius ORM attributes. Use when the user asks to create entity classes, add Aurelius mapping to existing classes, fix or review mapping attributes, explain how a class is mapped, or work with associations, inheritance, automapping, nullable fields, blobs, or composite identifiers. Triggers on requests like "create Aurelius entities for...", "map this class to Aurelius", "add ORM mapping", "fix the mapping on this class", "how do I map a one-to-many in Aurelius".
---

# Aurelius Mapping

Map Delphi classes to a relational database using TMS Aurelius attributes. All attributes are declared in unit `Aurelius.Mapping.Attributes`.

Read `references/mapping.md` for all attribute syntax, options tables, and code examples. The guidance below covers decisions and rules that the reference does not emphasize.

## Approach

**New schema (no existing tables):** Default to `[Automapping]`. It infers table names, column names, nullability, and the identifier from field naming conventions, requiring no extra attributes for simple cases.

**Legacy or fixed schema:** Use explicit attributes (`[Table]`, `[Column]`, `[Id]`, etc.) to match the existing column and table names exactly.

**Mixed:** Automapping is not all-or-nothing — add explicit attributes only where the defaults need to be overridden.

When the user hasn't specified, ask or infer from context (existing table definitions → explicit; greenfield → automapping).

## Critical Rules

These are the most common mistakes. Apply them without exception.

### Object lifetime — associations

- **Never** create or free a many-to-one associated object in the parent's constructor or destructor. Aurelius owns the lifetime of associated entity objects.
- Use plain `T` field type for eager associations; use `Proxy<T>` field type for lazy associations.
- Expose lazy associations through a property that returns `FArtist.Value`.

### Object lifetime — collections

- **Do** create and free the `TList<T>` container in the parent's constructor and destructor.
- **Never** create or free the child entity objects inside the list — Aurelius manages them.
- Do **not** use `TObjectList<T>` with `OwnsObjects = True`.
- For lazy collections, use `Proxy<TList<T>>` as the field type. Use `SetInitialValue`/`DestroyValue` instead of accessing `.Value` in constructor/destructor.

### Registering entities

Always add `RegisterEntity` calls in the `initialization` section of the unit:

```delphi
initialization
  RegisterEntity(TCustomer);
  RegisterEntity(TCountry);
```

This prevents the Delphi linker from removing the class. It is especially important in server applications (XData services) where entity classes may not be directly referenced in code.

## Reference

For all attribute signatures, options, and full code examples, read [references/mapping.md](references/mapping.md).

The reference covers: basic entity mapping, automapping rules and overrides, abstract entities, nullable fields, blob fields, many-to-one associations (eager and lazy), one-to-many associations (bidirectional and unidirectional, eager and lazy), collection ordering and filtering, foreign key naming, single-table and joined-tables inheritance, composite identifiers.
