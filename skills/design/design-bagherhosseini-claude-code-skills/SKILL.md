---
name: design
description: Guidance for designing ethically humane digital products through patterns focused on user well-being. This skill should be used when building user interfaces, applications, or digital experiences to ensure they respect users' time, attention, privacy, and autonomy. Apply these principles during design reviews, feature development, and when evaluating existing products for humane design patterns.
---

# Humane Design Skill

This skill provides guidance for designing ethically humane digital products through patterns focused on user well-being. It draws from the Humane by Design framework and related ethical design principles.

## Core Philosophy

Technology should augment human intellect and enhance abilities without dictating the rhythm of our lives. Design with respect for users' time, attention, privacy, and overall digital well-being. Prioritize empowerment over addiction, transparency over manipulation, and intentionality over convenience.

## The Seven Principles

### 1. Empowering

Ensure products center on the value they provide to people over the revenue they can generate.

**Best Practices:**

- **In Control**: Give people the control they need to manage the algorithms that shape their experiences
- **Privacy and Anonymity**: Give people the control they need to manage privacy and anonymity
- **Invisible Until Needed**: Technology should augment human ability without disrupting lives. The most profound technologies disappear, weaving into the fabric of everyday life
- **Promote Awareness**: Promote usage awareness to encourage healthier digital habits (e.g., screen time features)
- **Human in the Loop**: Balance trust and efficiency by helping users understand and trust AI decisions. Place humans in the AI-decision loop and empower them to steer algorithms

### 2. Finite

Maximize the overall quality of time spent by bounding the experience and prioritizing meaningful and relevant content.

**Best Practices:**

- **All Caught Up**: Use an indicator to inform users when they are caught up to help curb zombie scrolling
- **Load More**: Use explicit "load more" buttons instead of infinite scrolling to give users control
- **Autoplay Off**: Require an explicit action before playing videos to prevent harmful binge watching. Autoplay prevents users from making conscious choices

### 3. Inclusive

Enable and draw on the full range of human diversity.

**Best Practices:**

- **Build Diverse Teams**: Homogeneous teams create narrow designs; diverse teams create inclusive designs
- **Design for Disabilities First**: Solutions for the disabled often result in features everyone can benefit from
- **Give Control**: Provide users control so they can access and interact with content in ways they prefer. Never disable platform features like zoom, contrast, and font size settings. Enable turning off parallax scrolling, animations, and infinite scrolling

### 4. Intentional

Use friction to prevent abuse, protect privacy, steer people towards healthier digital habits, and consider long-term consequences over short-term gain.

**Best Practices:**

- **Manual Speed Bumps**: Use confirmation dialogs to prevent errors, avoid unintentional actions, and promote critical thought
- **Algorithmic Speed Bumps**: Implement algorithms that slow down unintentional consequences and deter bad actors
- **Embrace Positive Friction**: The right amount of friction results in more intentional choices. Not everything should be "frictionless"
- **Encourage Moderation**: Provide tools to help users keep viewing habits in check

**Designing with Intentionality:**

- Use **second-order thinking**: Ask "and then what?" repeatedly to identify consequences for both direct and indirect users
- Apply **Futures Wheel**: Map direct consequences and indirect consequences of those consequences
- Run **Pre-mortems**: Imagine the project has failed and work backward to identify and prevent risks

### 5. Resilient

Focus on the well-being of the most vulnerable and anticipate the potential for abuse.

**Best Practices:**

- **Enable Content Control**: Enable people to control who has access to their information and shared content
- **Enable Community Moderation**: Let people protect themselves against malicious intent
- **Focus on Edge Cases**: Design for a breadth of scenarios, especially those beyond MVP. Consider how products might be weaponized against vulnerable groups
- **Balance Data with Research**: Quantitative data tells what people are doing, not why. Combine with qualitative research

### 6. Respectful

Prioritize people's time, attention, and overall digital well-being.

**Best Practices:**

- **Align Delivery with Urgency**: Match notification delivery method with actual importance to minimize distraction
- **Allow for Personalization**: Let users customize from whom, when, and how they receive notifications
- **Include Full Text**: Include full text of comments and messages in email notifications to prevent unnecessary app opens
- **Respect and Adapt to Context**: Just as humans understand when and how to communicate appropriately, technology should respect and adapt to user context

### 7. Transparent

Be clear about intentions, honest in actions, and free of dark patterns.

**Best Practices:**

- **Right to Know**: Users have a right to know exactly what they are signing up for. Make it clear and specific
- **Data Transparency**: Communicate exactly what data is being collected and why
- **Access to Data**: Give users easy access to the data being collected on them
- **The Right to be Forgotten**: Provide the ability to permanently delete data and ensure it's easy to find
- **Avoid Misdirection**: Follow usability best practices, maintain consistent UI, ensure links and buttons are clear and recognizable, never disguise ads as content
- **Easy Exit**: Ensure users can easily unsubscribe or delete their account

## Key Concepts

### The Cost of Personalization

Personalization comes with trade-offs beyond privacy:

- **Filter Bubbles**: Algorithms can reinforce pre-existing beliefs and biases
- **Attention Capture**: Platforms use personalization to keep users captive, not to provide value
- **Erosion of Agency**: When algorithms make autonomous decisions, visible options are hidden and personal agency is lost
- **The Personalization Paradox**: Users want convenience without sacrificing privacy - balance is essential

**Counter-measures:**

- Promote usage awareness to encourage healthier digital habits
- Provide tools for users to oversee and regulate algorithms affecting their experience
- Consider reducing screen time through low-interface, utility-focused design
- Empower users to co-create with algorithms rather than being passively shaped by them

### Embrace Friction

Reject the obsession with "frictionless" design:

- Positive friction helps prevent errors and promotes critical thought
- Friction can protect privacy and security
- Speed bumps (manual and algorithmic) deter bad actors
- Some inconvenience is valuable for creating intentional choices

### Human in the Loop

For AI-based systems:

- Balance trust and efficiency through transparency
- Help users understand and trust AI decisions
- Empower users with the ability to steer algorithms
- Enable fine-tuning of algorithmic recommendations
- Build stronger human-machine relationships through collaboration, not automation

### Invisible Until Needed (Calm Technology)

Technology should:

- Augment human ability without disrupting lives
- Disappear and weave into the fabric of everyday life
- Not demand constant attention
- Recede to the background when not needed
- Respect that distraction is ever-present and meaningful connection is rare

## Dark Patterns to Avoid

- **Misdirection**: Using UI to direct attention away from important information
- **Disguised Ads**: Making advertisements look like content or navigation
- **Forced Continuity**: Making it difficult to cancel subscriptions
- **Roach Motel**: Making it easy to get into a situation but hard to get out
- **Privacy Zuckering**: Confusing users into sharing more than intended
- **Confirm Shaming**: Using guilt to steer users toward choices
- **Infinite Scrolling Without Bounds**: Eliminating any reason to pause or leave
- **Random Reinforcement Loops**: Using intermittent rewards to create addiction

## Design Review Checklist

When reviewing designs, ask:

1. Does this respect the user's time and attention?
2. Can users easily understand and control what's happening?
3. Have consequences for indirect users (beyond direct users) been considered?
4. Could this feature be abused or weaponized?
5. Is there appropriate friction to prevent unintended actions?
6. Is data collection transparent and necessary?
7. Can users easily opt out or delete their data?
8. Does this work for users with disabilities?
9. Does this promote healthy usage patterns?
10. Would I be comfortable with my family using this?

## Implementation Workflow

To apply humane design principles:

1. **Research**: Understand all user types, including indirect users affected by the product
2. **Anticipate**: Use second-order thinking and futures wheel to identify consequences
3. **Protect**: Design for edge cases and vulnerable users from the start
4. **Empower**: Give users control over their experience, data, and attention
5. **Bound**: Create natural stopping points and respect finite time
6. **Verify**: Run pre-mortems and test with diverse users
7. **Iterate**: Continuously evaluate products for unintended consequences

## Further Reading

For detailed guidance on specific principles, consult the `references/` directory:

- `principles.md` - Deep dive into each principle with examples
- `dark-patterns.md` - Comprehensive list of manipulative patterns to avoid
- `design-methods.md` - Detailed methodologies for intentional design
