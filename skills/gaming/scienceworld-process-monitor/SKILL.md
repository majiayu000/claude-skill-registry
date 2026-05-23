---
name: scienceworld-process-monitor
description: This skill observes the state of an active apparatus and its contents to track progress. It should be triggered periodically during a heating or reaction process to check for state changes (e.g., solid to liquid). The skill uses 'look at' or 'examine' actions on the apparatus and substance.
---
# Process Monitoring Protocol

## Purpose
Monitor an ongoing scientific process (e.g., heating, reaction) to detect state changes in the target substance and track progress toward a goal.

## Trigger Conditions
Activate this skill when:
1. An apparatus (e.g., stove, burner) is **active** (`activated` state).
2. A target substance is contained within or on the apparatus.
3. You need to determine if a phase/state transition has occurred (e.g., solid → liquid).

## Core Procedure
1.  **Observe the Apparatus**: Use `look at <APPARATUS>` to verify the apparatus is active and contains the target substance.
2.  **Inspect the Substance**: Use `examine <SUBSTANCE>` to check its current state description.
3.  **Record Observations**: Note any change in the substance's state description (e.g., "chocolate" → "liquid chocolate").

## Key Principles
*   **Periodic Execution**: Run this skill every few steps during an active process. Do not spam actions.
*   **State-Driven**: The skill's findings (state change detected or not) should inform the next step in the overarching experiment.
*   **Non-Destructive**: This skill only observes. It does not modify temperatures, turn equipment on/off, or handle substances.

## Integration with Other Skills
The output of this skill (e.g., "substance melted") should be passed to a decision-making skill (e.g., `scienceworld-measurement`) to take the next appropriate action, such as taking a final temperature reading or deactivating the apparatus.

## Example from Trajectory
*   **Apparatus**: `stove`
*   **Substance**: `chocolate`
*   **Initial State**: `chocolate`
*   **Monitoring Action**: `examine chocolate`
*   **Observed State Change**: `liquid chocolate`
*   **Next Action**: Trigger a temperature measurement skill.
