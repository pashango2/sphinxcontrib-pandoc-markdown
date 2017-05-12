# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import re
from tempfile import mkstemp
from six import PY2
from docutils.parsers.rst import Parser

REPLACE_CODE_TYPES = {
    "math": "math",
    "note": "note",
    "warning": "warning",
    "todo": "todo",

    "mermaid": "mermaid",
    "viz": "graphviz",
    "graph": "graph",
    "digraph": "digraph",
    "wavedrom": "wavedrom",
    "puml": "uml",
    "plantuml": "uml",
}


# noinspection PyUnresolvedReferences
def post_process(docs):
    new_docs = []
    code_re = re.compile(r".. code::\s+?@?(.*)")

    g = (x for x in docs.splitlines())

    for doc in g:
        group = code_re.match(doc)
        if group:
            code_type = group.group(1).strip()

            if code_type in REPLACE_CODE_TYPES:
                doc = ".. {}::".format(REPLACE_CODE_TYPES[code_type])
            elif code_type == "eval_rst":
                try:
                    doc = g.next() if PY2 else g.__next__()
                    if doc.strip() == "":
                        doc = g.next() if PY2 else g.__next__()
                        reg = re.match("^(\s+).*", doc)
                        if reg:
                            space = reg.group(1)
                        else:
                            continue

                        while True:
                            if doc.strip() == "":
                                break

                            doc = re.sub("^{}".format(space), "", doc)
                            new_docs.append(doc)

                            doc = g.next() if PY2 else g.__next__()
                except StopIteration:
                    break
                continue

        new_docs.append(doc)

    return "\n".join(new_docs)


class MarkdownParser(Parser):
    PANDOC_OPT = [
        "-f", "markdown+raw_html+markdown_in_html_blocks+autolink_bare_uris"
              "+tex_math_single_backslash-implicit_figures",
        "-t", "rst+raw_html-implicit_figures"
    ]

    # noinspection PyUnresolvedReferences
    def parse(self, input_string, document):
        pre_code = []
        _input_string = []
        for line in input_string.splitlines():
            if line.startswith(".. |"):
                pre_code.append(line)
            else:
                _input_string.append(line)

        input_string = "\n".join(_input_string)
        input_dir = None
        output_dir = None
        try:
            input_dir = mkstemp()
            output_dir = mkstemp()
            os.close(input_dir[0])
            os.close(output_dir[0])

            with open(input_dir[1], 'wt') as f:
                if PY2:
                    f.write(input_string.encode('utf-8'))
                else:
                    f.write(input_string)

            cmdline = "pandoc {} -r markdown -w rst {} -o {}".format(
                " ".join(self.PANDOC_OPT),
                input_dir[1], output_dir[1]
            )
            os.system(cmdline)

            if PY2:
                output_string = open(output_dir[1]).read().decode('utf-8')
            else:
                output_string = open(output_dir[1]).read()

            output_string = post_process(output_string)

        finally:
            if input_dir:
                os.unlink(input_dir[1])
            if output_dir:
                os.unlink(output_dir[1])

        if output_string:
            Parser.parse(self, output_string, document)

