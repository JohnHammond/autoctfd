"""
Output functions for autoctfd

These functions are meant to acts as quick conveniences to output specific
kinds of messages
"""

from colorama import *
import sys

verbose = True


def fatal_error(message):
    if verbose:
        sys.stderr.write(
            f"[{Fore.RED}{Style.BRIGHT}!{Fore.RESET}{Style.RESET_ALL}] {message}\n"
        )
    sys.exit(1)


def success(message):
    if verbose:
        sys.stdout.write(
            f"[{Fore.GREEN}{Style.BRIGHT}!{Fore.RESET}{Style.RESET_ALL}] {message}\n"
        )


def info(message):
    if verbose:
        sys.stdout.write(
            f"[{Fore.BLUE}{Style.BRIGHT}+{Fore.RESET}{Style.RESET_ALL}] {message}\n"
        )
