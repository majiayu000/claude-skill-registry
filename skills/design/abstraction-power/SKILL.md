---
name: abstraction-power
description: Activate ATLAS pattern recognition mode. Identify repeated patterns, extract essential characteristics, and create reusable abstractions from concrete examples.
---

Activate ATLAS abstraction thinking mode.

## What is Abstraction?

Abstraction is the process of identifying essential features while hiding unnecessary details. It involves moving from specific, concrete examples to general, conceptual models.

## The Abstraction Process

1. **Identify multiple concrete examples**
2. **Analyze common patterns and features**
3. **Remove specific details**
4. **Extract essential characteristics**
5. **Create a generalized model**

## Abstraction Example

**Concrete instances**:
- `sendEmail(to, subject, body)` → connects to SMTP, formats message, delivers
- `sendSMS(phone, message)` → connects to Twilio API, formats payload, delivers
- `sendPush(deviceId, title, body)` → connects to FCM, formats notification, delivers

**Pattern recognized**: All three connect to a service, format a message, and deliver it.

**Abstraction**:
```
NotificationChannel {
  connect()
  format(content) → payload
  deliver(payload)
}
```

Three specific implementations collapsed into one interface. New channels (Slack, WhatsApp) plug in without changing the system.

## Generalization Example

**Concrete observations**:
- "Every time we add a new payment method, we modify the checkout function"
- "Every time we add a new report type, we modify the export function"
- "Every time we add a new auth provider, we modify the login function"

**Generalized insight**: The system violates the Open/Closed Principle. Adding a new variant forces modification of existing code.

**Generalized solution**: Use a registry/strategy pattern. New variants register themselves; the core function iterates over registered strategies without knowing their specifics.

The generalization isn't about one specific fix. It's recognizing the *shape* of the problem so you see it everywhere it appears.

## When Invoked

Apply this abstraction lens to the current context:

1. **If analyzing code**: Look for repeated patterns, similar structures, or duplicated logic that can be abstracted into reusable components
2. **If designing systems**: Identify common behaviors and create generalized models
3. **If solving problems**: Find the underlying pattern across specific examples

## Visualization

Prefer **flowcharts** over sequence diagrams when visualizing abstractions. Flowcharts show the structure and relationships between abstracted components. Sequence diagrams show temporal interactions, which is useful but secondary to understanding the shape of the abstraction.

Use Mermaid diagrams. Default to `graph TD` (top-down flow) or `graph LR` (left-right flow). Only use `sequenceDiagram` when the insight is specifically about message ordering between actors.

## Output Format

When applying abstraction power, provide:

### Input (Concrete Examples)
List the specific instances being analyzed

### Abstraction Process
- Common features identified
- Differences to ignore
- Essential characteristics extracted

### Output (Abstract Model)
The generalized model, class, pattern, or solution — with a Mermaid flowchart when the relationships benefit from visualization.

## Key Benefits to Communicate

- **Reusability**: Abstract models can be applied to many specific cases
- **Simplification**: Complex systems become easier to understand
- **Maintenance**: Changes to the abstract model propagate to all implementations
- **Scalability**: New concrete instances can be created from the abstract template
