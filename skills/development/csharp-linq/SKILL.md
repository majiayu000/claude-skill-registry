---
name: csharp-linq
description: Use when lINQ query and method syntax, deferred execution, and performance optimization. Use when querying collections in C#.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# C# LINQ

Master Language Integrated Query (LINQ) for querying and transforming data in C#.
This skill covers query syntax, method syntax, deferred execution, performance
optimization, and advanced LINQ patterns from C# 8-12.

## LINQ Query Syntax vs Method Syntax

LINQ supports two syntaxes: query syntax (SQL-like) and method syntax (fluent).
Both compile to the same code.

### Query Syntax

```csharp
var students = new List<Student>
{
    new Student { Name = "Alice", Grade = 85, Age = 20 },
    new Student { Name = "Bob", Grade = 92, Age = 21 },
    new Student { Name = "Charlie", Grade = 78, Age = 20 }
};

// Query syntax - SQL-like
var topStudents = from student in students
                  where student.Grade >= 80
                  orderby student.Grade descending
                  select new { student.Name, student.Grade };

foreach (var student in topStudents)
{
    Console.WriteLine($"{student.Name}: {student.Grade}");
}
```

### Method Syntax

```csharp
// Method syntax - fluent API
var topStudents = students
    .Where(s => s.Grade >= 80)
    .OrderByDescending(s => s.Grade)
    .Select(s => new { s.Name, s.Grade });

// Method syntax is more flexible for complex queries
var result = students
    .Where(s => s.Age >= 20)
    .GroupBy(s => s.Age)
    .Select(g => new
    {
        Age = g.Key,
        AverageGrade = g.Average(s => s.Grade),
        Count = g.Count()
    })
    .OrderBy(x => x.Age);
```

### When to Use Each Syntax

```csharp
// Query syntax better for joins
var query1 = from student in students
             join course in courses on student.Id equals course.StudentId
             where course.Grade > 80
             select new { student.Name, course.Title };

// Method syntax better for chaining and complex logic
var query2 = students
    .Where(s => s.Age >= 20)
    .SelectMany(s => s.Courses)
    .Where(c => c.Grade > 80)
    .Distinct()
    .Take(10);

// Mixed approach
var query3 = (from s in students
              where s.Age >= 20
              select s)
    .Take(10)
    .ToList(); // Force execution
```

## Deferred Execution

LINQ queries use deferred execution - they don't execute until enumerated.

### Understanding Deferred Execution

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

// Query is defined but NOT executed
var query = numbers.Where(n => n > 2);

// Add more numbers
numbers.Add(6);
numbers.Add(7);

// Query executes NOW when enumerated
foreach (var num in query) // Gets: 3, 4, 5, 6, 7
{
    Console.WriteLine(num);
}

// Query executes AGAIN (sees current state)
var count = query.Count(); // 5

// Force immediate execution with ToList(), ToArray(), etc.
var snapshot = numbers.Where(n => n > 2).ToList();
numbers.Add(8);
Console.WriteLine(snapshot.Count); // Still 5, not 6
```

### Deferred vs Immediate Execution

```csharp
public class DeferredExecutionExample
{
    public void Demonstrate()
    {
        var data = new List<int> { 1, 2, 3, 4, 5 };

        // Deferred - query not executed yet
        var deferred = data.Where(x => x > 2);

        // Immediate - query executed now
        var immediate = data.Where(x => x > 2).ToList();

        // Modify source
        data.Add(6);

        Console.WriteLine(deferred.Count());  // 4 (includes 6)
        Console.WriteLine(immediate.Count()); // 3 (snapshot before 6 was added)
    }

    // Dangerous: query is rebuilt each iteration
    public void DangerousPattern()
    {
        var data = GetData(); // Expensive

        // ❌ BAD - GetData() called multiple times
        foreach (var item in GetData().Where(x => x.IsActive))
        {
            Process(item);
        }

        // ✅ GOOD - GetData() called once
        var items = GetData().Where(x => x.IsActive).ToList();
        foreach (var item in items)
        {
            Process(item);
        }
    }
}
```

## IEnumerable vs IQueryable

IEnumerable executes in memory (LINQ to Objects). IQueryable translates to
expression trees for remote execution (LINQ to SQL, EF).

### IEnumerable&lt;T&gt; - In-Memory

```csharp
public class InMemoryQueries
{
    public void QueryInMemory()
    {
        var products = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop", Price = 999 },
            new Product { Id = 2, Name = "Mouse", Price = 25 },
            new Product { Id = 3, Name = "Keyboard", Price = 75 }
        };

        // IEnumerable - executes in memory
        IEnumerable<Product> query = products
            .Where(p => p.Price > 50)
            .OrderBy(p => p.Name);

        // All filtering happens in C# code
        foreach (var product in query)
        {
            Console.WriteLine($"{product.Name}: ${product.Price}");
        }
    }
}
```

### IQueryable&lt;T&gt; - Expression Trees

```csharp
public class QueryableExamples
{
    private readonly DbContext _context;

    // IQueryable - translates to SQL
    public async Task<List<Product>> GetExpensiveProductsAsync()
    {
        // Query builds expression tree
        IQueryable<Product> query = _context.Products
            .Where(p => p.Price > 50)
            .OrderBy(p => p.Name);

        // SQL generated and executed here
        return await query.ToListAsync();
        // SQL: SELECT * FROM Products WHERE Price > 50 ORDER BY Name
    }

    // Composable queries
    public IQueryable<Product> GetActiveProducts()
    {
        return _context.Products.Where(p => p.IsActive);
    }

    public async Task<List<Product>> GetExpensiveActiveProductsAsync()
    {
        // Compose queries - still generates single SQL
        var products = await GetActiveProducts()
            .Where(p => p.Price > 100)
            .ToListAsync();

        // SQL: SELECT * FROM Products WHERE IsActive = 1 AND Price > 100
        return products;
    }
}
```

### Mixing IEnumerable and IQueryable

```csharp
public class MixingQueries
{
    private readonly DbContext _context;

    public async Task<List<ProductDto>> GetProductsDangerousAsync()
    {
        // ❌ BAD - ToList() brings ALL products to memory first
        var products = await _context.Products.ToListAsync();

        // Then filters in memory (inefficient)
        return products
            .Where(p => p.Price > 100) // In memory
            .Select(p => new ProductDto { Name = p.Name })
            .ToList();
    }

    public async Task<List<ProductDto>> GetProductsEfficientAsync()
    {
        // ✅ GOOD - everything in SQL
        return await _context.Products
            .Where(p => p.Price > 100) // In SQL
            .Select(p => new ProductDto { Name = p.Name }) // In SQL
            .ToListAsync(); // Execute once
    }

    public async Task<List<Product>> ComplexFilterAsync()
    {
        // ✅ GOOD - SQL where possible, memory when necessary
        return await _context.Products
            .Where(p => p.Price > 50) // SQL
            .ToListAsync() // Execute SQL
            .ContinueWith(t => t.Result
                .Where(p => ComplexInMemoryCheck(p)) // C# predicate
                .ToList()
            );
    }

    private bool ComplexInMemoryCheck(Product product)
    {
        // Logic that can't be translated to SQL
        return product.Name.Split(' ').Length > 2;
    }
}
```

## Common LINQ Operators

### Where - Filtering

```csharp
var numbers = Enumerable.Range(1, 100);

// Simple filter
var evens = numbers.Where(n => n % 2 == 0);

// Multiple conditions
var filtered = numbers.Where(n => n > 10 && n < 50 && n % 3 == 0);

// Filter with index
var everyThird = numbers.Where((n, index) => index % 3 == 0);

// Complex filtering
var products = GetProducts()
    .Where(p => p.IsActive)
    .Where(p => p.Price >= 10 && p.Price <= 100)
    .Where(p => p.Category.StartsWith("Electronics"));
```

### Select - Projection

```csharp
var students = GetStudents();

// Simple projection
var names = students.Select(s => s.Name);

// Anonymous types
var summary = students.Select(s => new
{
    s.Name,
    s.Grade,
    Status = s.Grade >= 80 ? "Pass" : "Fail"
});

// Projection with index
var indexed = students.Select((s, i) => new
{
    Index = i,
    Student = s
});

// DTOs
var dtos = students.Select(s => new StudentDto
{
    FullName = $"{s.FirstName} {s.LastName}",
    GradePoint = s.Grade / 100.0
});
```

### SelectMany - Flattening

```csharp
var departments = new List<Department>
{
    new Department
    {
        Name = "IT",
        Employees = new[]
        {
            new Employee { Name = "Alice" },
            new Employee { Name = "Bob" }
        }
    },
    new Department
    {
        Name = "HR",
        Employees = new[]
        {
            new Employee { Name = "Charlie" }
        }
    }
};

// Flatten nested collections
var allEmployees = departments.SelectMany(d => d.Employees);

// With result selector
var employeesWithDept = departments.SelectMany(
    dept => dept.Employees,
    (dept, emp) => new { Department = dept.Name, Employee = emp.Name }
);

// Multiple levels
var orders = GetOrders();
var allItems = orders
    .SelectMany(o => o.OrderLines)
    .SelectMany(ol => ol.Items);
```

### GroupBy - Grouping

```csharp
var sales = GetSales();

// Simple grouping
var byCategory = sales.GroupBy(s => s.Category);

foreach (var group in byCategory)
{
    Console.WriteLine($"{group.Key}: {group.Count()} items");
}

// Grouping with projection
var categoryTotals = sales
    .GroupBy(s => s.Category)
    .Select(g => new
    {
        Category = g.Key,
        TotalSales = g.Sum(s => s.Amount),
        AverageSale = g.Average(s => s.Amount),
        Count = g.Count()
    });

// Multiple key grouping
var grouped = sales.GroupBy(s => new { s.Category, s.Region });

// GroupBy with custom comparer
var byNameIgnoreCase = students.GroupBy(
    s => s.Name,
    StringComparer.OrdinalIgnoreCase
);
```

### Join - Combining Collections

```csharp
var customers = GetCustomers();
var orders = GetOrders();

// Inner join
var customerOrders = from c in customers
                     join o in orders on c.Id equals o.CustomerId
                     select new { c.Name, o.OrderDate, o.Total };

// Method syntax
var customerOrders2 = customers.Join(
    orders,
    c => c.Id,
    o => o.CustomerId,
    (c, o) => new { c.Name, o.OrderDate, o.Total }
);

// Left outer join
var leftJoin = from c in customers
               join o in orders on c.Id equals o.CustomerId into customerOrders
               from co in customerOrders.DefaultIfEmpty()
               select new
               {
                   Customer = c.Name,
                   OrderTotal = co?.Total ?? 0
               };

// Multiple joins
var fullData = from c in customers
               join o in orders on c.Id equals o.CustomerId
               join od in orderDetails on o.Id equals od.OrderId
               select new { c.Name, o.OrderDate, od.Product };
```

## Aggregation Operations

### Basic Aggregations

```csharp
var numbers = new[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// Count
int count = numbers.Count();
int evenCount = numbers.Count(n => n % 2 == 0);

// Sum
int sum = numbers.Sum();
decimal totalPrice = products.Sum(p => p.Price);

// Average
double avg = numbers.Average();
double avgGrade = students.Average(s => s.Grade);

// Min/Max
int min = numbers.Min();
int max = numbers.Max();
var cheapest = products.MinBy(p => p.Price); // C# 9+
var mostExpensive = products.MaxBy(p => p.Price); // C# 9+

// Any/All
bool hasEvens = numbers.Any(n => n % 2 == 0);
bool allPositive = numbers.All(n => n > 0);

// First/Last/Single
var first = numbers.First();
var firstEven = numbers.First(n => n % 2 == 0);
var firstOrNull = numbers.FirstOrDefault(n => n > 100); // 0
var single = numbers.Single(n => n == 5);
var last = numbers.Last();
```

### Advanced Aggregations

```csharp
public class AggregationExamples
{
    public void AdvancedAggregates()
    {
        var sales = GetSales();

        // Aggregate - custom accumulator
        var total = sales.Aggregate(0m, (acc, sale) => acc + sale.Amount);

        // Complex aggregation
        var stats = sales.Aggregate(
            new { Sum = 0m, Count = 0 },
            (acc, sale) => new
            {
                Sum = acc.Sum + sale.Amount,
                Count = acc.Count + 1
            },
            acc => new
            {
                acc.Sum,
                acc.Count,
                Average = acc.Sum / acc.Count
            }
        );

        // Grouped aggregations
        var categorySummary = sales
            .GroupBy(s => s.Category)
            .Select(g => new
            {
                Category = g.Key,
                Count = g.Count(),
                Total = g.Sum(s => s.Amount),
                Average = g.Average(s => s.Amount),
                Min = g.Min(s => s.Amount),
                Max = g.Max(s => s.Amount)
            });
    }
}
```

## Set Operations

### Distinct, Union, Intersect, Except

```csharp
var list1 = new[] { 1, 2, 3, 4, 5 };
var list2 = new[] { 4, 5, 6, 7, 8 };

// Distinct - remove duplicates
var unique = new[] { 1, 2, 2, 3, 3, 3 }.Distinct(); // 1, 2, 3

// DistinctBy - C# 9+
var customers = GetCustomers();
var uniqueByEmail = customers.DistinctBy(c => c.Email);

// Union - combine and remove duplicates
var union = list1.Union(list2); // 1, 2, 3, 4, 5, 6, 7, 8

// Concat - combine without removing duplicates
var concatenated = list1.Concat(list2); // 1, 2, 3, 4, 5, 4, 5, 6, 7, 8

// Intersect - common elements
var intersection = list1.Intersect(list2); // 4, 5

// Except - elements in first but not second
var difference = list1.Except(list2); // 1, 2, 3

// Set operations with custom comparer
var products1 = GetProducts();
var products2 = GetMoreProducts();
var uniqueProducts = products1.Union(products2, new ProductComparer());
```

### Custom Equality Comparers

```csharp
public class ProductComparer : IEqualityComparer<Product>
{
    public bool Equals(Product? x, Product? y)
    {
        if (x == null || y == null) return false;
        return x.Name.Equals(y.Name, StringComparison.OrdinalIgnoreCase);
    }

    public int GetHashCode(Product obj)
    {
        return obj.Name.ToUpperInvariant().GetHashCode();
    }
}

// Usage
var distinct = products.Distinct(new ProductComparer());
```

## Ordering and Pagination

### Ordering

```csharp
var products = GetProducts();

// OrderBy - ascending
var ascending = products.OrderBy(p => p.Price);

// OrderByDescending
var descending = products.OrderByDescending(p => p.Price);

// ThenBy - secondary sort
var sorted = products
    .OrderBy(p => p.Category)
    .ThenByDescending(p => p.Price)
    .ThenBy(p => p.Name);

// Reverse
var reversed = products.OrderBy(p => p.Price).Reverse();

// Custom comparer
var customSort = products.OrderBy(p => p.Name, StringComparer.OrdinalIgnoreCase);
```

### Pagination

```csharp
public class PaginationExamples
{
    public PagedResult<Product> GetPage(int pageNumber, int pageSize)
    {
        var query = _context.Products
            .Where(p => p.IsActive)
            .OrderBy(p => p.Name);

        var total = query.Count();

        var items = query
            .Skip((pageNumber - 1) * pageSize)
            .Take(pageSize)
            .ToList();

        return new PagedResult<Product>
        {
            Items = items,
            PageNumber = pageNumber,
            PageSize = pageSize,
            TotalCount = total,
            TotalPages = (int)Math.Ceiling(total / (double)pageSize)
        };
    }

    // Efficient pagination with keyset
    public List<Product> GetNextPage(int? lastId, int pageSize)
    {
        var query = _context.Products.Where(p => p.IsActive);

        if (lastId.HasValue)
        {
            query = query.Where(p => p.Id > lastId.Value);
        }

        return query
            .OrderBy(p => p.Id)
            .Take(pageSize)
            .ToList();
    }
}
```

## Custom LINQ Operators

### Extension Methods

```csharp
public static class LinqExtensions
{
    // WhereIf - conditional filtering
    public static IEnumerable<T> WhereIf<T>(
        this IEnumerable<T> source,
        bool condition,
        Func<T, bool> predicate)
    {
        return condition ? source.Where(predicate) : source;
    }

    // Batch - split into chunks
    public static IEnumerable<List<T>> Batch<T>(
        this IEnumerable<T> source,
        int batchSize)
    {
        var batch = new List<T>(batchSize);

        foreach (var item in source)
        {
            batch.Add(item);

            if (batch.Count == batchSize)
            {
                yield return batch;
                batch = new List<T>(batchSize);
            }
        }

        if (batch.Count > 0)
        {
            yield return batch;
        }
    }

    // ForEach
    public static void ForEach<T>(this IEnumerable<T> source, Action<T> action)
    {
        foreach (var item in source)
        {
            action(item);
        }
    }

    // DistinctBy (built-in in C# 9+)
    public static IEnumerable<T> DistinctBy<T, TKey>(
        this IEnumerable<T> source,
        Func<T, TKey> keySelector)
    {
        var seenKeys = new HashSet<TKey>();

        foreach (var item in source)
        {
            if (seenKeys.Add(keySelector(item)))
            {
                yield return item;
            }
        }
    }
}

// Usage
var filtered = products
    .WhereIf(filterByPrice, p => p.Price > 100)
    .WhereIf(filterByCategory, p => p.Category == "Electronics");

var batches = items.Batch(100);
foreach (var batch in batches)
{
    ProcessBatch(batch);
}
```

## Performance Considerations

### Materialization

```csharp
public class PerformanceExamples
{
    // ❌ BAD - Multiple enumerations
    public void MultipleEnumerations(IEnumerable<Product> products)
    {
        var query = products.Where(p => p.Price > 100);

        Console.WriteLine(query.Count()); // Enumeration 1
        Console.WriteLine(query.Sum(p => p.Price)); // Enumeration 2

        foreach (var p in query) // Enumeration 3
        {
            Console.WriteLine(p.Name);
        }
    }

    // ✅ GOOD - Single enumeration
    public void SingleEnumeration(IEnumerable<Product> products)
    {
        var list = products.Where(p => p.Price > 100).ToList();

        Console.WriteLine(list.Count);
        Console.WriteLine(list.Sum(p => p.Price));

        foreach (var p in list)
        {
            Console.WriteLine(p.Name);
        }
    }
}
```

### Database Query Optimization

```csharp
public class QueryOptimization
{
    private readonly DbContext _context;

    // ❌ BAD - N+1 query problem
    public async Task<List<OrderDto>> GetOrdersBadAsync()
    {
        var orders = await _context.Orders.ToListAsync();

        return orders.Select(o => new OrderDto
        {
            Id = o.Id,
            // Triggers separate query for each order!
            CustomerName = o.Customer.Name,
            ItemCount = o.OrderLines.Count
        }).ToList();
    }

    // ✅ GOOD - Eager loading
    public async Task<List<OrderDto>> GetOrdersGoodAsync()
    {
        return await _context.Orders
            .Include(o => o.Customer)
            .Include(o => o.OrderLines)
            .Select(o => new OrderDto
            {
                Id = o.Id,
                CustomerName = o.Customer.Name,
                ItemCount = o.OrderLines.Count
            })
            .ToListAsync();
    }

    // ✅ BETTER - Project in SQL
    public async Task<List<OrderDto>> GetOrdersBestAsync()
    {
        return await _context.Orders
            .Select(o => new OrderDto
            {
                Id = o.Id,
                CustomerName = o.Customer.Name,
                ItemCount = o.OrderLines.Count
            })
            .ToListAsync();
    }
}
```

## Expression Trees

Understanding LINQ's expression tree compilation.

```csharp
public class ExpressionTreeExamples
{
    public void ExpressionTreeDemo()
    {
        // Lambda as delegate
        Func<int, bool> isEvenDelegate = n => n % 2 == 0;

        // Lambda as expression tree
        Expression<Func<int, bool>> isEvenExpression = n => n % 2 == 0;

        // Examine expression structure
        var binary = (BinaryExpression)isEvenExpression.Body;
        Console.WriteLine(binary.NodeType); // Modulo

        // Compile and execute
        var compiled = isEvenExpression.Compile();
        bool result = compiled(4); // true
    }

    // Building expressions dynamically
    public IQueryable<T> ApplyFilter<T>(
        IQueryable<T> query,
        string propertyName,
        object value)
    {
        var parameter = Expression.Parameter(typeof(T), "x");
        var property = Expression.Property(parameter, propertyName);
        var constant = Expression.Constant(value);
        var equality = Expression.Equal(property, constant);
        var lambda = Expression.Lambda<Func<T, bool>>(equality, parameter);

        return query.Where(lambda);
    }
}
```

## Best Practices

1. **Use Method Syntax for Complex Queries**: More flexible than query syntax
2. **ToList/ToArray When Needed**: Materialize queries you'll enumerate
   multiple times
3. **Avoid Multiple Enumerations**: Cache results when reusing queries
4. **Project Early**: Select only needed properties, especially with EF
5. **Use AsNoTracking**: For read-only EF queries
6. **Batch Database Queries**: Use Include for related data
7. **Avoid LINQ in Loops**: Pull queries out of loops when possible
8. **Use IQueryable for Composition**: Build queries gradually
9. **Consider Compiled Queries**: For frequently-used EF queries
10. **Profile Your Queries**: Use logging to see generated SQL

## Common Pitfalls

1. **Multiple Enumerations**: Not materializing queries leads to re-execution
2. **N+1 Queries**: Forgetting to Include related entities in EF
3. **Premature Materialization**: Calling ToList() too early limits query composition
4. **Mixing IEnumerable and IQueryable**: Forces in-memory evaluation
5. **Client-Side Evaluation**: Using methods that can't translate to SQL
6. **Ignored Where Clauses**: Forgetting queries build incrementally
7. **Inefficient Ordering**: Ordering before filtering
8. **Large Result Sets**: Not using pagination or Take()
9. **Closure Capturing**: Variables captured in lambdas evaluated when query runs
10. **Exception Swallowing**: FirstOrDefault returns null, not an exception

## When to Use

Use this skill when:

- Querying collections in C#
- Working with Entity Framework or LINQ to SQL
- Transforming data with projections
- Filtering and sorting data
- Performing aggregations and grouping
- Joining multiple data sources
- Implementing pagination
- Building dynamic queries
- Optimizing query performance
- Working with expression trees

## Resources

- [LINQ Documentation](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)
- [101 LINQ Samples](https://learn.microsoft.com/en-us/samples/dotnet/try-samples/101-linq-samples/) <!-- markdownlint-disable-line MD013 -->
- [LINQ Performance Tips](https://learn.microsoft.com/en-us/dotnet/standard/linq/performance)
- [Expression Trees](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/expression-trees/)
- [Entity Framework LINQ](https://learn.microsoft.com/en-us/ef/core/querying/)
