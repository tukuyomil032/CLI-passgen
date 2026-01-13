"""Interactive mode for password generation."""

from ..core import generate_password, get_random_char_types, CHAR_SETS, copy_to_clipboard
from .display import Display, Colors


def interactive_mode(show_banner: bool = True):
    """Run interactive mode for password generation.

    Args:
        show_banner: If False, do not display the PASSGEN logo/banner on start.
    """
    # local toggle to control whether banner shows on subsequent loops
    display_banner = show_banner

    while True:
        if display_banner:
            Display.print_banner()

        Display.print_menu()

        # Character type selection
        while True:
            selection = Display.prompt("Selection")
            if not selection:
                Display.print_error("Please select at least one option")
                continue

            try:
                choices = [int(x.strip()) for x in selection.split(",")]

                # Handle special options
                if 5 in choices:  # All
                    char_types = list(CHAR_SETS.keys())
                    break
                elif 6 in choices:  # Random
                    char_types = get_random_char_types()
                    Display.print_info(f"Randomly selected: {', '.join(char_types)}")
                    break
                elif all(1 <= c <= 4 for c in choices):
                    type_map = {1: "numbers", 2: "lowercase", 3: "uppercase", 4: "special"}
                    char_types = list(set(type_map[c] for c in choices))
                    break
                else:
                    Display.print_error("Please enter numbers between 1-6")
                    continue
            except ValueError:
                Display.print_error("Please enter comma-separated numbers")
                continue

        # Password length input
        print()
        while True:
            length_input = Display.prompt("Password length (1-256)")
            try:
                length = int(length_input)
                if 1 <= length <= 256:
                    break
                Display.print_error("Please enter a number between 1-256")
            except ValueError:
                Display.print_error("Please enter a valid number")

        # Password count input
        while True:
            count_input = Display.prompt("Number of passwords (default: 1)")
            if not count_input:
                count = 1
                break
            try:
                count = int(count_input)
                if count >= 1:
                    break
                Display.print_error("Please enter a number >= 1")
            except ValueError:
                Display.print_error("Please enter a valid number")

        # Generate passwords (handle Ctrl+C during generation)
        passwords = []
        try:
            for _ in range(count):
                passwords.append(generate_password(length, char_types))
        except KeyboardInterrupt:
            # Delegate to interrupt handler; if it returns, treat as cancellation
            try:
                from .. import interrupt as _interrupt
                _interrupt.handle_keyboard_interrupt()
            except Exception:
                pass
            return 1

        Display.print_selected_types(char_types)

        if count == 1:
            Display.print_password(passwords[0])
            # Auto copy single password
            if copy_to_clipboard(passwords[0]):
                Display.print_success("Copied to clipboard!")
            else:
                Display.print_info("Clipboard not available. Install xclip or xsel on Linux.")
        else:
            Display.print_passwords(passwords)
            # Ask which password to copy
            _prompt_and_copy(passwords)

        # After one generation, ask whether to continue (require explicit y/n)
        while True:
            cont = Display.prompt("Continue template mode? (y/n)")
            if not cont:
                Display.print_error("Please enter 'y' or 'n'")
                continue
            cont = cont.strip().lower()
            if cont in ('y', 'n'):
                break
            Display.print_error("Please enter 'y' or 'n'")

        if cont == 'y':
            # Do not re-show the big PASSGEN logo on continue
            display_banner = False
            continue
        return 0


def _prompt_and_copy(passwords: list[str]):
    """Prompt user to select which password to copy."""
    print()
    while True:
        choice = Display.prompt(f"Copy to clipboard? (1-{len(passwords)}, 'a' for all, Enter to skip)")

        if not choice:
            # Skip copying
            return

        if choice.lower() == 'a':
            # Copy all passwords (one per line)
            all_passwords = "\n".join(passwords)
            if copy_to_clipboard(all_passwords):
                Display.print_success("All passwords copied to clipboard!")
            else:
                Display.print_error("Failed to copy to clipboard")
            return

        try:
            idx = int(choice)
            if 1 <= idx <= len(passwords):
                if copy_to_clipboard(passwords[idx - 1]):
                    Display.print_success(f"Password [{idx}] copied to clipboard!")
                else:
                    Display.print_error("Failed to copy to clipboard")
                return
            else:
                Display.print_error(f"Please enter a number between 1-{len(passwords)}")
        except ValueError:
            Display.print_error("Please enter a valid number, 'a', or press Enter to skip")
