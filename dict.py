#!/usr/bin/env python3
'''Dict application.
'''
from collections import OrderedDict
from typing import Optional
from os import path
import datetime
import os
import re
import readline as _
import sys


HOME_DIR = os.environ['HOME']

AUTHOR: str = 'Torgeir Børresen'
LOG_FILE = path.join(HOME_DIR, 'dict.log')


def show_author_subject():
    '''Display author and subject.'''
    print('Author:', AUTHOR)
    subject = get_last_subject()
    print('Subject:', subject)


def show_available_commands(file=sys.stdout, isatty=False):
    '''Display program commands on file.

    If isatty, use colors.
    '''
    out_fmt = '\t{col_emph:s}{cmd:{cmd_width:d}s}{col_normal:s}: {usage:20s}\n'
    heightened = '\u001b[31m' if isatty else ''
    reset = '\u001b[0m' if isatty else ''
    commands = OrderedDict([
        ('l[og]', 'dict l'),
        ('w[rite]', 'dict w'),
        ('s[earch]', 'dict s `regexp`'),
    ])
    cmd_str = ''
    cmd_width = max((len(c) for c in commands.keys()))
    for cmd, usage in commands.items():
        cmd_str += out_fmt.format(
            col_emph=heightened, col_normal=reset,
            cmd=cmd, cmd_width=cmd_width + 1, usage=usage,
        )
    print('Usage:', file=file)
    print(cmd_str, file=file, end='')


def get_last_subject() -> Optional[str]:
    '''Get last subject.'''
    line: Optional[str] = None
    if not path.exists(LOG_FILE):
        return None
    with open(LOG_FILE, 'r') as f:
        for line in f:
            continue
    if line is None:
        return None
    entries = line.strip().split('\t')
    return entries[1]


def log_write():
    '''Emit log.'''
    timestamp: str = datetime.datetime.now().isoformat()
    default_subject: Optional[str] = get_last_subject()
    subject_msg = 'subject (default: {default:s}): '.format(
        default=str(default_subject))
    subject: str = ''
    while not subject:
        subject = input(subject_msg).strip()
        if (not subject) and default_subject:
            subject = default_subject

    log_entry: str = ''
    while not log_entry:
        log_entry = input('log: ').strip().replace('\t', ' ')
    with open(LOG_FILE, 'a') as f:
        print(timestamp, subject, log_entry, sep='\t', file=f)


def log_search(log_fn, regex, out_buf, isatty=False):
    heightened = '\u001b[31m' if isatty else ''
    reset = '\u001b[0m' if isatty else ''
    exp = re.compile(regex)
    with open(log_fn, 'r') as f:
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
                    file=out_buf,
                )


def display_log(buf, isatty=False):
    default_subject: Optional[str] = get_last_subject()
    if not default_subject:
        sys.exit(0)
    regexp = '\t' + default_subject + '\t'
    log_search(LOG_FILE, regexp, buf, isatty)
    sys.exit(0)


if __name__ == '__main__':
    tty = sys.stdout.isatty()
    if len(sys.argv) == 1:
        show_author_subject()
        print()
        show_available_commands(file=sys.stdout, isatty=tty)
        sys.exit(0)
    elif sys.argv[1] in ('w', 'write'):
        log_write()
        sys.exit(0)
    elif sys.argv[1] in ('s', 'search'):
        if len(sys.argv) < 3:
            show_available_commands(file=sys.stderr, isatty=tty)
            sys.exit(1)
        log_search(LOG_FILE, sys.argv[2], sys.stdout, tty)
    elif sys.argv[1] in ('l', 'log'):
        display_log(buf=sys.stdout, isatty=tty)
