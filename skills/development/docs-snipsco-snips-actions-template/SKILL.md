---
name: docs-snipsco-snips-actions-template
description: The goal of this document is to explain the various things required in
  a snips skill.
---

# Snips skill specification
The goal of this document is to explain the various things required in a snips skill.

A snips skill is a folder containing the code needed to handle intents generated from the snips platform.

This folder is given to the snips-skills-server that will ensure the skill is running.

## Files required by the skill server

The skill server expects files named `action-*` to be at the root of the folder. These files must be executables and are expected to contain code connecting to the MQTT server and "looping forever" on it. Typical example of such an executable is a python script using the `hermes-python` library.

Each of these executable will be started by the skill server (and restarted in case the process exits/cashes).

If a subfolder named `venv` exists, the `snips-skill-server` will try to activate the virtualenv before starting the executables (ie sourcing `venv/bin/activate` before starting the executable). This can be used to easily install dependencies for a pyhton script.

Any other file or folder is ignored by the `snips-skill-server`

## Other interesting files.

By convention any configuration needed to be done before running should be done in a script named `setup.sh`. `sam` will automatically launch such a script upon install of a skill. If not using `sam` the user should launch it by hand. The rights required to run this script should be only write access to the skill dir, this script should not be used to install systemwide dependencies, and just be used to for example setup a python virtualenv or compile some source files.

By convention also, actions files should read there configuration in a file named `config.ini`. A section `secret` should be used for parameters that are sensitive (passwords / api keys...)

It is a good idea to include a `README` file explaining what the skill is doing, how to configure it, etc.

## `snips-template`

The `snips-template` executable can be used to generate such skill folders from snippets included by the console in `assistant.zip` files. Future version should include a `bootstrap` command to generate empty skill folders.

By default `snips-template` will generate one `action-` file per intent, but this is not something required by the spec (ie you can manage mulitple intents in the same executable if you want)

