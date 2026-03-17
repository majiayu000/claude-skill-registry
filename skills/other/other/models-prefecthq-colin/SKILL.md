---
colin:
  output:
    publish: false
  depends_on:
    - _tool-generator.md
    - _script-generator.md
---
{% set server = colin.mcp.source.server_info() %}
{% set server_name = vars.mcp_provider_name | default(server.name) %}
{% set skill_name = server_name | lower | replace(" ", "-") %}
{% file skill_name ~ "/SKILL.md" publish=true %}
---
name: {{ skill_name }}
description: {% llm model="anthropic:claude-haiku-4-5" id="skill-description" %}Write a 1-sentence description of this MCP server's capabilities for use as a skill description. Be concise.

Server name: {{ server.name }}
Server description: {{ server.instructions or "No description provided" }}
{%- endllm %}
{% if vars.generate_scripts | default(true) %}
allowed-tools: Read, Bash(python:*)
{%- endif %}
---

# {{ server.name or "MCP Server" }}

{{ server.instructions }}

{% if vars.generate_scripts | default(true) %}
## Running Tools

This skill includes Python scripts in `scripts/` that call MCP tools directly.

To use these scripts, install: `pip install fastmcp`

{% endif %}
{% set tools = colin.mcp.source.list_tools() %}
## Tools

This server provides {{ tools | length }} tool(s):

{% for tool in tools %}
{% set tool_doc = ref(skill_name ~ "/" ~ tool.name ~ ".md") %}
- [{{ tool.name }}]({{ tool.name }}.md){% if tool_doc and tool_doc.sections.summary %} - {{ tool_doc.sections.summary }}{% endif %}
{% endfor %}
{% endfile %}
