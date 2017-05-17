# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, ".")
from sphinxcontrib.pandoc_markdown import post_process
from sphinxcontrib.pandoc_markdown import MarkdownParser


def test_bug_import():
    markdown = """
@import "test.csv"
@import "test.csv"
    """.strip()

    ans = """
.. csv-table::
    :file: test.csv
    :header-rows: 1

.. csv-table::
    :file: test.csv
    :header-rows: 1
    """.strip()
    assert ans == MarkdownParser.convert(markdown).strip()


