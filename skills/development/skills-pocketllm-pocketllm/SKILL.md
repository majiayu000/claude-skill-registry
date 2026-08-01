---
name: skills-pocketllm-pocketllm
description: Claude Docs home page![light logo!dark logo](https://docs.claude.com/)
---

# Create Skill - Claude Docs> Source: https://docs.claude.com/en/api/skills/create-skillAgent Skills are now available! [Learn more about extending Claude's capabilities with Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview).
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)
English
Search...
⌘K
  * [Console](https://console.anthropic.com/login)
  * [Support](https://support.claude.com/)
  * [Discord](https://www.anthropic.com/discord)
  * [Sign up](https://console.anthropic.com/login)
  * [Sign up](https://console.anthropic.com/login)


Search...
Navigation
Skill Management
Create Skill
[Home](https://docs.claude.com/en/home)[Developer Guide](https://docs.claude.com/en/docs/intro)[API Reference](https://docs.claude.com/en/api/overview)[Model Context Protocol (MCP)](https://docs.claude.com/en/docs/mcp)[Resources](https://docs.claude.com/en/resources/overview)[Release Notes](https://docs.claude.com/en/release-notes/overview)
##### Using the API
  * [Features overview](https://docs.claude.com/en/api/overview)
  * [Client SDKs](https://docs.claude.com/en/api/client-sdks)
  * [Beta headers](https://docs.claude.com/en/api/beta-headers)
  * [Errors](https://docs.claude.com/en/api/errors)


##### Messages
  * [POSTMessages](https://docs.claude.com/en/api/messages)
  * [POSTCount Message tokens](https://docs.claude.com/en/api/messages-count-tokens)


##### Models
  * [GETList Models](https://docs.claude.com/en/api/models-list)
  * [GETGet a Model](https://docs.claude.com/en/api/models)


##### Message Batches
  * [POSTCreate a Message Batch](https://docs.claude.com/en/api/creating-message-batches)
  * [GETRetrieve a Message Batch](https://docs.claude.com/en/api/retrieving-message-batches)
  * [GETRetrieve Message Batch Results](https://docs.claude.com/en/api/retrieving-message-batch-results)
  * [GETList Message Batches](https://docs.claude.com/en/api/listing-message-batches)
  * [POSTCancel a Message Batch](https://docs.claude.com/en/api/canceling-message-batches)
  * [DELDelete a Message Batch](https://docs.claude.com/en/api/deleting-message-batches)


##### Files
  * [POSTCreate a File](https://docs.claude.com/en/api/files-create)
  * [GETList Files](https://docs.claude.com/en/api/files-list)
  * [GETGet File Metadata](https://docs.claude.com/en/api/files-metadata)
  * [GETDownload a File](https://docs.claude.com/en/api/files-content)
  * [DELDelete a File](https://docs.claude.com/en/api/files-delete)


##### Skills
  * Skill Management
    * [POSTCreate Skill](https://docs.claude.com/en/api/skills/create-skill)
    * [GETList Skills](https://docs.claude.com/en/api/skills/list-skills)
    * [GETGet Skill](https://docs.claude.com/en/api/skills/get-skill)
    * [DELDelete Skill](https://docs.claude.com/en/api/skills/delete-skill)
  * Skill Versions


##### Admin API
  * Organization Info
  * Organization Member Management
  * Organization Invites
  * Workspace Management
  * Workspace Member Management
  * API Keys
  * Usage and Cost


##### Experimental APIs
  * Prompt tools


##### Text Completions (Legacy)
  * [Migrating from Text Completions](https://docs.claude.com/en/api/migrating-from-text-completions-to-messages)


##### Support & configuration
  * [Rate limits](https://docs.claude.com/en/api/rate-limits)
  * [Service tiers](https://docs.claude.com/en/api/service-tiers)
  * [Versions](https://docs.claude.com/en/api/versioning)
  * [IP addresses](https://docs.claude.com/en/api/ip-addresses)
  * [Supported regions](https://docs.claude.com/en/api/supported-regions)
  * [OpenAI SDK compatibility](https://docs.claude.com/en/api/openai-sdk)


cURL
cURL
Copy
```
curl -X POST "https://api.anthropic.com/v1/skills" \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "anthropic-beta: skills-2025-10-02" \
     -F "display_title=My Excel Skill" \
     -F "files[]=@excel-skill/SKILL.md;filename=excel-skill/SKILL.md" \
     -F "files[]=@excel-skill/process_excel.py;filename=excel-skill/process_excel.py"
```

200
4XX
Copy
```
{
  "created_at": "2024-10-30T23:58:27.427722Z",
  "display_title": "My Custom Skill",
  "id": "skill_01JAbcdefghijklmnopqrstuvw",
  "latest_version": "1759178010641129",
  "source": "custom",
  "type": "skill",
  "updated_at": "2024-10-30T23:58:27.427722Z"
}
```

Skill Management
# Create Skill
Copy page
Copy page
POST
/
v1
/
skills
cURL
cURL
Copy
```
curl -X POST "https://api.anthropic.com/v1/skills" \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "anthropic-beta: skills-2025-10-02" \
     -F "display_title=My Excel Skill" \
     -F "files[]=@excel-skill/SKILL.md;filename=excel-skill/SKILL.md" \
     -F "files[]=@excel-skill/process_excel.py;filename=excel-skill/process_excel.py"
```

200
4XX
Copy
```
{
  "created_at": "2024-10-30T23:58:27.427722Z",
  "display_title": "My Custom Skill",
  "id": "skill_01JAbcdefghijklmnopqrstuvw",
  "latest_version": "1759178010641129",
  "source": "custom",
  "type": "skill",
  "updated_at": "2024-10-30T23:58:27.427722Z"
}
```

#### Headers
[​](https://docs.claude.com/en/api/skills/create-skill#parameter-anthropic-beta)
anthropic-beta
string[]
Optional header to specify the beta version(s) you want to use.
To use multiple betas, use a comma separated list like `beta1,beta2` or specify the header multiple times for each beta.
[​](https://docs.claude.com/en/api/skills/create-skill#parameter-anthropic-version)
anthropic-version
string
required
The version of the Claude API you want to use.
Read more about versioning and our version history [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
[​](https://docs.claude.com/en/api/skills/create-skill#parameter-x-api-key)
x-api-key
string
required
Your unique API key for authentication.
This key is required in the header of all API requests, to authenticate your account and access Anthropic's services. Get your API key through the [Console](https://console.anthropic.com/settings/keys). Each key is scoped to a Workspace.
#### Body
multipart/form-data
[​](https://docs.claude.com/en/api/skills/create-skill#body-display-title)
display_title
string | null
Display title for the skill.
This is a human-readable label that is not included in the prompt sent to the model.
[​](https://docs.claude.com/en/api/skills/create-skill#body-files)
files
file[] | null
Files to upload for the skill.
All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.
#### Response
200
application/json
Successful Response
[​](https://docs.claude.com/en/api/skills/create-skill#response-created-at)
created_at
string
required
ISO 8601 timestamp of when the skill was created.
Examples:
`"2024-10-30T23:58:27.427722Z"`
[​](https://docs.claude.com/en/api/skills/create-skill#response-display-title)
display_title
string | null
required
Display title for the skill.
This is a human-readable label that is not included in the prompt sent to the model.
Examples:
`"My Custom Skill"`
[​](https://docs.claude.com/en/api/skills/create-skill#response-id)
id
string
required
Unique identifier for the skill.
The format and length of IDs may change over time.
Examples:
`"skill_01JAbcdefghijklmnopqrstuvw"`
[​](https://docs.claude.com/en/api/skills/create-skill#response-latest-version)
latest_version
string | null
required
The latest version identifier for the skill.
This represents the most recent version of the skill that has been created.
Examples:
`"1759178010641129"`
[​](https://docs.claude.com/en/api/skills/create-skill#response-source)
source
string
required
Source of the skill.
This may be one of the following values:
  * `"custom"`: the skill was created by a user
  * `"anthropic"`: the skill was created by Anthropic


Examples:
`"custom"`
[​](https://docs.claude.com/en/api/skills/create-skill#response-type)
type
string
default:skill
required
Object type.
For Skills, this is always `"skill"`.
[​](https://docs.claude.com/en/api/skills/create-skill#response-updated-at)
updated_at
string
required
ISO 8601 timestamp of when the skill was last updated.
Examples:
`"2024-10-30T23:58:27.427722Z"`
Was this page helpful?
YesNo
[Delete a File](https://docs.claude.com/en/api/files-delete)[List Skills](https://docs.claude.com/en/api/skills/list-skills)
Assistant
Responses are generated using AI and may contain mistakes.
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)
Company
[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)
Help and security
[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)
Learn
[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)
Terms and policies
[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)
