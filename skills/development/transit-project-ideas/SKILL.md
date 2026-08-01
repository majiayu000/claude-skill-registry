---
name: transit-project-ideas
description: Paul Swartz
---

# Smart Speaker Skill for "When's the next X bus"

## Author
[Paul Swartz](https://github.com/paulswartz)

## Description

With more homes having a smart speaker, people are accustomed to asking the speaker questions such as "how many ounces are three tablespoons" or "is it going to rain today." To make public transit part of this ecosystem, it would be valuable to provide a speaker skill to answer questions like "when is the next 39 bus" with a human description of the prediction arrival times: "the next inbound 39 buses arrive in 8 minutes and 20 minutes. the next outbound buses arrive in 6 minutes and 15 minutes."

## Data Sources

The MBTA's [V3 API](https://api-v3.mbta.com/) provides the relevant data:
Predictions for upcoming vehicles can be queried around a location (given the latitude/longitude)
Static information about the stop and route are available through the Stops and Routes endpoints

Both [Google](https://developers.google.com/assistant) and [Amazon](https://developer.amazon.com/en-US/alexa/alexa-skills-kit) provide APIs to build skills for their speakers.

## Level
Intermediate
