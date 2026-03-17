---
name: firestore_patterns
router_kit: FullStackKit
description: Firebase Firestore NoSQL patterns, real-time sync ve security rules rehberi.
metadata:
  skillport:
    category: database
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, firestore patterns, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - realtime
---

# 🔥 Firestore Patterns

> Firebase Firestore NoSQL patterns rehberi.

---

## 📋 Temel İşlemler

```typescript
import { 
  collection, doc, getDoc, setDoc, 
  addDoc, updateDoc, deleteDoc, query, where 
} from 'firebase/firestore';

// Read
const docRef = doc(db, 'users', 'userId');
const docSnap = await getDoc(docRef);

// Create
await setDoc(doc(db, 'users', 'userId'), { name: 'John' });
await addDoc(collection(db, 'users'), { name: 'John' }); // Auto ID

// Update
await updateDoc(doc(db, 'users', 'userId'), { name: 'Jane' });

// Delete
await deleteDoc(doc(db, 'users', 'userId'));
```

---

## 🔄 Real-time Listeners

```typescript
import { onSnapshot } from 'firebase/firestore';

const unsubscribe = onSnapshot(
  doc(db, 'users', 'userId'),
  (doc) => {
    console.log('Data:', doc.data());
  }
);

// Cleanup
unsubscribe();
```

---

## 🔍 Queries

```typescript
const q = query(
  collection(db, 'users'),
  where('age', '>=', 18),
  where('status', '==', 'active'),
  orderBy('createdAt', 'desc'),
  limit(10)
);

const querySnapshot = await getDocs(q);
```

---

## 🔒 Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth.uid == userId;
    }
  }
}
```

---

*Firestore Patterns v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Firebase Security Rules Guide](https://firebase.google.com/docs/firestore/security/get-started)

### Aşama 1: Data Modeling
- [ ] **Access Patterns**: Veriyi nasıl okuyacağına göre modelle (SQL gibi normalize etme).
- [ ] **Subcollections**: 1MB döküman limitini aşmamak için alt koleksiyon kullan.
- [ ] **Denormalization**: Okuma performansını artırmak için veriyi çoğaltmayı düşün.

### Aşama 2: Security Implementation
- [ ] **Auth**: `request.auth != null` kontrolünü her kurala ekle.
- [ ] **Validation**: Gelen veriyi (type, length) security rules içinde doğrula.
- [ ] **Testing**: Emulator kullanarak kuralları unit test ile sına.

### Aşama 3: Optimization
- [ ] **Indexes**: Karmaşık sorgular için composite index oluştur.
- [ ] **Offline**: Mobil için offline persistence'ı aktif et.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Bir dökümanı okumak için 100 başka döküman okumak gerekiyor mu? (Kötü) |
| 2 | Herkesin yazabildiği (`allow write: if true`) bir yer kaldı mı? (Kritik) |
| 3 | Sorgular index hatası veriyor mu? |
