#!/usr/bin/env -S npx -y bun

/**
 * PPTX Helpers CLI
 *
 * Provides validation, theme management, and rendering commands for PPTX presentations.
 *
 * Usage:
 *   bun main.ts validate <deck.pptx>
 *   bun main.ts theme list
 *   bun main.ts theme show <name>
 *   bun main.ts render <deck.pptx> [--montage]
 */

// Re-export all modules for library usage
export * from './types.js';
export * from './util.js';
export * from './svg.js';
export * from './theme.js';
export * from './validation.js';
export * from './decorative.js';
export * from './code.js';
export * from './image.js';
export * from './text.js';
export * from './layout.js';
export * from './layout_builders.js';

import { PRESETS } from './theme.js';
import { validateDeck } from './validation.js';

const args = process.argv.slice(2);
const command = args[0];

async function main() {
  if (!command) {
    printUsage();
    process.exit(1);
  }

  switch (command) {
    case 'validate': {
      const deckPath = args[1];
      if (!deckPath) {
        console.error('Error: deck path required');
        console.error('Usage: bun main.ts validate <deck.pptx>');
        process.exit(1);
      }
      await handleValidate(deckPath);
      break;
    }

    case 'theme': {
      const subcommand = args[1];
      if (!subcommand) {
        console.error('Error: theme subcommand required');
        console.error('Usage: bun main.ts theme [list|show <name>]');
        process.exit(1);
      }
      if (subcommand === 'list') {
        handleThemeList();
      } else if (subcommand === 'show') {
        const themeName = args[2];
        if (!themeName) {
          console.error('Error: theme name required');
          console.error('Usage: bun main.ts theme show <name>');
          process.exit(1);
        }
        handleThemeShow(themeName);
      } else {
        console.error(`Unknown theme subcommand: ${subcommand}`);
        process.exit(1);
      }
      break;
    }

    default:
      console.error(`Unknown command: ${command}`);
      printUsage();
      process.exit(1);
  }
}

function printUsage(): void {
  console.log(`
PPTX Helpers CLI

Commands:
  validate <deck.pptx>      Validate a PPTX deck for common issues
  theme list                List all available theme presets
  theme show <name>         Display a specific theme configuration
`);
}

function handleThemeList(): void {
  const themes = Object.keys(PRESETS);
  console.log(`Found ${themes.length} theme presets:\n`);
  themes.forEach((name) => {
    console.log(`  - ${name}`);
  });
}

function handleThemeShow(themeName: string): void {
  if (!PRESETS[themeName]) {
    console.error(`Theme not found: ${themeName}`);
    console.error(`Available themes: ${Object.keys(PRESETS).join(', ')}`);
    process.exit(1);
  }
  const theme = PRESETS[themeName];
  console.log(`\nTheme: ${themeName}`);
  console.log(JSON.stringify(theme, null, 2));
}

async function handleValidate(deckPath: string): Promise<void> {
  try {
    // Note: This would require pptxgenjs integration in a real implementation
    console.log(`Would validate: ${deckPath}`);
    console.log('Validation not yet implemented in this CLI version');
  } catch (error) {
    console.error(`Error validating deck: ${error}`);
    process.exit(1);
  }
}


main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
