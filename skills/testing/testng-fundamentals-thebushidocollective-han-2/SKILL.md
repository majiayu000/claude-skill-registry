---
name: testng-fundamentals
description: Use when working with TestNG annotations, assertions, test lifecycle, and configuration for Java testing.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# TestNG Fundamentals

Master TestNG fundamentals including annotations, assertions, test lifecycle, and XML configuration for Java testing. This skill provides comprehensive coverage of essential concepts, patterns, and best practices for professional TestNG development.

## Overview

TestNG is a powerful testing framework for Java inspired by JUnit and NUnit, designed to cover a wider range of test categories: unit, functional, end-to-end, and integration testing. It supports annotations, data-driven testing, parameterization, and parallel execution.

## Installation and Setup

### Maven Configuration

Add TestNG to your Maven project:

```xml
<dependency>
    <groupId>org.testng</groupId>
    <artifactId>testng</artifactId>
    <version>7.9.0</version>
    <scope>test</scope>
</dependency>
```

Configure the Surefire plugin for TestNG:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.2.5</version>
    <configuration>
        <suiteXmlFiles>
            <suiteXmlFile>testng.xml</suiteXmlFile>
        </suiteXmlFiles>
    </configuration>
</plugin>
```

### Gradle Configuration

Add TestNG to your Gradle project:

```groovy
dependencies {
    testImplementation 'org.testng:testng:7.9.0'
}

test {
    useTestNG()
}
```

## Core Annotations

### Test Lifecycle Annotations

TestNG provides comprehensive lifecycle annotations:

```java
import org.testng.annotations.*;

public class LifecycleTest {

    @BeforeSuite
    public void beforeSuite() {
        // Runs once before the entire test suite
        System.out.println("Before Suite");
    }

    @AfterSuite
    public void afterSuite() {
        // Runs once after the entire test suite
        System.out.println("After Suite");
    }

    @BeforeTest
    public void beforeTest() {
        // Runs before each <test> tag in testng.xml
        System.out.println("Before Test");
    }

    @AfterTest
    public void afterTest() {
        // Runs after each <test> tag in testng.xml
        System.out.println("After Test");
    }

    @BeforeClass
    public void beforeClass() {
        // Runs once before the first test method in the class
        System.out.println("Before Class");
    }

    @AfterClass
    public void afterClass() {
        // Runs once after the last test method in the class
        System.out.println("After Class");
    }

    @BeforeMethod
    public void beforeMethod() {
        // Runs before each test method
        System.out.println("Before Method");
    }

    @AfterMethod
    public void afterMethod() {
        // Runs after each test method
        System.out.println("After Method");
    }

    @Test
    public void testMethod() {
        System.out.println("Test Method");
    }
}
```

### Test Annotation Attributes

The `@Test` annotation supports various attributes:

```java
public class TestAttributesExample {

    @Test(description = "Verifies user login functionality")
    public void testLogin() {
        // Test with description
    }

    @Test(enabled = false)
    public void disabledTest() {
        // This test will not run
    }

    @Test(priority = 1)
    public void firstTest() {
        // Runs first (lower priority = earlier execution)
    }

    @Test(priority = 2)
    public void secondTest() {
        // Runs second
    }

    @Test(groups = {"smoke", "regression"})
    public void groupedTest() {
        // Test belongs to multiple groups
    }

    @Test(dependsOnMethods = {"testLogin"})
    public void testDashboard() {
        // Runs only if testLogin passes
    }

    @Test(dependsOnGroups = {"setup"})
    public void dependentTest() {
        // Runs only if all tests in "setup" group pass
    }

    @Test(timeOut = 5000)
    public void timedTest() {
        // Fails if takes more than 5 seconds
    }

    @Test(invocationCount = 3)
    public void repeatedTest() {
        // Runs 3 times
    }

    @Test(invocationCount = 100, threadPoolSize = 10)
    public void parallelRepeatedTest() {
        // Runs 100 times across 10 threads
    }

    @Test(expectedExceptions = IllegalArgumentException.class)
    public void exceptionTest() {
        throw new IllegalArgumentException("Expected");
    }

    @Test(expectedExceptions = RuntimeException.class,
          expectedExceptionsMessageRegExp = ".*invalid.*")
    public void exceptionWithMessageTest() {
        throw new RuntimeException("This is invalid input");
    }
}
```

## Assertions

### Basic Assertions

TestNG provides comprehensive assertion methods:

```java
import org.testng.Assert;
import org.testng.annotations.Test;

public class AssertionExamples {

    @Test
    public void testBasicAssertions() {
        // Equality
        Assert.assertEquals(5, 5);
        Assert.assertEquals("hello", "hello");
        Assert.assertEquals(new int[]{1, 2, 3}, new int[]{1, 2, 3});

        // Boolean
        Assert.assertTrue(true);
        Assert.assertFalse(false);

        // Null checks
        Assert.assertNull(null);
        Assert.assertNotNull("value");

        // Same reference
        String s1 = "test";
        String s2 = s1;
        Assert.assertSame(s1, s2);
        Assert.assertNotSame(new String("test"), new String("test"));
    }

    @Test
    public void testAssertionsWithMessages() {
        // Assertions with custom failure messages
        Assert.assertEquals(5, 5, "Values should be equal");
        Assert.assertTrue(true, "Condition should be true");
        Assert.assertNotNull("value", "Value should not be null");
    }

    @Test
    public void testCollectionAssertions() {
        // Array assertions
        String[] expected = {"a", "b", "c"};
        String[] actual = {"a", "b", "c"};
        Assert.assertEquals(actual, expected);

        // Unordered comparison
        String[] array1 = {"a", "b", "c"};
        String[] array2 = {"c", "a", "b"};
        Assert.assertEqualsNoOrder(array1, array2);
    }
}
```

### Soft Assertions

Soft assertions allow multiple assertions to be collected before failing:

```java
import org.testng.annotations.Test;
import org.testng.asserts.SoftAssert;

public class SoftAssertExample {

    @Test
    public void testWithSoftAssert() {
        SoftAssert softAssert = new SoftAssert();

        // All assertions are executed
        softAssert.assertEquals(1, 1, "First check");
        softAssert.assertEquals(2, 3, "Second check - will fail");
        softAssert.assertTrue(false, "Third check - will fail");
        softAssert.assertNotNull(null, "Fourth check - will fail");

        // Report all failures at the end
        softAssert.assertAll();
    }
}
```

## TestNG XML Configuration

### Basic testng.xml Structure

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="My Test Suite" verbose="1">

    <test name="Unit Tests">
        <classes>
            <class name="com.example.tests.UserServiceTest"/>
            <class name="com.example.tests.ProductServiceTest"/>
        </classes>
    </test>

    <test name="Integration Tests">
        <packages>
            <package name="com.example.integration.*"/>
        </packages>
    </test>

</suite>
```

### Group Configuration

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Group Suite">

    <test name="Smoke Tests">
        <groups>
            <run>
                <include name="smoke"/>
            </run>
        </groups>
        <packages>
            <package name="com.example.tests.*"/>
        </packages>
    </test>

    <test name="Regression Tests">
        <groups>
            <run>
                <include name="regression"/>
                <exclude name="broken"/>
            </run>
        </groups>
        <packages>
            <package name="com.example.tests.*"/>
        </packages>
    </test>

</suite>
```

### Parameters in testng.xml

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Parameterized Suite">

    <parameter name="browser" value="chrome"/>
    <parameter name="environment" value="staging"/>

    <test name="Chrome Tests">
        <parameter name="browser" value="chrome"/>
        <classes>
            <class name="com.example.tests.BrowserTest"/>
        </classes>
    </test>

    <test name="Firefox Tests">
        <parameter name="browser" value="firefox"/>
        <classes>
            <class name="com.example.tests.BrowserTest"/>
        </classes>
    </test>

</suite>
```

Using parameters in tests:

```java
import org.testng.annotations.*;

public class BrowserTest {

    @Parameters({"browser", "environment"})
    @BeforeClass
    public void setUp(String browser, @Optional("production") String env) {
        System.out.println("Browser: " + browser);
        System.out.println("Environment: " + env);
    }

    @Test
    public void testBrowser() {
        // Test implementation
    }
}
```

## Test Groups

### Defining and Using Groups

```java
public class GroupExample {

    @BeforeGroups("database")
    public void setUpDatabase() {
        System.out.println("Setting up database");
    }

    @AfterGroups("database")
    public void tearDownDatabase() {
        System.out.println("Tearing down database");
    }

    @Test(groups = {"smoke", "frontend"})
    public void testHomePage() {
        System.out.println("Testing home page");
    }

    @Test(groups = {"smoke", "api"})
    public void testHealthEndpoint() {
        System.out.println("Testing health endpoint");
    }

    @Test(groups = {"regression", "database"})
    public void testDataPersistence() {
        System.out.println("Testing data persistence");
    }

    @Test(groups = {"slow", "integration"})
    public void testEndToEnd() {
        System.out.println("Testing end-to-end flow");
    }
}
```

### Group Dependencies

```java
public class GroupDependencyExample {

    @Test(groups = {"init"})
    public void initializeSystem() {
        System.out.println("Initializing");
    }

    @Test(groups = {"init"})
    public void configureSystem() {
        System.out.println("Configuring");
    }

    @Test(dependsOnGroups = {"init"}, groups = {"core"})
    public void coreTest1() {
        System.out.println("Core test 1");
    }

    @Test(dependsOnGroups = {"init"}, groups = {"core"})
    public void coreTest2() {
        System.out.println("Core test 2");
    }

    @Test(dependsOnGroups = {"core"}, groups = {"final"})
    public void finalTest() {
        System.out.println("Final test");
    }
}
```

## Listeners

### ITestListener

```java
import org.testng.*;

public class TestListener implements ITestListener {

    @Override
    public void onTestStart(ITestResult result) {
        System.out.println("Starting: " + result.getName());
    }

    @Override
    public void onTestSuccess(ITestResult result) {
        System.out.println("Passed: " + result.getName());
    }

    @Override
    public void onTestFailure(ITestResult result) {
        System.out.println("Failed: " + result.getName());
        System.out.println("Reason: " + result.getThrowable().getMessage());
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        System.out.println("Skipped: " + result.getName());
    }

    @Override
    public void onStart(ITestContext context) {
        System.out.println("Test suite starting: " + context.getName());
    }

    @Override
    public void onFinish(ITestContext context) {
        System.out.println("Test suite finished: " + context.getName());
    }
}
```

### Using Listeners

```java
// Using annotation
@Listeners(TestListener.class)
public class MyTest {
    @Test
    public void testMethod() {
        // Test implementation
    }
}
```

Or in testng.xml:

```xml
<suite name="Suite">
    <listeners>
        <listener class-name="com.example.listeners.TestListener"/>
    </listeners>
    <test name="Test">
        <classes>
            <class name="com.example.tests.MyTest"/>
        </classes>
    </test>
</suite>
```

## Best Practices

1. **Use descriptive test names** - Name tests clearly to indicate what they verify
2. **Group related tests** - Use groups to organize tests by feature or type
3. **Avoid test dependencies** - Tests should be independent when possible
4. **Use soft assertions wisely** - For multiple related checks in one test
5. **Configure timeouts** - Prevent tests from hanging indefinitely
6. **Use BeforeClass/AfterClass** - For expensive setup/teardown operations
7. **Leverage testng.xml** - For suite-level configuration and organization
8. **Implement listeners** - For custom reporting and test lifecycle hooks
9. **Use priority sparingly** - Prefer dependency declarations over priority
10. **Document test purpose** - Use the description attribute

## Common Pitfalls

1. **Test order dependency** - Relying on implicit test execution order
2. **Shared mutable state** - Tests modifying shared resources
3. **Missing assertions** - Tests without verification
4. **Overly broad groups** - Groups that are too generic to be useful
5. **Circular dependencies** - Tests that depend on each other in a cycle
6. **Long-running tests** - Tests without appropriate timeouts
7. **Poor failure messages** - Assertions without descriptive messages
8. **Ignoring test failures** - Using enabled=false to hide failing tests
9. **Hard-coded test data** - Not using parameters or data providers
10. **Missing cleanup** - Not properly releasing resources in @After methods

## When to Use This Skill

- Setting up TestNG in new Java projects
- Writing unit and integration tests with TestNG
- Configuring test suites with testng.xml
- Organizing tests with groups and dependencies
- Implementing custom test listeners
- Troubleshooting TestNG test failures
- Migrating from JUnit to TestNG
- Training team members on TestNG fundamentals
