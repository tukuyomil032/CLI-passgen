import { execSync } from "child_process";
import { platform } from "os";
import clipboardy from "clipboardy";

export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await clipboardy.write(text);
    return true;
  } catch {
    return false;
  }
}

export function isClipboardAvailable(): boolean {
  const sys = platform();

  try {
    if (sys === "darwin") {
      execSync("which pbcopy", { stdio: "pipe" });
      return true;
    } else if (sys === "linux") {
      try {
        execSync("which xclip", { stdio: "pipe" });
        return true;
      } catch {
        try {
          execSync("which xsel", { stdio: "pipe" });
          return true;
        } catch {
          return false;
        }
      }
    } else if (sys === "win32") {
      return true;
    }
    return false;
  } catch {
    return false;
  }
}
