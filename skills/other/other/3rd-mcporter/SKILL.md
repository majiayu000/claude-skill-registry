---
name: mcporter
description: Use when you need to access MCP servers without installing them directly in Claude Code. MCPorter provides CLI access to any MCP server via npx, enabling tool discovery, direct calls, and ad-hoc connections. Use for accessing external MCP capabilities like browser automation, API integrations, or any MCP-based tooling.
---

<mcporter_skill>
  <overview>
    MCPorter is a CLI and runtime for Model Context Protocol (MCP) servers. It enables access to any MCP server without direct installation, auto-discovers configured servers, and provides ergonomic tool calling from the command line.
  </overview>

  <when_to_use>
    <scenario>Accessing MCP tools without installing them directly in Claude Code</scenario>
    <scenario>Discovering what MCP servers are available on the user's machine</scenario>
    <scenario>Calling MCP tools via CLI for automation or testing</scenario>
    <scenario>Connecting to ad-hoc MCP endpoints without configuration</scenario>
    <scenario>Inspecting available tools and their schemas from any MCP server</scenario>
  </when_to_use>

  <installation>
    <note>No installation required - use via npx</note>
    <alternative>npm install -g mcporter</alternative>
    <alternative>brew install steipete/tap/mcporter</alternative>
  </installation>

  <core_commands>
    <command name="List all discovered MCP servers">
      npx mcporter list
    </command>

    <command name="List tools from a specific server">
      npx mcporter list server_name
    </command>

    <command name="List tools with full JSON schema">
      npx mcporter list server_name --schema
    </command>

    <command name="Call a tool (colon syntax)">
      npx mcporter call server_name.tool_name arg1:value1 arg2:value2
    </command>

    <command name="Call a tool (function syntax)">
      npx mcporter call 'server_name.tool_name(arg1: "value1", arg2: "value2")'
    </command>

    <command name="Ad-hoc connection to HTTP MCP server">
      npx mcporter list --http-url https://mcp-server-url --name custom_name
    </command>

    <command name="Ad-hoc connection to stdio MCP server">
      npx mcporter call --stdio "npx -y some-mcp-server@latest" server.tool_name
    </command>
  </core_commands>

  <ad_hoc_mcp_access>
    <description>Access any MCP server without configuration using stdio or http flags</description>

    <pattern name="Run MCP server via npx and call tool">
      npx mcporter call --stdio "npx -y mcp-server-name@latest" server.tool_name arg:value
    </pattern>

    <pattern name="Discover tools from npx MCP server">
      npx mcporter list --stdio "npx -y mcp-server-name@latest" --name my_server
    </pattern>

    <pattern name="Connect to remote HTTP MCP endpoint">
      npx mcporter call --http-url https://mcp.example.com/mcp server.tool_name
    </pattern>
  </ad_hoc_mcp_access>

  <daemon_management>
    <description>For stateful servers that need persistent connections (like Chrome DevTools)</description>
    <command name="Check daemon status">npx mcporter daemon status</command>
    <command name="Start daemon">npx mcporter daemon start</command>
    <command name="Stop daemon">npx mcporter daemon stop</command>
  </daemon_management>

  <code_generation>
    <command name="Generate standalone CLI from MCP server">
      npx mcporter generate-cli "npx -y some-mcp-server@latest"
    </command>

    <command name="Generate TypeScript types">
      npx mcporter emit-ts server_name --out types/server.d.ts
    </command>

    <command name="Generate TypeScript client wrapper">
      npx mcporter emit-ts server_name --mode client --out clients/server.ts
    </command>
  </code_generation>

  <output_handling>
    <description>Results wrap in CallResult with helper methods</description>
    <method name=".text()">Plain text output</method>
    <method name=".markdown()">Markdown formatted output</method>
    <method name=".json()">Parsed JSON output</method>
    <method name=".content()">Raw content array</method>

    <flags>
      <flag name="--json">Output as JSON</flag>
      <flag name="--output json">Alternative JSON output flag</flag>
    </flags>
  </output_handling>

  <common_mcp_servers>
    <server name="chrome-devtools">
      <access>npx mcporter call --stdio "npx -y chrome-devtools-mcp@latest" chrome-devtools.tool_name</access>
      <use_case>Browser automation, screenshots, DOM inspection, console access</use_case>
    </server>

    <server name="firecrawl">
      <use_case>Web crawling and scraping</use_case>
    </server>

    <server name="linear">
      <use_case>Linear issue tracking integration</use_case>
    </server>
  </common_mcp_servers>

  <troubleshooting>
    <issue name="Tool name typos">
      MCPorter provides "Did you mean...?" suggestions for typos
    </issue>

    <issue name="Timeout errors">
      <solution>Set MCPORTER_CALL_TIMEOUT environment variable</solution>
      <solution>Use --timeout flag</solution>
    </issue>

    <issue name="Debug logging">
      npx mcporter --log-level debug call server.tool
    </issue>
  </troubleshooting>

  <workflow>
    <step number="1">Discover available servers: npx mcporter list</step>
    <step number="2">Inspect server tools: npx mcporter list server_name</step>
    <step number="3">View tool schema if needed: npx mcporter list server_name --schema</step>
    <step number="4">Call the tool: npx mcporter call server_name.tool_name args</step>
  </workflow>
</mcporter_skill>
