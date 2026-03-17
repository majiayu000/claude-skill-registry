---
name: react-native-privacy
description: Implement privacy and security patterns for React Native apps handling sensitive data (health, recovery, PII). Use when adding biometric authentication, securing sensitive data, implementing app locks, handling HIPAA considerations, or adding privacy controls like data export/deletion.
---

# React Native Privacy & Security

Privacy-first patterns for sensitive data handling in React Native apps.

## Biometric Authentication

### Setup (expo-local-authentication)

```typescript
import * as LocalAuthentication from 'expo-local-authentication';

async function authenticateWithBiometrics(): Promise<boolean> {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  if (!hasHardware) return false;

  const isEnrolled = await LocalAuthentication.isEnrolledAsync();
  if (!isEnrolled) return false;

  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Authenticate to access your private data',
    fallbackLabel: 'Use passcode',
    disableDeviceFallback: false,
    cancelLabel: 'Cancel',
  });

  return result.success;
}
```

### App Lock Pattern

```typescript
function PrivacyGate({ children }: { children: React.ReactNode }) {
  const [authenticated, setAuthenticated] = useState(false);
  const { isEnabled } = usePrivacySettings();

  useEffect(() => {
    if (!isEnabled) {
      setAuthenticated(true);
      return;
    }
    checkAuth();
  }, [isEnabled]);

  async function checkAuth() {
    const success = await authenticateWithBiometrics();
    setAuthenticated(success);
  }

  if (!authenticated) {
    return <AuthPrompt onAuthenticate={checkAuth} />;
  }

  return children;
}
```

## Secure Storage Patterns

### Key Storage

```typescript
import * as SecureStore from 'expo-secure-store';

// Store encryption keys (NOT in AsyncStorage!)
await SecureStore.setItemAsync('encryption_key', key);

// Retrieve
const key = await SecureStore.getItemAsync('encryption_key');

// Delete on logout
await SecureStore.deleteItemAsync('encryption_key');
```

### What Goes Where

| Storage           | Use For                           | Never Store                |
| ----------------- | --------------------------------- | -------------------------- |
| SecureStore       | Encryption keys, auth tokens, PII | Large data                 |
| AsyncStorage      | UI state, cache, preferences      | Keys, tokens, PII          |
| SQLite            | App data, encrypted content       | Unencrypted sensitive data |
| Keychain/Keystore | Credentials, certificates         | -                          |

## Data Export (GDPR/CCPA)

```typescript
async function exportUserData(userId: string): Promise<string> {
  const db = await openDatabase();

  // Gather all user data
  const journal = await db.getAllAsync('SELECT * FROM journal WHERE user_id = ?', userId);
  const checkins = await db.getAllAsync('SELECT * FROM checkins WHERE user_id = ?', userId);

  // Decrypt what can be decrypted
  const decryptedJournal = await Promise.all(
    journal.map(async (entry) => ({
      ...entry,
      content: await decryptContent(entry.encrypted_body).catch(() => '[encrypted]'),
    })),
  );

  const exportData = {
    exported_at: new Date().toISOString(),
    user_id: userId,
    journal: decryptedJournal,
    checkins,
    // ... other tables
  };

  return JSON.stringify(exportData, null, 2);
}

async function shareDataExport(): Promise<void> {
  const data = await exportUserData(currentUser.id);
  const fileUri = FileSystem.cacheDirectory + 'export.json';

  await FileSystem.writeAsStringAsync(fileUri, data);
  await Sharing.shareAsync(fileUri, {
    mimeType: 'application/json',
    dialogTitle: 'Your Data Export',
  });
}
```

## Data Deletion

```typescript
async function deleteAllUserData(userId: string): Promise<void> {
  const db = await openDatabase();

  await db.withTransactionAsync(async () => {
    // Delete in order (respect FK constraints)
    await db.runAsync('DELETE FROM sync_queue WHERE user_id = ?', userId);
    await db.runAsync('DELETE FROM journal_entries WHERE user_id = ?', userId);
    await db.runAsync('DELETE FROM checkins WHERE user_id = ?', userId);
    await db.runAsync('DELETE FROM step_work WHERE user_id = ?', userId);
    await db.runAsync('DELETE FROM user_settings WHERE user_id = ?', userId);
  });

  // Clear secure storage
  await SecureStore.deleteItemAsync('encryption_key');
  await SecureStore.deleteItemAsync('auth_token');
}
```

## Privacy Settings UI

```typescript
function PrivacySettings() {
  const { settings, updateSetting } = usePrivacySettings();

  return (
    <View className="space-y-4">
      <SettingToggle
        title="Biometric Lock"
        description="Require Face ID/Touch ID to open app"
        value={settings.biometricLock}
        onChange={(v) => updateSetting('biometricLock', v)}
      />

      <SettingToggle
        title="Blur App in Switcher"
        description="Hide content in app switcher"
        value={settings.blurInSwitcher}
        onChange={(v) => updateSetting('blurInSwitcher', v)}
      />

      <SettingToggle
        title="Analytics"
        description="Help improve the app with anonymous usage data"
        value={settings.analyticsEnabled}
        onChange={(v) => updateSetting('analyticsEnabled', v)}
      />

      <Button
        title="Export My Data"
        variant="outline"
        onPress={shareDataExport}
      />

      <Button
        title="Delete All Data"
        variant="danger"
        onPress={confirmAndDelete}
      />
    </View>
  );
}
```

## App Switcher Privacy

```typescript
import { useAppState } from '@react-native-community/hooks';

function App({ children }) {
  const appState = useAppState();
  const [blur, setBlur] = useState(false);

  useEffect(() => {
    if (appState === 'background') {
      setBlur(true);
    } else if (appState === 'active') {
      // Optional: require auth after background
      setBlur(false);
    }
  }, [appState]);

  return (
    <View style={{ flex: 1 }}>
      {children}
      {blur && (
        <View
          style={StyleSheet.absoluteFill}
          className="bg-slate-900 items-center justify-center"
        >
          <Text className="text-white text-xl">Steps to Recovery</Text>
        </View>
      )}
    </View>
  );
}
```

## HIPAA Considerations

```typescript
// Audit logging for sensitive operations
async function auditLog(action: string, resource: string): Promise<void> {
  await db.runAsync(
    'INSERT INTO audit_log (user_id, action, resource, timestamp) VALUES (?, ?, ?, ?)',
    currentUser.id,
    action,
    resource,
    Date.now(),
  );
}

// Usage
async function viewJournalEntry(entryId: string) {
  await auditLog('VIEW', `journal:${entryId}`);
  // ... view logic
}

async function exportData() {
  await auditLog('EXPORT', 'user_data');
  // ... export logic
}
```

## Security Checklist

- [ ] Encryption keys in SecureStore only
- [ ] Biometric auth for sensitive screens
- [ ] App switcher blur enabled
- [ ] Auto-lock after inactivity
- [ ] Data export functionality
- [ ] Complete data deletion option
- [ ] Audit logging for HIPAA
- [ ] No PII in logs/crash reports
- [ ] Certificate pinning for API calls
- [ ] Sentry scrubbing for sensitive data
