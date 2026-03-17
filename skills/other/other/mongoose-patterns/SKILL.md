---
name: mongoose-patterns
description: Mongoose/MongoDB patterns for schema design, queries, indexes, aggregations. Use when working with MongoDB through Mongoose.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Mongoose Patterns - MongoDB ODM Best Practices

## Purpose

Expert guidance for Mongoose/MongoDB:

- **Schema Design** - Proper typing and validation
- **Queries** - Efficient query patterns
- **Indexes** - Performance optimization
- **Aggregations** - Complex data operations
- **Relationships** - References vs embedding

---

## Project Structure

```
server/
├── db/
│   ├── connection.ts      # MongoDB connection
│   └── index.ts           # Export db utilities
├── models/
│   ├── user.model.ts
│   ├── post.model.ts
│   └── index.ts           # Export all models
types/
└── models/
    ├── user.types.ts      # User interfaces
    └── post.types.ts      # Post interfaces
```

---

## Schema Design

### Basic Schema with TypeScript

```typescript
// types/models/user.types.ts
import { Types, Document } from 'mongoose';

export interface IUser {
	email: string;
	name: string;
	passwordHash: string;
	role: 'admin' | 'user' | 'guest';
	profile?: {
		bio?: string;
		avatar?: string;
	};
	createdAt: Date;
	updatedAt: Date;
}

export interface IUserDocument extends IUser, Document {
	_id: Types.ObjectId;
	comparePassword(password: string): Promise<boolean>;
	toPublic(): Omit<IUser, 'passwordHash'>;
}

// server/models/user.model.ts
import mongoose, { Schema, Model } from 'mongoose';
import { IUser, IUserDocument } from '$types/models/user.types';

const userSchema = new Schema<IUserDocument>(
	{
		email: {
			type: String,
			required: [true, 'Email is required'],
			unique: true,
			lowercase: true,
			trim: true,
			validate: {
				validator: (v: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
				message: 'Invalid email format',
			},
		},
		name: {
			type: String,
			required: [true, 'Name is required'],
			minlength: [2, 'Name must be at least 2 characters'],
			maxlength: [100, 'Name cannot exceed 100 characters'],
			trim: true,
		},
		passwordHash: {
			type: String,
			required: true,
			select: false, // Never include by default
		},
		role: {
			type: String,
			enum: ['admin', 'user', 'guest'],
			default: 'user',
		},
		profile: {
			bio: { type: String, maxlength: 500 },
			avatar: { type: String },
		},
	},
	{
		timestamps: true,
		toJSON: { virtuals: true },
		toObject: { virtuals: true },
	}
);

// Indexes
userSchema.index({ email: 1 }, { unique: true });
userSchema.index({ role: 1 });
userSchema.index({ createdAt: -1 });

// Instance methods
userSchema.methods.comparePassword = async function (password: string): Promise<boolean> {
	return Bun.password.verify(password, this.passwordHash);
};

userSchema.methods.toPublic = function () {
	const obj = this.toObject();
	delete obj.passwordHash;
	return obj;
};

// Static methods
userSchema.statics.findByEmail = function (email: string) {
	return this.findOne({ email: email.toLowerCase() });
};

export const UserModel: Model<IUserDocument> = mongoose.model('User', userSchema);
```

---

## Connection Management

```typescript
// server/db/connection.ts
import mongoose from 'mongoose';
import { logger } from '@common';

const MONGODB_URI = process.env['MONGODB_URI']!;

if (!MONGODB_URI) {
	throw new Error('MONGODB_URI environment variable not set');
}

let isConnected = false;

export async function connectDB(): Promise<void> {
	if (isConnected) {
		logger.info('Using existing MongoDB connection');
		return;
	}

	try {
		await mongoose.connect(MONGODB_URI, {
			maxPoolSize: 10,
			serverSelectionTimeoutMS: 5000,
			socketTimeoutMS: 45000,
		});

		isConnected = true;
		logger.info('Connected to MongoDB');
	} catch (error) {
		logger.error('MongoDB connection error:', error);
		throw error;
	}
}

export async function disconnectDB(): Promise<void> {
	if (!isConnected) return;

	await mongoose.disconnect();
	isConnected = false;
	logger.info('Disconnected from MongoDB');
}

// Graceful shutdown
process.on('SIGINT', async () => {
	await disconnectDB();
	process.exit(0);
});
```

---

## Query Patterns

### Find with Typing

```typescript
// Find one
const user = await UserModel.findById(id);
const userByEmail = await UserModel.findOne({ email });

// Find with projection
const users = await UserModel.find({ role: 'user' }).select('name email role').lean(); // Returns plain objects (faster)

// Find with pagination
const page = 1;
const limit = 20;
const users = await UserModel.find()
	.sort({ createdAt: -1 })
	.skip((page - 1) * limit)
	.limit(limit)
	.lean();

// Count
const total = await UserModel.countDocuments({ role: 'user' });
```

### Update Patterns

```typescript
// Update one (returns updated doc)
const updated = await UserModel.findByIdAndUpdate(
	id,
	{ $set: { name: 'New Name' } },
	{ new: true, runValidators: true }
);

// Update many
const result = await UserModel.updateMany({ role: 'guest' }, { $set: { role: 'user' } });
console.log(`Updated ${result.modifiedCount} documents`);

// Upsert
const user = await UserModel.findOneAndUpdate(
	{ email },
	{ $setOnInsert: { createdAt: new Date() }, $set: { lastLogin: new Date() } },
	{ upsert: true, new: true }
);
```

### Delete Patterns

```typescript
// Delete one
await UserModel.findByIdAndDelete(id);

// Delete many
const result = await UserModel.deleteMany({ role: 'guest' });
console.log(`Deleted ${result.deletedCount} documents`);

// Soft delete pattern
const softDeleteSchema = new Schema({
	deletedAt: { type: Date, default: null },
});

// Query middleware to exclude soft-deleted
userSchema.pre('find', function () {
	this.where({ deletedAt: null });
});
```

---

## Aggregation Pipeline

```typescript
// Complex aggregation
const stats = await UserModel.aggregate([
	// Match stage
	{ $match: { createdAt: { $gte: startDate } } },

	// Group stage
	{
		$group: {
			_id: '$role',
			count: { $sum: 1 },
			avgAge: { $avg: '$age' },
		},
	},

	// Sort stage
	{ $sort: { count: -1 } },

	// Project stage
	{
		$project: {
			role: '$_id',
			count: 1,
			avgAge: { $round: ['$avgAge', 1] },
			_id: 0,
		},
	},
]);

// Lookup (join)
const postsWithAuthors = await PostModel.aggregate([
	{
		$lookup: {
			from: 'users',
			localField: 'authorId',
			foreignField: '_id',
			as: 'author',
		},
	},
	{ $unwind: '$author' },
	{
		$project: {
			title: 1,
			content: 1,
			'author.name': 1,
			'author.email': 1,
		},
	},
]);
```

---

## Indexes

### Index Types

```typescript
// Single field
userSchema.index({ email: 1 }); // Ascending
userSchema.index({ createdAt: -1 }); // Descending

// Compound index
userSchema.index({ role: 1, createdAt: -1 });

// Unique index
userSchema.index({ email: 1 }, { unique: true });

// Sparse index (only index docs with field)
userSchema.index({ nickname: 1 }, { sparse: true });

// TTL index (auto-delete after time)
sessionSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });

// Text index (full-text search)
postSchema.index({ title: 'text', content: 'text' });

// Partial index
userSchema.index(
	{ email: 1 },
	{
		partialFilterExpression: { isActive: true },
	}
);
```

### Check Indexes

```bash
# List indexes
db.users.getIndexes()

# Explain query
db.users.find({ email: "test@test.com" }).explain("executionStats")
```

---

## Relationships

### Reference (Normalized)

```typescript
// Post references User
const postSchema = new Schema({
	title: String,
	authorId: {
		type: Schema.Types.ObjectId,
		ref: 'User',
		required: true,
		index: true,
	},
});

// Populate
const post = await PostModel.findById(id).populate('authorId', 'name email');

// Virtual populate
userSchema.virtual('posts', {
	ref: 'Post',
	localField: '_id',
	foreignField: 'authorId',
});

const user = await UserModel.findById(id).populate('posts');
```

### Embedded (Denormalized)

```typescript
// Comments embedded in Post
const postSchema = new Schema({
	title: String,
	comments: [
		{
			author: String,
			content: String,
			createdAt: { type: Date, default: Date.now },
		},
	],
});

// Add comment
await PostModel.findByIdAndUpdate(id, {
	$push: { comments: { author: 'John', content: 'Great post!' } },
});
```

---

## Middleware (Hooks)

```typescript
// Pre-save hook
userSchema.pre('save', async function (next) {
	if (this.isModified('passwordHash')) {
		this.passwordHash = await Bun.password.hash(this.passwordHash);
	}
	next();
});

// Post-save hook
userSchema.post('save', function (doc) {
	logger.info(`User saved: ${doc.email}`);
});

// Pre-find hook
userSchema.pre('find', function () {
	// Always exclude deleted documents
	this.where({ deletedAt: null });
});

// Error handling hook
userSchema.post('save', function (error: Error, doc: IUserDocument, next: () => void) {
	if (error.name === 'MongoServerError' && (error as any).code === 11000) {
		next(new Error('Email already exists'));
	} else {
		next();
	}
});
```

---

## Transactions

```typescript
import mongoose from 'mongoose';

async function transferCredits(fromId: string, toId: string, amount: number) {
	const session = await mongoose.startSession();

	try {
		session.startTransaction();

		await UserModel.findByIdAndUpdate(fromId, { $inc: { credits: -amount } }, { session });

		await UserModel.findByIdAndUpdate(toId, { $inc: { credits: amount } }, { session });

		await session.commitTransaction();
	} catch (error) {
		await session.abortTransaction();
		throw error;
	} finally {
		session.endSession();
	}
}
```

---

## Agent Integration

This skill is used by:

- **mongoose-schema-designer** agent
- **mongoose-index-optimizer** agent
- **mongoose-aggregation** agent
- **mongodb-query-optimizer** agent
- **database-seeder** agent

---

## FORBIDDEN

1. **User ID from input** - Always use session/context
2. **No indexes on query fields** - Always index filtered fields
3. **Returning passwordHash** - Use `select: false`
4. **N+1 queries** - Use `.populate()` or aggregation
5. **Unbounded queries** - Always use `.limit()`

---

## Version

- **v1.0.0** - Initial implementation based on Mongoose 8.x patterns
