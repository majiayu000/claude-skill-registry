---
name: '317'
description: This packet sends a specific skill.
---

# Send Skill
This packet sends a specific skill.

## Packet Details
| Key | Value |
|--|--|
| Name | Send Skill |
| Description | Sends a specific skill |
| Opcode | 154 |
| Type | Fixed |
| Length | N/A |
| Revision | 317 |

## Packet Structure
| Data Type | Description |
|--|--|
| [Byte](/Data-Types.html#common-data-types) | The skill you want to send. |
| [Int](/Data-Types.html#common-data-types) | The experience of that skill. |
| [Byte](/Data-Types.html#common-data-types) | The level of that skill. |
