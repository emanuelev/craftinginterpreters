"""
This module defines a custom pretty printer for lox standard output.
"""

def pretty_print(value: object):

    if value is None:
        print('nil')
    elif isinstance(value, float) and value.is_integer():
        print(int(value))
    else:
        print(value)
