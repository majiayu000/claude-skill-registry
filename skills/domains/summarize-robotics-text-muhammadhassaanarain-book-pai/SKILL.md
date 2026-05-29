---
name: "summarize-robotics-text"
description: "Summarize robotics-related text, research papers, or lecture notes into concise, clear, and structured summaries. Use when user asks to condense or simplify robotics content."
version: "1.0.0"
---

# Robotics Text Summarization Skill

## When to Use This Skill

- User asks to "summarize robotics text" or "condense content"  
- User provides research papers, lecture notes, or articles related to robotics, humanoid systems, or Physical AI  
- User wants a structured, easy-to-read summary with key concepts highlighted  

## Procedure

1. **Understand the text**: Identify the main topic, context, and target audience  
2. **Extract key points**: Focus on important concepts, formulas, techniques, and findings  
3. **Organize content**: Group information logically (e.g., Introduction → Methods → Applications → Conclusion)  
4. **Summarize**: Condense into concise paragraphs or bullet points without losing critical information  
5. **Optional highlights**: Include formulas, diagrams references, or real-world examples if relevant  

## Output Format

**Title/Topic**: Name of the text or article  
**Summary**: 3-5 concise paragraphs or numbered bullet points covering key concepts  
**Key Terms / Formulas**: List of important terms, variables, and formulas mentioned in the text  
**Applications / Insights**: Brief description of practical implications or real-world applications  

## Quality Criteria

- Summaries should be **concise but comprehensive**  
- Preserve **technical accuracy** and critical information  
- Use **clear language**, suitable for students or engineers in robotics  
- Include **formulas or definitions** if central to the text  

## Example

**Input**: "Summarize a lecture note on kinematics and dynamics of humanoid robots"

**Output**:  
- **Title/Topic**: Kinematics and Dynamics of Humanoid Robots  
- **Summary**:  
  1. Humanoid robots require precise kinematic modeling to compute joint positions and velocities.  
  2. Forward and inverse kinematics allow mapping between joint angles and end-effector positions.  
  3. Dynamics involves calculating forces and torques based on mass, inertia, and acceleration.  
  4. Control strategies use these models to ensure smooth and stable motion.  
- **Key Terms / Formulas**: Forward kinematics, inverse kinematics, τ = I * α, Jacobian matrix  
- **Applications / Insights**: Essential for designing walking, grasping, and manipulation tasks in humanoid robots
