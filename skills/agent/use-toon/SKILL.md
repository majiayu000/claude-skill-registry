---
name: use-toon
description: Use TOON (Token-Oriented Object Notation) with schema.org vocabulary for prompting and instructing subagents and builtin agents. Use when delegating tasks to agents, structuring agent prompts, or specifying expected response formats. DO NOT use for external API calls or when JSON parsing is required.
---

<objective>
TOON with schema.org vocabulary provides a standard format for prompting and instructing agents. Use it to structure task delegation, specify expected outputs, and ensure consistent responses from subagents and builtin agents.

Key benefits:
- **Clear task structure**: schema.org Action types define what the agent should do
- **Expected output format**: Specify result type so agents return consistent data
- **Token efficiency**: 30-60% fewer tokens than JSON = more context for agent reasoning
- **Semantic interoperability**: Standard vocabulary eliminates ambiguity
</objective>

<quick_start>
<syntax>
**Object**: `key: value`

**Nested**: Indentation (2 spaces)

**Simple array**: `items[3]: a,b,c`

**Tabular array** (uniform objects):

```toon
users[2,]{id,name}:
  1,Alice
  2,Bob
```

</syntax>

<when_to_use>
| Use TOON | Use JSON |
|----------|----------|
| Agent task prompts | External API calls |
| Subagent instructions | Parsing with JSON.parse() |
| Expected response format | Human debugging |
| Agent-to-agent data | Deeply nested structures |
</when_to_use>
</quick_start>

<agent_prompting>
<task_delegation>
Structure agent tasks as schema.org Actions:

```toon
@type: SearchAction
@id: task-001
description: Find all error handling patterns in the codebase

object:
  @type: SoftwareSourceCode
  codeRepository: ./src

expectedResult:
  @type: ItemList
  description: Files with error handling patterns
```

The agent knows:
- **What to do**: SearchAction = find/search
- **What to search**: object defines the target
- **What to return**: expectedResult specifies format
</task_delegation>

<instruction_format>
When instructing agents, include:

```
[Task description in natural language]

Input:
[TOON block with @type, @id, and structured data]

Return your result in TOON format using:
- @type: [expected type, e.g., ItemList, Report, SearchAction]
- @id: [task-id]-result
- Use tabular notation for lists
```
</instruction_format>

<common_task_types>
| Task | schema.org Type | Use |
|------|-----------------|-----|
| Find/search | `SearchAction` | Code search, file discovery |
| Create/generate | `CreateAction` | Generate code, create files |
| Modify/update | `UpdateAction` | Edit files, refactor code |
| Validate/review | `AssessAction` | Code review, validation |
| Delete/remove | `DeleteAction` | Remove files, clean up |
| Analyze | `AnalyzeAction` | Code analysis, metrics |
</common_task_types>
</agent_prompting>

<core_syntax>
<scalars>

```toon
name: Alice
age: 30
active: true
score: null
```

Types auto-detected: strings, numbers, booleans, null.
</scalars>

<nesting>
```toon
user:
  name: Alice
  address:
    city: Boston
    zip: 02101
```
Use 2-space indentation for nesting.
</nesting>

<simple_arrays>

```toon
tags[3]: red,green,blue
ids[4]: 1,2,3,4
```

Format: `key[count]: item1,item2,...`
</simple_arrays>

<tabular_arrays>
For arrays of uniform objects (most efficient):

```toon
users[3,]{id,name,role}:
  1,Alice,admin
  2,Bob,user
  3,Carol,user
```

Format: `key[rowCount,]{col1,col2,...}:`

Each row provides values in column order, comma-separated.
</tabular_arrays>

</core_syntax>

<schema_vocabulary>
Use schema.org types and properties as shared vocabulary between agents.

<required_metadata>
Every TOON object MUST include:
- `@type`: schema.org type (e.g., `Person`, `SearchAction`, `ItemList`)
- `@id`: Unique identifier for the object

```toon
@type: Person
@id: user-123
name: Alice
email: alice@example.com
```
</required_metadata>

<common_types>
| Type | Use Case | Key Properties |
|------|----------|----------------|
| `Action` | Task execution | agent, object, result, actionStatus |
| `SearchAction` | Search/find operations | query, result |
| `CreateAction` | Creation operations | result, targetCollection |
| `UpdateAction` | Modifications | targetCollection, result |
| `AssessAction` | Validation/review | result, actionStatus |
| `ItemList` | Collections | itemListElement, numberOfItems |
| `Thing` | Generic entity | name, description, identifier |
| `CreativeWork` | Documents/code | author, dateCreated, text |
| `SoftwareSourceCode` | Code snippets | programmingLanguage, codeRepository |
</common_types>

<action_status>
For Action types, use `actionStatus` property:

| Status | Meaning |
|--------|---------|
| `PotentialActionStatus` | Not yet started |
| `ActiveActionStatus` | In progress |
| `CompletedActionStatus` | Successfully finished |
| `FailedActionStatus` | Failed with error |

```toon
@type: SearchAction
@id: search-001
actionStatus: CompletedActionStatus
query: auth handlers
resultCount: 3
```
</action_status>

<nested_types>
Use `@type` for nested objects too:

```toon
@type: CreateAction
@id: create-file-001
actionStatus: CompletedActionStatus

result:
  @type: SoftwareSourceCode
  name: auth.ts
  programmingLanguage: TypeScript

agent:
  @type: SoftwareApplication
  name: CodeAgent
```
</nested_types>

<property_conventions>
Prefer schema.org property names:

| Instead of | Use | schema.org property |
|------------|-----|---------------------|
| `file` | `name` | Thing.name |
| `path` | `url` | Thing.url |
| `content` | `text` | CreativeWork.text |
| `created` | `dateCreated` | CreativeWork.dateCreated |
| `author` | `author` | CreativeWork.author |
| `count` | `numberOfItems` | ItemList.numberOfItems |
| `items` | `itemListElement` | ItemList.itemListElement |
| `error` | `error` | Action.error |
</property_conventions>
</schema_vocabulary>

<prompting_patterns>
<structured_input>
When asking an agent to process structured data, use schema.org types:

```
Process this item list:

@type: ItemList
@id: pending-review
numberOfItems: 3

itemListElement[3,]{@type,identifier,name,status}:
  Product,A1,Widget,pending
  Product,A2,Gadget,shipped
  Product,A3,Gizmo,pending

Return pending items as an ItemList in TOON format.
```
</structured_input>

<requesting_toon_output>
Include format instruction with schema.org guidance:

```
Return your answer in TOON format:
- Use appropriate schema.org @type (Action, ItemList, etc.)
- Include @id for the result object
- Use schema.org property names (name, description, result)
- Use tabular notation for uniform lists
- Wrap in ```toon code block
```
</requesting_toon_output>

<agent_task_pattern>
For agent task delegation, structure as Action:

```toon
@type: SearchAction
@id: task-001
description: Find all authentication handlers

object:
  @type: SoftwareSourceCode
  codeRepository: ./src

expectedResult:
  @type: ItemList
  description: Files with auth handlers
```
</agent_task_pattern>

<agent_response_pattern>
Agents return completed Actions:

```toon
@type: SearchAction
@id: task-001
actionStatus: CompletedActionStatus

result:
  @type: ItemList
  @id: task-001-result
  numberOfItems: 3

  itemListElement[3,]{@type,name,url,description}:
    SoftwareSourceCode,handleLogin,src/auth.ts:42,Login handler
    SoftwareSourceCode,handleLogout,src/auth.ts:78,Logout handler
    SoftwareSourceCode,authGuard,src/middleware.ts:15,Auth middleware
```
</agent_response_pattern>

<extraction_pattern>
Parse TOON from LLM response:

```python
def extract_toon(response: str) -> str:
    if "```toon" in response:
        return response.split("```toon")[1].split("```")[0].strip()
    elif "```" in response:
        return response.split("```")[1].split("```")[0].strip()
    return response.strip()
```
</extraction_pattern>
</prompting_patterns>

<api_reference>
Using the toon-format Python library (`pip install toon-format`):

```python
from toon_format import encode, decode, estimate_savings

# Python dict to TOON
toon_str = encode(data, options={})

# TOON to Python dict
data = decode(toon_str, options={})

# Check efficiency
stats = estimate_savings(data)
# Returns: {"json_tokens": N, "toon_tokens": M, "savings_percent": X}
```

<options>
| Option | Default | Use |
|--------|---------|-----|
| delimiter | "," | Row separator: ",", "\t", "|" |
| lengthMarker | "" | Prefix for lengths: "", "#" |
| strict | False | Validation strictness |
</options>
</api_reference>

<quoting_rules>
Quote strings when they would be ambiguous:

| Value    | Requires Quotes | Reason                      |
|----------|-----------------|-----------------------------|
| `""`     | Yes             | Empty string                |
| `"true"` | Yes             | Boolean keyword as string   |
| `"123"`  | Yes             | Numeric string (not number) |
| `"a,b"`  | Yes             | Contains delimiter          |

Unquoted values are parsed as their natural type.
</quoting_rules>

<success_criteria>
TOON with schema.org is correctly applied when:

- Every object has `@type` (schema.org type) and `@id`
- Property names follow schema.org conventions
- Actions use appropriate `actionStatus` values
- Tabular notation used for uniform `itemListElement` arrays
- Code blocks tagged with `toon` language
- Data round-trips correctly: `decode(encode(data)) == data`
</success_criteria>

<examples>
<example name="search_action">
```toon
@type: SearchAction
@id: search-auth-001
actionStatus: CompletedActionStatus
query: authentication handlers

result:
  @type: ItemList
  @id: search-auth-001-result
  numberOfItems: 3

  itemListElement[3,]{@type,name,url,description}:
    SoftwareSourceCode,handleLogin,src/auth.ts:42,Login handler
    SoftwareSourceCode,handleLogout,src/auth.ts:78,Logout handler
    SoftwareSourceCode,authGuard,src/middleware.ts:15,Auth middleware
```
</example>

<example name="create_action">
```toon
@type: CreateAction
@id: create-component-001
actionStatus: CompletedActionStatus
description: Create React component

result:
  @type: SoftwareSourceCode
  @id: button-component
  name: Button.tsx
  url: src/components/Button.tsx
  programmingLanguage: TypeScript
  dateCreated: 2025-01-15
```
</example>

<example name="assess_action">
```toon
@type: AssessAction
@id: validate-005
actionStatus: CompletedActionStatus
description: Validate outcome specification

result:
  @type: Report
  @id: validate-005-report
  name: Validation Report
  reportStatus: NeedsAttention

  itemListElement[2,]{@type,name,description}:
    Warning,missing-desc,Description field is empty
    Info,add-examples,Consider adding examples
```
</example>

<example name="item_list">
```toon
@type: ItemList
@id: pending-tasks
description: Tasks awaiting review
numberOfItems: 3

itemListElement[3,]{@type,identifier,name,status}:
  Action,task-001,Implement auth,PotentialActionStatus
  Action,task-002,Add tests,ActiveActionStatus
  Action,task-003,Update docs,PotentialActionStatus
```
</example>
</examples>
