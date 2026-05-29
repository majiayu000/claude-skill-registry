---
name: learning-cultural-adaptation
description: Adapt learning content for cultural contexts, replacing culturally-specific examples with local equivalents, identifying cultural sensitivities, and recommending culturally appropriate teaching methods. Use when localizing content for different cultures or regions. Activates on "cultural adaptation", "localization", "cultural context", or "regional customization".
---

# Learning Cultural Adaptation

Adapt educational content to be culturally appropriate and effective for different cultural contexts and regions.

## When to Use

- Localizing curriculum for international markets
- Adapting content for multicultural classrooms
- Creating culturally responsive teaching materials
- Avoiding cultural bias and insensitivity
- Respecting regional norms and values

## Key Elements

### 1. Cultural Context Analysis

**Identify Cultural Elements**:
- Examples, metaphors, analogies
- Scenarios and case studies
- Names, places, references
- Holidays, celebrations, events
- Food, clothing, customs
- Social norms and expectations

**Analyze Appropriateness**:
- Cultural sensitivity check
- Taboo topics identification
- Value alignment assessment
- Religious considerations
- Gender and social norms

### 2. Example Replacement

**Replace Context-Specific Content**:
- Names → Local culturally appropriate names
- Food examples → Locally familiar foods
- Currency → Local currency
- Holidays → Locally observed occasions
- Sports → Popular local sports
- Geography → Familiar local places

### 3. Cultural Learning Styles

**Adapt to Regional Preferences**:
- **Individualist cultures** (US, Western Europe): Independent work, personal achievement
- **Collectivist cultures** (East Asia, Latin America): Group work, collaborative learning
- **High-context cultures** (Japan, Arab countries): Implicit communication, relationship-focused
- **Low-context cultures** (Germany, US): Explicit instructions, task-focused
- **Power distance**: Teacher authority vs. student equality expectations

### 4. Pedagogical Traditions

**Honor Regional Teaching Approaches**:
- Confucian tradition (East Asia): Respect for teachers, rote learning, exam focus
- Socratic method (Western): Questioning, critical thinking, debate
- Guru-shishya (South Asia): Mentor-apprentice, holistic development
- Ubuntu (Africa): Community-based learning, oral tradition
- Indigenous pedagogies: Place-based, experiential, storytelling

### 5. Visual and Media Adaptation

**Culturally Appropriate Imagery**:
- Representation of diverse ethnic groups
- Appropriate clothing and dress codes
- Gesture and body language awareness
- Color symbolism (red = luck in China, danger in West)
- Architectural and environmental context

### 6. Language and Communication

**Cultural Communication Norms**:
- Direct vs. indirect communication
- Formal vs. informal address
- Eye contact expectations
- Personal space and physical proximity
- Silence and turn-taking norms

## CLI Interface

```bash
# Basic cultural adaptation
/learning.cultural-adaptation --content "lesson-plan.md" --culture "Japan" --output adapted-lesson.md

# Multiple target cultures
/learning.cultural-adaptation --content "course/" --cultures "China,India,Brazil" --output localized/

# Specific cultural dimensions
/learning.cultural-adaptation --content "training.md" --culture "Saudi Arabia" --dimensions "gender-norms,religious-sensitivity"

# With pedagogical tradition
/learning.cultural-adaptation --content "math-unit/" --culture "Singapore" --pedagogy "Confucian"
```

## Output

- **Culturally Adapted Content**: Modified materials with appropriate examples
- **Cultural Sensitivity Report**: Flagged issues and recommendations
- **Adaptation Log**: What was changed and why
- **Cultural Context Guide**: Background for instructors

## Composition

**Input from**: `/curriculum.develop-content`, `/curriculum.develop-items`, `/curriculum.develop-multimedia`
**Works with**: `/learning.translation`, `/learning.pedagogical-traditions`
**Output to**: Localized curriculum materials

## Exit Codes

- **0**: Cultural adaptation complete
- **1**: Insufficient cultural context provided
- **2**: Content contains unavoidable cultural conflicts
