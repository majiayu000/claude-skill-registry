---
name: active-inference
description: Apply Active Inference to minimize prediction error (Surprise).
context_cost: medium
tools: [run_command, read_file]
---

# Active Inference Skill

> "Action is the process of changing the world to match your prediction."

## 1. The Concept (Free Energy Principle)
Standard agents are "Goal-Directed" (Maximize Reward). **Active Inference** agents are "Surprise-Minimizing" (Minimize Prediction Error).
- **Goal:** Not just to "win", but to understand and control.
- **Surprise:** The difference between *Expectation* and *Observation*.

## 2. The Feedback Loop
1.  **Predict:** "If I run `go test`, it will output PASS."
2.  **Act/Sense:** Run the command and read the output.
3.  **Compare:** Calculate **Prediction Error**.
    - *Result:* "FAIL". -> **Surprise!**

## 3. Solving the Error
You have two choices to minimize surprise:
1.  **Perceptual Inference (Change Mind):** "My model was wrong. The code implies X, not Y." -> Update docs/mental model.
2.  **Active Inference (Change World):** "The code is wrong. I will edit it to make the test pass." -> Writes code.

## 4. Epistemic Action (Curiosity)
If Surprise is "Unknown" (Uncertainty is high), perform an **Epistemic Action** (Probe/Log) to gain information, rather than a pragmatic action to achieve a goal.

## 5. System Prompt Template

```markdown
You are an Active Inference Agent. Your goal is to minimize "Surprise".

### Your Cycle
1.  **PREDICT**: Based on your internal model, what do you expect to see next?
2.  **OBSERVE**: Look at the actual tool output or user input.
3.  **COMPARE**: Calculate the Prediction Error (Surprise).
4.  **RESOLVE**:
    - If Surprise is HIGH:
        - **Epistemic Action**: Gather more info to update your model.
        - **Pragmatic Action**: Act to force the world to match your prediction.
    - If Surprise is LOW:
        - Proceed with standard goal execution.

### Current State
- **Goal**: {{user_goal}}
- **Expectation**: {{current_expectation}}
- **Observation**: {{last_tool_output}}
```

## 6. Implementation (Pythonic Pseudo-code)

```python
def active_inference_step(agent, observation):
    prediction = agent.predict()
    surprise = calculate_divergence(prediction, observation)
    
    if surprise > THRESHOLD:
        if agent.uncertainty > 0.8:
            return "explore_environment" # Epistemic
        else:
            return "correct_environment" # Pragmatic (Active Inference)
    else:
        return "continue_goal"
```
