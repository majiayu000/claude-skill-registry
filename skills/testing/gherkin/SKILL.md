---
name: gherkin
description: Create and format Gherkin feature files using BDD syntax. Use when creating feature files, scenarios, or writing behavioral specifications.
allowed-tools: Read, Write, Edit, Glob, WebFetch
---

# Gherkin Feature File Skill

## File Naming Convention

**IMPORTANT**: All Gherkin feature files MUST follow this naming pattern:

```
gherkin.feature_N.feature
```

Where `N` is a sequential number (1, 2, 3, etc.)

Examples:
- `gherkin.feature_1.feature`
- `gherkin.feature_2.feature`
- `gherkin.feature_42.feature`

## When Uncertain About Formatting

If you have questions about Gherkin syntax or formatting:

1. **First**, check the examples below for common patterns
2. **If still unclear**, refer to the official documentation at:
   https://cucumber.io/docs/gherkin/reference

## Core Gherkin Structure

### Basic Feature Template

```gherkin
@tag
Feature: Feature Name

  Background: (Optional - runs before each scenario)
    Given some common precondition

  Scenario: Scenario Name
    Given a precondition
    When an action occurs
    Then an expected outcome
    And another expected outcome

  Scenario Outline: Scenario with examples
    Given a user with <status>
    When they perform <action>
    Then they should see <result>

    Examples:
      | status | action | result  |
      | admin  | delete | success |
      | user   | delete | denied  |
```

### Using Rules

```gherkin
Feature: Feature Name

  Rule: Business Rule Name

    Example: First scenario under this rule
      Given a precondition
      When an action
      Then an outcome

    Example: Second scenario under this rule
      Given another precondition
      When another action
      Then another outcome

  Rule: Another Business Rule

    Example: Scenario for second rule
      ...
```

## Keywords Reference

- **Feature**: High-level description of a software feature
- **Rule**: Represents a business rule to implement (optional)
- **Example/Scenario**: Concrete example illustrating a business rule
- **Scenario Outline**: Template scenario with multiple inputs via Examples table
- **Background**: Steps to run before each scenario in the feature
- **Given**: Describes the initial context (preconditions)
- **When**: Describes an event or action
- **Then**: Describes an expected outcome (postcondition)
- **And/But**: Additional steps for any of the above
- **@tag**: Annotations for filtering/organizing (e.g., @failing, @wip, @smoke)

## Canonical Examples

### Example 1: Simple Game Feature

```gherkin
@failing
Feature: Guess the word

  # The first example has two steps
  Scenario: Maker starts a game
    When the Maker starts a game
    Then the Maker waits for a Breaker to join

  # The second example has three steps
  Scenario: Breaker joins a game
    Given the Maker has started a game with the word "silky"
    When the Breaker joins the Maker's game
    Then the Breaker must guess a word with 5 characters
```

### Example 2: Feature with Rules

```gherkin
# -- FILE: features/gherkin.rule_example.feature
@failing
Feature: Highlander

  Rule: There can be only One

    Example: Only One -- More than one alive
      Given there are 3 ninjas
      And there are more than one ninja alive
      When 2 ninjas meet, they will fight
      Then one ninja dies (but not me)
      And there is one ninja less alive

    Example: Only One -- One alive
      Given there is only 1 ninja alive
      Then they will live forever ;-)

  Rule: There can be Two (in some cases)

    Example: Two -- Dead and Reborn as Phoenix
      ...
```

## Best Practices

1. **Use descriptive feature names** that clearly state the business capability
2. **Write scenarios from the user's perspective**, not implementation details
3. **Keep scenarios independent** - each should be able to run alone
4. **Use tags** to organize and filter scenarios (@smoke, @wip, @failing, etc.)
5. **Comments** can be added with `#` but use sparingly
6. **Rules** help organize related scenarios under business rules
7. **Data tables** can be used in steps for structured input
8. **Doc strings** (triple quotes) can include multi-line text in steps

## Common Patterns

### Data Tables in Steps

```gherkin
Given the following users exist:
  | name  | email           | role  |
  | Alice | alice@test.com  | admin |
  | Bob   | bob@test.com    | user  |
```

### Doc Strings

```gherkin
Given a blog post with content:
  """
  This is a multi-line
  blog post content
  """
```

## Creating New Feature Files

When asked to create a Gherkin feature:

1. **Determine the next number** by checking existing `gherkin.feature_*.feature` files
2. **Create the file** with the correct naming convention
3. **Start with a Feature declaration** including appropriate tags
4. **Use Rules** if organizing multiple related scenarios
5. **Write clear, behavior-focused scenarios** using Given/When/Then
6. **Add comments** only where they clarify complex logic
7. **Review against examples** above to ensure consistent style

## Additional Resources

For complex questions about Gherkin syntax, step arguments, or advanced features:
- Official Reference: https://cucumber.io/docs/gherkin/reference
- Gherkin Syntax: https://cucumber.io/docs/gherkin/
