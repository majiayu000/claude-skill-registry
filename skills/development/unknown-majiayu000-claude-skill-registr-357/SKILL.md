---
name: agent-repair
description: "A two-phase repair skill that analyzes errors and suggests fixes before executing repairs. Phase one: user describes error, agent analyzes and proposes solution. Phase two: upon approval, executes the repair action."
---

# Agent Network Repair

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

# Agent Network Repair Skill

## Overview
This skill provides a two-phase approach to diagnosing and repairing system errors, service failures, and configuration issues.

## Workflow

### Phase 1: Analysis and Discussion
When the user reports an error or issue:

1. **Gather Information**
   - Ask the user to describe the error, symptoms, and context
   - Collect error messages, stack traces, or failure logs
   - Identify which service, API, or component is affected

2. **Diagnose the Problem**
   - Analyze the error type (authentication, configuration, network, service availability, etc.)
   - Check relevant logs or status if accessible
   - Identify potential root causes
   - Consider multiple possible solutions

3. **Present Initial Analysis**
   - Clearly explain what the problem appears to be
   - List the likely root cause
   - Propose one or more repair actions
   - Explain potential risks or side effects
   - Invite questions or discussion

4. **Iterative Discussion Loop**
   - User can ask follow-up questions about the analysis
   - User can request alternative solutions or approaches
   - User can ask for more details about specific aspects
   - User can request additional investigation or checks
   - Agent refines analysis based on feedback
   - Continue this back-and-forth until user is satisfied
   - Only proceed to Phase 2 when user explicitly approves a specific action

**Discussion continues until user says**: "proceed", "do it", "approved", "go ahead", or similar confirmation

### Phase 2: Repair (Only After Explicit Approval)
Once the user approves the proposed solution:

1. **Execute Repair Actions**
   - Implement the approved fix (e.g., update configuration, restart service, fix credentials)
   - Use appropriate tools (file edits, bash commands, API calls)
   - Log all actions taken

2. **Verify the Fix**
   - Test that the issue is resolved
   - Confirm the service or component is working
   - Report results back to the user

3. **Document**
   - Summarize what was done
   - Note any follow-up actions needed

## Common Repair Scenarios

- **API Authentication Errors**: Check and update API keys or credentials
- **Service Connectivity Issues**: Verify endpoints, network access, service status
- **Configuration Problems**: Review and correct config files or environment variables
- **Permission Errors**: Adjust file permissions or access controls
- **Dependency Issues**: Install or update required packages or libraries

## Safety Guidelines

- NEVER proceed with repairs without explicit user approval
- Always explain what will be changed before making changes
- Prefer non-destructive solutions when possible
- Back up or note current state before making changes
- If uncertain, ask for clarification rather than guessing

## Example Usage

**User**: "The image generation service is failing with a NoneType error"

**Agent Phase 1 Response**: 
"I've analyzed the error. The issue appears to be that the image generation API is not properly configured or the API key is missing. The error 'NoneType object is not subscriptable' suggests the service is returning None instead of expected data. 

Proposed solution: Check the environment variables or configuration file for the image generation API key and endpoint. We may need to add or update the API credentials.

Shall I proceed with checking the configuration files?"

**User**: "Yes, proceed"

**Agent Phase 2**: Executes the approved repair actions and reports results.


## Resources

This skill includes example resource directories:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly.

### references/
Documentation and reference material to be loaded into context as needed.

### assets/
Files used within the output Claude produces (templates, images, fonts, etc.).

**Any unneeded directories can be deleted.**


## Extended Example with Discussion Loop

**User**: "The image generation service is failing with a NoneType error"

**Agent Initial Analysis**:
"I've analyzed the error. The issue appears to be that the image generation API is not properly configured or the API key is missing. The error 'NoneType object is not subscriptable' suggests the service is returning None instead of expected data.

Proposed solutions:
1. Check environment variables for missing API credentials
2. Verify the image generation service configuration file
3. Test the API endpoint directly to confirm it's accessible

What would you like to know more about, or would you like me to proceed with one of these approaches?"

**User**: "What are the risks of option one?"

**Agent**: "Checking environment variables is read-only and has no risk. However, if we need to add or update credentials, we would be modifying the environment configuration. The main risk is if we set incorrect credentials, the service might be locked out temporarily. I can show you the current values first before making any changes."

**User**: "Can you check what's currently configured first?"

**Agent**: "Absolutely. I will examine the current configuration and show you what's set. This is just a read operation, no changes yet."

**User**: "Okay, proceed with that"

**Agent Phase 2**: Executes the approved investigation, reports findings, and awaits further instruction or approval for actual repairs.

