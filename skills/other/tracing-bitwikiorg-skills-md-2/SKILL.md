---
description: Imported skill tracing from langchain
name: tracing
signature: 55e225e09d09984dee0fceb0daed0fd9527dfbefdf49a6ee22903b3beb4cb0c6
source: /a0/tmp/skills_research/langchain/libs/harbor/deepagents_harbor/tracing.py
---

"""LangSmith integration for Harbor DeepAgents."""

import hashlib
import uuid


def create_example_id_from_instruction(instruction: str, seed: int = 42) -> str:
    """Create a deterministic UUID from an instruction string.

    Normalizes the instruction by stripping whitespace and creating a
    SHA-256 hash, then converting to a UUID for LangSmith compatibility.

    Args:
        instruction: The task instruction string to hash
        seed: Integer seed to avoid collisions with existing examples

    Returns:
        A UUID string generated from the hash of the normalized instruction
    """
    # Normalize the instruction: strip leading/trailing whitespace
    normalized = instruction.strip()

    # Prepend seed as bytes to the instruction for hashing
    seeded_data = seed.to_bytes(8, byteorder="big") + normalized.encode("utf-8")

    # Create SHA-256 hash of the seeded instruction
    hash_bytes = hashlib.sha256(seeded_data).digest()

    # Use first 16 bytes to create a UUID
    example_uuid = uuid.UUID(bytes=hash_bytes[:16])

    return str(example_uuid)
