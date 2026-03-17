---
name: mobile-offline-support
description: Implement offline-first mobile apps with local storage, sync strategies, and conflict resolution. Covers AsyncStorage, Realm, SQLite, and background sync patterns.
---

# Mobile Offline Support

## Overview

Design offline-first mobile applications that provide seamless user experience regardless of connectivity.

## When to Use

- Building apps that work without internet connection
- Implementing seamless sync when connectivity returns
- Handling data conflicts between device and server
- Reducing server load with intelligent caching
- Improving app responsiveness with local storage

## Instructions

### 1. **React Native Offline Storage**

```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

class StorageManager {
  static async saveItems(items) {
    try {
      await AsyncStorage.setItem(
        'items_cache',
        JSON.stringify({ data: items, timestamp: Date.now() })
      );
    } catch (error) {
      console.error('Failed to save items:', error);
    }
  }

  static async getItems() {
    try {
      const data = await AsyncStorage.getItem('items_cache');
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Failed to retrieve items:', error);
      return null;
    }
  }

  static async queueAction(action) {
    try {
      const queue = await AsyncStorage.getItem('action_queue');
      const actions = queue ? JSON.parse(queue) : [];
      actions.push({ ...action, id: Date.now(), attempts: 0 });
      await AsyncStorage.setItem('action_queue', JSON.stringify(actions));
    } catch (error) {
      console.error('Failed to queue action:', error);
    }
  }

  static async getActionQueue() {
    try {
      const queue = await AsyncStorage.getItem('action_queue');
      return queue ? JSON.parse(queue) : [];
    } catch (error) {
      return [];
    }
  }

  static async removeFromQueue(actionId) {
    try {
      const queue = await AsyncStorage.getItem('action_queue');
      const actions = queue ? JSON.parse(queue) : [];
      const filtered = actions.filter(a => a.id !== actionId);
      await AsyncStorage.setItem('action_queue', JSON.stringify(filtered));
    } catch (error) {
      console.error('Failed to remove from queue:', error);
    }
  }
}

class OfflineAPIService {
  async fetchItems() {
    const isOnline = await this.checkConnectivity();

    if (isOnline) {
      try {
        const response = await fetch('https://api.example.com/items');
        const items = await response.json();
        await StorageManager.saveItems(items);
        return items;
      } catch (error) {
        const cached = await StorageManager.getItems();
        return cached?.data || [];
      }
    } else {
      const cached = await StorageManager.getItems();
      return cached?.data || [];
    }
  }

  async createItem(item) {
    const isOnline = await this.checkConnectivity();

    if (isOnline) {
      try {
        const response = await fetch('https://api.example.com/items', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item)
        });
        const created = await response.json();
        return { success: true, data: created };
      } catch (error) {
        await StorageManager.queueAction({
          type: 'CREATE_ITEM',
          payload: item
        });
        return { success: false, queued: true };
      }
    } else {
      await StorageManager.queueAction({
        type: 'CREATE_ITEM',
        payload: item
      });
      return { success: false, queued: true };
    }
  }

  async syncQueue() {
    const queue = await StorageManager.getActionQueue();

    for (const action of queue) {
      try {
        await this.executeAction(action);
        await StorageManager.removeFromQueue(action.id);
      } catch (error) {
        action.attempts = (action.attempts || 0) + 1;
        if (action.attempts > 3) {
          await StorageManager.removeFromQueue(action.id);
        }
      }
    }
  }

  private async executeAction(action) {
    switch (action.type) {
      case 'CREATE_ITEM':
        return fetch('https://api.example.com/items', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(action.payload)
        });
      default:
        return Promise.reject(new Error('Unknown action type'));
    }
  }

  async checkConnectivity() {
    const state = await NetInfo.fetch();
    return state.isConnected ?? false;
  }
}

export function OfflineListScreen() {
  const [items, setItems] = useState([]);
  const [isOnline, setIsOnline] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const apiService = new OfflineAPIService();

  useFocusEffect(
    useCallback(() => {
      loadItems();
      const unsubscribe = NetInfo.addEventListener(state => {
        setIsOnline(state.isConnected ?? false);
        if (state.isConnected) {
          syncQueue();
        }
      });

      return unsubscribe;
    }, [])
  );

  const loadItems = async () => {
    const items = await apiService.fetchItems();
    setItems(items);
  };

  const syncQueue = async () => {
    setSyncing(true);
    await apiService.syncQueue();
    await loadItems();
    setSyncing(false);
  };

  return (
    <View style={styles.container}>
      {!isOnline && <Text style={styles.offline}>Offline Mode</Text>}
      {syncing && <ActivityIndicator size="large" />}
      <FlatList
        data={items}
        renderItem={({ item }) => <ItemCard item={item} />}
        keyExtractor={item => item.id}
      />
    </View>
  );
}
```

### 2. **iOS Core Data Implementation**

```swift
import CoreData

class PersistenceController {
  static let shared = PersistenceController()

  let container: NSPersistentContainer

  init(inMemory: Bool = false) {
    container = NSPersistentContainer(name: "MyApp")

    if inMemory {
      container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
    }

    container.loadPersistentStores { _, error in
      if let error = error as NSError? {
        print("Core Data load error: \(error)")
      }
    }

    container.viewContext.automaticallyMergesChangesFromParent = true
  }

  func save(_ context: NSManagedObjectContext = PersistenceController.shared.container.viewContext) {
    if context.hasChanges {
      do {
        try context.save()
      } catch {
        print("Save error: \(error)")
      }
    }
  }
}

// Core Data Models
@NSManaged class ItemEntity: NSManagedObject {
  @NSManaged var id: String
  @NSManaged var title: String
  @NSManaged var description: String?
  @NSManaged var isSynced: Bool
}

@NSManaged class ActionQueueEntity: NSManagedObject {
  @NSManaged var id: UUID
  @NSManaged var type: String
  @NSManaged var payload: Data?
  @NSManaged var createdAt: Date
}

class OfflineSyncManager: NSObject, ObservableObject {
  @Published var isOnline = true
  @Published var isSyncing = false

  private let networkMonitor = NWPathMonitor()
  private let persistenceController = PersistenceController.shared

  override init() {
    super.init()
    setupNetworkMonitoring()
  }

  private func setupNetworkMonitoring() {
    networkMonitor.pathUpdateHandler = { [weak self] path in
      DispatchQueue.main.async {
        self?.isOnline = path.status == .satisfied
        if path.status == .satisfied {
          self?.syncWithServer()
        }
      }
    }

    let queue = DispatchQueue(label: "NetworkMonitor")
    networkMonitor.start(queue: queue)
  }

  func saveItem(_ item: Item) {
    let context = persistenceController.container.viewContext
    let entity = ItemEntity(context: context)
    entity.id = item.id
    entity.title = item.title
    entity.isSynced = false

    persistenceController.save(context)

    if isOnline {
      syncItem(item)
    }
  }

  func syncWithServer() {
    isSyncing = true
    let context = persistenceController.container.viewContext
    let request: NSFetchRequest<ActionQueueEntity> = ActionQueueEntity.fetchRequest()

    do {
      let pendingActions = try context.fetch(request)
      for action in pendingActions {
        context.delete(action)
      }
      persistenceController.save(context)
    } catch {
      print("Sync error: \(error)")
    }

    isSyncing = false
  }
}
```

### 3. **Android Room Database**

```kotlin
@Entity(tableName = "items")
data class ItemEntity(
  @PrimaryKey val id: String,
  val title: String,
  val description: String?,
  val isSynced: Boolean = false
)

@Entity(tableName = "action_queue")
data class ActionQueueEntity(
  @PrimaryKey val id: Long = System.currentTimeMillis(),
  val type: String,
  val payload: String,
  val createdAt: Long = System.currentTimeMillis()
)

@Dao
interface ItemDao {
  @Insert(onConflict = OnConflictStrategy.REPLACE)
  suspend fun insertItem(item: ItemEntity)

  @Query("SELECT * FROM items")
  fun getAllItems(): Flow<List<ItemEntity>>

  @Update
  suspend fun updateItem(item: ItemEntity)
}

@Dao
interface ActionQueueDao {
  @Insert
  suspend fun insertAction(action: ActionQueueEntity)

  @Query("SELECT * FROM action_queue ORDER BY createdAt ASC")
  suspend fun getAllActions(): List<ActionQueueEntity>

  @Delete
  suspend fun deleteAction(action: ActionQueueEntity)
}

@Database(entities = [ItemEntity::class, ActionQueueEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
  abstract fun itemDao(): ItemDao
  abstract fun actionQueueDao(): ActionQueueDao
}

@HiltViewModel
class OfflineItemsViewModel @Inject constructor(
  private val itemDao: ItemDao,
  private val actionQueueDao: ActionQueueDao,
  private val connectivityManager: ConnectivityManager
) : ViewModel() {
  private val _items = MutableStateFlow<List<Item>>(emptyList())
  val items: StateFlow<List<Item>> = _items.asStateFlow()

  init {
    viewModelScope.launch {
      itemDao.getAllItems().collect { entities ->
        _items.value = entities.map { it.toItem() }
      }
    }
    observeNetworkConnectivity()
  }

  fun saveItem(item: Item) {
    viewModelScope.launch {
      val entity = item.toEntity()
      itemDao.insertItem(entity)

      if (isNetworkAvailable()) {
        syncItem(item)
      } else {
        actionQueueDao.insertAction(
          ActionQueueEntity(
            type = "CREATE_ITEM",
            payload = Json.encodeToString(item)
          )
        )
      }
    }
  }

  private fun observeNetworkConnectivity() {
    val networkRequest = NetworkRequest.Builder()
      .addCapability(NET_CAPABILITY_INTERNET)
      .build()

    connectivityManager.registerNetworkCallback(
      networkRequest,
      object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
          viewModelScope.launch { syncQueue() }
        }
      }
    )
  }

  private suspend fun syncQueue() {
    val queue = actionQueueDao.getAllActions()
    for (action in queue) {
      try {
        actionQueueDao.deleteAction(action)
      } catch (e: Exception) {
        println("Sync error: ${e.message}")
      }
    }
  }

  private fun isNetworkAvailable(): Boolean {
    val activeNetwork = connectivityManager.activeNetwork ?: return false
    val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork) ?: return false
    return capabilities.hasCapability(NET_CAPABILITY_INTERNET)
  }
}
```

## Best Practices

### ✅ DO
- Implement robust local storage
- Use automatic sync when online
- Provide visual feedback for offline status
- Queue actions for later sync
- Handle conflicts gracefully
- Cache frequently accessed data
- Implement proper error recovery
- Test offline scenarios thoroughly
- Use compression for large data
- Monitor storage usage

### ❌ DON'T
- Assume constant connectivity
- Sync large files frequently
- Ignore storage limitations
- Force unnecessary syncing
- Lose data on offline mode
- Store sensitive data unencrypted
- Accumulate infinite queue items
- Ignore sync failures silently
- Sync in tight loops
- Deploy without offline testing
