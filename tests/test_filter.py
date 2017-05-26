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
    # print(json_obj)
    # print(json_obj.keys())
    # print(json_obj["blocks"])
    # print(json_obj["blocks"][0]["c"][0]["c"])
    # assert ans == MarkdownParser.convert(markdown).strip()

    for block in json_obj["blocks"]:
        print("---block", type(block), block["t"])

        block_type = block["t"]

        for contents in block["c"]:
            print(contents)

    markdown = """
![](path "alt")
    """.strip()

    json_str = MarkdownParser.to_json(markdown).strip()
    print(json_str)
#
#     markdown = """
#     ![](path)
#         """.strip()
#
#     json_str = MarkdownParser.to_json(markdown).strip()
#     print(json_str)