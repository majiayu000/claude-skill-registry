---
name: Achievements System
description: Rewarding players for completing specific goals through progress tracking, unlocking logic, rarity calculation, and achievement display for gamification and player engagement.
---

# Achievements System

> **Current Level:** Intermediate  
> **Domain:** Gaming / Backend

---

## Overview

Achievements reward players for completing specific goals. This guide covers progress tracking, unlocking logic, and rarity calculation for building engaging achievement systems that motivate players and increase retention.

## Achievement Types

### Progress-based
- Track incremental progress
- Example: "Kill 100 enemies"

### Milestone
- One-time achievements
- Example: "Complete first level"

### Hidden
- Secret achievements
- Revealed upon unlock

### Rare
- Difficult achievements
- Limited unlock rate

## Database Schema

```sql
-- achievements table
CREATE TABLE achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key VARCHAR(100) UNIQUE NOT NULL,
  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  icon_url VARCHAR(500),
  
  type VARCHAR(50) NOT NULL,
  category VARCHAR(100),
  
  hidden BOOLEAN DEFAULT FALSE,
  
  points INTEGER DEFAULT 0,
  
  requirement_type VARCHAR(50),
  requirement_value INTEGER,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_key (key),
  INDEX idx_category (category)
);

-- player_achievements table
CREATE TABLE player_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id UUID REFERENCES players(id) ON DELETE CASCADE,
  achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
  
  progress INTEGER DEFAULT 0,
  unlocked BOOLEAN DEFAULT FALSE,
  unlocked_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(player_id, achievement_id),
  INDEX idx_player (player_id),
  INDEX idx_unlocked (unlocked, unlocked_at)
);

-- achievement_stats table
CREATE TABLE achievement_stats (
  achievement_id UUID PRIMARY KEY REFERENCES achievements(id),
  
  total_unlocks INTEGER DEFAULT 0,
  unlock_rate DECIMAL(5,2) DEFAULT 0,
  
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## Achievement Tracking

```typescript
// services/achievement.service.ts
export class AchievementService {
  async trackProgress(
    playerId: string,
    achievementKey: string,
    increment: number = 1
  ): Promise<AchievementProgress> {
    const achievement = await db.achievement.findUnique({
      where: { key: achievementKey }
    });

    if (!achievement) {
      throw new Error('Achievement not found');
    }

    // Get or create player achievement
    let playerAchievement = await db.playerAchievement.findUnique({
      where: {
        playerId_achievementId: {
          playerId,
          achievementId: achievement.id
        }
      }
    });

    if (!playerAchievement) {
      playerAchievement = await db.playerAchievement.create({
        data: {
          playerId,
          achievementId: achievement.id,
          progress: 0
        }
      });
    }

    // Update progress
    const newProgress = playerAchievement.progress + increment;
    const isComplete = newProgress >= (achievement.requirementValue || 1);

    playerAchievement = await db.playerAchievement.update({
      where: { id: playerAchievement.id },
      data: {
        progress: newProgress,
        unlocked: isComplete,
        unlockedAt: isComplete ? new Date() : null
      }
    });

    // If unlocked, update stats and notify
    if (isComplete && !playerAchievement.unlocked) {
      await this.onAchievementUnlocked(playerId, achievement.id);
    }

    return {
      achievementId: achievement.id,
      achievementKey: achievement.key,
      progress: newProgress,
      required: achievement.requirementValue || 1,
      unlocked: isComplete,
      percentage: (newProgress / (achievement.requirementValue || 1)) * 100
    };
  }

  async trackEvent(playerId: string, eventType: string, data?: any): Promise<void> {
    // Get achievements triggered by this event
    const achievements = await db.achievement.findMany({
      where: { requirementType: eventType }
    });

    for (const achievement of achievements) {
      await this.trackProgress(playerId, achievement.key, 1);
    }
  }

  private async onAchievementUnlocked(
    playerId: string,
    achievementId: string
  ): Promise<void> {
    // Update stats
    await db.achievementStats.upsert({
      where: { achievementId },
      create: {
        achievementId,
        totalUnlocks: 1
      },
      update: {
        totalUnlocks: { increment: 1 }
      }
    });

    // Calculate unlock rate
    await this.updateUnlockRate(achievementId);

    // Send notification
    await this.sendUnlockNotification(playerId, achievementId);

    // Award points
    await this.awardPoints(playerId, achievementId);
  }

  private async updateUnlockRate(achievementId: string): Promise<void> {
    const totalPlayers = await db.player.count();
    const stats = await db.achievementStats.findUnique({
      where: { achievementId }
    });

    if (stats && totalPlayers > 0) {
      const unlockRate = (stats.totalUnlocks / totalPlayers) * 100;

      await db.achievementStats.update({
        where: { achievementId },
        data: { unlockRate }
      });
    }
  }

  private async sendUnlockNotification(
    playerId: string,
    achievementId: string
  ): Promise<void> {
    const achievement = await db.achievement.findUnique({
      where: { id: achievementId }
    });

    if (achievement) {
      // Emit WebSocket event
      io.to(`player:${playerId}`).emit('achievement-unlocked', {
        id: achievement.id,
        name: achievement.name,
        description: achievement.description,
        iconUrl: achievement.iconUrl,
        points: achievement.points
      });
    }
  }

  private async awardPoints(playerId: string, achievementId: string): Promise<void> {
    const achievement = await db.achievement.findUnique({
      where: { id: achievementId }
    });

    if (achievement && achievement.points > 0) {
      await db.player.update({
        where: { id: playerId },
        data: {
          achievementPoints: { increment: achievement.points }
        }
      });
    }
  }
}

interface AchievementProgress {
  achievementId: string;
  achievementKey: string;
  progress: number;
  required: number;
  unlocked: boolean;
  percentage: number;
}
```

## Progress Calculation

```typescript
// Different progress calculation strategies
export class ProgressCalculator {
  calculateLinear(current: number, required: number): number {
    return Math.min((current / required) * 100, 100);
  }

  calculateTiered(current: number, tiers: number[]): number {
    let completedTiers = 0;
    
    for (const tier of tiers) {
      if (current >= tier) {
        completedTiers++;
      }
    }

    return (completedTiers / tiers.length) * 100;
  }

  calculateCumulative(values: number[], required: number): number {
    const total = values.reduce((sum, val) => sum + val, 0);
    return Math.min((total / required) * 100, 100);
  }
}

// Example: Multi-step achievement
const multiStepAchievement = {
  key: 'master_warrior',
  name: 'Master Warrior',
  steps: [
    { key: 'kills_100', name: 'Kill 100 enemies', required: 100 },
    { key: 'wins_50', name: 'Win 50 battles', required: 50 },
    { key: 'level_50', name: 'Reach level 50', required: 50 }
  ]
};

async function trackMultiStepProgress(playerId: string): Promise<number> {
  const steps = multiStepAchievement.steps;
  let completedSteps = 0;

  for (const step of steps) {
    const progress = await getStepProgress(playerId, step.key);
    if (progress >= step.required) {
      completedSteps++;
    }
  }

  return (completedSteps / steps.length) * 100;
}
```

## Unlocking Logic

```typescript
// services/achievement-unlock.service.ts
export class AchievementUnlockService {
  async checkUnlockConditions(
    playerId: string,
    achievementKey: string
  ): Promise<boolean> {
    const achievement = await db.achievement.findUnique({
      where: { key: achievementKey }
    });

    if (!achievement) return false;

    switch (achievement.requirementType) {
      case 'score':
        return this.checkScoreRequirement(playerId, achievement);
      
      case 'level':
        return this.checkLevelRequirement(playerId, achievement);
      
      case 'kills':
        return this.checkKillsRequirement(playerId, achievement);
      
      case 'time_played':
        return this.checkTimePlayedRequirement(playerId, achievement);
      
      case 'consecutive_wins':
        return this.checkConsecutiveWinsRequirement(playerId, achievement);
      
      default:
        return false;
    }
  }

  private async checkScoreRequirement(
    playerId: string,
    achievement: Achievement
  ): Promise<boolean> {
    const player = await db.player.findUnique({ where: { id: playerId } });
    return (player?.highScore || 0) >= (achievement.requirementValue || 0);
  }

  private async checkLevelRequirement(
    playerId: string,
    achievement: Achievement
  ): Promise<boolean> {
    const player = await db.player.findUnique({ where: { id: playerId } });
    return (player?.level || 0) >= (achievement.requirementValue || 0);
  }

  private async checkKillsRequirement(
    playerId: string,
    achievement: Achievement
  ): Promise<boolean> {
    const stats = await db.playerStats.findUnique({ where: { playerId } });
    return (stats?.totalKills || 0) >= (achievement.requirementValue || 0);
  }

  private async checkTimePlayedRequirement(
    playerId: string,
    achievement: Achievement
  ): Promise<boolean> {
    const stats = await db.playerStats.findUnique({ where: { playerId } });
    return (stats?.totalPlayTime || 0) >= (achievement.requirementValue || 0);
  }

  private async checkConsecutiveWinsRequirement(
    playerId: string,
    achievement: Achievement
  ): Promise<boolean> {
    const stats = await db.playerStats.findUnique({ where: { playerId } });
    return (stats?.currentWinStreak || 0) >= (achievement.requirementValue || 0);
  }
}
```

## Rarity Calculation

```typescript
// services/achievement-rarity.service.ts
export class AchievementRarityService {
  async calculateRarity(achievementId: string): Promise<string> {
    const stats = await db.achievementStats.findUnique({
      where: { achievementId }
    });

    if (!stats) return 'common';

    const unlockRate = stats.unlockRate;

    if (unlockRate >= 50) return 'common';
    if (unlockRate >= 20) return 'uncommon';
    if (unlockRate >= 5) return 'rare';
    if (unlockRate >= 1) return 'epic';
    return 'legendary';
  }

  async getRarityColor(rarity: string): Promise<string> {
    const colors: Record<string, string> = {
      common: '#808080',
      uncommon: '#00ff00',
      rare: '#0070dd',
      epic: '#a335ee',
      legendary: '#ff8000'
    };

    return colors[rarity] || colors.common;
  }

  async getPlayerRarityStats(playerId: string): Promise<RarityStats> {
    const achievements = await db.playerAchievement.findMany({
      where: { playerId, unlocked: true },
      include: { achievement: { include: { stats: true } } }
    });

    const rarityCount: Record<string, number> = {
      common: 0,
      uncommon: 0,
      rare: 0,
      epic: 0,
      legendary: 0
    };

    for (const pa of achievements) {
      const rarity = await this.calculateRarity(pa.achievement.id);
      rarityCount[rarity]++;
    }

    return rarityCount;
  }
}

type RarityStats = Record<string, number>;
```

## Point System

```typescript
// Achievement points based on rarity
const pointsByRarity: Record<string, number> = {
  common: 10,
  uncommon: 25,
  rare: 50,
  epic: 100,
  legendary: 250
};

async function assignPoints(achievementId: string): Promise<void> {
  const rarity = await rarityService.calculateRarity(achievementId);
  const points = pointsByRarity[rarity];

  await db.achievement.update({
    where: { id: achievementId },
    data: { points }
  });
}
```

## Social Sharing

```typescript
// services/achievement-sharing.service.ts
export class AchievementSharingService {
  async generateShareImage(
    playerId: string,
    achievementId: string
  ): Promise<string> {
    // Generate image with achievement details
    // Return URL to generated image
    return `https://cdn.example.com/achievements/${achievementId}/share.png`;
  }

  async shareToSocial(
    playerId: string,
    achievementId: string,
    platform: 'twitter' | 'facebook'
  ): Promise<string> {
    const achievement = await db.achievement.findUnique({
      where: { id: achievementId }
    });

    const player = await db.player.findUnique({
      where: { id: playerId }
    });

    if (!achievement || !player) {
      throw new Error('Not found');
    }

    const shareUrl = `https://game.example.com/achievements/${achievementId}`;
    const text = `I just unlocked "${achievement.name}" in Game! ${shareUrl}`;

    if (platform === 'twitter') {
      return `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    } else {
      return `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
    }
  }
}
```

## Achievement Display

```typescript
// components/AchievementCard.tsx
export function AchievementCard({ achievement, progress }: AchievementCardProps) {
  const isUnlocked = progress?.unlocked || false;
  const percentage = progress?.percentage || 0;

  return (
    <div className={`achievement-card ${isUnlocked ? 'unlocked' : 'locked'}`}>
      <div className="achievement-icon">
        <img
          src={achievement.iconUrl}
          alt={achievement.name}
          style={{ filter: isUnlocked ? 'none' : 'grayscale(100%)' }}
        />
      </div>

      <div className="achievement-info">
        <h3>{achievement.name}</h3>
        <p>{achievement.hidden && !isUnlocked ? '???' : achievement.description}</p>

        {!isUnlocked && achievement.requirementValue && (
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${percentage}%` }}
            />
            <span>{progress?.progress || 0} / {achievement.requirementValue}</span>
          </div>
        )}

        {isUnlocked && progress?.unlockedAt && (
          <p className="unlock-date">
            Unlocked: {new Date(progress.unlockedAt).toLocaleDateString()}
          </p>
        )}

        <div className="achievement-meta">
          <span className="points">{achievement.points} pts</span>
          <span className={`rarity ${achievement.rarity}`}>
            {achievement.rarity}
          </span>
        </div>
      </div>
    </div>
  );
}

interface AchievementCardProps {
  achievement: Achievement;
  progress?: AchievementProgress;
}
```

---

## Quick Start

### Achievement System

```typescript
interface Achievement {
  id: string
  name: string
  description: string
  type: 'progress' | 'milestone' | 'hidden'
  condition: AchievementCondition
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
  points: number
}

interface AchievementCondition {
  type: 'kill_count' | 'level_complete' | 'time_played'
  target: number
}

async function checkAchievements(playerId: string, action: PlayerAction) {
  const achievements = await getUnlockedAchievements(playerId)
  const allAchievements = await getAllAchievements()
  
  for (const achievement of allAchievements) {
    if (achievements.includes(achievement.id)) continue
    
    if (checkCondition(achievement.condition, action)) {
      await unlockAchievement(playerId, achievement.id)
      await notifyPlayer(playerId, achievement)
    }
  }
}
```

---

## Production Checklist

- [ ] **Achievement Design**: Design achievement system
- [ ] **Progress Tracking**: Track all relevant actions
- [ ] **Unlock Logic**: Implement unlock conditions
- [ ] **Notifications**: Celebrate unlocks
- [ ] **Rarity System**: Calculate and display rarity
- [ ] **Points System**: Reward with points/badges
- [ ] **Social Features**: Enable sharing
- [ ] **Categories**: Organize achievements
- [ ] **Analytics**: Track unlock rates
- [ ] **Balance**: Mix easy and hard achievements
- [ ] **Testing**: Test unlock conditions
- [ ] **Documentation**: Document achievement system

---

## Anti-patterns

### ❌ Don't: Too Easy or Too Hard

```markdown
# ❌ Bad - Unbalanced
Achievement 1: "Play 1 game" (too easy)
Achievement 2: "Play 1,000,000 games" (too hard)
```

```markdown
# ✅ Good - Balanced progression
Achievement 1: "Play 10 games"
Achievement 2: "Play 100 games"
Achievement 3: "Play 1,000 games"
```

### ❌ Don't: No Progress Indication

```typescript
// ❌ Bad - No progress shown
if (kills >= 100) {
  unlockAchievement('kill_100')
}
// Player doesn't know progress!
```

```typescript
// ✅ Good - Show progress
const progress = kills / 100
showProgress('kill_100', progress)  // "Kill 100 enemies: 45/100"
```

---

## Integration Points

- **Leaderboards** (`38-gaming-features/leaderboards/`) - Achievement rankings
- **Game Analytics** (`38-gaming-features/game-analytics/`) - Achievement metrics
- **Matchmaking** (`38-gaming-features/matchmaking/`) - Game sessions

---

## Further Reading

- [Achievement System Design](https://www.gamedeveloper.com/design/achievement-systems)
- [Gamification Best Practices](https://www.gamify.com/gamification-blog/gamification-best-practices)

## Resources

- [Xbox Achievements](https://www.xbox.com/en-US/live/achievements)
- [PlayStation Trophies](https://www.playstation.com/en-us/support/games/ps4-trophy-information/)
- [Steam Achievements](https://partner.steamgames.com/doc/features/achievements)
- [Game Achievement Design](https://www.gamedeveloper.com/design/designing-achievements)
