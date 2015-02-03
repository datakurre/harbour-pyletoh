# -*- coding: utf-8 -*-
try:
    import pydevd
    pydevd.settrace('localhost', port=50000, stdoutToServer=True, stderrToServer=True)  # noqa
except ImportError:
    pass
