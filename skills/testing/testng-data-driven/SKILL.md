---
name: testng-data-driven
description: Use when implementing data-driven tests with TestNG DataProviders, factory methods, and parameterization patterns.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# TestNG Data-Driven Testing

Master TestNG data-driven testing including DataProviders, Factory patterns, and parameterization for comprehensive test coverage. This skill covers techniques for testing with multiple data sets efficiently.

## Overview

Data-driven testing separates test logic from test data, enabling a single test method to run against multiple inputs. TestNG provides powerful features for data-driven testing through DataProviders, Factory methods, and XML parameterization.

## DataProvider Basics

### Simple DataProvider

```java
import org.testng.annotations.*;
import static org.testng.Assert.*;

public class SimpleDataProviderTest {

    @DataProvider(name = "numbers")
    public Object[][] provideNumbers() {
        return new Object[][] {
            {1, 2, 3},
            {4, 5, 9},
            {0, 0, 0},
            {-1, 1, 0}
        };
    }

    @Test(dataProvider = "numbers")
    public void testAddition(int a, int b, int expected) {
        assertEquals(a + b, expected);
    }
}
```

### DataProvider with Single Values

```java
public class SingleValueDataProviderTest {

    @DataProvider(name = "validEmails")
    public Object[][] provideValidEmails() {
        return new Object[][] {
            {"user@example.com"},
            {"test.user@domain.org"},
            {"admin+tag@company.co.uk"},
            {"user123@test.io"}
        };
    }

    @Test(dataProvider = "validEmails")
    public void testValidEmail(String email) {
        assertTrue(isValidEmail(email), "Email should be valid: " + email);
    }

    private boolean isValidEmail(String email) {
        return email != null && email.matches("^[\\w+.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$");
    }
}
```

## Advanced DataProvider Patterns

### DataProvider in Separate Class

```java
// DataProviders class
public class TestDataProviders {

    @DataProvider(name = "userData")
    public static Object[][] provideUserData() {
        return new Object[][] {
            {"john", "john@example.com", 25},
            {"jane", "jane@example.com", 30},
            {"bob", "bob@example.com", 22}
        };
    }

    @DataProvider(name = "loginCredentials")
    public static Object[][] provideLoginCredentials() {
        return new Object[][] {
            {"admin", "admin123", true},
            {"user", "user456", true},
            {"invalid", "wrong", false}
        };
    }
}

// Test class using external DataProvider
public class UserTest {

    @Test(dataProvider = "userData", dataProviderClass = TestDataProviders.class)
    public void testUserCreation(String name, String email, int age) {
        User user = new User(name, email, age);
        assertNotNull(user);
        assertEquals(user.getName(), name);
        assertEquals(user.getEmail(), email);
        assertEquals(user.getAge(), age);
    }

    @Test(dataProvider = "loginCredentials", dataProviderClass = TestDataProviders.class)
    public void testLogin(String username, String password, boolean expectedSuccess) {
        boolean result = authService.login(username, password);
        assertEquals(result, expectedSuccess);
    }
}
```

### DataProvider with Method Context

```java
import org.testng.ITestContext;
import org.testng.annotations.*;
import java.lang.reflect.Method;

public class ContextAwareDataProviderTest {

    @DataProvider(name = "contextAwareData")
    public Object[][] provideContextAwareData(ITestContext context, Method method) {
        String testName = method.getName();
        String suiteName = context.getSuite().getName();

        System.out.println("Providing data for: " + testName + " in suite: " + suiteName);

        if (testName.contains("Admin")) {
            return new Object[][] {
                {"admin", "ADMIN_ROLE"},
                {"superadmin", "SUPER_ADMIN_ROLE"}
            };
        } else {
            return new Object[][] {
                {"user1", "USER_ROLE"},
                {"user2", "USER_ROLE"}
            };
        }
    }

    @Test(dataProvider = "contextAwareData")
    public void testAdminAccess(String username, String role) {
        // Test admin access
    }

    @Test(dataProvider = "contextAwareData")
    public void testUserAccess(String username, String role) {
        // Test user access
    }
}
```

### Parallel DataProvider

```java
public class ParallelDataProviderTest {

    @DataProvider(name = "parallelData", parallel = true)
    public Object[][] provideParallelData() {
        return new Object[][] {
            {"Test 1"},
            {"Test 2"},
            {"Test 3"},
            {"Test 4"},
            {"Test 5"},
            {"Test 6"},
            {"Test 7"},
            {"Test 8"},
            {"Test 9"},
            {"Test 10"}
        };
    }

    @Test(dataProvider = "parallelData")
    public void testParallel(String data) {
        System.out.println(Thread.currentThread().getName() + " - " + data);
        // Tests run in parallel threads
    }
}
```

### Iterator DataProvider

```java
import java.util.Iterator;
import java.util.Arrays;

public class IteratorDataProviderTest {

    @DataProvider(name = "iteratorData")
    public Iterator<Object[]> provideIteratorData() {
        // Useful for large datasets - generates data on demand
        return Arrays.asList(
            new Object[]{"data1", 1},
            new Object[]{"data2", 2},
            new Object[]{"data3", 3}
        ).iterator();
    }

    @Test(dataProvider = "iteratorData")
    public void testWithIterator(String name, int value) {
        assertNotNull(name);
        assertTrue(value > 0);
    }
}
```

### Lazy DataProvider for Large Datasets

```java
import java.util.Iterator;
import java.util.NoSuchElementException;

public class LazyDataProviderTest {

    @DataProvider(name = "lazyData")
    public Iterator<Object[]> provideLazyData() {
        return new Iterator<Object[]>() {
            private int current = 0;
            private final int max = 1000;

            @Override
            public boolean hasNext() {
                return current < max;
            }

            @Override
            public Object[] next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                // Generate data on demand
                return new Object[]{
                    "User_" + current,
                    "user" + current + "@example.com",
                    current++
                };
            }
        };
    }

    @Test(dataProvider = "lazyData")
    public void testLargeDataset(String name, String email, int id) {
        assertNotNull(name);
        assertTrue(email.contains("@"));
    }
}
```

## Factory Pattern

### Basic Factory

```java
import org.testng.annotations.*;

public class FactoryTest {
    private String browser;

    @Factory
    public static Object[] createInstances() {
        return new Object[] {
            new FactoryTest("chrome"),
            new FactoryTest("firefox"),
            new FactoryTest("safari")
        };
    }

    public FactoryTest(String browser) {
        this.browser = browser;
    }

    @Test
    public void testHomePage() {
        System.out.println("Testing home page on: " + browser);
    }

    @Test
    public void testLoginPage() {
        System.out.println("Testing login page on: " + browser);
    }
}
```

### Factory with DataProvider

```java
public class FactoryWithDataProviderTest {
    private String username;
    private String role;

    @Factory(dataProvider = "userRoles")
    public FactoryWithDataProviderTest(String username, String role) {
        this.username = username;
        this.role = role;
    }

    @DataProvider(name = "userRoles")
    public static Object[][] provideUserRoles() {
        return new Object[][] {
            {"admin", "ADMIN"},
            {"manager", "MANAGER"},
            {"user", "USER"},
            {"guest", "GUEST"}
        };
    }

    @Test
    public void testUserPermissions() {
        System.out.println("Testing permissions for " + username + " with role " + role);
        // Test specific permissions based on role
    }

    @Test
    public void testUserDashboard() {
        System.out.println("Testing dashboard for " + username + " with role " + role);
        // Test dashboard features based on role
    }

    @Override
    public String toString() {
        return username + "_" + role;
    }
}
```

## External Data Sources

### CSV DataProvider

```java
import java.io.*;
import java.util.*;

public class CsvDataProviderTest {

    @DataProvider(name = "csvData")
    public Object[][] provideCsvData() throws IOException {
        List<Object[]> data = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(
                new FileReader("src/test/resources/testdata.csv"))) {

            String line;
            // Skip header
            reader.readLine();

            while ((line = reader.readLine()) != null) {
                String[] values = line.split(",");
                data.add(new Object[]{
                    values[0].trim(),  // username
                    values[1].trim(),  // email
                    Integer.parseInt(values[2].trim())  // age
                });
            }
        }

        return data.toArray(new Object[0][]);
    }

    @Test(dataProvider = "csvData")
    public void testUserFromCsv(String username, String email, int age) {
        assertNotNull(username);
        assertTrue(email.contains("@"));
        assertTrue(age > 0);
    }
}
```

### JSON DataProvider

```java
import com.fasterxml.jackson.databind.*;
import java.io.*;
import java.util.*;

public class JsonDataProviderTest {

    @DataProvider(name = "jsonData")
    public Object[][] provideJsonData() throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        List<Map<String, Object>> testData = mapper.readValue(
            new File("src/test/resources/testdata.json"),
            new TypeReference<List<Map<String, Object>>>() {}
        );

        Object[][] data = new Object[testData.size()][3];
        for (int i = 0; i < testData.size(); i++) {
            Map<String, Object> entry = testData.get(i);
            data[i][0] = entry.get("name");
            data[i][1] = entry.get("email");
            data[i][2] = ((Number) entry.get("age")).intValue();
        }

        return data;
    }

    @Test(dataProvider = "jsonData")
    public void testUserFromJson(String name, String email, int age) {
        assertNotNull(name);
        assertFalse(name.isEmpty());
    }
}
```

### Excel DataProvider

```java
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.*;
import java.util.*;

public class ExcelDataProviderTest {

    @DataProvider(name = "excelData")
    public Object[][] provideExcelData() throws IOException {
        List<Object[]> data = new ArrayList<>();

        try (FileInputStream fis = new FileInputStream("src/test/resources/testdata.xlsx");
             Workbook workbook = new XSSFWorkbook(fis)) {

            Sheet sheet = workbook.getSheetAt(0);

            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row != null) {
                    data.add(new Object[]{
                        getCellValue(row.getCell(0)),
                        getCellValue(row.getCell(1)),
                        (int) row.getCell(2).getNumericCellValue()
                    });
                }
            }
        }

        return data.toArray(new Object[0][]);
    }

    private String getCellValue(Cell cell) {
        if (cell == null) return "";
        return cell.getCellType() == CellType.STRING
            ? cell.getStringCellValue()
            : String.valueOf((int) cell.getNumericCellValue());
    }

    @Test(dataProvider = "excelData")
    public void testUserFromExcel(String name, String email, int age) {
        assertNotNull(name);
        assertTrue(age >= 0);
    }
}
```

## Advanced Parameterization

### Optional Parameters

```java
public class OptionalParameterTest {

    @Parameters({"browser", "timeout"})
    @BeforeClass
    public void setUp(
            String browser,
            @Optional("30000") String timeout) {

        System.out.println("Browser: " + browser);
        System.out.println("Timeout: " + timeout);
    }

    @Test
    public void testMethod() {
        // Test implementation
    }
}
```

### Combining Parameters and DataProviders

```java
public class CombinedParametersTest {

    private String environment;

    @Parameters("environment")
    @BeforeClass
    public void setUp(String environment) {
        this.environment = environment;
    }

    @DataProvider(name = "users")
    public Object[][] provideUsers() {
        return new Object[][] {
            {"user1", "pass1"},
            {"user2", "pass2"}
        };
    }

    @Test(dataProvider = "users")
    public void testLogin(String username, String password) {
        System.out.println("Testing on " + environment + " with user: " + username);
        // Combine XML parameter with DataProvider data
    }
}
```

### Dynamic DataProvider Based on Parameters

```java
public class DynamicDataProviderTest {

    private static String environment;

    @Parameters("environment")
    @BeforeClass
    public static void setUp(@Optional("staging") String env) {
        environment = env;
    }

    @DataProvider(name = "environmentData")
    public Object[][] provideEnvironmentData() {
        switch (environment) {
            case "production":
                return new Object[][] {
                    {"prod-user1", "prod-api-key-1"},
                    {"prod-user2", "prod-api-key-2"}
                };
            case "staging":
                return new Object[][] {
                    {"staging-user1", "staging-api-key-1"},
                    {"staging-user2", "staging-api-key-2"}
                };
            default:
                return new Object[][] {
                    {"dev-user", "dev-api-key"}
                };
        }
    }

    @Test(dataProvider = "environmentData")
    public void testApiAccess(String user, String apiKey) {
        System.out.println("Testing API access for: " + user + " on " + environment);
    }
}
```

## Data Provider Naming

### Named Data Provider Rows

```java
public class NamedDataProviderTest {

    @DataProvider(name = "testCases")
    public Object[][] provideTestCases() {
        return new Object[][] {
            // Each row can have a name for better reporting
            {"TC001_ValidLogin", "admin", "admin123", true},
            {"TC002_InvalidPassword", "admin", "wrong", false},
            {"TC003_EmptyUsername", "", "password", false},
            {"TC004_SpecialCharacters", "user@#$", "pass@#$", false}
        };
    }

    @Test(dataProvider = "testCases")
    public void testLogin(String testCaseId, String username, String password, boolean expected) {
        System.out.println("Executing: " + testCaseId);
        // Test implementation
    }
}
```

## Best Practices

1. **Keep DataProviders focused** - One DataProvider per data type or scenario
2. **Use external files for large datasets** - CSV, JSON, or Excel for maintainability
3. **Make DataProviders static when shared** - Required for external DataProvider classes
4. **Include test case identifiers** - First column can be test case ID for tracing
5. **Use meaningful DataProvider names** - Clear names improve test reports
6. **Consider parallel execution** - Enable parallel flag for independent tests
7. **Handle null values explicitly** - Define behavior for null/empty data
8. **Document expected formats** - Comment data structure for complex providers
9. **Use Iterator for large datasets** - Avoid memory issues with lazy loading
10. **Separate test data from test logic** - Keep tests clean and data manageable

## Common Pitfalls

1. **Type mismatches** - DataProvider types must match test method parameters
2. **Missing static modifier** - External DataProvider methods must be static
3. **Array dimension errors** - Must return Object[][] not Object[]
4. **Null pointer exceptions** - Not handling null values in data
5. **Resource leaks** - Not closing file streams in DataProviders
6. **Tight coupling** - Hard-coding environment-specific data
7. **Over-parameterization** - Too many parameters make tests hard to read
8. **Missing test case IDs** - Hard to trace failures without identifiers
9. **Ignoring execution order** - DataProvider rows may run in any order
10. **Not considering parallelism** - Shared state issues with parallel DataProviders

## When to Use This Skill

- Testing with multiple input combinations
- Implementing boundary value testing
- Creating cross-browser or cross-environment tests
- Loading test data from external sources
- Building parameterized test suites
- Creating data-driven API tests
- Implementing database-driven tests
- Building reusable test data frameworks
