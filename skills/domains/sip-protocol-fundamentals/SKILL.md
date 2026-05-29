---
name: sip-protocol-fundamentals
description: Use when working with SIP messages, methods, call flows, and protocol fundamentals for VoIP applications.
allowed-tools:
  - Bash
  - Read
---

# SIP Protocol Fundamentals

Master the Session Initiation Protocol (SIP) for building VoIP applications, understanding SIP messages, methods, and call flows essential for real-time communications.

## Understanding SIP

SIP is an application-layer signaling protocol defined in RFC 3261 for creating, modifying, and terminating sessions with one or more participants.

## SIP Message Structure

```
INVITE sip:bob@biloxi.com SIP/2.0
Via: SIP/2.0/UDP pc33.atlanta.com;branch=z9hG4bK776asdhds
Max-Forwards: 70
To: Bob <sip:bob@biloxi.com>
From: Alice <sip:alice@atlanta.com>;tag=1928301774
Call-ID: a84b4c76e66710@pc33.atlanta.com
CSeq: 314159 INVITE
Contact: <sip:alice@pc33.atlanta.com>
Content-Type: application/sdp
Content-Length: 142
```

## When to Use This Skill

Use sip-protocol-fundamentals when building VoIP applications with SIP signaling.

## Best Practices

- Always include unique branch parameters in Via headers
- Implement proper transaction timeout and retransmission
- Handle all SIP response codes appropriately

## Common Pitfalls

- Forgetting to include branch parameter in Via headers
- Not implementing transaction retransmission timers
- Ignoring provisional responses

## Resources

- [RFC 3261 - SIP](https://tools.ietf.org/html/rfc3261)
- [PJSIP](https://www.pjsip.org/)
