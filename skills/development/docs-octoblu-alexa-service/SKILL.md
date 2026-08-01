---
name: docs-octoblu-alexa-service
description: Home | Getting Started | Custom Skill
---

[Home](index.md) | [Getting Started](getting-started.md) | **[Custom Skill](custom-skill.md)**

# Build a Custom Skill

# Table of Contents

* [Creating a Custom Skill](#creating-a-custom-skill)
* [Octoblu Usage](#octoblu-usage)
  * [Flows](#flows)
  * [Custom Flows](#custom-flows)

The Alexa Service, is a micro-service that allows [Octoblu](https://www.octoblu.com) to react and respond to requests from the [Amazon Echo](https://echo.amazon.com) device, or an Alexa App.

Octoblu hosts an instance of the Alexa Service at [alexa.octoblu.com](https://alexa.octoblu.com) and is available for public use.

# Creating a Custom Skill

- Create Amazon Developer Account
- See the [Getting Started Guide](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/getting-started-guide) by Amazon
- Add a new skill on the [skill list](https://developer.amazon.com/edw/home.html#/skills/list) page.
- **Skill Information**
  - Select "Custom Interaction Model"
  - Set your Skill Name
  - Set the Invocation Name
- **Interaction Model**
  - Set the Intent Schema to:
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
  - Create a Custom Slot with a type of "TRIGGER" and the values will be the name of the tasks you want to run. The values should be the same of the "echo-in" node name in your flow.
  - Add the following generic Sample Utterances
```json
{
  "intents": [
    {
      "name": "AMAZON.CancelIntent",
      "samples": []
    },
    {
      "name": "AMAZON.HelpIntent",
      "samples": [
        "what can I do"
      ]
    },
    {
      "name": "AMAZON.StopIntent",
      "samples": []
    },
    {
      "name": "ListTriggers",
      "samples": [
        "what are my triggers",
        "list triggers",
        "tell me my triggers",
        "list my triggers",
        "list my flows",
        "list my nodes",
        "list my echo-in nodes",
        "list my echo in nodes",
        "list my echo ins"
      ],
      "slots": []
    },
    {
      "name": "Trigger",
      "samples": [
        "fire {Name}",
        "fire off {Name}",
        "perform {Name}",
        "do {Name}",
        "trigger {Name}",
        "{Name}"
      ],
      "slots": [
        {
          "name": "Name",
          "type": "TriggerName",
          "samples": []
        }
      ]
    }
  ],
  "types": [
    {
      "name": "TriggerName",
      "values": [
        {
          "id": null,
          "name": {
            "value": "drove cars",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "activate chocolate water bottles",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "green wall",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "cement bacon",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "flash master dream",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "duck minor",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "weather walls up lake black book",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "karate",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "weather",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "stocks",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "lights",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "turn it on",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "my lights",
            "synonyms": []
          }
        },
        {
          "id": null,
          "name": {
            "value": "get the weather",
            "synonyms": []
          }
        }
      ]
    }
  ]
}
```
- **Configuration**
  - Set the Endpoint to HTTPS and `https://alexa.octoblu.com/trigger` or the url of your hosted Alexa Service.
  - Set Account Linking to "Yes"
  - Set the Authorization URL to `https://oauth.octoblu.com/alexa/authorize`
  - Create a Oauth Device / Application in Octoblu
    - Go to your [all things](https://app.octoblu.com/things/all) page.
    - Select and create a new Oauth Device
    - Add a name to the Oauth Device
    - Set the callbackUrl to the Redirect URL listed on the Configuration Page in your Alexa Skill.
    - The Oauth device creating in Octoblu should be discoverable by everyone. This can be set on the permissions tab.
    - The UUID and Token will of the device will be needed for the Alexa Skill. You can get the Token by generating a new one in the device configuration page in octoblu.
  - The Skill Client ID will be the UUID of the Oauth device you created.
  - The Following need to be added to the domain list
    - twitter.com
    - facebook.com
    - google.com
    - citrixonline.com
    - github.com
    - octoblu.com
  - No scope needs to be set
  - Set the Authorization Grant Type to "Auth Code Grant"
  - Set the Access Token URI to "https://oauth.octoblu.com/access_token"
  - Set the Client Secret to the Token of the Oauth Device
  - Set the Client Authentication Scheme to "HTTP Basic"
  - Set the terms to "https://app.octoblu.com/terms" or your own terms.
- **SSL Certificate**
  - Select the option, "My development endpoint has a certificate from a trusted certificate authority"
    - If you are hosting your own Alexa Service you may have different requirements for the SSL configuration.
- **Publishing Information** (If testing this section is optional)
  - This information is specific to your skill
- **Privacy & Compliance** (If testing this section is optional)
  - This information is specific to your skill

If you are getting unauthorized, disable and re-enable your skill, by going to http://alexa.amazon.com/spa/index.html#skills/your-skills and clicking on "link". This should open up another tab, authenticating you with Octoblu.

# Octoblu Usage

## Flows

* [Alexa Create GoToMeeting](https://app.octoblu.com/bluprints/import/297744cf-36d8-473b-b78a-245913c35986)
* [Alexa List GoToMeeting](https://app.octoblu.com/bluprints/import/84aca1ae-a9dd-4268-870c-582a40e2a8f9)
* [Alexa Podio Notifications](https://app.octoblu.com/bluprints/import/0554ffc9-f829-49d0-b9a8-9c4eeff5c9da)
* [Alexa Podio Tasks](https://app.octoblu.com/bluprints/import/7c4c73e8-e7f8-4d70-a5ad-508483343d9b)
* [Alexa Weather](https://app.octoblu.com/bluprints/import/8a262834-f140-43f1-9060-3c564f94eaff)

## Custom Flows
1. Import the base [Alexa Flow](https://app.octoblu.com/bluprints/import/9a6b516c-5f55-4676-bbf5-657612fb35e7)
1. An "Echo In" node in the [Octoblu Designer](https://app.octoblu.com) receives input into a flow from the Alexa Service. The name of the "Echo In" node should match a value in the Trigger custom slot configuration. When a Alexa Request is received, you will get a callbackUrl in the message and other information about the request.
1. An "Echo Out" allows you to respond to the Alexa request. You will need to use the callbackUrl from "Echo In" node. The value should be `{{msg.callbackUrl}}`.
  - You can optionally set the response text.
  - The latest version allows you to respond to an echo-out node with a "response" object. The response object will be passed along to the Alexa response. This gives you full access to the Alexa response object.
1. For every echo-in request, a response needs to be sent through the echo-out node.
1. The flow must be deployed and online.
