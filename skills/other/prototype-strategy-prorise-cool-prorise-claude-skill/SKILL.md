---
name: prototype-strategy
description: Plan prototyping approach - fidelity levels, tool selection, prototype types, testing strategies, and design-to-development handoff.
allowed-tools: Read, Glob, Grep, Task
---

# Prototype Strategy

Plan and execute prototyping approaches from paper sketches to high-fidelity interactive prototypes.

## When to Use This Skill

Use this skill when:

- **Prototype Strategy tasks** - Working on plan prototyping approach - fidelity levels, tool selection, prototype types, testing strategies, and design-to-development handoff
- **Planning or design** - Need guidance on Prototype Strategy approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Skill Loading First

Before answering ANY prototyping question:

2. Use established prototyping methodology sources
3. Base all guidance on validated design practices

## Fidelity Spectrum

### Fidelity Levels

| Level | Characteristics | Best For |
|-------|-----------------|----------|
| **Low (Lo-Fi)** | Sketchy, grayscale, static | Early exploration, concept testing |
| **Medium (Mid-Fi)** | Structured, placeholder content, limited interaction | Information architecture, flow validation |
| **High (Hi-Fi)** | Polished, real content, full interaction | Usability testing, stakeholder sign-off |

### Fidelity Dimensions

| Dimension | Low | Medium | High |
|-----------|-----|--------|------|
| **Visual** | Sketchy, boxes | Wireframes, grays | Pixel-perfect, branded |
| **Content** | Lorem ipsum | Representative | Real content |
| **Interaction** | Static/paper | Click-through | Micro-interactions |
| **Breadth** | Key screens | Critical flows | Full experience |

## Prototype Types

### By Purpose

| Type | Purpose | Fidelity | Tools |
|------|---------|----------|-------|
| **Concept Sketch** | Generate ideas | Very low | Paper, whiteboard |
| **Paper Prototype** | Quick flow testing | Low | Paper, Post-its |
| **Wireframe** | Layout validation | Low-Medium | Figma, Balsamiq |
| **Clickable Mockup** | Flow testing | Medium | Figma, Sketch |
| **Interactive Prototype** | Usability testing | High | Figma, Principle |
| **Coded Prototype** | Technical feasibility | High | HTML/CSS, React |
| **Wizard of Oz** | Simulate complex behavior | Varies | Mixed |

### Decision Matrix

```text
What are you testing?
├── General concept/direction
│   └── Paper prototypes, sketches (Low)
├── Information architecture / navigation
│   └── Wireframes, tree tests (Low-Medium)
├── Specific interactions / usability
│   └── Interactive prototype (Medium-High)
├── Visual design / brand
│   └── High-fidelity mockups (High)
├── Technical feasibility
│   └── Coded prototype (High)
└── AI/complex behaviors
    └── Wizard of Oz prototype (Varies)
```

## Prototyping Approaches

### Paper Prototyping

**When:** Early concept exploration, limited resources, rapid iteration

```markdown
## Paper Prototype Kit

### Materials
- Index cards or paper (one per screen)
- Markers/pens
- Sticky notes (for overlays, error states)
- Scissors (for buttons that "move")
- Clear sheet (for tracing overlays)

### Running a Paper Prototype Test
1. Explain: "This is rough - we're testing the concept, not the drawing"
2. Lay out starting screen
3. Give user a task
4. User "clicks" by pointing
5. Swap/update papers to show response
6. Observe, take notes
7. Ask follow-up questions
```

### Digital Low-Fidelity

**When:** Remote testing, slightly more polish needed, version control

```csharp
// Configuration for low-fidelity prototype
public class LoFiPrototypeSpec
{
    public required string ProjectName { get; init; }
    public required List<ScreenSpec> Screens { get; init; }
    public required List<FlowSpec> Flows { get; init; }

    public LoFiGuidelines Style { get; init; } = new()
    {
        UseGrayscale = true,
        ShowPlaceholderContent = true,
        IncludeInteractions = false,
        AnnotateDecisions = true
    };
}

public class ScreenSpec
{
    public required string Name { get; init; }
    public required string Purpose { get; init; }
    public required List<string> KeyElements { get; init; }
    public string? Notes { get; init; }
}

public class FlowSpec
{
    public required string Name { get; init; }
    public required List<string> ScreenSequence { get; init; }
    public required string UserGoal { get; init; }
}
```

### High-Fidelity Interactive

**When:** Usability testing, stakeholder demos, developer handoff

```csharp
public class HiFiPrototypeSpec
{
    public required string ProjectName { get; init; }
    public required string DesignSystemLink { get; init; }
    public required List<ScreenSpec> Screens { get; init; }
    public required List<InteractionSpec> Interactions { get; init; }
    public required List<StateSpec> States { get; init; }

    public HiFiGuidelines Style { get; init; } = new()
    {
        UseRealContent = true,
        IncludeAllStates = true,
        AddMicroInteractions = true,
        AnnotateForDev = true
    };
}

public class InteractionSpec
{
    public required string Trigger { get; init; }
    public required string Action { get; init; }
    public required string Target { get; init; }
    public AnimationType? Animation { get; init; }
    public TimeSpan? Delay { get; init; }
}

public enum AnimationType
{
    None,
    Fade,
    Slide,
    Scale,
    SmartAnimate,
    Custom
}

public class StateSpec
{
    public required string Component { get; init; }
    public required List<string> States { get; init; } // Default, Hover, Active, Disabled, etc.
}
```

### Coded Prototype

**When:** Complex interactions, data-driven UI, technical validation

```csharp
// Blazor prototype component
@page "/prototype/checkout"
@inject PrototypeDataService Data

<div class="prototype-container">
    <PrototypeBanner>
        This is a prototype - not the real product
    </PrototypeBanner>

    @switch (CurrentStep)
    {
        case CheckoutStep.Cart:
            <CartView
                Items="@cartItems"
                OnProceed="() => CurrentStep = CheckoutStep.Shipping" />
            break;

        case CheckoutStep.Shipping:
            <ShippingForm
                OnBack="() => CurrentStep = CheckoutStep.Cart"
                OnProceed="HandleShippingComplete" />
            break;

        case CheckoutStep.Payment:
            <PaymentForm
                OnBack="() => CurrentStep = CheckoutStep.Shipping"
                OnProceed="HandlePaymentComplete" />
            break;

        case CheckoutStep.Confirmation:
            <OrderConfirmation Order="@confirmedOrder" />
            break;
    }

    <PrototypeControls>
        <button @onclick="ResetPrototype">Reset</button>
        <button @onclick="() => ShowNotes = !ShowNotes">
            @(ShowNotes ? "Hide" : "Show") Notes
        </button>
    </PrototypeControls>

    @if (ShowNotes)
    {
        <PrototypeNotes Step="@CurrentStep" />
    }
</div>

@code {
    private CheckoutStep CurrentStep { get; set; } = CheckoutStep.Cart;
    private List<CartItem> cartItems = [];
    private Order? confirmedOrder;
    private bool ShowNotes { get; set; }

    protected override async Task OnInitializedAsync()
    {
        cartItems = await Data.GetSampleCartItems();
    }

    private void ResetPrototype()
    {
        CurrentStep = CheckoutStep.Cart;
        confirmedOrder = null;
    }
}
```

### Wizard of Oz Prototyping

**When:** AI features, voice interfaces, complex personalization

```csharp
public class WizardOfOzSetup
{
    public required string FeatureDescription { get; init; }
    public required List<ScenarioScript> Scenarios { get; init; }
    public required WizardControls Controls { get; init; }

    public class ScenarioScript
    {
        public required string UserAction { get; init; }
        public required List<WizardResponse> PossibleResponses { get; init; }
        public string? DefaultResponse { get; init; }
    }

    public class WizardResponse
    {
        public required string Label { get; init; }
        public required string Response { get; init; }
        public TimeSpan SimulatedDelay { get; init; } = TimeSpan.FromSeconds(1);
    }

    public class WizardControls
    {
        public required string TriggerHotkey { get; init; }
        public required string ResponsePanel { get; init; }
        public bool SimulateTyping { get; init; } = true;
        public bool AddRandomDelay { get; init; } = true;
    }
}
```

## Tool Selection

### Tool Comparison

| Tool | Fidelity | Collaboration | Dev Handoff | Best For |
|------|----------|---------------|-------------|----------|
| **Figma** | All | Excellent | Excellent | Team design |
| **Sketch** | Medium-High | Good (w/plugins) | Good | Mac teams |
| **Adobe XD** | Medium-High | Good | Good | Adobe ecosystem |
| **Framer** | High | Good | Limited | Complex interactions |
| **InVision** | Medium | Excellent | Good | Stakeholder feedback |
| **Balsamiq** | Low | Basic | N/A | Quick wireframes |
| **Axure** | All | Good | Detailed | Complex specs |
| **Principle** | High | Limited | Limited | Micro-interactions |
| **ProtoPie** | High | Good | Limited | Multi-device |

### Selection Criteria

```csharp
public class ToolEvaluation
{
    public required string ToolName { get; init; }
    public required Dictionary<string, int> Scores { get; init; } // 1-5

    public static readonly string[] Criteria =
    [
        "FidelityRange",      // Can handle low to high
        "Collaboration",      // Real-time co-editing
        "ComponentSystem",    // Reusable components
        "InteractionDepth",   // Animation, logic
        "DevHandoff",         // Specs, assets export
        "LearningCurve",      // Ease of adoption
        "TeamExisting",       // Team already knows it
        "Cost",               // Budget fit
        "Integration"         // Works with other tools
    ];

    public decimal OverallScore => Scores.Values.Average();
}
```

## Fidelity Progression

### Typical Progression

```text
Week 1-2: Discovery
├── Paper sketches
├── Concept exploration
└── Stakeholder sketches

Week 3-4: Definition
├── Wireframes
├── Information architecture
└── Content strategy

Week 5-6: Design
├── Visual design
├── Component creation
└── Style guide

Week 7-8: Prototype
├── Interactive flows
├── Micro-interactions
└── Usability testing

Week 9+: Handoff
├── Final specs
├── Asset export
└── Developer collaboration
```

### When to Skip Fidelity Levels

| Skip Lo-Fi When | Skip Mid-Fi When | Go Straight to Code When |
|-----------------|------------------|--------------------------|
| Clear requirements | Design system exists | Technical uncertainty |
| Existing patterns | Flows are known | Performance critical |
| Time pressure | Team is aligned | Highly data-driven |
| Small changes | Visual validation needed | Developer preference |

## Testing with Prototypes

### Matching Fidelity to Test Goals

| Test Goal | Recommended Fidelity |
|-----------|---------------------|
| Concept validation | Low |
| Navigation/IA | Low-Medium |
| Task completion | Medium |
| Aesthetic reactions | High |
| Micro-interactions | High |
| Accessibility | Medium-High |
| Emotional response | High |

### Prototype Testing Considerations

```csharp
public class PrototypeTestPlan
{
    public required string PrototypeUrl { get; init; }
    public required PrototypeFidelity Fidelity { get; init; }
    public required List<TestTask> Tasks { get; init; }
    public required List<PrototypeLimitation> Limitations { get; init; }

    public string IntroductionScript => Fidelity switch
    {
        PrototypeFidelity.Low => """
            This is an early concept - it's rough on purpose.
            We're testing ideas, not visual design.
            Some things won't work yet - just tell me what you'd expect.
            """,

        PrototypeFidelity.Medium => """
            This is a work-in-progress design.
            It's clickable but not everything will work.
            Focus on whether this flow makes sense to you.
            """,

        PrototypeFidelity.High => """
            This is close to what the final product will look like.
            Try to use it as if it were real.
            Let me know if anything seems off or confusing.
            """,

        _ => throw new ArgumentOutOfRangeException()
    };
}

public record PrototypeLimitation(
    string What,
    string Workaround,
    string ExplainToUser
);
```

### Briefing Participants

**Always clarify:**

- What's working vs. not working
- That you're testing the design, not them
- Permission to think aloud
- That rough appearance is intentional (if low-fi)

## Design-to-Development Handoff

### Handoff Checklist

```markdown
## Prototype Handoff Checklist

### Design Specs
- [ ] All screens exported
- [ ] Component specs documented
- [ ] Spacing and sizing annotated
- [ ] Typography specs included
- [ ] Color values specified
- [ ] Breakpoints defined

### Interactions
- [ ] State changes documented
- [ ] Animations specified (timing, easing)
- [ ] Error states included
- [ ] Loading states defined
- [ ] Empty states designed

### Assets
- [ ] Icons exported (SVG)
- [ ] Images optimized
- [ ] Fonts specified/included
- [ ] Design tokens exported

### Documentation
- [ ] User flows documented
- [ ] Edge cases noted
- [ ] Accessibility requirements
- [ ] Copy/content finalized
- [ ] Component behavior specs

### Collaboration
- [ ] Figma/design file shared
- [ ] Questions channel established
- [ ] Review meetings scheduled
- [ ] Iteration process defined
```

### Handoff Annotation Patterns

```csharp
public class HandoffAnnotation
{
    public required AnnotationType Type { get; init; }
    public required string Description { get; init; }
    public Position? ScreenPosition { get; init; }
    public string? LinkedComponent { get; init; }
    public Dictionary<string, string>? Properties { get; init; }
}

public enum AnnotationType
{
    Spacing,
    Behavior,
    Animation,
    Condition,
    EdgeCase,
    Accessibility,
    ResponsiveBreakpoint,
    DeveloperNote
}

// Example annotations
var annotations = new List<HandoffAnnotation>
{
    new()
    {
        Type = AnnotationType.Behavior,
        Description = "Button disabled until all required fields valid",
        LinkedComponent = "SubmitButton"
    },
    new()
    {
        Type = AnnotationType.Animation,
        Description = "Slide in from right, 300ms ease-out",
        Properties = new()
        {
            ["duration"] = "300ms",
            ["easing"] = "ease-out",
            ["direction"] = "right"
        }
    },
    new()
    {
        Type = AnnotationType.EdgeCase,
        Description = "If list > 100 items, show 'Load More' button"
    }
};
```

## Prototype Documentation

### Prototype Brief Template

```markdown
# Prototype Brief: [Feature Name]

## Objective
What are we trying to learn or validate?

## Scope
- **Flows included:** [List of user flows]
- **Flows excluded:** [What's not in prototype]
- **Fidelity level:** [Low/Medium/High]

## Target Users
Who will test this? [Persona or criteria]

## Key Scenarios

### Scenario 1: [Name]
**Setup:** [Starting conditions]
**Task:** [What user tries to accomplish]
**Success:** [How we know it worked]

### Scenario 2: [Name]
[Continue...]

## Prototype Links
- **Main prototype:** [URL]
- **Design file:** [URL]
- **Assets:** [URL]

## Known Limitations
| What | Why | Workaround |
|------|-----|------------|
| [Feature] | [Reason] | [How to handle] |

## Test Plan
- **Method:** [Moderated/unmoderated]
- **Participants:** [Number]
- **Duration:** [Per session]
- **Schedule:** [Dates]

## Questions to Answer
1. [Research question 1]
2. [Research question 2]
3. [Research question 3]

## Success Criteria
- [Metric/observation that indicates success]
- [Metric/observation that indicates success]
```

## Checklist: Prototype Planning

### Strategy

- [ ] Goals defined (what to learn)
- [ ] Fidelity level selected
- [ ] Tool chosen
- [ ] Scope determined
- [ ] Timeline set

### Creation

- [ ] Key screens identified
- [ ] Critical flows mapped
- [ ] States defined (error, empty, loading)
- [ ] Interactions specified
- [ ] Edge cases considered

### Testing Prep

- [ ] Test tasks written
- [ ] Limitations documented
- [ ] Participant intro script ready
- [ ] Recording setup tested
- [ ] Success criteria defined

### Handoff

- [ ] Specs annotated
- [ ] Assets exported
- [ ] Design tokens ready
- [ ] Developer walkthrough scheduled
- [ ] Feedback process defined

## Related Skills

- `usability-testing` - Testing the prototype
- `design-system-planning` - Reusable components
- `information-architecture` - Navigation prototyping
- `accessibility-planning` - Accessible prototypes
