"""
This module defines a custom pretty printer for lox standard output.
"""

import math


def pretty_print(value: object):

    if value is None:
        print("nil")
    elif isinstance(value, float) and value.is_integer():
        prefix = ""  # special case for negative integer zero.
        if value == 0.0 and math.copysign(1.0, value) < 0.0:
            prefix = "-"
        print(f"{prefix}{int(value)}")
    elif isinstance(value, bool):
        print("true" if value == True else "false")
    else:
        print(value)
