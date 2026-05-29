---
name: dart-pub-dev-search
description: "To search pub.dev for relevant Dart packages, query by keywords and return download counts, topics, license, and publisher."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"pub_dev_search","arguments":{}}
```

## Tool Description
Searches pub.dev for packages relevant to a given search query. The response will describe each result with its download count, package description, topics, license, and publisher.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "title": "Search query",
      "description": "The query to run against pub.dev package search.\n\nBesides freeform keyword search `pub.dev` supports the following search query\nexpressions:\n\n  - `\"exact phrase\"`: By default, when you perform a search, the results include\n    packages with similar phrases. When a phrase is inside quotes, you'll see\n    only those packages that contain exactly the specified phrase.\n\n  - `dependency:<package_name>`: Searches for packages that reference\n    `package_name` in their `pubspec.yaml`.\n\n  - `dependency*:<package_name>`: Searches for packages that depend on\n    `package_name` (as direct, dev, or transitive dependencies).\n\n  - `topic:<topic-name>`: Searches for packages that have specified the\n    `topic-name` [topic](/topics).\n\n  - `publisher:<publisher-name.com>`: Searches for packages published by `publisher-name.com`\n\n  - `sdk:<sdk>`: Searches for packages that support the given SDK. `sdk` can be either `flutter` or `dart`\n\n  - `runtime:<runtime>`: Searches for packages that support the given runtime. `runtime` can be one of `web`, `native-jit` and `native-aot`.\n\n  - `updated:<duration>`: Searches for packages updated in the given past days,\n    with the following recognized formats: `3d` (3 days), `2w` (two weeks), `6m` (6 months), `2y` 2 years.\n\n  - `has:executable`: Search for packages with Dart files in their `bin/` directory.\n\nTo search for alternatives do multiple searches. There is no \"or\" operator.\n  "
    }
  },
  "required": [
    "query"
  ]
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
