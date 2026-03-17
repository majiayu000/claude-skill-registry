---
name: use-case-2.0
description: "Use Case 2.0 methodology by Ivar Jacobson. Covers use case slices, lightweight documentation, user story derivation, and value-driven prioritization. Modern approach to use case modeling for agile teams."
allowed-tools: Read, Write, Glob, Grep, Task
---

# Use Case 2.0

A modern, lightweight approach to use case modeling that integrates with agile practices while preserving the benefits of structured requirements.

## When to Use This Skill

**Keywords:** use case, use case 2.0, Ivar Jacobson, use case slice, narrative, basic flow, alternate flow, exception, actor, goal, scenario, precondition, postcondition, trigger, user story from use case

**Use this skill when:**

- Modeling system behavior from user perspective
- Deriving user stories from use cases
- Planning releases using use case slices
- Documenting complex interactions with multiple paths
- Understanding actor goals and system responses
- Creating testable requirements from narratives

## What is Use Case 2.0?

Use Case 2.0 modernizes classic use cases for agile contexts while retaining their power for:

- Capturing functional requirements comprehensively
- Understanding system boundaries and actors
- Identifying all paths through a scenario (happy path + alternatives + exceptions)
- Creating traceable, testable specifications

### Key Principles

| Principle | Description |
|-----------|-------------|
| **Slice-based** | Use cases are implemented in slices, not all at once |
| **Lightweight** | Start simple, add detail only when needed |
| **Story-compatible** | User stories can be derived from use case slices |
| **Test-first** | Each slice is testable before implementation |
| **Value-driven** | Slices prioritized by business value |

## Use Case 2.0 Lifecycle

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   FIND       │ →  │   SLICE      │ →  │   PREPARE    │
│ Use Cases    │    │ Use Cases    │    │ Use Case     │
│              │    │              │    │ Slices       │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                    ┌──────────────┐    ┌──────┴───────┐
                    │   INSPECT    │ ←  │   ANALYZE    │
                    │   & ADAPT    │    │   Slices     │
                    └──────────────┘    └──────────────┘
```

### Phase Details

```yaml
use_case_lifecycle:
  find:
    purpose: "Identify use cases from goals and actors"
    activities:
      - "Identify actors (primary, supporting, offstage)"
      - "Capture actor goals"
      - "Name use cases (verb-noun)"
      - "Create use case diagram"
    output: "Use case model (diagram + brief descriptions)"

  slice:
    purpose: "Break use cases into implementable slices"
    activities:
      - "Identify basic flow (happy path)"
      - "Identify alternative flows"
      - "Identify exception flows"
      - "Group flows into slices"
    output: "Sliced use cases with prioritization"

  prepare:
    purpose: "Detail slices for implementation"
    activities:
      - "Write narrative for selected slice"
      - "Define test cases"
      - "Identify special requirements"
    output: "Ready-for-development slice"

  analyze:
    purpose: "Verify slice is implementable"
    activities:
      - "Review with stakeholders"
      - "Validate test cases"
      - "Confirm acceptance criteria"
    output: "Validated slice"

  inspect_adapt:
    purpose: "Learn and improve"
    activities:
      - "Review implemented slices"
      - "Update use case model"
      - "Refine remaining slices"
    output: "Updated backlog"
```

## Use Case Elements

### Actor Types

```yaml
actor_types:
  primary_actor:
    definition: "Actor whose goal the use case satisfies"
    examples:
      - "Customer placing an order"
      - "Administrator managing users"
    notation: "Stick figure connected to use case"

  supporting_actor:
    definition: "Actor that provides a service to the system"
    examples:
      - "Payment Gateway processing payment"
      - "Email Service sending notifications"
    notation: "Stick figure connected to use case (labeled)"

  offstage_actor:
    definition: "Actor with interest but no direct interaction"
    examples:
      - "Auditor requiring transaction logs"
      - "Regulator requiring compliance"
    notation: "Listed in stakeholders section"
```

### Use Case Brief

Lightweight initial documentation:

```yaml
use_case_brief:
  template:
    id: "UC-{domain}-{number}"
    name: "{Verb} {Noun}"
    primary_actor: "{Actor name}"
    goal: "{What the actor wants to achieve}"
    brief_description: "{1-2 sentences}"

  example:
    id: "UC-ORD-001"
    name: "Place Order"
    primary_actor: "Customer"
    goal: "Purchase products from the catalog"
    brief_description: "Customer selects products, provides shipping and payment information, and submits order for processing."
```

### Use Case Narrative

Full documentation format:

```markdown
## Use Case: {Name}

**ID:** UC-{XXX}-{NNN}
**Version:** {N.N}

### Overview

| Element | Description |
|---------|-------------|
| **Primary Actor** | {Actor name} |
| **Goal** | {What the actor wants to achieve} |
| **Scope** | {System boundary} |
| **Level** | {User goal / Subfunction / Summary} |
| **Trigger** | {What starts the use case} |

### Stakeholders and Interests

- **{Stakeholder 1}**: {Interest/concern}
- **{Stakeholder 2}**: {Interest/concern}

### Preconditions

- {Condition that must be true before use case can start}
- {Another precondition}

### Success Guarantee (Postconditions)

- {Condition guaranteed to be true after successful completion}
- {Another postcondition}

### Basic Flow (Main Success Scenario)

1. {Actor} {action}
2. System {response}
3. {Actor} {action}
4. System {response}
5. ...
6. System {final response indicating success}

### Alternative Flows

#### {Alternative Name} (at step {N})

**Condition:** {When this alternative applies}

{N}a. {Alternative action}
{N}b. System {alternative response}
{N}c. Return to step {M} / Use case ends

#### {Another Alternative} (at step {N})

...

### Exception Flows

#### {Exception Name} (at step {N})

**Condition:** {When this exception occurs}

{N}a. System {error detection}
{N}b. System {error handling}
{N}c. Use case ends in failure / Return to step {M}

### Special Requirements

- {Non-functional requirement affecting this use case}
- {Performance, security, usability requirement}

### Technology and Data Variations

- {Step N}: {Variation in technology or data format}

### Related Information

- **Frequency:** {How often this use case occurs}
- **Related Use Cases:** {Links to included/extended use cases}
- **Business Rules:** {BR-xxx, BR-yyy}
```

## Use Case Slicing

### What is a Slice?

```yaml
use_case_slice:
  definition: "A subset of a use case that delivers value and is independently testable"

  characteristics:
    - "Implements part of use case flows"
    - "Can be developed in one iteration"
    - "Has clear acceptance criteria"
    - "Delivers incremental value"

  slice_types:
    basic_flow_slice:
      description: "Happy path only (simplest implementation)"
      example: "Place Order - basic checkout with existing customer"

    flow_variation_slice:
      description: "Basic flow + one alternative"
      example: "Place Order - with new customer registration"

    exception_slice:
      description: "Basic flow + exception handling"
      example: "Place Order - payment declined handling"

    complete_slice:
      description: "Full use case with all paths"
      example: "Place Order - complete implementation"
```

### Slicing Strategies

```yaml
slicing_strategies:
  by_actor:
    description: "Different slices for different actors"
    example: "Customer checkout vs. Admin override checkout"

  by_data_variation:
    description: "Different data types or volumes"
    example: "Single item order vs. bulk order"

  by_business_rule:
    description: "Different rules applied"
    example: "Standard pricing vs. promotional pricing"

  by_interface:
    description: "Different UI or integration points"
    example: "Web checkout vs. API checkout"

  by_quality:
    description: "Different quality attributes"
    example: "Basic validation vs. full validation"
```

### Slice Template

```yaml
use_case_slice:
  id: "UC-{XXX}-{NNN}-S{NN}"
  use_case: "UC-{XXX}-{NNN}"
  name: "{Use Case Name} - {Slice Description}"

  scope:
    flows_included:
      - "Basic flow steps 1-6"
      - "Alternative 3a (guest checkout)"
    flows_excluded:
      - "Alternative 2a (saved addresses)"
      - "Exception 5a (payment failure)"

  value_statement: "{What this slice enables for the user}"

  acceptance_criteria:
    - given: "{Precondition}"
      when: "{Action}"
      then: "{Expected outcome}"

  test_scenarios:
    - "Happy path with valid data"
    - "Guest checkout without account"

  estimate: "{Story points or ideal days}"
  priority: "{Value/Risk ranking}"
```

## User Story Derivation

Convert use case slices to user stories:

```yaml
slice_to_story:
  pattern: "Each slice becomes one or more user stories"

  mapping:
    use_case_name: "Epic name"
    slice: "User story"
    acceptance_criteria: "Acceptance criteria"
    test_scenarios: "Test cases"

  example:
    use_case: "Place Order"
    slices:
      - slice: "Basic checkout"
        story: |
          As a Customer
          I want to place an order with items in my cart
          So that I can receive my purchased products

      - slice: "Guest checkout"
        story: |
          As a Guest
          I want to checkout without creating an account
          So that I can complete my purchase quickly

      - slice: "Payment retry"
        story: |
          As a Customer
          I want to retry payment if it fails
          So that I can complete my order without starting over
```

### Story Mapping from Use Cases

```text
Use Case Model              →    Story Map
─────────────────                ─────────────────
UC: Place Order                  Epic: Order Placement
├── Basic Flow               →   ├── Basic Checkout
├── Alt: Guest Checkout      →   ├── Guest Checkout
├── Alt: Saved Address       →   ├── Address Management
├── Alt: Gift Wrapping       →   ├── Gift Options
├── Exc: Payment Failed      →   ├── Payment Error Handling
└── Exc: Out of Stock        →   └── Inventory Handling
```

## Use Case Diagram

### UML Notation

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Order Management System                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  ╭──────────────╮       ╭─────────────────╮               │ │
│  │  │ Place Order  │───────│ Process Payment │               │ │
│  │  ╰──────────────╯       ╰─────────────────╯               │ │
│  │         │                        │                         │ │
│  │         │ «include»              │ «include»               │ │
│  │         ▼                        ▼                         │ │
│  │  ╭──────────────╮       ╭─────────────────╮               │ │
│  │  │ Select Items │       │ Validate Card   │               │ │
│  │  ╰──────────────╯       ╰─────────────────╯               │ │
│  │                                                            │ │
│  │  ╭──────────────╮                                         │ │
│  │  │ Cancel Order │                                         │ │
│  │  ╰──────────────╯                                         │ │
│  │         ▲                                                  │ │
│  │         │ «extend»                                         │ │
│  │         │ [within cancellation window]                     │ │
│  │  ╭──────────────╮                                         │ │
│  │  │ View Order   │                                         │ │
│  │  ╰──────────────╯                                         │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

     ○                                               ○
    /|\  ────────── Place Order                     /|\  ────────── Process Payment
    / \                                             / \
  Customer                                    Payment Gateway
```

### Relationships

```yaml
use_case_relationships:
  include:
    notation: "«include»"
    meaning: "Base use case ALWAYS includes the behavior"
    example: "Place Order «include» Process Payment"
    arrow: "Dashed arrow from base to included"

  extend:
    notation: "«extend»"
    meaning: "Extension use case MAY add behavior under conditions"
    example: "View Order «extend» Cancel Order [within window]"
    arrow: "Dashed arrow from extension to base"

  generalization:
    notation: "Triangle arrow"
    meaning: "Child use case inherits from parent"
    example: "Pay by Credit Card inherits from Make Payment"
```

## .NET/C# Implementation

### Use Case Model

```csharp
// Domain model for Use Case 2.0
namespace Requirements.UseCases;

public record UseCase
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public required Actor PrimaryActor { get; init; }
    public required string Goal { get; init; }
    public required UseCaseLevel Level { get; init; }
    public string? Trigger { get; init; }
    public string? Scope { get; init; }

    public List<Stakeholder> Stakeholders { get; init; } = [];
    public List<string> Preconditions { get; init; } = [];
    public List<string> Postconditions { get; init; } = [];
    public List<FlowStep> BasicFlow { get; init; } = [];
    public List<AlternativeFlow> AlternativeFlows { get; init; } = [];
    public List<ExceptionFlow> ExceptionFlows { get; init; } = [];
    public List<string> SpecialRequirements { get; init; } = [];
    public List<UseCaseSlice> Slices { get; init; } = [];
}

public enum UseCaseLevel
{
    Summary,      // High-level business process
    UserGoal,     // Primary level - user achieves goal
    Subfunction   // Supporting functionality
}

public record Actor(
    string Name,
    ActorType Type,
    string? Description = null
);

public enum ActorType
{
    Primary,
    Supporting,
    Offstage
}

public record FlowStep(
    int StepNumber,
    string ActorOrSystem,
    string Action
);

public record AlternativeFlow(
    string Name,
    int BranchAtStep,
    string Condition,
    List<FlowStep> Steps,
    FlowReturn Return
);

public record ExceptionFlow(
    string Name,
    int OccursAtStep,
    string Condition,
    List<FlowStep> Steps,
    bool EndsInFailure
);

public record FlowReturn(
    FlowReturnType Type,
    int? ReturnToStep = null
);

public enum FlowReturnType
{
    ReturnToBasicFlow,
    EndUseCase,
    EndInFailure
}
```

### Use Case Slice Model

```csharp
public record UseCaseSlice
{
    public required string Id { get; init; }
    public required string UseCaseId { get; init; }
    public required string Name { get; init; }
    public required string ValueStatement { get; init; }

    public List<string> IncludedFlows { get; init; } = [];
    public List<string> ExcludedFlows { get; init; } = [];
    public List<AcceptanceCriterion> AcceptanceCriteria { get; init; } = [];
    public List<string> TestScenarios { get; init; } = [];

    public int? StoryPoints { get; init; }
    public SlicePriority Priority { get; init; }
    public SliceStatus Status { get; init; }
}

public record AcceptanceCriterion(
    string Given,
    string When,
    string Then
);

public enum SlicePriority
{
    MustHave,
    ShouldHave,
    CouldHave,
    WontHave
}

public enum SliceStatus
{
    Identified,
    Prepared,
    Analyzed,
    Implementing,
    Done
}
```

### Slice to User Story Converter

```csharp
public class SliceToStoryConverter
{
    public UserStory Convert(UseCaseSlice slice, UseCase useCase)
    {
        return new UserStory
        {
            Id = $"US-{slice.Id}",
            Title = slice.Name,
            Narrative = GenerateNarrative(slice, useCase),
            AcceptanceCriteria = slice.AcceptanceCriteria
                .Select(ac => $"Given {ac.Given}, When {ac.When}, Then {ac.Then}")
                .ToList(),
            Epic = useCase.Name,
            StoryPoints = slice.StoryPoints,
            Priority = MapPriority(slice.Priority)
        };
    }

    private string GenerateNarrative(UseCaseSlice slice, UseCase useCase)
    {
        return $"""
            As a {useCase.PrimaryActor.Name}
            I want to {ExtractAction(slice, useCase)}
            So that {useCase.Goal}
            """;
    }

    private string ExtractAction(UseCaseSlice slice, UseCase useCase)
    {
        // Extract the main action from included flows
        var mainFlow = slice.IncludedFlows.FirstOrDefault() ?? useCase.Name.ToLowerInvariant();
        return mainFlow.Replace("Basic flow", useCase.Name.ToLowerInvariant());
    }

    private UserStoryPriority MapPriority(SlicePriority priority) =>
        priority switch
        {
            SlicePriority.MustHave => UserStoryPriority.Critical,
            SlicePriority.ShouldHave => UserStoryPriority.High,
            SlicePriority.CouldHave => UserStoryPriority.Medium,
            SlicePriority.WontHave => UserStoryPriority.Low,
            _ => UserStoryPriority.Medium
        };
}

public record UserStory
{
    public required string Id { get; init; }
    public required string Title { get; init; }
    public required string Narrative { get; init; }
    public List<string> AcceptanceCriteria { get; init; } = [];
    public string? Epic { get; init; }
    public int? StoryPoints { get; init; }
    public UserStoryPriority Priority { get; init; }
}

public enum UserStoryPriority
{
    Critical,
    High,
    Medium,
    Low
}
```

## Best Practices

### Writing Good Use Cases

```yaml
naming:
  pattern: "Verb + Noun"
  good_examples:
    - "Place Order"
    - "Register Customer"
    - "Generate Report"
  bad_examples:
    - "Order" # No verb
    - "Customer Registration System" # System, not goal
    - "Handle Click" # Too low-level

flow_writing:
  guidelines:
    - "Write in active voice"
    - "Actor or System starts each step"
    - "One observable action per step"
    - "Number steps sequentially"
    - "Keep steps at same abstraction level"

  good_steps:
    - "1. Customer enters shipping address"
    - "2. System validates address format"
    - "3. System calculates shipping options"
    - "4. Customer selects shipping method"

  bad_steps:
    - "1. Click submit button" # Too detailed
    - "2. Stuff happens" # Too vague
    - "3. The system processes" # No outcome

level_selection:
  user_goal: "Primary level - use most often"
  summary: "For business process overview"
  subfunction: "For shared functionality (include targets)"
```

### Slicing Guidelines

```yaml
slice_sizing:
  ideal: "1-5 story points per slice"
  too_big: "Cannot complete in one iteration"
  too_small: "No incremental value delivered"

prioritization:
  value_first: "Basic flow slice before alternatives"
  risk_reduction: "Risky slices early for learning"
  dependency_aware: "Prerequisites before dependents"

coverage:
  minimal_viable: "Basic flow slice = MVP"
  enhanced: "Add high-value alternatives"
  complete: "All flows including exceptions"
```

## Integration with Other Skills

### Upstream

- **stakeholder-simulation** - Identify actors and goals
- **interview-conducting** - Elicit use case details
- **gap-analysis** - Find missing use cases

### Downstream

- **user-story-mapping** - Derive stories from slices
- **prioritization-methods** - Prioritize slices
- **business-rules-analysis** - Extract rules from flows

### Related Skills

- **ears-authoring** (spec-driven-development) - Convert to EARS format
- **gherkin-authoring** (spec-driven-development) - Convert to Gherkin scenarios

## Output Format

### Use Case Catalog

```yaml
use_case_catalog:
  project: "{Project Name}"
  version: "1.0"
  last_updated: "{ISO-8601}"

  actors:
    - name: "Customer"
      type: "primary"
      description: "End user purchasing products"

    - name: "Payment Gateway"
      type: "supporting"
      description: "External payment processor"

  use_cases:
    - id: "UC-ORD-001"
      name: "Place Order"
      actor: "Customer"
      goal: "Purchase products from catalog"
      level: "UserGoal"
      slices:
        - id: "UC-ORD-001-S01"
          name: "Basic Checkout"
          status: "Done"
          priority: "MustHave"

        - id: "UC-ORD-001-S02"
          name: "Guest Checkout"
          status: "Implementing"
          priority: "ShouldHave"

  coverage:
    total_use_cases: 12
    total_slices: 34
    slices_done: 18
    slices_remaining: 16
```

## References

For additional guidance:

- [Flow Writing Examples](references/flow-examples.md)
- [Slicing Patterns](references/slicing-patterns.md)

## Version History

- v1.0.0 (2025-12-26): Initial release - Use Case 2.0 skill

---

**Last Updated:** 2025-12-26
