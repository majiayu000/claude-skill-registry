---
name: contact-center
description: --8<-- "includes/ccai-api-back-link.md"
---

--8<-- "includes/ccai-api-back-link.md"

# Update a Particular Skill

To update the particular skill with the given `streamId`, `skillGroupId`, and `skillId`.

| **Method**     | PUT                                                                                        |
|------------|-------------------------------------------------------------------------------------------|
| **Endpoint**   | `https://{{host}}/agentassist/api/v1/public/{{botId}}/skill-groups/{{skillGroupId}}/skills/{skillId}` |
| **Content Type** | `application/json`                                                                         |
| Authorization | `auth: {{JWT}}` <br>See [How to generate the JWT Token](../automation/api-introduction.md#generating-the-jwt-token) |
| **API Scope**  | SmartAssist Analytics                                                                      |

## Path Parameters

| **PARAMETER** | **DESCRIPTION**                                                         | **TYPE**          |
|-----------|---------------------------------------------------------------------|---------------|
| host      | Environment URL, for example, `https://platform.kore.ai`          | string, required |
| streamId     | botId or streamId. You can get it from the App Settings page. | string, required |
| skillId   | ID of the Skill.                                                   | string, required |

## Sample Request

```
curl --location --request PUT \
     'https://{{host}}/agentassist/api/v1/public/{{streamId}}/skill-groups/{{skillGroupId}}/skills/{skillId}' \
     --header 'auth: {jwt-code}' \
      --header 'Content-Type: application/json' \
      --data-raw '{
    "name": "Account Management",
    "description": "Manage Account and its Settings",
    "agents": [
        {
            "userId": "u-122x",
            "proficiencyLevel": "high",
            "firstName": "test",
            "lastName": "test",
            "email": "username@domain.com"
        }
    ],
}'
```

## Body Parameters

| **PARAMETER**       | **DESCRIPTION**                                                                                   | **TYPE**            |
|-----------------|-----------------------------------------------------------------------------------------------|-----------------|
| name            | Name of the skill.                                                                            | String, Required |
| description     | Brief description of the skill up to 200 characters.                                          | string, optional |
| skillGroupId    | Id of the skill Group, which you can find with [GET /skill-groups](../contact-center/get-a-skill-group.md). Example: sg-4372 | string, required |
| agents          | An array of Objects with the following details.                                               | string, optional |
| userId          | This is the user Id that you can find with [GET /agents](../contact-center/list-all-agents.md).     | string, optional |
| proficiencyLevel| The Proficiency level can be: expert, novice, average, good. For example, ‘expert’               | string, optional |

## Sample Response

```
 {
    "id": "sk-87679",
    "name": "Account Management",
    "description": "Manage Account and its Settings",
    "agents": 15,
    "skillGroupId": "sg-4372"
   }
```