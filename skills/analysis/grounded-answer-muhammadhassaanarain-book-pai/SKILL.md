---
name: "grounded-answer"
description: "Provide accurate, evidence-based answers by referencing sources from documents, textbooks, or research papers. Use when user asks for factual or source-backed responses."
version: "1.0.0"
---

# Grounded Answer Skill

## When to Use This Skill

- User asks a factual question related to robotics, Physical AI, or related fields  
- User requests answers supported by sources, references, or documents  
- User wants explanations with **verifiable evidence**  

## Procedure

1. **Understand the question**: Identify the key information requested  
2. **Search the knowledge base**: Look through provided documents, textbooks, or research papers  
3. **Select relevant sources**: Choose the most accurate and reliable references  
4. **Generate grounded answer**: Summarize the information clearly, citing sources  
5. **Optional explanations**: Include additional context, formulas, or examples if needed  

## Output Format

**Answer**: Concise, clear response to the question  
**Sources / References**: List of supporting documents, papers, or textbook sections  
**Explanation / Details** (Optional): Additional context, formulas, or examples for clarity  

## Quality Criteria

- Answers must be **accurate and factual**  
- Always **cite sources** when possible  
- Avoid speculation; if no source is available, indicate uncertainty  
- Maintain **clarity and relevance** for the user  

## Example

**Input**: "Explain the role of torque in humanoid robot joint control."

**Output**:  
- **Answer**: Torque is the rotational force applied at a robot joint, determining the joint’s angular acceleration according to τ = I * α. Proper torque control ensures stable and precise movement in humanoid robots.  
- **Sources / References**:  
  1. "Introduction to Robotics: Mechanics and Control" – Chapter 6, Joint Dynamics  
  2. Lecture notes on Humanoid Robotics, Kinematics and Dynamics section  
- **Explanation / Details**: The moment of inertia I and angular acceleration α define the required torque. Torque control is essential for walking, grasping, and manipulation tasks.
