import enquirer from "inquirer";
import { generatePassword, getRandomCharTypes } from "../core/generator.js";
import { CHAR_SETS } from "../core/constants.js";
import { copyToClipboard } from "../core/clipboard.js";
import { Display } from "./display.js";

type CharType = string;

export async function interactiveMode(showBanner: boolean = true): Promise<number> {
  let displayBanner = showBanner;

  while (true) {
    if (displayBanner) {
      Display.printBanner();
    }

    Display.printMenu();

    // Character type selection
    let charTypes: string[] = [];
    while (true) {
      const answers = await enquirer.prompt([
        {
          type: "input",
          name: "selection",
          message: "Selection",
          validate: (input) => input.trim() !== "" || "Please select at least one option",
        },
      ]);

      const selection = answers.selection as string;
      const choices = selection.split(",").map((x) => parseInt(x.trim()));

      try {
        if (choices.includes(5)) {
          charTypes = Object.keys(CHAR_SETS);
          break;
        } else if (choices.includes(6)) {
          charTypes = getRandomCharTypes();
          Display.printInfo(`Randomly selected: ${charTypes.join(", ")}`);
          break;
        } else if (choices.every((c) => c >= 1 && c <= 4)) {
          const typeMap: Record<number, string> = {
            1: "numbers",
            2: "lowercase",
            3: "uppercase",
            4: "special",
          };
          charTypes = [...new Set(choices.map((c) => typeMap[c]))];
          break;
        } else {
          Display.printError("Please enter numbers between 1-6");
        }
      } catch {
        Display.printError("Please enter comma-separated numbers");
      }
    }

    // Password length input
    console.log();
    let length = 0;
    while (true) {
      const answers = await enquirer.prompt([
        {
          type: "input",
          name: "length",
          message: "Password length (1-256)",
          validate: (input) => {
            const num = parseInt(input);
            if (isNaN(num) || num < 1 || num > 256) {
              return "Please enter a number between 1-256";
            }
            return true;
          },
        },
      ]);
      length = parseInt(answers.length as string);
      break;
    }

    // Password count input
    let count = 1;
    const countAnswers = await enquirer.prompt([
      {
        type: "input",
        name: "count",
        message: "Number of passwords (default: 1)",
        default: "1",
        validate: (input) => {
          const num = parseInt(input);
          if (isNaN(num) || num < 1) {
            return "Please enter a number >= 1";
          }
          return true;
        },
      },
    ]);
    count = parseInt(countAnswers.count as string);

    // Generate passwords
    const passwords: string[] = [];
    for (let i = 0; i < count; i++) {
      passwords.push(generatePassword(length, charTypes as any));
    }

    Display.printSelectedTypes(charTypes);

    if (count === 1) {
      Display.printPassword(passwords[0]);
      if (await copyToClipboard(passwords[0])) {
        Display.printSuccess("Copied to clipboard!");
      } else {
        Display.printInfo(
          "Clipboard not available. Install xclip or xsel on Linux."
        );
      }
    } else {
      Display.printPasswords(passwords);

      // Ask which password to copy
      const copyAnswers = await enquirer.prompt([
        {
          type: "input",
          name: "copyIndex",
          message: "Copy password to clipboard (1-N, or leave empty to skip)",
          validate: (input) => {
            if (input === "") return true;
            const num = parseInt(input);
            if (isNaN(num) || num < 1 || num > count) {
              return `Please enter a number between 1-${count}`;
            }
            return true;
          },
        },
      ]);

      const copyIndex = parseInt(copyAnswers.copyIndex as string);
      if (!isNaN(copyIndex) && copyIndex >= 1 && copyIndex <= count) {
        if (await copyToClipboard(passwords[copyIndex - 1])) {
          Display.printSuccess(`Password [${copyIndex}] copied to clipboard!`);
        } else {
          Display.printInfo("Clipboard not available.");
        }
      }
    }

    // Ask if they want to generate more
    const continueAnswers = await enquirer.prompt([
      {
        type: "confirm",
        name: "again",
        message: "Generate another password?",
        default: true,
      },
    ]);

    if (!continueAnswers.again) {
      return 0;
    }

    displayBanner = false;
  }
}
