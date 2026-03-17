---
skill_id: when-training-rl-agents-use-agentdb-learning
name: AgentDB Reinforcement Learning Training
version: 1.0.0
category: agentdb
subcategory: machine-learning
trigger_pattern: "when-training-rl-agents"
agents:
  - ml-developer
  - safla-neural
  - performance-benchmarker
complexity: advanced
estimated_duration: 6-10 hours
prerequisites:
  - AgentDB basics
  - Reinforcement learning fundamentals
  - Neural network knowledge
  - Python/TypeScript proficiency
outputs:
  - Trained RL agents
  - Learning plugin modules
  - Performance benchmarks
  - Deployment pipeline
validation_criteria:
  - Training converges successfully
  - Reward curve shows improvement
  - Agent passes validation tasks
  - Benchmarks meet targets
evidence_based_techniques:
  - Self-consistency validation
  - Program-of-thought decomposition
  - Chain-of-verification
  - Multi-agent consensus
metadata:
  author: claude-flow
  created: 2025-10-30
  updated: 2025-10-30
  tags:
    - agentdb
    - reinforcement-learning
    - neural-networks
    - ai-training
    - q-learning
---

# AgentDB Reinforcement Learning Training

## Overview

Train AI learning plugins with AgentDB's 9 reinforcement learning algorithms including Decision Transformer, Q-Learning, SARSA, Actor-Critic, PPO, and more. Build self-learning agents, implement RL, and optimize agent behavior through experience.

## When to Use This Skill

Use this skill when you need to:
- Train autonomous agents that learn from experience
- Implement reinforcement learning systems
- Optimize agent behavior through trial and error
- Build self-improving AI systems
- Deploy RL agents in production environments
- Benchmark and compare RL algorithms

## Available RL Algorithms

1. **Q-Learning** - Value-based, off-policy
2. **SARSA** - Value-based, on-policy
3. **Deep Q-Network (DQN)** - Deep RL with experience replay
4. **Actor-Critic** - Policy gradient with value baseline
5. **Proximal Policy Optimization (PPO)** - Trust region policy optimization
6. **Decision Transformer** - Offline RL with transformers
7. **Advantage Actor-Critic (A2C)** - Synchronous advantage estimation
8. **Twin Delayed DDPG (TD3)** - Continuous control
9. **Soft Actor-Critic (SAC)** - Maximum entropy RL

## SOP Framework: 5-Phase RL Training Deployment

### Phase 1: Initialize Learning Environment (1-2 hours)

**Objective:** Setup AgentDB learning infrastructure with environment configuration

**Agent:** ml-developer

**Steps:**

1. **Install AgentDB Learning Module**
```bash
npm install agentdb-learning@latest
npm install @agentdb/rl-algorithms @agentdb/environments
```

2. **Initialize learning database**
```typescript
import { AgentDB, LearningPlugin } from 'agentdb-learning';

const learningDB = new AgentDB({
  name: 'rl-training-db',
  dimensions: 512, // State embedding dimension
  learning: {
    enabled: true,
    persistExperience: true,
    replayBufferSize: 100000
  }
});

await learningDB.initialize();

// Create learning plugin
const learningPlugin = new LearningPlugin({
  database: learningDB,
  algorithms: ['q-learning', 'dqn', 'ppo', 'actor-critic'],
  config: {
    batchSize: 64,
    learningRate: 0.001,
    discountFactor: 0.99,
    explorationRate: 1.0,
    explorationDecay: 0.995
  }
});

await learningPlugin.initialize();
```

3. **Define environment**
```typescript
import { Environment } from '@agentdb/environments';

const environment = new Environment({
  name: 'grid-world',
  stateSpace: {
    type: 'continuous',
    shape: [10, 10],
    bounds: [[0, 10], [0, 10]]
  },
  actionSpace: {
    type: 'discrete',
    actions: ['up', 'down', 'left', 'right']
  },
  rewardFunction: (state, action, nextState) => {
    // Distance to goal reward
    const goalDistance = Math.sqrt(
      Math.pow(nextState[0] - 9, 2) +
      Math.pow(nextState[1] - 9, 2)
    );
    return -goalDistance + (goalDistance === 0 ? 100 : 0);
  },
  terminalCondition: (state) => {
    return state[0] === 9 && state[1] === 9; // Reached goal
  }
});

await environment.initialize();
```

4. **Setup monitoring**
```typescript
const monitor = learningPlugin.createMonitor({
  metrics: ['reward', 'loss', 'exploration-rate', 'episode-length'],
  logInterval: 100, // Log every 100 episodes
  saveCheckpoints: true,
  checkpointInterval: 1000
});

monitor.on('episode-complete', (episode) => {
  console.log('Episode:', episode.number, 'Reward:', episode.totalReward);
});
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/learning/environment', {
  name: environment.name,
  stateSpace: environment.stateSpace,
  actionSpace: environment.actionSpace,
  initialized: Date.now()
});
```

**Validation:**
- Learning database initialized
- Environment configured and tested
- Monitor capturing metrics
- Configuration stored in memory

### Phase 2: Configure RL Algorithm (1-2 hours)

**Objective:** Select and configure RL algorithm for the learning task

**Agent:** ml-developer

**Steps:**

1. **Select algorithm**
```typescript
// Example: Deep Q-Network (DQN)
const dqnAgent = learningPlugin.createAgent({
  algorithm: 'dqn',
  config: {
    networkArchitecture: {
      layers: [
        { type: 'dense', units: 128, activation: 'relu' },
        { type: 'dense', units: 128, activation: 'relu' },
        { type: 'dense', units: environment.actionSpace.size, activation: 'linear' }
      ]
    },
    learningRate: 0.001,
    batchSize: 64,
    replayBuffer: {
      size: 100000,
      prioritized: true,
      alpha: 0.6,
      beta: 0.4
    },
    targetNetwork: {
      updateFrequency: 1000,
      tauSync: 0.001 // Soft update
    },
    exploration: {
      initial: 1.0,
      final: 0.01,
      decay: 0.995
    },
    training: {
      startAfter: 1000, // Start training after 1000 experiences
      updateFrequency: 4
    }
  }
});

await dqnAgent.initialize();
```

2. **Configure hyperparameters**
```typescript
const hyperparameters = {
  // Learning parameters
  learningRate: 0.001,
  discountFactor: 0.99, // Gamma
  batchSize: 64,

  // Exploration
  epsilonStart: 1.0,
  epsilonEnd: 0.01,
  epsilonDecay: 0.995,

  // Experience replay
  replayBufferSize: 100000,
  minReplaySize: 1000,
  prioritizedReplay: true,

  // Training
  maxEpisodes: 10000,
  maxStepsPerEpisode: 1000,
  targetUpdateFrequency: 1000,

  // Evaluation
  evalFrequency: 100,
  evalEpisodes: 10
};

dqnAgent.setHyperparameters(hyperparameters);
```

3. **Setup experience replay**
```typescript
import { PrioritizedReplayBuffer } from '@agentdb/rl-algorithms';

const replayBuffer = new PrioritizedReplayBuffer({
  capacity: 100000,
  alpha: 0.6, // Prioritization exponent
  beta: 0.4, // Importance sampling
  betaIncrement: 0.001,
  epsilon: 0.01 // Small constant for stability
});

dqnAgent.setReplayBuffer(replayBuffer);
```

4. **Configure training loop**
```typescript
const trainingConfig = {
  episodes: 10000,
  stepsPerEpisode: 1000,
  warmupSteps: 1000,
  trainFrequency: 4,
  targetUpdateFrequency: 1000,
  saveFrequency: 1000,
  evalFrequency: 100,
  earlyStoppingPatience: 500,
  earlyStoppingThreshold: 0.01
};

dqnAgent.setTrainingConfig(trainingConfig);
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/learning/algorithm-config', {
  algorithm: 'dqn',
  hyperparameters: hyperparameters,
  trainingConfig: trainingConfig,
  configured: Date.now()
});
```

**Validation:**
- Algorithm selected and configured
- Hyperparameters validated
- Replay buffer initialized
- Training config set

### Phase 3: Train Agents (3-4 hours)

**Objective:** Execute training iterations and optimize agent behavior

**Agent:** safla-neural

**Steps:**

1. **Start training loop**
```typescript
async function trainAgent() {
  console.log('Starting RL training...');

  const trainingStats = {
    episodes: [],
    totalReward: [],
    episodeLength: [],
    loss: [],
    explorationRate: []
  };

  for (let episode = 0; episode < trainingConfig.episodes; episode++) {
    let state = await environment.reset();
    let episodeReward = 0;
    let episodeLength = 0;
    let episodeLoss = 0;

    for (let step = 0; step < trainingConfig.stepsPerEpisode; step++) {
      // Select action
      const action = await dqnAgent.selectAction(state, {
        explore: true
      });

      // Execute action
      const { nextState, reward, done } = await environment.step(action);

      // Store experience
      await dqnAgent.storeExperience({
        state,
        action,
        reward,
        nextState,
        done
      });

      // Train if enough experiences
      if (dqnAgent.canTrain()) {
        const loss = await dqnAgent.train();
        episodeLoss += loss;
      }

      episodeReward += reward;
      episodeLength += 1;
      state = nextState;

      if (done) break;
    }

    // Update target network
    if (episode % trainingConfig.targetUpdateFrequency === 0) {
      await dqnAgent.updateTargetNetwork();
    }

    // Decay exploration
    dqnAgent.decayExploration();

    // Log progress
    trainingStats.episodes.push(episode);
    trainingStats.totalReward.push(episodeReward);
    trainingStats.episodeLength.push(episodeLength);
    trainingStats.loss.push(episodeLoss / episodeLength);
    trainingStats.explorationRate.push(dqnAgent.getExplorationRate());

    if (episode % 100 === 0) {
      console.log(`Episode ${episode}:`, {
        reward: episodeReward.toFixed(2),
        length: episodeLength,
        loss: (episodeLoss / episodeLength).toFixed(4),
        epsilon: dqnAgent.getExplorationRate().toFixed(3)
      });
    }

    // Save checkpoint
    if (episode % trainingConfig.saveFrequency === 0) {
      await dqnAgent.save(`checkpoint-${episode}`);
    }

    // Evaluate
    if (episode % trainingConfig.evalFrequency === 0) {
      const evalReward = await evaluateAgent(dqnAgent, environment);
      console.log(`Evaluation at episode ${episode}: ${evalReward.toFixed(2)}`);
    }

    // Early stopping
    if (checkEarlyStopping(trainingStats, episode)) {
      console.log('Early stopping triggered');
      break;
    }
  }

  return trainingStats;
}

const trainingStats = await trainAgent();
```

2. **Monitor training progress**
```typescript
monitor.on('training-update', (stats) => {
  // Calculate moving averages
  const window = 100;
  const recentRewards = stats.totalReward.slice(-window);
  const avgReward = recentRewards.reduce((a, b) => a + b, 0) / recentRewards.length;

  // Store metrics
  agentDB.memory.store('agentdb/learning/training-progress', {
    episode: stats.episodes[stats.episodes.length - 1],
    avgReward: avgReward,
    explorationRate: stats.explorationRate[stats.explorationRate.length - 1],
    timestamp: Date.now()
  });

  // Plot learning curve (if visualization enabled)
  if (monitor.visualization) {
    monitor.plot('reward-curve', stats.episodes, stats.totalReward);
    monitor.plot('loss-curve', stats.episodes, stats.loss);
  }
});
```

3. **Handle convergence**
```typescript
function checkConvergence(stats, windowSize = 100, threshold = 0.01) {
  if (stats.totalReward.length < windowSize * 2) {
    return false;
  }

  const recent = stats.totalReward.slice(-windowSize);
  const previous = stats.totalReward.slice(-windowSize * 2, -windowSize);

  const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
  const previousAvg = previous.reduce((a, b) => a + b, 0) / previous.length;

  const improvement = (recentAvg - previousAvg) / Math.abs(previousAvg);

  return improvement < threshold;
}
```

4. **Save trained model**
```typescript
await dqnAgent.save('trained-agent-final', {
  includeReplayBuffer: false,
  includeOptimizer: false,
  metadata: {
    trainingStats: trainingStats,
    hyperparameters: hyperparameters,
    finalReward: trainingStats.totalReward[trainingStats.totalReward.length - 1]
  }
});

console.log('Training complete. Model saved.');
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/learning/training-results', {
  algorithm: 'dqn',
  episodes: trainingStats.episodes.length,
  finalReward: trainingStats.totalReward[trainingStats.totalReward.length - 1],
  converged: checkConvergence(trainingStats),
  modelPath: 'trained-agent-final',
  timestamp: Date.now()
});
```

**Validation:**
- Training completed or converged
- Reward curve shows improvement
- Model saved successfully
- Training stats stored

### Phase 4: Validate Performance (1-2 hours)

**Objective:** Benchmark trained agent and validate performance

**Agent:** performance-benchmarker

**Steps:**

1. **Load trained agent**
```typescript
const trainedAgent = await learningPlugin.loadAgent('trained-agent-final');
```

2. **Run evaluation episodes**
```typescript
async function evaluateAgent(agent, env, numEpisodes = 100) {
  const results = {
    rewards: [],
    episodeLengths: [],
    successRate: 0
  };

  for (let i = 0; i < numEpisodes; i++) {
    let state = await env.reset();
    let episodeReward = 0;
    let episodeLength = 0;
    let success = false;

    for (let step = 0; step < 1000; step++) {
      const action = await agent.selectAction(state, { explore: false });
      const { nextState, reward, done } = await env.step(action);

      episodeReward += reward;
      episodeLength += 1;
      state = nextState;

      if (done) {
        success = env.isSuccessful(state);
        break;
      }
    }

    results.rewards.push(episodeReward);
    results.episodeLengths.push(episodeLength);
    if (success) results.successRate += 1;
  }

  results.successRate /= numEpisodes;

  return {
    meanReward: results.rewards.reduce((a, b) => a + b, 0) / results.rewards.length,
    stdReward: calculateStd(results.rewards),
    meanLength: results.episodeLengths.reduce((a, b) => a + b, 0) / results.episodeLengths.length,
    successRate: results.successRate,
    results: results
  };
}

const evalResults = await evaluateAgent(trainedAgent, environment, 100);
console.log('Evaluation results:', evalResults);
```

3. **Compare with baseline**
```typescript
// Random policy baseline
const randomAgent = learningPlugin.createAgent({ algorithm: 'random' });
const randomResults = await evaluateAgent(randomAgent, environment, 100);

// Calculate improvement
const improvement = {
  rewardImprovement: (evalResults.meanReward - randomResults.meanReward) / Math.abs(randomResults.meanReward),
  lengthImprovement: (randomResults.meanLength - evalResults.meanLength) / randomResults.meanLength,
  successImprovement: evalResults.successRate - randomResults.successRate
};

console.log('Improvement over random:', improvement);
```

4. **Run comprehensive benchmarks**
```typescript
const benchmarks = {
  performanceMetrics: {
    meanReward: evalResults.meanReward,
    stdReward: evalResults.stdReward,
    successRate: evalResults.successRate,
    meanEpisodeLength: evalResults.meanLength
  },
  algorithmComparison: {
    dqn: evalResults,
    random: randomResults,
    improvement: improvement
  },
  inferenceTiming: {
    actionSelection: 0,
    totalEpisode: 0
  }
};

// Measure inference speed
const timingTrials = 1000;
const startTime = performance.now();
for (let i = 0; i < timingTrials; i++) {
  const state = await environment.randomState();
  await trainedAgent.selectAction(state, { explore: false });
}
const endTime = performance.now();
benchmarks.inferenceTiming.actionSelection = (endTime - startTime) / timingTrials;

await agentDB.memory.store('agentdb/learning/benchmarks', benchmarks);
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/learning/validation', {
  evaluated: true,
  meanReward: evalResults.meanReward,
  successRate: evalResults.successRate,
  improvement: improvement,
  timestamp: Date.now()
});
```

**Validation:**
- Evaluation completed (100 episodes)
- Mean reward exceeds threshold
- Success rate acceptable
- Improvement over baseline demonstrated

### Phase 5: Deploy Trained Agents (1-2 hours)

**Objective:** Deploy trained agents to production environment

**Agent:** ml-developer

**Steps:**

1. **Export production model**
```typescript
await trainedAgent.export('production-agent', {
  format: 'onnx', // or 'tensorflowjs', 'pytorch'
  optimize: true,
  quantize: 'int8', // Quantization for faster inference
  includeMetadata: true
});
```

2. **Create inference API**
```typescript
import express from 'express';

const app = express();
app.use(express.json());

// Load production agent
const productionAgent = await learningPlugin.loadAgent('production-agent');

app.post('/api/predict', async (req, res) => {
  try {
    const { state } = req.body;

    const action = await productionAgent.selectAction(state, {
      explore: false,
      returnProbabilities: true
    });

    res.json({
      action: action.action,
      probabilities: action.probabilities,
      confidence: action.confidence
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('RL agent API running on port 3000');
});
```

3. **Setup monitoring**
```typescript
import { ProductionMonitor } from '@agentdb/monitoring';

const prodMonitor = new ProductionMonitor({
  agent: productionAgent,
  metrics: ['inference-latency', 'action-distribution', 'reward-feedback'],
  alerting: {
    latencyThreshold: 100, // ms
    anomalyDetection: true
  }
});

await prodMonitor.start();
```

4. **Create deployment pipeline**
```typescript
const deploymentPipeline = {
  stages: [
    {
      name: 'validation',
      steps: [
        'Load trained model',
        'Run validation suite',
        'Check performance metrics',
        'Verify inference speed'
      ]
    },
    {
      name: 'export',
      steps: [
        'Export to production format',
        'Optimize model',
        'Quantize weights',
        'Package artifacts'
      ]
    },
    {
      name: 'deployment',
      steps: [
        'Deploy to staging',
        'Run smoke tests',
        'Deploy to production',
        'Monitor performance'
      ]
    }
  ]
};

await agentDB.memory.store('agentdb/learning/deployment-pipeline', deploymentPipeline);
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/learning/production', {
  deployed: true,
  modelPath: 'production-agent',
  apiEndpoint: 'http://localhost:3000/api/predict',
  monitoring: true,
  timestamp: Date.now()
});
```

**Validation:**
- Model exported successfully
- API running and responding
- Monitoring active
- Deployment pipeline documented

## Integration Scripts

### Complete Training Script

```bash
#!/bin/bash
# train-rl-agent.sh

set -e

echo "AgentDB RL Training Script"
echo "=========================="

# Phase 1: Initialize
echo "Phase 1: Initializing learning environment..."
npm install agentdb-learning @agentdb/rl-algorithms

# Phase 2: Configure
echo "Phase 2: Configuring algorithm..."
node -e "require('./config-algorithm.js')"

# Phase 3: Train
echo "Phase 3: Training agent..."
node -e "require('./train-agent.js')"

# Phase 4: Validate
echo "Phase 4: Validating performance..."
node -e "require('./evaluate-agent.js')"

# Phase 5: Deploy
echo "Phase 5: Deploying to production..."
node -e "require('./deploy-agent.js')"

echo "Training complete!"
```

### Quick Start Script

```typescript
// quickstart-rl.ts
import { setupRLTraining } from './setup';

async function quickStart() {
  console.log('Starting RL training quick setup...');

  // Setup
  const { learningDB, environment, agent } = await setupRLTraining({
    algorithm: 'dqn',
    environment: 'grid-world',
    episodes: 1000
  });

  // Train
  console.log('Training agent...');
  const stats = await agent.train(environment, {
    episodes: 1000,
    logInterval: 100
  });

  // Evaluate
  console.log('Evaluating agent...');
  const results = await agent.evaluate(environment, {
    episodes: 100
  });
  console.log('Results:', results);

  // Save
  await agent.save('quickstart-agent');
  console.log('Quick start complete!');
}

quickStart().catch(console.error);
```

## Evidence-Based Success Criteria

1. **Training Convergence (Self-Consistency)**
   - Reward curve stabilizes
   - Moving average improvement < 1%
   - Agent achieves consistent performance

2. **Performance Benchmarks (Quantitative)**
   - Mean reward exceeds baseline by 50%
   - Success rate > 80%
   - Inference time < 10ms per action

3. **Algorithm Validation (Chain-of-Verification)**
   - Hyperparameters validated
   - Exploration-exploitation balanced
   - Experience replay functioning

4. **Production Readiness (Multi-Agent Consensus)**
   - Model exported successfully
   - API responds within latency threshold
   - Monitoring active and alerting
   - Deployment pipeline documented

## Additional Resources

- AgentDB Learning Documentation: https://agentdb.dev/docs/learning
- RL Algorithms Guide: https://agentdb.dev/docs/rl-algorithms
- Training Best Practices: https://agentdb.dev/docs/training
- Production Deployment: https://agentdb.dev/docs/deployment
