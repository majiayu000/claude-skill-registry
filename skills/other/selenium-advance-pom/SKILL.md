---
name: Selenium Advanced POM Framework
description: Advanced Selenium WebDriver framework with three Page Object Model patterns (Basic POM, Improved POM, Page Factory), retry mechanisms, Allure reporting, Excel data-driven testing, and Selenoid grid support.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [selenium, java, pom, page-object-model, page-factory, allure, testng, data-driven, selenoid, retry]
testingTypes: [e2e]
frameworks: [selenium]
languages: [java]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Selenium Advanced POM Framework Skill

You are an expert QA automation engineer specializing in advanced Selenium WebDriver frameworks with Java. When the user asks you to build, review, or debug a Selenium test automation framework, follow these detailed instructions covering three Page Object Model patterns, retry mechanisms, data-driven testing, and cloud grid execution.

## Core Principles

1. **Three POM patterns** -- Implement Basic POM, Improved POM (with inheritance), and Page Factory depending on project needs.
2. **CommonToAllPage base class** -- Centralize reusable page actions (click, type, getText) in a single base class that all page objects extend.
3. **DriverManager singleton** -- Manage WebDriver lifecycle through a centralized DriverManager with static getter/setter and multi-browser support.
4. **Listener-driven reporting** -- Use TestNG listeners (ITestListener, IRetryAnalyzer, IAnnotationTransformer) for automatic screenshots, retry logic, and Allure integration.
5. **Data externalization** -- Store test data in properties files and Excel spreadsheets, never hardcoded in test methods.
6. **Wait strategy hierarchy** -- Prefer explicit waits via WebDriverWait, use fluent waits for polling scenarios, avoid Thread.sleep entirely.
7. **Environment-specific suites** -- Maintain separate TestNG XML suite files for QA, staging, and production environments.
8. **Grid-ready architecture** -- Design the framework to run locally or on Selenoid/Docker grid without code changes.

## Project Structure

```
src/
  main/java/com/thetestingacademy/
    base/
      CommonToAllPage.java            # Base class for all page objects
    driver/
      DriverManager.java              # WebDriver lifecycle management
    pages/
      pageFactory/vwo/
        LoginPage_PF.java             # Page Factory pattern (@FindBy)
        DashBoardPage_PF.java
      pageObjectModel/
        normal_POM/normal_POM/vwo/
          LoginPage.java              # Basic POM pattern
          DashBoardPage.java
          ForgetPasswordPage.java
          FreeTrial.java
          SupportPage.java
        normal_POM/imporved_POM/vwo/
          LoginPage.java              # Improved POM (extends CommonToAllPage)
          DashBoardPage.java
    utils/
      PropertiesReader.java           # Config from .properties files
      WaitHelpers.java                # Explicit, Fluent, Implicit waits
  main/resources/
    data.properties                   # Test configuration & credentials
    log4j2.xml                        # Logging configuration
  test/java/com/thetestingacademy/
    base/
      CommonToAllTest.java            # Base test class (setUp/tearDown)
    listeners/
      RetryAnalyzer.java              # IRetryAnalyzer implementation
      RetryListener.java              # IAnnotationTransformer for global retry
      ScreenshotListener.java         # Screenshot on failure + Allure attach
    tests/
      sample/
        TestCaseBoilerPlate.java      # Test template
      pageFactoryTests/vwo/
        TestVWOLogin_PF.java          # Page Factory tests
      pageObjectModelTests/vwo/
        TestVWOLogin_01_NormalScript_POM.java
        TestVWOLogin_02_PropertyReader_DriverManager_POM_CommonToAll.java
        TestVWOLogin_03_Retry.java    # Tests with retry logic
    utilexcel/
      UtilExcel.java                  # Apache POI Excel reader
  test/resources/
    TestData.xlsx                     # Excel test data
testng_vwo_normal_s1.xml              # Basic test suite
testng_vwo_qa.xml                     # QA environment suite
testng_vwo_prod.xml                   # Production suite
testng_vwo_retry.xml                  # Retry + listeners suite
pom.xml
```

## Maven Dependencies

```xml
<dependencies>
    <dependency>
        <groupId>org.seleniumhq.selenium</groupId>
        <artifactId>selenium-java</artifactId>
        <version>4.31.0</version>
    </dependency>
    <dependency>
        <groupId>org.testng</groupId>
        <artifactId>testng</artifactId>
        <version>7.11.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.qameta.allure</groupId>
        <artifactId>allure-testng</artifactId>
        <version>2.26.0</version>
    </dependency>
    <dependency>
        <groupId>org.uncommons</groupId>
        <artifactId>reportng</artifactId>
        <version>1.1.2</version>
    </dependency>
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>3.25.1</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.apache.poi</groupId>
        <artifactId>poi-ooxml</artifactId>
        <version>5.2.4</version>
    </dependency>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <version>3.0.0-beta2</version>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>11</source>
                <target>11</target>
            </configuration>
        </plugin>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.5</version>
            <configuration>
                <suiteXmlFiles>
                    <suiteXmlFile>testng.xml</suiteXmlFile>
                </suiteXmlFiles>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## Driver Management

```java
package com.thetestingacademy.driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class DriverManager {
    private static WebDriver driver;

    public static WebDriver getDriver() {
        return driver;
    }

    public static void setDriver(WebDriver driver) {
        DriverManager.driver = driver;
    }

    public static void init() {
        String browser = PropertiesReader.readKey("browser");
        switch (browser.toLowerCase()) {
            case "chrome":
                ChromeOptions chromeOptions = new ChromeOptions();
                chromeOptions.addArguments("--guest");
                driver = new ChromeDriver(chromeOptions);
                break;
            case "edge":
                driver = new EdgeDriver();
                break;
            case "firefox":
                driver = new FirefoxDriver();
                break;
            default:
                driver = new ChromeDriver();
        }
        driver.manage().window().maximize();
    }

    public static void down() {
        if (driver != null) {
            driver.quit();
            driver = null;
        }
    }
}
```

## Page Object Model -- Pattern 1: Basic POM

The simplest POM pattern where each page class owns its locators and uses `driver.findElement()` directly.

```java
package com.thetestingacademy.pages.pageObjectModel.normal_POM.normal_POM.vwo;

import com.thetestingacademy.utils.PropertiesReader;
import com.thetestingacademy.utils.WaitHelpers;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage {
    private WebDriver driver;

    // Locators
    private By username = By.id("login-username");
    private By password = By.id("login-password");
    private By signButton = By.id("js-login-btn");
    private By error_message = By.cssSelector("[data-qa='error-text']");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public String loginToVWOLoginInvalidCreds(String user, String pwd) {
        driver.get(PropertiesReader.readKey("url"));
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pwd);
        driver.findElement(signButton).click();
        WaitHelpers.checkVisibility(driver, error_message, 3);
        return driver.findElement(error_message).getText();
    }

    public void loginToVWOLoginValidCreds(String user, String pwd) {
        driver.get(PropertiesReader.readKey("url"));
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pwd);
        driver.findElement(signButton).click();
    }
}
```

## Page Object Model -- Pattern 2: Improved POM (Inheritance)

Extends `CommonToAllPage` to reuse common actions like `clickElement()`, `enterInput()`, `getText()`. Eliminates repeated `driver.findElement()` calls.

```java
package com.thetestingacademy.pages.pageObjectModel.normal_POM.imporved_POM.vwo;

import com.thetestingacademy.base.CommonToAllPage;
import com.thetestingacademy.utils.WaitHelpers;
import org.openqa.selenium.By;

public class LoginPage extends CommonToAllPage {
    private By username = By.id("login-username");
    private By password = By.id("login-password");
    private By signButton = By.id("js-login-btn");
    private By error_message = By.cssSelector("[data-qa='error-text']");

    public String loginToVWOLoginInvalidCreds(String user, String pwd) {
        openVWOUrl();
        enterInput(username, user);
        enterInput(password, pwd);
        clickElement(signButton);
        WaitHelpers.checkVisibility(getDriver(), error_message);
        return getText(error_message);
    }
}
```

## Page Object Model -- Pattern 3: Page Factory

Uses Selenium's `@FindBy` annotations for declarative element location. Elements are automatically initialized via `PageFactory.initElements()`.

```java
package com.thetestingacademy.pages.pageFactory.vwo;

import com.thetestingacademy.base.CommonToAllPage;
import com.thetestingacademy.utils.PropertiesReader;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class LoginPage_PF extends CommonToAllPage {

    @FindBy(id = "login-username")
    private WebElement username;

    @FindBy(name = "password")
    private WebElement password;

    @FindBy(id = "js-login-btn")
    private WebElement signButton;

    @FindBy(css = "[data-qa='error-text']")
    private WebElement error_message;

    public LoginPage_PF(WebDriver driver) {
        PageFactory.initElements(driver, this);
    }

    public String loginToVWOInvalidCreds() {
        openVWOUrl();
        enterInput(username, PropertiesReader.readKey("invalid_username"));
        enterInput(password, PropertiesReader.readKey("invalid_password"));
        clickElement(signButton);
        return getText(error_message);
    }
}
```

## CommonToAllPage -- Base Page Object

```java
package com.thetestingacademy.base;

import com.thetestingacademy.driver.DriverManager;
import com.thetestingacademy.utils.PropertiesReader;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class CommonToAllPage {

    public WebDriver getDriver() {
        return DriverManager.getDriver();
    }

    public void clickElement(By by) {
        getDriver().findElement(by).click();
    }

    public void clickElement(WebElement element) {
        element.click();
    }

    public void enterInput(By by, String text) {
        getDriver().findElement(by).sendKeys(text);
    }

    public void enterInput(WebElement element, String text) {
        element.sendKeys(text);
    }

    public String getText(By by) {
        return getDriver().findElement(by).getText();
    }

    public String getText(WebElement element) {
        return element.getText();
    }

    public void openVWOUrl() {
        getDriver().get(PropertiesReader.readKey("url"));
    }

    public void openOrangeHRMUrl() {
        getDriver().get(PropertiesReader.readKey("ohr_url"));
    }
}
```

## CommonToAllTest -- Base Test Class

```java
package com.thetestingacademy.base;

import com.thetestingacademy.driver.DriverManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

public class CommonToAllTest {
    protected WebDriver driver;
    protected Logger logger = LogManager.getLogger(this.getClass());

    public WebDriver getDriver() {
        return DriverManager.getDriver();
    }

    @BeforeMethod
    public void setUp() {
        DriverManager.init();
        driver = DriverManager.getDriver();
    }

    @AfterMethod
    public void tearDown() {
        DriverManager.down();
    }
}
```

## Wait Helpers

```java
package com.thetestingacademy.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

public class WaitHelpers {

    // Implicit Wait
    public static void waitImplicitWait(WebDriver driver, int timeInSeconds) {
        driver.manage().timeouts().implicitlyWait(timeInSeconds, TimeUnit.SECONDS);
    }

    // Explicit Wait -- Visibility
    public static void checkVisibility(WebDriver driver, By locator, int timeInSeconds) {
        new WebDriverWait(driver, Duration.ofSeconds(timeInSeconds))
            .until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    // Explicit Wait -- Visibility (default 10s)
    public static void checkVisibility(WebDriver driver, By locator) {
        new WebDriverWait(driver, Duration.ofSeconds(10))
            .until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    // Explicit Wait -- Text Present
    public static void checkVisibilityOfAndTextToBePresentInElement(
            WebDriver driver, By locator, String text, int timeInSeconds) {
        new WebDriverWait(driver, Duration.ofSeconds(timeInSeconds))
            .until(ExpectedConditions.textToBePresentInElementLocated(locator, text));
    }

    // Explicit Wait -- Presence
    public static WebElement presenceOfElement(WebDriver driver, By locator, int timeInSeconds) {
        return new WebDriverWait(driver, Duration.ofSeconds(timeInSeconds))
            .until(ExpectedConditions.presenceOfElementLocated(locator));
    }

    // Fluent Wait
    public static void checkVisibilityByFluentWait(WebDriver driver, By locator) {
        new FluentWait<>(driver)
            .withTimeout(Duration.ofSeconds(30))
            .pollingEvery(Duration.ofMillis(500))
            .ignoring(NoSuchElementException.class)
            .until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    // JVM Sleep (use sparingly)
    public static void waitJVM(int timeInMillis) {
        try {
            Thread.sleep(timeInMillis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## Properties Reader

```java
package com.thetestingacademy.utils;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class PropertiesReader {
    public static String readKey(String key) {
        Properties properties = new Properties();
        try {
            FileInputStream fis = new FileInputStream("src/main/resources/data.properties");
            properties.load(fis);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read properties file", e);
        }
        return properties.getProperty(key);
    }
}
```

## Configuration -- data.properties

```properties
# Application URLs
url=https://app.vwo.com
ohr_url=https://awesomeqa.com/hr/web/index.php/auth/login
katalon_url=https://katalon-demo-cura.herokuapp.com/

# Credentials
username=user@example.com
password=SecurePass123
invalid_username=admin@admin.com
invalid_password=Test@2024
error_message=Your email, password, IP address or location did not match

# Browser
browser=Chrome

# Expected values
expected_username=Test User
```

## Writing Tests -- Basic POM Test

```java
package com.thetestingacademy.tests.pageObjectModelTests.vwo;

import com.thetestingacademy.base.CommonToAllTest;
import com.thetestingacademy.pages.pageObjectModel.normal_POM.normal_POM.vwo.DashBoardPage;
import com.thetestingacademy.pages.pageObjectModel.normal_POM.normal_POM.vwo.LoginPage;
import com.thetestingacademy.utils.PropertiesReader;
import io.qameta.allure.Description;
import io.qameta.allure.Owner;
import org.testng.Assert;
import org.testng.annotations.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class TestVWOLogin_01_NormalScript_POM extends CommonToAllTest {

    @Description("Verify that with invalid email and password, error message is shown")
    @Owner("Promode")
    @Test
    public void test_negative_vwo_login() {
        LoginPage loginPage = new LoginPage(driver);
        String error_msg = loginPage.loginToVWOLoginInvalidCreds(
            PropertiesReader.readKey("invalid_username"),
            PropertiesReader.readKey("invalid_password")
        );

        assertThat(error_msg).isNotNull().isNotBlank().isNotEmpty();
        Assert.assertEquals(error_msg, PropertiesReader.readKey("error_message"));
    }

    @Test
    public void testLoginPositiveVWO() {
        LoginPage loginPage = new LoginPage(driver);
        loginPage.loginToVWOLoginValidCreds(
            PropertiesReader.readKey("username"),
            PropertiesReader.readKey("password")
        );

        DashBoardPage dashBoardPage = new DashBoardPage(driver);
        String usernameLoggedIn = dashBoardPage.loggedInUserName();
        Assert.assertEquals(usernameLoggedIn, PropertiesReader.readKey("expected_username"));
    }
}
```

## Writing Tests -- Page Factory Test

```java
package com.thetestingacademy.tests.pageFactoryTests.vwo;

import com.thetestingacademy.base.CommonToAllTest;
import com.thetestingacademy.pages.pageFactory.vwo.LoginPage_PF;
import com.thetestingacademy.utils.PropertiesReader;
import org.testng.Assert;
import org.testng.annotations.Test;

public class TestVWOLogin_PF extends CommonToAllTest {

    @Test
    public void testLoginNegativeVWO_PF() {
        logger.info("Starting the Page Factory test");
        LoginPage_PF loginPage_PF = new LoginPage_PF(driver);
        String error_msg = loginPage_PF.loginToVWOInvalidCreds();
        logger.info("Error msg: " + error_msg);
        Assert.assertEquals(error_msg, PropertiesReader.readKey("error_message"));
    }
}
```

## Data-Driven Testing with Excel

```java
package com.thetestingacademy.utilexcel;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileInputStream;
import java.io.IOException;

public class UtilExcel {

    public static Object[][] getTestDataFromExcel(String sheetName) {
        Object[][] data = null;
        try {
            FileInputStream fis = new FileInputStream("src/test/resources/TestData.xlsx");
            Workbook workbook = new XSSFWorkbook(fis);
            Sheet sheet = workbook.getSheet(sheetName);

            int rowCount = sheet.getPhysicalNumberOfRows();
            int colCount = sheet.getRow(0).getPhysicalNumberOfCells();

            data = new Object[rowCount - 1][colCount]; // skip header row

            for (int i = 1; i < rowCount; i++) {
                Row row = sheet.getRow(i);
                for (int j = 0; j < colCount; j++) {
                    Cell cell = row.getCell(j);
                    data[i - 1][j] = getCellValue(cell);
                }
            }
            workbook.close();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read Excel file", e);
        }
        return data;
    }

    private static Object getCellValue(Cell cell) {
        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue();
            case NUMERIC:
                return cell.getNumericCellValue();
            case BOOLEAN:
                return cell.getBooleanCellValue();
            default:
                return "";
        }
    }
}
```

### Using Excel Data Provider in Tests

```java
@DataProvider(name = "loginData")
public Object[][] getLoginData() {
    return UtilExcel.getTestDataFromExcel("LoginData");
}

@Test(dataProvider = "loginData")
public void testDataDrivenLogin(String email, String password, String expectedResult) {
    LoginPage loginPage = new LoginPage(driver);
    String result = loginPage.loginToVWOLoginInvalidCreds(email, password);
    Assert.assertEquals(result, expectedResult);
}
```

## Retry Mechanism

### RetryAnalyzer

```java
package com.thetestingacademy.listeners;

import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;

public class RetryAnalyzer implements IRetryAnalyzer {
    private int retryCount = 0;
    private static final int maxRetryCount = 1;

    @Override
    public boolean retry(ITestResult iTestResult) {
        if (retryCount < maxRetryCount) {
            retryCount++;
            return true;
        }
        return false;
    }
}
```

### RetryListener (Global Retry)

```java
package com.thetestingacademy.listeners;

import org.testng.IAnnotationTransformer;
import org.testng.annotations.ITestAnnotation;

import java.lang.reflect.Constructor;
import java.lang.reflect.Method;

public class RetryListener implements IAnnotationTransformer {
    @Override
    public void transform(ITestAnnotation annotation, Class testClass,
                         Constructor testConstructor, Method testMethod) {
        annotation.setRetryAnalyzer(RetryAnalyzer.class);
    }
}
```

## Screenshot Listener with Allure

```java
package com.thetestingacademy.listeners;

import com.thetestingacademy.driver.DriverManager;
import io.qameta.allure.Allure;
import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.ITestListener;
import org.testng.ITestResult;
import org.testng.Reporter;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ScreenshotListener implements ITestListener {

    @Override
    public void onTestFailure(ITestResult result) {
        WebDriver driver = DriverManager.getDriver();
        String methodName = result.getName();
        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());

        if (driver != null) {
            try {
                File scrFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
                String screenshotPath = "failure_screenshots/" + methodName + "_" + timestamp + ".png";
                FileUtils.copyFile(scrFile, new File(screenshotPath));

                Reporter.log("<a href='" + screenshotPath + "'> Screenshot</a>");
                Allure.addAttachment("Screenshot on Failure", "image/png",
                    new java.io.FileInputStream(screenshotPath), "png");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void onTestStart(ITestResult result) {
        System.out.println("Starting test: " + result.getName());
    }

    @Override
    public void onTestSuccess(ITestResult result) {
        System.out.println("Test passed: " + result.getName());
    }
}
```

## TestNG XML Configuration

### Basic Suite

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="VWO Basic Suite">
    <test verbose="2" preserve-order="true" name="BasicPOMTests">
        <classes>
            <class name="com.thetestingacademy.tests.pageObjectModelTests.vwo.TestVWOLogin_01_NormalScript_POM"/>
        </classes>
    </test>
</suite>
```

### Retry Suite with Listeners

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Retry Suite">
    <listeners>
        <listener class-name="com.thetestingacademy.listeners.RetryListener"/>
        <listener class-name="com.thetestingacademy.listeners.ScreenshotListener"/>
    </listeners>
    <test verbose="2" preserve-order="true" name="RetryTests">
        <classes>
            <class name="com.thetestingacademy.tests.pageObjectModelTests.vwo.TestVWOLogin_03_Retry"/>
        </classes>
    </test>
</suite>
```

### Multi-Environment Suite

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="QA Environment Suite" parallel="methods" thread-count="2">
    <parameter name="browser" value="chrome"/>
    <parameter name="environment" value="qa"/>
    <test verbose="2" name="QA Smoke Tests">
        <groups>
            <run>
                <include name="smoke"/>
            </run>
        </groups>
        <classes>
            <class name="com.thetestingacademy.tests.pageObjectModelTests.vwo.TestVWOLogin_01_NormalScript_POM"/>
            <class name="com.thetestingacademy.tests.pageFactoryTests.vwo.TestVWOLogin_PF"/>
        </classes>
    </test>
</suite>
```

## Selenoid Docker Grid Integration

```java
// Remote WebDriver configuration for Selenoid
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

public static void initRemote(String browser) {
    DesiredCapabilities capabilities = new DesiredCapabilities();
    capabilities.setBrowserName(browser);
    capabilities.setVersion("latest");
    capabilities.setCapability("enableVNC", true);
    capabilities.setCapability("enableVideo", true);

    try {
        driver = new RemoteWebDriver(
            new URL("http://localhost:4444/wd/hub"),
            capabilities
        );
    } catch (MalformedURLException e) {
        throw new RuntimeException("Invalid Selenoid hub URL", e);
    }
    driver.manage().window().maximize();
}
```

### Selenoid docker-compose.yml

```yaml
version: '3'
services:
  selenoid:
    image: aerokube/selenoid:latest
    ports:
      - "4444:4444"
    volumes:
      - "./browsers.json:/etc/selenoid/browsers.json"
      - "/var/run/docker.sock:/var/run/docker.sock"
  selenoid-ui:
    image: aerokube/selenoid-ui:latest
    ports:
      - "8080:8080"
    command: ["--selenoid-uri", "http://selenoid:4444"]
```

## Allure Reporting

### Annotations

```java
@Test
@Description("Verify login with invalid credentials shows error")
@Owner("Promode")
@Severity(SeverityLevel.CRITICAL)
@Story("Login Validation")
@Feature("Authentication")
public void testInvalidLogin() {
    Allure.step("Navigate to login page");
    Allure.step("Enter invalid credentials");
    Allure.step("Verify error message");
    // test implementation
}
```

### Generate and Open Report

```bash
# Run tests
mvn clean test -Dsurefire.suiteXmlFiles=testng_vwo_retry.xml

# Generate Allure report
mvn allure:report

# Or use Allure CLI
allure generate target/allure-results --clean -o allure-report
allure open allure-report
```

## Log4j2 Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1} - %m%n"/>
        </Console>
        <File name="FileLogger" fileName="logs/test.log">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1} - %m%n"/>
        </File>
    </Appenders>
    <Loggers>
        <Root level="info">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="FileLogger"/>
        </Root>
    </Loggers>
</Configuration>
```

## Best Practices

1. **Choose the right POM pattern** -- Use Basic POM for small projects, Improved POM for medium projects needing code reuse, and Page Factory for large projects with many elements.
2. **Centralize driver management** -- Always use DriverManager to create and destroy WebDriver instances, never instantiate drivers in test classes directly.
3. **Externalize all test data** -- Use `data.properties` for configuration and `TestData.xlsx` for parameterized test data. Never hardcode URLs, credentials, or expected values.
4. **Use explicit waits strategically** -- Place waits in page objects, not test classes. Prefer `WebDriverWait` with `ExpectedConditions` over implicit waits.
5. **Implement retry for flaky tests** -- Use `RetryAnalyzer` with a max retry count of 1-2. Apply globally via `RetryListener` in TestNG XML.
6. **Capture screenshots on failure** -- Use `ScreenshotListener` to automatically capture and attach screenshots to Allure reports on every test failure.
7. **Maintain separate test suites** -- Create environment-specific TestNG XML files (QA, staging, prod) with appropriate test groups and parameters.
8. **Use AssertJ for fluent assertions** -- Combine TestNG's `Assert.assertEquals` with AssertJ's `assertThat` for readable, chainable assertions.
9. **Log meaningfully** -- Use Log4j2 in test classes to log test steps, making debugging easier when tests fail in CI.
10. **Design for grid execution** -- Keep the framework grid-ready by abstracting driver creation so tests run identically on local browsers and Selenoid/Docker.

## Anti-Patterns to Avoid

1. **`Thread.sleep()` for synchronization** -- Always use explicit waits with conditions. Sleep causes brittle, slow tests.
2. **Hardcoded test data in methods** -- Extract to properties files or Excel. Hardcoded data makes maintenance difficult.
3. **Direct `driver.findElement()` in test classes** -- Always go through page objects. Tests should only call page object methods.
4. **Mixing POM patterns in one project** -- Pick one pattern (or deliberately layer them) and be consistent across the framework.
5. **Not quitting the driver in tearDown** -- Always call `DriverManager.down()` in `@AfterMethod` to prevent zombie browser processes.
6. **Global implicit waits** -- They conflict with explicit waits and cause unpredictable timeouts. Use explicit waits only.
7. **Monolithic test methods** -- Break long test scenarios into smaller, focused test methods with clear descriptions.
8. **Ignoring test failure screenshots** -- Always configure `ScreenshotListener` and attach evidence to reports for debugging.
9. **Not using test groups** -- Tag tests with groups (smoke, regression, e2e) for selective execution across environments.
10. **Running tests only locally** -- Set up Selenoid or a cloud grid early. Tests that only run locally miss cross-browser issues.
