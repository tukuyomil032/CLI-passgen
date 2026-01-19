#!/usr/bin/env node

import yargs from "yargs";
import { hideBin } from "yargs/helpers";
import ora from "ora";
import { generatePassword, getRandomCharTypes } from "./core/generator.js";
import { CHAR_SETS, CHAR_TYPE_NAMES, type CharType } from "./core/constants.js";
import { copyToClipboard } from "./core/clipboard.js";
import { Display } from "./ui/display.js";
import { interactiveMode } from "./ui/interactive.js";

const VERSION = "1.0.0";

async function executeCommand(args: any): Promise<number> {
  // Interactive mode if no length specified
  if (args.length === undefined && args.temp !== true) {
    return interactiveMode(true);
  }

  // Set default length for --temp flag
  if (args.temp) {
    if (args.length === undefined) {
      args.length = 16;
    }
    return interactiveMode(true);
  }

  const length = args.length as number;

  // Validate length
  if (!Number.isInteger(length) || length < 1 || length > 256) {
    Display.printError("Password length must be between 1-256");
    return 1;
  }

  const count = Math.max(1, args.count as number);

  // Determine character types
  let charTypes: CharType[] = [];

  if (args.random) {
    charTypes = getRandomCharTypes();
    if (!args.quiet) {
      Display.printInfo(`Randomly selected: ${charTypes.join(", ")}`);
    }
  } else {
    if (args.numbers) charTypes.push("numbers");
    if (args.lowercase) charTypes.push("lowercase");
    if (args.uppercase) charTypes.push("uppercase");
    if (args.special) charTypes.push("special");

    // Use all types if none specified
    if (charTypes.length === 0) {
      charTypes = Object.keys(CHAR_SETS) as CharType[];
    }
  }

  // Generate passwords with spinner
  const spinner = ora({
    text: "Generating passwords...",
    isEnabled: !args.quiet && count > 1,
  }).start();

  const passwords: string[] = [];
  try {
    for (let i = 0; i < count; i++) {
      passwords.push(generatePassword(length, charTypes));
    }
    if (spinner.isSpinning) {
      spinner.succeed("Passwords generated!");
    }
  } catch (error) {
    if (spinner.isSpinning) {
      spinner.fail("Failed to generate passwords");
    }
    Display.printError((error as Error).message);
    return 1;
  }

  // Output
  if (args.quiet) {
    passwords.forEach((pwd) => console.log(pwd));
  } else if (count === 1) {
    Display.printPassword(passwords[0]);
  } else {
    Display.printPasswords(passwords);
  }

  // Handle clipboard
  if (!args.quiet && !args.no_copy) {
    if (args.copy !== undefined) {
      const copyIndex = args.copy as number;
      if (copyIndex >= 1 && copyIndex <= passwords.length) {
        const copied = await copyToClipboard(passwords[copyIndex - 1]);
        if (copied) {
          Display.printSuccess(`Password [${copyIndex}] copied to clipboard!`);
        } else {
          Display.printError("Failed to copy to clipboard");
        }
      } else {
        Display.printError(`Invalid password number: ${copyIndex}`);
      }
    } else if (count === 1) {
      const copied = await copyToClipboard(passwords[0]);
      if (copied) {
        Display.printSuccess("Copied to clipboard!");
      } else {
        Display.printInfo(
          "Clipboard not available. Install xclip or xsel on Linux."
        );
      }
    }
  }

  return 0;
}

async function main() {
  const argv = yargs(hideBin(process.argv))
    .version("version", VERSION)
    .alias("v", "version")
    .option("length", {
      alias: "l",
      type: "number",
      describe: "Password length (1-256)",
      default: undefined,
    })
    .option("count", {
      alias: "c",
      type: "number",
      describe: "Number of passwords to generate",
      default: 1,
    })
    .option("numbers", {
      alias: "n",
      type: "boolean",
      describe: "Include numbers (0-9)",
      default: false,
    })
    .option("lowercase", {
      alias: "a",
      type: "boolean",
      describe: "Include lowercase letters (a-z)",
      default: false,
    })
    .option("uppercase", {
      alias: "A",
      type: "boolean",
      describe: "Include uppercase letters (A-Z)",
      default: false,
    })
    .option("special", {
      alias: "s",
      type: "boolean",
      describe: "Include special characters",
      default: false,
    })
    .option("random", {
      alias: "r",
      type: "boolean",
      describe: "Use random character types",
      default: false,
    })
    .option("quiet", {
      alias: "q",
      type: "boolean",
      describe: "Output only passwords (for scripting)",
      default: false,
    })
    .option("no-copy", {
      type: "boolean",
      describe: "Disable auto-copy to clipboard",
      default: false,
    })
    .option("copy", {
      type: "number",
      describe: "Copy Nth password to clipboard",
      default: undefined,
    })
    .option("temp", {
      type: "boolean",
      describe: "Temporarily enter interactive menu",
      default: false,
    })
    .alias("help", "h")
    .epilogue(
      `Examples:
  passgen                              Interactive mode
  passgen -l 16                        16 chars with all character types
  passgen -l 20 -n -a                  20 chars with numbers and lowercase
  passgen -l 32 -n -a -A -s            32 chars with all types
  passgen -l 16 -c 5                   Generate 5 passwords of 16 chars
  passgen -l 24 -r                     24 chars with random character types
  passgen -l 16 --no-copy              Disable auto-copy to clipboard`
    )
    .parseSync();

  const exitCode = await executeCommand(argv);
  process.exit(exitCode);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
