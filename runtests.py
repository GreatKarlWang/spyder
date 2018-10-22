# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""
Script for running Spyder tests programmatically.
"""

# Standard library imports
import os
import sys
import argparse

# Third party imports
import pytest


# To run our slow tests only in our CIs
RUN_CI = os.environ.get('CI', None) is not None
run_slow = RUN_CI


def main(run_slow=run_slow, extra_args=None):
    """
    Run pytest tests for Spyder.
    """
    pytest_args = ['spyder',
                   'spyder_profiler',
                   '-vv',
                   '-rw',
                   '--durations=10']

    if RUN_CI:
        pytest_args.append('-x')
    elif extra_args:
        pytest_args += extra_args
    if run_slow and '--run-slow' not in pytest_args:
        pytest_args.append('--run-slow')

    print("Pytest Arguments: " + str(pytest_args))
    errno = pytest.main(pytest_args)

    # sys.exit doesn't work here because some things could be running in the
    # background (e.g. closing the main window) when this point is reached.
    # If that's the case, sys.exit doesn't stop the script as you would expect.
    if errno != 0:
        raise SystemExit(errno)


if __name__ == '__main__':
    test_parser = argparse.ArgumentParser(
        usage='python runtests.py [--run-slow] [-- pytest_args]')
    test_parser.add_argument('--run-slow', action='store_true',
                             default=run_slow,
                             help='Run the slow (mainly GUI/functional) tests')
    test_parser.add_argument('pytest_args', nargs='*',
                             help="Args to pass to pytest")
    test_args = test_parser.parse_args()
    main(run_slow=test_args.run_slow, extra_args=test_args.pytest_args)
