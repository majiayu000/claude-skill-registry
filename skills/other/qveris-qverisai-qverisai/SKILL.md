---
name: QVeris
description: Find third-party APIs and connect to them in code to assist users in various fields such as finance, economics, healthcare, sports, scientific research, and more
---

Whenever an external functionality is needed, do the following steps:

1. **FIND A QVERISAI's TOOL**: You can use the qveris MCP server to find API tools to assist users. Firstly, consider which tools may be useful for completing user tasks. Then, use the search_tools tool and enter a query that describes the tool's functionality, rather than the parameters you will pass to the tool later. Limit the number of results to 10 if no special requirements. Next, you should use the Execute_tool to try out a suitable search tool and pass parameters to the search tool through params_to_tool. You can refer to the examples provided by each tool (if any). You can call multiple searches in a single response. The previous steps of interaction between search_tool and executioner_tool can help you find available tools.
2. **CALL QVERISAI's TOOL**: Once you find a suitable tool, you can use the qveris execute rest API described below to write code that calls the tool to meet user needs. Notice that you should not use the tool call's result from first step, you will generate real product code for user, and use the api key in the mcp server's config in the code. The generated code no longer requires a search interface call, and you can directly use the tool of MCP's choice. You can set request's timeout to 5 seconds, and you should handle the error returns of the REST API correctly.

# QVeris API Documentation

## Authentication

All API requests require authentication via Bearer token in the
`Authorization` header.

``` http
Authorization: Bearer YOUR_API_KEY
```

## Base URL

``` text
https://qveris.ai/api/v1
```

## API Endpoints

### 1. Execute Tool

Execute a tool with specified parameters.

#### Endpoint

``` http
POST /tools/execute?tool_id={tool_id}
```

#### Example Request Body

``` json
{
  "search_id": "string",
  "session_id": "string",
  "parameters": {
    "city": "London",
    "units": "metric"
  },
  "max_response_size": 20480
}
```

#### Example Response (200 OK)

``` json
{
  "execution_id": "string",
  "result": {
    "data": {
      "temperature": 15.5,
      "humidity": 72
    }
  },
  "success": true,
  "error_message": null,
  "elapsed_time_ms": 847
}
```

