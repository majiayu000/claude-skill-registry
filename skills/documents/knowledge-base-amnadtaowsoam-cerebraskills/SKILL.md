---
name: Knowledge Base Implementation
description: Building self-service support systems by organizing articles, documentation, and FAQs with search functionality, categorization, and analytics to help users find answers without contacting support.
---

# Knowledge Base Implementation

> **Current Level:** Intermediate  
> **Domain:** Customer Support / Documentation

---

## Overview

A knowledge base provides self-service support by organizing articles, documentation, and FAQs that help users find answers without contacting support. Effective knowledge bases include search functionality, categorization, rich content, and analytics to improve findability and reduce support tickets.

---

## Core Concepts

### Table of Contents

1. [Knowledge Base Structure](#knowledge-base-structure)
2. [Article Management](#article-management)
3. [Categories and Tags](#categories-and-tags)
4. [Search Functionality](#search-functionality)
5. [Article Templates](#article-templates)
6. [Rich Content Editor](#rich-content-editor)
7. [Media Management](#media-management)
8. [Analytics](#analytics)
9. [Related Articles](#related-articles)
10. [SEO Optimization](#seo-optimization)
11. [Multi-Language Support](#multi-language-support)
12. [Best Practices](#best-practices)

---

## Knowledge Base Structure

### Data Models

```typescript
interface Article {
  id: string;
  title: string;
  slug: string;
  excerpt?: string;
  content: string;
  status: 'draft' | 'published' | 'archived';
  categoryId: string;
  tags: string[];
  authorId: string;
  language: string;
  version: number;
  publishedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  seo?: SEOData;
  customFields?: Record<string, any>;
}

interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  parentId?: string;
  icon?: string;
  order: number;
  language: string;
  articleCount: number;
}

interface Tag {
  id: string;
  name: string;
  slug: string;
  color?: string;
  articleCount: number;
}

interface SEOData {
  metaTitle?: string;
  metaDescription?: string;
  keywords?: string[];
  ogImage?: string;
  canonicalUrl?: string;
}

interface ArticleVersion {
  id: string;
  articleId: string;
  version: number;
  title: string;
  content: string;
  createdBy: string;
  createdAt: Date;
  changeLog: string;
}
```

### Database Schema

```sql
-- Categories
CREATE TABLE kb_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL UNIQUE,
  description TEXT,
  parent_id UUID REFERENCES kb_categories(id) ON DELETE SET NULL,
  icon VARCHAR(100),
  "order" INTEGER DEFAULT 0,
  language VARCHAR(10) NOT NULL DEFAULT 'en',
  article_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Tags
CREATE TABLE kb_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) NOT NULL UNIQUE,
  color VARCHAR(7),
  article_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Articles
CREATE TABLE kb_articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR(500) NOT NULL,
  slug VARCHAR(500) NOT NULL,
  excerpt TEXT,
  content TEXT NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'draft',
  category_id UUID REFERENCES kb_categories(id) ON DELETE SET NULL,
  author_id UUID NOT NULL,
  language VARCHAR(10) NOT NULL DEFAULT 'en',
  version INTEGER DEFAULT 1,
  published_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  seo_meta_title VARCHAR(500),
  seo_meta_description TEXT,
  seo_keywords TEXT[],
  seo_og_image VARCHAR(500),
  seo_canonical_url VARCHAR(500),
  custom_fields JSONB,
  UNIQUE(slug, language)
);

-- Article tags (many-to-many)
CREATE TABLE kb_article_tags (
  article_id UUID REFERENCES kb_articles(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES kb_tags(id) ON DELETE CASCADE,
  PRIMARY KEY (article_id, tag_id)
);

-- Article versions
CREATE TABLE kb_article_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES kb_articles(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,
  title VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  created_by UUID NOT NULL,
  change_log TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(article_id, version)
);

-- Article views
CREATE TABLE kb_article_views (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES kb_articles(id) ON DELETE CASCADE,
  user_id UUID,
  session_id VARCHAR(255),
  viewed_at TIMESTAMP DEFAULT NOW(),
  ip_address INET,
  user_agent TEXT
);

-- Article feedback
CREATE TABLE kb_article_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES kb_articles(id) ON DELETE CASCADE,
  user_id UUID,
  helpful BOOLEAN,
  comment TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Media
CREATE TABLE kb_media (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES kb_articles(id) ON DELETE SET NULL,
  file_name VARCHAR(255) NOT NULL,
  file_url VARCHAR(500) NOT NULL,
  file_size INTEGER NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  width INTEGER,
  height INTEGER,
  alt_text VARCHAR(500),
  uploaded_by UUID NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_kb_articles_status ON kb_articles(status);
CREATE INDEX idx_kb_articles_category_id ON kb_articles(category_id);
CREATE INDEX idx_kb_articles_language ON kb_articles(language);
CREATE INDEX idx_kb_articles_published_at ON kb_articles(published_at);
CREATE INDEX idx_kb_articles_slug ON kb_articles(slug);
CREATE INDEX idx_kb_article_tags_article_id ON kb_article_tags(article_id);
CREATE INDEX idx_kb_article_tags_tag_id ON kb_article_tags(tag_id);
CREATE INDEX idx_kb_article_views_article_id ON kb_article_views(article_id);
CREATE INDEX idx_kb_article_views_viewed_at ON kb_article_views(viewed_at);
CREATE INDEX idx_kb_article_feedback_article_id ON kb_article_feedback(article_id);
CREATE INDEX idx_kb_media_article_id ON kb_media(article_id);
```

---

## Article Management

### Article CRUD Operations

```typescript
class ArticleManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create article
   */
  async createArticle(params: {
    title: string;
    content: string;
    excerpt?: string;
    categoryId: string;
    tags?: string[];
    authorId: string;
    language?: string;
    seo?: SEOData;
    customFields?: Record<string, any>;
  }): Promise<Article> {
    // Generate slug
    const slug = this.generateSlug(params.title);

    // Create article
    const article = await this.prisma.kbArticle.create({
      data: {
        title: params.title,
        slug,
        excerpt: params.excerpt,
        content: params.content,
        categoryId: params.categoryId,
        authorId: params.authorId,
        language: params.language || 'en',
        status: 'draft',
        version: 1,
        seoMetaTitle: params.seo?.metaTitle,
        seoMetaDescription: params.seo?.metaDescription,
        seoKeywords: params.seo?.keywords,
        seoOgImage: params.seo?.ogImage,
        seoCanonicalUrl: params.seo?.canonicalUrl,
        customFields: params.customFields,
      },
    });

    // Add tags
    if (params.tags && params.tags.length > 0) {
      await this.addTagsToArticle(article.id, params.tags);
    }

    // Update category count
    await this.updateCategoryCount(params.categoryId);

    return article;
  }

  /**
   * Update article
   */
  async updateArticle(
    articleId: string,
    updates: Partial<Omit<Article, 'id' | 'createdAt' | 'updatedAt' | 'version'>>,
    createVersion: boolean = true
  ): Promise<Article> {
    const existing = await this.prisma.kbArticle.findUnique({
      where: { id: articleId },
    });

    if (!existing) {
      throw new Error('Article not found');
    }

    // Create version if requested
    if (createVersion) {
      await this.createArticleVersion(existing.id, existing.version);
    }

    // Update article
    const updated = await this.prisma.kbArticle.update({
      where: { id: articleId },
      data: {
        ...updates,
        version: existing.version + 1,
        updatedAt: new Date(),
        // Update published date if publishing
        publishedAt: updates.status === 'published' && existing.status !== 'published'
          ? new Date()
          : existing.publishedAt,
      },
    });

    // Update tags if provided
    if (updates.tags) {
      await this.updateArticleTags(articleId, updates.tags);
    }

    // Update category count if changed
    if (updates.categoryId && updates.categoryId !== existing.categoryId) {
      await this.updateCategoryCount(updates.categoryId);
      await this.updateCategoryCount(existing.categoryId);
    }

    return updated;
  }

  /**
   * Delete article
   */
  async deleteArticle(articleId: string): Promise<void> {
    const article = await this.prisma.kbArticle.findUnique({
      where: { id: articleId },
    });

    if (!article) {
      throw new Error('Article not found');
    }

    await this.prisma.kbArticle.delete({
      where: { id: articleId },
    });

    // Update category count
    await this.updateCategoryCount(article.categoryId);
  }

  /**
   * Publish article
   */
  async publishArticle(articleId: string): Promise<Article> {
    return await this.updateArticle(articleId, {
      status: 'published',
      publishedAt: new Date(),
    });
  }

  /**
   * Unpublish article
   */
  async unpublishArticle(articleId: string): Promise<Article> {
    return await this.updateArticle(articleId, {
      status: 'draft',
    });
  }

  /**
   * Archive article
   */
  async archiveArticle(articleId: string): Promise<Article> {
    return await this.updateArticle(articleId, {
      status: 'archived',
    });
  }

  /**
   * Get article by ID
   */
  async getArticle(articleId: string): Promise<Article | null> {
    return await this.prisma.kbArticle.findUnique({
      where: { id: articleId },
      include: {
        category: true,
        tags: true,
        author: true,
      },
    });
  }

  /**
   * Get article by slug
   */
  async getArticleBySlug(slug: string, language: string = 'en'): Promise<Article | null> {
    return await this.prisma.kbArticle.findUnique({
      where: {
        slug_language: {
          slug,
          language,
        },
      },
      include: {
        category: true,
        tags: true,
        author: true,
      },
    });
  }

  /**
   * List articles
   */
  async listArticles(params: {
    status?: Article['status'][];
    categoryId?: string;
    tagId?: string;
    language?: string;
    authorId?: string;
    search?: string;
    page?: number;
    limit?: number;
    sortBy?: 'createdAt' | 'publishedAt' | 'title' | 'views';
    sortOrder?: 'asc' | 'desc';
  }): Promise<{
    articles: Article[];
    total: number;
    page: number;
    totalPages: number;
  }> {
    const where: any = {};

    if (params.status) {
      where.status = params.status;
    }

    if (params.categoryId) {
      where.categoryId = params.categoryId;
    }

    if (params.tagId) {
      where.tags = {
        some: { id: params.tagId },
      };
    }

    if (params.language) {
      where.language = params.language;
    }

    if (params.authorId) {
      where.authorId = params.authorId;
    }

    if (params.search) {
      where.OR = [
        { title: { contains: params.search, mode: 'insensitive' } },
        { content: { contains: params.search, mode: 'insensitive' } },
      ];
    }

    const page = params.page || 1;
    const limit = params.limit || 20;
    const skip = (page - 1) * limit;

    const orderBy: any = {};
    const sortBy = params.sortBy || 'createdAt';
    const sortOrder = params.sortOrder || 'desc';
    orderBy[sortBy] = sortOrder;

    const [articles, total] = await Promise.all([
      this.prisma.kbArticle.findMany({
        where,
        include: {
          category: true,
          tags: true,
        },
        orderBy,
        skip,
        take: limit,
      }),
      this.prisma.kbArticle.count({ where }),
    ]);

    return {
      articles,
      total,
      page,
      totalPages: Math.ceil(total / limit),
    };
  }

  /**
   * Generate slug from title
   */
  private generateSlug(title: string): string {
    let slug = title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');

    // Ensure uniqueness
    let counter = 1;
    let uniqueSlug = slug;

    while (true) {
      const existing = await this.prisma.kbArticle.findUnique({
        where: { slug: uniqueSlug },
      });

      if (!existing) {
        break;
      }

      uniqueSlug = `${slug}-${counter}`;
      counter++;
    }

    return uniqueSlug;
  }

  /**
   * Create article version
   */
  private async createArticleVersion(articleId: string, currentVersion: number): Promise<void> {
    const article = await this.prisma.kbArticle.findUnique({
      where: { id: articleId },
    });

    if (!article) return;

    await this.prisma.kbArticleVersion.create({
      data: {
        articleId,
        version: currentVersion,
        title: article.title,
        content: article.content,
        createdBy: article.authorId,
        changeLog: `Version ${currentVersion}`,
      },
    });
  }

  /**
   * Add tags to article
   */
  private async addTagsToArticle(articleId: string, tagNames: string[]): Promise<void> {
    for (const tagName of tagNames) {
      const tag = await this.getOrCreateTag(tagName);
      await this.prisma.kbArticleTag.create({
        data: {
          articleId,
          tagId: tag.id,
        },
      });
    }
  }

  /**
   * Update article tags
   */
  private async updateArticleTags(articleId: string, tagNames: string[]): Promise<void> {
    // Remove existing tags
    await this.prisma.kbArticleTag.deleteMany({
      where: { articleId },
    });

    // Add new tags
    await this.addTagsToArticle(articleId, tagNames);
  }

  /**
   * Get or create tag
   */
  private async getOrCreateTag(name: string): Promise<any> {
    const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-');

    let tag = await this.prisma.kbTag.findUnique({
      where: { slug },
    });

    if (!tag) {
      tag = await this.prisma.kbTag.create({
        data: {
          name,
          slug,
          articleCount: 0,
        },
      });
    }

    return tag;
  }

  /**
   * Update category count
   */
  private async updateCategoryCount(categoryId: string): Promise<void> {
    const count = await this.prisma.kbArticle.count({
      where: { categoryId },
    });

    await this.prisma.kbCategory.update({
      where: { id: categoryId },
      data: { articleCount: count },
    });
  }
}
```

---

## Categories and Tags

### Category Management

```typescript
class CategoryManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create category
   */
  async createCategory(params: {
    name: string;
    description?: string;
    parentId?: string;
    icon?: string;
    order?: number;
    language?: string;
  }): Promise<Category> {
    const slug = this.generateSlug(params.name);

    const category = await this.prisma.kbCategory.create({
      data: {
        name: params.name,
        slug,
        description: params.description,
        parentId: params.parentId,
        icon: params.icon,
        order: params.order || 0,
        language: params.language || 'en',
      },
    });

    return category;
  }

  /**
   * Update category
   */
  async updateCategory(
    categoryId: string,
    updates: Partial<Omit<Category, 'id' | 'createdAt' | 'updatedAt' | 'articleCount'>>
  ): Promise<Category> {
    return await this.prisma.kbCategory.update({
      where: { id: categoryId },
      data: updates,
    });
  }

  /**
   * Delete category
   */
  async deleteCategory(categoryId: string): Promise<void> {
    await this.prisma.kbCategory.delete({
      where: { id: categoryId },
    });
  }

  /**
   * Get category tree
   */
  async getCategoryTree(language: string = 'en'): Promise<CategoryNode[]> {
    const categories = await this.prisma.kbCategory.findMany({
      where: { language },
      orderBy: { order: 'asc' },
    });

    return this.buildTree(categories);
  }

  /**
   * Build tree structure
   */
  private buildTree(categories: Category[]): CategoryNode[] {
    const categoryMap = new Map<string, CategoryNode>();
    const roots: CategoryNode[] = [];

    // Create nodes
    for (const category of categories) {
      categoryMap.set(category.id, {
        ...category,
        children: [],
      });
    }

    // Build tree
    for (const category of categories) {
      const node = categoryMap.get(category.id)!;

      if (category.parentId) {
        const parent = categoryMap.get(category.parentId);
        if (parent) {
          parent.children.push(node);
        }
      } else {
        roots.push(node);
      }
    }

    return roots;
  }

  /**
   * Generate slug
   */
  private generateSlug(name: string): string {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-');
  }
}

interface CategoryNode extends Category {
  children: CategoryNode[];
}
```

### Tag Management

```typescript
class TagManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create tag
   */
  async createTag(params: {
    name: string;
    color?: string;
  }): Promise<Tag> {
    const slug = params.name.toLowerCase().replace(/[^a-z0-9]+/g, '-');

    return await this.prisma.kbTag.create({
      data: {
        name: params.name,
        slug,
        color: params.color,
      },
    });
  }

  /**
   * Update tag
   */
  async updateTag(
    tagId: string,
    updates: Partial<Omit<Tag, 'id' | 'articleCount' | 'createdAt'>>
  ): Promise<Tag> {
    return await this.prisma.kbTag.update({
      where: { id: tagId },
      data: updates,
    });
  }

  /**
   * Delete tag
   */
  async deleteTag(tagId: string): Promise<void> {
    await this.prisma.kbTag.delete({
      where: { id: tagId },
    });
  }

  /**
   * Get all tags
   */
  async getAllTags(): Promise<Tag[]> {
    return await this.prisma.kbTag.findMany({
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Get popular tags
   */
  async getPopularTags(limit: number = 20): Promise<Tag[]> {
    return await this.prisma.kbTag.findMany({
      orderBy: { articleCount: 'desc' },
      take: limit,
    });
  }
}
```

---

## Search Functionality

### Full-Text Search

```typescript
class ArticleSearch {
  constructor(private prisma: PrismaClient) {}

  /**
   * Search articles
   */
  async search(params: {
    query: string;
    categoryId?: string;
    tagId?: string;
    language?: string;
    page?: number;
    limit?: number;
  }): Promise<{
    articles: Article[];
    total: number;
    page: number;
    totalPages: number;
  }> {
    const where: any = {
      status: 'published',
    };

    // Text search
    if (params.query) {
      where.OR = [
        { title: { contains: params.query, mode: 'insensitive' } },
        { content: { contains: params.query, mode: 'insensitive' } },
        { excerpt: { contains: params.query, mode: 'insensitive' } },
      ];
    }

    // Category filter
    if (params.categoryId) {
      where.categoryId = params.categoryId;
    }

    // Tag filter
    if (params.tagId) {
      where.tags = {
        some: { id: params.tagId },
      };
    }

    // Language filter
    if (params.language) {
      where.language = params.language;
    }

    const page = params.page || 1;
    const limit = params.limit || 20;
    const skip = (page - 1) * limit;

    const [articles, total] = await Promise.all([
      this.prisma.kbArticle.findMany({
        where,
        include: {
          category: true,
          tags: true,
        },
        orderBy: { publishedAt: 'desc' },
        skip,
        take: limit,
      }),
      this.prisma.kbArticle.count({ where }),
    ]);

    return {
      articles,
      total,
      page,
      totalPages: Math.ceil(total / limit),
    };
  }

  /**
   * Get search suggestions
   */
  async getSuggestions(
    query: string,
    language: string = 'en',
    limit: number = 10
  ): Promise<Array<{
    id: string;
    title: string;
    slug: string;
    category: string;
  }>> {
    const articles = await this.prisma.kbArticle.findMany({
      where: {
        status: 'published',
        language,
        title: { contains: query, mode: 'insensitive' },
      },
      select: {
        id: true,
        title: true,
        slug: true,
        category: {
          select: { name: true },
        },
      },
      take: limit,
      orderBy: { publishedAt: 'desc' },
    });

    return articles.map(a => ({
      id: a.id,
      title: a.title,
      slug: a.slug,
      category: a.category?.name || '',
    }));
  }
}
```

### Semantic Search with Embeddings

```typescript
// npm install @pinecone-database/pinecone openai
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';

class SemanticSearch {
  private pinecone: Pinecone;
  private openai: OpenAI;

  constructor() {
    this.pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! });
    this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });
  }

  /**
   * Index article
   */
  async indexArticle(article: Article): Promise<void> {
    // Generate embedding
    const embedding = await this.generateEmbedding(
      `${article.title} ${article.excerpt || ''}`
    );

    // Store in Pinecone
    const index = this.pinecone.index(process.env.PINECONE_INDEX!);
    await index.upsert([
      {
        id: article.id,
        values: embedding,
        metadata: {
          title: article.title,
          slug: article.slug,
          categoryId: article.categoryId,
          language: article.language,
        },
      },
    ]);
  }

  /**
   * Search articles
   */
  async search(
    query: string,
    filters?: {
      categoryId?: string;
      language?: string;
    },
    limit: number = 10
  ): Promise<Array<{
    articleId: string;
    score: number;
    metadata: any;
  }>> {
    // Generate query embedding
    const queryEmbedding = await this.generateEmbedding(query);

    // Search in Pinecone
    const index = this.pinecone.index(process.env.PINECONE_INDEX!);
    const results = await index.query({
      vector: queryEmbedding,
      topK: limit,
      includeMetadata: true,
      filter: {
        ...filters?.language && { language: { $eq: filters.language } },
        ...filters?.categoryId && { categoryId: { $eq: filters.categoryId } },
      },
    });

    return results.matches.map((match: any) => ({
      articleId: match.id,
      score: match.score,
      metadata: match.metadata,
    }));
  }

  /**
   * Generate embedding
   */
  private async generateEmbedding(text: string): Promise<number[]> {
    const response = await this.openai.embeddings.create({
      model: 'text-embedding-ada-002',
      input: text,
    });

    return response.data[0].embedding;
  }
}
```

---

## Article Templates

### Template System

```typescript
interface ArticleTemplate {
  id: string;
  name: string;
  description: string;
  content: string;
  variables: TemplateVariable[];
  categoryId?: string;
  tags?: string[];
  isDefault: boolean;
}

interface TemplateVariable {
  name: string;
  type: 'text' | 'number' | 'date' | 'select';
  required: boolean;
  options?: string[];
  defaultValue?: any;
}

class TemplateManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create template
   */
  async createTemplate(template: Omit<ArticleTemplate, 'id'>): Promise<string> {
    const created = await this.prisma.kbArticleTemplate.create({
      data: template,
    });

    return created.id;
  }

  /**
   * Get template
   */
  async getTemplate(templateId: string): Promise<ArticleTemplate | null> {
    return await this.prisma.kbArticleTemplate.findUnique({
      where: { id: templateId },
    });
  }

  /**
   * List templates
   */
  async listTemplates(): Promise<ArticleTemplate[]> {
    return await this.prisma.kbArticleTemplate.findMany({
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Render template with variables
   */
  renderTemplate(template: ArticleTemplate, variables: Record<string, any>): string {
    let content = template.content;

    for (const variable of template.variables) {
      const value = variables[variable.name] ?? variable.defaultValue;
      content = content.replace(new RegExp(`{{${variable.name}}}`, 'g'), String(value));
    }

    return content;
  }

  /**
   * Create article from template
   */
  async createFromTemplate(
    templateId: string,
    variables: Record<string, any>,
    params: {
      title: string;
      authorId: string;
      categoryId: string;
      tags?: string[];
    }
  ): Promise<Article> {
    const template = await this.getTemplate(templateId);
    if (!template) {
      throw new Error('Template not found');
    }

    const content = this.renderTemplate(template, variables);
    const excerpt = content.substring(0, 200) + '...';

    const articleManager = new ArticleManager(this.prisma);
    return await articleManager.createArticle({
      ...params,
      content,
      excerpt,
    });
  }
}
```

---

## Rich Content Editor

### Editor Configuration

```typescript
// npm install @tiptap/react @tiptap/starter-kit
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';

const ArticleEditor: React.FC<{
  content: string;
  onChange: (content: string) => void;
}> = ({ content, onChange }) => {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Image,
      Link,
      Table,
      TableHeader,
      TableCell,
      TableRow,
      CodeBlockLowlight,
      Placeholder,
    ],
    content,
    onUpdate: ({ editor }) => {
      onChange(editor.getHTML());
    },
  });

  return (
    <div className="editor-container">
      <div className="editor-toolbar">
        <button
          onClick={() => editor.chain().focus().toggleBold().run()}
          className={editor.isActive('bold') ? 'is-active' : ''}
        >
          Bold
        </button>
        <button
          onClick={() => editor.chain().focus().toggleItalic().run()}
          className={editor.isActive('italic') ? 'is-active' : ''}
        >
          Italic
        </button>
        <button
          onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
          className={editor.isActive('heading', { level: 1 }) ? 'is-active' : ''}
        >
          H1
        </button>
        <button
          onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
          className={editor.isActive('heading', { level: 2 }) ? 'is-active' : ''}
        >
          H2
        </button>
        <button
          onClick={() => editor.chain().focus().toggleBulletList().run()}
          className={editor.isActive('bulletList') ? 'is-active' : ''}
        >
          Bullet List
        </button>
        <button
          onClick={() => editor.chain().focus().toggleCodeBlock().run()}
          className={editor.isActive('codeBlock') ? 'is-active' : ''}
        >
          Code Block
        </button>
        <button onClick={() => editor.chain().focus().unsetAllMarks().run()}>
          Clear Formatting
        </button>
      </div>

      <EditorContent editor={editor} className="editor-content" />
    </div>
  );
};
```

---

## Media Management

### Media Upload

```typescript
import multer from 'multer';
import path from 'path';

// Configure multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = path.join(process.cwd(), 'uploads', 'kb');
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  },
});

const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  },
});

// Express route for media upload
app.post('/api/kb/media/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    // Get image dimensions
    const dimensions = await getImageDimensions(req.file.path);

    // Store in database
    const media = await prisma.kbMedia.create({
      data: {
        articleId: req.body.articleId,
        fileName: req.file.originalname,
        fileUrl: `/uploads/kb/${req.file.filename}`,
        fileSize: req.file.size,
        mimeType: req.file.mimetype,
        width: dimensions.width,
        height: dimensions.height,
        altText: req.body.altText,
        uploadedBy: req.user.id,
      },
    });

    res.json({
      id: media.id,
      url: media.fileUrl,
      fileName: media.fileName,
      width: media.width,
      height: media.height,
    });
  } catch (error) {
    console.error('Error uploading media:', error);
    res.status(500).json({ error: 'Failed to upload media' });
  }
});

// Get image dimensions
async function getImageDimensions(filePath: string): Promise<{
  width: number;
  height: number;
}> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      resolve({ width: image.width, height: image.height });
    };
    image.onerror = () => {
      reject(new Error('Failed to load image'));
    };
    image.src = filePath;
  });
}
```

---

## Analytics

### Article Analytics

```typescript
class ArticleAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Track article view
   */
  async trackView(params: {
    articleId: string;
    userId?: string;
    sessionId: string;
    ipAddress?: string;
    userAgent?: string;
  }): Promise<void> {
    await this.prisma.kbArticleView.create({
      data: {
        articleId: params.articleId,
        userId: params.userId,
        sessionId: params.sessionId,
        ipAddress: params.ipAddress,
        userAgent: params.userAgent,
      },
    });

    // Update article view count
    await this.prisma.kbArticle.update({
      where: { id: params.articleId },
      data: { viewCount: { increment: 1 } },
    });
  }

  /**
   * Track helpful feedback
   */
  async trackFeedback(params: {
    articleId: string;
    userId?: string;
    helpful: boolean;
    comment?: string;
  }): Promise<void> {
    await this.prisma.kbArticleFeedback.create({
      data: {
        articleId: params.articleId,
        userId: params.userId,
        helpful: params.helpful,
        comment: params.comment,
      },
    });
  }

  /**
   * Get article statistics
   */
  async getArticleStats(articleId: string): Promise<{
    views: number;
    helpful: number;
    notHelpful: number;
    helpfulPercentage: number;
  }> {
    const [views, feedback] = await Promise.all([
      this.prisma.kbArticleView.count({
        where: { articleId },
      }),
      this.prisma.kbArticleFeedback.groupBy({
        by: ['helpful'],
        where: { articleId },
        _count: true,
      }),
    ]);

    const helpfulCount = feedback.find(f => f.helpful === true)?._count || 0;
    const notHelpfulCount = feedback.find(f => f.helpful === false)?._count || 0;
    const totalFeedback = helpfulCount + notHelpfulCount;
    const helpfulPercentage = totalFeedback > 0
      ? (helpfulCount / totalFeedback) * 100
      : 0;

    return {
      views,
      helpful: helpfulCount,
      notHelpful: notHelpfulCount,
      helpfulPercentage,
    };
  }

  /**
   * Get popular articles
   */
  async getPopularArticles(params: {
    categoryId?: string;
    language?: string;
    limit?: number;
    days?: number;
  }): Promise<Article[]> {
    const where: any = {
      status: 'published',
    };

    if (params.categoryId) {
      where.categoryId = params.categoryId;
    }

    if (params.language) {
      where.language = params.language;
    }

    if (params.days) {
      where.publishedAt = {
        gte: new Date(Date.now() - params.days * 24 * 60 * 60 * 1000),
      };
    }

    return await this.prisma.kbArticle.findMany({
      where,
      include: {
        category: true,
        tags: true,
      },
      orderBy: { viewCount: 'desc' },
      take: params.limit || 10,
    });
  }

  /**
   * Get trending articles
   */
  async getTrendingArticles(params: {
    categoryId?: string;
    language?: string;
    limit?: number;
    days?: number;
  }): Promise<Article[]> {
    const startDate = new Date(Date.now() - (params.days || 7) * 24 * 60 * 60 * 1000);

    const articleIds = await this.prisma.kbArticleView.groupBy({
      by: ['articleId'],
      where: {
        viewedAt: { gte: startDate },
      },
      _count: true,
      orderBy: {
        _count: 'desc',
      },
      take: params.limit || 10,
    });

    const ids = articleIds.map((a: any) => a.articleId);

    return await this.prisma.kbArticle.findMany({
      where: {
        id: { in: ids },
        status: 'published',
        ...params.categoryId && { categoryId: params.categoryId },
        ...params.language && { language: params.language },
      },
      include: {
        category: true,
        tags: true,
      },
    });
  }
}
```

---

## Related Articles

### Related Articles Algorithm

```typescript
class RelatedArticles {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get related articles
   */
  async getRelatedArticles(articleId: string, limit: number = 5): Promise<Article[]> {
    const article = await this.prisma.kbArticle.findUnique({
      where: { id: articleId },
      include: {
        category: true,
        tags: true,
      },
    });

    if (!article) {
      return [];
    }

    // Get articles in same category
    const categoryArticles = await this.prisma.kbArticle.findMany({
      where: {
        id: { not: articleId },
        categoryId: article.categoryId,
        status: 'published',
        language: article.language,
      },
      include: {
        tags: true,
      },
      take: limit * 2,
    });

    // Score articles based on tag overlap
    const scored = categoryArticles.map(a => ({
      article: a,
      score: this.calculateScore(article, a),
    }));

    // Sort by score and take top results
    scored.sort((a, b) => b.score - a.score);

    return scored.slice(0, limit).map(s => s.article);
  }

  /**
   * Calculate relatedness score
   */
  private calculateScore(article1: Article, article2: Article): number {
    let score = 0;

    // Tag overlap
    const tags1 = new Set(article1.tags.map((t: any) => t.name));
    const tags2 = new Set(article2.tags.map((t: any) => t.name));
    const intersection = new Set([...tags1].filter(x => tags2.has(x)));
    const union = new Set([...tags1, ...tags2]);

    if (union.size > 0) {
      score += (intersection.size / union.size) * 50;
    }

    // Same category
    if (article1.categoryId === article2.categoryId) {
      score += 30;
    }

    // Title similarity (simple)
    const title1Words = article1.title.toLowerCase().split(/\s+/);
    const title2Words = article2.title.toLowerCase().split(/\s+/);
    const titleIntersection = title1Words.filter(w => title2Words.includes(w));

    if (title1Words.length > 0) {
      score += (titleIntersection.length / title1Words.length) * 20;
    }

    return score;
  }
}
```

---

## SEO Optimization

### SEO Manager

```typescript
class SEOManager {
  /**
   * Generate meta title
   */
  static generateMetaTitle(title: string, maxLength: number = 60): string {
    if (title.length <= maxLength) {
      return title;
    }

    return title.substring(0, maxLength - 3) + '...';
  }

  /**
   * Generate meta description
   */
  static generateMetaDescription(content: string, maxLength: number = 160): string {
    // Strip HTML tags
    const text = content.replace(/<[^>]*>/g, ' ');
    // Remove extra whitespace
    const cleaned = text.replace(/\s+/g, ' ').trim();

    if (cleaned.length <= maxLength) {
      return cleaned;
    }

    return cleaned.substring(0, maxLength - 3) + '...';
  }

  /**
   * Generate keywords
   */
  static generateKeywords(title: string, content: string): string[] {
    const text = `${title} ${content}`.toLowerCase();
    const words = text.match(/\b[a-z]{3,}\b/g) || [];

    // Count word frequency
    const frequency = new Map<string, number>();
    for (const word of words) {
      frequency.set(word, (frequency.get(word) || 0) + 1);
    }

    // Sort by frequency and get top keywords
    const sorted = Array.from(frequency.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);

    return sorted;
  }

  /**
   * Generate Open Graph tags
   */
  static generateOpenGraph(article: Article, baseUrl: string): string {
    const ogImage = article.seo?.ogImage || `${baseUrl}/default-og-image.jpg`;
    const ogTitle = article.seo?.metaTitle || article.title;
    const ogDescription = article.seo?.metaDescription || article.excerpt;

    return `
    <meta property="og:title" content="${this.escapeHtml(ogTitle)}">
    <meta property="og:description" content="${this.escapeHtml(ogDescription)}">
    <meta property="og:image" content="${ogImage}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="${baseUrl}/kb/${article.slug}">
    <meta property="og:site_name" content="Knowledge Base">
    `.trim();
  }

  /**
   * Generate structured data
   */
  static generateStructuredData(article: Article, baseUrl: string): string {
    return `
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "${this.escapeHtml(article.title)}",
      "description": "${this.escapeHtml(article.excerpt || '')}",
      "author": {
        "@type": "Person",
        "name": "${this.escapeHtml(article.author?.name || '')}"
      },
      "datePublished": "${article.publishedAt?.toISOString() || ''}",
      "dateModified": "${article.updatedAt.toISOString()}",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "${baseUrl}/kb/${article.slug}"
      }
    }
    </script>
    `.trim();
  }

  /**
   * Generate canonical URL
   */
  static generateCanonicalUrl(article: Article, baseUrl: string): string {
    return `${baseUrl}/kb/${article.slug}`;
  }

  private static escapeHtml(text: string): string {
    const map: Record<string, string> = {
      '&': '&',
      '<': '<',
      '>': '>',
      '"': '"',
      "'": '&#039;',
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }
}
```

---

## Multi-Language Support

### Translation Manager

```typescript
interface Translation {
  id: string;
  articleId: string;
  language: string;
  title: string;
  content: string;
  excerpt?: string;
  slug: string;
  translatedBy: string;
  translatedAt: Date;
  status: 'draft' | 'published';
}

class TranslationManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create translation
   */
  async createTranslation(params: {
    articleId: string;
    language: string;
    title: string;
    content: string;
    excerpt?: string;
    translatedBy: string;
  }): Promise<Translation> {
    const originalArticle = await this.prisma.kbArticle.findUnique({
      where: { id: params.articleId },
    });

    if (!originalArticle) {
      throw new Error('Original article not found');
    }

    // Generate slug for translation
    const slug = `${originalArticle.slug}-${params.language}`;

    return await this.prisma.kbArticle.create({
      data: {
        title: params.title,
        slug,
        content: params.content,
        excerpt: params.excerpt,
        categoryId: originalArticle.categoryId,
        authorId: params.translatedBy,
        language: params.language,
        status: 'draft',
        customFields: {
          translationOf: params.articleId,
        },
      },
    });
  }

  /**
   * Get available languages for article
   */
  async getAvailableLanguages(articleId: string): Promise<string[]> {
    const article = await this.prisma.kbArticle.findUnique({
      where: { id: articleId },
    });

    if (!article) {
      return [];
    }

    // Get translations
    const translations = await this.prisma.kbArticle.findMany({
      where: {
        customFields: {
          path: ['translationOf'],
          equals: articleId,
        },
        status: 'published',
      },
      select: { language: true },
    });

    return [article.language, ...translations.map(t => t.language)];
  }

  /**
   * Auto-translate using translation service
   */
  async autoTranslate(
    articleId: string,
    targetLanguages: string[]
  ): Promise<Translation[]> {
    const article = await this.prisma.kbArticle.findUnique({
      where: { id: articleId },
    });

    if (!article) {
      throw new Error('Article not found');
    }

    const translations: Translation[] = [];

    for (const language of targetLanguages) {
      // Translate using translation service
      const translated = await this.translateText(article.content, language);
      const translatedTitle = await this.translateText(article.title, language);

      // Create translation
      const translation = await this.createTranslation({
        articleId,
        language,
        title: translatedTitle,
        content: translated,
        excerpt: article.excerpt,
        translatedBy: 'system',
      });

      translations.push(translation);
    }

    return translations;
  }

  /**
   * Translate text
   */
  private async translateText(text: string, targetLanguage: string): Promise<string> {
    // Implement translation service integration
    // Example: Google Translate, DeepL, etc.
    return text; // Placeholder
  }
}
```

---

## Best Practices

### Knowledge Base Best Practices

```typescript
// 1. Use clear, concise titles
function validateTitle(title: string): {
  valid: boolean;
  warnings: string[];
} {
  const warnings: string[] = [];

  if (title.length < 10) {
    warnings.push('Title is too short (minimum 10 characters)');
  }

  if (title.length > 100) {
    warnings.push('Title is too long (maximum 100 characters)');
  }

  if (!/[A-Z]/.test(title)) {
    warnings.push('Title should start with a capital letter');
  }

  return {
    valid: warnings.length === 0,
    warnings,
  };
}

// 2. Use consistent formatting
function formatArticleContent(content: string): string {
  // Ensure consistent heading structure
  // Use proper paragraph breaks
  // Add code blocks for technical content
  return content;
}

// 3. Include examples and screenshots
function enrichArticle(article: Article): Article {
  // Add code examples
  // Add screenshots
  // Add step-by-step instructions
  return article;
}

// 4. Keep content up to date
async function reviewOutdatedArticles(): Promise<void> {
  const threeMonthsAgo = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000);

  const outdatedArticles = await prisma.kbArticle.findMany({
    where: {
      status: 'published',
      updatedAt: { lt: threeMonthsAgo },
    },
  });

  for (const article of outdatedArticles) {
    // Send review notification
    await notifyAuthorForReview(article.id);
  }
}

// 5. Use categories effectively
function organizeCategories(articles: Article[]): CategoryTree[] {
  // Group articles by category
  // Create logical hierarchy
  // Limit depth to 3 levels
  return [];
}
```

---

---

## Quick Start

### Basic Knowledge Base

```typescript
interface Article {
  id: string
  title: string
  content: string
  category: string
  tags: string[]
  published: boolean
}

async function createArticle(article: Article) {
  return await db.articles.create({
    data: {
      ...article,
      slug: slugify(article.title),
      searchVector: generateSearchVector(article.content)
    }
  })
}

async function searchArticles(query: string) {
  return await db.articles.findMany({
    where: {
      OR: [
        { title: { contains: query, mode: 'insensitive' } },
        { content: { contains: query, mode: 'insensitive' } },
        { tags: { has: query } }
      ],
      published: true
    },
    orderBy: { relevance: 'desc' }
  })
}
```

---

## Production Checklist

- [ ] **Article Management**: Create, edit, delete articles
- [ ] **Categories**: Organize articles by categories
- [ ] **Tags**: Tag articles for better discovery
- [ ] **Search**: Full-text search functionality
- [ ] **Rich Content**: Rich text editor for content
- [ ] **Media**: Image and video support
- [ ] **SEO**: SEO optimization for articles
- [ ] **Analytics**: Track article views and searches
- [ ] **Related Articles**: Suggest related articles
- [ ] **Multi-language**: Support multiple languages
- [ ] **Access Control**: Permissions for editing
- [ ] **Versioning**: Article version history

---

## Anti-patterns

### ❌ Don't: Poor Search

```typescript
// ❌ Bad - Simple LIKE query
const articles = await db.articles.findMany({
  where: { content: { contains: query } }  // Slow, no ranking
})
```

```typescript
// ✅ Good - Full-text search with ranking
const articles = await db.$queryRaw`
  SELECT *, ts_rank(search_vector, plainto_tsquery(${query})) as rank
  FROM articles
  WHERE search_vector @@ plainto_tsquery(${query})
  ORDER BY rank DESC
`
```

### ❌ Don't: No Organization

```markdown
# ❌ Bad - Flat structure
- Article 1
- Article 2
- Article 3
# ... 1000 articles
```

```markdown
# ✅ Good - Organized
## Getting Started
- Article 1
- Article 2
## Troubleshooting
- Article 3
- Article 4
```

---

## Integration Points

- **Live Chat** (`29-customer-support/live-chat/`) - Link to articles
- **Search** (`20-ai-integration/ai-search/`) - Advanced search
- **Content Management** (`33-content-management/`) - Content patterns

---

## Further Reading

- [Tiptap Editor](https://tiptap.dev/)
- [Pinecone Vector Database](https://www.pinecone.io/)
- [Knowledge Base Best Practices](https://www.zendesk.com/blog/knowledge-base-best-practices/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Prisma Documentation](https://www.prisma.io/docs/)
