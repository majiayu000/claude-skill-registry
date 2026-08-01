---
name: instructions
description: <img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/fact/header.TTH.png"
  />
---

# Build An Alexa Decision Tree Skill
<img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/fact/header._TTH_.png" />


# How to Build a Decision Tree skill for Alexa


## What You Will Learn
*  [Alexa Skills Kit (ASK)](https://developer.amazon.com/alexa-skills-kit)
*  Voice User Interface (VUI) Design
*  Skill Certification
*  Reprompts
*  State Management
*  A Simple Binary ("Yes" or "No") Decision Tree Algorithm Implementation

## What You Will Need
*  [Amazon Developer Portal Account](http://developer.amazon.com)
*  [Amazon Web Services Account](http://aws.amazon.com/) (optional)
*  The sample code provided in this repository.
*  A series of yes or no questions to ask your users and results based on their answers. Good types of question and answers for this could be:
*  Magazine style quizzes like "What kind of job is good for me?", or "Which superhero personality type am I?"
*  Suggestion and Recommendation based skills like "Where cuisine should I eat today?", or "What genre of movie should I watch?"

## What Your Skill Will Do

We make choices every day. We choose what to wear, where to go for dinner, which route to take to work or school. Decision making is a vital and regular part of our livelihood.

Sometimes we're faced with so many choices, that arriving at a conclusive decision can be difficult. Decision trees can help simplify this for us.

Decision trees are a model that provide a structured process to chart out a course of action or arrive at a generalized conclusion, based on specific facts. Inherent in their name, decision trees are visualized as a tree like structure illuminating possible outcomes down a series of branches.

To learn more about decision trees, a good place to start would be [the wikipedia page for Decision Trees](https://en.wikipedia.org/wiki/Decision_tree)

Decision trees can form the basis of many different kinds of Alexa skills. In a turn based adventure game, presenting a user with a choice can progress a narrative. Additionally, decision trees can be utilized to recommend, or suggest a course of action (i.e. "What movie should I watch?").

In this sample skill, we'll explore how a decision tree can be implemented. Alexa will provide an ideal career by asking a series of questions and giving you an answer. Alexa will ask questions such as:
*   "Do you like working with people?"
*   "Do you like caring for others?"
*   "Would you like to work during the day?"

The response to each question will procedurally progress the user through the nodes (branches) in the decision tree.
Alexa will continue asking more questions until a final decision node is reached,
at which point she will suggest an ideal career for you!


### Skill Architecture
Each skill consists of two basic parts, a front end and a back end.
The front end is the voice interface, or VUI.
The voice interface is configured through the voice interaction model.
The back end is where the logic of your skill resides.

### Three Options for Skill Setup
There are a number of different ways for you to setup your skill, depending on your experience and what tools you have available.

 * If this is your first skill, choose the [Alexa-Hosted backend instructions](./setup-vui-alexa-hosted.md) to get started quickly.
 * If you want to manage the backend resources in your own AWS account, you can follow the [AWS-Hosted instructions](./setup-vui-aws-hosted.md).
 * Developers with the ASK Command Line Interface configured may follow the ASK CLI instructions on the main [README](../README.md).


---

<img height="1" width="1" src="https://www.facebook.com/tr?id=1847448698846169&ev=PageView&noscript=1"/>
