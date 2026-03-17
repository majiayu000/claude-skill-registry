---
name: "extract-physical-ai-formulas"
description: "Extract and explain formulas used in Physical AI and Humanoid Robotics from text, lecture notes, or papers. Use when user asks to identify or understand relevant formulas."
version: "1.0.0"
---

# Physical AI Formula Extraction Skill

## When to Use This Skill

- User asks to "extract formulas" or "find equations" related to Physical AI or Humanoid Robotics  
- User provides textbooks, lecture notes, or research papers with formulas  
- User wants formulas explained with units, meaning, and practical applications  

## Procedure

1. **Read the text**: Identify all mathematical formulas related to Physical AI, robotics, or control systems  
2. **Format formulas**: Convert formulas into clear LaTeX or plain-text notation  
3. **Explain formulas**: Provide a brief description, meaning of variables, and units  
4. **Provide examples**: Give small, practical examples when possible  
5. **Optional context**: Link formulas to applications in humanoid robotics, sensors, actuators, or control systems  

## Output Format

**Formula**: The extracted formula in LaTeX or plain-text  
**Description**: Explanation of the formula and its purpose  
**Variables / Units**: Meaning and units of each variable  
**Application / Example**: How the formula is used in robotics  

## Quality Criteria

- Formulas must be **accurate and correctly formatted**  
- Explanations should be **clear and concise**  
- Include **observable outcomes or examples** when possible  
- Maintain **relevance to Physical AI and humanoid robotics**  

## Example

**Input**: "The torque τ required for a robotic joint can be calculated using τ = I * α, where I is the moment of inertia and α is the angular acceleration."

**Output**:  
- **Formula**: τ = I * α  
- **Description**: Torque τ equals the moment of inertia I multiplied by angular acceleration α  
- **Variables / Units**: τ [Nm], I [kg·m²], α [rad/s²]  
- **Application / Example**: Used to calculate torque requirements for joint actuators in humanoid robots
