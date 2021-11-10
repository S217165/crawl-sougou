#!/usr/bin/env python
"""
-- coding: utf-8 --
@File : main.py
@Software : PyCharm
@D6esc :用于Scrapy调试
"""

from scrapy.cmdline import execute
import sys
import os

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "collectBlogs"])
