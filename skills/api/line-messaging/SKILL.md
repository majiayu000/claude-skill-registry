---
name: line-messaging
description: World-class expert LINE Messaging API and LINE Official Account specialist. Use when building LINE bots, integrating LINE Login, implementing webhook handling, creating rich menus, or working with LINE Platform APIs including Messaging API, LIFF, and LINE OA features at production scale.
---

# LINE Messaging API & LINE OA Expert - World-Class Edition

## Project Context: DriverConnect (eddication.io)

**IMPORTANT**: This project uses LINE LIFF for the driver-facing mobile application.

### LIFF Application Details

- **App Name**: DriverConnect Driver App
- **App Folder**: `PTGLG/driverconnect/driverapp/`
- **Entry Point**: `PTGLG/driverconnect/driverapp/index.html`
- **Config**: `PTGLG/driverconnect/driverapp/config.js`

### LIFF Features Used

| Feature | Implementation | File |
| :--- | :--- | :--- |
| **Profile Access** | Get driver name, picture URL | `js/app.js` |
| **Context Detection** | Chat vs web view detection | `js/app.js` |
| **Send Messages** | Job completion notifications | `js/app.js` |
| **Close Window** | After job completion | `js/app.js` |
| **Friendship Status** | Check if following LINE OA | N/A |

### Key LIFF Functions

```javascript
// Initialize LIFF
await liff.init({ liffId: config.LIFF_ID, withLoginOnExternalBrowser: true });

// Get driver profile
const profile = liff.getProfile();
// Returns: { userId, displayName, pictureUrl, statusMessage }

// Check if in LINE app
const inClient = liff.isInClient();

// Get context (1:1 chat vs group chat)
const context = liff.getContext();
// Returns: { type: 'ut' | 'none', viewType: 'full' | 'tall' | 'compact', userId }

// Send message after job completion
await liff.sendMessages([{ type: 'text', text: 'Job completed!' }]);

// Close LIFF after completion
liff.closeWindow();
```

### LINE OA Features (Planned)

- **Rich Menu**: Dynamic menu based on driver status
- **Quick Reply**: For check-in confirmation
- **Flex Messages**: For job details display
- **Broadcast**: For job assignments

### Configuration File

`PTGLG/driverconnect/driverapp/config.js`:

```javascript
const config = {
  LIFF_ID: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
  LINE_CHANNEL_ID: 'xxxxxxxx',
  // ... other config
};
```

---

## Overview

You are a world-class expert in LINE Platform development, specializing in the LINE Messaging API, LINE Official Accounts (LINE OA), and related services. You design scalable, secure, and production-ready LINE bots with advanced features like interactive flows, rich UI components, and enterprise integrations.

---

# Philosophy & Principles

## Core Principles
1. **Webhook Reliability** - Always verify signatures, handle retries
2. **Rate Limiting** - Respect LINE's API limits
3. **UX First** - Design intuitive conversational flows
4. **Scalability** - Use efficient data structures and caching
5. **Security** - Validate all inputs, never expose secrets
6. **Thai Language Support** - Full support for Thai users

## Best Practices
- **Always verify webhook signatures** for security
- **Use reply tokens** instead of push when possible
- **Implement graceful degradation** for unsupported features
- **Monitor webhook delivery** for reliability
- **Test on both 1:1 and group chats**
- **Handle all edge cases** in user interactions

---

# LINE Platform Architecture

## Service Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      LINE Platform                          │
│  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐       │
│  │  Messaging  │ │  LINE Login  │ │     LIFF     │       │
│  │    API      │ │              │ │              │       │
│  └─────────────┘ └──────────────┘ └───────────────┘       │
│  ┌─────────────┐ ┌──────────────────┐ ┌─────────────┐     │
│  │  LINE OA    │ │  Messaging API   │ │   Modules   │     │
│  │ Management  │ │  Webhook Server  │ │   Insight   │     │
│  └─────────────┘ └──────────────────┘ └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Your Application                        │
│  Web Server  │  Edge Functions  │  Message Queue  │  DB  │
└─────────────────────────────────────────────────────────────┘
```

## Service Relationships

| Service | Description | Use Case |
|---------|-------------|----------|
| **Messaging API** | Send/receive messages | Chatbots, notifications |
| **LINE Login** | OAuth authentication | User authentication |
| **LIFF** | Web app in LINE | Embedded web apps |
| **LINE OA** | Official account management | Business accounts |
| **Modules** | Messaging extensions | Custom message types |

---

# Messaging API Deep Dive

## Webhook Server Implementation

### Express.js Webhook Handler

```typescript
import express from 'express';
import crypto from 'crypto';
import { LineClient } from './line-client';

const app = express();

// Signature verification middleware
function verifySignature(
  channelSecret: string
): express.RequestHandler {
  return (req, res, next) => {
    const signature = req.headers['x-line-signature'];
    if (!signature) {
      return res.status(401).send('Missing signature');
    }

    const body = JSON.stringify(req.body);
    const hash = crypto
      .createHmac('SHA256', channelSecret)
      .update(body)
      .digest('base64');

    if (signature !== hash) {
      return res.status(401).send('Invalid signature');
    }

    next();
  };
}

// Webhook endpoint
app.post(
  '/webhook',
  express.raw({ type: 'application/json' }),
  verifySignature(process.env.LINE_CHANNEL_SECRET!),
  async (req, res) => {
    const events = req.body.events;
    const client = new LineClient(process.env.LINE_ACCESS_TOKEN!);

    for (const event of events) {
      try {
        await handleEvent(event, client);
      } catch (error) {
        console.error('Error handling event:', error);
        // Log to monitoring system
      }
    }

    res.status(200).send('OK');
  }
);

// Event handler router
async function handleEvent(event: WebhookEvent, client: LineClient) {
  switch (event.type) {
    case 'message':
      await handleMessage(event, client);
      break;
    case 'follow':
      await handleFollow(event, client);
      break;
    case 'unfollow':
      await handleUnfollow(event);
      break;
    case 'join':
      await handleJoin(event, client);
      break;
    case 'leave':
      await handleLeave(event);
      break;
    case 'postback':
      await handlePostback(event, client);
      break;
    case 'beacon':
      await handleBeacon(event, client);
      break;
    default:
      console.log('Unknown event type:', event.type);
  }
}
```

### Type Definitions

```typescript
// Event source types
interface EventSource {
  type: 'user' | 'group' | 'room';
  userId?: string;
  groupId?: string;
  roomId?: string;
}

// Message event
interface MessageEvent {
  type: 'message';
  mode: 'active' | 'standby';
  timestamp: number;
  source: EventSource;
  replyToken: string;
  webhookEventId: string;
  deliveryContext: { isRedelivery: boolean };
  message: Message;
}

// Message types
type Message =
  | TextMessage
  | ImageMessage
  | VideoMessage
  | AudioMessage
  | LocationMessage
  | StickerMessage
  | FileMessage
  | LocationMessage;

interface TextMessage {
  id: string;
  type: 'text';
  text: string;
  emojis?: Emoji[];
  mention?: Mention;
}

interface ImageMessage {
  id: string;
  type: 'image';
  contentProvider: ContentProvider;
  imageSet?: ImageSet;
}

interface StickerMessage {
  id: string  ;
  type: 'sticker';
  packageId: string;
  stickerId: string;
  stickerResourceType: 'STATIC' | 'ANIMATION' | 'ANIMATION_SOUND' | 'POPUP' | 'POPUP_SOUND' | 'CUSTOM' | 'MESSAGE';
}

// Follow event
interface FollowEvent {
  type: 'follow';
  mode: 'active' | 'standby';
  timestamp: number;
  source: EventSource;
  replyToken: string;
  webhookEventId: string;
}

// Postback event
interface PostbackEvent {
  type: 'postback';
  mode: 'active' | 'standby';
  timestamp: number;
  source: EventSource;
  replyToken: string;
  postback: {
    data: string;
    params?: PostbackParams;
  };
}

interface PostbackParams {
  date?: string;
  time?: string;
  datetime?: string;
  new comer_status?: string;
  newcomerItems?: Record<string, unknown>;
}

// Beacon event (for LINE Things)
interface BeaconEvent {
  type: 'beacon';
  hwid: string;
  type: string;
  deviceContext?: {
    inactivityDuration?: number;
  };
}

type WebhookEventType = MessageEvent | FollowEvent | UnfollowEvent | JoinEvent | LeaveEvent | PostbackEvent | BeaconEvent;
```

## Message Types Complete Reference

### Text Message with Features

```typescript
// Basic text
const basicText: TextMessage = {
  type: 'text',
  text: 'Hello, World!'
};

// With emojis
const textWithEmojis: TextMessage = {
  type: 'text',
  text: '$ Hello!',
  emojis: [
    {
      index: 0,
      productId: '5ac1b400029d2f6779d1',
      emojiId: '01'
    }
  ]
};

// With mention
const textWithMention: TextMessage = {
  type: 'text',
  text: '@displayName Hello!',
  mention: {
    mentionees: [
      {
        index: 0,
        length: 12,
        userId: 'U1234567890'
      }
    ]
  }
};
```

### Template Messages

```typescript
// Buttons template
interface ButtonsTemplate {
  type: 'template';
  altText: string;
  template: {
    type: 'buttons';
    thumbnailImageUrl?: string;
    imageAspectRatio?: 'rectangle' | 'square';
    imageSize?: 'cover' | 'contain';
    imageBackgroundColor?: string;
    title?: string;
    text: string;
    defaultAction?: URIAction;
    action?: URIAction;
    actions: Action[];
  };
}

// Confirm template
interface ConfirmTemplate {
  type: 'template';
  altText: string;
  template: {
    type: 'confirm';
    text: string;
    defaultAction?: URIAction;
    actions: [Action, Action];
  };
}

// Carousel template
interface CarouselTemplate {
  type: 'template';
  altText: string;
  template: {
    type: 'carousel';
    imageAspectRatio?: 'rectangle' | 'square';
    imageSize?: 'cover' | 'contain';
    columns: CarouselColumn[];
  };
}

interface CarouselColumn {
  thumbnailImageUrl?: string;
  imageBackgroundColor?: string;
  title?: string;
  text: string;
  defaultAction?: URIAction;
  actions: Action[];
  image?: {
    url: string;
    size: 'cover' | 'contain';
    aspectRatio: 'rectangle' | 'square';
    backgroundColor: string;
  };
}

// Image carousel template
interface ImageCarouselTemplate {
  type: 'template';
  altText: string;
  template: {
    type: 'image_carousel';
    columns: ImageCarouselColumn[];
  };
}

interface ImageCarouselColumn {
  imageUrl: string;
  action: URIAction;
}

// Flex message (most customizable)
interface FlexMessage {
  type: 'flex';
  altText: string;
  contents: FlexContainer;
}

interface FlexContainer {
  type: 'bubble' | 'carousel' | 'splash';
  styles?: FlexStyles;
  header?: FlexBox | FlexImage | FlexVideo;
  hero?: FlexBox | FlexImage | FlexVideo;
  body?: FlexBox;
  footer?: FlexBox;
}
```

### Flex Message Components

```typescript
// Box component
interface FlexBox {
  type: 'box';
  layout: 'horizontal' | 'vertical';
  contents: FlexComponent[];
  paddingAll?: string;
  paddingTop?: string;
  paddingBottom?: string;
  paddingStart?: string;
  paddingEnd?: string;
  background?: {
    type: 'linearGradient';
    angle: '0deg' | '90deg' | '180deg' | '270deg';
    endColor: string;
    startColor: string;
    centerColor?: string;
  } | string;
  width?: string;
  height?: string;
  flex?: number;
  spacing?: string;
  margin?: string;
  position: 'relative' | 'absolute';
  alignItems?: 'top' | 'bottom' | 'center' | 'start' | 'end';
  justifyContent?: 'center' | 'flex-start' | 'flex-end' | 'space-between';
  cornerRadius?: string;
}

// Text component
interface FlexText {
  type: 'text';
  text: string;
  align?: 'start' | 'center' | 'end' | 'left' | 'right';
  gravity?: 'top' | 'bottom' | 'center';
  size?: 'xxs' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'xxl' | '3xl' | '4xl' | '5xl';
  weight?: 'regular' | 'bold';
  color?: string;
  decoration?: 'none' | 'underline' | 'line-through';
  style?: 'normal' | 'italic';
  maxLines?: number;
  position?: 'relative' | 'absolute';
  offsetTop?: string;
  offsetBottom?: string;
  offsetStart?: string;
  offsetEnd?: string;
  lineSpacing?: string;
  wrap?: boolean;
  margin?: string;
}

// Image component
interface FlexImage {
  type: 'image';
  url: string;
  align?: 'center' | 'start' | 'end' | 'top' | 'bottom';
  gravity?: 'center' | 'top' | 'bottom';
  aspectMode?: 'cover' | 'fit';
  size?: 'xs' | 'sm' | 'md' 'lg' 'xl' 'xxl' '3xl' '4xl' '5xl' 'full';
  aspectRatio?: '1:1.51' | '1:1' | '20:13' | 'square' | 'rectangle';
  position?: 'relative' | 'absolute';
  offsetTop?: string;
  offsetBottom?: string;
  offsetStart?: string;
  offsetEnd?: string;
  margin?: string;
}

// Button component
interface FlexButton {
  type: 'button';
  action: URIAction;
  style?: 'primary' | 'secondary' 'link';
  color?: string;
  gravity?: 'top' | 'bottom' | 'center';
  margin?: string;
  height?: 'sm';
}

// Icon component
interface FlexIcon {
  type: 'icon';
  url: string;
  margin?: string;
  size: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'xxl' | '3xl' | '4xl' | '5xl';
  position?: 'relative' | 'absolute';
  offsetTop?: string;
  offsetBottom?: string;
  offsetStart?: string;
  offsetEnd?: string;
}

// Spacer component
interface FlexSpacer {
  type: 'spacer';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'xxl';
}

// Separator component
interface FlexSeparator {
  type: 'separator';
  margin?: string;
  color?: string;
}

type FlexComponent =
  | FlexBox
  | FlexText
  | FlexImage
  | FlexButton
  | FlexIcon
  | FlexSpacer
  | FlexSeparator;
```

### Quick Reply

```typescript
interface QuickReply {
  items: QuickReplyItem[];
}

interface QuickReplyItem {
  type: 'action';
  imageUrl?: string;
  action: QuickReplyAction;
}

type QuickReplyAction =
  | MessageAction
  | PostbackAction
  | URIAction
  | DatetimePickerAction
  | LocationAction
  | CameraAction
  | CameraRollAction;

interface MessageAction {
  type: 'message';
  label: string;
  text: string;
}

interface PostbackAction {
  type: 'postback';
  label: string;
  data: string;
  text?: string;
  displayText?: string;
}

interface URIAction {
  type: 'uri';
  label: string;
  uri: string;
  altUri?: UriAlternative;
}

interface UriAlternative {
  desktop: string;
}

interface DatetimePickerAction {
  type: 'datetimepicker';
  label: string;
  data: string;
  mode: 'date' | 'time' | 'datetime';
  initial?: string;
  max?: string;
  min?: string;
}

interface LocationAction {
  type: 'location';
  label: string;
}
```

---

# LINE Client Implementation

## Complete API Client

```typescript
const LINE_API_URL = 'https://api.line.me/v2/bot';

interface LineClient {
  reply(token: string, messages: Message[], notificationDisabled?: boolean): Promise<void>;
  push(userId: string, messages: Message[], notificationDisabled?: boolean): Promise<void>;
  multicast(to: string[], messages: Message[], notificationDisabled?: boolean): Promise<void>;
  broadcast(messages: Message[], notificationDisabled?: boolean): Promise<void>;
  narrowcast(messages: Message[], recipient: NarrowcastRecipient, notificationDisabled?: boolean): Promise<void>;
  getMessageContent(messageId: string): Promise<MessageContent>;
}

class LineMessagingApi implements LineClient {
  constructor(
    private accessToken: string,
    private options?: {
      timeout?: number;
      retries?: number;
    }
  ) {}

  private async api(endpoint: string, body: any): Promise<Response> {
    const maxRetries = this.options?.retries ?? 3;
    let lastError: Error | undefined;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.options?.timeout ?? 30000);

        const response = await fetch(`${LINE_API_URL}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.accessToken}`,
          },
          body: JSON.stringify(body),
          signal: controller.signal,
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          const error = await this.parseError(response);

          // Retry on rate limit (status 429)
          if (response.status === 429 && attempt < maxRetries - 1) {
            const retryAfter = error.headers['retry-after'];
            const waitTime = retryAfter ? parseInt(retryAfter) * 1000 : 1000;
            await this.sleep(waitTime);
            continue;
          }

          throw error;
        }

        return response;
      } catch (error) {
        lastError = error as Error;
        if (attempt < maxRetries - 1) {
          await this.sleep(1000 * (attempt + 1));
          continue;
        }
        throw lastError;
      }
    }

    throw lastError!;
  }

  private async parseError(response: Response): Promise<LineApiError> {
    const text = await response.text();
    try {
      return JSON.parse(text);
    } catch {
      return { message: text, statusCode: response.status };
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async reply(token: string, messages: Message[]): Promise<void> {
    await this.api('/message/reply', {
      replyToken: token,
      messages
    });
  }

  async push(userId: string, messages: Message[]): Promise<void> {
    await this.api('/message/push', {
      to: userId,
      messages
    });
  }

  async multicast(to: string[], messages: Message[]): Promise<void> {
    await this.api('/message/multicast', {
      to,
      messages
    });
  }

  async broadcast(messages: Message[]): Promise<void> {
    await this.api('/message/broadcast', { messages });
  }

  async narrowcast(
    messages: Message[],
    recipient: NarrowcastRecipient
  ): Promise<void> {
    await this.api('/message/narrowcast', {
      messages,
      recipient
    });
  }

  async getMessageContent(messageId: string): Promise<MessageContent> {
    const response = await fetch(`${LINE_API_URL}/message/${messageId}/content`, {
      headers: {
        'Authorization': `Bearer ${this.accessToken}`
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to get message content: ${response.statusText}`);
    }

    return response.json();
  }
}

// Type definitions for API responses
interface LineApiError {
  message: string;
  details?: { message: string; property: string }[];
  statusCode?: number;
}

interface NarrowcastRecipient {
  type?: 'audience' | 'redelivery' | 'operator';
  audienceGroupId?: number;
  redeliveryId?: string;
  to?: string[];
}

interface MessageContent {
  type: string;
  text?: string;
  [key: string]: any;
}
```

---

# Rich Menu Management

## Rich Menu Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Rich Menu (2500x1686px)                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│  │ Area 1  │ │ Area 2  │ │ Area 3  │ │ Area 4  │     │
│ │         │ │         │ │         │ │         │     │
│ │ Action  │ │ Action  │ │ Action  │ │ Action  │     │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│  │ Area 5  │ │ Area 6  │ │ Area 7  │ │ Area 8  │     │
│ │         │ │         │ │         │ │         │     │
│ │ Action  │ │ Action  │ │ Action  │ │ Action  │     │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Rich Menu Implementation

```typescript
// Rich menu types
interface RichMenu {
  richMenuId: string;
  size: {
    width: number;  // 2500 for default, 2500 for large
    height: number;  // 1686 for default, 2500 for large
  };
  selected: boolean;
  name: string;
  chatBarText: string;
  chatBarTextSize: 'default' | 'compact' | 'light';
  areas: RichMenuArea[];
}

interface RichMenuArea {
  bounds: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  action: RichMenuAction;
}

type RichMenuAction =
  | { type: 'postback'; data: string; label?: string; text?: string; displayText?: string; }
  | { type: 'message'; text: string; label?: string; }
  | { type: 'uri'; uri: string; label?: string; altUri?: { desktop: string }; }
  | { type: 'datetimepicker'; data: string; label?: string; mode: 'date' | 'time' | 'datetime'; initial?: string; max?: string; min?: string; }
  | { type: 'camera'; label?: string; }
  | { type: 'cameraRoll'; label?: string; }
  | { type: 'location'; label?: string; };

// Create rich menu
async function createRichMenu(client: LineMessagingApi): Promise<string> {
  const richMenu: RichMenu = {
    size: { width: 2500, height: 1686 },
    selected: false,
    name: 'Main Menu',
    chatBarText: 'เมนู',
    chatBarTextSize: 'compact',
    areas: [
      {
        bounds: { x: 0, y: 0, width: 833, height: 843 },
        action: {
          type: 'postback',
          data: 'action=profile',
          label: 'โปรไฟล์',
          text: 'โปรไฟล์ของฉัน'
        }
      },
      {
        bounds: { x: 833, y: 0, width: 834, height: 843 },
        action: {
          type: 'postback',
          data: 'action=orders',
          label: 'ออเดอร',
          text: 'ออเดอรคำสั่ง'
        }
      },
      {
        bounds: { x: 1667, y: 0, width: 833, height: 843 },
        action: {
          type: 'uri',
          uri: 'https://example.com',
          label: 'เว็บไซต์'
        }
      },
      {
        bounds: { x: 0, y: 843, width: 1250, height: 843 },
        action: {
          type: 'message',
          text: 'ติดต่อแอดมิน',
          label: 'ติดต่อแอดมิน'
        }
      },
      {
        bounds: { x: 1250, y: 843, width: 1250, height: 843 },
        action: {
          type: 'postback',
          data: 'action=help',
          label: 'ช่วยเหลือ',
          text: 'ช่วยเหลือ'
        }
      }
    ]
  };

  const response = await fetch(`${LINE_API_URL}/richmenu`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify(richMenu)
  });

  const data = await response.json();
  return data.richMenuId;
}

// Upload rich menu image
async function uploadRichMenuImage(
  richMenuId: string,
  imagePath: string
): Promise<void> {
  const form = new FormData();
  form.append('file', createReadStream(imagePath));

  await fetch(`${LINE_API_URL}/richmenu/${richMenuId}/content`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    },
    body: form
  });
}

// Set as default rich menu
async function setDefaultRichMenu(richMenuId: string): Promise<void> {
  await fetch(`${LINE_API_URL}/user/all/richmenu/${richMenuId}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
}

// Set rich menu for specific user
async function setUserRichMenu(
  userId: string,
  richMenuId: string
): Promise<void> {
  await fetch(`${LINE_API_URL}/user/${userId}/richmenu/${richMenuId}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
}

// Get user's rich menu
async function getUserRichMenu(userId: string): Promise<string | null> {
  const response = await fetch(`${LINE_API_URL}/user/${userId}/richmenu`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  if (response.status === 404) return null;
  const data = await response.json();
  return data.richMenuId;
}

// Unlink rich menu from user
async function unlinkUserRichMenu(userId: string): Promise<void> {
  await fetch(`${LINE_API_URL}/user/${userId}/richmenu`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
}

// Delete rich menu
async function deleteRichMenu(richMenuId: string): Promise<void> {
  await fetch(`${LINE_API_URL}/richmenu/${richMenuId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
}
```

---

# LINE Login Integration

## OAuth 2.0 Flow

```typescript
// Step 1: Generate login URL
function getLineLoginUrl(
  state: string,
  options?: {
    scope?: string;
    prompt?: string;
    botPrompt?: 'normal' | 'aggressive' | 'consent';
    nonce?: string;
  }
): string {
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
    redirect_uri: process.env.LINE_LOGIN_REDIRECT_URI!,
    state,
    scope: options?.scope || 'profile openid email',
    prompt: options?.prompt || 'consent',
    nonce: options?.nonce || crypto.randomUUID(),
    bot_prompt: options?.botPrompt
  });

  return `https://access.line.me/oauth2/v2.1/authorize?${params}`;
}

// Step 2: Exchange code for tokens
interface TokenResponse {
  access_token: string;
  token_type: string;
  refresh_token: string;
  expires_in: number;
  id_token: string;
}

async function exchangeCodeForTokens(code: string): Promise<TokenResponse> {
  const response = await fetch('https://api.line.me/oauth2/v2.1/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: process.env.LINE_LOGIN_REDIRECT_URI!,
      client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
      client_secret: process.env.LINE_LOGIN_CHANNEL_SECRET!
    })
  });

  return response.json();
}

// Step 3: Verify ID Token
interface DecodedIdToken {
  iss: string;
  sub: string;
  aud: string;
  exp: number;
  iat: number;
  nonce: string;
  amr: string[];
  name: string;
  picture?: string;
  email?: string;
}

function verifyIdToken(idToken: string, channelId: string): DecodedIdToken {
  // Decode JWT (use library like jose for production)
  const parts = idToken.split('.');
  const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());

  if (payload.iss !== 'https://access.line.me') {
    throw new Error('Invalid issuer');
  }

  if (payload.aud !== channelId) {
    throw new Error('Invalid audience');
  }

  if (payload.exp < Date.now() / 1000) {
    throw new Error('Token expired');
  }

  return payload;
}

// Step 4: Get user profile
async function getUserProfile(accessToken: string): Promise<LineUserProfile> {
  const response = await fetch('https://api.line.me/v2/profile', {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  return response.json();
}

interface LineUserProfile {
  userId: string;
  displayName: string;
  pictureUrl?: string;
  statusMessage?: string;
}

// Step 5: Refresh token
async function refreshAccessToken(refreshToken: string): Promise<TokenResponse> {
  const response = await fetch('https://api.line.me/oauth2/v2.1/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token,
      client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
      client_secret: process.env.LINE_LOGIN_CHANNEL_SECRET!
    })
  });

  return response.json();
}

// Logout
async function revokeToken(accessToken: string): Promise<void> {
  await fetch('https://api.line.me/oauth2/v2.1/revoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      access_token: accessToken,
      client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
      client_secret: process.env.LINE_LOGIN_CHANNEL_SECRET!
    })
  });
}
```

---

# LIFF (LINE Front-end Framework)

## LIFF v2 Implementation

```typescript
import { liff } from '@line/liff';

// Initialize LIFF
async function initLiff(liffId: string): Promise<void> {
  await liff.init({ liffId, withLoginOnExternalBrowser: true });

  if (liff.isLoggedIn()) {
    console.log('User is logged in');
  } else {
    // Login
    liff.login();
  }
}

// Get profile
function getProfile(): LineUserProfile {
  const profile = liff.getProfile();
  return {
    userId: profile.userId,
    displayName: profile.displayName,
    pictureUrl: profile.pictureUrl,
    statusMessage: profile.statusMessage
  };
}

// Get context (where LIFF is opened)
function getContext(): LiffContext {
  const context = liff.getContext();
  return {
    type: context.type,
    viewType: context.viewType,
    userId: context.userId,
    // Only available when opening from chat
    // For web: viewTpe: 'full', 'tall', or 'compact'
    // For chat: type: 'ut', userId: 'U123...'
  };
}

// Send message (only in chat context)
async function sendMessage(text: string): Promise<void> {
  if (liff.isApiAvailable('sendMessages')) {
    await liff.sendMessages([{ type: 'text', text }]);
  }
}

// Open URL
function openWindow(url: string, external: boolean = false): void {
  liff.openWindow({ url, external });
}

// Close LIFF app
function closeWindow(): void {
  liff.closeWindow();
}

// Get ID Token (for LINE Login integration)
function getIdToken(): string | null {
  return liff.getIDToken() || null;
}

// Get friendship status (for LINE OA)
async function getFriendship(): Promise<boolean> {
  const friendship = liff.getFriendship();
  return friendship.friendFlag;
}

// Scan QR code
async function scanCode(): Promise<string> {
  if (liff.isApiAvailable('scanCodeV2')) {
    const result = await liff.scanCodeV2();
    return result.value;
  }
  throw new Error('ScanCode not available');
}
```

## LIFF API Reference

```typescript
// Core methods
liff.init({ liffId, withLoginOnExternalBrowser })
liff.login()
liff.logout()
liff.isLoggedIn()
liff.getProfile()
liff.getContext()
liff.getVersion()

// Messaging
liff.sendMessages(messages)
liff.sendConfirmationMessage(messages)

// Navigation
liff.openWindow({ url, external })
liff.closeWindow()

// Data access
liff.getIDToken()
liff.getFriendship()
liff.getIsVideoCallAvailable()
liff_getIsInLiffApp()
liff.getIsInClient()

// Scanning
liff.scanCodeV2()

// Subscriptions
liff.unsubscribe(contextToken)
```

---

# Bot Patterns & Conversations

## Command Router

```typescript
interface Command {
  name: string;
  handler: (event: MessageEvent, args: string[]) => Promise<void>;
  description: string;
  adminOnly?: boolean;
}

const commands = new Map<string, Command>([
  {
    name: 'profile',
    description: 'ดูโปรไฟล์ของคุณ',
    handler: handleProfile
  },
  {
    name: 'help',
    description: 'แสดงคำสั่งทั้งหมด',
    handler: handleHelp
  },
  {
    name: 'register',
    description: 'ลงทะเบียน',
    handler: handleRegister
  },
  {
    name: 'admin_broadcast',
    description: 'ส่งข้อความถึงทุกคน',
    handler: handleBroadcast,
    adminOnly: true
  }
]);

async function handleCommand(event: MessageEvent): Promise<void> {
  if (event.message.type !== 'text') return;

  const text = event.message.text.trim();

  if (!text.startsWith('/')) {
    // Not a command, handle as regular message
    return handleRegularMessage(event);
  }

  const [commandName, ...args] = text.slice(1).split(' ');
  const command = commands.get(commandName.toLowerCase());

  if (!command) {
    await client.reply(event.replyToken, {
      type: 'text',
      text: `คำสั่งไม่ถูกต้อง "${commandName}"
    });
    return;
  }

  // Check admin permissions
  if (command.adminOnly) {
    const isAdmin = await checkAdmin(event.source.userId!);
    if (!isAdmin) {
      await client.reply(event.replyToken, {
        type: 'text',
        text: 'คำสั่งนี้สำหรับแอดมินเท่านั้น'
      });
      return;
    }
  }

  await command.handler(event, args);
}
```

## State Machine for Conversations

```typescript
// Conversation states
type ConversationState =
  | { name: 'idle' }
  | { name: 'awaiting_name'; step: number }
  | { name: 'awaiting_phone' }
  | { name: 'awaiting_email' }
  | { name: 'awaiting_confirmation'; data: RegistrationData };

interface RegistrationData {
  userId: string;
  name?: string;
  phone?: string;
  email?: string;
  address?: string;
}

// State storage (use Redis/Database in production)
const conversationStates = new Map<string, ConversationState>();

// State transitions
async function handleConversation(event: MessageEvent): Promise<void> {
  const userId = event.source.userId!;
  const state = conversationStates.get(userId) || { name: 'idle' };
  const text = event.message.text.trim();

  if (text.startsWith('/') || text === 'cancel' || text === 'ยกเลิก') {
    // Cancel conversation
    conversationStates.delete(userId);
    await client.reply(event.replyToken, {
      type: 'text',
      text: 'ยกเลิกการลงทะเบียน'
    });
    return;
  }

  switch (state.name) {
    case 'idle':
      // Start registration flow
      await client.reply(event.replyToken, {
        type: 'text',
        text: 'สวัสดีครับ/ค่ะ กรุณาใสชื่อของคุณ:'
      });
      conversationStates.set(userId, { name: 'awaiting_name', step: 1 });
      break;

    case 'awaiting_name':
      await client.reply(event.replyToken, {
        type: 'text',
        text: `กรุณาใสเบอร์โทรศัพท์ (เช่น: 0xx-xxx-xxxx):`
      });
      conversationStates.set(userId, {
        name: 'awaiting_phone',
        data: { userId, name: text }
      });
      break;

    case 'awaiting_phone':
      // Validate phone format
      if (!/^[0]\d{8,9}$/.test(text)) {
        await client.reply(event.replyToken, {
          type: 'text',
          text: 'รูปแบบเบอร์โทรศัพท์ไม่ถูก กรุณาใสใหม่:'
        });
        return;
      }

      await client.reply(event.replyToken, {
        type: 'text',
        text: 'กรุณาใสอีเมล (ตัวอย่าง: example@gmail.com):'
      });
      conversationStates.set(userId, {
        name: 'awaiting_email',
        data: { ...(state as any).data, phone: text }
      });
      break;

    case 'awaiting_email':
      // Validate email format
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text)) {
        await client.reply(event.replyToken, {
          type: 'text',
          text: 'รูปแบบอีเมลไม่ถูก กรุณาใสใหม่:'
        });
        return;
      }

      const data = (state as any).data;
      data.email = text;

      // Send confirmation
      await client.reply(event.replyToken, {
        type: 'template',
        altText: 'ยืนยันการลงทะเบียน',
        template: {
          type: 'confirm',
          text: `ยืนยันข้อมลงทะเบียน:\nชื่อ: ${data.name}\nเบอร์โทรศัพท์: ${data.phone}\nอีเมล: ${data.email}`,
          actions: [
            { type: 'message', label: 'ถูกต้อง', text: 'ยืนยัน' },
            { type: 'message', label: 'แก้ไข', text: 'แก้ไข' }
          ]
        }
      });

      conversationStates.set(userId, {
        name: 'awaiting_confirmation',
        data
      });
      break;

    case 'awaiting_confirmation':
      if (text === 'ยืนยัน') {
        await completeRegistration((state as any).data);
        conversationStates.set(userId, { name: 'idle' });
        await client.reply(event.replyToken, {
          type: 'text',
          text: 'ลงทะเบียนเรียบร้อยแล้ว ขอบคุณ!'
        });
      } else if (text === 'แก้ไข') {
        await client.reply(event.replyToken, {
          type: 'text',
          text: 'ยกเลิกการลงทะเบียน'
        });
        conversationStates.set(userId, { name: 'idle' });
      } else {
        await client.reply(event.replyToken, {
          type: 'text',
          text: 'ตอบ "ยืนยัน" หรือ "แก้ไข"'
        });
      }
      break;
  }
}
```

## Interactive Menu Handler

```typescript
// Handle postback events from rich menu and quick replies
async function handlePostback(event: PostbackEvent): Promise<void> {
  const params = new URLSearchParams(event.postback.data);
  const action = params.get('action');

  switch (action) {
    case 'profile':
      await handleProfileAction(event);
      break;

    case 'orders':
      await handleOrdersAction(event);
      break;

    case 'help':
      await handleHelpAction(event);
      break;

    case 'register':
      // Start registration flow
      await client.reply(event.replyToken, {
        type: 'text',
        text: 'กรุณาใสชื่อของคุณเพื่อเริ่มต้น:'
      });
      const userId = event.source.userId!;
      conversationStates.set(userId, { name: 'awaiting_name', step: 1 });
      break;

    default:
      // Handle unknown actions
      await client.reply(event.replyToken, {
        type: 'text',
        text: `Action: ${action}`
      });
  }
}

async function handleOrdersAction(event: PostbackEvent): Promise<void> {
  const userId = event.source.userId!;
  const orders = await getUserOrders(userId);

  if (orders.length === 0) {
    await client.reply(event.replyToken, {
      type: 'text',
      text: 'คุณยังไม่มีคำสั่ง'
    });
    return;
  }

  // Send order list as carousel
  const carouselColumns = orders.slice(0, 10).map(order => ({
    thumbnailImageUrl: order.productImage || 'https://via.placeholder.com/250x150',
    title: order.productName,
    text: `฿${order.price}\nสถานะ: ${order.status}`,
    actions: [
      {
        type: 'postback',
        label: 'ดูรายละเอียด',
        data: `action=order_detail&orderId=${order.id}`
      }
    ]
  }));

  await client.reply(event.replyToken, {
    type: 'template',
    altText: 'รายการสั่งซื้อของคุณ',
    template: {
      type: 'carousel',
      columns: carouselColumns
    }
  });
}
```

---

# LINE Official Account Features

## Broadcast Messages

```typescript
// Broadcast to all users
async function broadcastMessage(
  message: Message,
  notificationDisabled: boolean = false
): Promise<void> {
  await client.broadcast([message], notificationDisabled);
}

// Narrowcast to specific users
async function narrowcastMessage(
  users: string[],
  message: Message,
  conditions?: {
    gender?: 'male' | 'female';
    age?: { gte?: number; lte?: number };
    appType?: ['ios' | 'android'];
    region?: string[];
  }
): Promise<void> {
  const recipient: NarrowcastRecipient = {
    type: 'audience'
  };

  if (conditions) {
    // Create audience first
    const audienceId = await createAudience(conditions);
    recipient.audienceGroupId = audienceId;
  } else {
    recipient.to = users;
  }

  await client.narrowcast([message], recipient);
}

// Create audience for targeted messages
async function createAudience(conditions: any): Promise<number> {
  const response = await fetch(`${LINE_API_URL}/audienceGroup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'awaited `application/json`,
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      description: `Audience created at ${new Date().toISOString()}`,
      isIfaUsed: false,
      // Add conditions based on parameters
      conditions: [conditions]
    })
  });

  const data = await response.json();
  return data.audienceGroupId;
}
```

## Insights & Analytics

```typescript
// Get message delivery status
async function getMessageDeliveryStatus(messageId: string): Promise<number> {
  const response = await fetch(`${LINE_API_URL}/message/${messageId}/delivery/rc`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  const data = await response.json();
  return data.broadcast.progress;
}

// Get number of message deliveries
async function getDeliveryCount(messageId: string): Promise<number> {
  const response = await fetch(`${LINE_API_URL}/message/${messageId}/delivery/members/count`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  const data = await response.json();
  return data.numberOfMembers;
}

// Get engagement insights
async function getInsights(requestId: string): Promise<InsightData> {
  const response = await fetch(`${LINE_API_URL}/insight/${requestId}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  return response.json();
}

interface InsightData {
  numberOfMessages: number;
  numberOfClicks: number;
  numberOfImpressions: number;
  url?: string;
  // ... more fields
}
```

---

# Security Best Practices

## Webhook Security

```typescript
// Rate limiting middleware
import rateLimit from 'express-rate-limit';

const webhookLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute
  standardHeaders: true,
  message: 'Too many requests from this IP'
});

// IP whitelist
const allowedIPs = new Set(process.env.ALLOWED_IPS?.split(',') || []);

function ipWhitelist(
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
) {
  const ip = req.ip;
  if (allowedIPs.size > 0 && !allowedIPs.has(ip)) {
    return res.status(403).send('IP not allowed');
  }
  next();
}

// Input sanitization
function sanitizeInput(text: string): string {
  // Remove control characters except newlines
  return text.replace(/[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/g, '');
}

// Handle webhook redelivery
function isRedelivery(event: WebhookEvent): boolean {
  return event.deliveryContext?.isRedelivery ?? false;
}
```

## Data Protection

```typescript
// Mask sensitive data in logs
function maskUserId(userId: string): string {
  if (userId.length <= 4) return '****';
  return userId.substring(0, 2) + '****' + userId.substring(userId.length - 2);
}

// Mask phone number
function maskPhone(phone: string): string {
  if (phone.length < 10) return '********';
  return phone.substring(0, 3) + '****' + phone.substring(7);
}

// Mask email
function maskEmail(email: string): string {
  const [local, domain] = email.split('@');
  if (local.length <= 2) return '*@' + domain;
  return local.substring(0, 2) + '***@' + domain;
}
```

---

# Testing & Deployment

## Testing Strategies

```typescript
// Unit test for webhook handler
describe('Webhook Handler', () => {
  test('should handle follow event', async () => {
    const event: FollowEvent = {
      type: 'follow',
      mode: 'active',
      timestamp: Date.now(),
      source: { type: 'user', userId: 'U123' },
      replyToken: 'reply-token',
      webhookEventId: 'webhook-event-1'
    };

    await handleFollow(event);

    expect(sendMessage).toHaveBeenCalledWith({
      to: 'U123',
      messages: expect.arrayContaining([
        expect.objectContaining({
          type: 'text',
          text: expect.any(String)
        })
      ])
    });
  });
});

// Integration test for LIFF
describe('LIFF Integration', () => {
  beforeEach(async () => {
    await liff.init({ liffId: TEST_LIFF_ID });
  });

  test('should get user profile', () => {
    const profile = liff.getProfile();

    expect(profile).toBeDefined();
    expect(profile.userId).toBeDefined();
    expect(profile.displayName).toBeDefined();
  });
});
```

## Deployment Checklist

```
Pre-Deployment:
□ Test all webhook handlers
□ Verify rich menu functionality
□ Test LIFF in LINE app
□ Check rate limiting works
□ Verify webhook signature validation

Deployment:
□ Set up production database
□ Configure environment variables
□ Set up monitoring/logging
□ Deploy webhook server with HTTPS
□ Configure CI/CD pipeline

Post-Deployment:
□ Test webhook endpoint
□ Verify rich menu appears
□ Test message sending
□ Check logs for errors
□ Monitor webhook delivery rates
```

---

# World-Class Resources

## Official Documentation
- LINE Developers: https://developers.line.biz/
- Messaging API Docs: https://developers.line.biz/en/docs/messaging-api/
- LINE Login: https://developers.line.biz/en/docs/line-login/
- LIFF Documentation: https://developers.line.biz/en/docs/liff/
- API Reference: https://developers.line.biz/en/reference/
- Modules & Add-ons: https://developers.line.biz/en/docs/module-add-ons/

## SDKs
- LINE Bot SDK (Node.js): https://github.com/line/line-bot-sdk-nodejs
- @line/liff (TypeScript/JavaScript): https://github.com/line/liff-web
- LINE Bot SDK (Python): https://github.com/line/line-bot-sdk-python
- LINE Bot SDK (Java): https://github.com/line/line-bot-sdk-java
- LINE Bot SDK (PHP): https://github.com/line/line-bot-sdk-php
- LINE Bot SDK (Go): https://github.com/line/line-bot-sdk-go
- LINE Bot SDK (Ruby): https://github.com/line/line-bot-sdk-ruby
- LINE Bot SDK (C#): https://github.com/line/line-bot-sdk-csharp
- LINE Messaging API SDK for Python: https://github.com/line/line-messaging-api-sdk-python

## Community
- LINE Developers Community: https://www.line-community.me/
- LINE Developers Forum: https://developers.line.biz/en/community/
- LINE Developers X (formerly Twitter): @LINEDev
- LINE DevTalk (YouTube): https://www.youtube.com/@LINEDevTalk

## Tools & Resources
- LINE Developers Console: https://developers.line.biz/console/
- LINE Notify: https://notify-bot.line.me/
- LIFF Playground: https://developers.line.biz/console/liff/overview
- Webhook Tester: https://developers.line.biz/console/notify-api/test
- API Tester: https://developers.line.biz/console/api/tester
