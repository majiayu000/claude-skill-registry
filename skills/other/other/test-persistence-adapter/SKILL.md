---
name: test-persistence-adapter
argument-hint: "<path-to-adapter-file-or-test-file>"
allowed-tools: Read, Write, Edit, Glob, Bash(./gradlew *)
description: Generate a `@DataJpaTest` slice test for a JPA persistence adapter using H2 in-memory database and `TestEntityManager`. Use when the user asks to "write tests for a persistence adapter", "generate JPA tests", or "test the repository adapter". Covers all CRUD operations; uses `@Sql` fixtures for read/delete tests; calls `flush()` and `clear()` after writes to bypass the JPA cache; asserts with `usingRecursiveComparison()`.
---

# Skill: test-persistence-adapter

Generate or fix a test for a persistence adapter using `@DataJpaTest` with H2 in-memory database.

## IMPORTANT

- `@DataJpaTest` + `@Import(AdapterClass::class)` — no full Spring context, no custom base class
- `@Autowired` inject both the adapter under test and `TestEntityManager`
- Call `entityManager.flush()` then `entityManager.clear()` after every write before re-reading,
  to ensure the JPA first-level cache does not mask a missing database round-trip
- **Data strategy**: only the `save` test writes data programmatically; every other test that needs
  existing data uses `@Sql` — this keeps tests independent of each other
- Use `@Sql("classpath:sql/<entity>.sql")` for `find`, `search` (found path), and `delete` tests; SQL
  files go in `src/test/resources/sql/` — derive column names from the entity's `@Column` annotations
  and values from the domain test builder so `usingRecursiveComparison()` assertions pass without delta
- Use `assertThat(result).usingRecursiveComparison().isEqualTo(expected)` for aggregate comparisons
- Use test builders from `domain/TestObjectBuilder.kt` for test data
- Fixed UUID strings for deterministic test data

## Example invocation

```
/test-persistence-adapter services/example-service/src/main/kotlin/io/miragon/example/adapter/outbound/db/NewsletterSubscriptionPersistenceAdapter.kt
```

## Pattern

`@DataJpaTest` loads only the JPA slice (no full Spring context).
The adapter itself is not part of that slice and must be imported explicitly.
`TestEntityManager` replaces any custom cache-flush helper.

```kotlin
@DataJpaTest
@Import(YourPersistenceAdapter::class)
class YourPersistenceAdapterTest {
    @Autowired
    private lateinit var underTest: YourPersistenceAdapter
    @Autowired
    private lateinit var entityManager: TestEntityManager

    @Test
    fun `saves and reloads entity`() {
        // given / when: entity is saved and persistence context is flushed
        underTest.save(obj); entityManager.flush(); entityManager.clear()
        // then: entity can be reloaded from the database
        assertThat(underTest.find(id))...
    }
    @Test
    fun `search returns null when not found`() {
        assertThat(underTest.search(id)).isNull()
    }
    @Test
    fun `find throws when not found`() {
        assertThatThrownBy { underTest.find(id) }...
    }
    @Test
    @Sql("classpath:sql/entity.sql")
    fun `find returns entity when exists`() {
        assertThat(underTest.find(id))...
    }
    @Test
    @Sql("...")
    fun `search returns entity when exists`() {
        assertThat(underTest.search(id))...
    }
    @Test
    @Sql("...")
    fun `deletes existing entity`() {
        underTest.delete(id); entityManager.flush(); entityManager.clear(); assertThat(underTest.search(id)).isNull()
    }
}
```

See `references/persistence-adapter-test-template.kt` for the full annotated example.

## Instructions

### Step 1 – Read and identify

If `$ARGUMENTS` is empty or the file at that path cannot be read, do not proceed.
Instead, use Glob to search for `**/*PersistenceAdapter.kt` under `src/main/kotlin`.
If exactly one file is found, use it. If multiple files are found, list them and ask the user which one to test.
If none are found, stop and ask the user: "Please provide the path to the persistence adapter you want to test."

Read the persistence-adapter file and extract:

- Adapter class name and the outbound port interface it implements
- Public methods, their signatures, and whether they read or write
- JPA repository used, entity class, domain/value types, ID type

Then read the entity class to understand `@Column` mappings (needed for SQL fixtures).

### Step 2 – Locate the test file

Mirror `src/main/kotlin` → `src/test/kotlin`, same package path, append `Test` to the class name.
If the file already exists, open it and switch to fix mode. If not, proceed to generate a new file.

### Step 3 – Determine required test cases

Standard coverage for a persistence adapter (up to 6 tests):

- save+reload (programmatic write), find (SQL), search-found (SQL), search-null (no data),
  find-throws (no data), delete (SQL)

Only include tests for methods that actually exist on the adapter. If more scenarios apply, list them
and ask for permission first.

### Step 4 – Generate or fix the test file

- Use `references/persistence-adapter-test-template.kt` as a starting point
- Only the save test writes data programmatically; all others use `@Sql`
- SQL values must match the domain test builder so `usingRecursiveComparison()` passes

### Step 5 – Write, run, and report

Write the test file and any required SQL fixture; run all tests in the class via an appropriate
Gradle command; report the created or updated file path and a brief summary.
If the existing test file was already correct and required no changes, report that explicitly instead of silently succeeding.
