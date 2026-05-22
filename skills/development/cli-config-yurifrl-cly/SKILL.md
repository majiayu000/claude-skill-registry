---
name: cli-config
description: Manage CLI application configuration with Cobra and Viper. Use when implementing config files, environment variables, flags binding, or when user mentions Viper, configuration management, config files, or CLI settings.
---

# CLI Configuration with Cobra & Viper

Build flexible, hierarchical configuration systems for CLI applications using Cobra (commands/flags) and Viper (config management).

## Your Role: Configuration Architect

You design configuration systems with proper precedence and flexibility. You:

✅ **Implement config hierarchy** - Flags > Env > Config > Defaults
✅ **Bind flags to Viper** - Seamless integration
✅ **Support multiple formats** - YAML, JSON, TOML
✅ **Handle environment variables** - With prefixes
✅ **Provide config commands** - init, show, validate
✅ **Follow CLY patterns** - Use project structure

❌ **Do NOT hardcode paths** - Use conventions
❌ **Do NOT skip validation** - Validate config
❌ **Do NOT ignore precedence** - Follow hierarchy

## Configuration Precedence

Viper uses this precedence order (highest to lowest):

1. Explicit `viper.Set()` calls
2. Command-line flags
3. Environment variables
4. Config file values
5. Defaults

```go
viper.SetDefault("port", 8080)              // 5. Default
// config.yaml: port: 8081                  // 4. Config file
os.Setenv("APP_PORT", "8082")              // 3. Environment
cobra.Flags().Int("port", 0, "Port")       // 2. Flag
viper.Set("port", 8083)                     // 1. Explicit set
```

## Basic Setup

### Initialize Viper

```go
package config

import (
    "fmt"
    "os"

    "github.com/spf13/viper"
)

func Init() error {
    // Set config name (no extension)
    viper.SetConfigName("config")

    // Set config type
    viper.SetConfigType("yaml")

    // Add search paths
    viper.AddConfigPath(".")
    viper.AddConfigPath("$HOME/.myapp")
    viper.AddConfigPath("/etc/myapp")

    // Read config
    if err := viper.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); ok {
            // Config file not found; use defaults
            return nil
        }
        return fmt.Errorf("error reading config: %w", err)
    }

    return nil
}
```

### With Cobra Integration

```go
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var cfgFile string

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My application",
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}

func init() {
    cobra.OnInitialize(initConfig)

    // Global flags
    rootCmd.PersistentFlags().StringVar(
        &cfgFile,
        "config",
        "",
        "config file (default is $HOME/.myapp/config.yaml)",
    )
}

func initConfig() {
    if cfgFile != "" {
        // Use explicit config file
        viper.SetConfigFile(cfgFile)
    } else {
        // Find home directory
        home, err := os.UserHomeDir()
        if err != nil {
            fmt.Println(err)
            os.Exit(1)
        }

        // Search config in home directory and current directory
        viper.AddConfigPath(home + "/.myapp")
        viper.AddConfigPath(".")
        viper.SetConfigType("yaml")
        viper.SetConfigName("config")
    }

    // Read environment variables
    viper.AutomaticEnv()
    viper.SetEnvPrefix("MYAPP")

    // Read config file
    if err := viper.ReadInConfig(); err == nil {
        fmt.Println("Using config file:", viper.ConfigFileUsed())
    }
}
```

## Configuration Patterns

### Set Defaults

```go
func setDefaults() {
    // Server
    viper.SetDefault("server.port", 8080)
    viper.SetDefault("server.host", "localhost")
    viper.SetDefault("server.timeout", "30s")

    // Database
    viper.SetDefault("database.host", "localhost")
    viper.SetDefault("database.port", 5432)
    viper.SetDefault("database.name", "myapp")

    // Logging
    viper.SetDefault("log.level", "info")
    viper.SetDefault("log.format", "json")
}
```

### Bind Flags

**Single flag:**
```go
cmd.Flags().IntP("port", "p", 8080, "Port to run on")
viper.BindPFlag("server.port", cmd.Flags().Lookup("port"))
```

**All flags:**
```go
cmd.Flags().Int("port", 8080, "Port")
cmd.Flags().String("host", "localhost", "Host")

viper.BindPFlags(cmd.Flags())
```

**Persistent flags:**
```go
rootCmd.PersistentFlags().String("log-level", "info", "Log level")
viper.BindPFlag("log.level", rootCmd.PersistentFlags().Lookup("log-level"))
```

### Environment Variables

**Auto-map all env vars:**
```go
viper.AutomaticEnv()
viper.SetEnvPrefix("MYAPP")

// MYAPP_SERVER_PORT → server.port
// MYAPP_DATABASE_NAME → database.name
```

**Custom env key replacer:**
```go
import "strings"

viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
viper.AutomaticEnv()
viper.SetEnvPrefix("MYAPP")

// MYAPP_SERVER_PORT → server.port (. → _)
```

**Bind specific env var:**
```go
viper.BindEnv("database.password", "DB_PASSWORD")

// DB_PASSWORD → database.password
```

### Read Config Values

**Get typed values:**
```go
port := viper.GetInt("server.port")
host := viper.GetString("server.host")
enabled := viper.GetBool("feature.enabled")
timeout := viper.GetDuration("server.timeout")
tags := viper.GetStringSlice("tags")
```

**Check if set:**
```go
if viper.IsSet("server.port") {
    port := viper.GetInt("server.port")
}
```

**Get with default:**
```go
port := viper.GetInt("server.port")
if port == 0 {
    port = 8080
}
```

### Unmarshal to Struct

**Full config:**
```go
type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
    Log      LogConfig      `mapstructure:"log"`
}

type ServerConfig struct {
    Port    int    `mapstructure:"port"`
    Host    string `mapstructure:"host"`
    Timeout string `mapstructure:"timeout"`
}

var config Config

if err := viper.Unmarshal(&config); err != nil {
    return fmt.Errorf("unable to decode config: %w", err)
}
```

**Subsection:**
```go
var serverConfig ServerConfig

if err := viper.UnmarshalKey("server", &serverConfig); err != nil {
    return fmt.Errorf("unable to decode server config: %w", err)
}
```

### Write Config

**Create default config:**
```go
func createDefaultConfig(path string) error {
    viper.SetDefault("server.port", 8080)
    viper.SetDefault("server.host", "localhost")

    return viper.WriteConfigAs(path)
}
```

**Save current config:**
```go
viper.Set("server.port", 9090)

// Write to current config file
viper.WriteConfig()

// Write to specific file
viper.WriteConfigAs("/path/to/config.yaml")

// Safe write (won't overwrite)
viper.SafeWriteConfig()
```

## CLY Project Pattern

### Config Package

**pkg/config/config.go:**
```go
package config

import (
    "fmt"
    "os"
    "path/filepath"

    "github.com/spf13/viper"
)

type Config struct {
    Server ServerConfig `mapstructure:"server"`
    Log    LogConfig    `mapstructure:"log"`
}

type ServerConfig struct {
    Port int    `mapstructure:"port"`
    Host string `mapstructure:"host"`
}

type LogConfig struct {
    Level  string `mapstructure:"level"`
    Format string `mapstructure:"format"`
}

var cfg *Config

// Init initializes the configuration
func Init(cfgFile string) error {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, err := os.UserHomeDir()
        if err != nil {
            return err
        }

        viper.AddConfigPath(filepath.Join(home, ".cly"))
        viper.AddConfigPath(".")
        viper.SetConfigType("yaml")
        viper.SetConfigName("config")
    }

    setDefaults()

    viper.AutomaticEnv()
    viper.SetEnvPrefix("CLY")

    if err := viper.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
            return err
        }
    }

    cfg = &Config{}
    if err := viper.Unmarshal(cfg); err != nil {
        return fmt.Errorf("unable to decode config: %w", err)
    }

    return nil
}

func setDefaults() {
    viper.SetDefault("server.port", 8080)
    viper.SetDefault("server.host", "localhost")
    viper.SetDefault("log.level", "info")
    viper.SetDefault("log.format", "text")
}

// Get returns the current config
func Get() *Config {
    return cfg
}

// GetString returns a config value as string
func GetString(key string) string {
    return viper.GetString(key)
}

// GetInt returns a config value as int
func GetInt(key string) int {
    return viper.GetInt(key)
}

// GetBool returns a config value as bool
func GetBool(key string) bool {
    return viper.GetBool(key)
}
```

### Root Command Integration

**cmd/root.go:**
```go
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
    "github.com/yurifrl/cly/pkg/config"
)

var cfgFile string

var RootCmd = &cobra.Command{
    Use:   "cly",
    Short: "CLY - Command Line Yuri",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        return config.Init(cfgFile)
    },
}

func Execute() {
    if err := RootCmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func init() {
    RootCmd.PersistentFlags().StringVar(
        &cfgFile,
        "config",
        "",
        "config file (default is $HOME/.cly/config.yaml)",
    )
}
```

### Config Command

**modules/config/cmd.go:**
```go
package configcmd

import (
    "fmt"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "config",
        Short: "Manage configuration",
    }

    cmd.AddCommand(
        initCmd(),
        showCmd(),
        validateCmd(),
    )

    parent.AddCommand(cmd)
}

func initCmd() *cobra.Command {
    return &cobra.Command{
        Use:   "init",
        Short: "Initialize config file",
        RunE: func(cmd *cobra.Command, args []string) error {
            path, _ := cmd.Flags().GetString("path")
            if path == "" {
                path = "$HOME/.cly/config.yaml"
            }

            if err := viper.SafeWriteConfigAs(path); err != nil {
                return fmt.Errorf("failed to create config: %w", err)
            }

            fmt.Printf("Config created at: %s\n", path)
            return nil
        },
    }
}

func showCmd() *cobra.Command {
    return &cobra.Command{
        Use:   "show",
        Short: "Show current configuration",
        RunE: func(cmd *cobra.Command, args []string) error {
            fmt.Println("Current configuration:")
            fmt.Println("Config file:", viper.ConfigFileUsed())
            fmt.Println()

            for _, key := range viper.AllKeys() {
                fmt.Printf("%s: %v\n", key, viper.Get(key))
            }

            return nil
        },
    }
}

func validateCmd() *cobra.Command {
    return &cobra.Command{
        Use:   "validate",
        Short: "Validate configuration",
        RunE: func(cmd *cobra.Command, args []string) error {
            // Add validation logic
            fmt.Println("Configuration is valid")
            return nil
        },
    }
}
```

## Advanced Patterns

### Remote Config (etcd, Consul)

```go
import _ "github.com/spf13/viper/remote"

func initRemoteConfig() error {
    viper.AddRemoteProvider("etcd", "http://127.0.0.1:4001", "/config/myapp.json")
    viper.SetConfigType("json")

    if err := viper.ReadRemoteConfig(); err != nil {
        return err
    }

    return nil
}

// Watch for changes
func watchRemoteConfig() {
    go func() {
        for {
            time.Sleep(time.Second * 5)
            err := viper.WatchRemoteConfig()
            if err != nil {
                log.Printf("unable to read remote config: %v", err)
                continue
            }
        }
    }()
}
```

### Watch Config File

```go
viper.WatchConfig()
viper.OnConfigChange(func(e fsnotify.Event) {
    fmt.Println("Config file changed:", e.Name)

    // Reload config
    var newConfig Config
    if err := viper.Unmarshal(&newConfig); err != nil {
        log.Printf("error reloading config: %v", err)
        return
    }

    // Update application state
    updateAppConfig(newConfig)
})
```

### Multiple Config Instances

```go
// Default instance
viper.SetConfigName("config")
viper.ReadInConfig()

// Custom instance
v := viper.New()
v.SetConfigName("other-config")
v.AddConfigPath(".")
v.ReadInConfig()

port := v.GetInt("port")
```

### Config with Validation

```go
type Config struct {
    Server ServerConfig `mapstructure:"server" validate:"required"`
    DB     DBConfig     `mapstructure:"database" validate:"required"`
}

type ServerConfig struct {
    Port int    `mapstructure:"port" validate:"required,min=1,max=65535"`
    Host string `mapstructure:"host" validate:"required,hostname"`
}

func Load() (*Config, error) {
    var cfg Config

    if err := viper.Unmarshal(&cfg); err != nil {
        return nil, err
    }

    // Validate
    validate := validator.New()
    if err := validate.Struct(cfg); err != nil {
        return nil, fmt.Errorf("invalid config: %w", err)
    }

    return &cfg, nil
}
```

### Nested Config Keys

```go
// Dot notation
viper.Set("server.database.host", "localhost")

// Nested maps
viper.Set("server", map[string]interface{}{
    "database": map[string]interface{}{
        "host": "localhost",
        "port": 5432,
    },
})

// Access nested
host := viper.GetString("server.database.host")

// Get sub-tree
dbConfig := viper.Sub("server.database")
if dbConfig != nil {
    host := dbConfig.GetString("host")
}
```

## Config File Formats

### YAML

**config.yaml:**
```yaml
server:
  port: 8080
  host: localhost
  timeout: 30s

database:
  host: localhost
  port: 5432
  name: myapp
  user: postgres
  password: secret

log:
  level: info
  format: json
  output: stdout

features:
  enabled:
    - feature1
    - feature2
```

### JSON

**config.json:**
```json
{
  "server": {
    "port": 8080,
    "host": "localhost"
  },
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

### TOML

**config.toml:**
```toml
[server]
port = 8080
host = "localhost"

[database]
host = "localhost"
port = 5432
name = "myapp"
```

## Best Practices

### 1. Always Set Defaults

```go
func init() {
    viper.SetDefault("server.port", 8080)
    viper.SetDefault("log.level", "info")
}
```

### 2. Use Environment Variables

```go
viper.AutomaticEnv()
viper.SetEnvPrefix("MYAPP")

// Now MYAPP_SERVER_PORT overrides config
```

### 3. Validate Config

```go
type Config struct {
    Port int `validate:"required,min=1,max=65535"`
}

if err := validate.Struct(cfg); err != nil {
    return err
}
```

### 4. Provide Config Commands

```
myapp config init      # Create default config
myapp config show      # Show current config
myapp config validate  # Validate config
```

### 5. Handle Missing Config Gracefully

```go
if err := viper.ReadInConfig(); err != nil {
    if _, ok := err.(viper.ConfigFileNotFoundError); ok {
        // Config not found, use defaults
        log.Println("No config file found, using defaults")
    } else {
        return err
    }
}
```

### 6. Don't Store Secrets in Config

```go
// ❌ BAD
database:
  password: "mysecret"

// ✅ GOOD - Use env vars
database:
  password: ${DB_PASSWORD}

// Or
viper.BindEnv("database.password", "DB_PASSWORD")
```

### 7. Use Struct Tags

```go
type ServerConfig struct {
    Port    int    `mapstructure:"port" json:"port" yaml:"port"`
    Host    string `mapstructure:"host" json:"host" yaml:"host"`
    Timeout string `mapstructure:"timeout" json:"timeout" yaml:"timeout"`
}
```

## Common Patterns

### Config Init Command

```go
func initConfigCmd() *cobra.Command {
    var force bool

    cmd := &cobra.Command{
        Use:   "init",
        Short: "Initialize configuration",
        RunE: func(cmd *cobra.Command, args []string) error {
            configPath := viper.ConfigFileUsed()
            if configPath == "" {
                configPath = filepath.Join(os.Getenv("HOME"), ".myapp", "config.yaml")
            }

            // Check if exists
            if _, err := os.Stat(configPath); err == nil && !force {
                return fmt.Errorf("config already exists: %s (use --force to overwrite)", configPath)
            }

            // Create directory
            if err := os.MkdirAll(filepath.Dir(configPath), 0755); err != nil {
                return err
            }

            // Write config
            if err := viper.WriteConfigAs(configPath); err != nil {
                return err
            }

            fmt.Printf("Config initialized: %s\n", configPath)
            return nil
        },
    }

    cmd.Flags().BoolVar(&force, "force", false, "Overwrite existing config")
    return cmd
}
```

### Config Migration

```go
func migrateConfig() error {
    version := viper.GetInt("version")

    switch version {
    case 0:
        // Migrate from v0 to v1
        viper.Set("new_field", "default")
        viper.Set("version", 1)
        fallthrough
    case 1:
        // Migrate from v1 to v2
        viper.Set("another_field", true)
        viper.Set("version", 2)
    }

    return viper.WriteConfig()
}
```

## Testing

```go
func TestConfig(t *testing.T) {
    // Use separate viper instance
    v := viper.New()
    v.SetConfigType("yaml")

    var yamlConfig = []byte(`
server:
  port: 8080
  host: localhost
`)

    v.ReadConfig(bytes.NewBuffer(yamlConfig))

    assert.Equal(t, 8080, v.GetInt("server.port"))
    assert.Equal(t, "localhost", v.GetString("server.host"))
}
```

## Checklist

- [ ] Defaults set for all config values
- [ ] Config file search paths defined
- [ ] Environment variable support
- [ ] Flags bound to config
- [ ] Config struct with mapstructure tags
- [ ] Config validation
- [ ] Config commands (init, show, validate)
- [ ] Error handling for missing config
- [ ] Secrets via env vars only
- [ ] Config file format documented

## Resources

- [Viper Documentation](https://github.com/spf13/viper)
- [Cobra User Guide](https://github.com/spf13/cobra/blob/main/user_guide.md)
- [12-Factor Config](https://12factor.net/config)
- CLY config: `pkg/config/`, `modules/config/`
