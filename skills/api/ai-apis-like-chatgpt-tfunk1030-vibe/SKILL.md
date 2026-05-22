---
name: ai-apis-like-chatgpt
description: How to use AI APIs like OpenAI, ChatGPT, Elevenlabs, etc. When a user asks you to make an app that requires an AI API, use this skill to understand how to use the API or how to respond to the user.
---

# ai-apis-like-chatgpt

## Instructions
The Vibecode Enviroment comes pre-installed with a lot of AI APIs like OpenAI, ChatGPT, Elevenlabs, etc. You can use these APIs to generate text, images, videos, sounds, etc.

Users can find most of the APIs in the API tab of the Vibecode App. You can tell the user to look there for any custom or advanced API integrations.

However, we will go over the basic OpenAI APIs.

## Examples

### Responses API (Generate text, analyze images, search the web)

You can use the OpenAI Responses API to generate text, search the web, and analyze images. The latest model family is `gpt-5.2` as of December 2025. Docs: https://platform.openai.com/docs/api-reference/responses/create

**Basic request:**
```typescript
const response = await fetch("https://api.openai.com/v1/responses", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${process.env.EXPO_PUBLIC_VIBECODE_OPENAI_API_KEY}`,
  },
  body: JSON.stringify({ model: "gpt-5.2", input: "Your prompt here" }),
});
```

**Vision (Image Analysis):** Use `expo-image-picker` to select images. You must use `expo-file-system` to read as base64 data URL:
```typescript
import * as ImagePicker from "expo-image-picker";
import * as FileSystem from "expo-file-system";

// Pick image from library
const result = await ImagePicker.launchImageLibraryAsync({
  mediaTypes: ["images"],
  allowsEditing: true,
  quality: 0.8,
});
if (result.canceled) return;
const imageUri = result.assets[0].uri;

// Read as base64 and build data URL
const base64 = await FileSystem.readAsStringAsync(imageUri, {
  encoding: FileSystem.EncodingType.Base64,
});
const mimeType = imageUri.endsWith(".png") ? "image/png" : "image/jpeg";
const dataUrl = `data:${mimeType};base64,${base64}`;

// Send to vision API
const response = await fetch("https://api.openai.com/v1/responses", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${process.env.EXPO_PUBLIC_VIBECODE_OPENAI_API_KEY}`,
  },
  body: JSON.stringify({
    model: "gpt-5.2",
    input: [{
      role: "user",
      content: [
        { type: "input_text", text: "What's in this image?" },
        { type: "input_image", image_url: dataUrl },
      ],
    }],
  }),
});
```

### Image Generation API (Generate images)

Model: `gpt-image-1`. Docs: https://platform.openai.com/docs/api-reference/images/create

```typescript
const response = await fetch("https://api.openai.com/v1/images/generations", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${process.env.EXPO_PUBLIC_VIBECODE_OPENAI_API_KEY}`,
  },
  body: JSON.stringify({
    model: "gpt-image-1",
    prompt: "A cute baby sea otter",
    n: 1,
    size: "1024x1024",
  }),
});
const data = await response.json();
const imageUrl = data.data[0].url; // or data.data[0].b64_json for base64
```

### Image Edit API (Edit images)

Model: `gpt-image-1`. Docs: https://platform.openai.com/docs/api-reference/images/createEdit

Use `File` from `expo-file-system/next` and `.blob()` for FormData (same pattern as audio):
```typescript
import { File } from "expo-file-system/next";

const file = new File(imageUri);
const blob = await file.blob();

const formData = new FormData();
formData.append("image", blob, file.name);
formData.append("prompt", "Add a hat to the person");
formData.append("model", "gpt-image-1");
formData.append("n", "1");
formData.append("size", "1024x1024");

const response = await fetch("https://api.openai.com/v1/images/edits", {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.EXPO_PUBLIC_VIBECODE_OPENAI_API_KEY}` },
  body: formData,
});
const data = await response.json();
const editedImageUrl = data.data[0].url;
```

### Audio Transcription API (Transcribe audio)

Model: `gpt-4o-transcribe`. Docs: https://platform.openai.com/docs/api-reference/audio/create

**React Native FormData with expo/fetch:** Use `File` from `expo-file-system/next` and call `.blob()`:
```typescript
import { File } from "expo-file-system/next";

const file = new File(audioUri); // audioUri from expo-av recording
const blob = await file.blob();

const formData = new FormData();
formData.append("file", blob, file.name);
formData.append("model", "gpt-4o-transcribe");

const response = await fetch("https://api.openai.com/v1/audio/transcriptions", {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.EXPO_PUBLIC_VIBECODE_OPENAI_API_KEY}` },
  body: formData,
});
const data = await response.json();
const transcription = data.text;
```

**Recording audio:** Use `expo-av` to record. See: https://docs.expo.dev/versions/latest/sdk/av/