---
description: Imported skill _utils from langchain
name: _utils
signature: a23cbada440b01243619a6debd625a3c62c8b7271c74dc4b30fa58576e4b7f6d
source: /a0/tmp/skills_research/langchain/libs/deepagents/deepagents/middleware/_utils.py
---

"""Utility functions for middleware."""

from langchain_core.messages import SystemMessage


def append_to_system_message(
    system_message: SystemMessage | None,
    text: str,
) -> SystemMessage:
    """Append text to a system message.

    Args:
        system_message: Existing system message or None.
        text: Text to add to the system message.

    Returns:
        New SystemMessage with the text appended.
    """
    new_content: list[str | dict[str, str]] = list(system_message.content_blocks) if system_message else []
    if new_content:
        text = f"\n\n{text}"
    new_content.append({"type": "text", "text": text})
    return SystemMessage(content=new_content)
