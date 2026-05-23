---
name: n8n-skills
description: "n8n workflow automation knowledge base. Provides n8n node information, node functionality details, workflow patterns, and configuration examples. Covers triggers, data transformation, data input/output, AI integration, covering 10 nodes. Keywords: n8n, workflow, automation, node, trigger, webhook, http request, database, ai agent."
license: MIT
metadata:
  author: Frank Chen
  version: "2.2.0"
---

# n8n Workflow Automation Skill Pack

## Overview

This skill helps with:
- Understanding n8n node functionality and usage
- Finding nodes suitable for specific tasks
- Learning common workflow patterns
- Getting node configuration examples
- Solving workflow design problems

This skill includes:
- Detailed information on the 10 most commonly used built-in n8n nodes
- 30+ popular community packages for extended functionality
- Node configuration examples and best practices
- Common workflow patterns
- Node categorization and indexing for both built-in and community nodes

## Table of Contents

- [Overview](#overview)
- [Common Workflow Patterns](#common-workflow-patterns)
- [How to Find Nodes](resources/guides/how-to-find-nodes.md)
- [Usage Guide](resources/guides/usage-guide.md)
- [License and Attribution](#license-and-attribution)

# Common Workflow Patterns

Here are some common workflow patterns you can use as a starting point:

## 1. HTTP Data Fetching

Fetch data from APIs and process it

Nodes used:
- HTTP Request
- Set
- IF

Example: Use HTTP Request node to fetch data from external APIs, Set node to transform formats, and IF node for conditional logic

## 2. Email Automation

Monitor emails and auto-respond or forward

Nodes used:
- Email Trigger (IMAP)
- Gmail
- IF

Example: Use Email Trigger to monitor inbox, IF node to filter specific conditions, and Gmail node to auto-reply or forward

## 3. Database Synchronization

Sync data between different systems

Nodes used:
- Schedule Trigger
- HTTP Request
- Postgres
- MySQL

Example: Scheduled trigger to read data from one database, transform it, and write to another database

## 4. Webhook Processing

Receive external webhooks and trigger actions

Nodes used:
- Webhook
- Set
- HTTP Request
- Slack

Example: Receive webhook events, process data, and send notifications to Slack or other systems

## 5. AI Assistant Integration

Use AI models to process and generate content

Nodes used:
- AI Agent
- OpenAI
- Vector Store
- Embeddings OpenAI

Example: Build AI assistants to handle user queries, integrate vector databases for semantic search

## 6. File Processing

Automatically process and transform files

Nodes used:
- Google Drive Trigger
- Extract from File
- Move Binary Data
- Dropbox

Example: Monitor Google Drive for new files, extract and process content, then upload to Dropbox

## Complete Template Library

We have collected 20 popular workflow templates from n8n.io, categorized by use case:

- [AI & Chatbots](resources/templates/ai-chatbots/README.md) - AI Agents, RAG systems, intelligent conversations
- [Social Media & Video](resources/templates/social-media/README.md) - TikTok, Instagram, YouTube automation
- [Data Processing & Analysis](resources/templates/data-processing/README.md) - Google Sheets, database integration
- [Communication & Collaboration](resources/templates/communication/README.md) - Email, WhatsApp, Telegram automation

See the [complete template index](resources/templates/README.md) for all available templates.


---

# License and Attribution

## This Skill Pack License

This skill pack project is licensed under the MIT License.
See: https://github.com/haunchen/n8n-skills/blob/main/LICENSE

## Important Notice

This is an unofficial educational project and is not affiliated with n8n GmbH.

This skill content is generated based on the following resources:
- n8n node type definitions (Sustainable Use License)
- n8n official documentation (MIT License)
- n8n-mcp project architecture (MIT License)

For detailed attribution information, please refer to the ATTRIBUTIONS.md file in the project.

## About n8n

n8n is an open-source workflow automation platform developed and maintained by n8n GmbH.

- Official website: https://n8n.io
- Documentation: https://docs.n8n.io
- Source code: https://github.com/n8n-io/n8n
- License: Sustainable Use License

When using n8n software, you must comply with n8n's license terms. See: https://github.com/n8n-io/n8n/blob/master/LICENSE.md