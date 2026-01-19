import crypto from "crypto";
import { CHAR_SETS, CharType } from "./constants.js";

export function generatePassword(length: number, charTypes: CharType[]): string {
  const allChars = charTypes
    .map((ct) => CHAR_SETS[ct])
    .join("");

  if (!allChars) {
    throw new Error("At least one character type must be selected");
  }

  let password = "";
  for (let i = 0; i < length; i++) {
    const randomIndex = crypto.randomInt(0, allChars.length);
    password += allChars[randomIndex];
  }
  return password;
}

export function getRandomCharTypes(): CharType[] {
  const allTypes: CharType[] = ["numbers", "lowercase", "uppercase", "special"];
  const numTypes = crypto.randomInt(1, allTypes.length + 1);

  // Fisher-Yates shuffle to select random types
  const shuffled = [...allTypes];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = crypto.randomInt(0, i + 1);
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }

  return shuffled.slice(0, numTypes);
}
