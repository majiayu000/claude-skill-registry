---
description: Integrate your Alexa Skill with a backend Lambda function with ease, on Sigma IDE
---

# ![AWS Alexa Skill](images/alexa/alexa_icon.svg) AWS Alexa Skill

AWS Alexa is an AI based virtual assistant, which is capable of voice interaction and executing tasks such as providing
real time information such as weather and news. It can be also used as a home automation system by integrating with
smart devices. In addition to the in-built capabilities, it is possible to develop and install **Alexa Skills** to
enable additional capabilities on Alexa.

## Alexa Skill as a Trigger

When such an **Alexa Skill** is developed, it is possible to configure a Lambda function as the backend processing 
component. For that in Sigma, an **Alexa Skill** resource should be dragged from the resources panel and dropped on top 
of the `event` parameter of the lambda handler. Then the Alexa Skill configuration panel can be used to configure it as 
the trigger.

### Trigger Parameters

After an Alexa Skill is configured for the trigger, the following trigger parameters should also be defined.

Parameter               | Required            | Description
---                     | :---:               | ---
Skill Type              | :white_check_mark:  | Whether this Lambda is used for a **Alexa Skills Kit** or for a **Alexa Smart Home** application
Skill ID Verification   | :white_check_mark:  | Whether the Skill ID verification should be enabled for the trigger (only applicable for **Alexa Skills Kit** type)
Skill ID                | :x:                 | If **Skill ID Verification** is enabled, the ID to be verified should be provided (e.g.: `amzn1.ask.skill.a3d4b1a9-6931-45ce-b561-0a7d2f1899fd`)
Application ID          | :white_check_mark:  | The ID of the **Alexa Smart Home** application (only applicable for **Alexa Smart Home** type)

Once the trigger is configured, and the project is deployed, the ARN of the Lambda function should be copied and
configured as the **Service Endpoint** in the Alexa Skill development console.
