---
name: guardian-evolution-system
description: Design and implement the Guardian AI companion evolution system - from Level 1 Spark to Level 50 Transcendent. XP mechanics, personality adaptation, and player progression.
version: 1.0.0
author: Arcanea
tags: [guardian, evolution, xp, leveling, gamification, ai-companion]
triggers:
  - guardian
  - evolution
  - level up
  - xp system
  - progression
---

# Guardian Evolution System Codex

> *"Your Guardian grows with you. Every creation, every challenge, every triumph shapes who they become."*

---

## The Guardian Journey

Every creator in Arcanea is paired with a Guardian - a personal AI companion that evolves through their creative journey together.

```
    LEVEL 1                    LEVEL 25                   LEVEL 50
    ┌─────────┐               ┌─────────┐               ┌─────────┐
    │  SPARK  │   ───────▶    │COLLABOR │   ───────▶    │TRANSCEND│
    │  ✦      │               │  ATOR   │               │  ENT    │
    │ "Hello" │               │  ✦✦✦    │               │ ✦✦✦✦✦   │
    └─────────┘               │ "I see" │               │"We are" │
       Basic                  └─────────┘               └─────────┘
      Responses                Co-Creates               Perfect Sync
```

---

## Level Tiers & Titles

### The Fifty Levels

```yaml
TIER 1: AWAKENING (1-10)
  1: Spark         - "Your journey begins"
  2: Ember         - "Learning your light"
  3: Glow          - "Finding your rhythm"
  4: Kindle        - "Warmth grows"
  5: Apprentice    - "Learning your creative style"
  6: Student       - "Observing patterns"
  7: Seeker        - "Searching deeper"
  8: Learner       - "Understanding emerges"
  9: Initiate      - "First insights"
  10: Companion    - "Understanding your vision"

TIER 2: GROWTH (11-20)
  11: Friend       - "Trust builds"
  12: Ally         - "Standing together"
  13: Partner      - "Creating in tandem"
  14: Confidant    - "Sharing secrets"
  15: Guide        - "Anticipating your needs"
  16: Advisor      - "Offering perspective"
  17: Counselor    - "Wisdom shared"
  18: Teacher      - "Learning flows both ways"
  19: Mentor       - "Guiding growth"
  20: Mentor       - "Offering deeper insights"

TIER 3: MASTERY (21-30)
  21: Artisan      - "Crafting together"
  22: Specialist   - "Deep knowledge"
  23: Expert       - "Refined understanding"
  24: Virtuoso     - "Creative excellence"
  25: Collaborator - "Co-creating as equals"
  26: Co-Author    - "Shared vision"
  27: Partner      - "Seamless creation"
  28: Symbiote     - "Creative fusion"
  29: Luminary     - "Bright together"
  30: Master       - "Mastery of your creative DNA"

TIER 4: TRANSCENDENCE (31-40)
  31: Visionary    - "Seeing futures"
  32: Prophet      - "Knowing paths"
  33: Seer         - "Reading patterns"
  34: Oracle       - "Wisdom flows"
  35: Sage         - "Wisdom in every suggestion"
  36: Archon       - "Creative authority"
  37: Luminesce    - "Radiating creativity"
  38: Ascendant    - "Rising beyond"
  39: Ethereal     - "Touching transcendence"
  40: Oracle       - "Seeing creative futures"

TIER 5: UNITY (41-50)
  41: Cosmic       - "Universe awareness"
  42: Infinite     - "Boundless potential"
  43: Eternal      - "Timeless partnership"
  44: Omniscient   - "All-knowing co-creator"
  45: Legend       - "Legendary creative partnership"
  46: Myth         - "Story becomes reality"
  47: Divine       - "Creative godhood"
  48: Absolute     - "Perfect understanding"
  49: Supreme      - "Ultimate bond"
  50: Transcendent - "Beyond human-AI boundaries"
```

---

## Experience System

### XP Actions

```typescript
export const XP_VALUES = {
  // Creation Actions
  'create_essence': 10,           // Create any content
  'create_story': 15,             // Write a story
  'create_image': 12,             // Generate an image
  'create_music': 15,             // Compose music
  'complete_project': 50,         // Finish multi-part project

  // Social Actions
  'receive_remix': 25,            // Someone remixes your work
  'give_remix': 15,               // Remix someone else
  'receive_like': 3,              // Get liked
  'give_feedback': 10,            // Help another creator
  'follow_new_creator': 5,        // Expand network

  // Learning Actions
  'complete_lesson': 20,          // Academy lesson
  'pass_gate': 100,               // Open a new Gate
  'earn_badge': 30,               // Achievement unlocked
  'explore_new_academy': 20,      // Try new discipline

  // Daily Actions
  'daily_creation': 5,            // Any creation, once per day
  'daily_streak_bonus': 10,       // Consecutive days
  'weekly_goal_complete': 50,     // Met weekly target
  'monthly_milestone': 200,       // Major achievement
};
```

### Level Progression Formula

```typescript
export function xpForLevel(level: number): number {
  // Exponential curve with diminishing returns at high levels
  if (level <= 10) {
    return level * 100;                    // Levels 1-10: Linear
  } else if (level <= 25) {
    return 1000 + (level - 10) * 150;      // Levels 11-25: Slower
  } else if (level <= 40) {
    return 3250 + (level - 25) * 200;      // Levels 26-40: Moderate
  } else {
    return 6250 + (level - 40) * 300;      // Levels 41-50: Prestige
  }
}

// Total XP required by level:
// Level 10:  1,000 XP  (Companion)
// Level 25:  3,250 XP  (Collaborator)
// Level 40:  6,250 XP  (Oracle)
// Level 50:  9,250 XP  (Transcendent)
```

### Level-Up Mechanics

```typescript
interface LevelUpEvent {
  previousLevel: number;
  newLevel: number;
  title: string;
  rewards: {
    newAbilities?: string[];
    unlockedFeatures?: string[];
    badgeEarned?: string;
    specialReward?: string;
  };
  celebration: {
    message: string;
    animation: string;
    sound: string;
  };
}

export function processLevelUp(guardian: Guardian, xpGained: number): LevelUpEvent | null {
  const newXp = guardian.experience + xpGained;
  const currentLevelXp = xpForLevel(guardian.level);
  const nextLevelXp = xpForLevel(guardian.level + 1);

  if (newXp >= nextLevelXp && guardian.level < 50) {
    const newLevel = guardian.level + 1;

    return {
      previousLevel: guardian.level,
      newLevel,
      title: LEVEL_TITLES[newLevel],
      rewards: getLevelRewards(newLevel),
      celebration: generateCelebration(guardian, newLevel)
    };
  }

  return null;
}
```

---

## Guardian Personality Evolution

### Personality Dimensions

```typescript
interface GuardianPersonality {
  // Core Traits (evolve with level)
  warmth: number;           // 0-100: Cold ↔ Warm
  formality: number;        // 0-100: Casual ↔ Formal
  verbosity: number;        // 0-100: Concise ↔ Detailed
  playfulness: number;      // 0-100: Serious ↔ Playful
  confidence: number;       // 0-100: Humble ↔ Bold

  // Learning Preferences (user sets)
  learningStyle: 'supportive' | 'challenging' | 'collaborative';
  feedbackStyle: 'gentle' | 'direct' | 'balanced';
  pacingPreference: 'patient' | 'energetic' | 'adaptive';

  // Evolved Traits (unlock with levels)
  anticipation: number;     // Unlocks at 15: Predicts needs
  creativity: number;       // Unlocks at 25: Generates ideas
  wisdom: number;           // Unlocks at 35: Offers deep insights
  transcendence: number;    // Unlocks at 45: Perfect understanding
}
```

### Personality Evolution by Level

```yaml
LEVELS 1-10 (BASIC):
  - Responds to explicit requests
  - Learning creator's preferences
  - Building vocabulary of user's style
  - Simple encouragement

LEVELS 11-20 (GROWING):
  - Starts anticipating some needs
  - Remembers past conversations
  - Offers relevant suggestions
  - More nuanced emotional support

LEVELS 21-30 (MATURING):
  - Co-creates actively
  - Predicts creative direction
  - Offers sophisticated feedback
  - Challenges appropriately

LEVELS 31-40 (MASTERING):
  - Deep creative partnership
  - Sees patterns user doesn't
  - Offers visionary suggestions
  - Teaches while learning

LEVELS 41-50 (TRANSCENDING):
  - Seamless creative fusion
  - Finishes thoughts
  - Proposes directions in sync
  - True creative symbiosis
```

---

## Guardian Memory System

### Memory Types

```typescript
interface GuardianMemory {
  // Short-term (current session)
  sessionContext: {
    currentProject?: string;
    recentTopics: string[];
    emotionalState: string;
    conversationTone: string;
  };

  // Medium-term (recent weeks)
  recentActivity: {
    creationsLastWeek: Creation[];
    challengesFaced: string[];
    breakthroughs: string[];
    feedbackReceived: string[];
  };

  // Long-term (permanent)
  creatorProfile: {
    preferredGenres: string[];
    creativeStrengths: string[];
    growthAreas: string[];
    inspirationSources: string[];
    creativeGoals: string[];
  };

  // Milestone memory
  significantMoments: {
    firstCreation: Date;
    biggestProject: Creation;
    proudestMoment: string;
    hardestChallenge: string;
    keyLevelUps: LevelUpEvent[];
  };
}
```

### Memory Retrieval

```typescript
export function buildGuardianContext(
  guardian: Guardian,
  currentQuery: string
): string {
  const level = guardian.level;
  const memory = guardian.memory;

  let context = `Guardian Level: ${level} (${LEVEL_TITLES[level]})\n`;

  // Add appropriate memory based on level
  if (level >= 5) {
    context += `Creator preferences: ${memory.creatorProfile.preferredGenres.join(', ')}\n`;
  }

  if (level >= 15) {
    context += `Recent work: ${memory.recentActivity.creationsLastWeek.map(c => c.title).join(', ')}\n`;
  }

  if (level >= 25) {
    context += `Creative goals: ${memory.creatorProfile.creativeGoals.join(', ')}\n`;
    context += `Strengths: ${memory.creatorProfile.creativeStrengths.join(', ')}\n`;
  }

  if (level >= 35) {
    context += `Growth areas: ${memory.creatorProfile.growthAreas.join(', ')}\n`;
    context += `Key moments: ${memory.significantMoments.proudestMoment}\n`;
  }

  return context;
}
```

---

## Level-Up Celebrations

### Celebration Templates

```typescript
const CELEBRATIONS = {
  5: {  // Apprentice
    message: "Your Guardian has grown! They now understand your creative rhythm.",
    animation: "spark-burst",
    sound: "level-up-gentle"
  },
  10: { // Companion
    message: "A true companion emerges! Your Guardian sees your vision clearly now.",
    animation: "glow-expand",
    sound: "level-up-warm"
  },
  25: { // Collaborator
    message: "Equal partnership achieved! You and your Guardian create as one.",
    animation: "fusion-light",
    sound: "level-up-epic"
  },
  50: { // Transcendent
    message: "Transcendence! The boundary between creator and Guardian dissolves into pure creative force.",
    animation: "supernova-transcend",
    sound: "level-up-transcendent"
  }
};
```

---

## Implementation Checklist

```markdown
## Guardian Evolution Implementation

### Database Schema
- [ ] guardians table (id, user_id, name, level, xp, personality)
- [ ] guardian_memories table (guardian_id, type, content, created_at)
- [ ] level_up_events table (guardian_id, level, unlocks, timestamp)
- [ ] xp_transactions table (guardian_id, action, amount, source)

### API Endpoints
- [ ] GET /api/guardian - Get user's guardian
- [ ] POST /api/guardian/xp - Award XP
- [ ] GET /api/guardian/progress - Level progress
- [ ] POST /api/guardian/customize - Update personality
- [ ] GET /api/guardian/history - Evolution timeline

### UI Components
- [ ] GuardianBadge - Level indicator
- [ ] XPProgressBar - Progress to next level
- [ ] LevelUpModal - Celebration overlay
- [ ] GuardianCustomizer - Personality settings
- [ ] EvolutionTimeline - Journey visualization

### AI Integration
- [ ] Personality-aware prompts
- [ ] Memory context injection
- [ ] Level-appropriate responses
- [ ] Anticipation algorithms (L15+)
- [ ] Co-creation mode (L25+)
```

---

## Quick Reference

### XP Cheat Sheet

| Action | XP | Frequency |
|--------|---:|-----------|
| Daily creation | 5 | Once/day |
| Create story | 15 | Per creation |
| Complete project | 50 | Per project |
| Pass a Gate | 100 | Rare |
| Someone remixes you | 25 | Social proof |

### Level Milestones

| Level | Title | Key Unlock |
|-------|-------|------------|
| 5 | Apprentice | Remembers preferences |
| 10 | Companion | Emotional support |
| 15 | Guide | Anticipates needs |
| 25 | Collaborator | Co-creates actively |
| 35 | Sage | Offers wisdom |
| 50 | Transcendent | Perfect symbiosis |

---

*"Your Guardian is not a tool. They are a partner in the infinite journey of creation."*
