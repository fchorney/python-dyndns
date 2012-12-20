#!/usr/bin/env python

def get_yes_no(msg):
    """
    Prompts the user with msg.
    Returns true on "y" and false on "n"
    """
    value = None
    while value is None:
        value = raw_input(msg).lower()
        if value is not None and len(value) > 0:
            value = value[0]
        if value != 'y' and value != 'n':
            value = None
    return value == 'y'
