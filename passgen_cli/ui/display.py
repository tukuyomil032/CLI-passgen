"""Display utilities for decorated CLI output."""

import sys
import time

from .. import __version__


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Cursor control
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR_LINE = "\033[2K"
    MOVE_UP = "\033[1A"


class Display:
    """Decorated display utilities for CLI output."""

    # Banner frame (static parts)
    BANNER_TOP = f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗{Colors.RESET}"
    BANNER_MID = f"{Colors.CYAN}╠═══════════════════════════════════════════════════════════════╣{Colors.RESET}"
    BANNER_BOT = f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}"
    BANNER_VER = f"{Colors.CYAN}║{Colors.DIM}              Secure Password Generator v1.0.0               {Colors.CYAN}║{Colors.RESET}"

    # PASSGEN ASCII art lines (content only, without border)
    PASSGEN_ART = [
        "  ██████╗  █████╗ ███████╗███████╗ ██████╗ ███████╗███╗   ██╗  ",
        "  ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝ ██╔════╝████╗  ██║  ",
        "  ██████╔╝███████║███████╗███████╗██║  ███╗█████╗  ██╔██╗ ██║  ",
        "  ██╔═══╝ ██╔══██║╚════██║╚════██║██║   ██║██╔══╝  ██║╚██╗██║  ",
        "  ██║     ██║  ██║███████║███████║╚██████╔╝███████╗██║ ╚████║  ",
        "  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ",
    ]

    @staticmethod
    def print_banner(animate: bool = True):
        """Print the application banner with optional animation."""
        print()  # Initial newline

        if not animate:
            # Print without animation
            print(Display.BANNER_TOP)
            for art_line in Display.PASSGEN_ART:
                print(f"{Colors.CYAN}║{Colors.BRIGHT_CYAN}{art_line}{Colors.CYAN}║{Colors.RESET}")
            print(Display.BANNER_MID)
            print(Display.BANNER_VER)
            print(Display.BANNER_BOT)
            # Print exit and help hint outside the box
            print(f"{Colors.DIM}Exit: Ctrl+C    Help: passgen --help{Colors.RESET}")
            print()
            return

        # Hide cursor during animation
        sys.stdout.write(Colors.HIDE_CURSOR)
        sys.stdout.flush()

        try:
            # Run startup spinner BEFORE drawing the box
            Display._copilot_startup()

            # Compute dynamic width based on ASCII art to avoid misalignment
            # Use the exact content width: PASSGEN_ART already includes
            # any desired left/right padding, so do not add extra padding here.
            content_width = max(len(line) for line in Display.PASSGEN_ART)
            inner_width = content_width

            # Build borders dynamically
            top = f"{Colors.CYAN}╔" + ("═" * inner_width) + f"╗{Colors.RESET}"
            mid = f"{Colors.CYAN}╠" + ("═" * inner_width) + f"╣{Colors.RESET}"
            bot = f"{Colors.CYAN}╚" + ("═" * inner_width) + f"╝{Colors.RESET}"
            ver_text = f" Secure Password Generator v{__version__} "
            ver_line = ver_text.center(inner_width)
            ver = f"{Colors.CYAN}║{Colors.DIM}{ver_line}{Colors.CYAN}║{Colors.RESET}"

            # Print top border
            print(top)

            # Animate PASSGEN text lines smoothly (pad/truncate to content_width)
            for art_line in Display.PASSGEN_ART:
                padded = art_line.ljust(content_width)[:content_width]
                Display._animate_passgen_line(padded, char_delay=0.002)
                time.sleep(0.035)

            # Print middle, version and bottom borders
            print(mid)
            print(ver)
            print(bot)

            # Print exit and help hint outside the box
            print(f"{Colors.DIM}Exit: Ctrl+C    Help: passgen --help{Colors.RESET}")
            print()
        finally:
            # Always show cursor again
            sys.stdout.write(Colors.SHOW_CURSOR)
            sys.stdout.flush()

    @staticmethod
    def _animate_passgen_line(content: str, char_delay: float = 0.0008):
        """Animate PASSGEN text line with left-to-right reveal."""
        # Print left border immediately
        sys.stdout.write(f"{Colors.CYAN}║{Colors.BRIGHT_CYAN}")
        sys.stdout.flush()

        # Animate content character by character
        for char in content:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(char_delay)

        # Print right border immediately
        print(f"{Colors.CYAN}║{Colors.RESET}")

    @staticmethod
    def _startup_spinner(duration: float = 0.6):
        """Display a small spinner for `duration` seconds."""
        spinner = "|/-\\"
        end_time = time.time() + duration
        sys.stdout.write(" ")
        sys.stdout.flush()
        i = 0
        while time.time() < end_time:
            ch = spinner[i % len(spinner)]
            sys.stdout.write(f"{Colors.BRIGHT_YELLOW}{ch}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.07)
            # erase spinner char
            sys.stdout.write("\b ")
            sys.stdout.write("\b")
            sys.stdout.flush()
            i += 1

    @staticmethod
    def _copilot_startup():
        """Show a short spinner line (npm-style thinking) then clear it.

        This displays a spinner on its own line and then erases the line so
        the ASCII box can be drawn cleanly without stray characters.
        """
        try:
            spinner = "|/-\\"
            duration = 0.9
            end_time = time.time() + duration
            i = 0
            # Host the spinner on the current (already-printed) blank line
            while time.time() < end_time:
                ch = spinner[i % len(spinner)]
                # carriage return to spinner line start, write char, flush
                sys.stdout.write(f"\r{Colors.BRIGHT_CYAN}{ch}{Colors.RESET}")
                sys.stdout.flush()
                time.sleep(0.08)
                i += 1

            # Clear the spinner line entirely before returning
            sys.stdout.write(f"\r{Colors.CLEAR_LINE}\r")
            sys.stdout.flush()
        except Exception:
            try:
                sys.stdout.write("\n")
                sys.stdout.flush()
            except Exception:
                pass

    @staticmethod
    def print_password(password: str, index: int = None):
        """Print a generated password with decoration."""
        if index is not None:
            prefix = f"{Colors.DIM}[{index}]{Colors.RESET} "
        else:
            prefix = ""

        print(f"""
{Colors.CYAN}┌{'─' * (len(password) + 4)}┐{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.BRIGHT_GREEN}{Colors.BOLD}{password}{Colors.RESET}  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}└{'─' * (len(password) + 4)}┘{Colors.RESET}
""")

    @staticmethod
    def print_passwords(passwords: list[str]):
        """Print multiple passwords with decoration."""
        print(f"\n{Colors.CYAN}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}  Generated Passwords{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 50}{Colors.RESET}\n")

        for i, password in enumerate(passwords, 1):
            print(f"  {Colors.DIM}[{i}]{Colors.RESET} {Colors.BRIGHT_GREEN}{Colors.BOLD}{password}{Colors.RESET}")

        print(f"\n{Colors.CYAN}{'═' * 50}{Colors.RESET}\n")

    @staticmethod
    def print_success(message: str):
        """Print a success message."""
        print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

    @staticmethod
    def print_error(message: str):
        """Print an error message."""
        print(f"{Colors.RED}✗ Error: {message}{Colors.RESET}")

    @staticmethod
    def print_info(message: str):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")

    @staticmethod
    def print_help(text: str):
        """Print help text with improved coloring for readability."""
        import re

        # Header
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}Help{Colors.RESET}\n")
        # Enhance help text: show uppercase variants for long options and colorize
        for line in text.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("-"):
                # Split option definitions from description by two-or-more spaces
                parts = re.split(r"\s{2,}", stripped, maxsplit=1)
                opt_field = parts[0]
                rest = parts[1] if len(parts) > 1 else ""

                # Replace each option token (short or long) with dual-case variant
                def _dual_token(m):
                    s = m.group(0)
                    return f"{s} / {s.upper()}"

                opt_disp = re.sub(r"-{1,2}[A-Za-z0-9][A-Za-z0-9\-]*(?:=[A-Za-z0-9_\-]+)?", _dual_token, opt_field)

                print(f"  {Colors.CYAN}{opt_disp}{Colors.RESET} {Colors.DIM}{rest}{Colors.RESET}")
            else:
                print(f"{Colors.DIM}{line}{Colors.RESET}")

    @staticmethod
    def print_examples(examples: list[str]):
        """Print a short examples block with highlighting."""
        print(f"\n{Colors.BRIGHT_CYAN}{Colors.BOLD}Examples:{Colors.RESET}")
        for ex in examples:
            # highlight flags within example
            parts = ex.split()
            out = []
            for p in parts:
                if p.startswith("-"):
                    out.append(f"{Colors.CYAN}{p}{Colors.RESET}")
                else:
                    out.append(p)
            print("  " + " ".join(out))

    @staticmethod
    def print_selected_types(char_types: list[str]):
        """Print selected character types."""
        type_display = {
            "numbers": "0-9",
            "lowercase": "a-z",
            "uppercase": "A-Z",
            "special": "!@#"
        }
        selected = [type_display.get(t, t) for t in char_types]
        print(f"{Colors.DIM}  Character types: [{', '.join(selected)}]{Colors.RESET}")

    @staticmethod
    def print_menu():
        """Print the character type selection menu."""
        print(f"""
{Colors.BRIGHT_CYAN}Select character types{Colors.RESET} {Colors.DIM}(comma-separated, e.g., 1,2,3){Colors.RESET}

  {Colors.YELLOW}1.{Colors.RESET} Numbers      {Colors.DIM}(0-9){Colors.RESET}
  {Colors.YELLOW}2.{Colors.RESET} Lowercase    {Colors.DIM}(a-z){Colors.RESET}
  {Colors.YELLOW}3.{Colors.RESET} Uppercase    {Colors.DIM}(A-Z){Colors.RESET}
  {Colors.YELLOW}4.{Colors.RESET} Special      {Colors.DIM}(!@#$%...){Colors.RESET}
  {Colors.CYAN}───────────────────────{Colors.RESET}
  {Colors.GREEN}5.{Colors.RESET} All          {Colors.DIM}(1+2+3+4){Colors.RESET}
  {Colors.MAGENTA}6.{Colors.RESET} Random       {Colors.DIM}(surprise me!){Colors.RESET}
""")

    @staticmethod
    def prompt(message: str) -> str:
        """Display a prompt and return user input."""
        try:
            return input(f"{Colors.BRIGHT_WHITE}▸ {message}: {Colors.RESET}").strip()
        except KeyboardInterrupt:
            # Delegate handling to the interrupt module if available.
            try:
                # Import here to avoid circular imports at module import time
                from .. import interrupt as _interrupt
                _interrupt.handle_keyboard_interrupt()
            except Exception:
                # Fallback: print a newline and return empty input
                print()
            return ""
