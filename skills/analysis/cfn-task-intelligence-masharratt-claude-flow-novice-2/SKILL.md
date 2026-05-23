---
name: cfn-task-intelligence
description: Classify tasks (type/domain), estimate complexity/iterations, recommend specialists from feedback themes
version: 1.0.0
tags: classification, complexity, specialists, cfn-loop
status: production
---

# What it does
Analyzes task descriptions → classifies type (software, content, research, design, infrastructure, data), detects domains (frontend, backend, security, devops, testing, database, docs), estimates complexity + iterations, recommends specialists from recurring feedback.

# When to use
1. New task → Determine CFN Loop config and agents
2. Estimate iterations → How many loops before gates pass
3. Recurring issues → After 3 security feedback, recommend security-specialist
4. Multi-agent coordination → Identify domains and dependencies

# When NOT to use
1. Task already classified → Proceed with execution
2. Simple type check → Use /write-plan instead
3. Agent failure debugging → Use /cfn-check-errors
4. Adjust teams mid-execution → Use /cfn-agent-lifecycle

# How to use
Classify: ./cfn-task-intelligence.sh --task-description "..." --mode classify
Complexity: --mode complexity (returns iterations 2-7, confidence 0.70-0.80)
Specialist: --mode specialist --current-loop3 "..." --feedback-themes "security,auth" --recurring-count 3
Full: --mode all

# Parameters
--task-description, --mode (classify/complexity/specialist/all), --current-loop3, --feedback-themes, --recurring-count

# Expected output
Classify: {task_type, domains[], complexity, keyword_counts}
Complexity: {complexity, estimated_iterations, confidence, factors, reasoning}
Specialist: {add_specialist, reasoning, new_loop3_agents[]}

# Real-world
"Microservice with K8s and streaming" → infrastructure, [backend,devops,database], high, 6 iterations → spawn DevOps + backend, enterprise mode