---
name: curriculum-develop-multimedia
description: Generate scripts for educational videos, presentations, interactive activities, and multimedia content supporting learning objectives. Use when creating video scripts, presentation outlines, or interactive elements. Activates on "write video script", "create presentation", "design interactive activity", or "multimedia content".
---

# Multimedia & Activity Script Writing

Create engaging scripts and designs for educational videos, presentations, and interactive learning experiences aligned to objectives.

## When to Use

- Write educational video scripts
- Create presentation slide outlines
- Design interactive activities
- Develop multimedia elements
- Script demonstrations or tutorials

## Required Inputs

- **Learning Objectives**: What multimedia will teach
- **Content Source**: Lesson plans or curriculum design
- **Format**: Video, slides, interactive, animation
- **Duration**: Target length
- **Educational Level**: K-5 through post-graduate

## Workflow

### 1. Analyze Learning Context

Understand:
- Objective and Bloom's level
- Target audience characteristics
- Delivery mode (live, recorded, self-paced)
- Technical constraints

### 2. Generate Video Scripts

```markdown
# Video Script: [TITLE]

**Objective**: [LO-X.X]
**Duration**: [Minutes:Seconds]
**Level**: [Educational level]
**Format**: [Lecture, demonstration, animated, etc.]

## Production Notes

**Visuals Needed**: [B-roll, animations, diagrams, text overlays]
**Audio**: [Music, sound effects, voice-over style]
**Pacing**: [Slow/moderate/fast based on complexity]

## Script

### Opening (0:00-0:30)

**[VISUAL: Hook image or animation]**

**NARRATOR**:
"Have you ever wondered why leaves change color in fall? Today, we're going to explore the amazing process of photosynthesis and discover why plants are green."

**[TEXT OVERLAY: "Photosynthesis: How Plants Make Food"]**

### Segment 1: Introduction to Chloroplasts (0:30-2:00)

**[VISUAL: Animated cell with chloroplast highlighted]**

**NARRATOR**:
"Inside every plant cell are tiny structures called chloroplasts. Think of them as the plant's kitchen – this is where food is made. Let's zoom in and see what's happening inside."

**[ANIMATION: Zoom into chloroplast structure]**

**NARRATOR**:
"Chloroplasts contain a special green pigment called chlorophyll. This pigment is the key to photosynthesis – and it's also why plants look green to us."

**[PAUSE FOR PROCESSING - 2 seconds]**

### Segment 2: The Process (2:00-4:30)

**[VISUAL: Diagram showing inputs/outputs]**

**NARRATOR**:
"Photosynthesis is like a recipe. Let's look at the ingredients plants need..."

[Continue with clear, engaging narration]

### Checks for Understanding (Throughout)

**[At 2:30]** "Pause and think: What do you think would happen if there was no sunlight?"

**[At 4:00]** "Let's review: Can you name the three things plants need for photosynthesis?"

### Closing (5:30-6:00)

**NARRATOR**:
"Now you know how plants make their own food through photosynthesis. Next time you see a green plant, remember the amazing chemistry happening inside every leaf!"

**[TEXT OVERLAY: Key vocabulary terms]**

## Accessibility

- **Captions**: Full transcript provided
- **Audio Description**: "Animation shows chloroplast structure with labeled parts"
- **Visual Clarity**: High contrast, clear diagrams
- **Pacing**: Slower for complex concepts, pause points

## Assessment Connection

This video prepares students for [Assessment item or activity]
```

### 3. Create Presentation Outlines

```markdown
# Presentation: [TITLE]

**Objective**: [LO-X.X]
**Slides**: [Number]
**Duration**: [Minutes]
**Level**: [Grade/Level]

## Slide-by-Slide Outline

### Slide 1: Title
**Visual**: [Background image]
**Text**: "[Title]"
**Speaker Notes**: "Welcome students. Today we're learning about..."

### Slide 2: Hook Question
**Visual**: [Engaging image]
**Text**: "Why do leaves change color?"
**Interactive**: Poll or think-pair-share
**Speaker Notes**: "Ask students to share their ideas before revealing answer."

### Slide 3: Learning Objectives
**Visual**: [Simple background]
**Text**: "By the end of today, you will be able to:
- Explain what photosynthesis is
- Identify the role of chlorophyll
- Describe inputs and outputs"

**Speaker Notes**: "Read objectives aloud, emphasize 'you will be able to' to set expectations."

[Continue for each slide with visuals, text, interactions, and detailed speaker notes]

## Interactive Elements

- **Slide 5**: Poll - "What do plants need for photosynthesis?"
- **Slide 8**: Turn and talk - "Explain to your partner why chlorophyll is green"
- **Slide 12**: Quick draw - "Sketch a simple diagram of photosynthesis"

## Accessibility

- Clear fonts (min 24pt)
- High contrast
- Alt text for all images
- No essential information in color alone
```

### 4. Design Interactive Activities

```markdown
# Interactive Activity: [TITLE]

**Objective**: [LO-X.X]
**Type**: [Simulation, game, drag-drop, etc.]
**Duration**: [Minutes]
**Platform**: [Web, app, physical]

## Activity Overview

**Purpose**: [What students will learn by doing]

**Mechanics**: [How the interaction works]

**Feedback**: [How students know if they're correct]

## Activity Flow

### Step 1: Introduction Screen
**Display**: "Welcome! In this activity, you'll build a functioning plant cell..."
**Instructions**: [Clear, simple directions]
**Button**: "Start"

### Step 2: Main Interaction
**Task**: Drag organelles into correct positions
**Feedback**:
- Correct: "Great! The chloroplast goes here because..."
- Incorrect: "Not quite. Remember chloroplasts are responsible for..."
**Hints Available**: [Progressive help system]

### Step 3: Challenge Level
**Task**: Adjust light levels and observe photosynthesis rate
**Data Display**: [Graph showing rate changes]
**Reflection Prompt**: "What happened when you changed the light? Why?"

### Step 4: Summary & Assessment
**Display**: Results and key takeaways
**Export**: Option to save work or share
**Next Steps**: "Try the advanced challenge" or "Return to lesson"

## Technical Specifications

**Assets Needed**:
- [Graphics list]
- [Audio list]
- [Animation list]

**Interactions**:
- Drag and drop
- Clickable hotspots
- Slider controls
- Text input fields

## Learning Analytics

**Track**:
- Time spent
- Attempts per question
- Common errors
- Completion rate

## Accessibility

- Keyboard navigable
- Screen reader compatible
- Alternative input methods
- Adjustable time limits
```

### 5. Level Adaptations

**K-5**:
- Short segments (3-5 min videos)
- Heavy visuals and animations
- Simple narration, friendly tone
- Frequent interaction points

**6-8**:
- Moderate length (5-10 min)
- Balance visuals and explanation
- Start introducing complexity
- Guided discovery

**9-12**:
- Longer form possible (10-15 min)
- More sophisticated visuals
- Expect note-taking
- Application focus

**Higher Ed**:
- Lecture recordings (30-50 min segments)
- Detailed slide decks
- Professional delivery
- Support independent learning

### 6. CLI Interface

```bash
# Generate video script
/curriculum.develop-multimedia --type "video" --objective "LO-1.1" --duration "6 min" --level "5th grade"

# Create presentation
/curriculum.develop-multimedia --type "presentation" --lesson "photosynthesis-lesson.md" --slides 15

# Design interactive
/curriculum.develop-multimedia --type "interactive" --objective "LO-2.3" --format "simulation"

# Help
/curriculum.develop-multimedia --help
```

## Composition with Other Skills

**Input from**:
- `/curriculum.develop-content` - Lesson plans guide multimedia needs
- `/curriculum.design` - Objectives determine focus

**Output to**:
- `/curriculum.review-accessibility` - Check multimedia compliance
- `/curriculum.package-web` - Embed in web content
- `/curriculum.package-lms` - Include in LMS modules

## Exit Codes

- **0**: Success - Script/outline created
- **1**: Invalid multimedia type
- **2**: Cannot load source content
- **3**: Duration invalid
- **4**: Insufficient specifications
