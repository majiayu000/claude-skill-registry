---
name: dart-run-tests
description: "To run Dart or Flutter tests with the agent-centric test runner, execute tests using this tool instead of shell `dart test` or `flutter test`."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"run_tests","arguments":{}}
```

## Tool Description
Run Dart or Flutter tests with an agent centric UX. ALWAYS use instead of `dart test` or `flutter test` shell commands.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "roots": {
      "type": "array",
      "title": "All projects roots to run this tool in.",
      "items": {
        "type": "object",
        "properties": {
          "root": {
            "type": "string",
            "title": "The file URI of the project root to run this tool in.",
            "description": "This must be equal to or a subdirectory of one of the roots allowed by the client. Must be a URI with a `file:` scheme (e.g. file:///absolute/path/to/root)."
          },
          "paths": {
            "type": "array",
            "title": "Paths to run this tool on. Must resolve to a path that is within the \"root\".",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "root"
        ]
      }
    },
    "testRunnerArgs": {
      "type": "object",
      "properties": {
        "help": {
          "type": "boolean",
          "description": "Show this usage information.\ndefaults to \"false\""
        },
        "version": {
          "type": "boolean",
          "description": "Show the package:test version.\ndefaults to \"false\""
        },
        "name": {
          "type": "array",
          "description": "A substring of the name of the test to run.\nRegular expression syntax is supported.\nIf passed multiple times, tests must match all substrings.\ndefaults to \"[]\"",
          "items": {
            "type": "string"
          }
        },
        "plain-name": {
          "type": "array",
          "description": "A plain-text substring of the name of the test to run.\nIf passed multiple times, tests must match all substrings.\ndefaults to \"[]\"",
          "items": {
            "type": "string"
          }
        },
        "tags": {
          "type": "array",
          "description": "Run only tests with all of the specified tags.\nSupports boolean selector syntax.\ndefaults to \"[]\"",
          "items": {
            "type": "string"
          }
        },
        "exclude-tags": {
          "type": "array",
          "description": "Don't run tests with any of the specified tags.\nSupports boolean selector syntax.\ndefaults to \"[]\"",
          "items": {
            "type": "string"
          }
        },
        "run-skipped": {
          "type": "boolean",
          "description": "Run skipped tests instead of skipping them.\ndefaults to \"false\""
        },
        "platform": {
          "type": "array",
          "description": "The platform(s) on which to run the tests.\n[vm (default), chrome, firefox, edge, node].\nEach platform supports the following compilers:\n[vm]: kernel (default), source, exe\n[chrome]: dart2js (default), dart2wasm\n[firefox]: dart2js (default), dart2wasm\n[edge]: dart2js (default)\n[node]: dart2js (default), dart2wasm\ndefaults to \"[]\"",
          "items": {
            "type": "string"
          }
        },
        "compiler": {
          "type": "array",
          "description": "The compiler(s) to use to run tests, supported compilers are [dart2js, dart2wasm, exe, kernel, source].\nEach platform has a default compiler but may support other compilers.\nYou can target a compiler to a specific platform using arguments of the following form [<platform-selector>:]<compiler>.\nIf a platform is specified but no given compiler is supported for that platform, then it will use its default compiler.\ndefaults to \"[]\"",
          "items": {
            "type": "string"
          }
        },
        "preset": {
          "type": "array",
          "description": "The configuration preset(s) to use.\ndefaults to \"[]\"",
          "items": {
            "type": "string"
          }
        },
        "concurrency": {
          "type": "string",
          "description": "The number of concurrent test suites run.\ndefaults to \"8\""
        },
        "total-shards": {
          "type": "string",
          "description": "The total number of invocations of the test runner being run."
        },
        "shard-index": {
          "type": "string",
          "description": "The index of this test runner invocation (of --total-shards)."
        },
        "timeout": {
          "type": "string",
          "description": "The default test timeout. For example: 15s, 2x, none\ndefaults to \"30s\""
        },
        "ignore-timeouts": {
          "type": "boolean",
          "description": "Ignore all timeouts (useful if debugging)\ndefaults to \"false\""
        },
        "pause-after-load": {
          "type": "boolean",
          "description": "Pause for debugging before any tests execute.\nImplies --concurrency=1, --debug, and --ignore-timeouts.\nCurrently only supported for browser tests.\ndefaults to \"false\""
        },
        "debug": {
          "type": "boolean",
          "description": "Run the VM and Chrome tests in debug mode.\ndefaults to \"false\""
        },
        "coverage": {
          "type": "string",
          "description": "Gather coverage and output it to the specified directory.\nImplies --debug."
        },
        "chain-stack-traces": {
          "type": "boolean",
          "description": "Use chained stack traces to provide greater exception details\nespecially for asynchronous code. It may be useful to disable\nto provide improved test performance but at the cost of\ndebuggability.\ndefaults to \"false\""
        },
        "no-retry": {
          "type": "boolean",
          "description": "Don't rerun tests that have retry set.\ndefaults to \"false\""
        },
        "test-randomize-ordering-seed": {
          "type": "string",
          "description": "Use the specified seed to randomize the execution order of test cases.\nMust be a 32bit unsigned integer or \"random\".\nIf \"random\", pick a random seed to use.\nIf not passed, do not randomize test case execution order."
        },
        "fail-fast": {
          "type": "boolean",
          "description": "Stop running tests after the first failure.\n\ndefaults to \"false\""
        },
        "reporter": {
          "type": "string",
          "description": "Set how to print test results.\ndefaults to \"compact\"\nallowed values: compact, expanded, failures-only, github, json, silent"
        },
        "file-reporter": {
          "type": "string",
          "description": "Enable an additional reporter writing test results to a file.\nShould be in the form <reporter>:<filepath>, Example: \"json:reports/tests.json\""
        },
        "verbose-trace": {
          "type": "boolean",
          "description": "Emit stack traces with core library frames.\ndefaults to \"false\""
        },
        "js-trace": {
          "type": "boolean",
          "description": "Emit raw JavaScript stack traces for browser tests.\ndefaults to \"false\""
        },
        "color": {
          "type": "boolean",
          "description": "Use terminal colors.\n(auto-detected by default)\ndefaults to \"false\""
        }
      },
      "required": []
    }
  }
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
