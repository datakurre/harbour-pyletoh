# -*- coding: utf-8 -*-
def from_rgb(red, green, blue):
    """Return HTML color from RGB values"""
    return '#%02x%02x%02x' % (red, green, blue)


def to_rgb(s):
    """Return RGB tuple from HTML color value"""
    s = s.strip().strip('#')
    s += '0' * (6 - len(s))
    return int(s[:2], 16), int(s[2:4], 16), int(s[4:6], 16)
