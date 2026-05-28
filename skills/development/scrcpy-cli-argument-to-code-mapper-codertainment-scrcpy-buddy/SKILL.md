---
name: scrcpy-cli-argument-to-code-mapper
description: This skill should generate classes for scrcpy CLI arguments. This skill should be used when adding support for new scrcpy CLI arguments to the app.
---

# Scrcpy CLI Argument to Code mapper

Supported or plan-to-be-supported arguments are documented inside [/docs/scrcpy_options/](/docs/scrcpy_options/). 

Refer to this folder first to get an idea about the CLI argument. See below for more details.

## Steps

1. Gather information
2. Create class(es) inside categorised directories

## 1. Gather information: Option name, description and type

Refer to [/docs/scrcpy_options](/docs/scrcpy_options) for the categorised and supported options.

Each file lists the options for that category.

The information is in a table format, indicating the scrcpy argument, a short description, it's UI control type and
whether it should be inside the "Advanced" section

## 1. Gather information: Unknown CLI argument

If information for the requested CLI argument cannot be found in the folder:

- Refer to [scrcpy docs](https://github.com/Genymobile/scrcpy) and
  the [latest releases](https://github.com/Genymobile/scrcpy/releases)
- Come up with a draft in the following format: argument, description, UI Control type, Advanced?
- Confirm with the user before proceeding

## 2. Create class(es)

- Refer to [Supported scrcpy CLI Options](/README.md) to get an understanding of the current structure.
- Refer to classes inside `@lib/application/model/scrcpy/arguments/video` to get an understanding of the existing
  format.
- Then, proceed to create classes inside their category directory in `@lib/application/model/scrcpy/arguments`. (Create
  category directory if it doesn't exist yet)
