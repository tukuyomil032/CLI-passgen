export const CHAR_SETS = {
  numbers: "0123456789",
  lowercase: "abcdefghijklmnopqrstuvwxyz",
  uppercase: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
  special: '!"@#$%^&*()_+-=[]\\{}|;:\'",.<>?/`~',
} as const;

export type CharType = keyof typeof CHAR_SETS;

export const CHAR_TYPE_NAMES = {
  numbers: "Numbers (0-9)",
  lowercase: "Lowercase (a-z)",
  uppercase: "Uppercase (A-Z)",
  special: "Special characters",
} as const;
