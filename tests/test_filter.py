# -*- coding: utf-8 -*-
import sys
import json
sys.path.insert(0, ".")
from sphinxcontrib.pandoc_markdown import post_process
from sphinxcontrib.pandoc_markdown import MarkdownParser


def test_image():
    markdown = """
![alt](path "title")
    """.strip()

    output = MarkdownParser.convert(markdown).strip()
    print(output)

#     markdown = """
# ![alt]("path" "caption")
# **caption!**
#     """.strip()
#
#     output = MarkdownParser.convert(markdown).strip()
#     print(output)


def test_bug_import():
    markdown = """
![alt](path "caption")
    """.strip()

    json_str = MarkdownParser.to_json(markdown).strip()
    json_obj = json.loads(json_str)
    print(json_obj)

    markdown = """
one
# two
    """.strip()

    json_str = MarkdownParser.to_json(markdown).strip()
    json_obj = json.loads(json_str)
    print(json_obj)