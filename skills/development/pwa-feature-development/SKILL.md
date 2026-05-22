---
name: pwa-feature-development
description: Create progressive web app features following established patterns
version: 1.0.0
author: Saberloop Project
usage: |
  Use this skill for PWA feature development:
  - Implementing new views following BaseView patterns
  - Adding service worker functionality and caching strategies
  - Creating P2P features and WebRTC connections
  - Setting up offline capabilities and data sync
  - Implementing quiz sharing/import functionality
  
  Examples:
  "Create new results view using the pwa-feature-development skill"
  "Implement P2P quiz sharing using the pwa-feature-development skill"
  "Add service worker caching using the pwa-feature-development skill"

# PWA Feature Development Skill

## Overview

This skill automates the creation of progressive web app features following Saberloop's established patterns, including BaseView architecture, service worker strategies, WebRTC P2P functionality, and offline capabilities.

## PWA Architecture Overview

### Core Components

| Component | Purpose | Key Files |
|------------|---------|-------------|
| View Layer | UI screens and navigation | `src/views/*.js` |
| Service Worker | Offline caching, background sync | `public/sw.js`, `vite.config.js` |
| P2P Layer | Real-time connections | `src/services/p2p-service.js` |
| State Management | App-wide state | `src/core/state.js` |
| Database | Offline storage | `src/core/db.js` |

### Data Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     View      │◀──▶│     State      │◀──▶│    Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Service Worker │◀──▶│   P2P Service  │◀──▶│   API Layer     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
   Network/Cache             WebRTC              External APIs
```

## When to Use This Skill

Use this skill when ANY of these are true:
- [ ] Creating new views or screens
- [ ] Adding P2P or real-time features
- [ ] Implementing offline functionality
- [ ] Setting up service worker caching
- [ ] Creating sharing/import features
- [ ] Adding WebRTC capabilities
- [ ] Implementing background sync

## BaseView Pattern Implementation

### Step 1: Create New View

#### View Template

```javascript
// src/views/NewFeatureView.js
import BaseView from './BaseView.js';
import { state } from '@/core/state.js';
import { logger } from '@/utils/logger.js';
import { t } from '@/core/i18n.js';

export default class NewFeatureView extends BaseView {
  constructor() {
    super();
    this.featureData = null;
    this.isLoading = false;
    this.error = null;
  }

  /**
   * Render the view
   */
  render() {
    if (this.isLoading) {
      return this.renderLoading();
    }

    if (this.error) {
      return this.renderError();
    }

    return this.renderContent();
  }

  /**
   * Render loading state
   */
  renderLoading() {
    this.setHTML(`
      <div class="flex min-h-screen items-center justify-center bg-background-light dark:bg-background-dark">
        <div class="text-center">
          <span class="material-symbols-outlined text-5xl text-primary animate-spin">progress_activity</span>
          <p class="mt-4 text-lg font-medium text-text-light dark:text-text-dark">
            ${t('newFeature.loading')}
          </p>
        </div>
      </div>
    `);
  }

  /**
   * Render error state
   */
  renderError() {
    this.setHTML(`
      <div class="flex min-h-screen items-center justify-center bg-background-light dark:bg-background-dark">
        <div class="text-center max-w-sm">
          <span class="material-symbols-outlined text-5xl text-red-500">error</span>
          <p class="mt-4 text-lg font-medium text-text-light dark:text-text-dark">
            ${t('newFeature.error')}
          </p>
          <p class="mt-2 text-sm text-subtext-light dark:text-subtext-dark">
            ${this.error}
          </p>
          <button onclick="window.location.hash = '#/home'" class="mt-6 px-6 py-3 bg-primary text-white rounded-xl font-medium hover:bg-primary/90">
            ${t('common.goHome')}
          </button>
        </div>
      </div>
    `);
  }

  /**
   * Render main content
   */
  renderContent() {
    this.setHTML(`
      <div class="min-h-screen bg-background-light dark:bg-background-dark">
        <header class="bg-white dark:bg-gray-800 shadow-sm">
          <div class="max-w-4xl mx-auto px-4 py-4">
            <h1 class="text-2xl font-bold text-text-light dark:text-text-dark">
              ${t('newFeature.title')}
            </h1>
          </div>
        </header>
        
        <main class="max-w-4xl mx-auto px-4 py-8">
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <p class="text-text-light dark:text-text-dark">
              ${t('newFeature.description')}
            </p>
            
            <div class="mt-6">
              <button 
                onclick="window.newFeatureView.handleAction()"
                class="px-6 py-3 bg-primary text-white rounded-xl font-medium hover:bg-primary/90"
              >
                ${t('newFeature.action')}
              </button>
            </div>
          </div>
        </main>
      </div>
    `);

    this.setupEventListeners();
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Add any interactive elements
    const actionButton = this.querySelector('button[onclick*="handleAction"]');
    if (actionButton) {
      this.addEventListener(actionButton, 'click', () => this.handleAction());
    }
  }

  /**
   * Handle main action
   */
  async handleAction() {
    try {
      this.isLoading = true;
      this.render();
      
      logger.info('New feature action started');
      
      // Perform the main action
      await this.performAction();
      
      // Navigate to next view
      this.navigateTo('#/results');
      
    } catch (error) {
      logger.error('New feature action failed', { error: error.message });
      this.error = error.message;
      this.isLoading = false;
      this.render();
    }
  }

  /**
   * Perform the main feature logic
   */
  async performAction() {
    // Implement the feature logic here
    this.featureData = await this.processFeatureData();
    
    // Save to state if needed
    state.set('newFeatureData', this.featureData);
    
    // Save to database if needed
    // await saveFeatureData(this.featureData);
    
    return this.featureData;
  }

  /**
   * Process feature data
   */
  async processFeatureData() {
    // Implement data processing logic
    return {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      data: 'processed data'
    };
  }

  /**
   * Cleanup method
   */
  destroy() {
    // Remove event listeners and cleanup
    super.destroy();
    
    // Clear any intervals/timeouts
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }
    
    logger.info('NewFeatureView destroyed');
  }
}
```

### Step 2: Register Route

```javascript
// In src/main.js
import NewFeatureView from './views/NewFeatureView.js';

// Add to router initialization
router.addRoute('/new-feature', NewFeatureView);

// Or for dynamic routes
router.addRoute('/new-feature/:id', NewFeatureView);
```

## Service Worker Patterns

### Step 1: Update Service Worker Configuration

#### Caching Strategy Template

```javascript
// In vite.config.js - PWA plugin section
workbox: {
  globPatterns: ['**/*.{js,css,html,ico,png,svg,json}'],

  runtimeCaching: [
    // API calls (Network First)
    {
      urlPattern: /^https:\/\/.*\.saberloop\.com\/api\/.*/,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'api-cache',
        expiration: {
          maxEntries: 50,
          maxAgeSeconds: 5 * 60 // 5 minutes
        },
        cacheableResponse: {
          statuses: [0, 200]
        }
      }
    },

    // Static assets (Cache First)
    {
      urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
      handler: 'CacheFirst',
      options: {
        cacheName: 'images-cache',
        expiration: {
          maxEntries: 100,
          maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
        }
      }
    },

    // HTML pages (Stale While Revalidate)
    {
      urlPattern: /\.(?:html)$/,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'html-cache',
        expiration: {
          maxEntries: 20,
          maxAgeSeconds: 24 * 60 * 60 // 24 hours
        }
      }
    }
  ],

  cleanupOutdatedCaches: true,
  navigateFallback: '/index.html',
  navigateFallbackDenylist: [/^\/api/]
}
```

### Step 2: Background Sync

```javascript
// In public/sw.js (if custom service worker needed)
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  try {
    // Get pending data from IndexedDB
    const pendingData = await getPendingSyncData();
    
    if (pendingData.length > 0) {
      // Sync with server
      for (const data of pendingData) {
        await syncDataToServer(data);
      }
      
      // Clear pending data
      await clearPendingSyncData();
      
      // Notify user
      self.registration.showNotification('Data synced successfully');
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}
```

## P2P WebRTC Implementation

### Step 1: P2P Service Structure

```javascript
// src/services/p2p-service.js
import { logger } from '@/utils/logger.js';

export class P2PService {
  constructor() {
    this.localConnection = null;
    this.remoteConnections = new Map();
    this.roomId = null;
    this.isHost = false;
    this.onMessageCallback = null;
    this.onConnectionCallback = null;
  }

  /**
   * Create or join a room
   */
  async createRoom(roomId) {
    this.roomId = roomId;
    this.isHost = true;
    
    try {
      // Create peer connection
      this.localConnection = new RTCPeerConnection({
        iceServers: this.getIceServers()
      });

      // Setup connection handlers
      this.setupConnectionHandlers();

      // Create data channel for messaging
      this.dataChannel = this.localConnection.createDataChannel('quiz-channel', {
        ordered: true,
        reliable: true
      });

      this.setupDataChannelHandlers();

      logger.info('P2P room created', { roomId, isHost: true });

    } catch (error) {
      logger.error('Failed to create P2P room', { roomId, error });
      throw error;
    }
  }

  /**
   * Join an existing room
   */
  async joinRoom(roomId, signalingUrl) {
    this.roomId = roomId;
    this.isHost = false;

    try {
      // Connect to signaling server
      await this.connectToSignalingServer(signalingUrl);

      // Join room
      await this.signaling.emit('join-room', { roomId });

      logger.info('P2P room joined', { roomId, isHost: false });

    } catch (error) {
      logger.error('Failed to join P2P room', { roomId, error });
      throw error;
    }
  }

  /**
   * Setup ICE servers
   */
  getIceServers() {
    return [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' }
    ];
  }

  /**
   * Setup connection event handlers
   */
  setupConnectionHandlers() {
    this.localConnection.onicecandidate = (event) => {
      if (event.candidate) {
        this.sendSignalingMessage('ice-candidate', {
          candidate: event.candidate
        });
      }
    };

    this.localConnection.onconnectionstatechange = (event) => {
      logger.info('P2P connection state changed', { 
        state: event.target.connectionState 
      });
      
      if (this.onConnectionCallback) {
        this.onConnectionCallback(event.target.connectionState);
      }
    };
  }

  /**
   * Setup data channel handlers
   */
  setupDataChannelHandlers() {
    this.dataChannel.onopen = () => {
      logger.info('P2P data channel opened');
    };

    this.dataChannel.onmessage = (event) => {
      const message = JSON.parse(event.data);
      logger.debug('P2P message received', { message });
      
      if (this.onMessageCallback) {
        this.onMessageCallback(message);
      }
    };

    this.dataChannel.onclose = () => {
      logger.info('P2P data channel closed');
    };
  }

  /**
   * Send message to peer
   */
  sendMessage(type, data) {
    if (this.dataChannel && this.dataChannel.readyState === 'open') {
      const message = JSON.stringify({
        type,
        data,
        timestamp: Date.now()
      });
      
      this.dataChannel.send(message);
      logger.debug('P2P message sent', { type, data });
    } else {
      logger.warn('P2P data channel not ready');
    }
  }

  /**
   * Handle quiz-specific messages
   */
  sendQuizStart(quizData) {
    this.sendMessage('quiz-start', quizData);
  }

  sendQuizAnswer(questionIndex, answerIndex) {
    this.sendMessage('quiz-answer', {
      questionIndex,
      answerIndex
    });
  }

  sendQuizComplete(results) {
    this.sendMessage('quiz-complete', results);
  }

  /**
   * Set event callbacks
   */
  onMessage(callback) {
    this.onMessageCallback = callback;
  }

  onConnection(callback) {
    this.onConnectionCallback = callback;
  }

  /**
   * Cleanup P2P connection
   */
  destroy() {
    if (this.dataChannel) {
      this.dataChannel.close();
    }
    
    if (this.localConnection) {
      this.localConnection.close();
    }
    
    this.remoteConnections.clear();
    
    logger.info('P2P service destroyed');
  }
}
```

### Step 2: Quiz Sharing Implementation

```javascript
// src/services/quiz-share.js
import { p2pService } from './p2p-service.js';
import { logger } from '@/utils/logger.js';

export class QuizShareService {
  constructor() {
    this.p2pService = new P2PService();
    this.quizData = null;
    this.participants = new Map();
  }

  /**
   * Host a shared quiz session
   */
  async hostSharedQuiz(quizData) {
    try {
      this.quizData = quizData;
      
      // Generate room ID
      const roomId = this.generateRoomId();
      
      // Create P2P room
      await this.p2pService.createRoom(roomId);
      
      // Setup message handlers
      this.p2pService.onMessage((message) => {
        this.handleParticipantMessage(message);
      });

      // Notify when participants join
      this.p2pService.onConnection((state) => {
        logger.info('Participant connection state', { state });
        
        if (state === 'connected') {
          this.handleParticipantJoin();
        }
      });

      // Share room code with participants
      const shareUrl = this.generateShareUrl(roomId);
      
      logger.info('Quiz sharing session started', { 
        roomId, 
        shareUrl,
        quizTitle: quizData.title 
      });

      return {
        roomId,
        shareUrl,
        qrCode: this.generateQRCode(shareUrl)
      };

    } catch (error) {
      logger.error('Failed to host shared quiz', { error });
      throw error;
    }
  }

  /**
   * Join a shared quiz session
   */
  async joinSharedQuiz(roomCode) {
    try {
      // Join P2P room
      await this.p2pService.joinRoom(roomCode);
      
      // Setup message handlers
      this.p2pService.onMessage((message) => {
        this.handleHostMessage(message);
      });

      // Request quiz data
      this.p2pService.sendMessage('quiz-request', {
        participantId: this.generateParticipantId()
      });

      logger.info('Joined shared quiz session', { roomCode });

    } catch (error) {
      logger.error('Failed to join shared quiz', { error });
      throw error;
    }
  }

  /**
   * Handle participant messages
   */
  handleParticipantMessage(message) {
    switch (message.type) {
      case 'quiz-request':
        this.handleQuizRequest(message.data);
        break;
        
      case 'quiz-answer':
        this.handleQuizAnswer(message.data);
        break;
        
      case 'quiz-complete':
        this.handleQuizComplete(message.data);
        break;
    }
  }

  /**
   * Handle host messages
   */
  handleHostMessage(message) {
    switch (message.type) {
      case 'quiz-start':
        this.handleQuizStart(message.data);
        break;
        
      case 'quiz-question':
        this.handleQuizQuestion(message.data);
        break;
        
      case 'quiz-results':
        this.handleQuizResults(message.data);
        break;
    }
  }

  /**
   * Generate shareable room code
   */
  generateRoomId() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 6; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  /**
   * Generate share URL
   */
  generateShareUrl(roomId) {
    const baseUrl = window.location.origin + '/app/';
    return `${baseUrl}#/join/${roomId}`;
  }

  /**
   * Generate QR code for mobile sharing
   */
  generateQRCode(url) {
    // Use qrcode library
    import QRCode from 'qrcode';
    
    return QRCode.toDataURL(url, {
      width: 200,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    });
  }
}
```

## Offline Functionality

### Step 1: Offline Detection

```javascript
// src/utils/network.js
import { logger } from './logger.js';
import { state } from '@/core/state.js';

export class NetworkManager {
  constructor() {
    this.isOnline = navigator.onLine;
    this.listeners = [];
    
    // Setup network listeners
    window.addEventListener('online', this.handleOnline.bind(this));
    window.addEventListener('offline', this.handleOffline.bind(this));
  }

  handleOnline() {
    this.isOnline = true;
    state.set('networkStatus', 'online');
    logger.info('Network connection restored');
    
    // Trigger background sync
    this.triggerBackgroundSync();
    
    // Notify listeners
    this.listeners.forEach(callback => callback('online'));
  }

  handleOffline() {
    this.isOnline = false;
    state.set('networkStatus', 'offline');
    logger.warn('Network connection lost');
    
    // Notify listeners
    this.listeners.forEach(callback => callback('offline'));
  }

  onNetworkChange(callback) {
    this.listeners.push(callback);
  }

  async triggerBackgroundSync() {
    if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
      const registration = await navigator.serviceWorker.ready;
      registration.sync.register('background-sync');
    }
  }
}
```

### Step 2: Offline Data Management

```javascript
// src/utils/offline-sync.js
import { getDatabase } from '@/core/db.js';

export class OfflineSync {
  constructor() {
    this.db = null;
  }

  async init() {
    this.db = await getDatabase();
  }

  /**
   * Queue action for offline sync
   */
  async queueAction(type, data) {
    const action = {
      id: Date.now().toString(),
      type,
      data,
      timestamp: new Date().toISOString(),
      synced: false
    };

    await this.db.add('syncQueue', action);
    logger.info('Action queued for sync', { type, actionId: action.id });
  }

  /**
   * Process queued actions when online
   */
  async processQueue() {
    const actions = await this.db.getAll('syncQueue');
    const unsynced = actions.filter(action => !action.synced);

    for (const action of unsynced) {
      try {
        await this.processAction(action);
        
        // Mark as synced
        action.synced = true;
        await this.db.put('syncQueue', action);
        
        logger.info('Action synced successfully', { 
          type: action.type, 
          actionId: action.id 
        });
        
      } catch (error) {
        logger.error('Failed to sync action', { 
          type: action.type, 
          actionId: action.id, 
          error 
        });
      }
    }
  }

  /**
   * Process individual action
   */
  async processAction(action) {
    switch (action.type) {
      case 'quiz-result':
        return await this.syncQuizResult(action.data);
        
      case 'quiz-progress':
        return await this.syncQuizProgress(action.data);
        
      case 'user-preferences':
        return await this.syncUserPreferences(action.data);
        
      default:
        throw new Error(`Unknown sync action type: ${action.type}`);
    }
  }

  /**
   * Sync quiz results to server
   */
  async syncQuizResult(data) {
    const response = await fetch('/api/quiz-results', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`Failed to sync quiz result: ${response.status}`);
    }

    return await response.json();
  }
}
```

## Integration and Testing

### Step 1: Feature Integration

```javascript
// In src/main.js or appropriate view
import { quizShareService } from '@/services/quiz-share.js';
import { networkManager } from '@/utils/network.js';

// Initialize P2P service
const shareService = new QuizShareService();

// Setup network monitoring
networkManager.onNetworkChange((status) => {
  if (status === 'online') {
    shareService.syncPendingActions();
  }
});
```

### Step 2: PWA Testing

#### Service Worker Testing

```javascript
// tests/service-worker.test.js
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

// Mock service worker environment
global.self = {
  addEventListener: vi.fn(),
  registration: {
    sync: vi.fn(),
    showNotification: vi.fn()
  }
};

describe('Service Worker', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should cache static assets', async () => {
    // Test caching strategy
    const cache = await caches.open('static-cache');
    expect(cache.addAll).toHaveBeenCalled();
  });

  it('should handle background sync', async () => {
    const syncEvent = { tag: 'background-sync', waitUntil: vi.fn() };
    
    // Trigger sync event
    global.self.addEventListener.mock.calls[0][1](syncEvent);
    
    expect(syncEvent.waitUntil).toHaveBeenCalled();
  });
});
```

#### P2P Testing

```javascript
// tests/p2p-service.test.js
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { P2PService } from '@/services/p2p-service.js';

// Mock WebRTC
global.RTCPeerConnection = vi.fn().mockImplementation(() => ({
  createDataChannel: vi.fn().mockReturnValue({
    send: vi.fn(),
    close: vi.fn()
  }),
  onicecandidate: null,
  onconnectionstatechange: null
}));

describe('P2P Service', () => {
  let p2pService;

  beforeEach(() => {
    p2pService = new P2PService();
  });

  it('should create room with correct configuration', async () => {
    await p2pService.createRoom('TEST123');
    
    expect(global.RTCPeerConnection).toHaveBeenCalledWith({
      iceServers: expect.arrayContaining([
        expect.objectContaining({ urls: 'stun:stun.l.google.com:19302' })
      ])
    });
  });

  it('should handle message sending', () => {
    const mockDataChannel = {
      readyState: 'open',
      send: vi.fn()
    };
    
    p2pService.dataChannel = mockDataChannel;
    p2pService.sendMessage('test-type', { data: 'test' });
    
    expect(mockDataChannel.send).toHaveBeenCalledWith(
      expect.stringContaining('"type":"test-type"')
    );
  });
});
```

## Quality Assurance

### PWA Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| Service Worker registered | ✅ | Caching strategy configured |
| Offline functionality | ✅ | Network detection and sync |
| P2P connections | ✅ | WebRTC implementation |
| Responsive design | ✅ | Mobile-optimized UI |
| Background sync | ✅ | Queued actions processing |
| Share functionality | ✅ | URL and QR code sharing |

### Performance Metrics

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| First Contentful Paint | <2s | Lighthouse audit |
| Service Worker Registration | <500ms | Performance monitoring |
| P2P Connection Time | <5s | Connection analytics |
| Cache Hit Rate | >80% | Service worker analytics |
| Offline Queue Processing | <30s | Sync performance |

## Integration with Other Skills

This skill integrates with:
- **epic-hygiene-process** - For PWA code quality improvements
- **testing-suite-management** - For comprehensive PWA testing
- **architecture-compliance** - For validating PWA layer structure
- **feature-flag-management** - For gradual PWA feature rollout

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**Compatible with:** Saberloop v2.0.0+