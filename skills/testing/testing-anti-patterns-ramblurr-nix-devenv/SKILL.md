---
name: Testing-Anti-Patterns
description: Use when writing or changing tests, adding mocks, or tempted to add test-only methods to production code - prevents testing mock behavior, production pollution with test-only methods, and mocking without understanding dependencies
---

# Testing Anti-Patterns

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle:** Test what the code does, not what the mocks do.

**Following strict TDD prevents these anti-patterns.**

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only functions to production namespaces
3. NEVER mock without understanding dependencies
```

## Anti-Pattern 1: Testing Mock Behavior

**The violation:**

```clojure
;; BAD: Testing that the mock was called, not that the behavior is correct
(deftest processes-order-test
  (with-redefs [db/save-order (fn [_] nil)]
    (process-order {:id 1 :items ["a"]})
    ;; Only verifies mock was called - tells us nothing about real behavior
    (is (= 1 @call-count))))
```

**Why this is wrong:**

- You're verifying the mock works, not that the function works
- Test passes when mock is present, fails when it's not
- Tells you nothing about real behavior

**Your human partner's correction:** "Are we testing the behavior of a mock?"

**The fix:**

```clojure
;; GOOD: Test the actual outcome, not the mock
(deftest processes-order-test
  (with-redefs [db/save-order (fn [order] (swap! test-db conj order))]
    (let [order {:id 1 :items ["a" "b"]}]
      (process-order order)
      ;; Test the real behavior: order was processed correctly
      (is (= 1 (count @test-db)))
      (is (= order (first @test-db))))))

;; OR better: use a test database fixture instead of mocking
(deftest processes-order-test
  (let [order {:id 1 :items ["a" "b"]}]
    (process-order order)
    (is (= order (db/get-order *test-db* 1)))))
```

### Gate Function

```
BEFORE asserting on any mock:
  Ask: "Am I testing real behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or use real implementation

  Test real behavior instead
```

## Anti-Pattern 2: Test-Only Functions in Production

**The violation:**

```clojure
;; BAD: reset-state! only used in tests
(ns myapp.session)

(defonce ^:private state (atom {}))

(defn create-session [user-id]
  (swap! state assoc user-id {:created (System/currentTimeMillis)}))

;; This function exists only for tests!
(defn reset-state!
  "Resets internal state. FOR TESTING ONLY."
  []
  (reset! state {}))
```

**Why this is wrong:**

- Production namespace polluted with test-only code
- Dangerous if accidentally called in production
- Violates separation of concerns
- The comment "FOR TESTING ONLY" is a code smell

**The fix:**

```clojure
;; GOOD: Production code has no test-only functions
(ns myapp.session)

(defonce ^:private state (atom {}))

(defn create-session [user-id]
  (swap! state assoc user-id {:created (System/currentTimeMillis)}))

;; In test namespace - use fixture for cleanup
(ns myapp.session-test
  (:require [clojure.test :refer [deftest is use-fixtures]]
            [myapp.session :as session]))

;; Access internal state via var for testing only
(defn reset-session-state-fixture [f]
  (reset! @#'session/state {})
  (f)
  (reset! @#'session/state {}))

(use-fixtures :each reset-session-state-fixture)
```

### Gate Function

```
BEFORE adding any function to production namespace:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test namespace or test utilities instead

  Ask: "Does this namespace own this resource's lifecycle?"

  IF no:
    STOP - Wrong namespace for this function
```

## Anti-Pattern 3: Mocking Without Understanding

**The violation:**

```clojure
;; BAD: Mock breaks test logic
(deftest detects-duplicate-server-test
  ;; Mock prevents config write that test depends on!
  (with-redefs [config/save-server (fn [_] nil)]
    (add-server {:name "server1" :url "http://localhost"})
    ;; This should throw duplicate error - but config was never saved!
    (is (thrown? Exception
                 (add-server {:name "server1" :url "http://localhost"})))))
```

**Why this is wrong:**

- Mocked function had side effect test depended on (writing config)
- Over-mocking to "be safe" breaks actual behavior
- Test passes for wrong reason or fails mysteriously

**The fix:**

```clojure
;; GOOD: Mock at correct level - only the slow/external operation
(deftest detects-duplicate-server-test
  ;; Only mock the actual network call, preserve config behavior
  (with-redefs [http/connect (fn [_] {:status :connected})]
    (add-server {:name "server1" :url "http://localhost"})
    ;; Config was written, duplicate detection works
    (is (thrown? Exception
                 (add-server {:name "server1" :url "http://localhost"})))))
```

### Gate Function

```
BEFORE mocking any function:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real function have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level function the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

## Anti-Pattern 4: Incomplete Mocks

**The violation:**

```clojure
;; BAD: Partial mock - only fields you think you need
(deftest processes-api-response-test
  (with-redefs [api/fetch-user (fn [_] {:id 123 :name "Alice"})]
    ;; Later: breaks when code accesses (:email response) or (:metadata response)
    (is (= "Alice" (:name (process-user-response 123))))))
```

**Why this is wrong:**

- **Partial mocks hide structural assumptions** - You only mocked fields you know about
- **Downstream code may depend on fields you didn't include** - Silent nil failures
- **Tests pass but integration fails** - Mock incomplete, real API complete
- **False confidence** - Test proves nothing about real behavior

**The Iron Rule:** Mock the COMPLETE data structure as it exists in reality, not just fields your immediate test uses.

**The fix:**

```clojure
;; GOOD: Mirror real API response completely
(def mock-user-response
  {:id 123
   :name "Alice"
   :email "alice@example.com"
   :metadata {:request-id "req-789"
              :timestamp 1234567890}
   :permissions #{:read :write}})

(deftest processes-api-response-test
  (with-redefs [api/fetch-user (fn [_] mock-user-response)]
    (let [result (process-user-response 123)]
      (is (= "Alice" (:name result)))
      (is (some? (:metadata result))))))
```

### Gate Function

```
BEFORE creating mock data:
  Check: "What fields does the real data structure contain?"

  Actions:
    1. Examine actual API response/data from docs or REPL
    2. Include ALL fields system might consume downstream
    3. Verify mock matches real data schema completely

  Critical:
    If you're creating a mock, you must understand the ENTIRE structure
    Partial mocks fail silently when code depends on omitted fields

  If uncertain: Include all documented fields
```

## Anti-Pattern 5: Misusing with-redefs vs binding

**The violation:**

```clojure
;; BAD: Using with-redefs for dynamic vars
(def ^:dynamic *config* {:env :prod})

(deftest config-test
  ;; with-redefs on dynamic var - affects all threads, not scoped properly
  (with-redefs [*config* {:env :test}]
    (is (= :test (:env *config*)))))
```

**Why this is wrong:**

- `with-redefs` modifies the var root, affecting all threads
- Not thread-safe for dynamic vars
- `binding` exists specifically for this purpose

**The fix:**

```clojure
;; GOOD: Use binding for dynamic vars
(def ^:dynamic *config* {:env :prod})

(deftest config-test
  (binding [*config* {:env :test}]
    (is (= :test (:env *config*)))))

;; GOOD: Use with-redefs for regular functions
(deftest api-test
  (with-redefs [http/get (fn [_] {:status 200 :body "ok"})]
    (is (= 200 (:status (fetch-data))))))
```

### Gate Function

```
BEFORE choosing mock mechanism:
  Ask: "Is this a dynamic var (^:dynamic)?"

  IF yes:
    Use binding - thread-local, properly scoped

  IF no (regular var/function):
    Use with-redefs - temporarily replaces root binding
```

## Anti-Pattern 6: Integration Tests as Afterthought

**The violation:**

```
Implementation complete
No tests written
"Ready for testing"
```

**Why this is wrong:**

- Testing is part of implementation, not optional follow-up
- TDD would have caught this
- Can't claim complete without tests

**The fix:**

```
TDD cycle:
1. Write failing test
2. Implement to pass
3. Refactor
4. THEN claim complete
```

## Anti-Pattern 7: Fragmented Assertions

**The violation:**

```clojure
;; BAD: Picking apart the result piece by piece
(deftest user-creation-test
  (let [result (sut/create-user {:name "Alice" :email "alice@example.com"})]
    (is (= "Alice" (:name result)))
    (is (= "alice@example.com" (:email result)))
    (is (uuid? (:id result)))
    (is (inst? (:created-at result)))
    (is (= :active (:status result)))))
```

**Why this is wrong:**

- **Obscures the actual data shape** - Can't see at a glance what the function returns
- **Harder to maintain** - Adding a field means adding another assertion
- **Poor failure messages** - "expected: Alice, actual: Bob" tells you less than a full diff
- **Verbose and noisy** - Five lines of assertions when one would do
- **Easy to miss fields** - You might forget to assert on important keys

**The fix:**

```clojure
;; GOOD: Single assertion on the whole structure
(deftest user-creation-test
  (let [result (sut/create-user {:name "Alice" :email "alice@example.com"})]
    (is (= {:name "Alice"
            :email "alice@example.com"
            :id (:id result)              ; capture generated values
            :created-at (:created-at result)
            :status :active}
           result))))
```

**For generated/dynamic values:**

```clojure
;; GOOD: Use select-keys when you can't predict all fields
(deftest user-creation-test
  (let [result (sut/create-user {:name "Alice" :email "alice@example.com"})]
    ;; Assert on known fields
    (is (= {:name "Alice"
            :email "alice@example.com"
            :status :active}
           (select-keys result [:name :email :status])))
    ;; Separately verify generated fields exist and have correct type
    (is (uuid? (:id result)))
    (is (inst? (:created-at result)))))
```

### Gate Function

```
BEFORE writing multiple (is (= ...)) assertions on the same result:
  Ask: "Could this be a single data comparison?"

  IF yes:
    Write one (is (= {...expected...} result))
    Use select-keys if you need to ignore some fields
    Only use separate assertions for type checks on generated values

  Benefits:
    - Shows complete expected shape in one place
    - Test failure diff shows exactly what's different
    - Easier to update when data shape changes
```

## When Mocks Become Too Complex

**Warning signs:**

- Mock setup longer than test logic
- Using `with-redefs` on 5+ functions
- Mocks missing behavior real functions have
- Test breaks when mock changes

**Your human partner's question:** "Do we need to be using a mock here?"

**Consider:** Integration tests with real components (using fixtures) often simpler than complex mocks

```clojure
;; BAD: Complex mock setup
(deftest complex-workflow-test
  (with-redefs [db/query (fn [_] [...])
                cache/get (fn [_] nil)
                cache/set (fn [_ _] nil)
                api/fetch (fn [_] {...})
                metrics/record (fn [_] nil)]
    ;; Test logic buried under mocks
    ...))

;; GOOD: Use test fixtures with real (or test) implementations
(use-fixtures :each db-fixture cache-fixture)

(deftest complex-workflow-test
  ;; Only mock external API
  (with-redefs [api/fetch (fn [_] mock-api-response)]
    (let [result (complex-workflow {:id 1})]
      (is (= :success (:status result)))
      ;; Verify real db state
      (is (some? (db/get-by-id *test-db* 1))))))
```

## TDD Prevents These Anti-Patterns

**Why TDD helps:**

1. **Write test first** - Forces you to think about what you're actually testing
2. **Watch it fail** - Confirms test tests real behavior, not mocks
3. **Minimal implementation** - No test-only functions creep in
4. **Real dependencies** - You see what the test actually needs before mocking

**If you're testing mock behavior, you violated TDD** - you added mocks without watching test fail against real code first.

## Quick Reference

| Anti-Pattern                    | Fix                                           |
| ------------------------------- | --------------------------------------------- |
| Assert on mock calls            | Test real behavior or outcomes                |
| Test-only fns in production     | Move to test namespace/utilities              |
| Mock without understanding      | Understand dependencies first, mock minimally |
| Incomplete mock data            | Mirror real data structure completely         |
| with-redefs on dynamic vars     | Use binding instead                           |
| Tests as afterthought           | TDD - tests first                             |
| Over-complex mocks              | Consider integration tests with fixtures      |
| Fragmented assertions           | Single `(is (= {...} result))` comparison     |

## Red Flags

- Test only verifies mock was called
- Functions only called in test files
- Mock setup is >50% of test
- Test fails when you remove mock
- Can't explain why mock is needed
- Mocking "just to be safe"
- Using `with-redefs` on `^:dynamic` vars
- Multiple `(is (= x (:key result)))` on same result

## The Bottom Line

**Mocks are tools to isolate, not things to test.**

If TDD reveals you're testing mock behavior, you've gone wrong.

Fix: Test real behavior or question why you're mocking at all.
