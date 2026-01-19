import ora from "ora";
import fs from "fs";

const VERSION = "1.0.0";

export const Colors = {
  RESET: "\x1b[0m",
  BOLD: "\x1b[1m",
  DIM: "\x1b[2m",

  RED: "\x1b[31m",
  GREEN: "\x1b[32m",
  YELLOW: "\x1b[33m",
  BLUE: "\x1b[34m",
  MAGENTA: "\x1b[35m",
  CYAN: "\x1b[36m",
  WHITE: "\x1b[37m",

  BRIGHT_GREEN: "\x1b[92m",
  BRIGHT_YELLOW: "\x1b[93m",
  BRIGHT_CYAN: "\x1b[96m",
  BRIGHT_WHITE: "\x1b[97m",

  HIDE_CURSOR: "\x1b[?25l",
  SHOW_CURSOR: "\x1b[?25h",
  CLEAR_LINE: "\x1b[2K",
  MOVE_UP: "\x1b[1A",
};

export class Display {
  static readonly PASSGEN_ART = [
    "  ██████╗  █████╗ ███████╗███████╗ ██████╗ ███████╗███╗   ██╗  ",
    "  ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝ ██╔════╝████╗  ██║  ",
    "  ██████╔╝███████║███████╗███████╗██║  ███╗█████╗  ██╔██╗ ██║  ",
    "  ██╔═══╝ ██╔══██║╚════██║╚════██║██║   ██║██╔══╝  ██║╚██╗██║  ",
    "  ██║     ██║  ██║███████║███████║╚██████╔╝███████╗██║ ╚████║  ",
    "  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ",
  ];

  static printBanner(animate: boolean = true): void {
    console.log();

    if (!animate) {
      for (const artLine of Display.PASSGEN_ART) {
        console.log(`${Colors.BRIGHT_CYAN}${artLine}${Colors.RESET}`);
      }
      console.log(
        `${Colors.DIM}Secure Password Generator v1.0.0${Colors.RESET}`
      );
      console.log(`${Colors.DIM}Exit: Ctrl+C    Help: passgen --help${Colors.RESET}`);
      console.log();
      return;
    }

    // Hide cursor
    process.stdout.write(Colors.HIDE_CURSOR);

    try {
      // Show spinner during startup
      const spinner = ora({
        text: "",
        isEnabled: false,
      }).start();

      spinner.stop();

      // Print PASSGEN text lines
      for (const artLine of Display.PASSGEN_ART) {
        console.log(`${Colors.BRIGHT_CYAN}${artLine}${Colors.RESET}`);
      }

      console.log(
        `${Colors.DIM}Secure Password Generator v1.0.0${Colors.RESET}`
      );
      console.log(`${Colors.DIM}Exit: Ctrl+C    Help: passgen --help${Colors.RESET}`);
      console.log();
    } finally {
      process.stdout.write(Colors.SHOW_CURSOR);
    }
  }

  static printPassword(password: string, index?: number): void {
    console.log(`${Colors.BRIGHT_GREEN}${password}${Colors.RESET}`);
  }

  static printPasswords(passwords: string[]): void {
    console.log();
    passwords.forEach((password, index) => {
      console.log(
        `${Colors.DIM}[${index + 1}]${Colors.RESET} ${Colors.BRIGHT_GREEN}${password}${Colors.RESET}`
      );
    });
    console.log();
  }

  static printSuccess(message: string): void {
    console.log(`${Colors.BRIGHT_GREEN}✓${Colors.RESET} ${message}`);
  }

  static printError(message: string): void {
    console.log(`${Colors.RED}✗${Colors.RESET} ${message}`);
  }

  static printInfo(message: string): void {
    console.log(`${Colors.BRIGHT_CYAN}ℹ${Colors.RESET} ${message}`);
  }

  static printSelectedTypes(charTypes: string[]): void {
    const typeLabels: Record<string, string> = {
      numbers: "Numbers",
      lowercase: "Lowercase",
      uppercase: "Uppercase",
      special: "Special",
    };
    const labels = charTypes.map((t) => typeLabels[t] || t).join(", ");
    console.log(`${Colors.DIM}Character types: ${labels}${Colors.RESET}`);
  }

  static printMenu(): void {
    console.log(`
${Colors.BRIGHT_CYAN}${Colors.BOLD}Character Types:${Colors.RESET}
  ${Colors.CYAN}1${Colors.RESET}) Numbers (0-9)
  ${Colors.CYAN}2${Colors.RESET}) Lowercase (a-z)
  ${Colors.CYAN}3${Colors.RESET}) Uppercase (A-Z)
  ${Colors.CYAN}4${Colors.RESET}) Special characters
  ${Colors.CYAN}5${Colors.RESET}) All types
  ${Colors.CYAN}6${Colors.RESET}) Random types
    `);
  }

  static prompt(message: string): string {
    process.stdout.write(`${Colors.CYAN}${message}${Colors.RESET}: `);
    const buffer = Buffer.alloc(1024);
    const bytesRead = fs.readSync(0, buffer, 0, 1024, null);
    return buffer.toString("utf8", 0, bytesRead).trim();
  }
}
