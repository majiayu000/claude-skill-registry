---
name: contacts-framework
description: "Read, create, update, and pick contacts using the Contacts and ContactsUI frameworks. Use when fetching contact data, saving new contacts, wrapping CNContactPickerViewController in SwiftUI, handling contact permissions, or working with CNContactStore fetch and save requests."
---

# Contacts Framework

Fetch, create, update, and pick contacts from the user's Contacts database using
`CNContactStore`, `CNSaveRequest`, and `CNContactPickerViewController`. Targets
Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Authorization](#authorization)
- [Fetching Contacts](#fetching-contacts)
- [Key Descriptors](#key-descriptors)
- [Creating and Updating Contacts](#creating-and-updating-contacts)
- [Contact Picker](#contact-picker)
- [Observing Changes](#observing-changes)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Project Configuration

1. Add `NSContactsUsageDescription` to Info.plist explaining why the app accesses contacts
2. No additional capability or entitlement is required for basic Contacts access
3. For contact notes access, add the `com.apple.developer.contacts.notes` entitlement

### Imports

```swift
import Contacts       // CNContactStore, CNSaveRequest, CNContact
import ContactsUI     // CNContactPickerViewController
```

## Authorization

Request access before fetching or saving contacts. The picker (`CNContactPickerViewController`)
does not require authorization -- the system grants access only to the contacts
the user selects.

```swift
let store = CNContactStore()

func requestAccess() async throws -> Bool {
    return try await store.requestAccess(for: .contacts)
}

// Check current status without prompting
func checkStatus() -> CNAuthorizationStatus {
    CNContactStore.authorizationStatus(for: .contacts)
}
```

### Authorization States

| Status | Meaning |
|---|---|
| `.notDetermined` | User has not been prompted yet |
| `.authorized` | Full read/write access granted |
| `.denied` | User denied access; direct to Settings |
| `.restricted` | Parental controls or MDM restrict access |
| `.limited` | iOS 18+: user granted access to selected contacts only |

## Fetching Contacts

Use `unifiedContacts(matching:keysToFetch:)` for predicate-based queries.
Use `enumerateContacts(with:usingBlock:)` for batch enumeration of all contacts.

### Fetch by Name

```swift
func fetchContacts(named name: String) throws -> [CNContact] {
    let predicate = CNContact.predicateForContacts(matchingName: name)
    let keys: [CNKeyDescriptor] = [
        CNContactGivenNameKey as CNKeyDescriptor,
        CNContactFamilyNameKey as CNKeyDescriptor,
        CNContactPhoneNumbersKey as CNKeyDescriptor
    ]
    return try store.unifiedContacts(matching: predicate, keysToFetch: keys)
}
```

### Fetch by Identifier

```swift
func fetchContact(identifier: String) throws -> CNContact {
    let keys: [CNKeyDescriptor] = [
        CNContactGivenNameKey as CNKeyDescriptor,
        CNContactFamilyNameKey as CNKeyDescriptor,
        CNContactEmailAddressesKey as CNKeyDescriptor
    ]
    return try store.unifiedContact(withIdentifier: identifier, keysToFetch: keys)
}
```

### Enumerate All Contacts

Perform I/O-heavy enumeration off the main thread.

```swift
func fetchAllContacts() throws -> [CNContact] {
    let keys: [CNKeyDescriptor] = [
        CNContactGivenNameKey as CNKeyDescriptor,
        CNContactFamilyNameKey as CNKeyDescriptor
    ]
    let request = CNContactFetchRequest(keysToFetch: keys)
    request.sortOrder = .givenName

    var contacts: [CNContact] = []
    try store.enumerateContacts(with: request) { contact, _ in
        contacts.append(contact)
    }
    return contacts
}
```

## Key Descriptors

Only fetch the properties you need. Accessing an unfetched property throws
`CNContactPropertyNotFetchedException`.

### Common Keys

| Key | Property |
|---|---|
| `CNContactGivenNameKey` | First name |
| `CNContactFamilyNameKey` | Last name |
| `CNContactPhoneNumbersKey` | Phone numbers array |
| `CNContactEmailAddressesKey` | Email addresses array |
| `CNContactPostalAddressesKey` | Mailing addresses array |
| `CNContactImageDataKey` | Full-resolution contact photo |
| `CNContactThumbnailImageDataKey` | Thumbnail contact photo |
| `CNContactBirthdayKey` | Birthday date components |
| `CNContactOrganizationNameKey` | Company name |

### Composite Key Descriptors

Use `CNContactFormatter.descriptorForRequiredKeys(for:)` to fetch all keys needed
for formatting a contact's name.

```swift
let nameKeys = CNContactFormatter.descriptorForRequiredKeys(for: .fullName)
let keys: [CNKeyDescriptor] = [nameKeys, CNContactPhoneNumbersKey as CNKeyDescriptor]
```

## Creating and Updating Contacts

Use `CNMutableContact` to build new contacts and `CNSaveRequest` to persist changes.

### Creating a New Contact

```swift
func createContact(givenName: String, familyName: String, phone: String) throws {
    let contact = CNMutableContact()
    contact.givenName = givenName
    contact.familyName = familyName
    contact.phoneNumbers = [
        CNLabeledValue(
            label: CNLabelPhoneNumberMobile,
            value: CNPhoneNumber(stringValue: phone)
        )
    ]

    let saveRequest = CNSaveRequest()
    saveRequest.add(contact, toContainerWithIdentifier: nil) // nil = default container
    try store.execute(saveRequest)
}
```

### Updating an Existing Contact

You must fetch the contact with the properties you intend to modify, create a
mutable copy, change the properties, then save.

```swift
func updateContactEmail(identifier: String, email: String) throws {
    let keys: [CNKeyDescriptor] = [
        CNContactEmailAddressesKey as CNKeyDescriptor
    ]
    let contact = try store.unifiedContact(withIdentifier: identifier, keysToFetch: keys)
    guard let mutable = contact.mutableCopy() as? CNMutableContact else { return }

    mutable.emailAddresses.append(
        CNLabeledValue(label: CNLabelWork, value: email as NSString)
    )

    let saveRequest = CNSaveRequest()
    saveRequest.update(mutable)
    try store.execute(saveRequest)
}
```

### Deleting a Contact

```swift
func deleteContact(identifier: String) throws {
    let keys: [CNKeyDescriptor] = [CNContactIdentifierKey as CNKeyDescriptor]
    let contact = try store.unifiedContact(withIdentifier: identifier, keysToFetch: keys)
    guard let mutable = contact.mutableCopy() as? CNMutableContact else { return }

    let saveRequest = CNSaveRequest()
    saveRequest.delete(mutable)
    try store.execute(saveRequest)
}
```

## Contact Picker

`CNContactPickerViewController` lets users pick contacts without granting full
Contacts access. The app receives only the selected contact data.

### SwiftUI Wrapper

```swift
import SwiftUI
import ContactsUI

struct ContactPicker: UIViewControllerRepresentable {
    @Binding var selectedContact: CNContact?

    func makeUIViewController(context: Context) -> CNContactPickerViewController {
        let picker = CNContactPickerViewController()
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: CNContactPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    final class Coordinator: NSObject, CNContactPickerDelegate {
        let parent: ContactPicker

        init(_ parent: ContactPicker) {
            self.parent = parent
        }

        func contactPicker(_ picker: CNContactPickerViewController, didSelect contact: CNContact) {
            parent.selectedContact = contact
        }

        func contactPickerDidCancel(_ picker: CNContactPickerViewController) {
            parent.selectedContact = nil
        }
    }
}
```

### Using the Picker

```swift
struct ContactSelectionView: View {
    @State private var selectedContact: CNContact?
    @State private var showPicker = false

    var body: some View {
        VStack {
            if let contact = selectedContact {
                Text("\(contact.givenName) \(contact.familyName)")
            }
            Button("Select Contact") {
                showPicker = true
            }
        }
        .sheet(isPresented: $showPicker) {
            ContactPicker(selectedContact: $selectedContact)
        }
    }
}
```

### Filtering the Picker

Use predicates to control which contacts appear and what the user can select.

```swift
let picker = CNContactPickerViewController()
// Only show contacts that have an email address
picker.predicateForEnablingContact = NSPredicate(format: "emailAddresses.@count > 0")
// Selecting a contact returns it directly (no detail card)
picker.predicateForSelectionOfContact = NSPredicate(value: true)
```

## Observing Changes

Listen for external contact database changes to refresh cached data.

```swift
func observeContactChanges() {
    NotificationCenter.default.addObserver(
        forName: .CNContactStoreDidChange,
        object: nil,
        queue: .main
    ) { _ in
        // Refetch contacts -- cached CNContact objects are stale
        refreshContacts()
    }
}
```

## Common Mistakes

### DON'T: Fetch all keys when you only need a name

Over-fetching wastes memory and slows queries, especially for contacts with
large photos.

```swift
// WRONG: Fetches everything including full-resolution photos
let keys: [CNKeyDescriptor] = [CNContactCompleteNameKey as CNKeyDescriptor,
    CNContactImageDataKey as CNKeyDescriptor,
    CNContactPhoneNumbersKey as CNKeyDescriptor,
    CNContactEmailAddressesKey as CNKeyDescriptor,
    CNContactPostalAddressesKey as CNKeyDescriptor,
    CNContactBirthdayKey as CNKeyDescriptor]

// CORRECT: Fetch only what you display
let keys: [CNKeyDescriptor] = [
    CNContactGivenNameKey as CNKeyDescriptor,
    CNContactFamilyNameKey as CNKeyDescriptor
]
```

### DON'T: Access unfetched properties

Accessing a property that was not in `keysToFetch` throws
`CNContactPropertyNotFetchedException` at runtime.

```swift
// WRONG: Only fetched name keys, now accessing phone
let keys: [CNKeyDescriptor] = [CNContactGivenNameKey as CNKeyDescriptor]
let contact = try store.unifiedContact(withIdentifier: id, keysToFetch: keys)
let phone = contact.phoneNumbers.first // CRASH

// CORRECT: Include the key you need
let keys: [CNKeyDescriptor] = [
    CNContactGivenNameKey as CNKeyDescriptor,
    CNContactPhoneNumbersKey as CNKeyDescriptor
]
```

### DON'T: Mutate a CNContact directly

`CNContact` is immutable. You must call `mutableCopy()` to get a `CNMutableContact`.

```swift
// WRONG: CNContact has no setter
let contact = try store.unifiedContact(withIdentifier: id, keysToFetch: keys)
contact.givenName = "New Name" // Compile error

// CORRECT: Create mutable copy
guard let mutable = contact.mutableCopy() as? CNMutableContact else { return }
mutable.givenName = "New Name"
```

### DON'T: Skip authorization and assume access

Without calling `requestAccess(for:)`, fetch methods return empty results or throw.

```swift
// WRONG: Jump straight to fetch
let contacts = try store.unifiedContacts(matching: predicate, keysToFetch: keys)

// CORRECT: Check or request access first
let granted = try await store.requestAccess(for: .contacts)
guard granted else { return }
let contacts = try store.unifiedContacts(matching: predicate, keysToFetch: keys)
```

### DON'T: Run heavy fetches on the main thread

`enumerateContacts` performs I/O. Running it on the main thread blocks the UI.

```swift
// WRONG: Main thread enumeration
func loadContacts() {
    try store.enumerateContacts(with: request) { contact, _ in ... }
}

// CORRECT: Run on a background thread
func loadContacts() async throws -> [CNContact] {
    try await Task.detached {
        var results: [CNContact] = []
        try store.enumerateContacts(with: request) { contact, _ in
            results.append(contact)
        }
        return results
    }.value
}
```

## Review Checklist

- [ ] `NSContactsUsageDescription` added to Info.plist
- [ ] `requestAccess(for: .contacts)` called before fetch or save operations
- [ ] Authorization denial handled gracefully (guide user to Settings)
- [ ] Only needed `CNKeyDescriptor` keys included in fetch requests
- [ ] `CNContactFormatter.descriptorForRequiredKeys(for:)` used when formatting names
- [ ] Mutable copy created via `mutableCopy()` before modifying contacts
- [ ] `CNSaveRequest` used for all create/update/delete operations
- [ ] Heavy fetches (`enumerateContacts`) run off the main thread
- [ ] `CNContactStoreDidChange` observed to refresh cached contacts
- [ ] `CNContactPickerViewController` used when full Contacts access is unnecessary
- [ ] Picker predicates set before presenting the picker view controller
- [ ] Single `CNContactStore` instance reused across the app

## References

- Extended patterns (multi-select picker, vCard export, search optimization): `references/contacts-patterns.md`
- [Contacts framework](https://sosumi.ai/documentation/contacts)
- [CNContactStore](https://sosumi.ai/documentation/contacts/cncontactstore)
- [CNContactFetchRequest](https://sosumi.ai/documentation/contacts/cncontactfetchrequest)
- [CNSaveRequest](https://sosumi.ai/documentation/contacts/cnsaverequest)
- [CNMutableContact](https://sosumi.ai/documentation/contacts/cnmutablecontact)
- [CNContactPickerViewController](https://sosumi.ai/documentation/contactsui/cncontactpickerviewcontroller)
- [CNContactPickerDelegate](https://sosumi.ai/documentation/contactsui/cncontactpickerdelegate)
- [Accessing the contact store](https://sosumi.ai/documentation/contacts/accessing-the-contact-store)
- [NSContactsUsageDescription](https://sosumi.ai/documentation/bundleresources/information-property-list/nscontactsusagedescription)
