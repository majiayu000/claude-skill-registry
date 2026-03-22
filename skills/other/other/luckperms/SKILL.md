---
name: luckperms
description: LuckPerms - Minecraft permission plugin for managing permissions, groups, and user access
---

# LuckPerms Skill

LuckPerms is a permissions plugin for Minecraft servers. It allows server admins to control what features players can use by creating groups and assigning permissions.

## When to Use This Skill

This skill should be triggered when:
- Working with LuckPerms permissions plugin
- Asking about LuckPerms features, configuration, or APIs
- Implementing permission systems in Minecraft plugins
- Setting up groups, permissions, or inheritance
- Debugging permission-related issues
- Integrating with LuckPerms API

## Quick Reference

### What is LuckPerms?

LuckPerms is:
- **fast** - written with performance and scalability in mind
- **reliable** - trusted by thousands of server admins and large server networks
- **easy to use** - setup permissions using commands, config files, or web editor
- **flexible** - supports a variety of data storage options and server types
- **extensive** - a plethora of customization options and settings
- **free** - available at no cost, permissively licensed (MIT)

### Supported Platforms

LuckPerms works on:
- **Bukkit/Spigot/Paper** - Traditional Minecraft server software
- **BungeeCord** - Proxy server for networking multiple servers
- **Velocity** - Modern proxy server alternative to BungeeCord
- **Fabric** - Modded Minecraft server
- **Forge/NeoForge** - Modded Minecraft server
- **Sponge** - Modded Minecraft server API
- **Nukkit** - Bedrock Edition server
- **Standalone** - Can run independently

### Project Structure

- **API** (`net.luckperms:api`) - Public, semantically versioned API for plugin integration
- **Common** - Core implementation shared across all platforms
- **Platform modules** - Platform-specific implementations (Bukkit, Bungee, Velocity, etc.)

### Building from Source

```bash
git clone https://github.com/LuckPerms/LuckPerms.git
cd LuckPerms/
./gradlew build
```

Output jars are in `loader/build/libs` or `build/libs`.

### API Dependency (Maven)

```xml
<dependency>
    <groupId>net.luckperms</groupId>
    <artifactId>api</artifactId>
    <version>5.4</version>
    <scope>provided</scope>
</dependency>
```

### Code Style

LuckPerms loosely follows the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html).

### Key Concepts

1. **Permissions** - Granular control over what players can do
2. **Groups** - Collections of permissions assigned to multiple users
3. **Inheritance** - Groups can inherit from other groups
4. **Contexts** - Permissions can vary based on context (world, server, etc.)
5. **Weight** - Determines priority when permissions conflict
6. **Tracks** - Progression systems for ranking up players

### Common Commands

- `/lp user <player> permission set <permission>` - Grant permission to user
- `/lp group <group> permission set <permission>` - Grant permission to group
- `/lp user <player> parent add <group>` - Add user to group
- `/lp creategroup <group>` - Create a new group
- `/lp group <group> parent add <parent>` - Set group inheritance
- `/lp sync` - Sync data across servers
- `/lp editor` - Open web editor

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - API documentation
- **index.md** - Wiki index

## Resources

### Official Links
- **Homepage**: https://luckperms.net
- **Wiki**: https://luckperms.net/wiki
- **Discord**: https://discord.gg/luckperms
- **GitHub**: https://github.com/LuckPerms/LuckPerms
- **CI**: https://ci.lucko.me/job/LuckPerms/
- **Javadoc**: https://javadoc.io/doc/net.luckperms/api

### Support
- Use Discord for community support
- Report bugs via [GitHub Issues](https://github.com/LuckPerms/LuckPerms/issues)
- Check existing issues before reporting

## Notes

- This skill was generated from official LuckPerms documentation and source code
- LuckPerms is licensed under the MIT License
- The project uses semantic versioning for the API
- Consider discussing large changes via GitHub Issues before submitting PRs

## Updating

To refresh this skill with updated information:
1. Check https://luckperms.net/wiki for latest documentation
2. Review the GitHub repository for API changes
3. Update reference files as needed
