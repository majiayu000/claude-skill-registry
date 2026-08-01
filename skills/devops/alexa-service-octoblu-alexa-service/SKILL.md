---
name: alexa-service
description: '"intent": "ListTriggers"'
---

## Intent Schema

```json
{
  "intents": [
    {
      "intent": "Trigger",
      "slots": [
        {
          "name": "Name",
          "type": "TRIGGER"
        }
      ]
    },
    {
      "intent": "ListTriggers"
    },
    {
      "intent": "AMAZON.HelpIntent"
    },
    {
      "intent": "AMAZON.StopIntent"
    },
    {
      "intent": "AMAZON.CancelIntent"
    }
  ]
}
```

## Custom Slot Types:

### `TRIGGER`

* tasks
* notifications
* podio notifications
* meetings
* create meeting

## Sample Utterances

```txt
Trigger give me the {Name}
Trigger give me {Name}
Trigger give me a {Name}
Trigger get me the {Name}
Trigger get me {Name}
Trigger get me a {Name}
Trigger could you set {Name}
Trigger could you please set {Name}
Trigger i need {Name}
Trigger i need {Name} please
Trigger tell me my {Name}
Trigger list {Name}
Trigger i want {Name}
Trigger create {Name}
Trigger create a {Name}
ListTriggers what my triggers are
ListTriggers give me a list of my triggers
ListTriggers get me a list of my triggers
ListTriggers a list of my triggers
ListTriggers my triggers
ListTriggers the triggers i have
ListTriggers what triggers do i have
```

### Example commands

* Alexa ask Citrix list my tasks
* Alexa ask Citrix list my meetings
* Alexa ask Citrix create meeting
* Alexa ask Citrix get me my notifications
* Alexa ask Citrix my triggers
* Alexa ask Citrix help
