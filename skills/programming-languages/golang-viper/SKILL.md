---
name: golang-viper
description: Go Viper configuration library (github.com/spf13/viper). Use when working with config file reading (SetConfigName, AddConfigPath, ReadInConfig), setting defaults, environment variable binding (SetEnvPrefix, AutomaticEnv, BindEnv), unmarshaling to structs (Unmarshal, UnmarshalKey, mapstructure tags), or any spf13/viper configuration management.
---

# Golang Viper Configuration

Viper is Go's most popular configuration library. It handles config files, environment variables, defaults, and remote config stores with a unified API.

## Config Precedence (highest to lowest)

1. `viper.Set()` - explicit runtime overrides
2. Command-line flags (via pflag)
3. Environment variables
4. Config files
5. Remote key/value stores (etcd, Consul)
6. `viper.SetDefault()` - defaults

## Quick Reference

```go
// Basic setup
viper.SetConfigName("config")        // filename without extension
viper.SetConfigType("yaml")          // explicit format
viper.AddConfigPath(".")             // search current dir
viper.AddConfigPath("$HOME/.myapp")  // search home dir

// Set defaults before reading
viper.SetDefault("server.port", 8080)

// Read config
if err := viper.ReadInConfig(); err != nil {
    if _, ok := err.(viper.ConfigFileNotFoundError); ok {
        // Config file not found; use defaults
    } else {
        return fmt.Errorf("config error: %w", err)
    }
}

// Get values
host := viper.GetString("server.host")
port := viper.GetInt("server.port")
debug := viper.GetBool("debug")

// Unmarshal to struct
var config Config
viper.Unmarshal(&config)
viper.UnmarshalKey("server", &config.Server)
```

## Key Behaviors

- **Keys are case-insensitive**: `server.PORT` and `server.port` are the same
- **Env vars ARE case-sensitive**: `APP_PORT` differs from `app_port`
- **Nested keys use dots**: `server.host` maps to YAML `server: { host: ... }`
- **Not thread-safe**: wrap concurrent access with mutex

## References

Detailed documentation for each feature area:

- `references/core-config.md` - Config files, paths, defaults, reading, multiple configs
- `references/environment-vars.md` - Env binding, prefixes, key replacers, AutomaticEnv
- `references/unmarshaling.md` - Structs, mapstructure tags, type getters, custom types
- `references/advanced-features.md` - Watching changes, remote config, writing configs

## Common Patterns

### Multiple Config Files (config + secrets)

```go
// Main config
viper.SetConfigName("config")
viper.ReadInConfig()

// Separate secrets file
secretsViper := viper.New()
secretsViper.SetConfigName("secrets")
secretsViper.AddConfigPath(".")
secretsViper.ReadInConfig()
```

### Environment Variable Override

```go
viper.SetEnvPrefix("MYAPP")           // MYAPP_SERVER_PORT
viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
viper.AutomaticEnv()
```
