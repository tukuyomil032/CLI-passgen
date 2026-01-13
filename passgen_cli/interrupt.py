"""Graceful SIGINT handling with double-press-to-exit logic.

Usage:
  import passgen_cli.interrupt as interrupt
  interrupt.init(Display)

This module provides a signal handler that, on first Ctrl+C, prints a
confirmation message and starts a 5-second window; pressing Ctrl+C again
within that window exits the program.
"""
from __future__ import annotations

import signal
import sys
import threading
import time
from typing import Optional

_display = None
_last_sigint: float = 0.0
_lock = threading.Lock()
_timer: Optional[threading.Timer] = None
_WINDOW = 5.0


def init(display_class) -> None:
    """Initialize interrupt handling and register the SIGINT handler.

    Pass the Display class (or any object exposing a `print_info` method)
    so messages use the app's output style.
    """
    global _display
    _display = display_class
    signal.signal(signal.SIGINT, _signal_handler)


def _reset_last_sigint() -> None:
    global _last_sigint, _timer
    with _lock:
        _last_sigint = 0.0
        if _timer:
            try:
                _timer.cancel()
            except Exception:
                pass
            _timer = None


def _signal_handler(signum, frame) -> None:
    """Signal handler invoked on SIGINT.

    This handler tries to be lightweight: it delegates to
    ``handle_keyboard_interrupt`` which contains the main logic.
    """
    handle_keyboard_interrupt()


def handle_keyboard_interrupt() -> None:
    """Handle a KeyboardInterrupt-like event.

    - On first call: record timestamp, show a confirmation message, and
      start/reset a timer that clears the timestamp after the window.
    - If called again within the window: exit the process.
    """
    global _last_sigint, _timer
    now = time.time()
    with _lock:
        if _last_sigint and (now - _last_sigint) <= _WINDOW:
            # Second press within window -> exit
            try:
                if _display and hasattr(_display, "print_info"):
                    _display.print_info("Exiting...")
            except Exception:
                pass
            sys.exit(1)

        # First press: set timestamp and print confirmation
        _last_sigint = now
        try:
            if _display and hasattr(_display, "print_info"):
                _display.print_info("Press Ctrl+C again within 5 seconds to exit")
            else:
                print("Press Ctrl+C again within 5 seconds to exit")
        except Exception:
            print("Press Ctrl+C again within 5 seconds to exit")

        # Start/reset timer to clear the timestamp after the window
        try:
            if _timer:
                _timer.cancel()
        except Exception:
            pass

        _timer = threading.Timer(_WINDOW, _reset_last_sigint)
        _timer.daemon = True
        _timer.start()
