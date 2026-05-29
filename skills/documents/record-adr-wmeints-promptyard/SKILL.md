---
name: record-adr
description: Use this to create or modify architecture decision records (ADRs)
---

IMPORTANT: Use the template stored in `./templates/adr.md` to record the architecture decision.

## Guidelines for recording the decision

- Use a single sentence to describe the decision made.
- Defer any explanation for why to the context section.

## Guidelines for recording the context

- Make sure to include alternatives to the choice we're recording.
- Explain why we have to make the choice in the first place.

IMPORTANT: If you don't have this information, ask the user to provide the information!

## Guidelines for recording the options considered

- Create a sub section per option and provide a short description of the pros and cons of the option.
- Keep the description short and consise

## Guidelines for recording the consequences

- List the consequences one-by-one
- Include both positive and negative consequences in the list

## Where to store the ADR files

- Store ADR files in `docs/architecture/adr`
- Give a unique number to each ADR and write files like this: `001-title-of-the-adr.md`
- Include the ADR in the TOC in `09-decisions.md` located in in `docs/architecture`