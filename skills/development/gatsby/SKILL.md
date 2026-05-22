---
name: gatsby
description: Builds static and hybrid sites with Gatsby, React, and GraphQL data layer. Use when creating content-heavy websites, blogs, e-commerce storefronts, or when user mentions Gatsby, static site generation with React, or GraphQL-powered sites.
---

# Gatsby

React-based framework for building fast, static and dynamic websites with a unified GraphQL data layer.

## Quick Start

```bash
# Create new project
npm init gatsby my-site
cd my-site
npm run develop

# Or with specific options
npm init gatsby -- -y my-site
```

## Project Structure

```
my-site/
  gatsby-config.js      # Site configuration & plugins
  gatsby-node.js        # Node APIs (page creation)
  gatsby-browser.js     # Browser APIs
  gatsby-ssr.js         # SSR APIs
  src/
    pages/              # File-based routing
      index.js          # -> /
      about.js          # -> /about
      blog/{slug}.js    # -> /blog/:slug (DSG)
    components/         # Reusable components
    templates/          # Page templates
    images/             # Static images
  static/               # Unprocessed assets
```

## Pages

### Basic Page

```jsx
// src/pages/index.js
import * as React from "react"
import { Link } from "gatsby"
import Layout from "../components/layout"

export default function HomePage() {
  return (
    <Layout>
      <h1>Welcome to My Site</h1>
      <Link to="/about">About</Link>
    </Layout>
  )
}

// Head API for SEO
export const Head = () => (
  <>
    <title>Home | My Site</title>
    <meta name="description" content="Welcome to my Gatsby site" />
  </>
)
```

### Dynamic Routes (File System Route API)

```jsx
// src/pages/products/{Product.slug}.js
import * as React from "react"
import { graphql } from "gatsby"

export default function ProductPage({ data }) {
  const product = data.product
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span>${product.price}</span>
    </div>
  )
}

export const query = graphql`
  query ($id: String!) {
    product(id: { eq: $id }) {
      name
      description
      price
      slug
    }
  }
`

export const Head = ({ data }) => <title>{data.product.name}</title>
```

## GraphQL Data Layer

### Page Queries

```jsx
// src/pages/blog.js
import * as React from "react"
import { graphql, Link } from "gatsby"

export default function BlogPage({ data }) {
  return (
    <div>
      <h1>Blog Posts</h1>
      <ul>
        {data.allMarkdownRemark.nodes.map((post) => (
          <li key={post.id}>
            <Link to={post.fields.slug}>
              <h2>{post.frontmatter.title}</h2>
              <p>{post.excerpt}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

// Query runs at build time
export const query = graphql`
  query {
    allMarkdownRemark(sort: { frontmatter: { date: DESC } }) {
      nodes {
        id
        excerpt(pruneLength: 200)
        fields {
          slug
        }
        frontmatter {
          title
          date(formatString: "MMMM DD, YYYY")
        }
      }
    }
  }
`
```

### useStaticQuery (Component Queries)

```jsx
// src/components/seo.js
import * as React from "react"
import { useStaticQuery, graphql } from "gatsby"

export function SEO({ title, description, children }) {
  const { site } = useStaticQuery(graphql`
    query {
      site {
        siteMetadata {
          title
          description
          siteUrl
        }
      }
    }
  `)

  const seo = {
    title: title || site.siteMetadata.title,
    description: description || site.siteMetadata.description,
  }

  return (
    <>
      <title>{seo.title}</title>
      <meta name="description" content={seo.description} />
      <meta property="og:title" content={seo.title} />
      <meta property="og:description" content={seo.description} />
      {children}
    </>
  )
}
```

### Custom Hook Pattern

```jsx
// src/hooks/use-site-metadata.js
import { useStaticQuery, graphql } from "gatsby"

export function useSiteMetadata() {
  const data = useStaticQuery(graphql`
    query {
      site {
        siteMetadata {
          title
          description
          siteUrl
          social {
            twitter
          }
        }
      }
    }
  `)
  return data.site.siteMetadata
}

// Usage
import { useSiteMetadata } from "../hooks/use-site-metadata"

function Footer() {
  const { title, social } = useSiteMetadata()
  return <footer>{title} - @{social.twitter}</footer>
}
```

## Configuration

### gatsby-config.js

```javascript
// gatsby-config.js
module.exports = {
  siteMetadata: {
    title: "My Gatsby Site",
    description: "A blazing fast site built with Gatsby",
    siteUrl: "https://example.com",
  },
  plugins: [
    // TypeScript support
    "gatsby-plugin-typescript",

    // Image optimization
    "gatsby-plugin-image",
    "gatsby-plugin-sharp",
    "gatsby-transformer-sharp",

    // Source filesystem
    {
      resolve: "gatsby-source-filesystem",
      options: {
        name: "images",
        path: `${__dirname}/src/images`,
      },
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        name: "posts",
        path: `${__dirname}/content/posts`,
      },
    },

    // Markdown processing
    {
      resolve: "gatsby-transformer-remark",
      options: {
        plugins: [
          "gatsby-remark-prismjs",
          "gatsby-remark-images",
        ],
      },
    },

    // CMS integration
    {
      resolve: "gatsby-source-contentful",
      options: {
        spaceId: process.env.CONTENTFUL_SPACE_ID,
        accessToken: process.env.CONTENTFUL_ACCESS_TOKEN,
      },
    },

    // SEO & Performance
    "gatsby-plugin-sitemap",
    "gatsby-plugin-robots-txt",
    {
      resolve: "gatsby-plugin-manifest",
      options: {
        name: "My Gatsby Site",
        short_name: "Gatsby",
        start_url: "/",
        background_color: "#ffffff",
        theme_color: "#663399",
        display: "standalone",
        icon: "src/images/icon.png",
      },
    },
  ],
}
```

## Rendering Options

### Static Site Generation (SSG) - Default

```jsx
// Pages are statically generated at build time
export default function AboutPage() {
  return <h1>About Us</h1>
}
```

### Deferred Static Generation (DSG)

```jsx
// src/pages/products/{Product.slug}.js
import { graphql } from "gatsby"

export default function ProductPage({ data }) {
  return <div>{data.product.name}</div>
}

export const query = graphql`
  query ($id: String!) {
    product(id: { eq: $id }) {
      name
    }
  }
`

// Defer generation until first request
export async function config() {
  return ({ params }) => ({
    defer: true,
  })
}
```

### Server-Side Rendering (SSR)

```jsx
// src/pages/dashboard.js
import * as React from "react"

export default function DashboardPage({ serverData }) {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>User: {serverData.user.name}</p>
    </div>
  )
}

// Runs on every request
export async function getServerData() {
  const res = await fetch("https://api.example.com/user")
  const user = await res.json()

  return {
    props: { user },
    headers: {
      "Cache-Control": "public, max-age=60",
    },
  }
}
```

## Programmatic Page Creation

```javascript
// gatsby-node.js
const path = require("path")

exports.createPages = async ({ graphql, actions }) => {
  const { createPage } = actions

  const result = await graphql(`
    query {
      allMarkdownRemark {
        nodes {
          id
          fields {
            slug
          }
        }
      }
    }
  `)

  const template = path.resolve("src/templates/blog-post.js")

  result.data.allMarkdownRemark.nodes.forEach((node) => {
    createPage({
      path: `/blog${node.fields.slug}`,
      component: template,
      context: {
        id: node.id,
      },
    })
  })
}

// Add slug field to markdown nodes
exports.onCreateNode = ({ node, actions, getNode }) => {
  const { createNodeField } = actions

  if (node.internal.type === "MarkdownRemark") {
    const slug = createFilePath({ node, getNode })
    createNodeField({
      node,
      name: "slug",
      value: slug,
    })
  }
}
```

## Image Optimization

### Static Images

```jsx
import { StaticImage } from "gatsby-plugin-image"

function Hero() {
  return (
    <StaticImage
      src="../images/hero.jpg"
      alt="Hero image"
      placeholder="blurred"
      layout="fullWidth"
      formats={["auto", "webp", "avif"]}
    />
  )
}
```

### Dynamic Images (GatsbyImage)

```jsx
import { GatsbyImage, getImage } from "gatsby-plugin-image"
import { graphql } from "gatsby"

function ProductCard({ data }) {
  const image = getImage(data.product.image)

  return (
    <GatsbyImage
      image={image}
      alt={data.product.name}
      className="product-image"
    />
  )
}

export const query = graphql`
  query {
    product {
      name
      image {
        childImageSharp {
          gatsbyImageData(
            width: 400
            placeholder: BLURRED
            formats: [AUTO, WEBP, AVIF]
          )
        }
      }
    }
  }
`
```

## Common Plugins

| Plugin | Purpose |
|--------|---------|
| `gatsby-source-filesystem` | Source local files |
| `gatsby-transformer-remark` | Parse Markdown |
| `gatsby-plugin-mdx` | MDX support |
| `gatsby-plugin-image` | Optimized images |
| `gatsby-source-contentful` | Contentful CMS |
| `gatsby-source-sanity` | Sanity CMS |
| `gatsby-source-wordpress` | WordPress |
| `gatsby-plugin-sitemap` | Generate sitemap |
| `gatsby-plugin-google-gtag` | Analytics |

## TypeScript Support

```tsx
// src/pages/index.tsx
import * as React from "react"
import { graphql, PageProps, HeadFC } from "gatsby"

type DataProps = {
  site: {
    siteMetadata: {
      title: string
    }
  }
}

const IndexPage: React.FC<PageProps<DataProps>> = ({ data }) => {
  return <h1>{data.site.siteMetadata.title}</h1>
}

export default IndexPage

export const Head: HeadFC<DataProps> = ({ data }) => (
  <title>{data.site.siteMetadata.title}</title>
)

export const query = graphql`
  query {
    site {
      siteMetadata {
        title
      }
    }
  }
`
```

## Build & Deploy

```bash
# Development
npm run develop          # Start dev server at localhost:8000
npm run develop -- -H 0.0.0.0  # Expose to network

# Production build
npm run build            # Generate static files
npm run serve            # Preview production build

# Clean cache
npm run clean            # Clear .cache and public/
```

## Performance Tips

1. **Use gatsby-plugin-image** for all images
2. **Enable incremental builds** for large sites
3. **Defer low-traffic pages** with DSG
4. **Code-split** heavy components with React.lazy
5. **Preload critical resources** in gatsby-browser.js

## Reference Files

- [graphql-patterns.md](references/graphql-patterns.md) - Advanced GraphQL query patterns
- [plugin-development.md](references/plugin-development.md) - Creating custom plugins
