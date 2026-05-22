---
name: webpack
description: Configures Webpack 5 for JavaScript/TypeScript bundling with loaders, plugins, code splitting, and Module Federation. Use when setting up custom builds, migrating to Webpack 5, or implementing micro-frontends.
---

# Webpack 5

Industry-standard module bundler for JavaScript applications with extensive plugin ecosystem.

## Quick Start

```bash
npm install --save-dev webpack webpack-cli webpack-dev-server

# Create config
touch webpack.config.js

# Run development server
npx webpack serve

# Production build
npx webpack --mode production
```

## Basic Configuration

### webpack.config.js

```javascript
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: 'development', // or 'production'

  entry: './src/index.js',

  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    clean: true,
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
  ],

  devServer: {
    static: './dist',
    port: 3000,
    hot: true,
  },
};
```

## TypeScript Setup

```bash
npm install --save-dev typescript ts-loader
```

```javascript
// webpack.config.js
module.exports = {
  entry: './src/index.ts',

  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },

  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
};
```

## Loaders

### CSS/Sass

```bash
npm install --save-dev css-loader style-loader sass sass-loader postcss-loader
```

```javascript
rules: [
  // CSS
  {
    test: /\.css$/,
    use: ['style-loader', 'css-loader', 'postcss-loader'],
  },

  // CSS Modules
  {
    test: /\.module\.css$/,
    use: [
      'style-loader',
      {
        loader: 'css-loader',
        options: {
          modules: {
            localIdentName: '[name]__[local]--[hash:base64:5]',
          },
        },
      },
    ],
  },

  // Sass
  {
    test: /\.scss$/,
    use: ['style-loader', 'css-loader', 'postcss-loader', 'sass-loader'],
  },
]
```

### Assets

```javascript
rules: [
  // Images
  {
    test: /\.(png|svg|jpg|jpeg|gif)$/i,
    type: 'asset/resource',
  },

  // Fonts
  {
    test: /\.(woff|woff2|eot|ttf|otf)$/i,
    type: 'asset/resource',
  },

  // Inline small assets
  {
    test: /\.svg$/,
    type: 'asset',
    parser: {
      dataUrlCondition: {
        maxSize: 4 * 1024, // 4kb
      },
    },
  },
]
```

### Babel

```javascript
{
  test: /\.(js|jsx)$/,
  exclude: /node_modules/,
  use: {
    loader: 'babel-loader',
    options: {
      presets: [
        ['@babel/preset-env', { targets: 'defaults' }],
        '@babel/preset-react',
      ],
      plugins: ['@babel/plugin-transform-runtime'],
    },
  },
}
```

## Essential Plugins

```bash
npm install --save-dev html-webpack-plugin mini-css-extract-plugin css-minimizer-webpack-plugin terser-webpack-plugin
```

```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      minify: {
        removeComments: true,
        collapseWhitespace: true,
      },
    }),

    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css',
    }),
  ],

  optimization: {
    minimizer: [
      new TerserPlugin(),
      new CssMinimizerPlugin(),
    ],
  },
};
```

## Code Splitting

### Entry Points

```javascript
module.exports = {
  entry: {
    main: './src/index.js',
    vendor: './src/vendor.js',
  },

  output: {
    filename: '[name].[contenthash].js',
  },
};
```

### Dynamic Imports

```javascript
// In your code
const LazyComponent = React.lazy(() => import('./LazyComponent'));

// Or with magic comments
import(/* webpackChunkName: "my-chunk" */ './module');
```

### SplitChunks

```javascript
optimization: {
  splitChunks: {
    chunks: 'all',
    cacheGroups: {
      vendor: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all',
      },
      common: {
        minChunks: 2,
        priority: -10,
        reuseExistingChunk: true,
      },
    },
  },
  runtimeChunk: 'single',
}
```

## Module Federation

Share code between independent builds at runtime.

### Host Application

```javascript
const { ModuleFederationPlugin } = require('webpack').container;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'host',
      remotes: {
        remoteApp: 'remoteApp@http://localhost:3001/remoteEntry.js',
      },
      shared: {
        react: { singleton: true, requiredVersion: '^18.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
      },
    }),
  ],
};
```

### Remote Application

```javascript
new ModuleFederationPlugin({
  name: 'remoteApp',
  filename: 'remoteEntry.js',
  exposes: {
    './Button': './src/components/Button',
    './utils': './src/utils',
  },
  shared: {
    react: { singleton: true },
    'react-dom': { singleton: true },
  },
})
```

### Consuming Remote Modules

```javascript
// Dynamic import from remote
const RemoteButton = React.lazy(() => import('remoteApp/Button'));

// Use in component
<Suspense fallback="Loading...">
  <RemoteButton />
</Suspense>
```

## Development Server

```javascript
devServer: {
  static: {
    directory: path.join(__dirname, 'public'),
  },
  port: 3000,
  hot: true,
  open: true,
  historyApiFallback: true, // For SPA routing

  proxy: [
    {
      context: ['/api'],
      target: 'http://localhost:8080',
      changeOrigin: true,
    },
  ],

  client: {
    overlay: {
      errors: true,
      warnings: false,
    },
  },
}
```

## Production Optimization

```javascript
module.exports = {
  mode: 'production',

  output: {
    filename: '[name].[contenthash].js',
    chunkFilename: '[name].[contenthash].chunk.js',
    clean: true,
  },

  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: { drop_console: true },
        },
      }),
      new CssMinimizerPlugin(),
    ],
    splitChunks: {
      chunks: 'all',
    },
    runtimeChunk: 'single',
    moduleIds: 'deterministic',
  },

  performance: {
    hints: 'warning',
    maxEntrypointSize: 250000,
    maxAssetSize: 250000,
  },
};
```

## Environment Variables

```javascript
const webpack = require('webpack');

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      'process.env.API_URL': JSON.stringify(process.env.API_URL),
    }),

    new webpack.EnvironmentPlugin({
      NODE_ENV: 'development',
      DEBUG: false,
    }),
  ],
};
```

## Source Maps

```javascript
// Development - fast, less accurate
devtool: 'eval-cheap-module-source-map',

// Production - slow, accurate
devtool: 'source-map',

// Production - no source maps
devtool: false,
```

## Resolve Configuration

```javascript
resolve: {
  extensions: ['.tsx', '.ts', '.jsx', '.js'],

  alias: {
    '@': path.resolve(__dirname, 'src'),
    '@components': path.resolve(__dirname, 'src/components'),
    '@utils': path.resolve(__dirname, 'src/utils'),
  },

  fallback: {
    // Polyfills for Node.js modules
    path: require.resolve('path-browserify'),
    crypto: require.resolve('crypto-browserify'),
  },
}
```

See [references/plugins.md](references/plugins.md) for plugin catalog and [references/optimization.md](references/optimization.md) for advanced optimization techniques.
