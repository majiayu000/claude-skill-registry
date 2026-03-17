---
name: analytics
description: >-
  Understand and work with EPA and OPR analytics algorithms in FTC Metrics.
  Use when calculating team ratings, implementing match predictions,
  troubleshooting analytics calculations, or understanding the scoring methodology.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: analytics
---

# FTC Metrics Analytics

FTC Metrics uses two primary rating systems to evaluate team performance:
- **EPA** (Expected Points Added) - Bayesian-style incremental updates
- **OPR** (Offensive Power Rating) - Linear algebra matrix solution

## Quick Reference

| Metric | Best For | Updates |
|--------|----------|---------|
| EPA | Predicting future performance | After each match |
| OPR | Analyzing historical contribution | Recalculated per event |

## EPA (Expected Points Added)

EPA represents how many points above/below average a team contributes to their alliance score.

### Algorithm Overview

1. Start with season baseline (average scores)
2. After each match, calculate expected vs actual
3. Distribute score difference to teams
4. Apply adaptive K-factor for learning rate

### Usage

```typescript
import { calculateEPA, type MatchForEPA } from "@ftcmetrics/api/lib/stats";

const matches: MatchForEPA[] = [
  {
    matchNumber: 1,
    redTeam1: 12345,
    redTeam2: 12346,
    blueTeam1: 12347,
    blueTeam2: 12348,
    redScore: 45,
    blueScore: 38,
    redAutoScore: 12,
    redTeleopScore: 28,
    redEndgameScore: 5,
    // ... blue scores
  },
];

const epaResults = calculateEPA(matches);
const team12345 = epaResults.get(12345);
// { epa: 5.2, autoEpa: 1.5, teleopEpa: 3.2, endgameEpa: 0.5, ... }
```

### EPA Result Structure

```typescript
interface EPAResult {
  teamNumber: number;
  epa: number;          // Total EPA
  autoEpa: number;      // Autonomous phase
  teleopEpa: number;    // Teleop phase
  endgameEpa: number;   // Endgame phase
  matchCount: number;   // Matches played
  recentEpa?: number;   // Last 5 matches average
  trend?: "up" | "down" | "stable";
}
```

### Adaptive K-Factor

K-factor determines how much each new match affects the rating:

```typescript
// High K (0.4) for new teams = ratings change quickly
// Low K (0.1) for experienced teams = ratings stabilize
function getAdaptiveKFactor(matchCount: number): number {
  const minK = 0.1;
  const maxK = 0.4;
  const decayRate = 0.1;
  return Math.max(minK, maxK * Math.exp(-decayRate * matchCount));
}
```

## OPR (Offensive Power Rating)

OPR uses linear algebra to decompose alliance scores into individual team contributions.

### Algorithm Overview

1. Build matrix of alliance compositions
2. Build vector of alliance scores
3. Solve using iterative least squares
4. Each team's OPR = their contribution to alliance score

### Usage

```typescript
import { calculateOPR, type MatchForOPR } from "@ftcmetrics/api/lib/stats";

const matches: MatchForOPR[] = [...]; // Match data

const oprResults = calculateOPR(matches);
const team12345 = oprResults.get(12345);
// { opr: 22.5, autoOpr: 6.0, teleopOpr: 14.0, endgameOpr: 2.5, dpr: 3.2, ccwm: 19.3 }
```

### OPR Result Structure

```typescript
interface OPRResult {
  teamNumber: number;
  opr: number;          // Offensive Power Rating
  autoOpr: number;      // Auto contribution
  teleopOpr: number;    // Teleop contribution
  endgameOpr: number;   // Endgame contribution
  dpr: number;          // Defensive Power Rating
  ccwm: number;         // Calculated Contribution to Winning Margin
}
```

## Match Predictions

Predictions combine EPA values to estimate match outcomes:

```typescript
interface PredictionResult {
  redExpectedScore: number;
  blueExpectedScore: number;
  redWinProbability: number;
  blueWinProbability: number;
  predictedMargin: number;
}
```

### Prediction Formula

```typescript
// Sum EPAs and add baseline
const redExpected = baseline + redTeam1EPA + redTeam2EPA;
const blueExpected = baseline + blueTeam1EPA + blueTeam2EPA;

// Win probability using logistic function
const margin = redExpected - blueExpected;
const redWinProb = 1 / (1 + Math.exp(-margin / SCORE_VARIANCE));
```

## DECODE Season Baselines

```typescript
const DECODE_BASELINE = {
  autoScore: 8,      // Average auto per alliance
  teleopScore: 25,   // Average teleop per alliance
  endgameScore: 5,   // Average endgame per alliance
  totalScore: 38,    // Average total per alliance
};
```

These baselines are updated dynamically based on actual match data.

## Common Patterns

### Calculate Rankings for Event

```typescript
async function getEventRankings(eventCode: string) {
  const matches = await fetchMatchesWithScores(eventCode);

  const epaResults = calculateEPA(matches);
  const oprResults = calculateOPR(matches);

  // Combine and sort by EPA
  const rankings = Array.from(epaResults.values())
    .map((epa) => ({
      ...epa,
      opr: oprResults.get(epa.teamNumber),
    }))
    .sort((a, b) => b.epa - a.epa);

  return rankings;
}
```

### Track EPA Over Time

```typescript
// Store EPA after each match for trend analysis
interface EPAHistory {
  teamNumber: number;
  eventCode: string;
  matchNumber: number;
  epaValue: number;
  recordedAt: Date;
}
```

## Anti-Patterns

- ❌ Using OPR for predictions (use EPA instead - OPR overfits to past data)
- ❌ Calculating EPA without sorting matches chronologically
- ❌ Using static K-factor (adaptive K improves accuracy)
- ❌ Ignoring component scores (auto/teleop/endgame give better insights)

## Implementation Files

- `packages/api/src/lib/stats/epa.ts` - EPA calculator
- `packages/api/src/lib/stats/opr.ts` - OPR calculator
- `packages/api/src/routes/analytics.ts` - Analytics API endpoints

## References

- [Statbotics EPA Methodology](https://www.statbotics.io/blog/epa)
- [OPR Explained](https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/)
