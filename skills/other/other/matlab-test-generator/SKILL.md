---
name: matlab-test-generator
description: Create comprehensive MATLAB unit tests using the MATLAB Testing Framework. Use when generating test files, test cases, unit tests, test suites, or when the user requests testing for MATLAB code, functions, or classes.
license: MathWorks BSD-3-Clause (see LICENSE)
---

# MATLAB Test Generator

This skill provides comprehensive guidelines for creating robust unit tests using the MATLAB Testing Framework. Generate test classes, test methods, and test suites following MATLAB best practices.

## When to Use This Skill

- Creating unit tests for MATLAB functions or classes
- Generating test suites for existing code
- Writing test cases with assertions and fixtures
- Creating parameterized tests
- Setting up test environments with setup/teardown methods
- When user requests testing, test coverage, or mentions unit tests

## MATLAB Testing Framework Overview

MATLAB supports multiple testing approaches:

1. **Script-Based Tests** - Simple test scripts with assertions
2. **Function-Based Tests** - Test functions with local functions for each test
3. **Class-Based Tests** - Full-featured test classes (recommended for complex testing)

## Test Class Structure

### Basic Test Class Template

```matlab
classdef MyFunctionTest < matlab.unittest.TestCase
    % Tests for myFunction

    properties (TestParameter)
        % Define parameters for parameterized tests
    end

    properties
        % Test fixtures and shared data
    end

    methods (TestClassSetup)
        % Runs once before all tests
    end

    methods (TestClassTeardown)
        % Runs once after all tests
    end

    methods (TestMethodSetup)
        % Runs before each test method
    end

    methods (TestMethodTeardown)
        % Runs after each test method
    end

    methods (Test)
        % Individual test methods
    end
end
```

## Critical Rules

### File Naming
- **Test files MUST end with `Test.m`** (e.g., `myFunctionTest.m`)
- Class name must match filename
- Follow PascalCase naming convention
- Place in `tests/` directory or alongside source with `Test` suffix

### Test Method Naming
- Use descriptive, readable names
- Start with lowercase letter
- Use camelCase
- Describe what is being tested
- Example: `testAdditionWithPositiveNumbers`

### Assertions
Always use the appropriate assertion method:
- `verifyEqual(actual, expected)` - Continues testing on failure
- `assertEqual(actual, expected)` - Stops testing on failure (legacy)
- `verifyTrue(condition)` - Verify boolean condition
- `verifyError(f, errorID)` - Verify function throws error
- `verifyWarning(f, warningID)` - Verify function issues warning
- `verifyInstanceOf(actual, expectedClass)` - Verify object type
- `verifySize(actual, expectedSize)` - Verify array size
- `verifyEmpty(actual)` - Verify empty array

## Complete Test Examples

### Example 1: Testing a Simple Function

Function to test (`add.m`):
```matlab
function result = add(a, b)
    % ADD Add two numbers
    result = a + b;
end
```

Test class (`addTest.m`):
```matlab
classdef addTest < matlab.unittest.TestCase
    % Tests for add function

    methods (Test)
        function testAddPositiveNumbers(testCase)
            % Test addition of positive numbers
            result = add(2, 3);
            testCase.verifyEqual(result, 5);
        end

        function testAddNegativeNumbers(testCase)
            % Test addition of negative numbers
            result = add(-2, -3);
            testCase.verifyEqual(result, -5);
        end

        function testAddMixedNumbers(testCase)
            % Test addition of positive and negative
            result = add(5, -3);
            testCase.verifyEqual(result, 2);
        end

        function testAddZero(testCase)
            % Test addition with zero
            result = add(5, 0);
            testCase.verifyEqual(result, 5);
        end

        function testAddArrays(testCase)
            % Test element-wise addition of arrays
            result = add([1 2 3], [4 5 6]);
            testCase.verifyEqual(result, [5 7 9]);
        end
    end
end
```

### Example 2: Parameterized Tests

```matlab
classdef calculateAreaTest < matlab.unittest.TestCase
    % Tests for calculateArea function with parameters

    properties (TestParameter)
        rectangleDims = struct(...
            'small', struct('width', 2, 'height', 3, 'expected', 6), ...
            'large', struct('width', 10, 'height', 20, 'expected', 200), ...
            'unit', struct('width', 1, 'height', 1, 'expected', 1));
    end

    methods (Test)
        function testRectangleArea(testCase, rectangleDims)
            % Test rectangle area calculation
            area = calculateArea(rectangleDims.width, rectangleDims.height);
            testCase.verifyEqual(area, rectangleDims.expected);
        end
    end
end
```

### Example 3: Tests with Fixtures

```matlab
classdef DataProcessorTest < matlab.unittest.TestCase
    % Tests for DataProcessor class with setup/teardown

    properties
        TestData
        TempFile
    end

    methods (TestMethodSetup)
        function createTestData(testCase)
            % Create test data before each test
            testCase.TestData = rand(100, 5);
            testCase.TempFile = tempname;
        end
    end

    methods (TestMethodTeardown)
        function deleteTestData(testCase)
            % Clean up after each test
            if isfile(testCase.TempFile)
                delete(testCase.TempFile);
            end
        end
    end

    methods (Test)
        function testDataLoading(testCase)
            % Test data loading functionality
            save(testCase.TempFile, 'data', testCase.TestData);
            processor = DataProcessor(testCase.TempFile);
            testCase.verifyEqual(processor.data, testCase.TestData);
        end

        function testDataNormalization(testCase)
            % Test data normalization
            processor = DataProcessor();
            processor.data = testCase.TestData;
            normalized = processor.normalize();
            testCase.verifyLessThanOrEqual(max(normalized(:)), 1);
            testCase.verifyGreaterThanOrEqual(min(normalized(:)), 0);
        end
    end
end
```

### Example 4: Error Testing

```matlab
classdef validateInputTest < matlab.unittest.TestCase
    % Tests for validateInput function

    methods (Test)
        function testValidInput(testCase)
            % Test valid input passes
            testCase.verifyWarningFree(@() validateInput(5));
        end

        function testNegativeInputError(testCase)
            % Test negative input throws error
            testCase.verifyError(@() validateInput(-5), 'MATLAB:validators:mustBePositive');
        end

        function testNonNumericInputError(testCase)
            % Test non-numeric input throws error
            testCase.verifyError(@() validateInput('text'), 'MATLAB:validators:mustBeNumeric');
        end

        function testEmptyInputError(testCase)
            % Test empty input throws error
            testCase.verifyError(@() validateInput([]), 'MATLAB:validators:mustBeNonempty');
        end
    end
end
```

## Test Organization Best Practices

### Directory Structure
```
project/
├── src/
│   ├── myFunction.m
│   └── MyClass.m
└── tests/
    ├── myFunctionTest.m
    └── MyClassTest.m
```

### Running Tests

**Run all tests in directory:**
```matlab
results = runtests('tests')
```

**Run specific test class:**
```matlab
results = runtests('myFunctionTest')
```

**Run specific test method:**
```matlab
results = runtests('myFunctionTest/testAddPositiveNumbers')
```

**Generate test suite:**
```matlab
suite = testsuite('tests');
results = run(suite);
```

**With coverage report:**
```matlab
import matlab.unittest.TestRunner
import matlab.unittest.plugins.CodeCoveragePlugin

runner = TestRunner.withTextOutput;
runner.addPlugin(CodeCoveragePlugin.forFolder('src'));
results = runner.run(testsuite('tests'));
```

## Assertion Tolerance

For floating-point comparisons, use tolerance:

```matlab
% Absolute tolerance
testCase.verifyEqual(actual, expected, 'AbsTol', 1e-10);

% Relative tolerance
testCase.verifyEqual(actual, expected, 'RelTol', 1e-6);

% Both
testCase.verifyEqual(actual, expected, 'AbsTol', 1e-10, 'RelTol', 1e-6);
```

## Test Assumptions

Use assumptions to skip tests when prerequisites aren't met:

```matlab
function testPlotting(testCase)
    % Skip test if not running in graphical environment
    testCase.assumeTrue(usejava('desktop'), 'Requires desktop environment');

    % Test code here
    fig = figure;
    plot(1:10);
    testCase.verifyInstanceOf(fig, 'matlab.ui.Figure');
    close(fig);
end
```

## Test Tagging

Tag tests for selective execution:

```matlab
methods (Test, TestTags = {'Unit'})
    function testBasicOperation(testCase)
        % Fast unit test
    end
end

methods (Test, TestTags = {'Integration', 'Slow'})
    function testDatabaseConnection(testCase)
        % Slower integration test
    end
end
```

Run tagged tests:
```matlab
% Run only Unit tests
suite = testsuite('tests', 'Tag', 'Unit');
results = run(suite);
```

## Mock Objects and Stubs

For testing code with dependencies:

```matlab
function testWithMock(testCase)
    % Create mock object
    import matlab.mock.TestCase
    [mock, behavior] = testCase.createMock(?MyInterface);

    % Define behavior
    testCase.assignOutputsWhen(withAnyInputs(behavior.methodName), expectedOutput);

    % Use mock in test
    result = functionUnderTest(mock);
    testCase.verifyEqual(result, expectedValue);
end
```

## Performance Testing

Test execution time:

```matlab
function testPerformance(testCase)
    % Test function executes within time limit
    tic;
    result = expensiveFunction(largeData);
    elapsedTime = toc;

    testCase.verifyLessThan(elapsedTime, 1.0, ...
        'Function should complete within 1 second');
end
```

## Checklist for Test Creation

Before finalizing tests, verify:
- [ ] Test file ends with `Test.m`
- [ ] Class inherits from `matlab.unittest.TestCase`
- [ ] Test methods use descriptive names
- [ ] Appropriate assertions used (verify vs assert)
- [ ] Edge cases covered (empty, zero, negative, large values)
- [ ] Error cases tested with `verifyError`
- [ ] Floating-point comparisons use tolerance
- [ ] Setup/teardown methods clean up resources
- [ ] Tests are independent (can run in any order)
- [ ] Tests follow Arrange-Act-Assert pattern
- [ ] Parameterized tests used for similar test cases
- [ ] Comments explain what is being tested

## Common Patterns

### Arrange-Act-Assert Pattern

```matlab
function testCalculation(testCase)
    % Arrange - Set up test data
    input1 = 5;
    input2 = 3;
    expected = 8;

    % Act - Execute the code under test
    actual = myFunction(input1, input2);

    % Assert - Verify the result
    testCase.verifyEqual(actual, expected);
end
```

### Testing Private Methods

```matlab
% Use access to test private methods
classdef MyClassTest < matlab.unittest.TestCase
    methods (Test)
        function testPrivateMethod(testCase)
            obj = MyClass();
            % Access private method
            result = obj.privateMethod(testCase);
            testCase.verifyEqual(result, expectedValue);
        end
    end
end
```

### Testing Static Methods

```matlab
function testStaticMethod(testCase)
    % Test static method without instantiation
    result = MyClass.staticMethod(input);
    testCase.verifyEqual(result, expected);
end
```

## Troubleshooting

**Issue**: Tests not discovered
- **Solution**: Ensure filename ends with `Test.m` and class inherits from `matlab.unittest.TestCase`

**Issue**: Floating-point comparison failures
- **Solution**: Use `'AbsTol'` or `'RelTol'` parameters with `verifyEqual`

**Issue**: Tests affecting each other
- **Solution**: Ensure proper cleanup in teardown methods and test independence

**Issue**: Slow test execution
- **Solution**: Use tags to separate fast unit tests from slow integration tests

## Additional Resources

- Use `doc matlab.unittest.TestCase` for complete assertion reference
- Use `doc matlab.unittest.fixtures` for advanced fixture usage
- Use `doc matlab.mock` for mocking framework documentation
