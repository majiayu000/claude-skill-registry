---
name: cloud-challenges
description: Flow Nexus coding challenges and gamification. Use for browsing challenges, submitting solutions, tracking achievements, and competing on leaderboards.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - challenge_discovery
  - solution_submission
  - achievement_tracking
  - leaderboard_competition
  - skill_progression
  - credit_rewards
tools:
  - mcp__flow-nexus__challenges_list
  - mcp__flow-nexus__challenge_get
  - mcp__flow-nexus__challenge_submit
  - mcp__flow-nexus__app_store_complete_challenge
  - mcp__flow-nexus__leaderboard_get
  - mcp__flow-nexus__achievements_list
  - mcp__flow-nexus__app_store_earn_ruv
related_skills:
  - cloud-payments
  - cloud-auth
  - cloud-sandbox
---

# Cloud Challenges

> Engage with coding challenges, earn credits, track achievements, and compete on leaderboards in Flow Nexus.

## Quick Start

```javascript
// Browse available challenges
const challenges = await mcp__flow-nexus__challenges_list({
  difficulty: "intermediate",
  category: "algorithms",
  status: "active"
});

// Get challenge details
const challenge = await mcp__flow-nexus__challenge_get({
  challenge_id: "challenge_id"
});

// Submit solution
await mcp__flow-nexus__challenge_submit({
  challenge_id: "challenge_id",
  user_id: "user_id",
  solution_code: "function solve(input) { return input.sort(); }",
  language: "javascript"
});

// Check leaderboard
const leaderboard = await mcp__flow-nexus__leaderboard_get({
  type: "global",
  limit: 10
});
```

## When to Use

- Finding coding challenges to improve skills
- Submitting solutions for validation and scoring
- Tracking personal achievements and badges
- Competing on global and challenge-specific leaderboards
- Earning rUv credits through challenge completion
- Following learning paths for skill development

## Prerequisites

- Flow Nexus account with active session
- Basic programming knowledge
- Sandbox access for testing solutions

## Core Concepts

### Difficulty Levels

| Level | Description | Credits |
|-------|-------------|---------|
| **Beginner** | Basic concepts, simple algorithms | 10-50 |
| **Intermediate** | Data structures, moderate complexity | 50-100 |
| **Advanced** | Complex algorithms, optimization | 100-250 |
| **Expert** | System design, cutting-edge problems | 250-500 |

### Challenge Categories

| Category | Focus |
|----------|-------|
| **Algorithms** | Classic algorithm problems |
| **Data Structures** | Implementation and optimization |
| **System Design** | Scalable architecture |
| **Optimization** | Performance-focused problems |
| **Security** | Cryptography, vulnerability analysis |
| **ML Basics** | Machine learning fundamentals |

### Gamification Features

- **Dynamic Scoring**: Based on code quality, efficiency, creativity
- **Achievement Badges**: Progressive unlocks for accomplishments
- **Learning Streaks**: Rewards for consistent engagement
- **Leaderboards**: Global, weekly, monthly, per-challenge

## MCP Tools Reference

### Challenge Discovery

```javascript
// List challenges
mcp__flow-nexus__challenges_list({
  difficulty: "intermediate",  // beginner, intermediate, advanced, expert
  category: "algorithms",      // algorithms, data_structures, system_design, etc.
  status: "active",            // active, completed, locked
  limit: 20                    // Max results (1-100)
})
// Returns: { challenges: [{ id, title, difficulty, category, credits }] }

// Get challenge details
mcp__flow-nexus__challenge_get({
  challenge_id: "challenge_id"
})
// Returns: { id, title, description, examples, constraints, credits, time_limit }
```

### Solution Submission

```javascript
mcp__flow-nexus__challenge_submit({
  challenge_id: "challenge_id",
  user_id: "user_id",
  solution_code: "function solve(input) { /* solution */ }",
  language: "javascript",       // javascript, python, go, rust, etc.
  execution_time: 45            // Optional: time taken in ms
})
// Returns: { passed, score, test_results, credits_earned, feedback }
```

### Challenge Completion

```javascript
mcp__flow-nexus__app_store_complete_challenge({
  challenge_id: "challenge_id",
  user_id: "user_id",
  submission_data: {
    solution_code: "...",
    time_taken: 120,
    attempts: 2
  }
})
// Returns: { completed, credits_awarded, achievements_unlocked }
```

### Achievements

```javascript
mcp__flow-nexus__achievements_list({
  user_id: "user_id",
  category: "speed_demon"       // Optional category filter
})
// Returns: { achievements: [{ id, name, description, earned_at }] }
```

### Leaderboards

```javascript
mcp__flow-nexus__leaderboard_get({
  type: "global",              // global, weekly, monthly, challenge
  challenge_id: "id",          // Required for type="challenge"
  limit: 10                    // Max entries (1-100)
})
// Returns: { rankings: [{ rank, user, score, challenges_completed }] }
```

### Earning Credits

```javascript
mcp__flow-nexus__app_store_earn_ruv({
  user_id: "user_id",
  amount: 100,
  reason: "Challenge completion: Binary Search Tree",
  source: "challenge"
})
// Returns: { new_balance, credits_earned }
```

## Usage Examples

### Example 1: Finding and Solving a Challenge

```javascript
// Browse available challenges for your skill level
const challenges = await mcp__flow-nexus__challenges_list({
  difficulty: "intermediate",
  category: "algorithms",
  status: "active",
  limit: 10
});

console.log("Available Challenges:");
for (const c of challenges.challenges) {
  console.log(`- ${c.title} (${c.difficulty}): ${c.credits} credits`);
}

// Get details for a specific challenge
const challenge = await mcp__flow-nexus__challenge_get({
  challenge_id: challenges.challenges[0].id
});

console.log(`
Challenge: ${challenge.title}
--------------------------
${challenge.description}

Examples:
${challenge.examples.map(e => `Input: ${e.input} → Output: ${e.output}`).join('\n')}

Constraints:
${challenge.constraints.join('\n')}

Time Limit: ${challenge.time_limit}ms
Credits: ${challenge.credits}
`);

// Test solution in sandbox first (recommended)
const sandbox = await mcp__flow-nexus__sandbox_create({
  template: "node"
});

const testResult = await mcp__flow-nexus__sandbox_execute({
  sandbox_id: sandbox.sandbox_id,
  code: `
    function solve(input) {
      // Your solution here
      return input.sort((a, b) => a - b);
    }
    console.log(solve([3, 1, 4, 1, 5, 9]));
  `,
  language: "javascript"
});

// Submit solution
const submission = await mcp__flow-nexus__challenge_submit({
  challenge_id: challenge.id,
  user_id: "your_user_id",
  solution_code: "function solve(input) { return input.sort((a, b) => a - b); }",
  language: "javascript"
});

if (submission.passed) {
  console.log(`\nChallenge Passed! Score: ${submission.score}`);
  console.log(`Credits Earned: ${submission.credits_earned}`);
} else {
  console.log("\nSome tests failed:");
  for (const result of submission.test_results) {
    if (!result.passed) {
      console.log(`- Test ${result.id}: ${result.feedback}`);
    }
  }
}
```

### Example 2: Tracking Progress and Achievements

```javascript
// Get your achievements
const achievements = await mcp__flow-nexus__achievements_list({
  user_id: "your_user_id"
});

console.log("Your Achievements:");
for (const a of achievements.achievements) {
  console.log(`🏆 ${a.name} - ${a.description}`);
  console.log(`   Earned: ${a.earned_at}`);
}

// Achievement categories
const categories = ["speed_demon", "problem_solver", "streak_master", "explorer"];

for (const category of categories) {
  const catAchievements = await mcp__flow-nexus__achievements_list({
    user_id: "your_user_id",
    category: category
  });

  console.log(`\n${category.replace('_', ' ').toUpperCase()}:`);
  console.log(`- Earned: ${catAchievements.achievements.length} achievements`);
}
```

### Example 3: Competing on Leaderboards

```javascript
// Global leaderboard
const globalBoard = await mcp__flow-nexus__leaderboard_get({
  type: "global",
  limit: 10
});

console.log("🌍 Global Leaderboard:");
for (const entry of globalBoard.rankings) {
  console.log(`#${entry.rank} ${entry.user} - ${entry.score} pts (${entry.challenges_completed} challenges)`);
}

// Weekly leaderboard
const weeklyBoard = await mcp__flow-nexus__leaderboard_get({
  type: "weekly",
  limit: 10
});

console.log("\n📅 This Week's Top Performers:");
for (const entry of weeklyBoard.rankings) {
  console.log(`#${entry.rank} ${entry.user} - ${entry.score} pts`);
}

// Challenge-specific leaderboard
const challengeBoard = await mcp__flow-nexus__leaderboard_get({
  type: "challenge",
  challenge_id: "specific_challenge_id",
  limit: 10
});

console.log("\n🎯 Challenge Leaderboard:");
for (const entry of challengeBoard.rankings) {
  console.log(`#${entry.rank} ${entry.user} - ${entry.score} pts (${entry.execution_time}ms)`);
}
```

### Example 4: Learning Path Progression

```javascript
// Start with beginner challenges
const beginnerChallenges = await mcp__flow-nexus__challenges_list({
  difficulty: "beginner",
  category: "algorithms"
});

console.log("📚 Learning Path: Algorithms");
console.log("Step 1: Beginner Challenges");

let completedCount = 0;
for (const challenge of beginnerChallenges.challenges.slice(0, 5)) {
  console.log(`- ${challenge.title} (${challenge.credits} credits)`);
}

// Progress to intermediate after completing beginner
if (completedCount >= 5) {
  const intermediateChallenges = await mcp__flow-nexus__challenges_list({
    difficulty: "intermediate",
    category: "algorithms"
  });

  console.log("\n🎯 Step 2: Intermediate Challenges Unlocked!");
  for (const challenge of intermediateChallenges.challenges.slice(0, 5)) {
    console.log(`- ${challenge.title} (${challenge.credits} credits)`);
  }
}
```

## Execution Checklist

- [ ] Browse challenges matching your skill level
- [ ] Read challenge description and constraints carefully
- [ ] Test solution in sandbox before submitting
- [ ] Submit solution for validation
- [ ] Review feedback if tests fail
- [ ] Collect credits on successful completion
- [ ] Check for unlocked achievements
- [ ] Review leaderboard position

## Best Practices

1. **Start at Your Level**: Begin with beginner challenges, progress gradually
2. **Understand First**: Read problem statement completely before coding
3. **Test Locally**: Use sandbox to test before submitting
4. **Optimize After**: Get it working first, then optimize
5. **Learn from Failures**: Use feedback to improve solutions
6. **Maintain Streaks**: Consistent daily practice builds skills

## Scoring Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 50% | All test cases pass |
| **Efficiency** | 25% | Time and space complexity |
| **Code Quality** | 15% | Clean, readable code |
| **Creativity** | 10% | Novel approaches |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `challenge_not_found` | Invalid challenge_id | Use `challenges_list` to find valid IDs |
| `submission_failed` | Runtime error or timeout | Check code syntax and efficiency |
| `time_limit_exceeded` | Solution too slow | Optimize algorithm complexity |
| `wrong_answer` | Incorrect output | Review logic and edge cases |
| `compilation_error` | Invalid syntax | Fix syntax errors |

## Metrics & Success Criteria

- **Completion Rate**: Target >70% first-attempt success
- **Average Score**: Target >80/100 on solved challenges
- **Streak Days**: Maintain 7+ day streaks
- **Rank Progress**: Improve leaderboard position weekly

## Integration Points

### With Sandboxes

```javascript
// Test solution in isolated environment
const sandbox = await mcp__flow-nexus__sandbox_create({
  template: "node"
});

await mcp__flow-nexus__sandbox_execute({
  sandbox_id: sandbox.sandbox_id,
  code: solutionCode
});
```

### With Payments

```javascript
// Credits earned from challenges
const balance = await mcp__flow-nexus__check_balance();
console.log(`Total credits from challenges: ${balance.challenge_earnings}`);
```

### Related Skills

- [cloud-sandbox](../cloud-sandbox/SKILL.md) - Test solutions
- [cloud-payments](../cloud-payments/SKILL.md) - Track earnings
- [cloud-auth](../cloud-auth/SKILL.md) - User management

## References

- [Flow Nexus Challenges](https://flow-nexus.ruv.io/challenges)
- [Leaderboards](https://flow-nexus.ruv.io/leaderboard)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-challenges agent
