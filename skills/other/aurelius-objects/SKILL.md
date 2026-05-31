---
name: aurelius-objects
description: Save, load, update, delete, merge, and navigate entity objects using TMS Aurelius ORM (TObjectManager). Use when the user asks how to persist or retrieve data with Aurelius, manage object lifetime, work with associations or collections at runtime, handle transactions, use cached updates, or control concurrency. Does NOT cover query DSL or criteria/projections (those are in a separate skill). Triggers on requests like "save an entity with Aurelius", "load a customer from the database", "add items to a collection", "how do I update an object", "flush changes", "delete a record with Aurelius", "merge a transient object", "how do transactions work in Aurelius", "batch updates Aurelius".
---

## Approach

Always work through a `TObjectManager` instance. All persistence methods (`Save`, `Flush`, `Remove`, etc.) are called on the manager, never written as raw SQL.

**Loading a known id:** use `Manager.Find<T>(Id)` — returns the cached instance if already loaded, otherwise hits the database.

**Loading multiple objects with criteria:** use `Manager.Find<T>` (no argument) to get a fluent query builder, then call `.List`.

**Saving a new object:** call `Manager.Save(obj)` — the manager takes ownership and tracks changes from that point. `Save` executes the INSERT immediately. Do **not** call `Flush` after `Save` for a new object; that is only for persisting changes to already-managed objects.

**Updating a managed object:** just change its properties and call `Manager.Flush` (or `Manager.Flush(obj)` for a single object). No explicit "update" call needed.

**Updating a transient object (from outside the manager):** call `Manager.Update(obj)` — but be aware this writes *all* properties on flush, not just the changed ones.

**Conflicting identity:** if an object with the same id is already cached, use `Manager.Merge<T>(transient)` instead of `Update` — it copies data into the existing managed instance.

**Deleting:** call `Manager.Remove(obj)` — the object must be managed (loaded through this manager or registered via `Save`/`Update`).

## Critical Rules

### Object lifetime
- Managed entities are owned by the manager and destroyed when it is destroyed — **do not free them manually**.
- When a query returns a list (`TList<T>`), **free the list** but **not the items inside it** — the items remain managed.
- Projection queries (`ListValues`) return lists with `OwnsObjects = True`; destroying the list also destroys the items.
- If you need entities to survive after the manager is freed, set `Manager.OwnsObjects := False` before calling `Free`.
- Call `Manager.AddOwnership(obj)` *before* `Save` if you want the manager to own the object even when `Save` raises an exception.

### Flush granularity
- Prefer `Manager.Flush(singleObject)` over `Manager.Flush` (no args). The no-arg form iterates the **entire** manager cache and can be slow when many objects are loaded.

### Associations — always use object references
- Assign the **associated object** to the association property, never a raw foreign key value. Setting a hypothetical `Invoice.CustomerId` field bypasses the ORM and causes inconsistencies.
- For bidirectional associations, set **both sides**: assign the parent to the child's property *and* add the child to the parent's collection.

```delphi
// WRONG — bypasses the ORM:
Invoice.CustomerId := 42;

// CORRECT — assign the managed object:
Invoice.Customer := Manager.Find<TCustomer>(42);
```

### Removing from a collection
- With `CascadeTypeAll` (no orphan removal): removing an item from the collection sets its foreign key to `NULL` — the row stays in the database as an orphan.
- With `CascadeTypeAllRemoveOrphan`: removing an item from the collection deletes the row on the next flush. Use this for child entities that have no meaning without their parent (e.g. invoice line items).

### Lazy associations and manager lifetime
- Accessing a lazy-loaded association issues a SELECT at that moment. The manager **must still be alive** when you access a lazy property. Do not destroy the manager while holding references to entities whose lazy associations you may still access.

### Merging vs. Update
- `Update` raises an exception if the same id is already cached under a different instance — use `Merge<T>` in that case.
- After `Merge<T>`, the returned object is the managed one; the transient object you passed in is **not** managed — free it yourself.

### Transactions
- `BeginTransaction` is called on the connection (`Manager.Connection.BeginTransaction`), not on the manager itself.
- Always `Rollback` in the `except` block and re-raise — never swallow the exception.
- Aurelius supports nested transactions; only the outermost `Commit`/`Rollback` hits the database.

### Cached updates and identity ids
- When `CachedUpdates = True` and the entity uses database-generated ids (identity/autoincrement), the INSERT is executed **immediately** even though other SQL is deferred — because the generated id is needed to proceed.

### Concurrency with `[Version]`
- If a versioned entity is modified concurrently, Aurelius raises `EVersionedConcurrencyControl` on flush. Handle it by refreshing the object and retrying the operation.

## Reference

For full method signatures, code examples, and details on all operations, read [references/objects.md](references/objects.md).

The reference covers: TObjectManager creation and TAureliusManager component, memory management (transient vs. persistent, unique instances, ownership transfer), saving objects (simple, with associations, cascades, collections), updating (flush, Update, Merge, Replicate, updating associations), finding objects (by id, fluent query builder, querying through associations, eager vs. lazy navigation), refreshing, removing (with and without cascade), evicting, transactions, concurrency control (changed-field detection, entity versioning), cached updates, and batch/bulk updates.