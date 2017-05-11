# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import re
from tempfile import mkstemp
from six import PY2
from docutils import nodes
from docutils import parsers
from docutils.parsers.rst import Parser


REPLACE_CODE_TYPES = {
    "math": "math",
    "note": "note",
    "warning": "warning",
    "todo": "todo",

    "mermaid": "mermaid",
    "puml": "",
    "viz": "graphviz",
    "graph": "graph",
    "digraph": "digraph",
}


def post_process(docs):
    new_docs = []
    code_re = re.compile(r".. code::\s+?(.*)")

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

    def parse(self, inputstring, document):
        outputstring = None

        pre_code = []
        input_string = []
        for line in inputstring.splitlines():
            if line.startswith(".. |"):
                pre_code.append(line)
            else:
                input_string.append(line)

        input_string = "\n".join(input_string)

        try:
            input = mkstemp()
            output = mkstemp()
            os.close(input[0])
            os.close(output[0])

            with open(input[1], 'wt') as f:
                if PY2:
                    f.write(input_string.encode('utf-8'))
                else:
                    f.write(input_string)

            cmdline = "pandoc %s -R -r markdown -w rst %s -o %s" % (" ".join(self.PANDOC_OPT), input[1], output[1])
            os.system(cmdline)

            if PY2:
                outputstring = open(output[1]).read().decode('utf-8')
            else:
                outputstring = open(output[1]).read()

            outputstring = post_process(outputstring)

        finally:
            os.unlink(input[1])
            os.unlink(output[1])

        if outputstring:
            super(MarkdownParser, self).parse(outputstring, document)
