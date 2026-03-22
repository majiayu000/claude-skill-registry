---
name: vk
description: "Manage VK.com (Vkontakte) community: post content (text, photos, videos) and handle messages. Use for automating community management via VK API."
---

# VK Community Management

This skill allows you to manage a VK community using the VK API.

## Requirements
- VK Access Token. **Важно:** Используйте **User Token** для полных прав (удаление постов, простая загрузка фото). См. [references/api.md](references/api.md) для деталей.
- Node.js environment.

## Core Workflows

### 1. Posting to the Wall
To post to a community wall:
1. Если есть медиафайлы, загрузите их:
   - `node scripts/vk_cli.js upload-photo $TOKEN $GROUP_ID "./image.jpg"`
2. Используйте `post` с полученным ID вложения:
   - `node scripts/vk_cli.js post $TOKEN -$GROUP_ID "Текст поста" $ATTACH_ID`

### 2. Handling Messages
To respond to user messages:
1. Fetch history with `get-messages`.
2. Send a reply with `message`.

### 3. Real-time Monitoring (Long Poll)
To receive and process messages instantly:
1. Ensure **Long Poll API** is enabled in your group settings (Manage → API Interaction → Long Poll API).
2. Use the `poll` command:
   - `node scripts/vk_cli.js poll $TOKEN $GROUP_ID 1` (where `1` means auto-mark as read).

**Note:** This skill works best with a **User Token** that has `messages,wall,groups,offline` permissions. Use [VK Host](https://vkhost.github.io/) to get a permanent token.

## Advanced Features
For details on setting up Long Poll and specialized API methods, refer to [references/api.md](references/api.md).
