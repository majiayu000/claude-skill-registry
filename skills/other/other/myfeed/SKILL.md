---
name: my-life-feed
description: Manage MyFeed things and groups via the MyFeed REST API.
homepage: https://myfeed.life
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["jq"],"env":["Myfeed_API_KEY"]}}}
---

# My Life Feed Skill

Add things for friends and groups, list my groups

## Setup

1. Get your API key: ask the owner to get it from My Life Feed app
2. Set environment variables:   
   ```bash
   export Myfeed_API_KEY="your-api-key"
   ```

## Usage

All commands use curl to hit the My Life Feed REST API.

### Create thing and invite a friend

```bash
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": Thing starttime in epoch,
   "alarms":[
     {
        "type": "minutes / hours / days / weeks / months",
        "value": how many units
     }
    ],
   "invites": [
      {"phone_number":"Friend phone number"}
    ]
   
 }
}'
```

### List groups and receive group id
```bash
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" -d '
{
 "request":"get_groups",
 "params":{
   "starting_from": 1739383324000
   }
}'| jq '.groups[] | {group_id,url_group,is_admin}'
```

### Create thing and invite a group
```bash
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": Thing starttime in epoch in miliseconds,
   "alarms":[
     {
        "type": "minutes / hours / days / weeks / months",
        "value": how many units
     }
    ],
   "invites": [
      {"group_id":group_id }
    ]
   
 }
}'
```
## Notes

- Group Id can be found by listing the groups with a certain name
- The API key and token provide full access to your My Life Feed / MyFeed account - keep them secret!
- Rate limits: 3 requests per 10 seconds per API key; 

## Examples

```bash
#Get the group id by group name. Now i'm looking for the group_id of the group that has "friends" in his name.
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" -d '
{
 "request":"get_groups",
 "params":{
   "starting_from": 1739383324000
   }
}'| jq '.groups[] | select(.group|contains ("friends"))'
# Add a thing and invite a group. When you invite a group, you can't invite other people. You are adding 2 reminders before the thing time in this invite: one with 10 minutes ahead and one with 4 hours. You are adding the thing for the group with the group_id 564564646. The thing time is 1770935248000. Start time needs to be in the future.
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": 1770935248000,
   "alarms":[
     {
        "type": "minutes",
        "value": 10
     },
     {
        "type": "hours",
        "value": 4
     }
    ],
   "invites": [
      {"group_id":564564646 }
    ]
   
 }
}'
#Invites friends to a thing. Add them reminders. Add the phone number of the friend in invitation. The format is country prefix + phone number like in the example. Make sure there is no + within phone number.  You are adding 2 reminders before the thing time in this invite: one with 10 minutes ahead and one with 4 hours. Start time needs to be in the future.
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": 1770935248000,
   "alarms":[
     {
        "type": "minutes",
        "value": 10
     },
     {
        "type": "hours",
        "value": 4
     }
    ],
   "invites": [
      {"phone_number":"19255264501"}
    ]
 }
}'
```
