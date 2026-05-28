---
name: ericsson-ran-features-expert
description: Expert knowledge base for Ericsson LTE/NR radio access network features, parameters, counters, and engineering guidelines. Contains 377 features with 6164 parameters, 4257 counters, and activation codes.
license: MIT
metadata:
  features: 377
  parameters: 6164
  counters: 4257
  created: 2025-10-19
---

# Ericsson RAN Features Expert

## Overview
This skill provides comprehensive access to Ericsson LTE/NR radio features, including:
- 377 feature descriptions with technical details
- 6164 parameters with types and descriptions
- 4257 performance counters and KPI explanations
- Feature dependencies and relationships
- Engineering guidelines and best practices
- CXC feature codes for activation/deactivation

## When to Use This Skill

Use this skill when you need to:
- Understand Ericsson radio feature capabilities
- Configure feature parameters
- Activate or deactivate features
- Troubleshoot feature-related issues
- Plan feature deployments
- Understand feature interactions

## Capabilities

### Feature Information
- Get complete feature description: "Tell me about FAJ 121 3094"
- List features by category: "Show all MIMO features"
- Find features by parameter: "Which features use MimoSleepFunction?"
- Find feature by CXC code: "What is CXC4011808?"

### Technical Details
- Parameter lookup: "What does MimoSleepFunction.mimoSleepMode do?"
- Counter explanations: "Explain pmMimoSleepTime counter"
- Feature impact: "What is the network impact of MIMO Sleep Mode?"

### Activation and Configuration
- Get activation commands: "How do I activate CXC4011808?"
- Get deactivation commands: "How to deactivate MIMO Sleep Mode?"
- Prerequisites checking: "What do I need before activating this feature?"

### Engineering Support
- Configuration guidelines: "How should I configure MIMO Sleep Mode?"
- Best practices: "What are recommended settings for energy saving?"
- Troubleshooting: "Why is my feature not working?"

## Quick Reference

### Common Feature Categories
- **Carrier Aggregation**: 25 features
- **Dual Connectivity**: 3 features
- **Energy Efficiency**: 2 features
- **MIMO Features**: 6 features
- **Mobility**: 27 features
- **Other**: 314 features

### Access Patterns
- FAJ ID format: FAJ XXX XXXX (e.g., FAJ 121 3094)
- CXC Code format: CXC followed by numbers (e.g., CXC4011808)
- Parameter format: MOClass.parameterName
- Counter format: pmCounterName

## Reference Files
- `references/features/` - Complete feature documentation
- `references/parameters/` - Parameter master index
- `references/counters/` - Performance counter reference
- `references/cxc_codes/` - Activation code index
- `references/guidelines/` - Engineering guidelines

## Usage Examples

### Example 1: Feature Lookup
**User**: "Tell me about MIMO Sleep Mode feature"
**Response**: Provides complete feature details including FAJ ID, CXC code, parameters, activation steps, and engineering guidelines.

### Example 2: Activation Help
**User**: "How to activate CXC4011808?"
**Response**: Provides exact activation command, prerequisites, and any related features.

### Example 3: Configuration
**User**: "What are the recommended settings for MIMO Sleep Mode?"
**Response**: Provides configuration guidelines and best practices from engineering documentation.

## Notes
- This skill contains documentation for Ericsson Radio System features
- Always check prerequisites before activating features
- Verify compatibility with your specific node type and software version
- Consult engineering guidelines for optimal configuration

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Features: {self.summary['total_features']}
