---
name: REST Assured API Automation Framework
description: Production-grade REST API automation framework with REST Assured, POJO serialization using GSON, PayloadManager pattern, E2E integration workflows with TestNG ITestContext, and Allure reporting.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [rest-assured, api-testing, java, gson, pojo, e2e-integration, allure, testng, data-driven, payload-manager]
testingTypes: [api, integration]
frameworks: [rest-assured]
languages: [java]
domains: [api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# REST Assured API Automation Framework Skill

You are an expert QA automation engineer specializing in REST API automation with Java using REST Assured. When the user asks you to build, review, or debug an API test automation framework, follow these detailed instructions covering POJO-based request/response handling, PayloadManager pattern, E2E integration workflows, and advanced reporting.

## Core Principles

1. **PayloadManager pattern** -- Centralize all request payload creation and response deserialization in a dedicated PayloadManager class using GSON.
2. **POJO-driven requests and responses** -- Use Java objects with `@SerializedName` and `@Expose` annotations for type-safe JSON handling.
3. **RequestSpecBuilder for DRY setup** -- Configure base URI, headers, and content type once in BaseTest, reuse across all tests.
4. **Custom assertion helpers** -- Wrap common assertions in an AssertActions class using AssertJ for fluent, readable validations.
5. **E2E integration with ITestContext** -- Share state (booking IDs, tokens) across test methods using TestNG's ITestContext for multi-step workflows.
6. **Centralized API constants** -- Store all endpoint paths in a single APIConstants class, never hardcode URLs in tests.
7. **Multiple data strategies** -- Support static payloads, JavaFaker random data, and edge-case payloads for comprehensive coverage.
8. **Allure metadata on every test** -- Annotate with @Description, @Owner, @TmsLink for full traceability in reports.

## Project Structure

```
src/
  main/java/com/thetestingacademy/
    endpoints/
      APIConstants.java               # Base URL and endpoint paths
    modules/
      PayloadManager.java             # Payload creation and response parsing
    pojos/
      request/
        Auth.java                     # Authentication POJO
        Booking.java                  # Booking request POJO
        Bookingdates.java             # Nested dates POJO
      reponse/
        BookingResponse.java          # Booking response POJO
        TokenResponse.java            # Token response POJO
  test/java/com/thetestingacademy/
    base/
      BaseTest.java                   # Setup, teardown, token helper
    asserts/
      AssertActions.java              # Custom assertion methods
    tests/
      crud/
        TestHealthCheck.java          # API health check
        TestCreateToken.java          # Token creation test
        TestCreateBooking.java        # CRUD booking tests
      e2e_integration/
        TestIntegrationFlow1.java     # Full E2E workflow (Create→Read→Update→Delete)
        TestIntegrationFlow2.java     # Alternate integration flow
      sample/
        TestIntegrationSample.java    # Test template
    resources/
      data.properties                 # Configuration
testng.xml                            # Default test suite
testng_e2e.xml                        # E2E integration suite
pom.xml
```

## Maven Dependencies

```xml
<dependencies>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <version>5.5.1</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>json-schema-validator</artifactId>
        <version>5.4.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testng</groupId>
        <artifactId>testng</artifactId>
        <version>7.10.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.qameta.allure</groupId>
        <artifactId>allure-testng</artifactId>
        <version>2.27.0</version>
    </dependency>
    <dependency>
        <groupId>com.google.code.gson</groupId>
        <artifactId>gson</artifactId>
        <version>2.11.0</version>
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
        <version>5.2.3</version>
    </dependency>
    <dependency>
        <groupId>com.github.javafaker</groupId>
        <artifactId>javafaker</artifactId>
        <version>1.0.2</version>
    </dependency>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <version>2.24.0</version>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.1.2</version>
            <configuration>
                <suiteXmlFiles>
                    <suiteXmlFile>testng.xml</suiteXmlFile>
                </suiteXmlFiles>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## API Constants

```java
package com.thetestingacademy.endpoints;

public class APIConstants {
    public static String BASE_URL = "https://restful-booker.herokuapp.com";
    public static String CREATE_UPDATE_BOOKING_URL = "/booking";
    public static String AUTH_URL = "/auth";
    public static String PING_URL = "/ping";
}
```

## POJO Models -- Request

### Auth.java

```java
package com.thetestingacademy.pojos.request;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Auth {
    @SerializedName("username")
    @Expose
    private String username;

    @SerializedName("password")
    @Expose
    private String password;

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}
```

### Booking.java

```java
package com.thetestingacademy.pojos.request;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Booking {
    @SerializedName("firstname")
    @Expose
    private String firstname;

    @SerializedName("lastname")
    @Expose
    private String lastname;

    @SerializedName("totalprice")
    @Expose
    private Integer totalprice;

    @SerializedName("depositpaid")
    @Expose
    private Boolean depositpaid;

    @SerializedName("bookingdates")
    @Expose
    private Bookingdates bookingdates;

    @SerializedName("additionalneeds")
    @Expose
    private String additionalneeds;

    // Getters and Setters
    public String getFirstname() { return firstname; }
    public void setFirstname(String firstname) { this.firstname = firstname; }
    public String getLastname() { return lastname; }
    public void setLastname(String lastname) { this.lastname = lastname; }
    public Integer getTotalprice() { return totalprice; }
    public void setTotalprice(Integer totalprice) { this.totalprice = totalprice; }
    public Boolean getDepositpaid() { return depositpaid; }
    public void setDepositpaid(Boolean depositpaid) { this.depositpaid = depositpaid; }
    public Bookingdates getBookingdates() { return bookingdates; }
    public void setBookingdates(Bookingdates bookingdates) { this.bookingdates = bookingdates; }
    public String getAdditionalneeds() { return additionalneeds; }
    public void setAdditionalneeds(String additionalneeds) { this.additionalneeds = additionalneeds; }
}
```

### Bookingdates.java

```java
package com.thetestingacademy.pojos.request;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Bookingdates {
    @SerializedName("checkin")
    @Expose
    private String checkin;

    @SerializedName("checkout")
    @Expose
    private String checkout;

    public String getCheckin() { return checkin; }
    public void setCheckin(String checkin) { this.checkin = checkin; }
    public String getCheckout() { return checkout; }
    public void setCheckout(String checkout) { this.checkout = checkout; }
}
```

## POJO Models -- Response

### TokenResponse.java

```java
package com.thetestingacademy.pojos.reponse;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class TokenResponse {
    @SerializedName("token")
    @Expose
    private String token;

    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }
}
```

### BookingResponse.java

```java
package com.thetestingacademy.pojos.reponse;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import com.thetestingacademy.pojos.request.Booking;

public class BookingResponse {
    @SerializedName("bookingid")
    @Expose
    private Integer bookingid;

    @SerializedName("booking")
    @Expose
    private Booking booking;

    public Integer getBookingid() { return bookingid; }
    public void setBookingid(Integer bookingid) { this.bookingid = bookingid; }
    public Booking getBooking() { return booking; }
    public void setBooking(Booking booking) { this.booking = booking; }
}
```

## PayloadManager Pattern

The PayloadManager centralizes all payload creation, serialization, and deserialization. This keeps test classes clean and focused on assertions.

```java
package com.thetestingacademy.modules;

import com.github.javafaker.Faker;
import com.google.gson.Gson;
import com.thetestingacademy.pojos.reponse.BookingResponse;
import com.thetestingacademy.pojos.reponse.TokenResponse;
import com.thetestingacademy.pojos.request.Auth;
import com.thetestingacademy.pojos.request.Booking;
import com.thetestingacademy.pojos.request.Bookingdates;

public class PayloadManager {
    Gson gson;
    Faker faker;

    // --- Serialization: Java Object → JSON String ---

    public String createPayloadBookingAsString() {
        Booking booking = new Booking();
        booking.setFirstname("Pramod");
        booking.setLastname("Dutta");
        booking.setTotalprice(112);
        booking.setDepositpaid(true);

        Bookingdates bookingdates = new Bookingdates();
        bookingdates.setCheckin("2024-02-01");
        bookingdates.setCheckout("2024-02-10");
        booking.setBookingdates(bookingdates);
        booking.setAdditionalneeds("Breakfast");

        gson = new Gson();
        return gson.toJson(booking);
    }

    // Payload with random data using JavaFaker
    public String createPayloadBookingFakerJS() {
        faker = new Faker();
        Booking booking = new Booking();
        booking.setFirstname(faker.name().firstName());
        booking.setLastname(faker.name().lastName());
        booking.setTotalprice(faker.random().nextInt(1, 1000));
        booking.setDepositpaid(faker.random().nextBoolean());

        Bookingdates bookingdates = new Bookingdates();
        bookingdates.setCheckin("2024-02-01");
        bookingdates.setCheckout("2024-02-10");
        booking.setBookingdates(bookingdates);
        booking.setAdditionalneeds("Lunch");

        gson = new Gson();
        return gson.toJson(booking);
    }

    // Edge case payload with non-ASCII characters
    public String createPayloadBookingAsStringWrongBody() {
        Booking booking = new Booking();
        booking.setFirstname("会意; 會意");
        booking.setLastname("Test");
        booking.setTotalprice(112);
        booking.setDepositpaid(true);

        Bookingdates bookingdates = new Bookingdates();
        bookingdates.setCheckin("5025-02-01");
        bookingdates.setCheckout("5025-02-10");
        booking.setBookingdates(bookingdates);
        booking.setAdditionalneeds("Breakfast");

        gson = new Gson();
        return gson.toJson(booking);
    }

    // Full update payload
    public String fullUpdatePayloadAsString() {
        Booking booking = new Booking();
        booking.setFirstname("UpdatedFirstName");
        booking.setLastname("UpdatedLastName");
        booking.setTotalprice(500);
        booking.setDepositpaid(false);

        Bookingdates bookingdates = new Bookingdates();
        bookingdates.setCheckin("2024-03-01");
        bookingdates.setCheckout("2024-03-15");
        booking.setBookingdates(bookingdates);
        booking.setAdditionalneeds("Dinner");

        gson = new Gson();
        return gson.toJson(booking);
    }

    // Auth payload
    public String setAuthPayload() {
        Auth auth = new Auth();
        auth.setUsername("admin");
        auth.setPassword("password123");
        gson = new Gson();
        return gson.toJson(auth);
    }

    // --- Deserialization: JSON String → Java Object ---

    public BookingResponse bookingResponseJava(String responseString) {
        gson = new Gson();
        return gson.fromJson(responseString, BookingResponse.class);
    }

    public String getTokenFromJSON(String tokenResponse) {
        gson = new Gson();
        TokenResponse response = gson.fromJson(tokenResponse, TokenResponse.class);
        return response.getToken();
    }
}
```

## Base Test Class

```java
package com.thetestingacademy.base;

import com.thetestingacademy.asserts.AssertActions;
import com.thetestingacademy.endpoints.APIConstants;
import com.thetestingacademy.modules.PayloadManager;
import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.http.ContentType;
import io.restassured.path.json.JsonPath;
import io.restassured.response.Response;
import io.restassured.response.ValidatableResponse;
import io.restassured.specification.RequestSpecification;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.AfterTest;

public class BaseTest {
    public RequestSpecification requestSpecification;
    public AssertActions assertActions;
    public PayloadManager payloadManager;
    public JsonPath jsonPath;
    public Response response;
    public ValidatableResponse validatableResponse;

    @BeforeTest
    public void setUp() {
        payloadManager = new PayloadManager();
        assertActions = new AssertActions();

        requestSpecification = new RequestSpecBuilder()
            .setBaseUri(APIConstants.BASE_URL)
            .addHeader("Content-Type", "application/json")
            .build().log().all();
    }

    public String getToken() {
        requestSpecification = RestAssured.given();
        requestSpecification.baseUri(APIConstants.BASE_URL)
            .basePath(APIConstants.AUTH_URL);

        String payload = payloadManager.setAuthPayload();
        response = requestSpecification.contentType(ContentType.JSON)
            .body(payload).when().post();

        return payloadManager.getTokenFromJSON(response.asString());
    }

    @AfterTest
    public void tearDown() {
        System.out.println("Finished the Test!");
    }
}
```

## Custom Assertion Helpers

```java
package com.thetestingacademy.asserts;

import io.restassured.response.Response;

import static org.assertj.core.api.Assertions.assertThat;
import static org.testng.Assert.assertEquals;

public class AssertActions {

    public void verifyResponseBody(String actual, String expected, String description) {
        assertEquals(actual, expected, description);
    }

    public void verifyResponseBody(int actual, int expected, String description) {
        assertEquals(actual, expected, description);
    }

    public void verifyStatusCode(Response response, Integer expected) {
        assertEquals(response.getStatusCode(), (int) expected);
    }

    public void verifyStringKey(String keyExpect, String keyActual) {
        assertThat(keyExpect).isNotNull();
        assertThat(keyExpect).isNotBlank();
        assertThat(keyExpect).isEqualTo(keyActual);
    }

    public void verifyStringKeyNotNull(Integer keyExpect) {
        assertThat(keyExpect).isNotNull();
    }

    public void verifyStringKeyNotNull(String keyExpect) {
        assertThat(keyExpect).isNotNull();
    }

    public void verifyResponseTime(Response response, long maxMillis) {
        assertThat(response.getTime()).isLessThan(maxMillis);
    }

    public void verifyContentType(Response response, String expectedContentType) {
        assertThat(response.getContentType()).contains(expectedContentType);
    }
}
```

## CRUD Test Patterns

### Health Check

```java
package com.thetestingacademy.tests.crud;

import com.thetestingacademy.base.BaseTest;
import com.thetestingacademy.endpoints.APIConstants;
import io.restassured.RestAssured;
import org.testng.annotations.Test;

public class TestHealthCheck extends BaseTest {

    @Test(groups = "reg", priority = 1)
    public void testHealthCheckGET() {
        requestSpecification.basePath(APIConstants.PING_URL);
        response = RestAssured.given(requestSpecification)
            .when()
            .get();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(201);
    }
}
```

### Token Creation

```java
package com.thetestingacademy.tests.crud;

import com.thetestingacademy.base.BaseTest;
import com.thetestingacademy.endpoints.APIConstants;
import io.qameta.allure.Description;
import io.qameta.allure.Owner;
import io.restassured.RestAssured;
import org.testng.annotations.Test;

public class TestCreateToken extends BaseTest {

    @Test(groups = "reg", priority = 1)
    @Owner("Promode")
    @Description("TC#2 - Create Token and Verify")
    public void testTokenPOST() {
        requestSpecification.basePath(APIConstants.AUTH_URL);
        response = RestAssured.given(requestSpecification)
            .when()
            .body(payloadManager.setAuthPayload())
            .post();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);

        String token = payloadManager.getTokenFromJSON(response.asString());
        assertActions.verifyStringKeyNotNull(token);
    }
}
```

### Booking CRUD -- Positive and Negative

```java
package com.thetestingacademy.tests.crud;

import com.thetestingacademy.base.BaseTest;
import com.thetestingacademy.endpoints.APIConstants;
import com.thetestingacademy.pojos.reponse.BookingResponse;
import io.qameta.allure.Description;
import io.qameta.allure.Owner;
import io.restassured.RestAssured;
import org.testng.annotations.Test;

public class TestCreateBooking extends BaseTest {

    @Test(groups = "reg", priority = 1)
    @Owner("Promode")
    @Description("TC#1 - Verify that the Booking can be Created")
    public void testCreateBookingPOST_Positive() {
        requestSpecification.basePath(APIConstants.CREATE_UPDATE_BOOKING_URL);
        response = RestAssured.given(requestSpecification)
            .when()
            .body(payloadManager.createPayloadBookingAsString())
            .log().all()
            .post();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);

        BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());

        assertActions.verifyStringKeyNotNull(bookingResponse.getBookingid());
        assertActions.verifyStringKey(bookingResponse.getBooking().getFirstname(), "Pramod");
    }

    @Test(groups = "reg", priority = 2)
    @Description("TC#2 - Verify booking with empty payload returns error")
    public void testCreateBookingPOST_Negative_EmptyBody() {
        requestSpecification.basePath(APIConstants.CREATE_UPDATE_BOOKING_URL);
        response = RestAssured.given(requestSpecification)
            .when()
            .body("")
            .post();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(500);
    }

    @Test(groups = "reg", priority = 3)
    @Description("TC#3 - Verify booking with non-ASCII characters")
    public void testCreateBookingPOST_EdgeCase_NonASCII() {
        requestSpecification.basePath(APIConstants.CREATE_UPDATE_BOOKING_URL);
        response = RestAssured.given(requestSpecification)
            .when()
            .body(payloadManager.createPayloadBookingAsStringWrongBody())
            .post();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);

        BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());
        assertActions.verifyStringKeyNotNull(bookingResponse.getBookingid());
    }

    @Test(groups = "qa", priority = 4)
    @Description("TC#4 - Verify booking with random Faker data")
    public void testCreateBookingPOST_FakerData() {
        requestSpecification.basePath(APIConstants.CREATE_UPDATE_BOOKING_URL);
        response = RestAssured.given(requestSpecification)
            .when()
            .body(payloadManager.createPayloadBookingFakerJS())
            .post();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);

        BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());
        assertActions.verifyStringKeyNotNull(bookingResponse.getBookingid());
        assertActions.verifyStringKeyNotNull(bookingResponse.getBooking().getFirstname());
    }
}
```

## E2E Integration Flow with ITestContext

This pattern demonstrates a complete CRUD workflow where test methods share state via TestNG's `ITestContext`. Each step depends on the previous one.

```java
package com.thetestingacademy.tests.e2e_integration;

import com.thetestingacademy.base.BaseTest;
import com.thetestingacademy.endpoints.APIConstants;
import com.thetestingacademy.pojos.reponse.BookingResponse;
import io.restassured.RestAssured;
import org.testng.ITestContext;
import org.testng.annotations.Test;

public class TestIntegrationFlow1 extends BaseTest {

    // Step 1: Create a booking
    @Test(priority = 1)
    public void testCreateBooking(ITestContext iTestContext) {
        requestSpecification.basePath(APIConstants.CREATE_UPDATE_BOOKING_URL);
        response = RestAssured.given(requestSpecification)
            .when()
            .body(payloadManager.createPayloadBookingAsString())
            .post();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);

        BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());

        // Store booking ID for subsequent steps
        iTestContext.setAttribute("bookingid", bookingResponse.getBookingid());

        assertActions.verifyStringKeyNotNull(bookingResponse.getBookingid());
    }

    // Step 2: Verify the booking exists
    @Test(priority = 2)
    public void testVerifyBookingId(ITestContext iTestContext) {
        Integer bookingid = (Integer) iTestContext.getAttribute("bookingid");

        String basePathGET = APIConstants.CREATE_UPDATE_BOOKING_URL + "/" + bookingid;
        requestSpecification.basePath(basePathGET);

        response = RestAssured.given(requestSpecification)
            .when()
            .get();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);

        // Verify the returned booking matches what we created
        BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());
        assertActions.verifyStringKey(bookingResponse.getBooking().getFirstname(), "Pramod");
    }

    // Step 3: Update the booking (requires auth token)
    @Test(priority = 3)
    public void testUpdateBookingByID(ITestContext iTestContext) {
        Integer bookingid = (Integer) iTestContext.getAttribute("bookingid");
        String token = getToken();

        // Store token for the delete step
        iTestContext.setAttribute("token", token);

        String basePathPUT = APIConstants.CREATE_UPDATE_BOOKING_URL + "/" + bookingid;
        requestSpecification.basePath(basePathPUT);

        response = RestAssured.given(requestSpecification)
            .cookie("token", token)
            .when()
            .body(payloadManager.fullUpdatePayloadAsString())
            .put();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);
    }

    // Step 4: Verify the update
    @Test(priority = 4)
    public void testVerifyUpdatedBooking(ITestContext iTestContext) {
        Integer bookingid = (Integer) iTestContext.getAttribute("bookingid");

        String basePathGET = APIConstants.CREATE_UPDATE_BOOKING_URL + "/" + bookingid;
        requestSpecification.basePath(basePathGET);

        response = RestAssured.given(requestSpecification)
            .when()
            .get();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(200);

        BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());
        assertActions.verifyStringKey(bookingResponse.getBooking().getFirstname(), "UpdatedFirstName");
    }

    // Step 5: Delete the booking
    @Test(priority = 5)
    public void testDeleteBookingById(ITestContext iTestContext) {
        Integer bookingid = (Integer) iTestContext.getAttribute("bookingid");
        String token = (String) iTestContext.getAttribute("token");

        String basePathDELETE = APIConstants.CREATE_UPDATE_BOOKING_URL + "/" + bookingid;
        requestSpecification.basePath(basePathDELETE);

        response = RestAssured.given().spec(requestSpecification)
            .cookie("token", token)
            .when()
            .delete();

        validatableResponse = response.then().log().all();
        validatableResponse.statusCode(201);
    }
}
```

## Authentication Handling

```java
// Token-based authentication flow:

// 1. Generate token via /auth endpoint
public String getToken() {
    requestSpecification = RestAssured.given();
    requestSpecification.baseUri(APIConstants.BASE_URL)
        .basePath(APIConstants.AUTH_URL);

    String payload = payloadManager.setAuthPayload();
    response = requestSpecification.contentType(ContentType.JSON)
        .body(payload).when().post();

    return payloadManager.getTokenFromJSON(response.asString());
}

// 2. Use token as cookie in protected requests
String token = getToken();
response = RestAssured.given(requestSpecification)
    .cookie("token", token)
    .when()
    .body(payloadManager.fullUpdatePayloadAsString())
    .put();

// 3. Bearer token alternative
response = RestAssured.given(requestSpecification)
    .header("Authorization", "Bearer " + token)
    .when()
    .get();
```

## TestNG XML Configuration

### Default Suite

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="API Test Suite">
    <test verbose="2" preserve-order="true" name="CRUD Tests">
        <classes>
            <class name="com.thetestingacademy.tests.crud.TestHealthCheck"/>
            <class name="com.thetestingacademy.tests.crud.TestCreateToken"/>
            <class name="com.thetestingacademy.tests.crud.TestCreateBooking"/>
        </classes>
    </test>
</suite>
```

### E2E Integration Suite

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="E2E Integration Suite">
    <test verbose="2" preserve-order="true" name="Integration Flow 1">
        <classes>
            <class name="com.thetestingacademy.tests.e2e_integration.TestIntegrationFlow1"/>
        </classes>
    </test>
</suite>
```

### Parallel Execution Suite

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Parallel API Suite" parallel="methods" thread-count="3">
    <test verbose="2" name="Regression">
        <groups>
            <run>
                <include name="reg"/>
            </run>
        </groups>
        <classes>
            <class name="com.thetestingacademy.tests.crud.TestHealthCheck"/>
            <class name="com.thetestingacademy.tests.crud.TestCreateToken"/>
            <class name="com.thetestingacademy.tests.crud.TestCreateBooking"/>
        </classes>
    </test>
</suite>
```

## Allure Reporting

### Annotations

```java
import io.qameta.allure.*;

@Test(groups = "reg", priority = 1)
@TmsLink("https://bugz.atlassian.net/browse/TS-1")
@Owner("Promode")
@Description("TC#1 - Verify that the Booking can be Created")
@Severity(SeverityLevel.CRITICAL)
@Story("Booking CRUD")
@Feature("Booking API")
public void testCreateBookingPOST() {
    Allure.step("Set base path to booking endpoint");
    requestSpecification.basePath(APIConstants.CREATE_UPDATE_BOOKING_URL);

    Allure.step("Send POST request with booking payload");
    response = RestAssured.given(requestSpecification)
        .when()
        .body(payloadManager.createPayloadBookingAsString())
        .post();

    Allure.step("Verify response status code is 200");
    validatableResponse = response.then().statusCode(200);

    Allure.step("Verify booking ID is not null");
    BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());
    assertActions.verifyStringKeyNotNull(bookingResponse.getBookingid());

    Allure.addAttachment("Response Body", "application/json", response.asString(), "json");
}
```

### Generate and Open Report

```bash
# Run tests with specific suite
mvn clean test -DsuiteXmlFile=testng_e2e.xml

# Generate Allure report
allure generate target/allure-results --clean -o allure-report
allure open allure-report
```

## Response Extraction Patterns

```java
// Extract single value with JsonPath
String firstname = response.jsonPath().getString("booking.firstname");
Integer bookingId = response.jsonPath().getInt("bookingid");
List<Integer> allIds = response.jsonPath().getList(".", Integer.class);

// Extract as POJO with GSON
BookingResponse bookingResponse = payloadManager.bookingResponseJava(response.asString());

// Extract with ValidatableResponse
validatableResponse = response.then()
    .body("booking.firstname", equalTo("Pramod"))
    .body("booking.totalprice", greaterThan(0))
    .body("bookingid", notNullValue());

// Chain extraction
String token = response.then()
    .statusCode(200)
    .extract()
    .path("token");
```

## JSON Schema Validation

```java
import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;

@Test
public void testBookingResponseMatchesSchema() {
    response = RestAssured.given(requestSpecification)
        .basePath(APIConstants.CREATE_UPDATE_BOOKING_URL)
        .when()
        .body(payloadManager.createPayloadBookingAsString())
        .post();

    response.then()
        .statusCode(200)
        .body(matchesJsonSchemaInClasspath("schemas/booking-response-schema.json"));
}
```

### booking-response-schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["bookingid", "booking"],
  "properties": {
    "bookingid": { "type": "integer" },
    "booking": {
      "type": "object",
      "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
      "properties": {
        "firstname": { "type": "string" },
        "lastname": { "type": "string" },
        "totalprice": { "type": "integer" },
        "depositpaid": { "type": "boolean" },
        "bookingdates": {
          "type": "object",
          "required": ["checkin", "checkout"],
          "properties": {
            "checkin": { "type": "string" },
            "checkout": { "type": "string" }
          }
        },
        "additionalneeds": { "type": "string" }
      }
    }
  }
}
```

## Best Practices

1. **Use PayloadManager for all payloads** -- Never create JSON strings inline in tests. Centralize all payload logic in PayloadManager for maintainability.
2. **Separate request and response POJOs** -- Keep request models separate from response models. Response models may have extra fields (IDs, timestamps).
3. **Store state in ITestContext** -- For E2E integration flows, use `iTestContext.setAttribute()` to share booking IDs and tokens across test methods.
4. **Use test groups and priorities** -- Tag tests with groups (`reg`, `qa`, `smoke`) and set priorities for ordered execution in integration flows.
5. **Validate more than status codes** -- Always assert response body fields, not just HTTP status. Use AssertActions for consistent validation.
6. **Test edge cases explicitly** -- Include tests for empty payloads, non-ASCII characters, invalid dates, and boundary values.
7. **Generate random test data** -- Use JavaFaker for non-deterministic test data to catch unexpected failures with varied inputs.
8. **Log all requests and responses** -- Use `.log().all()` on both request and response for easy debugging when tests fail.
9. **Keep API constants centralized** -- Store all endpoint paths in APIConstants. Update once when API paths change.
10. **Use Allure annotations consistently** -- Add @Description, @Owner, @TmsLink on every test method for full traceability in reports.

## Anti-Patterns to Avoid

1. **Hardcoded base URLs in tests** -- Always use APIConstants. Hardcoded URLs break when environments change.
2. **String concatenation for JSON** -- Never build JSON manually with string concatenation. Use POJOs with GSON serialization.
3. **Shared mutable state between tests** -- Use ITestContext for state sharing, not static fields. Static state breaks parallel execution.
4. **Missing assertions** -- A test that only calls an endpoint without assertions is not a test. Always verify response body.
5. **Token generation in every test** -- Generate tokens once in setup or share via ITestContext. Avoid redundant auth calls.
6. **Ignoring response time** -- Add response time assertions for performance-critical endpoints using `assertActions.verifyResponseTime()`.
7. **No schema validation** -- Use JSON Schema validation to catch breaking contract changes before they reach production.
8. **Testing only happy paths** -- Always include negative tests (empty body, invalid auth, wrong content type, non-existent resources).
9. **Monolithic test classes** -- Separate tests by feature area (CRUD, auth, integration) into dedicated test classes.
10. **Not using test suites** -- Always configure TestNG XML suites for different scenarios (smoke, regression, e2e) instead of running all tests every time.
