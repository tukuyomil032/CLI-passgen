#!/usr/bin/env python3
"""passgen-cli - A customizable password generator CLI tool.

This module provides a REPL-style interactive shell when invoked with no
arguments. In that shell all lines entered are treated as `passgen` commands
until the user exits (double Ctrl+C or 'exit'). The alias `pg` is accepted
as a shorthand for `passgen` inside the shell.
"""

import argparse
import shlex
import sys
import os
try:
    import readline
except Exception:
    readline = None

from . import __version__
from .core import generate_password, get_random_char_types, CHAR_SETS, copy_to_clipboard
from .ui import Display, interactive_mode
from . import interrupt

# Initialize interrupt handling (sets SIGINT handler)
interrupt.init(Display)


def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="passgen",
        description="A customizable password generator CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  passgen                              Interactive mode
  passgen -l 16                        16 chars with all character types
  passgen -l 20 -n -a                  20 chars with numbers and lowercase
  passgen -l 32 -n -a -A -s            32 chars with all types
  passgen -l 16 -c 5                   Generate 5 passwords of 16 chars
  passgen -l 24 -r                     24 chars with random character types
  passgen -l 16 --no-copy              Disable auto-copy to clipboard
        """
    )

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-l", "--length", type=int, metavar="N", help="Password length (1-256)")
    parser.add_argument("-c", "--count", type=int, default=1, metavar="N", help="Number of passwords to generate (default: 1)")
    parser.add_argument("-n", "--numbers", action="store_true", help="Include numbers (0-9)")
    parser.add_argument("-a", "--lowercase", action="store_true", help="Include lowercase letters (a-z)")
    parser.add_argument("-A", "--uppercase", action="store_true", help="Include uppercase letters (A-Z)")
    parser.add_argument("-s", "--special", action="store_true", help="Include special characters")
    parser.add_argument("-r", "--random", action="store_true", help="Use random character types")
    parser.add_argument("-q", "--quiet", action="store_true", help="Output only passwords (for scripting)")
    parser.add_argument("--no-copy", action="store_true", help="Disable auto-copy to clipboard")
    parser.add_argument("--copy", type=int, metavar="N", help="Copy Nth password to clipboard (use with -c)")
    parser.add_argument("--temp", action="store_true", help="Temporarily enter interactive menu (REPL only)")

    return parser


def _normalize_tokens(tokens: list[str]) -> list[str]:
    """Normalize long option tokens to lowercase to allow case-insensitive options."""
    out = []
    for tok in tokens:
        if tok.startswith("--"):
            if "=" in tok:
                k, v = tok.split("=", 1)
                out.append("--" + k[2:].lower() + "=" + v)
            else:
                out.append("--" + tok[2:].lower())
        elif tok.startswith("-") and not tok.startswith("--"):
            # Short options: lowercase all alphabetic chars after the dash
            prefix = "-"
            rest = tok[1:]
            new_rest_chars = []
            for ch in rest:
                if ch.isalpha():
                    new_rest_chars.append(ch.lower())
                else:
                    new_rest_chars.append(ch)
            out.append(prefix + "".join(new_rest_chars))
        else:
            out.append(tok)
    return out


def _normalize_tokens_for_parser(parser: argparse.ArgumentParser, tokens: list[str]) -> list[str]:
    """Normalize tokens with awareness of parser-defined options.

    This will lowercase long options unconditionally, but for short options
    it will prefer the exact token if the parser accepts it; otherwise it
    will try a lowercase variant so users can type either case for single
    letter options when the parser only defines the lowercase form.
    """
    out = []
    valid_opts = set(parser._option_string_actions.keys())

    for tok in tokens:
        if tok.startswith("--"):
            # lowercase long options
            if "=" in tok:
                k, v = tok.split("=", 1)
                out.append("--" + k[2:].lower() + "=" + v)
            else:
                out.append("--" + tok[2:].lower())
            continue

        if tok.startswith("-") and not tok.startswith("--"):
            # if parser already accepts this exact short token, keep it
            if tok in valid_opts:
                out.append(tok)
                continue

            # otherwise try a lowercase variant (map letters to lower)
            prefix = "-"
            rest = tok[1:]
            new_rest = "".join(ch.lower() if ch.isalpha() else ch for ch in rest)
            cand = prefix + new_rest
            if cand in valid_opts:
                out.append(cand)
            else:
                out.append(tok)
            continue

        out.append(tok)

    return out


def _execute_command(args, default_length: int | None = None) -> int:
    """Execute generation logic for parsed `args`.

    If `default_length` is provided and `args.length` is None, it will be
    used so that simple flag-based commands can generate without invoking the
    interactive flow.
    """
    # Interactive mode if no length specified and no default provided
    if args.length is None:
        if default_length is None:
            return interactive_mode()
        args.length = default_length

    # Validate length
    if not 1 <= args.length <= 256:
        Display.print_error("Password length must be between 1-256")
        return 1

    if args.count < 1:
        Display.print_error("Count must be at least 1")
        return 1

    # Determine character types
    if args.random:
        char_types = get_random_char_types()
        if not args.quiet:
            Display.print_info(f"Randomly selected: {', '.join(char_types)}")
    else:
        char_types = []
        if args.numbers:
            char_types.append("numbers")
        if args.lowercase:
            char_types.append("lowercase")
        if args.uppercase:
            char_types.append("uppercase")
        if args.special:
            char_types.append("special")

        # Use all types if none specified
        if not char_types:
            char_types = list(CHAR_SETS.keys())

    # Generate passwords (handle KeyboardInterrupt during generation)
    passwords = []
    try:
        for _ in range(args.count):
            passwords.append(generate_password(args.length, char_types))
    except KeyboardInterrupt:
        # Delegate to interrupt handler which may exit or reset
        interrupt.handle_keyboard_interrupt()
        return 1

    # Output
    if args.quiet:
        for password in passwords:
            print(password)
    elif args.count == 1:
        Display.print_password(passwords[0])
    else:
        Display.print_passwords(passwords)

    # Handle clipboard
    if not args.quiet and not args.no_copy:
        if args.copy:
            # Copy specific password
            if 1 <= args.copy <= len(passwords):
                if copy_to_clipboard(passwords[args.copy - 1]):
                    Display.print_success(f"Password [{args.copy}] copied to clipboard!")
            else:
                Display.print_error(f"Invalid password number: {args.copy}")
        elif args.count == 1:
            # Auto-copy single password
            if copy_to_clipboard(passwords[0]):
                Display.print_success("Copied to clipboard!")
        else:
            # Multiple passwords - prompt for selection
            _prompt_and_copy(passwords)

    return 0


def _prompt_and_copy(passwords: list[str]):
    """Prompt user to select which password to copy."""
    while True:
        choice = Display.prompt(f"Copy to clipboard? (1-{len(passwords)}, 'a' for all, Enter to skip)")

        if not choice:
            return

        if choice.lower() == 'a':
            all_passwords = "\n".join(passwords)
            if copy_to_clipboard(all_passwords):
                Display.print_success("All passwords copied to clipboard!")
            return

        try:
            idx = int(choice)
            if 1 <= idx <= len(passwords):
                if copy_to_clipboard(passwords[idx - 1]):
                    Display.print_success(f"Password [{idx}] copied to clipboard!")
                return
            else:
                Display.print_error(f"Please enter 1-{len(passwords)}")
        except ValueError:
            Display.print_error("Enter a number, 'a', or press Enter to skip")


def interactive_repl():
    """REPL where each entered line is treated as a `passgen` command.

    Alias `pg` is accepted. Typing `--temp` (or including `--temp`) will invoke
    the temporary interactive menu (`interactive_mode`). The REPL exits on
    double Ctrl+C (handled globally) or typing `exit`/`quit`.
    """

    parser = _get_parser()

    # Enable readline-based history/navigation if available
    histfile = os.path.expanduser("~/.passgen_history")
    if readline:
        try:
            readline.parse_and_bind('tab: complete')
            if os.path.exists(histfile):
                try:
                    readline.read_history_file(histfile)
                except Exception:
                    pass
        except Exception:
            pass

    # Initial banner and examples
    Display.print_banner()
    Display.print_examples([
        "passgen -l 16 -a -A -n -s -c 5",
        "passgen --temp",
        "pg -l 12 -r -c 3",
    ])

    while True:
        try:
            line = Display.prompt("passgen")
        except KeyboardInterrupt:
            # interrupt module prints confirmation; continue REPL
            continue

        if not line:
            continue

        # simple exit commands
        if line.strip() in ("exit", "quit"):
            return 0

        try:
            tokens = shlex.split(line)
        except ValueError:
            Display.print_error("Failed to parse command")
            continue

        # Support alias 'pg' and full 'passgen' token at start (case-insensitive)
        if tokens and tokens[0].lower() in ("pg", "passgen"):
            tokens = tokens[1:]

        # Normalize tokens (long and short options) to be case-insensitive
        tokens = _normalize_tokens_for_parser(parser, tokens)

        if not tokens:
            continue

        # If user requested temporary interactive flow
        if "--temp" in tokens:
            # Run interactive menu without showing the big PASSGEN banner
            interactive_mode(show_banner=False)
            continue

        # If user asked for help, print colored help
        if any(t.lower() in ("-h", "--help") for t in tokens):
            try:
                Display.print_help(parser.format_help())
            except Exception:
                Display.print_info("Help unavailable")
            continue

        # Parse args and execute; in REPL we provide a sensible default length
        try:
            args = parser.parse_args(tokens)
        except SystemExit:
            # argparse prints help or error; continue REPL
            continue

        # In REPL, if length isn't provided, default to 16 so flags can be used directly
        _execute_command(args, default_length=16)

        # persist history after each command
        if readline:
            try:
                readline.write_history_file(histfile)
            except Exception:
                pass


def main():
    parser = _get_parser()
    # Normalize options for one-shot invocation using parser-aware normalization
    norm_argv = [sys.argv[0]] + _normalize_tokens_for_parser(parser, sys.argv[1:])
    # If the user requested help in the one-shot invocation, print colored help
    if any(a in ("-h", "--help") for a in norm_argv[1:]):
        try:
            Display.print_help(parser.format_help())
        except Exception:
            # fallback to argparse behavior
            args = parser.parse_args(norm_argv[1:])
        return 0

    try:
        args = parser.parse_args(norm_argv[1:])
    except SystemExit:
        # argparse already printed errors/help; propagate exit code
        raise

    # If user requested temporary interactive menu in one-shot mode
    if getattr(args, "temp", False):
        interactive_mode(show_banner=False)
        return 0

    # Interactive REPL if no length specified and no other args provided
    if len(sys.argv) == 1:
        return interactive_repl()

    # Otherwise execute normally as single-invocation CLI
    return _execute_command(args)


if __name__ == "__main__":
    sys.exit(main())
