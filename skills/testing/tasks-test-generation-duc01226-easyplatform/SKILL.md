---
name: tasks-test-generation
description: Use when creating or enhancing unit tests, integration tests, or defining test strategies for backend and frontend code.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

> **Skill Variant:** Use this skill for **autonomous test generation** with structured templates. For interactive test writing with user feedback, use `test-generation` instead.

# Test Generation Workflow

## When to Use This Skill

- Creating unit tests for new code
- Adding tests for bug fixes
- Integration test development
- Test coverage improvement

## Pre-Flight Checklist

- [ ] Identify code to test (command, query, entity, component)
- [ ] Find existing test patterns: `grep "Test.*{Feature}" --include="*.cs"`
- [ ] Determine test type (unit, integration, e2e)
- [ ] Identify dependencies to mock

## File Locations

### Backend Tests

```
tests/
└── {Service}.Tests/
    ├── UnitTests/
    │   ├── Commands/
    │   │   └── Save{Entity}CommandTests.cs
    │   ├── Queries/
    │   │   └── Get{Entity}ListQueryTests.cs
    │   └── Entities/
    │       └── {Entity}Tests.cs
    └── IntegrationTests/
        └── {Feature}IntegrationTests.cs
```

### Frontend Tests

```
src/Frontend/apps/{app}/src/app/
└── features/
    └── {feature}/
        ├── {feature}.component.spec.ts
        └── {feature}.store.spec.ts
```

## Pattern 1: Command Handler Unit Test

```csharp
public class SaveEmployeeCommandTests
{
    private readonly Mock<IPlatformQueryableRootRepository<Employee>> _employeeRepoMock;
    private readonly Mock<IPlatformApplicationRequestContextAccessor> _contextMock;
    private readonly SaveEmployeeCommandHandler _handler;

    public SaveEmployeeCommandTests()
    {
        _employeeRepoMock = new Mock<IPlatformQueryableRootRepository<Employee>>();
        _contextMock = new Mock<IPlatformApplicationRequestContextAccessor>();

        // Setup default context
        var requestContext = new Mock<IPlatformApplicationRequestContext>();
        requestContext.Setup(x => x.UserId()).Returns("test-user-id");
        requestContext.Setup(x => x.CurrentCompanyId()).Returns("test-company-id");
        _contextMock.Setup(x => x.Current).Returns(requestContext.Object);

        _handler = new SaveEmployeeCommandHandler(
            Mock.Of<ILoggerFactory>(),
            Mock.Of<IPlatformUnitOfWorkManager>(),
            Mock.Of<IServiceProvider>(),
            Mock.Of<IPlatformRootServiceProvider>(),
            _employeeRepoMock.Object
        );
    }

    [Fact]
    public async Task HandleAsync_CreateEmployee_ReturnsNewEmployee()
    {
        // Arrange
        var command = new SaveEmployeeCommand
        {
            Name = "John Doe",
            Email = "john@example.com"
        };

        _employeeRepoMock
            .Setup(x => x.CreateAsync(It.IsAny<Employee>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync((Employee e, CancellationToken _) => e);

        // Act
        var result = await _handler.HandleAsync(command, CancellationToken.None);

        // Assert
        Assert.NotNull(result.Employee);
        Assert.Equal("John Doe", result.Employee.Name);
        _employeeRepoMock.Verify(x => x.CreateAsync(
            It.Is<Employee>(e => e.Name == "John Doe"),
            It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task HandleAsync_UpdateEmployee_UpdatesExisting()
    {
        // Arrange
        var existingEmployee = new Employee { Id = "emp-1", Name = "Old Name" };
        var command = new SaveEmployeeCommand
        {
            Id = "emp-1",
            Name = "New Name"
        };

        _employeeRepoMock
            .Setup(x => x.GetByIdAsync("emp-1", It.IsAny<CancellationToken>()))
            .ReturnsAsync(existingEmployee);

        _employeeRepoMock
            .Setup(x => x.UpdateAsync(It.IsAny<Employee>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync((Employee e, CancellationToken _) => e);

        // Act
        var result = await _handler.HandleAsync(command, CancellationToken.None);

        // Assert
        Assert.Equal("New Name", result.Employee.Name);
        _employeeRepoMock.Verify(x => x.UpdateAsync(
            It.Is<Employee>(e => e.Name == "New Name"),
            It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task HandleAsync_InvalidCommand_ReturnsValidationError()
    {
        // Arrange
        var command = new SaveEmployeeCommand
        {
            Name = ""  // Invalid: empty name
        };

        // Act & Assert
        var result = command.Validate();
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.Contains("Name"));
    }
}
```

## Pattern 2: Query Handler Unit Test

```csharp
public class GetEmployeeListQueryTests
{
    private readonly Mock<IPlatformQueryableRootRepository<Employee>> _repoMock;
    private readonly GetEmployeeListQueryHandler _handler;

    [Fact]
    public async Task HandleAsync_WithFilters_ReturnsFilteredResults()
    {
        // Arrange
        var employees = new List<Employee>
        {
            new() { Id = "1", Name = "Active", Status = EmployeeStatus.Active },
            new() { Id = "2", Name = "Inactive", Status = EmployeeStatus.Inactive }
        };

        _repoMock.Setup(x => x.CountAsync(It.IsAny<Expression<Func<Employee, bool>>>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(1);

        _repoMock.Setup(x => x.GetAllAsync(It.IsAny<Func<IPlatformUnitOfWork, IQueryable<Employee>, IQueryable<Employee>>>(), It.IsAny<CancellationToken>(), It.IsAny<Expression<Func<Employee, object>>[]>()))
            .ReturnsAsync(employees.Where(e => e.Status == EmployeeStatus.Active).ToList());

        var query = new GetEmployeeListQuery
        {
            Statuses = [EmployeeStatus.Active],
            SkipCount = 0,
            MaxResultCount = 10
        };

        // Act
        var result = await _handler.HandleAsync(query, CancellationToken.None);

        // Assert
        Assert.Single(result.Items);
        Assert.Equal("Active", result.Items[0].Name);
    }
}
```

## Pattern 3: Entity Validation Test

```csharp
public class EmployeeEntityTests
{
    [Fact]
    public void UniqueExpr_ReturnsCorrectExpression()
    {
        // Arrange
        var employees = new List<Employee>
        {
            new() { CompanyId = "c1", UserId = "u1" },
            new() { CompanyId = "c1", UserId = "u2" },
            new() { CompanyId = "c2", UserId = "u1" }
        }.AsQueryable();

        // Act
        var expr = Employee.UniqueExpr("c1", "u1");
        var result = employees.Where(expr).ToList();

        // Assert
        Assert.Single(result);
        Assert.Equal("u1", result[0].UserId);
    }

    [Fact]
    public async Task ValidateAsync_DuplicateCode_ReturnsError()
    {
        // Arrange
        var repoMock = new Mock<IPlatformQueryableRootRepository<Employee>>();
        repoMock.Setup(x => x.AnyAsync(It.IsAny<Expression<Func<Employee, bool>>>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);  // Duplicate exists

        var employee = new Employee { Id = "new", Code = "EMP001", CompanyId = "c1" };

        // Act
        var result = await employee.ValidateAsync(repoMock.Object, CancellationToken.None);

        // Assert
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.Contains("already exists"));
    }

    [Fact]
    public void ComputedProperty_IsActive_CalculatesCorrectly()
    {
        // Arrange
        var activeEmployee = new Employee { Status = EmployeeStatus.Active, IsDeleted = false };
        var inactiveEmployee = new Employee { Status = EmployeeStatus.Inactive, IsDeleted = false };
        var deletedEmployee = new Employee { Status = EmployeeStatus.Active, IsDeleted = true };

        // Assert
        Assert.True(activeEmployee.IsActive);
        Assert.False(inactiveEmployee.IsActive);
        Assert.False(deletedEmployee.IsActive);
    }
}
```

## Pattern 4: Angular Component Test

```typescript
describe('FeatureListComponent', () => {
    let component: FeatureListComponent;
    let fixture: ComponentFixture<FeatureListComponent>;
    let store: FeatureListStore;
    let apiMock: jasmine.SpyObj<FeatureApiService>;

    beforeEach(async () => {
        apiMock = jasmine.createSpyObj('FeatureApiService', ['getList', 'delete']);

        await TestBed.configureTestingModule({
            imports: [FeatureListComponent],
            providers: [FeatureListStore, { provide: FeatureApiService, useValue: apiMock }]
        }).compileComponents();

        fixture = TestBed.createComponent(FeatureListComponent);
        component = fixture.componentInstance;
        store = TestBed.inject(FeatureListStore);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should load items on init', () => {
        // Arrange
        const items = [{ id: '1', name: 'Test' }];
        apiMock.getList.and.returnValue(of({ items, totalCount: 1 }));

        // Act
        fixture.detectChanges();

        // Assert
        expect(apiMock.getList).toHaveBeenCalled();
        expect(component.vm()?.items).toEqual(items);
    });

    it('should delete item', fakeAsync(() => {
        // Arrange
        store.updateState({ items: [{ id: '1', name: 'Test' }] });
        apiMock.delete.and.returnValue(of(void 0));

        // Act
        component.onDelete({ id: '1', name: 'Test' });
        tick();

        // Assert
        expect(apiMock.delete).toHaveBeenCalledWith('1');
        expect(component.vm()?.items.length).toBe(0);
    }));

    it('should show loading state', () => {
        // Arrange
        apiMock.getList.and.returnValue(new Subject()); // Never completes

        // Act
        fixture.detectChanges();

        // Assert
        expect(store.isLoading$('loadItems')()).toBe(true);
    });
});
```

## Pattern 5: Angular Store Test

```typescript
describe('FeatureListStore', () => {
    let store: FeatureListStore;
    let apiMock: jasmine.SpyObj<FeatureApiService>;

    beforeEach(() => {
        apiMock = jasmine.createSpyObj('FeatureApiService', ['getList', 'save', 'delete']);

        TestBed.configureTestingModule({
            providers: [FeatureListStore, { provide: FeatureApiService, useValue: apiMock }]
        });

        store = TestBed.inject(FeatureListStore);
    });

    it('should initialize with default state', () => {
        expect(store.currentVm().items).toEqual([]);
        expect(store.currentVm().pagination.pageIndex).toBe(0);
    });

    it('should load items', fakeAsync(() => {
        // Arrange
        const items = [{ id: '1', name: 'Test' }];
        apiMock.getList.and.returnValue(of({ items, totalCount: 1 }));

        // Act
        store.loadItems();
        tick();

        // Assert
        expect(store.currentVm().items).toEqual(items);
        expect(store.currentVm().pagination.totalCount).toBe(1);
    }));

    it('should update state immutably', () => {
        // Arrange
        const initialItems = store.currentVm().items;

        // Act
        store.updateState({ items: [{ id: '1', name: 'New' }] });

        // Assert
        expect(store.currentVm().items).not.toBe(initialItems);
    });

    it('should handle API error', fakeAsync(() => {
        // Arrange
        apiMock.getList.and.returnValue(throwError(() => new Error('API Error')));

        // Act
        store.loadItems();
        tick();

        // Assert
        expect(store.getErrorMsg$('loadItems')()).toContain('Error');
    }));
});
```

## Test Naming Convention

```
[MethodName]_[Scenario]_[ExpectedBehavior]

Examples:
- HandleAsync_ValidCommand_ReturnsSuccess
- HandleAsync_InvalidId_ThrowsNotFound
- UniqueExpr_MatchingValues_ReturnsTrue
- LoadItems_ApiError_SetsErrorState
```

## Anti-Patterns to AVOID

:x: **Testing implementation, not behavior**

```csharp
// WRONG - testing internal method calls
Assert.True(handler.WasValidateCalled);

// CORRECT - testing observable behavior
Assert.Equal("Expected", result.Value);
```

:x: **Not mocking dependencies**

```csharp
// WRONG - using real repository
var handler = new Handler(new RealRepository());

// CORRECT - using mock
var repoMock = new Mock<IRepository>();
var handler = new Handler(repoMock.Object);
```

:x: **Missing edge cases**

```csharp
// WRONG - only happy path
[Fact] public void Save_ValidData_Succeeds() { }

// CORRECT - include edge cases
[Fact] public void Save_EmptyName_ReturnsError() { }
[Fact] public void Save_DuplicateCode_ReturnsError() { }
[Fact] public void Save_NullInput_ThrowsException() { }
```

## Verification Checklist

- [ ] Unit tests cover happy path
- [ ] Edge cases and error conditions tested
- [ ] Dependencies properly mocked
- [ ] Test naming follows convention
- [ ] Assertions are specific and meaningful
- [ ] No test interdependencies
- [ ] Tests are deterministic (no random, no time-dependent)

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
