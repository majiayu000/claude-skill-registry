---
name: "learning-objective-generator"
description: "Generate clear, measurable, and curriculum-aligned learning objectives for any topic. Use when user asks to define goals, outcomes, or objectives for a lesson or course."
version: "1.0.0"
---

# Learning Objective Generator Skill

## When to Use This Skill

- User asks to "create learning objectives" or "define course outcomes"
- User mentions topics, modules, or skills to teach
- User wants objectives that are specific, measurable, and actionable

## Procedure

1. **Understand the topic**: Clarify subject, target audience, and skill level
2. **Determine cognitive level**: Apply Bloom’s taxonomy (Remember, Understand, Apply, Analyze, Evaluate, Create)
3. **Draft objectives**: Write 3-5 concise objectives per topic/module
4. **Ensure measurability**: Include action verbs and observable outcomes
5. **Optional alignment**: Map objectives to curriculum standards or assessments

## Output Format

**Topic/Module**: Name of the topic or module  
**Learning Objectives**: Numbered list of 3-5 clear, measurable objectives  
**Cognitive Level**: Indicate Bloom’s taxonomy level for each objective  

## Quality Criteria

- Objectives are **specific and measurable** (e.g., "Describe the steps of kinematic analysis" not "Understand kinematics")  
- Use **action verbs** (e.g., identify, explain, demonstrate, design, evaluate)  
- Align with the **target audience skill level**  
- Include **observable outcomes** where possible  

## Example

**Input**: "Generate learning objectives for a lesson on robotic joint control"

**Output**:  
- **Topic/Module**: Robotic Joint Control  
- **Learning Objectives**:  
  1. Describe the principles of torque and angular acceleration in robotic joints. (Understand)  
  2. Calculate torque required for a joint given moment of inertia and angular acceleration. (Apply)  
  3. Analyze the effect of friction and damping on joint performance. (Analyze)  
  4. Design a simple control strategy for a single robotic joint. (Create)  
- **Cognitive Level**: Mix of Understand, Apply, Analyze, Create
