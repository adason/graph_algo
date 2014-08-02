# -*- coding: utf-8 -*-
"""Test the CLI"""


from __future__ import unicode_literals
import pytest
from subprocess import check_output
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


def run_cmd(cmd):
    """Run a shell command `cmd` and return its output."""
    return check_output(cmd, shell=True).decode('utf-8')


def test_echo():
    """An example test."""
    result = run_cmd("echo hello world")
    assert result == "hello world\n"