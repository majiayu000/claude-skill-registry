---
name: sonarqube-check
description: This skill should be used when checking why the last pull request failed SonarQube/SonarCloud quality gates. It uses the SonarQube MCP server to retrieve failure details and report the reasons.
allowed-tools: ["mcp__sonarqube__*"]
---

# SonarQube Check

Use the SonarQube MCP server to get the reason the last PR failed checks.

Retrieve the quality gate status and report all failures with their details.
