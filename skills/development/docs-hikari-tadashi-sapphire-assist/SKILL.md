---
name: docs-hikari-tadashi-sapphire-assist
description: 'Location: packages/skills/CalendarSkill/'
---

# CalendarSkill Module

**Location**: `packages/skills/CalendarSkill/`
**Package Category**: **Skills** - User-facing functionality

## Overview
The CalendarSkill module provides calendar management functionality for the Sapphire Assistant Framework. It demonstrates how to implement a skill module that can handle calendar-related voice commands and operations.

## Key Components

### CalendarService.kt
**Location**: `packages/skills/CalendarSkill/src/main/java/com/example/calendarskill/CalendarService.kt`

**Purpose**: Main service for handling calendar operations including create, retrieve, update, and delete actions.

**Key Methods**:
- `onStartCommand()`: Processes calendar intents and performs CRUD operations
- `getManditoryVariables()`: Extracts required parameters (action, dateTime, event)
- `checkForOptional()`: Handles optional parameters like description
- `populateCalendar()`: Manages date/time ranges for events

**Functionality**: Currently logs calendar actions but appears to be a prototype without actual calendar integration.

### CalendarPostOfficeService.kt
**Location**: `packages/skills/CalendarSkill/src/main/java/com/example/calendarskill/CalendarPostOfficeService.kt`

**Purpose**: Handles module registration and file data management for the calendar skill.

**Key Methods**:
- `sendFileNames()`: Provides list of files this module offers
- `coreTransferFile()`: Manages file transfers between modules
- `registerModule()`: Registers the calendar module with the core

## Configuration Files
**Location**: `packages/skills/CalendarSkill/src/main/assets/`

- `alarm.intent`: Intent patterns for alarm-related commands
- `calendar.conf`: Configuration for calendar operations
- `date.entity`: Date entity recognition patterns
- `get.intent`: Intent patterns for retrieving calendar information
- `set.intent`: Intent patterns for setting calendar events

## Module Type
**SKILL** - This module demonstrates the skill architecture for domain-specific functionality.

## Package Dependencies
- `packages/framework/ComponentFramework/` - Base service functionality
- `packages/core/CoreModule/` - Routing and communication
- Android Calendar Provider (not currently implemented)

## Build Configuration
```gradle
// In settings.gradle
include ':packages:skills:CalendarSkill'

// Build command
./gradlew :packages:skills:CalendarSkill:build
```

## Integration with Framework
This skill integrates with the Sapphire Framework through:
- **Intent Processing**: Receives intents from `packages/processing/ProcessorModule/`
- **Core Communication**: Routes through `packages/core/CoreModule/`
- **Base Classes**: Extends services from `packages/framework/ComponentFramework/`

## Usage
This module serves as a template for implementing calendar functionality and can be extended to integrate with Android's Calendar Provider or other calendar systems.

## Development Notes
- See `examples/HelloWorldSkill/` for a simpler skill example
- Follow the patterns established in ComponentFramework
- Use the Developer Guide for skill creation best practices

## Status
**Prototype** - Basic structure implemented but lacks actual calendar integration.