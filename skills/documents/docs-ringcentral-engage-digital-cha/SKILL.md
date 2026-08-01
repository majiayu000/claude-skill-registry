---
name: docs-ringcentral-engage-digital-cha
description: 'For a simple ping-pong bot skill:'
---

# Write/use a bot skill

## Write a bot skill

For a simple ping-pong bot skill:

```js

const cheerio = require('cheerio')
const _ = require('lodash')

exports.name = 'ping-pong bot skill'

exports.description = 'reply to "ping" with "pong"'

function isPing (event) {
  let $ = cheerio.load(_.get(event, 'resource.metadata.body'))
  let txt = $('body').text().trim()
  console.log('txt:', txt)
  return txt === 'ping'
}

exports.onEvent = async ({
  event,
  client,
  handled // hanlded by prev skills
}) => {
  if (handled) {
    return
  }
  if (isPing(event)) {
    await client.reply(event, {
      title: 'pong',
      body: 'pong'
    })
    return true
  }
}

```

For full config, check [full-config-skill.js](../example-skills/full-config-skill.js)

## Use a bot skill

```js
// in you bot file
const skillA = require('skill-a')
const skillB = require('skill-b')
exports.skills = [skillA, skillB]
```

That is it.

## Real example

- todo
