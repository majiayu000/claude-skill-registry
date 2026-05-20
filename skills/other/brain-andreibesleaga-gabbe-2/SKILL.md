---
name: sensory-motor
description: Embodied cognition patterns for treating tools as muscles and inputs as senses.
context_cost: medium
tools: [run_command, read_file]
---

# Sensory-Motor Skill (Embodied Cognition)

> "Intelligence is not a brain in a jar; it is a body in a world."

## 1. The Body Schema (Proprioception)
An agent must know the state of its "Body" (its available tools and context).
- **Senses:** `read_file`, `list_dir`, `search_web`.
- **Muscles:** `write_to_file`, `run_command`, `replace_file_content`.
- **Proprioception:** "Do I have write access here?", "Is the linter running?", "What is my current working directory?"

## 2. Multimodal Binding (Perception)
Inputs are not just strings; they are "Percepts" that must be bound together.
- **Visual:** Screenshots, images.
- **Auditory:** Text-to-speech logs.
- **Symbolic:** Code, JSON.
- **The Binding Problem:** You must integrate `Visual(Error Screenshot)` + `Symbolic(Log File)` into a unified `Concept(System Failure)`.

## 3. Optimal Feedback Control (Action)
Do not just "fire and forget" commands. Control the "Limb" (Tool) continuously.
1.  **Motor Command:** `run_command(npm test)`
2.  **Sensory Feedback:** *Command is taking too long...*
3.  **Correction:** `send_command_input(Ctrl+C)` (Reflex arc).

## 4. System Prompt Parameters

```markdown
### Body State (Proprioception)
- **Muscles Available**: [Bash, Python, FileSystem]
- **Senses Active**: [Linter, TestRunner, Browser]
- **Health**: [Filesystem: RW, Network: Connected]

### Motor Control Policy
"I will not just execute; I will monitor. If a tool fails (muscle failure), I will not hallucinate success. I will acknowledge the physical limitation and try a different strategy."
```

## 5. Implementation Example

```python
def execute_motor_command(command):
    # 1. Forward Model: Predict outcome
    expected_duration = estimate_duration(command)
    
    # 2. Motor Command
    process = subprocess.Popen(command)
    
    # 3. Feedback Loop (OFC)
    start_time = time.time()
    while process.poll() is None:
        if time.time() - start_time > expected_duration * 1.5:
             # Reflex: Abort!
             process.kill()
             raise MotorError("Muscle fatigue (Timeout)")
             
    return process.returncode
```
