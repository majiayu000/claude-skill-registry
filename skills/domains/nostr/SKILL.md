---
name: nostr
description: Knowledge about the Nostr protocol. Use to view up-to-date NIPs, discover capabilities of the Nostr protocol, and to implement Nostr functionality correctly.
license: CC-BY-SA-4.0
---

# Nostr Protocol

Nostr is a simple, open protocol that enables truly censorship-resistant and global social networks using cryptographic keys and signatures.

## Finding Nostr Documentation

All Nostr protocol documentation is maintained in the NIPs (Nostr Implementation Possibilities) repository. To access this information:

### Reading Individual NIPs

Individual NIPs can be fetched from:
```
https://github.com/nostr-protocol/nips/blob/master/{NIP}.md
```

For example, NIP-01 (the basic protocol specification) is available at:
```
https://github.com/nostr-protocol/nips/blob/master/01.md
```

### Finding Event Kinds

Documentation for Nostr event kinds is spread across one or more NIPs. **There is no direct relationship between the NIP number and the kind number.**

To find which NIPs document a specific event kind:

1. First, fetch the README:
   ```
   https://github.com/nostr-protocol/nips/blob/master/README.md
   ```

2. Reference the "Event Kinds" table in the README to find which NIP(s) document the kind you're looking for

### Discovering Existing Capabilities

The README should be consulted to:

- **View the list of NIPs** - Use this to discover what capabilities already exist on the Nostr network
- **Review client and relay messages** - Understand the communication protocol
- **Check the list of tags** - See what standardized tags are available
- **Decide on using existing NIPs** - Before implementing a feature, check if an existing NIP already covers it

### Best Practices

Always start by fetching and reviewing the README to understand the current state of the protocol and avoid reinventing existing functionality.
