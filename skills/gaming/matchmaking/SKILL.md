---
name: Matchmaking
description: Pairing players for multiplayer games based on skill, latency, and party composition using ELO rating systems, queue management, and balance algorithms for fair and engaging matches.
---

# Matchmaking

> **Current Level:** Intermediate  
> **Domain:** Gaming / Backend

---

## Overview

Matchmaking pairs players for multiplayer games based on skill, latency, and party composition. This guide covers ELO, queue systems, and balance algorithms for creating fair, balanced matches that provide good gameplay experiences.

---

## Matchmaking Concepts

```
Player Queue → Skill Matching → Latency Check → Team Balance → Match Created
```

**Goals:**
- Fair matches
- Low wait times
- Balanced teams
- Good connection quality

## Skill-based Matching

### ELO Rating System

```typescript
// services/elo.service.ts
export class ELOService {
  private K_FACTOR = 32; // Sensitivity to rating changes

  calculateNewRatings(
    player1Rating: number,
    player2Rating: number,
    player1Won: boolean
  ): { player1: number; player2: number } {
    const expectedScore1 = this.getExpectedScore(player1Rating, player2Rating);
    const expectedScore2 = this.getExpectedScore(player2Rating, player1Rating);

    const actualScore1 = player1Won ? 1 : 0;
    const actualScore2 = player1Won ? 0 : 1;

    const newRating1 = player1Rating + this.K_FACTOR * (actualScore1 - expectedScore1);
    const newRating2 = player2Rating + this.K_FACTOR * (actualScore2 - expectedScore2);

    return {
      player1: Math.round(newRating1),
      player2: Math.round(newRating2)
    };
  }

  private getExpectedScore(ratingA: number, ratingB: number): number {
    return 1 / (1 + Math.pow(10, (ratingB - ratingA) / 400));
  }

  getRatingDifference(rating1: number, rating2: number): number {
    return Math.abs(rating1 - rating2);
  }

  isBalancedMatch(rating1: number, rating2: number, threshold: number = 200): boolean {
    return this.getRatingDifference(rating1, rating2) <= threshold;
  }
}
```

### Glicko-2 Rating System

```typescript
// services/glicko.service.ts
export class GlickoService {
  private TAU = 0.5; // System constant
  private EPSILON = 0.000001;

  calculateNewRating(
    rating: number,
    ratingDeviation: number,
    volatility: number,
    opponents: Opponent[]
  ): GlickoRating {
    // Convert to Glicko-2 scale
    const mu = (rating - 1500) / 173.7178;
    const phi = ratingDeviation / 173.7178;

    // Calculate v (variance)
    const v = this.calculateVariance(mu, phi, opponents);

    // Calculate delta
    const delta = this.calculateDelta(mu, phi, opponents, v);

    // Calculate new volatility
    const newVolatility = this.calculateNewVolatility(phi, volatility, delta, v);

    // Calculate new rating deviation
    const phiStar = Math.sqrt(phi * phi + newVolatility * newVolatility);
    const newPhi = 1 / Math.sqrt(1 / (phiStar * phiStar) + 1 / v);

    // Calculate new rating
    const newMu = mu + newPhi * newPhi * this.calculateDelta(mu, phi, opponents, v);

    // Convert back to original scale
    return {
      rating: Math.round(newMu * 173.7178 + 1500),
      ratingDeviation: Math.round(newPhi * 173.7178),
      volatility: newVolatility
    };
  }

  private calculateVariance(mu: number, phi: number, opponents: Opponent[]): number {
    let sum = 0;
    
    for (const opp of opponents) {
      const oppMu = (opp.rating - 1500) / 173.7178;
      const oppPhi = opp.ratingDeviation / 173.7178;
      const g = this.g(oppPhi);
      const E = this.E(mu, oppMu, oppPhi);
      
      sum += g * g * E * (1 - E);
    }

    return 1 / sum;
  }

  private calculateDelta(mu: number, phi: number, opponents: Opponent[], v: number): number {
    let sum = 0;
    
    for (const opp of opponents) {
      const oppMu = (opp.rating - 1500) / 173.7178;
      const oppPhi = opp.ratingDeviation / 173.7178;
      const g = this.g(oppPhi);
      const E = this.E(mu, oppMu, oppPhi);
      
      sum += g * (opp.score - E);
    }

    return v * sum;
  }

  private g(phi: number): number {
    return 1 / Math.sqrt(1 + 3 * phi * phi / (Math.PI * Math.PI));
  }

  private E(mu: number, muJ: number, phiJ: number): number {
    return 1 / (1 + Math.exp(-this.g(phiJ) * (mu - muJ)));
  }

  private calculateNewVolatility(
    phi: number,
    sigma: number,
    delta: number,
    v: number
  ): number {
    // Simplified implementation
    return sigma;
  }
}

interface Opponent {
  rating: number;
  ratingDeviation: number;
  score: number; // 1 for win, 0 for loss, 0.5 for draw
}

interface GlickoRating {
  rating: number;
  ratingDeviation: number;
  volatility: number;
}
```

## Queue System

```typescript
// services/matchmaking-queue.service.ts
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL!);

export class MatchmakingQueueService {
  async joinQueue(playerId: string, gameMode: string): Promise<void> {
    const player = await db.player.findUnique({
      where: { id: playerId },
      include: { rating: true }
    });

    if (!player) throw new Error('Player not found');

    const queueEntry: QueueEntry = {
      playerId,
      rating: player.rating?.rating || 1500,
      joinedAt: Date.now(),
      region: player.region || 'us-east',
      partyId: null
    };

    // Add to Redis sorted set (sorted by rating)
    await redis.zadd(
      `queue:${gameMode}`,
      queueEntry.rating,
      JSON.stringify(queueEntry)
    );

    // Set expiry (5 minutes)
    await redis.expire(`queue:${gameMode}`, 300);

    // Start matchmaking
    await this.findMatch(gameMode);
  }

  async leaveQueue(playerId: string, gameMode: string): Promise<void> {
    const members = await redis.zrange(`queue:${gameMode}`, 0, -1);

    for (const member of members) {
      const entry: QueueEntry = JSON.parse(member);
      if (entry.playerId === playerId) {
        await redis.zrem(`queue:${gameMode}`, member);
        break;
      }
    }
  }

  private async findMatch(gameMode: string): Promise<void> {
    const queueSize = await redis.zcard(`queue:${gameMode}`);

    if (queueSize < 2) return; // Need at least 2 players

    // Get all players in queue
    const members = await redis.zrange(`queue:${gameMode}`, 0, -1);
    const players: QueueEntry[] = members.map(m => JSON.parse(m));

    // Try to find matches
    const matches = this.createMatches(players);

    for (const match of matches) {
      await this.createMatch(match, gameMode);

      // Remove matched players from queue
      for (const player of match) {
        await redis.zrem(`queue:${gameMode}`, JSON.stringify(player));
      }
    }
  }

  private createMatches(players: QueueEntry[]): QueueEntry[][] {
    const matches: QueueEntry[][] = [];
    const used = new Set<string>();

    // Sort by rating
    players.sort((a, b) => a.rating - b.rating);

    for (let i = 0; i < players.length - 1; i++) {
      if (used.has(players[i].playerId)) continue;

      const player1 = players[i];
      
      // Find best match
      for (let j = i + 1; j < players.length; j++) {
        if (used.has(players[j].playerId)) continue;

        const player2 = players[j];

        // Check rating difference
        if (Math.abs(player1.rating - player2.rating) <= 200) {
          // Check region
          if (player1.region === player2.region) {
            matches.push([player1, player2]);
            used.add(player1.playerId);
            used.add(player2.playerId);
            break;
          }
        }
      }
    }

    return matches;
  }

  private async createMatch(players: QueueEntry[], gameMode: string): Promise<void> {
    const match = await db.match.create({
      data: {
        gameMode,
        status: 'pending',
        players: {
          create: players.map(p => ({
            playerId: p.playerId,
            team: 0
          }))
        }
      }
    });

    // Notify players
    for (const player of players) {
      io.to(`player:${player.playerId}`).emit('match-found', {
        matchId: match.id,
        players: players.map(p => p.playerId)
      });
    }
  }
}

interface QueueEntry {
  playerId: string;
  rating: number;
  joinedAt: number;
  region: string;
  partyId: string | null;
}
```

## Party/Group Matchmaking

```typescript
// services/party-matchmaking.service.ts
export class PartyMatchmakingService {
  async createParty(leaderId: string): Promise<string> {
    const party = await db.party.create({
      data: {
        leaderId,
        members: {
          create: [{ playerId: leaderId }]
        }
      }
    });

    return party.id;
  }

  async joinParty(playerId: string, partyId: string): Promise<void> {
    const party = await db.party.findUnique({
      where: { id: partyId },
      include: { members: true }
    });

    if (!party) throw new Error('Party not found');
    if (party.members.length >= 4) throw new Error('Party full');

    await db.partyMember.create({
      data: {
        partyId,
        playerId
      }
    });
  }

  async joinQueueAsParty(partyId: string, gameMode: string): Promise<void> {
    const party = await db.party.findUnique({
      where: { id: partyId },
      include: {
        members: {
          include: {
            player: { include: { rating: true } }
          }
        }
      }
    });

    if (!party) throw new Error('Party not found');

    // Calculate average party rating
    const avgRating = party.members.reduce(
      (sum, m) => sum + (m.player.rating?.rating || 1500),
      0
    ) / party.members.length;

    const queueEntry: PartyQueueEntry = {
      partyId,
      playerIds: party.members.map(m => m.playerId),
      avgRating,
      size: party.members.length,
      joinedAt: Date.now()
    };

    await redis.zadd(
      `queue:${gameMode}:party`,
      avgRating,
      JSON.stringify(queueEntry)
    );
  }
}

interface PartyQueueEntry {
  partyId: string;
  playerIds: string[];
  avgRating: number;
  size: number;
  joinedAt: number;
}
```

## Latency-based Matching

```typescript
// services/latency-matcher.service.ts
export class LatencyMatcherService {
  async measureLatency(playerId: string, region: string): Promise<number> {
    // Ping test to regional server
    const start = Date.now();
    await fetch(`https://${region}.gameserver.com/ping`);
    const latency = Date.now() - start;

    // Store latency
    await redis.setex(`latency:${playerId}:${region}`, 300, latency.toString());

    return latency;
  }

  async findBestRegion(playerId: string): Promise<string> {
    const regions = ['us-east', 'us-west', 'eu-west', 'ap-southeast'];
    const latencies: Array<{ region: string; latency: number }> = [];

    for (const region of regions) {
      const latency = await this.measureLatency(playerId, region);
      latencies.push({ region, latency });
    }

    latencies.sort((a, b) => a.latency - b.latency);
    return latencies[0].region;
  }

  async matchByLatency(
    players: QueueEntry[],
    maxLatencyDiff: number = 50
  ): Promise<QueueEntry[][]> {
    const matches: QueueEntry[][] = [];

    // Group players by region
    const byRegion = new Map<string, QueueEntry[]>();
    
    for (const player of players) {
      const region = player.region;
      if (!byRegion.has(region)) {
        byRegion.set(region, []);
      }
      byRegion.get(region)!.push(player);
    }

    // Match within regions
    for (const [region, regionPlayers] of byRegion) {
      for (let i = 0; i < regionPlayers.length - 1; i += 2) {
        matches.push([regionPlayers[i], regionPlayers[i + 1]]);
      }
    }

    return matches;
  }
}
```

## Balance Algorithms

```typescript
// services/team-balancer.service.ts
export class TeamBalancerService {
  balanceTeams(players: Player[]): { team1: Player[]; team2: Player[] } {
    // Sort by rating
    players.sort((a, b) => b.rating - a.rating);

    const team1: Player[] = [];
    const team2: Player[] = [];

    // Snake draft
    for (let i = 0; i < players.length; i++) {
      if (i % 2 === 0) {
        team1.push(players[i]);
      } else {
        team2.push(players[i]);
      }
    }

    return { team1, team2 };
  }

  calculateTeamRating(team: Player[]): number {
    return team.reduce((sum, p) => sum + p.rating, 0) / team.length;
  }

  isBalanced(team1: Player[], team2: Player[], threshold: number = 100): boolean {
    const rating1 = this.calculateTeamRating(team1);
    const rating2 = this.calculateTeamRating(team2);

    return Math.abs(rating1 - rating2) <= threshold;
  }
}

interface Player {
  id: string;
  rating: number;
}
```

---

## Quick Start

### Basic Matchmaking Queue

```typescript
interface Player {
  id: string
  rating: number
  region: string
  partyId?: string
}

class MatchmakingQueue {
  private queue: Player[] = []
  
  addPlayer(player: Player) {
    this.queue.push(player)
    this.tryMatch()
  }
  
  tryMatch() {
    // Sort by rating
    this.queue.sort((a, b) => a.rating - b.rating)
    
    // Find players within rating range
    for (let i = 0; i < this.queue.length - 1; i++) {
      const player1 = this.queue[i]
      const player2 = this.queue[i + 1]
      
      const ratingDiff = Math.abs(player1.rating - player2.rating)
      if (ratingDiff <= 100 && player1.region === player2.region) {
        this.createMatch([player1, player2])
        this.queue.splice(i, 2)
        break
      }
    }
  }
  
  createMatch(players: Player[]) {
    // Create match and notify players
    console.log('Match created:', players.map(p => p.id))
  }
}
```

### ELO Rating Update

```typescript
function updateELO(playerRating: number, opponentRating: number, won: boolean): number {
  const expectedScore = 1 / (1 + Math.pow(10, (opponentRating - playerRating) / 400))
  const actualScore = won ? 1 : 0
  const kFactor = 32
  
  return Math.round(playerRating + kFactor * (actualScore - expectedScore))
}
```

---

## Production Checklist

- [ ] **Skill Matching**: Use ELO or Glicko-2 rating system
- [ ] **Queue Management**: Efficient queue management
- [ ] **Rating Range**: Configurable rating range for matching
- [ ] **Latency Consideration**: Match players in same region
- [ ] **Party Support**: Support group/party matchmaking
- [ ] **Wait Time**: Balance fairness vs wait time
- [ ] **Queue Time Limits**: Maximum queue time
- [ ] **Match Quality**: Monitor match quality metrics
- [ ] **Testing**: Test with various player pools
- [ ] **Analytics**: Track matchmaking metrics
- [ ] **Documentation**: Document matchmaking rules
- [ ] **Anti-cheat**: Prevent rating manipulation

---

## Anti-patterns

### ❌ Don't: No Skill Matching

```typescript
// ❌ Bad - Random matching
function matchPlayers(players: Player[]) {
  return [players[0], players[1]]  // Random!
}
```

```typescript
// ✅ Good - Skill-based matching
function matchPlayers(players: Player[]) {
  // Find players with similar rating
  const ratingRange = 100
  for (const player1 of players) {
    const match = players.find(p => 
      p.id !== player1.id &&
      Math.abs(p.rating - player1.rating) <= ratingRange
    )
    if (match) return [player1, match]
  }
}
```

### ❌ Don't: Ignore Latency

```typescript
// ❌ Bad - Match across regions
function matchPlayers(players: Player[]) {
  return [players[0], players[1]]  // Could be different regions!
}
```

```typescript
// ✅ Good - Region-aware matching
function matchPlayers(players: Player[]) {
  const region = players[0].region
  const sameRegion = players.filter(p => p.region === region)
  // Match within same region
  return findMatch(sameRegion)
}
```

---

## Integration Points

- **Leaderboards** (`38-gaming-features/leaderboards/`) - Rating systems
- **Real-time Multiplayer** (`38-gaming-features/real-time-multiplayer/`) - Match execution
- **Game Analytics** (`38-gaming-features/game-analytics/`) - Matchmaking metrics

---

## Further Reading

- [ELO Rating System](https://en.wikipedia.org/wiki/Elo_rating_system)
- [Glicko-2 Rating System](http://www.glicko.net/glicko/glicko2.pdf)
- [Matchmaking Algorithms](https://www.gamedeveloper.com/design/matchmaking-algorithms)
5. **Balance** - Create fair teams
6. **Timeout** - Handle queue timeouts
7. **Scaling** - Design for high concurrency
8. **Analytics** - Track match quality
9. **Feedback** - Show queue position
10. **Testing** - Test with various scenarios

## Resources

- [ELO Rating System](https://en.wikipedia.org/wiki/Elo_rating_system)
- [Glicko-2 Rating](http://www.glicko.net/glicko/glicko2.pdf)
- [Matchmaking in Games](https://www.gamedeveloper.com/design/matchmaking-in-multiplayer-games)
- [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/)
