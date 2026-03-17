---
name: run-simulation
description: Create or run simulation features for analyzing work flow through value streams
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: Create Simulation Feature

Add a new simulation or what-if scenario feature.

## Usage

```
/run-simulation <feature-name>
```

## Prerequisites

Create a feature file first using `/new-feature` that describes:
- What the simulation models
- What parameters users can configure
- What insights users gain from the simulation

## Example Feature File

```gherkin
Feature: Work Flow Simulation
  As a team analyzing their process
  I want to simulate work flowing through our value stream
  So that I can identify bottlenecks and queuing problems

  Scenario: Run basic flow simulation
    Given a value stream with 3 steps
    And each step has capacity for 1 item at a time
    When I add 5 work items to the queue
    And run the simulation
    Then I should see items move through each step
    And completed items should appear at the end

  Scenario: Identify bottleneck through simulation
    Given a value stream where step 2 takes twice as long as others
    When I run the simulation with 10 work items
    Then step 2 should show the largest queue buildup
    And it should be highlighted as a bottleneck

  Scenario: Adjust batch size and see impact
    Given a value stream with batch size of 5 at deployment
    When I change batch size to 1
    And run the simulation comparison
    Then I should see reduced lead time in the smaller batch scenario
```

## Architecture

Simulations follow this pattern:

1. **Configuration** - User sets parameters via UI
2. **Engine** - Pure functions that calculate state transitions
3. **Visualization** - React components that display animation
4. **Results** - Metrics and insights from the simulation run

## Implementation Steps

1. Define simulation parameters in `src/utils/simulation/{feature}.js`
2. Create the simulation engine as pure functions
3. Add configuration UI in `src/components/simulation/{Feature}Config.jsx`
4. Create visualization component in `src/components/simulation/{Feature}Viz.jsx`
5. Add results display in `src/components/simulation/{Feature}Results.jsx`
6. Write thorough tests for the simulation logic

## Simulation Engine Pattern

```javascript
// src/utils/simulation/{feature}.js

/**
 * Initialize simulation state
 * @param {Object} vsm - Value stream map
 * @param {Object} config - Simulation configuration
 * @returns {Object} Initial simulation state
 */
export function initializeSimulation(vsm, config) {
  return {
    currentTick: 0,
    workItems: Array.from({ length: config.workItemCount }, (_, i) => ({
      id: `item-${i}`,
      currentStep: null,
      stepProgress: 0,
      history: []
    })),
    stepStates: new Map(vsm.steps.map(step => [
      step.id,
      { queue: [], processing: null, completed: 0 }
    ])),
    metrics: {
      throughput: 0,
      avgCycleTime: 0,
      maxQueueSize: 0
    }
  };
}

/**
 * Simulate one tick of the system
 * Pure function: returns new state without mutation
 * @param {Object} state - Current simulation state
 * @param {Object} vsm - Value stream map
 * @returns {Object} New simulation state
 */
export function simulateTick(state, vsm) {
  // Create new state object (immutable)
  const newState = {
    ...state,
    currentTick: state.currentTick + 1,
    workItems: [...state.workItems],
    stepStates: new Map(state.stepStates)
  };

  // Process each step
  for (const step of vsm.steps) {
    // Move completed work to next step
    // Process work in progress
    // Pull from queue if capacity available
  }

  // Update metrics
  newState.metrics = calculateMetrics(newState);

  return newState;
}

/**
 * Run complete simulation
 * @param {Object} vsm - Value stream map
 * @param {Object} config - Simulation configuration
 * @returns {Object} Simulation results with history
 */
export function runSimulation(vsm, config) {
  let state = initializeSimulation(vsm, config);
  const history = [state];

  for (let i = 0; i < config.ticks; i++) {
    state = simulateTick(state, vsm);
    history.push(state);
  }

  return {
    finalState: state,
    history,
    insights: analyzeResults(history, vsm)
  };
}
```

## Visualization Component

```jsx
// src/components/simulation/{Feature}Viz.jsx

import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

function {Feature}Viz({ simulationHistory, speed }) {
  const [currentFrame, setCurrentFrame] = useState(0);

  useEffect(() => {
    if (currentFrame >= simulationHistory.length - 1) return;

    const timer = setTimeout(() => {
      setCurrentFrame(f => f + 1);
    }, 1000 / speed);

    return () => clearTimeout(timer);
  }, [currentFrame, simulationHistory.length, speed]);

  const state = simulationHistory[currentFrame];

  return (
    <div data-testid="simulation-viz">
      <div className="simulation-controls">
        <span>Tick: {state.currentTick}</span>
        <button onClick={() => setCurrentFrame(0)}>Reset</button>
      </div>
      <div className="simulation-canvas">
        {/* Render work items at their current positions */}
      </div>
    </div>
  );
}

{Feature}Viz.propTypes = {
  simulationHistory: PropTypes.array.isRequired,
  speed: PropTypes.number
};

{Feature}Viz.defaultProps = {
  speed: 1
};

export default {Feature}Viz;
```

## Key Simulation Concepts

- **Tick**: One unit of simulation time
- **Work Item**: An individual unit flowing through the system
- **Step State**: Current status of a process step (idle, processing, blocked)
- **Queue**: Work items waiting to enter a step
- **Throughput**: Items completed per time unit
- **Cycle Time**: Time for one item to traverse the entire stream
