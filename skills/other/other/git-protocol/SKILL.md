---
name: git-protocol
description: Git protocol implementation patterns using gitoxide for Guts repository operations
---

# Git Protocol Skill for Guts

You are implementing Git-compatible repository operations using gitoxide (gix).

## Gitoxide Overview

Gitoxide is a pure-Rust Git implementation. Key crates:

- `gix`: High-level Git operations
- `gix-object`: Git object types
- `gix-hash`: Object ID handling
- `gix-pack`: Pack file operations
- `gix-transport`: Git protocol transport

## Repository Operations

### Opening/Creating Repositories

```rust
use gix::Repository;
use std::path::Path;

pub async fn open_or_create(path: &Path) -> Result<Repository> {
    match gix::open(path) {
        Ok(repo) => Ok(repo),
        Err(_) => {
            // Create new bare repository
            gix::init_bare(path)?
        }
    }
}
```

### Working with Objects

```rust
use gix::ObjectId;
use gix::object::Kind;

pub struct ObjectStore {
    repo: Repository,
}

impl ObjectStore {
    pub fn get_object(&self, id: &ObjectId) -> Result<Object> {
        let object = self.repo.find_object(id)?;

        match object.kind {
            Kind::Blob => self.decode_blob(object),
            Kind::Tree => self.decode_tree(object),
            Kind::Commit => self.decode_commit(object),
            Kind::Tag => self.decode_tag(object),
        }
    }

    pub fn write_blob(&self, data: &[u8]) -> Result<ObjectId> {
        let id = self.repo.write_blob(data)?;
        Ok(id)
    }
}
```

### Commits

```rust
use gix::actor::Signature;

pub struct CommitBuilder<'a> {
    repo: &'a Repository,
    tree: ObjectId,
    parents: Vec<ObjectId>,
    message: String,
    author: Signature,
}

impl<'a> CommitBuilder<'a> {
    pub fn new(repo: &'a Repository) -> Self {
        let now = gix::date::Time::now_local_or_utc();
        let default_sig = Signature {
            name: "Guts User".into(),
            email: "user@guts.local".into(),
            time: now,
        };

        Self {
            repo,
            tree: ObjectId::null(),
            parents: vec![],
            message: String::new(),
            author: default_sig,
        }
    }

    pub fn tree(mut self, tree: ObjectId) -> Self {
        self.tree = tree;
        self
    }

    pub fn parent(mut self, parent: ObjectId) -> Self {
        self.parents.push(parent);
        self
    }

    pub fn message(mut self, msg: impl Into<String>) -> Self {
        self.message = msg.into();
        self
    }

    pub fn commit(self) -> Result<ObjectId> {
        let commit = gix::objs::CommitRef {
            tree: self.tree,
            parents: self.parents.into(),
            author: self.author.clone(),
            committer: self.author,
            encoding: None,
            message: self.message.into(),
            extra_headers: vec![],
        };

        let id = self.repo.write_object(&commit)?;
        Ok(id)
    }
}
```

## Git Protocol Implementation

### Smart HTTP Protocol

```rust
use axum::{Router, routing::post, extract::Path};

pub fn git_http_router() -> Router {
    Router::new()
        .route("/:owner/:repo/git-upload-pack", post(upload_pack))
        .route("/:owner/:repo/git-receive-pack", post(receive_pack))
        .route("/:owner/:repo/info/refs", get(info_refs))
}

async fn upload_pack(
    Path((owner, repo)): Path<(String, String)>,
    body: Bytes,
) -> Result<impl IntoResponse> {
    let repo = get_repository(&owner, &repo).await?;

    // Parse want/have lines
    let request = parse_upload_pack_request(&body)?;

    // Generate packfile with requested objects
    let packfile = generate_packfile(&repo, &request).await?;

    Ok((
        [(header::CONTENT_TYPE, "application/x-git-upload-pack-result")],
        packfile,
    ))
}

async fn receive_pack(
    Path((owner, repo)): Path<(String, String)>,
    body: Bytes,
) -> Result<impl IntoResponse> {
    let repo = get_repository(&owner, &repo).await?;

    // Parse commands and packfile
    let (commands, packfile) = parse_receive_pack(&body)?;

    // Verify permissions
    verify_push_permissions(&owner, &repo).await?;

    // Apply packfile
    apply_packfile(&repo, &packfile).await?;

    // Update refs
    for cmd in commands {
        update_ref(&repo, &cmd).await?;
    }

    Ok((
        [(header::CONTENT_TYPE, "application/x-git-receive-pack-result")],
        "ok\n",
    ))
}
```

### Pack File Generation

```rust
use gix::pack;

pub async fn generate_packfile(
    repo: &Repository,
    wants: &[ObjectId],
    haves: &[ObjectId],
) -> Result<Vec<u8>> {
    // Find all objects to include
    let objects = repo.rev_walk(wants)
        .sorting(Sorting::ByCommitTimeNewestFirst)
        .ancestors()
        .filter(|id| !haves.contains(id))
        .collect::<Vec<_>>();

    // Create pack file
    let mut pack_data = Vec::new();
    let mut writer = pack::data::output::bytes::Writer::new(&mut pack_data);

    for oid in objects {
        let object = repo.find_object(oid)?;
        writer.write_entry(object)?;
    }

    writer.finish()?;

    Ok(pack_data)
}
```

## Reference Management

```rust
pub struct RefStore {
    repo: Repository,
}

impl RefStore {
    pub fn list_refs(&self) -> Result<Vec<(String, ObjectId)>> {
        let refs = self.repo.references()?;

        refs.all()?
            .map(|r| {
                let r = r?;
                Ok((r.name().to_string(), r.target().id()))
            })
            .collect()
    }

    pub fn update_ref(&self, name: &str, new_id: ObjectId, old_id: Option<ObjectId>) -> Result<()> {
        let ref_log_message = format!("guts: update {}", name);

        if let Some(old) = old_id {
            // Atomic compare-and-swap
            self.repo
                .reference(name, new_id, PreviousValue::MustExistAndMatch(old.into()))?;
        } else {
            // Create new ref
            self.repo
                .reference(name, new_id, PreviousValue::MustNotExist)?;
        }

        Ok(())
    }

    pub fn get_head(&self) -> Result<ObjectId> {
        let head = self.repo.head_commit()?;
        Ok(head.id)
    }
}
```

## Guts Extensions to Git

```rust
/// Extended commit with Guts-specific metadata
#[derive(Debug, Clone)]
pub struct GutsCommit {
    /// Standard Git commit
    pub git_commit: gix::Commit,

    /// Ed25519 signature of commit hash
    pub signature: Signature,

    /// Signer's public key
    pub signer: PublicKey,

    /// Consensus round when commit was accepted
    pub consensus_round: Option<u64>,
}

impl GutsCommit {
    pub fn verify(&self) -> Result<bool> {
        let commit_hash = self.git_commit.id.as_bytes();
        self.signer.verify(commit_hash, &self.signature)
    }
}
```
