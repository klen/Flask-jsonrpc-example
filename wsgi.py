#!/usr/bin/env python
# coding: utf-8

import sys
import os

sys.stdin = sys.stdout

BASE_DIR = os.path.join(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from api import create_app

application = create_app()
