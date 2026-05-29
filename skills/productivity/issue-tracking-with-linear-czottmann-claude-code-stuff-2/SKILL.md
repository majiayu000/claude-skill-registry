---
name: issue-tracking-with-linear
description: Use when working with Linear tickets/issues - establishes workflows for creating and updating tickets (issues)
---

## Accessing Linear

Use your Bash tool to call the `linearis` executable for communicating with Linear. Prior to your first use of `linearis` you must run `linearis usage` once to learn how to use it.

## Creating issues and sub-issues

If it's not clear which project a new ticket belongs to, stop and ask the user. When creating sub-issues, use the parent ticket's project.

## Working on issues

When you work on or make changes to a ticket, you must add your label to it. You'll find your label in the ENV var `AGENTS_CONSTRUCTION_KIT__LINEAR_LABEL`. If that ENV var is empty, stop and ask me.

The return values of the `issues` commands contain an `embeds` array which holds the URLs of the screenshots, documents, etc. that are part of the ticket description. If a ticket or comment contains such embeds, fetch and view them as well. Use local caching when needed.

## Updating tickets

When you work on a ticket, and the the status of a task in the ticket description has changed (task incomplete -> task done), update the description.

When updating a ticket with a progress report that is more than just a checkbox change, add that report as a ticket comment.

General rule: The ticket description is the starting point for planning. But when work is ongoing, I want to be able to retrace our steps by looking at the ticket and its comments.

## Eagerness

Never declare "Implementation Complete!" in a ticket unless explicitly told so.
