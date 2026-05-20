---
name: code-elevation
description: Transform "vibe coded" prototypes into production-ready, maintainable code through systematic refactoring. Use when code has grown complex, tests are slow, changes affect multiple areas, or a class has multiple responsibilities. Also use when refactoring god classes, improving testability, or applying SOLID principles to existing code.
---

# Code Elevation

Transform "vibe coded" prototypes into clean, production-ready architecture through systematic refactoring.

## Philosophy

> "Vibe coding is cute, but pair it with intentional development cycles, and watch how far you can take a project with coding agents today."

**Vibe coding** gets you moving fast - prototypes, MVPs, proof-of-concepts. It's exploratory, creative, and responsive.

**Code elevation** is the intentional process of hardening that code into production-ready architecture with clear responsibilities, fast tests, and maintainable structure.

Both have value. This skill bridges them.

## When to Use This Skill

Use code elevation when you notice these warning signs:

### Red Flags (Immediate action needed)
- **God class**: Single class >200 lines with 5+ responsibilities
- **Slow tests**: Unit tests taking >10ms (file I/O in business logic)
- **Shotgun surgery**: Simple changes require editing multiple unrelated methods
- **Fear factor**: Scared to refactor because tests might break

### Yellow Flags (Consider refactoring soon)
- **Growing complexity**: Class approaching 150 lines with 3-4 concerns
- **Conditional complexity**: Multiple nested if/else for different modes
- **Hard to test**: Need complex setup for simple tests
- **Code duplication**: Similar logic repeated across methods

### Green Flags (You're doing fine!)
- Classes <100 lines with single responsibility
- Tests run in <1ms with no I/O
- Changes isolated to single classes
- Easy to explain what each class does

## The Code Elevation Process

### Phase 1: Assessment (10-15 minutes)

**Goal**: Understand what's wrong before fixing it.

1. **Count responsibilities**: What distinct jobs does this class do?
   - Schema/config loading
   - I/O operations (file, network, database)
   - Business logic & algorithms
   - Data transformation
   - Validation
   - Error handling
   - Result formatting

2. **Identify SOLID violations**:
   - **SRP**: Multiple reasons to change? 
   - **OCP**: Hard to extend without modifying?
   - **DIP**: Depends on concrete implementations?

3. **Measure pain points**:
   - How long do tests take?
   - How many lines need to change for common requests?
   - What's the coupling score? (dependencies × responsibilities)

4. **Document findings**: Create an assessment document (see example below)

**When to read the example**: If this is your first assessment, read `references/examples/direct-extractor/01-assessment-direct-extractor.md` to see a complete analysis.

### Phase 2: Target Architecture (10-15 minutes)

**Goal**: Design the "after" state with clear boundaries.

1. **Choose architecture pattern** based on complexity:
   - **Simple extraction** (1-2 concerns): Just split into 2-3 service classes
   - **Medium complexity** (3-4 concerns): Service layer pattern
   - **Complex orchestration** (5+ concerns): Hexagonal architecture

2. **Define new classes**: One responsibility each
   - **Repository**: Data/config loading (implements interface)
   - **Adapter**: External I/O (implements interface)
   - **Service**: Pure business logic (no I/O, just algorithms)
   - **Orchestrator**: Thin coordinator (just wiring)

3. **Plan dependencies**: Use dependency injection
   - Infrastructure injected into orchestrator
   - Services depend only on interfaces
   - No hard-coded file paths or API endpoints

4. **Verify design**:
   - ✅ Each class has one reason to change
   - ✅ Services have no I/O (tests will be fast)
   - ✅ Adding features extends, doesn't modify
   - ✅ Can explain each class in one sentence

**When to read the example**: Read `references/examples/direct-extractor/02-target-architecture.md` to see a complete before/after design with metrics.

### Phase 3: Incremental Refactoring (30-60 minutes)

**Goal**: Transform the code safely with tests as safety net.

#### Core Refactoring Pattern

For each responsibility to extract:

1. **Write characterization tests** (if missing)
   - Test current behavior before changing anything
   - These tests should pass both before and after refactoring

2. **Extract the responsibility** into new class
   - Create new class with focused responsibility
   - Keep methods pure (no hidden I/O)
   - Use constructor injection for dependencies

3. **Update tests**
   - Add fast unit tests for new class (<1ms)
   - Verify new class works in isolation
   - Keep integration tests for wiring

4. **Refactor original class** to use new class
   - Replace inline logic with calls to new class
   - Inject new class as dependency

5. **Verify** everything still works
   - All tests pass (characterization + new unit tests)
   - No behavior changes
   - Backward compatibility maintained

6. **Commit** before moving to next extraction

#### Extraction Priority Order

Extract in this order for maximum safety:

1. **I/O adapters** first (Repository, TextReader)
   - Easiest to extract and test
   - Removes file system coupling immediately
   - Makes remaining logic easier to test

2. **Pure algorithms** second (Services)
   - No dependencies on extracted I/O
   - Fast tests with simple inputs/outputs
   - High confidence, low risk

3. **Orchestration** last (Main class becomes thin coordinator)
   - Now just wires dependencies together
   - Should be <60 lines
   - Integration tests verify wiring

**When to read the example**: Read `references/examples/direct-extractor/03-refactoring-steps.md` for detailed step-by-step instructions with code examples.

### Phase 4: Validation (5-10 minutes)

**Goal**: Confirm the elevation achieved its goals.

Check these metrics before/after:

| Metric | Target |
|--------|--------|
| Lines per class | <100 (ideally 30-80) |
| Responsibilities per class | 1 |
| Unit test speed | <1ms |
| Test setup complexity | Simple (just instantiate class) |
| Dependencies injected | All infrastructure |
| Coupling score | Low (3-5 dependencies max per class) |

If targets aren't met, identify what's still coupled and consider another extraction.

## Key Architectural Patterns

### Repository Pattern

**Problem**: Data/config loading scattered throughout business logic

**Solution**: 
```python
class SchemaRepository(ABC):
    @abstractmethod
    def get_schema(self, name: str) -> Dict[str, Any]:
        pass

class FileSystemSchemaRepository(SchemaRepository):
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def get_schema(self, name: str) -> Dict[str, Any]:
        # File I/O isolated here
        path = self.base_path / f"{name}.json"
        return json.loads(path.read_text())
```

**Benefits**:
- Business logic doesn't know about files
- Easy to test with mock repository
- Easy to switch to DB or API later

### Adapter Pattern

**Problem**: Direct dependencies on external systems (files, network, etc.)

**Solution**:
```python
class TextReader(ABC):
    @abstractmethod
    def read_text(self, path: Path) -> str:
        pass

class PdfTextReader(TextReader):
    def read_text(self, path: Path) -> str:
        # PDF-specific logic isolated here
        return extract_pdf_text(path)

class PlainTextReader(TextReader):
    def read_text(self, path: Path) -> str:
        return path.read_text()
```

**Benefits**:
- Swap implementations without changing business logic
- Test with fake in-memory reader
- No file I/O in unit tests

### Service Layer Pattern

**Problem**: Complex algorithms buried in god class

**Solution**:
```python
class LinePreprocessor:
    """Pure business logic - no I/O, just transformations"""
    
    def preprocess(self, lines: List[str]) -> List[str]:
        # Pure function: same input = same output
        # No file access, no network calls
        # Fast tests: <1ms
        return self._join_multiline_items(lines)
```

**Benefits**:
- Pure logic = fast tests
- Reusable across different contexts
- Easy to understand and modify

### Dependency Injection

**Problem**: Hard-coded dependencies make testing impossible

**Solution**:
```python
class DocumentExtractor:
    def __init__(
        self,
        schema_repo: SchemaRepository,
        text_reader: TextReader,
        preprocessor: LinePreprocessor,
        matcher: PatternMatcher
    ):
        # All dependencies injected
        self.schema_repo = schema_repo
        self.text_reader = text_reader
        self.preprocessor = preprocessor
        self.matcher = matcher
    
    def extract(self, document_path: Path) -> ExtractionResult:
        # Just orchestrate - all work delegated
        schema = self.schema_repo.get_schema("invoice")
        text = self.text_reader.read_text(document_path)
        lines = self.preprocessor.preprocess(text.split('\n'))
        return self.matcher.match(lines, schema)
```

**Benefits**:
- Test each component independently
- Mock any dependency easily
- Change implementations without touching orchestrator

## Testing Strategy

### Unit Tests (Many, Fast)
- Test ONE class in isolation
- Mock all dependencies
- No I/O operations
- Target: <1ms execution
- Goal: 80%+ code coverage

### Integration Tests (Few, Slower)
- Test the wiring
- Use real or near-real dependencies
- Verify components work together
- Target: <100ms execution
- Goal: Cover critical paths only

### Example Test Structure
```python
# Unit test - Fast (<1ms)
def test_line_preprocessor():
    preprocessor = LinePreprocessor()
    result = preprocessor.preprocess(["Line 1", "  Line 2"])
    assert result == ["Line 1", "Line 2"]  # No I/O!

# Integration test - Slower (~10ms)
def test_full_extraction():
    schema_repo = FileSystemSchemaRepository(Path("./schemas"))
    text_reader = PdfTextReader()
    extractor = DocumentExtractor(schema_repo, text_reader, ...)
    result = extractor.extract(Path("test.pdf"))
    assert result.items_found > 0
```

## Common Refactoring Techniques

### Extract Class
When a class has multiple responsibilities, extract one into a new class.

**Before**:
```python
class Extractor:
    def extract(self, path):
        # Load schema (20 lines)
        # Read file (15 lines)
        # Parse (50 lines)
        # Validate (30 lines)
```

**After**:
```python
class SchemaLoader:
    # 20 lines - one job

class FileReader:
    # 15 lines - one job

class Parser:
    # 50 lines - one job

class Validator:
    # 30 lines - one job

class Extractor:
    def __init__(self, loader, reader, parser, validator):
        # 10 lines - just orchestration
```

### Extract Interface
When a class has concrete dependencies, extract an interface.

**Before**:
```python
class Processor:
    def process(self):
        data = json.loads(Path("file.json").read_text())  # Hard-coded!
```

**After**:
```python
class DataSource(ABC):
    @abstractmethod
    def load_data(self) -> dict: pass

class FileDataSource(DataSource):
    def load_data(self) -> dict:
        return json.loads(Path("file.json").read_text())

class Processor:
    def __init__(self, data_source: DataSource):
        self.data_source = data_source
    
    def process(self):
        data = self.data_source.load_data()  # Flexible!
```

### Replace Conditional with Polymorphism
When you have mode flags or type checking, use polymorphism.

**Before**:
```python
def process(self, data, mode):
    if mode == "simple":
        # 20 lines
    elif mode == "advanced":
        # 30 lines
    elif mode == "custom":
        # 25 lines
```

**After**:
```python
class Processor(ABC):
    @abstractmethod
    def process(self, data): pass

class SimpleProcessor(Processor):
    def process(self, data):
        # 20 lines

class AdvancedProcessor(Processor):
    def process(self, data):
        # 30 lines

# Use: processor.process(data)  # Polymorphic!
```

## Real-World Example: DirectExtractor

A complete case study showing the transformation of a 300-line god class into clean architecture.

**Read these files in order**:

1. **Assessment**: `references/examples/direct-extractor/01-assessment-direct-extractor.md`
   - Shows how to identify problems
   - Demonstrates SOLID violation analysis
   - Calculates coupling metrics

2. **Target Architecture**: `references/examples/direct-extractor/02-target-architecture.md`
   - Shows the planned "after" state
   - Explains architecture choices
   - Provides before/after metrics

3. **Refactoring Steps**: `references/examples/direct-extractor/03-refactoring-steps.md`
   - Step-by-step transformation
   - Code examples for each extraction
   - Test examples at each step

4. **Summary**: `references/examples/direct-extractor/04-summary-and-next-steps.md`
   - Key learnings
   - Applicability to other projects
   - Next steps for iteration

## Success Criteria

You've successfully elevated your code when:

- ✅ Each class has <100 lines and one clear responsibility
- ✅ Unit tests run in <1ms (no I/O in business logic)
- ✅ Changes affect only one class
- ✅ New features extend rather than modify existing code
- ✅ You can explain what each class does in one sentence
- ✅ Tests are simple to write and maintain

## Tips for Working with Code Agents

### Start with Assessment
Don't jump straight to refactoring. Take 10 minutes to document:
- Current responsibilities
- SOLID violations
- Test pain points
- Coupling metrics

This creates shared context with the agent and ensures you're solving the right problems.

### Refactor Incrementally
Each extraction should be a separate commit:
1. Extract one responsibility
2. Add tests
3. Verify everything works
4. Commit
5. Move to next extraction

This makes it easy to roll back if something breaks.

### Prioritize I/O First
Extract file/network/database dependencies before business logic:
- Easier to extract
- Removes coupling immediately
- Makes remaining refactoring simpler
- Enables fast tests sooner

### Keep Tests Green
Never break existing tests during refactoring:
- Write characterization tests first
- Keep them passing throughout
- Add new unit tests as you extract
- Integration tests verify wiring

### Know When to Stop
Don't over-engineer. Stop when:
- Each class has single responsibility
- Tests are fast (<1ms for unit tests)
- Changes are localized
- Code is easy to understand

Perfect is the enemy of good enough.

## Next Steps After Elevation

Once code is elevated:

1. **Document architecture**: Add README explaining structure
2. **Set up guardrails**: Linting rules, architecture tests
3. **Share patterns**: Help team recognize and fix similar issues
4. **Iterate**: Apply to other god classes in codebase

Remember: Code elevation is a continuous process, not a one-time event.

## Questions to Ask Yourself

- Which class in my codebase is hardest to test?
- Which class has the most responsibilities?
- What change would be risky to make today?
- If I could only refactor one thing, what would it be?

The answers point to your next elevation target.
