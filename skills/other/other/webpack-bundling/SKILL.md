---
name: webpack-bundling
description: "Optimize JavaScript applications with Webpack 5 using code splitting, tree shaking, and advanced bundling strategies. Configure loaders, plugins, and optimization techniques for production builds. Use for: bundling JavaScript modules and assets, implementing code splitting for faster load times, optimizing bundle size with tree shaking, configuring development and production builds, integrating with Babel/TypeScript, managing CSS and asset loading, implementing hot module replacement, and deploying optimized production bundles with caching strategies."
---

# Webpack Bundling

Master module bundling and optimization with Webpack 5 for production-ready JavaScript applications.

## Overview

Webpack is a powerful static module bundler for JavaScript applications. Webpack 5 introduces improved caching, module federation, better tree shaking, and performance enhancements. It processes application modules, creates dependency graphs, and outputs optimized bundles for deployment.

## Core Concepts

### Entry Points

```javascript
// webpack.config.js
module.exports = {
  entry: './src/index.js',
  
  // Multiple entry points
  entry: {
    app: './src/app.js',
    admin: './src/admin.js'
  },
  
  // Dynamic entry
  entry: () => ({
    app: './src/app.js',
    vendor: ['react', 'react-dom']
  })
};
```

### Output Configuration

```javascript
const path = require('path');

module.exports = {
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    chunkFilename: '[name].[contenthash].chunk.js',
    clean: true, // Clean dist folder
    publicPath: '/assets/'
  }
};
```

### Loaders

```javascript
module.exports = {
  module: {
    rules: [
      // Babel loader for JavaScript
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      
      // TypeScript loader
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      },
      
      // CSS loader
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      
      // SCSS loader
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader']
      },
      
      // File loader for images
      {
        test: /\.(png|jpg|gif|svg)$/,
        type: 'asset/resource'
      },
      
      // Inline small assets
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        type: 'asset/inline'
      }
    ]
  }
};
```

### Plugins

```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { DefinePlugin } = require('webpack');

module.exports = {
  plugins: [
    // Generate HTML file
    new HtmlWebpackPlugin({
      template: './src/index.html',
      minify: true
    }),
    
    // Extract CSS to separate file
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css'
    }),
    
    // Define environment variables
    new DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production'),
      'process.env.API_URL': JSON.stringify('https://api.example.com')
    })
  ]
};
```

## Code Splitting

### Entry Point Splitting

```javascript
module.exports = {
  entry: {
    app: './src/app.js',
    vendor: './src/vendor.js'
  },
  optimization: {
    runtimeChunk: 'single'
  }
};
```

### SplitChunksPlugin

```javascript
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        // Vendor chunk
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        },
        
        // Common chunk
        common: {
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true
        },
        
        // React chunk
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'react',
          priority: 20
        }
      }
    }
  }
};
```

### Dynamic Imports

```javascript
// Lazy load module
button.addEventListener('click', () => {
  import(/* webpackChunkName: "lodash" */ 'lodash')
    .then(({ default: _ }) => {
      console.log(_.join(['Hello', 'webpack'], ' '));
    });
});

// Prefetch
import(/* webpackPrefetch: true */ './components/Modal');

// Preload
import(/* webpackPreload: true */ './components/Chart');
```

## Optimization

### Production Configuration

```javascript
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  mode: 'production',
  
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true
          }
        }
      }),
      new CssMinimizerPlugin()
    ],
    
    // Module IDs
    moduleIds: 'deterministic',
    
    // Runtime chunk
    runtimeChunk: 'single',
    
    // Split chunks
    splitChunks: {
      chunks: 'all',
      maxInitialRequests: 25,
      minSize: 20000
    }
  },
  
  performance: {
    hints: 'warning',
    maxEntrypointSize: 512000,
    maxAssetSize: 512000
  }
};
```

### Tree Shaking

```javascript
// package.json
{
  "sideEffects": false
}

// Or specify files with side effects
{
  "sideEffects": ["*.css", "*.scss"]
}

// webpack.config.js
module.exports = {
  mode: 'production',
  optimization: {
    usedExports: true
  }
};
```

### Caching

```javascript
module.exports = {
  output: {
    filename: '[name].[contenthash].js',
    chunkFilename: '[name].[contenthash].chunk.js'
  },
  
  optimization: {
    moduleIds: 'deterministic',
    runtimeChunk: 'single',
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all'
        }
      }
    }
  },
  
  cache: {
    type: 'filesystem',
    buildDependencies: {
      config: [__filename]
    }
  }
};
```

## Development Server

```javascript
module.exports = {
  devServer: {
    static: './dist',
    port: 3000,
    hot: true,
    open: true,
    historyApiFallback: true,
    
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    },
    
    headers: {
      'Access-Control-Allow-Origin': '*'
    }
  },
  
  devtool: 'eval-source-map'
};
```

## Module Federation

```javascript
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'app1',
      filename: 'remoteEntry.js',
      exposes: {
        './Button': './src/Button',
        './Header': './src/Header'
      },
      remotes: {
        app2: 'app2@http://localhost:3002/remoteEntry.js'
      },
      shared: {
        react: { singleton: true },
        'react-dom': { singleton: true }
      }
    })
  ]
};
```

## Complete Configuration Example

```javascript
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
  mode: isProduction ? 'production' : 'development',
  
  entry: './src/index.js',
  
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: isProduction ? '[name].[contenthash].js' : '[name].js',
    clean: true
  },
  
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: [
          isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        type: 'asset/resource'
      }
    ]
  },
  
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html'
    }),
    isProduction && new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css'
    })
  ].filter(Boolean),
  
  optimization: {
    minimize: isProduction,
    minimizer: [
      new TerserPlugin(),
      new CssMinimizerPlugin()
    ],
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        }
      }
    }
  },
  
  devServer: {
    static: './dist',
    port: 3000,
    hot: true
  },
  
  devtool: isProduction ? 'source-map' : 'eval-source-map'
};
```

## Using the Reference Files

### When to Read Each Reference

**`/references/advanced-optimization.md`** — Read when implementing advanced code splitting, tree shaking, or bundle analysis.

**`/references/loaders-plugins.md`** — Read when configuring custom loaders, writing plugins, or integrating build tools.

**`/references/module-federation.md`** — Read when implementing micro-frontends or sharing code between applications.

**`/references/troubleshooting.md`** — Read when debugging build issues, resolving loader conflicts, or optimizing build performance.
