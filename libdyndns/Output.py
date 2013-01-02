#!/usr/bin/env python

from sys import stderr, stdout, exit as sysexit

LEVELS = {
    'extra': 3,
    'debug': 2,
    'info' : 1
}

def print_date():
    if not hasattr(print_date, 'has_been_called'):
        from datetime import datetime
        date = datetime.now().strftime("%A %B %d, %Y %I:%M:%S.%f %p")
        print >> stderr, date
        setattr(print_date, 'has_been_called', True)


def error(msg):
    """Print msg to stderr"""
    print_date()
    print >> stderr, 'Error: %s' % msg


def message(msg):
    """Always print msg to stdout"""
    print_date()
    print >> stdout, msg


def exit(return_code=0, msg=None):
    """Print msg to stderr and exit with return_code"""
    if msg is not None:
        error(msg)
    sysexit(return_code)


def extra(verbosity, msg):
    """Only print msg if verbosity is level extra or higher"""
    if verbosity >= LEVELS['extra']:
        message(msg)


def debug(verbosity, msg):
    """Only print msg if verbosity is level debug or higher"""
    if verbosity >= LEVELS['debug']:
        message(msg)


def info(verbosity, msg):
    """Only print msg if verbosity is level info or higher"""
    if verbosity >= LEVELS['info']:
        message(msg)
