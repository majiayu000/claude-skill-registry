---
name: docs-danisla-iot-bed
description: The Custom Skill is used instead of the Home Skill because the Home skill
  assumes you have a OAuth service managing the IoT devices where the Custom Skill
  can just invoke a Lambda function with a custom intent mapping.
---

# Configure Alexa Custom Skill for IoT Bed

The Custom Skill is used instead of the Home Skill because the Home skill assumes you have a OAuth service managing the IoT devices where the Custom Skill can just invoke a Lambda function with a custom intent mapping.

## Intent Schema

```js
{
  "intents": [
    {
      "intent": "SetPreset",
      "slots": [
        {
          "name": "Preset",
          "type": "LIST_OF_PRESETS"
        }
      ]
    },
    {
      "intent": "SetMassage",
      "slots": [
        {
          "name": "State",
          "type": "LIST_OF_STATES"
        }
      ]
    }
  ]
}
```

`LIST_OF_PRESETS` custom slot type:

```
flat
0g
0 g
tv
```

`LIST_OF_STATES` custom slot type:

```
on
off
```

> NOTE that the zero-g preset is listed as `0g` this is what is passed when 'Zero-G' is passed via AVS.

## Sample Utterances File

```
SetPreset turn on {Preset}
SetMassage turn massage {State}
SetPreset turn on preset {Preset}
SetPreset turn on {Preset} preset
```

## Create Skill

Follow the wizard on the [Amazon Developer Portal](https://developer.amazon.com/edw/home.html) to create the custom skill for Alexa in your account.

Enter the Intent Schema, custom slot types and Sample Utterances File from above to their respective fields.

> NOTE as of writing, Alexa skills only work with the IoT Devices and Lambda functions in the us-east-1 region.

## Testing

Make sure the following is setup before testing:

- Alexa Custom skill is enabled (check alexa mobile app)
- Lambda function with correct version is set in the Alexa Skill Configuration
- [`iot-bed.py`](https://github.com/danisla/iot-bed/blob/master/src/iot/iot-bed.py) script is running on your CHIP or Raspberry Pi device.

Now, ask Alexa to adjust your bed:

```
Alexa, tell bed to turn on zero g
```

> The bed should move to the Zero-G position


```
Alexa, tell bed to turn on flat preset
```

> The bed should move to the Flat position


```
Alexa, tell bed to turn massage on
```

> The bed should start the massage at the lowest level.


```
Alexa, tell bed to turn massage on
```

> The bed should increase the massage level.


```
Alexa, tell bed to turn massage off
```

> The bed should increase the massage level twice then turn off.

If the voice commands worked then you successfully hacked your bed and turned it into a cloud-connected voice-controlled device. Welcome to the Internet of Things, I need a nap.

## References

- [Amazon Developer Portal](https://developer.amazon.com/edw/home.html)
- [Blog about using Alexa Skills with IoT devices](https://developer.amazon.com/public/community/post/Tx3828JHC7O9GZ9/Using-Alexa-Skills-Kit-and-AWS-IoT-to-Voice-Control-Connected-Devices)
- [Alexa Smart Home Skills API](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/smart-home-skill-api-reference)
