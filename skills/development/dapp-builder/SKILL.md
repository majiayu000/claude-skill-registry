---
name: shelby-dapp-builder
description: Expert on building decentralized applications with Shelby Protocol storage on Aptos. Helps with dApp architecture, wallet integration (Petra), browser SDK usage, React/Vue integration, file uploads, content delivery, and building Shelby-powered applications. Triggers on keywords Shelby dApp, build on Shelby, Shelby application, Petra wallet, browser storage, web3 app, decentralized app Shelby, React Shelby, Vue Shelby.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Shelby DApp Builder

## Purpose

Guide developers in building decentralized applications (dApps) that leverage Shelby Protocol for storage. Covers wallet integration, browser SDK usage, frontend frameworks (React, Vue), user authentication, and complete dApp architecture patterns.

## When to Use

Auto-invoke when users ask about:
- **DApp Development** - Build Shelby app, create dApp, web3 application
- **Browser Integration** - Browser SDK, client-side uploads, web app
- **Wallet Integration** - Petra wallet, Aptos wallet, authentication
- **Frontend Frameworks** - React Shelby, Vue Shelby, Next.js integration
- **User Experience** - File uploads, download flows, progress tracking
- **Architecture** - DApp architecture, frontend/backend split, design patterns

## Knowledge Base

DApp development documentation:
```
.claude/skills/blockchain/aptos/docs/
```

Key files:
- `sdks_typescript_browser.md` - Browser SDK overview
- `sdks_typescript_browser_guides_upload.md` - Upload workflows
- `tools_wallets_petra-setup.md` - Wallet integration
- `sdks_typescript_acquire-api-keys.md` - API key setup
- `protocol.md` - Protocol fundamentals

## Core DApp Architecture

### Three-Layer Pattern

```
┌─────────────────────────────────────────────┐
│         Frontend (Browser)                  │
│  - React/Vue/vanilla JS                     │
│  - Shelby Browser SDK                       │
│  - Wallet integration (Petra)               │
│  - User interface                           │
└──────────────────┬──────────────────────────┘
                   │ HTTPS
                   ↓
┌─────────────────────────────────────────────┐
│         Shelby RPC Servers                  │
│  - Blob storage/retrieval                   │
│  - Erasure coding                           │
│  - Payment processing                       │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────┐
│         Aptos Blockchain                    │
│  - Smart contracts                          │
│  - Wallet accounts                          │
│  - State coordination                       │
└─────────────────────────────────────────────┘
```

### Key Components

**1. Wallet Integration**
- User authentication via Petra wallet
- Transaction signing
- Account management
- Balance checking

**2. Shelby Browser SDK**
- File uploads from browser
- Blob downloads
- Session management
- Progress tracking

**3. Frontend Framework**
- React, Vue, or vanilla JavaScript
- File upload UI
- Content gallery
- User feedback

## Wallet Integration (Petra)

### Setup

**Install Petra Wallet:**
```
Chrome Extension: https://petra.app/
```

**Detect Wallet:**
```typescript
// Check if Petra is installed
const isPetraInstalled = 'aptos' in window;

if (!isPetraInstalled) {
  alert('Please install Petra Wallet');
  window.open('https://petra.app/', '_blank');
}
```

### Connect Wallet

```typescript
import { Network } from '@aptos-labs/ts-sdk';

class WalletManager {
  async connect(): Promise<string> {
    try {
      // Request wallet connection
      const response = await window.aptos.connect();

      // Get account address
      const account = await window.aptos.account();

      console.log('Connected:', account.address);
      return account.address;
    } catch (error) {
      console.error('Wallet connection failed:', error);
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    await window.aptos.disconnect();
  }

  async getAccount(): Promise<any> {
    const account = await window.aptos.account();
    return account;
  }

  async getNetwork(): Promise<string> {
    const network = await window.aptos.network();
    return network;
  }

  async signAndSubmitTransaction(payload: any): Promise<any> {
    const response = await window.aptos.signAndSubmitTransaction(payload);
    return response;
  }
}

export const walletManager = new WalletManager();
```

### Check Balance

```typescript
async function checkBalance(address: string): Promise<any> {
  const response = await fetch(
    `https://api.shelbynet.shelby.xyz/v1/accounts/${address}/resources`
  );

  const resources = await response.json();

  // Find APT and ShelbyUSD balances
  const aptCoin = resources.find(
    r => r.type === '0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>'
  );

  const shelbyUSD = resources.find(
    r => r.type.includes('ShelbyUSD')
  );

  return {
    apt: aptCoin?.data?.coin?.value || '0',
    shelbyUSD: shelbyUSD?.data?.coin?.value || '0'
  };
}
```

## Browser SDK Integration

### Installation

```bash
npm install @shelby-protocol/sdk @aptos-labs/ts-sdk
```

### Initialize SDK

```typescript
import { ShelbyClient } from '@shelby-protocol/sdk/browser';
import { Network, Account, Ed25519PrivateKey } from '@aptos-labs/ts-sdk';

class ShelbyService {
  private client: ShelbyClient;
  private account: Account;

  async initialize(walletAddress: string): Promise<void> {
    // For wallet-based signing, use wallet provider
    // For API key usage (server-side), create account differently

    this.client = new ShelbyClient({
      network: Network.SHELBYNET,
      apiKey: process.env.NEXT_PUBLIC_SHELBY_API_KEY // Optional
    });
  }

  getClient(): ShelbyClient {
    return this.client;
  }
}

export const shelbyService = new ShelbyService();
```

### File Upload from Browser

```typescript
class FileUploader {
  async uploadFile(
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<string> {
    // Read file as ArrayBuffer
    const arrayBuffer = await file.arrayBuffer();
    const data = new Uint8Array(arrayBuffer);

    // Generate blob name
    const blobName = `uploads/${Date.now()}-${file.name}`;

    // Set expiration (30 days from now)
    const expirationTimestamp = Date.now() + 30 * 24 * 60 * 60 * 1000;

    // Upload to Shelby
    await shelbyService.getClient().uploadBlob({
      blobName,
      data,
      expirationTimestamp,
      onProgress: (progressEvent) => {
        const percentage = (progressEvent.loaded / progressEvent.total) * 100;
        onProgress?.(percentage);
      }
    });

    return blobName;
  }

  async uploadMultiple(
    files: FileList,
    onProgress?: (file: string, progress: number) => void
  ): Promise<string[]> {
    const uploads = Array.from(files).map(async (file) => {
      const blobName = await this.uploadFile(file, (progress) => {
        onProgress?.(file.name, progress);
      });
      return blobName;
    });

    return await Promise.all(uploads);
  }
}

export const fileUploader = new FileUploader();
```

### Download Blob

```typescript
async function downloadBlob(blobName: string, account: string): Promise<Blob> {
  const data = await shelbyService.getClient().getBlob(blobName);

  // Convert to Blob for browser download
  return new Blob([data]);
}

async function downloadAndSave(blobName: string, account: string, filename: string) {
  const blob = await downloadBlob(blobName, account);

  // Create download link
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

## React Integration

### Upload Component

```typescript
import React, { useState } from 'react';
import { fileUploader } from './shelby-service';

export function FileUploadComponent() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [blobName, setBlobName] = useState<string | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setProgress(0);

    try {
      const result = await fileUploader.uploadFile(
        selectedFile,
        (percentage) => {
          setProgress(percentage);
        }
      );

      setBlobName(result);
      alert('Upload successful!');
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-component">
      <h2>Upload to Shelby</h2>

      <input
        type="file"
        onChange={handleFileSelect}
        disabled={uploading}
      />

      {selectedFile && (
        <div className="file-info">
          <p>Selected: {selectedFile.name}</p>
          <p>Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!selectedFile || uploading}
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      {uploading && (
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          />
          <span>{progress.toFixed(1)}%</span>
        </div>
      )}

      {blobName && (
        <div className="success">
          <p>Blob Name: {blobName}</p>
          <p>Stored successfully on Shelby!</p>
        </div>
      )}
    </div>
  );
}
```

### Gallery Component

```typescript
import React, { useState, useEffect } from 'react';

interface BlobMetadata {
  name: string;
  size: number;
  expirationTimestamp: number;
  url: string;
}

export function BlobGalleryComponent({ account }: { account: string }) {
  const [blobs, setBlobs] = useState<BlobMetadata[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBlobs();
  }, [account]);

  const loadBlobs = async () => {
    try {
      // Query indexer or smart contract for user's blobs
      const response = await fetch(
        `https://api.shelbynet.shelby.xyz/indexer/v1/blobs/${account}`
      );

      const data = await response.json();

      const blobList = data.map((blob: any) => ({
        name: blob.name,
        size: blob.size,
        expirationTimestamp: blob.expiration,
        url: `https://api.shelbynet.shelby.xyz/shelby/v1/blobs/${account}/${blob.name}`
      }));

      setBlobs(blobList);
    } catch (error) {
      console.error('Failed to load blobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (blob: BlobMetadata) => {
    const filename = blob.name.split('/').pop() || 'download';
    await downloadAndSave(blob.name, account, filename);
  };

  if (loading) {
    return <div>Loading your blobs...</div>;
  }

  return (
    <div className="blob-gallery">
      <h2>Your Blobs</h2>

      {blobs.length === 0 ? (
        <p>No blobs found. Upload your first file!</p>
      ) : (
        <div className="blob-grid">
          {blobs.map((blob) => (
            <div key={blob.name} className="blob-card">
              <h3>{blob.name}</h3>
              <p>Size: {(blob.size / 1024 / 1024).toFixed(2)} MB</p>
              <p>
                Expires: {new Date(blob.expirationTimestamp).toLocaleDateString()}
              </p>

              {blob.name.match(/\.(jpg|jpeg|png|gif)$/i) && (
                <img src={blob.url} alt={blob.name} className="blob-preview" />
              )}

              <button onClick={() => handleDownload(blob)}>
                Download
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### Complete React App

```typescript
import React, { useState, useEffect } from 'react';
import { walletManager } from './wallet-manager';
import { shelbyService } from './shelby-service';
import { FileUploadComponent } from './FileUploadComponent';
import { BlobGalleryComponent } from './BlobGalleryComponent';

export function App() {
  const [connected, setConnected] = useState(false);
  const [account, setAccount] = useState<string | null>(null);
  const [balance, setBalance] = useState({ apt: '0', shelbyUSD: '0' });

  useEffect(() => {
    checkWalletConnection();
  }, []);

  const checkWalletConnection = async () => {
    try {
      const isConnected = await window.aptos?.isConnected();
      if (isConnected) {
        const account = await window.aptos.account();
        setAccount(account.address);
        setConnected(true);
        await loadBalance(account.address);
        await shelbyService.initialize(account.address);
      }
    } catch (error) {
      console.error('Failed to check wallet:', error);
    }
  };

  const handleConnect = async () => {
    try {
      const address = await walletManager.connect();
      setAccount(address);
      setConnected(true);
      await loadBalance(address);
      await shelbyService.initialize(address);
    } catch (error) {
      console.error('Connection failed:', error);
    }
  };

  const handleDisconnect = async () => {
    await walletManager.disconnect();
    setConnected(false);
    setAccount(null);
  };

  const loadBalance = async (address: string) => {
    const balances = await checkBalance(address);
    setBalance(balances);
  };

  return (
    <div className="app">
      <header>
        <h1>Shelby Storage DApp</h1>

        {!connected ? (
          <button onClick={handleConnect}>Connect Petra Wallet</button>
        ) : (
          <div className="wallet-info">
            <p>Account: {account?.slice(0, 6)}...{account?.slice(-4)}</p>
            <p>APT: {(parseInt(balance.apt) / 1e8).toFixed(4)}</p>
            <p>ShelbyUSD: {(parseInt(balance.shelbyUSD) / 1e8).toFixed(4)}</p>
            <button onClick={handleDisconnect}>Disconnect</button>
          </div>
        )}
      </header>

      {connected && account ? (
        <main>
          <FileUploadComponent />
          <BlobGalleryComponent account={account} />
        </main>
      ) : (
        <div className="connect-prompt">
          <p>Please connect your Petra wallet to use this app</p>
        </div>
      )}
    </div>
  );
}
```

## Vue Integration

### Upload Component (Vue 3)

```vue
<template>
  <div class="upload-component">
    <h2>Upload to Shelby</h2>

    <input
      type="file"
      @change="handleFileSelect"
      :disabled="uploading"
    />

    <div v-if="selectedFile" class="file-info">
      <p>Selected: {{ selectedFile.name }}</p>
      <p>Size: {{ fileSizeMB }} MB</p>
    </div>

    <button
      @click="handleUpload"
      :disabled="!selectedFile || uploading"
    >
      {{ uploading ? 'Uploading...' : 'Upload' }}
    </button>

    <div v-if="uploading" class="progress-bar">
      <div
        class="progress-fill"
        :style="{ width: `${progress}%` }"
      />
      <span>{{ progress.toFixed(1) }}%</span>
    </div>

    <div v-if="blobName" class="success">
      <p>Blob Name: {{ blobName }}</p>
      <p>Stored successfully on Shelby!</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { fileUploader } from './shelby-service';

const selectedFile = ref<File | null>(null);
const uploading = ref(false);
const progress = ref(0);
const blobName = ref<string | null>(null);

const fileSizeMB = computed(() => {
  if (!selectedFile.value) return 0;
  return (selectedFile.value.size / 1024 / 1024).toFixed(2);
});

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    selectedFile.value = file;
  }
};

const handleUpload = async () => {
  if (!selectedFile.value) return;

  uploading.value = true;
  progress.value = 0;

  try {
    const result = await fileUploader.uploadFile(
      selectedFile.value,
      (percentage) => {
        progress.value = percentage;
      }
    );

    blobName.value = result;
    alert('Upload successful!');
  } catch (error) {
    console.error('Upload failed:', error);
    alert('Upload failed: ' + error.message);
  } finally {
    uploading.value = false;
  }
};
</script>
```

## Complete DApp Examples

### Example 1: Decentralized Image Gallery

```typescript
// Image Gallery DApp
class ImageGalleryDApp {
  async uploadImage(imageFile: File, metadata: any) {
    // Resize/compress image if needed
    const optimized = await this.optimizeImage(imageFile);

    // Upload to Shelby
    const blobName = `gallery/${metadata.albumId}/${Date.now()}.jpg`;

    await shelbyService.getClient().uploadBlob({
      blobName,
      data: optimized,
      expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000
    });

    // Store metadata on-chain or in separate index
    await this.storeMetadata(blobName, metadata);

    return blobName;
  }

  async loadGallery(albumId: string): Promise<Image[]> {
    // Query blobs by prefix
    const images = await this.queryBlobs(`gallery/${albumId}/`);

    return images.map(blob => ({
      url: this.getBlobURL(blob.name),
      metadata: blob.metadata,
      thumbnail: this.getBlobURL(blob.name, { size: 'thumbnail' })
    }));
  }

  getBlobURL(blobName: string, options?: any): string {
    const baseUrl = `https://api.shelbynet.shelby.xyz/shelby/v1/blobs`;
    return `${baseUrl}/${this.account}/${blobName}`;
  }
}
```

### Example 2: Decentralized Video Platform

```typescript
// Video Streaming DApp
class VideoStreamingDApp {
  async uploadVideo(videoFile: File, metadata: any) {
    // Transcode to HLS format
    const hlsSegments = await this.transcodeToHLS(videoFile);

    // Upload each segment
    const videoId = Date.now().toString();
    const uploadPromises = hlsSegments.map(segment =>
      shelbyService.getClient().uploadBlob({
        blobName: `videos/${videoId}/${segment.name}`,
        data: segment.data,
        expirationTimestamp: Date.now() + 90 * 24 * 60 * 60 * 1000
      })
    );

    await Promise.all(uploadPromises);

    // Upload playlist manifest
    await this.uploadPlaylist(videoId, hlsSegments);

    // Store video metadata
    await this.storeVideoMetadata(videoId, metadata);

    return videoId;
  }

  getStreamURL(videoId: string): string {
    return `https://api.shelbynet.shelby.xyz/shelby/v1/blobs/${this.account}/videos/${videoId}/playlist.m3u8`;
  }
}
```

### Example 3: Decentralized File Sharing

```typescript
// File Sharing DApp
class FileSharingDApp {
  async shareFile(file: File, recipients: string[], expireDays: number) {
    // Upload file to Shelby
    const shareId = this.generateShareId();
    const blobName = `shares/${shareId}/${file.name}`;

    await shelbyService.getClient().uploadBlob({
      blobName,
      data: await file.arrayBuffer(),
      expirationTimestamp: Date.now() + expireDays * 24 * 60 * 60 * 1000
    });

    // Create shareable link
    const shareLink = `https://myapp.com/share/${shareId}`;

    // Store access control (on-chain or off-chain)
    await this.storeAccessControl(shareId, recipients);

    return shareLink;
  }

  async accessSharedFile(shareId: string, userAccount: string) {
    // Check access control
    const hasAccess = await this.checkAccess(shareId, userAccount);
    if (!hasAccess) {
      throw new Error('Access denied');
    }

    // Download file
    const metadata = await this.getShareMetadata(shareId);
    return await downloadBlob(metadata.blobName, metadata.owner);
  }
}
```

## Best Practices

### 1. User Experience

**Progress Feedback:**
```typescript
// Always show upload/download progress
const [progress, setProgress] = useState(0);

await uploadFile(file, (percent) => {
  setProgress(percent);
  // Update UI
});
```

**Error Handling:**
```typescript
try {
  await uploadFile(file);
} catch (error) {
  if (error.code === 'INSUFFICIENT_FUNDS') {
    alert('Please add ShelbyUSD to your wallet');
  } else if (error.code === 'FILE_TOO_LARGE') {
    alert('File size exceeds limit');
  } else {
    alert('Upload failed. Please try again.');
  }
}
```

**Loading States:**
```typescript
// Show loading indicators
const [loading, setLoading] = useState(false);

// Disable actions during operations
<button disabled={loading || uploading}>Upload</button>
```

### 2. Performance Optimization

**Image Optimization:**
```typescript
async function optimizeImage(file: File): Promise<Uint8Array> {
  return new Promise((resolve) => {
    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;

      // Resize if needed
      const maxWidth = 1920;
      const maxHeight = 1080;
      let { width, height } = img;

      if (width > maxWidth) {
        height = (height * maxWidth) / width;
        width = maxWidth;
      }

      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0, width, height);

      // Convert to blob with compression
      canvas.toBlob(
        (blob) => {
          blob!.arrayBuffer().then(buffer => {
            resolve(new Uint8Array(buffer));
          });
        },
        'image/jpeg',
        0.85 // Quality
      );
    };
  });
}
```

**Lazy Loading:**
```typescript
// Load blobs on-demand
const [visibleBlobs, setVisibleBlobs] = useState<string[]>([]);

useEffect(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Load blob when visible
        loadBlob(entry.target.dataset.blobName);
      }
    });
  });

  // Observe blob containers
}, []);
```

### 3. Security

**Wallet Integration:**
```typescript
// Always verify wallet connection
const isConnected = await window.aptos?.isConnected();
if (!isConnected) {
  throw new Error('Please connect wallet');
}

// Verify network
const network = await window.aptos.network();
if (network !== 'shelbynet') {
  alert('Please switch to Shelby Network');
}
```

**Input Validation:**
```typescript
// Validate file types
const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
if (!allowedTypes.includes(file.type)) {
  throw new Error('File type not supported');
}

// Validate file size
const maxSize = 100 * 1024 * 1024; // 100MB
if (file.size > maxSize) {
  throw new Error('File too large');
}
```

### 4. Cost Management

**Estimate Costs:**
```typescript
async function estimateUploadCost(fileSize: number, durationDays: number): Promise<number> {
  // Rough estimation based on size and duration
  const costPerMBPerDay = 0.001; // Example rate in ShelbyUSD
  const sizeMB = fileSize / (1024 * 1024);
  return sizeMB * durationDays * costPerMBPerDay;
}

// Show cost before upload
const cost = await estimateUploadCost(file.size, 30);
const confirmed = confirm(`This upload will cost ~${cost.toFixed(4)} ShelbyUSD. Continue?`);
```

## Process for Helping Users

### 1. Understand App Requirements

**Questions:**
- What type of dApp are you building?
- What files/data need storage?
- Who are your users?
- What's the user flow?
- Mobile or desktop (or both)?

### 2. Design Architecture

**Choose Pattern:**
- Pure client-side (browser SDK only)
- Hybrid (frontend + backend API)
- Server-side rendering with Shelby

**Plan Components:**
- Authentication/wallet
- Upload interface
- Download/display logic
- State management

### 3. Provide Implementation

**Show:**
- Complete code examples
- Component structure
- Integration patterns
- Best practices

### 4. Testing & Deployment

**Guide:**
- Local testing workflow
- Testnet deployment
- Production considerations
- Monitoring

## Response Style

- **Framework-aware** - Provide React, Vue, or vanilla JS examples
- **Complete** - Show full component implementations
- **User-focused** - Emphasize UX and user feedback
- **Practical** - Working code ready to adapt
- **Modern** - Use current best practices (hooks, composition API)

## Example Interaction

```
User: "How do I build a React app for uploading images to Shelby?"

Response:
1. Show wallet integration (Petra)
2. Provide complete React upload component
3. Show gallery/display component
4. Include image optimization
5. Add progress tracking and error handling
6. Suggest deployment strategy
7. Reference: sdks_typescript_browser_guides_upload.md
```

## Limitations

- Browser SDK has different constraints than Node.js
- Wallet-based signing differs from API key approach
- CORS considerations for direct API calls
- Be clear about testnet vs mainnet differences

## Follow-up Suggestions

- State management (Redux, Zustand)
- Mobile app development (React Native)
- PWA features (offline support)
- Testing strategies (Jest, Playwright)
- Performance monitoring
- User analytics
