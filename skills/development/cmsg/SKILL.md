---
name: cmsg
description: 'Direction: Client -> Server'
---

# CMSG_USE_SKILL (0x0017)

**Direction**: Client -> Server
**Status**: Confirmed (Schema-Driven, Live-Validated)

## Summary

This opcode is used by the client to inform the server about a skill activation. The process typically involves a sequence of two packets: a larger, data-rich packet to initiate the skill, followed by a smaller, simpler packet that may act as a confirmation or state update.

The packet is schema-driven, and its variable size is a direct result of a large **Optional Block** within its schema. The first packet in the sequence includes this optional data, while the second one omits it, resulting in the different observed sizes (e.g., 40 bytes and 16 bytes).

## Construction Chain

The packet is created via a deep and complex call chain, confirming it as a core gameplay action:

1.  **Skill Command Handler (`CMSG_Skill_CommandHandler`):** The top-level function that receives the command to use a skill.
2.  **Pre-Aggregator/Gate (`CMSG_Skill_PreAggregator`):** Validates the skill use and identifies the generic builder function that needs to be called.
3.  **Data Aggregator (at `*param_1 + 0x30`):** A virtual function that gathers all the detailed skill data (target, position, etc.) into a temporary structure.
4.  **Generic Builder (`CMSG_Builder_FromAggregatedData`):** The aggregator makes a virtual call to this function, passing it the temporary data structure.
5.  **Serialization (`CMSG::BuildAndSendPacket`):** The generic builder calls the main serialization engine, which uses the schema for opcode `0x0017` to build the packet.
6.  **Sending Mechanism (Buffered Stream):** The packet is written to the main `MsgSendContext` buffer and sent in a batch when `MsgConn::FlushPacketBuffer` is called.

## Schema Information

- **Opcode:** `0x0017`
- **Schema Address (Live):** `0x7FF6E0EA5FB0`

## Packet Structure (Decoded from Schema)

The full packet structure contains 7 primary fields. The final field is an **Optional Block** which, when present, contains another 5 fields. This optional block is what causes the size difference between the first and second packets in a skill-use sequence.

| Field # | Typecode | Data Type (Inferred) | Description |
| :--- | :--- | :--- | :--- |
| 1 | `0x01` | `short` | A subtype or sequence ID. Observed as `0x009B`. |
| 2 | `0x03` | `short` | A secondary subtype or sequence ID. |
| 3 | `0x04` | Compressed `int` | A timestamp or server tick. |
| 4 | `0x02` | `byte` | A flag or state byte. |
| 5 | `0x04` | Compressed `int` | An ID, possibly the target agent ID. |
| 6 | `0x14` | Small Buffer | A buffer with a 1-byte length prefix. |
| 7 | `0x0F` | **Optional Block** | If present, contains the detailed skill context. |
| 7a | `0x01` | `short` | (Optional) Subtype for the skill context. |
| 7b | `0x04` | Compressed `int` | (Optional) Timestamp for the skill context. |
| 7c | `0x02` | `byte` | (Optional) Flag. |
| 7d | `0x04` | Compressed `int` | (Optional) Target Agent ID for the context. |
| 7e | `0x14` | Small Buffer | (Optional) Additional data buffer for the context. |

### Schema Analysis Notes
The structure above is confirmed by a direct decoding of the schema definition at `0x7FF6E0EA5FB0`. Analysis of the `Msg::MsgPack` assembly (`0x00fd2d5f`) shows that typecode `0x03` is handled by the same code path as `0x01`, confirming it as a `short`.

## Live Packet Samples

**Default Attack Sequence:**
```
03:54:27.491 [S] CMSG_USE_SKILL Op:0x0017 | Sz:40 | 17 00 9B 00 C9 F1 0C 03 83 D5 81 80 08 02 2A 05 17 00 9B 00 C9 F1 0C 03 85 D5 81 80 08 0A 23 00 00 00 00 09 74 00 00 05
03:54:27.556 [S] CMSG_USE_SKILL Op:0x0017 | Sz:16 | 17 00 9B 00 CB F1 0C 03 86 D5 81 80 08 02 29 05
```
The 40-byte packet contains the full structure including the Optional Block. The 16-byte packet contains only the first 5 fields.

