#!/usr/bin/env python3
from typing import Optional
from os import path
import datetime
import os
import re
import readline
import sqlite3
import sys


HOME_DIR = os.environ["HOME"]

AUTHOR: str = "Torgeir Børresen"
LOG_FILE = path.join(HOME_DIR, "dict.log")


def show_author_subject():
    """Display author and subject."""
    print("Author:", AUTHOR)
    subject = get_last_subject()
    print("Subject:", subject)


def get_last_subject() -> Optional[str]:
    """Get last subject."""
    line: Optional[str] = None
    if not path.exists(LOG_FILE):
        return None
    with open(LOG_FILE, "r") as f:
        for line in f:
            continue
    if line is None:
        return None
    entries = line.strip().split("\t")
    return entries[1]


def log_write():
    """Emit log."""
    timestamp: str = datetime.datetime.now().isoformat()
    default_subject: Optional[str] = get_last_subject()
    subject_msg = "subject (default: {default:s}): ".format(
        default=str(default_subject))
    subject: str = ''
    while not subject:
        subject = input(subject_msg).strip()
        if (not subject) and default_subject:
            subject = default_subject

    log_entry: str = ''
    while not log_entry:
        log_entry = input("log: ").strip()
    with open(LOG_FILE, "a") as f:
        print(timestamp, subject, log_entry, sep="\t", file=f)


def log_search(filename, regex, isatty=False):
    heightened = "\u001b[31m" if isatty else ""
    reset = "\u001b[0m" if isatty else ""
    exp = re.compile(regex)
    with open(filename, "r") as f:
        for line in f:
            match = exp.search(line)
            if match:
                s = match.start(0)
                e = match.end(0)
                print(
                    line[:s],
                    heightened, line[s:e], reset,
                    line[e:],
                    sep='', end='',
                )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_author_subject()
        exit(0)
    elif sys.argv[1] == "w":
        log_write()
        exit(0)
    elif sys.argv[1] == "s":
        if len(sys.argv) < 2:
            print("usage: dict s `regexp`", file=sys.stderr)
            exit(1)
        log_search(LOG_FILE, sys.argv[2], sys.stdout.isatty())
