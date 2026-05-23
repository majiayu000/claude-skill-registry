---
name: "Chat Participant Patterns Skill"
description: "VS Code Chat API patterns."
applyTo: "**/*participant*,**/*chat*,**/*copilot*,**/lm/**"
user-invokable: false
---

# Chat Participant Patterns Skill

> VS Code Chat API patterns.

## ⚠️ Staleness Warning

Chat APIs evolve with VS Code releases. **Last validated:** February 2026 (VS Code 1.108+)

**Check:** [Chat API](https://code.visualstudio.com/api/extension-guides/ai/chat), [LM API](https://code.visualstudio.com/api/extension-guides/ai/language-model), [Tools API](https://code.visualstudio.com/api/extension-guides/ai/tools)

---

## Create Participant

```typescript
// package.json contribution
"contributes": {
    "chatParticipants": [{
        "id": "my-ext.participant",
        "name": "myparticipant",
        "fullName": "My Participant",
        "description": "What can I help with?",
        "isSticky": true,
        "commands": [{ "name": "help", "description": "Get help" }]
    }]
}

// In activate()
const participant = vscode.chat.createChatParticipant('my-ext.participant', handler);
participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');
```

## Handler Signature

```typescript
const handler: vscode.ChatRequestHandler = async (
    request: vscode.ChatRequest,
    context: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
): Promise<IChatResult> => {
    // Handle request
};
```

## Key Operations

| Operation | Method |
| --------- | ------ |
| Stream text | `stream.markdown()` |
| Show progress | `stream.progress()` |
| Add button | `stream.button()` |
| File tree | `stream.filetree()` |
| Reference | `stream.reference()` |
| Inline anchor | `stream.anchor()` |
| Access history | `context.history` |
| Get references | `request.references` |
| Get model | `request.model` |
| Check command | `request.command` |
| Chat location | `request.location` |

## Response Types

```typescript
// Markdown (supports CommonMark)
stream.markdown('# Title\n**bold** and _italic_');

// Code block with IntelliSense
stream.markdown('```typescript\nconst x = 1;\n```');

// Progress message
stream.progress('Processing...');

// Button (invokes VS Code command)
stream.button({ command: 'my.command', title: 'Run' });

// Command link in markdown
const md = new vscode.MarkdownString('[Run](command:my.command)');
md.isTrusted = { enabledCommands: ['my.command'] };
stream.markdown(md);

// File tree
stream.filetree([{ name: 'src', children: [{ name: 'app.ts' }] }], baseUri);

// Reference
stream.reference(vscode.Uri.file('/path/to/file.ts'));
stream.reference(new vscode.Location(uri, range));
```

## LM Integration

```typescript
const models = await vscode.lm.selectChatModels({ vendor: 'copilot' });
const response = await models[0].sendRequest(messages, {}, token);
for await (const chunk of response.text) {
    stream.markdown(chunk);
}
```

## Tool Calling

```typescript
// Using @vscode/chat-extension-utils library (recommended)
import * as chatUtils from '@vscode/chat-extension-utils';

const tools = vscode.lm.tools.filter(t => t.tags.includes('my-tag'));
const result = chatUtils.sendChatParticipantRequest(request, context, {
    prompt: 'System instructions here',
    responseStreamOptions: { stream, references: true, responseText: true },
    tools
}, token);
return await result.result;
```

## Tool Registration

```typescript
vscode.lm.registerTool('tool_name', {
    async invoke(options, token) {
        return new vscode.LanguageModelToolResult([
            new vscode.LanguageModelTextPart('result text')
        ]);
    }
});
```

## Participant Detection (Auto-routing)

```json
"chatParticipants": [{
    "id": "my-ext.participant",
    "disambiguation": [{
        "category": "my-domain",
        "description": "Questions about X domain",
        "examples": ["How do I do X?", "Explain Y concept"]
    }]
}]
```

## Follow-up Provider

```typescript
participant.followupProvider = {
    provideFollowups(result, context, token) {
        return [{ prompt: 'Tell me more', label: 'More details' }];
    }
};
```

## Message History

```typescript
// Get previous requests to this participant
const previousRequests = context.history.filter(
    h => h instanceof vscode.ChatRequestTurn
);
```

## Best Practices

| Do | Don't |
| -- | ----- |
| Stream responses incrementally | Block until complete |
| Handle cancellation via token | Ignore cancellation token |
| Catch and handle errors | Let exceptions crash |
| Use progress for long operations | Leave user waiting silently |
| Limit to one participant per extension | Create multiple participants |
| Ask consent for costly operations | Auto-execute destructive actions |

## Synapses

See [synapses.json](synapses.json) for connections.
