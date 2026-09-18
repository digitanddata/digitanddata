"""
Entry point for GoDaddy cPanel "Setup Python App" (Passenger) hosting.
Passenger imports this file and looks for an `application` callable.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from digitanddata.wsgi import application  # noqa: E402
