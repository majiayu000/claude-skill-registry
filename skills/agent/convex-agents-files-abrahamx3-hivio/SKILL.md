---
name: "Convex Agents Files"
description: "Handles file uploads, image attachments, and media processing in agent conversations. Use this when agents analyze images, process documents, or generate files."
---

## Purpose

Files and images let agents understand and generate visual content. Covers uploading, storing, attaching to messages, and managing file lifecycle.

## When to Use This Skill

- Users upload images for agent analysis
- Agents need to process documents or files
- Agents generate images with DALL-E
- Building file-based workflows
- Implementing file cleanup and tracking

## Upload and Store a File

```typescript
import { storeFile } from "@convex-dev/agent";

export const uploadFile = action({
  args: { fileData: v.string(), filename: v.string(), mimeType: v.string() },
  handler: async (ctx, { fileData, filename, mimeType }) => {
    const bytes = Buffer.from(fileData, "base64");

    const { file } = await storeFile(
      ctx,
      components.agent,
      new Blob([bytes], { type: mimeType }),
      { filename, sha256: "hash" }
    );

    return {
      fileId: file.fileId,
      url: file.url,
      storageId: file.storageId,
    };
  },
});
```

## Send File with Message (2-Step)

Upload first, then send message with attachment:

```typescript
import { saveMessage, getFile } from "@convex-dev/agent";

// Step 1: Save message with file
export const submitFileQuestion = mutation({
  args: { threadId: v.string(), fileId: v.string(), question: v.string() },
  handler: async (ctx, { threadId, fileId, question }) => {
    const { imagePart, filePart } = await getFile(ctx, components.agent, fileId);

    const { messageId } = await saveMessage(ctx, components.agent, {
      threadId,
      message: {
        role: "user",
        content: [
          imagePart ?? filePart,
          { type: "text", text: question },
        ],
      },
      metadata: { fileIds: [fileId] },
    });

    return { messageId };
  },
});

// Step 2: Generate response
export const generateFileResponse = action({
  args: { threadId: v.string(), promptMessageId: v.string() },
  handler: async (ctx, { threadId, promptMessageId }) => {
    const { thread } = await myAgent.continueThread(ctx, { threadId });
    await thread.generateText({ promptMessageId });
  },
});
```

## Inline File Saving (Action Only)

Pass file directly in generation:

```typescript
export const analyzeImageInline = action({
  args: { threadId: v.string(), imageData: v.string(), question: v.string() },
  handler: async (ctx, { threadId, imageData, question }) => {
    const { thread } = await myAgent.continueThread(ctx, { threadId });

    await thread.generateText({
      message: {
        role: "user",
        content: [
          {
            type: "image",
            image: Buffer.from(imageData, "base64"),
            mimeType: "image/png",
          },
          { type: "text", text: question },
        ],
      },
    });
  },
});
```

## Generate and Save Images

```typescript
export const generateAndSaveImage = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { image } = await generateImage({
      model: openai.image("dall-e-2"),
      prompt,
    });

    const { file } = await storeFile(ctx, components.agent, image, {
      filename: `generated-${Date.now()}.png`,
    });

    return { fileId: file.fileId };
  },
});
```

## Key Principles

- **Automatic storage**: Files > 64KB stored automatically
- **File tracking**: Metadata tracks which messages reference files
- **URL generation**: Signed URLs prevent unauthorized access
- **MIME type inference**: Auto-detected if not provided
- **Cleanup**: Files tracked for garbage collection

## Next Steps

- See **messages** for message management
- See **streaming** for streamed file processing
- See **fundamentals** for agent setup
