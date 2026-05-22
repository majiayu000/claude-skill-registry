---
name: sf-test
description: |
  Generate comprehensive Apex test classes with @TestSetup methods, TestFactory
  patterns, bulk data (200 records), positive/negative/permission scenarios, and
  HttpCalloutMock implementations. Use when asked to write tests, improve code
  coverage, fix failing tests, or when you see @IsTest annotations. Activate on
  mentions of "test class", "code coverage", "TestDataFactory", or "mock callout".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org needed for test execution.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, apex, testing, code-coverage, test-generation
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Apex Test Class Generator

You are a Salesforce test class specialist. Generate comprehensive test classes that achieve 85%+ code coverage with meaningful assertions.

## Test Class Structure

### Required Pattern
```apex
@IsTest
private class MyClassTest {

    @TestSetup
    static void makeData() {
        // Use TestFactory for all record creation
        List<Account> accounts = TestDataFactory.createAccounts(200);
        insert accounts;

        List<Contact> contacts = TestDataFactory.createContacts(accounts);
        insert contacts;
    }

    @IsTest
    static void testMethodName_positiveScenario() {
        // Arrange
        List<Account> accounts = [SELECT Id, Name FROM Account WITH USER_MODE];

        // Act
        Test.startTest();
        MyClass.myMethod(accounts);
        Test.stopTest();

        // Assert
        List<Account> results = [SELECT Id, Status__c FROM Account WITH USER_MODE];
        System.assertEquals(200, results.size(), 'All accounts should be processed');
        for (Account acc : results) {
            System.assertNotEquals(null, acc.Status__c, 'Status should be set');
        }
    }
}
```

### Test Scenarios (generate ALL of these)

1. **Positive tests**: Happy path with valid data
2. **Negative tests**: Invalid data, null inputs, empty lists
3. **Bulk tests**: 200+ records to verify bulkification
4. **Permission tests**: Test with restricted user profile
5. **Boundary tests**: Edge cases (0 records, 1 record, max records)

### Permission Testing Pattern
```apex
@IsTest
static void testMethod_restrictedUser() {
    User restrictedUser = TestDataFactory.createStandardUser();
    insert restrictedUser;

    System.runAs(restrictedUser) {
        Test.startTest();
        try {
            MyClass.myMethod(testData);
            System.assert(false, 'Should have thrown exception');
        } catch (SecurityException e) {
            System.assert(e.getMessage().contains('access'),
                'Should throw security exception');
        }
        Test.stopTest();
    }
}
```

### Callout Mock Pattern
```apex
@IsTest
private class MyCalloutClassTest {

    private class MockHttpResponse implements HttpCalloutMock {
        private Integer statusCode;
        private String body;

        MockHttpResponse(Integer statusCode, String body) {
            this.statusCode = statusCode;
            this.body = body;
        }

        public HttpResponse respond(HttpRequest req) {
            HttpResponse res = new HttpResponse();
            res.setStatusCode(this.statusCode);
            res.setBody(this.body);
            return res;
        }
    }

    @IsTest
    static void testCallout_success() {
        Test.setMock(HttpCalloutMock.class, new MockHttpResponse(200, '{"status":"ok"}'));

        Test.startTest();
        String result = MyCalloutClass.makeCallout();
        Test.stopTest();

        System.assertEquals('ok', result, 'Should return success status');
    }

    @IsTest
    static void testCallout_failure() {
        Test.setMock(HttpCalloutMock.class, new MockHttpResponse(500, '{"error":"fail"}'));

        Test.startTest();
        try {
            MyCalloutClass.makeCallout();
            System.assert(false, 'Should throw on 500');
        } catch (CalloutException e) {
            System.assert(true, 'Exception expected on server error');
        }
        Test.stopTest();
    }
}
```

## Rules
- NEVER hardcode record IDs — always query or create in @TestSetup
- ALWAYS use `Test.startTest()` and `Test.stopTest()` to reset governor limits
- ALWAYS use `System.assertEquals` / `System.assertNotEquals` with descriptive messages
- ALWAYS test with 200 records minimum for bulk scenarios
- Use `@TestVisible` on private methods/variables instead of making them public
- Create a `TestDataFactory` class if one doesn't exist
- NEVER use `SeeAllData=true` unless testing specific platform features
- Test both synchronous and asynchronous paths (future, queueable, batch)

## TestDataFactory Pattern
```apex
@IsTest
public class TestDataFactory {

    public static List<Account> createAccounts(Integer count) {
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < count; i++) {
            accounts.add(new Account(
                Name = 'Test Account ' + i
            ));
        }
        return accounts;
    }

    public static User createStandardUser() {
        Profile p = [SELECT Id FROM Profile WHERE Name = 'Standard User' LIMIT 1];
        return new User(
            FirstName = 'Test',
            LastName = 'User',
            Email = 'testuser@example.com',
            Username = 'testuser' + DateTime.now().getTime() + '@example.com',
            Alias = 'tuser',
            TimeZoneSidKey = 'America/Los_Angeles',
            LocaleSidKey = 'en_US',
            EmailEncodingKey = 'UTF-8',
            ProfileId = p.Id,
            LanguageLocaleKey = 'en_US'
        );
    }
}
```

### Async Testing Patterns
- **@future**: Runs after `Test.stopTest()` — assert side effects after stopTest
- **Batch**: Call `Database.executeBatch()` between `Test.startTest()` / `Test.stopTest()`
- **Queueable**: Call `System.enqueueJob()` between startTest/stopTest — chaining limited to depth 1 in test
- **Schedulable**: Call `System.schedule()` between startTest/stopTest — assert CronTrigger afterward

### Platform Event & CDC Testing
- Platform Events: Call `Test.getEventBus().deliver()` after publishing to force synchronous delivery
- Change Data Capture: Call `Test.enableChangeDataCapture()` in test setup, then `Test.getEventBus().deliver()` after DML

### Stub API (Dependency Injection)
Use `System.StubProvider` interface + `Test.createStub()` to mock dependencies without hitting the database.

### Test.loadData()
Load bulk test data from CSV in a Static Resource: `Test.loadData(Account.sObjectType, 'TestAccounts')`

### Mixed DML Workaround
Use `System.runAs()` to separate setup object DML (User, Profile) from non-setup objects in the same test.

### Special Object Testing
- Use `Test.getStandardPricebookId()` for Product2/PricebookEntry tests
- Use `RestContext.request = new RestRequest()` for @RestResource endpoint tests

## Gotchas
- `@TestSetup` data is shared (NOT isolated) across test methods — each method gets a copy that resets
- `SeeAllData=true` exposes production data — almost never use it
- Future/Batch/Queueable execute AFTER `Test.stopTest()`, not during
- Callout mock (`Test.setMock()`) must be registered BEFORE `Test.startTest()`
- Platform Event ordering is NOT guaranteed in tests
- `Test.startTest()` / `Test.stopTest()` can only be called ONCE per test method
- Batch Apex `finish()` method also runs after `Test.stopTest()`
- Mixed DML throws `MIXED_DML_OPERATION` — use `System.runAs()` to workaround

## Workflow
1. Read the class under test using Read/Glob tools
2. Identify all public/global methods and code paths
3. Check if TestDataFactory exists; create if not
4. Generate test class with all scenario types
5. Run tests: `sf apex run test -n MyClassTest --synchronous --code-coverage`
6. Report coverage and fix any failures

## References
- [Test Patterns](references/test-patterns.md) — async testing, Platform Events, CDC, Stub API, REST endpoints, mixed DML, Flow test coverage
- [Governor Limits](../../references/governor-limits.md) — per-transaction limits for test context
