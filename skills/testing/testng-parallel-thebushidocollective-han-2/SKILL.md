---
name: testng-parallel
description: Use when configuring parallel test execution with TestNG including thread pools, suite configuration, and synchronization.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# TestNG Parallel Execution

Master TestNG parallel test execution including thread pool configuration, suite-level parallelism, method-level parallelism, and thread safety patterns. This skill covers techniques for maximizing test throughput while maintaining test reliability.

## Overview

TestNG supports parallel execution at multiple levels: suite, test, class, and method. Proper parallel configuration can significantly reduce test execution time, but requires careful consideration of thread safety and resource management.

## Parallel Execution Modes

### Suite-Level Parallelism

Run multiple `<test>` tags in parallel:

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Parallel Suite" parallel="tests" thread-count="3">

    <test name="Chrome Tests">
        <classes>
            <class name="com.example.tests.BrowserTest"/>
        </classes>
    </test>

    <test name="Firefox Tests">
        <classes>
            <class name="com.example.tests.BrowserTest"/>
        </classes>
    </test>

    <test name="Safari Tests">
        <classes>
            <class name="com.example.tests.BrowserTest"/>
        </classes>
    </test>

</suite>
```

### Class-Level Parallelism

Run test classes in parallel:

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Parallel Classes" parallel="classes" thread-count="4">

    <test name="All Tests">
        <classes>
            <class name="com.example.tests.UserServiceTest"/>
            <class name="com.example.tests.ProductServiceTest"/>
            <class name="com.example.tests.OrderServiceTest"/>
            <class name="com.example.tests.PaymentServiceTest"/>
        </classes>
    </test>

</suite>
```

### Method-Level Parallelism

Run test methods in parallel:

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Parallel Methods" parallel="methods" thread-count="5">

    <test name="Service Tests">
        <classes>
            <class name="com.example.tests.IndependentMethodsTest"/>
        </classes>
    </test>

</suite>
```

### Instance-Level Parallelism

Run test instances in parallel (useful with Factory):

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Parallel Instances" parallel="instances" thread-count="3">

    <test name="Factory Tests">
        <classes>
            <class name="com.example.tests.FactoryGeneratedTest"/>
        </classes>
    </test>

</suite>
```

## Thread Pool Configuration

### Basic Thread Configuration

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Thread Pool Suite" parallel="methods" thread-count="10">
    <!-- Global thread pool configuration -->

    <test name="Test Group 1" thread-count="5">
        <!-- Override for this specific test -->
        <classes>
            <class name="com.example.tests.Test1"/>
        </classes>
    </test>

    <test name="Test Group 2">
        <!-- Uses suite-level thread-count -->
        <classes>
            <class name="com.example.tests.Test2"/>
        </classes>
    </test>

</suite>
```

### Data Provider Parallel Execution

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="DataProvider Suite" data-provider-thread-count="20">

    <test name="Data Driven Tests">
        <classes>
            <class name="com.example.tests.ParallelDataProviderTest"/>
        </classes>
    </test>

</suite>
```

```java
public class ParallelDataProviderTest {

    @DataProvider(name = "largeDataSet", parallel = true)
    public Object[][] provideLargeDataSet() {
        Object[][] data = new Object[100][2];
        for (int i = 0; i < 100; i++) {
            data[i] = new Object[]{"User" + i, "user" + i + "@example.com"};
        }
        return data;
    }

    @Test(dataProvider = "largeDataSet")
    public void testWithParallelData(String name, String email) {
        System.out.println(Thread.currentThread().getName() + " - Testing: " + name);
        // Each data row runs in parallel
    }
}
```

## Thread Safety Patterns

### Thread-Local Storage

```java
import org.testng.annotations.*;

public class ThreadLocalTest {

    // Thread-local storage for test-specific resources
    private static ThreadLocal<WebDriver> driverThread = new ThreadLocal<>();
    private static ThreadLocal<String> sessionThread = new ThreadLocal<>();

    @BeforeMethod
    public void setUp() {
        // Initialize thread-local resources
        driverThread.set(createWebDriver());
        sessionThread.set(generateSessionId());
    }

    @AfterMethod
    public void tearDown() {
        // Clean up thread-local resources
        WebDriver driver = driverThread.get();
        if (driver != null) {
            driver.quit();
        }
        driverThread.remove();
        sessionThread.remove();
    }

    @Test
    public void testParallelBrowser() {
        WebDriver driver = driverThread.get();
        String session = sessionThread.get();
        System.out.println("Thread: " + Thread.currentThread().getName() +
                          " Session: " + session);
        // Use thread-local driver
    }

    private WebDriver createWebDriver() {
        // Create browser instance
        return new ChromeDriver();
    }

    private String generateSessionId() {
        return UUID.randomUUID().toString();
    }
}
```

### Synchronized Shared Resources

```java
import org.testng.annotations.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.ConcurrentHashMap;

public class SynchronizedResourceTest {

    // Thread-safe counter
    private static AtomicInteger testCounter = new AtomicInteger(0);

    // Thread-safe collection
    private static ConcurrentHashMap<String, String> sharedCache = new ConcurrentHashMap<>();

    // Lock object for critical sections
    private static final Object lock = new Object();

    @Test(threadPoolSize = 5, invocationCount = 100)
    public void testAtomicOperations() {
        int count = testCounter.incrementAndGet();
        System.out.println("Test count: " + count);
    }

    @Test(threadPoolSize = 3, invocationCount = 50)
    public void testConcurrentMap() {
        String threadName = Thread.currentThread().getName();
        sharedCache.put(threadName, String.valueOf(System.currentTimeMillis()));
        // Thread-safe without explicit synchronization
    }

    @Test(threadPoolSize = 2, invocationCount = 10)
    public void testSynchronizedBlock() {
        synchronized (lock) {
            // Critical section - only one thread at a time
            performCriticalOperation();
        }
    }

    private void performCriticalOperation() {
        // Operations that require exclusive access
    }
}
```

### Immutable Test Data

```java
import java.util.Collections;
import java.util.List;
import java.util.Arrays;

public class ImmutableDataTest {

    // Immutable test data - inherently thread-safe
    private static final List<String> TEST_USERS = Collections.unmodifiableList(
        Arrays.asList("user1", "user2", "user3", "user4", "user5")
    );

    private static final Map<String, String> CONFIG = Collections.unmodifiableMap(
        Map.of(
            "url", "https://api.example.com",
            "timeout", "30000",
            "retries", "3"
        )
    );

    @Test(threadPoolSize = 5, invocationCount = 20)
    public void testWithImmutableData() {
        // Safe to read from multiple threads
        int userIndex = ThreadLocalRandom.current().nextInt(TEST_USERS.size());
        String user = TEST_USERS.get(userIndex);
        String url = CONFIG.get("url");

        System.out.println(Thread.currentThread().getName() +
                          " - User: " + user + ", URL: " + url);
    }
}
```

## Test Isolation Patterns

### Independent Test Methods

```java
public class IndependentTestsExample {

    // Each test method is completely independent
    @Test
    public void testFeatureA() {
        // Create its own resources
        UserService service = new UserService();
        User user = service.createUser("testA");
        assertNotNull(user);
        // Clean up
        service.deleteUser(user.getId());
    }

    @Test
    public void testFeatureB() {
        // Completely separate from testFeatureA
        ProductService service = new ProductService();
        Product product = service.createProduct("testB");
        assertNotNull(product);
        service.deleteProduct(product.getId());
    }

    @Test
    public void testFeatureC() {
        // No shared state with other tests
        OrderService service = new OrderService();
        Order order = service.createOrder();
        assertNotNull(order);
        service.cancelOrder(order.getId());
    }
}
```

### Isolated Database Tests

```java
import org.testng.annotations.*;

public class IsolatedDatabaseTest {

    private Connection connection;
    private String testSchema;

    @BeforeMethod
    public void setUp() throws SQLException {
        // Create isolated schema for each test
        testSchema = "test_" + Thread.currentThread().getId() + "_" + System.currentTimeMillis();
        connection = DriverManager.getConnection(DB_URL, USER, PASSWORD);
        connection.createStatement().execute("CREATE SCHEMA " + testSchema);
        connection.setCatalog(testSchema);
        initializeTestData();
    }

    @AfterMethod
    public void tearDown() throws SQLException {
        // Drop isolated schema
        connection.createStatement().execute("DROP SCHEMA " + testSchema + " CASCADE");
        connection.close();
    }

    @Test
    public void testDatabaseOperation1() throws SQLException {
        // Operations in isolated schema
        PreparedStatement ps = connection.prepareStatement(
            "INSERT INTO users (name) VALUES (?)"
        );
        ps.setString(1, "TestUser1");
        ps.executeUpdate();

        ResultSet rs = connection.createStatement().executeQuery(
            "SELECT COUNT(*) FROM users"
        );
        rs.next();
        assertEquals(rs.getInt(1), 1);
    }

    @Test
    public void testDatabaseOperation2() throws SQLException {
        // Completely isolated from testDatabaseOperation1
        PreparedStatement ps = connection.prepareStatement(
            "INSERT INTO products (name) VALUES (?)"
        );
        ps.setString(1, "TestProduct");
        ps.executeUpdate();
    }

    private void initializeTestData() throws SQLException {
        // Create tables in isolated schema
    }
}
```

## Parallel Execution with Dependencies

### Preserving Order Within Groups

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Ordered Parallel" parallel="classes" thread-count="3">

    <test name="Ordered Test" preserve-order="true">
        <classes>
            <!-- Classes run in parallel, methods in order -->
            <class name="com.example.tests.OrderedTest1">
                <methods>
                    <include name="step1"/>
                    <include name="step2"/>
                    <include name="step3"/>
                </methods>
            </class>
            <class name="com.example.tests.OrderedTest2"/>
        </classes>
    </test>

</suite>
```

### Group Threading

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Group Threading" parallel="methods" thread-count="4" group-by-instances="true">

    <test name="Instance Grouped">
        <classes>
            <class name="com.example.tests.InstanceGroupTest"/>
        </classes>
    </test>

</suite>
```

```java
public class InstanceGroupTest {

    private String instanceId;

    @Factory
    public Object[] createInstances() {
        return new Object[] {
            new InstanceGroupTest("instance1"),
            new InstanceGroupTest("instance2"),
            new InstanceGroupTest("instance3")
        };
    }

    public InstanceGroupTest() {}

    public InstanceGroupTest(String instanceId) {
        this.instanceId = instanceId;
    }

    @Test
    public void step1() {
        System.out.println(instanceId + " - Step 1");
    }

    @Test(dependsOnMethods = "step1")
    public void step2() {
        System.out.println(instanceId + " - Step 2");
    }

    @Test(dependsOnMethods = "step2")
    public void step3() {
        System.out.println(instanceId + " - Step 3");
    }
}
```

## Performance Optimization

### Optimal Thread Count

```java
public class ThreadCountOptimization {

    // Determine optimal thread count based on available resources
    public static int getOptimalThreadCount() {
        int availableProcessors = Runtime.getRuntime().availableProcessors();

        // For CPU-bound tests
        int cpuBoundThreads = availableProcessors;

        // For I/O-bound tests (network, file, database)
        int ioBoundThreads = availableProcessors * 2;

        // For mixed workloads
        int mixedThreads = (int) (availableProcessors * 1.5);

        return mixedThreads;
    }
}
```

### Resource Pool Pattern

```java
import java.util.concurrent.*;

public class ResourcePoolTest {

    // Connection pool for parallel tests
    private static BlockingQueue<Connection> connectionPool;

    @BeforeSuite
    public void setUpSuite() {
        int poolSize = 10;
        connectionPool = new ArrayBlockingQueue<>(poolSize);
        for (int i = 0; i < poolSize; i++) {
            connectionPool.offer(createConnection());
        }
    }

    @AfterSuite
    public void tearDownSuite() {
        Connection conn;
        while ((conn = connectionPool.poll()) != null) {
            closeConnection(conn);
        }
    }

    @Test(threadPoolSize = 5, invocationCount = 50)
    public void testWithPooledConnection() throws InterruptedException {
        Connection conn = connectionPool.take(); // Borrow
        try {
            // Use connection
            performDatabaseOperation(conn);
        } finally {
            connectionPool.offer(conn); // Return
        }
    }

    private Connection createConnection() {
        // Create database connection
        return null;
    }

    private void closeConnection(Connection conn) {
        // Close connection
    }

    private void performDatabaseOperation(Connection conn) {
        // Database operations
    }
}
```

## Reporting for Parallel Tests

### Custom Reporter for Parallel Execution

```java
import org.testng.*;
import java.util.concurrent.ConcurrentHashMap;

public class ParallelTestReporter implements ITestListener {

    private static ConcurrentHashMap<Long, List<String>> threadTestMap =
        new ConcurrentHashMap<>();

    @Override
    public void onTestStart(ITestResult result) {
        long threadId = Thread.currentThread().getId();
        threadTestMap.computeIfAbsent(threadId, k -> new CopyOnWriteArrayList<>())
                     .add(result.getName());
    }

    @Override
    public void onFinish(ITestContext context) {
        System.out.println("\n=== Thread Distribution Report ===");
        threadTestMap.forEach((threadId, tests) -> {
            System.out.println("Thread " + threadId + ": " + tests.size() + " tests");
            tests.forEach(test -> System.out.println("  - " + test));
        });
        System.out.println("Total threads used: " + threadTestMap.size());
    }
}
```

### Timeout Configuration

```java
public class TimeoutTest {

    @Test(timeOut = 5000)
    public void testWithTimeout() {
        // Fails if takes more than 5 seconds
    }

    @Test(timeOut = 10000, threadPoolSize = 3, invocationCount = 10)
    public void testParallelWithTimeout() {
        // Each invocation has 10 second timeout
    }
}
```

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Timeout Suite" time-out="60000">
    <!-- Suite-level timeout: 60 seconds total -->

    <test name="Quick Tests" time-out="10000">
        <!-- Test-level timeout: 10 seconds for all tests in this group -->
        <classes>
            <class name="com.example.tests.QuickTest"/>
        </classes>
    </test>

</suite>
```

## Best Practices

1. **Design for independence** - Tests should not depend on shared mutable state
2. **Use ThreadLocal for per-thread resources** - Drivers, sessions, connections
3. **Prefer immutable data** - Thread-safe by design
4. **Set appropriate thread counts** - Based on resource availability
5. **Implement proper cleanup** - Prevent resource leaks in parallel execution
6. **Use thread-safe collections** - ConcurrentHashMap, CopyOnWriteArrayList
7. **Configure timeouts** - Prevent hung tests from blocking threads
8. **Monitor thread distribution** - Ensure balanced workload
9. **Test locally first** - Verify thread safety before CI/CD
10. **Document thread safety requirements** - Clear expectations for test authors

## Common Pitfalls

1. **Shared mutable state** - Causes race conditions and flaky tests
2. **Static fields without synchronization** - Not thread-safe
3. **Resource contention** - Too many threads competing for limited resources
4. **Order dependencies** - Tests that assume execution order
5. **Missing cleanup** - ThreadLocal resources not removed
6. **Insufficient isolation** - Database tests affecting each other
7. **Too many threads** - Overhead exceeds benefits
8. **Ignoring timeouts** - Hung tests blocking execution
9. **Non-deterministic failures** - Hard to reproduce parallel issues
10. **Improper connection pooling** - Connection leaks or exhaustion

## When to Use This Skill

- Reducing test suite execution time
- Configuring CI/CD parallel test execution
- Implementing thread-safe test infrastructure
- Designing parallel-friendly test architecture
- Troubleshooting parallel test failures
- Optimizing resource utilization in tests
- Building scalable test frameworks
- Implementing cross-browser parallel testing
