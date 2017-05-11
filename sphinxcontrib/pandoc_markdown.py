# -*- coding: utf-8 -*-
import os
import re
from tempfile import mkstemp
from six import PY2


class MarkdownProcessor(object):
    def on_source_read(self, app, docname, source):
        if docname == 'index':
            return

        try:
            input = mkstemp()
            output = mkstemp()
            os.close(input[0])
            os.close(output[0])

            with open(input[1], 'wt') as f:
                if PY2:
                    f.write(source[0].encode('utf-8'))
                else:
                    f.write(source[0])

            to_opt = [
                "-f", "markdown+raw_html+markdown_in_html_blocks+autolink_bare_uris"
                      "+tex_math_single_backslash-implicit_figures",
                "-t", "rst+raw_html-implicit_figures"
            ]

            cmdline = "pandoc %s -R -r markdown -w rst %s -o %s" % (" ".join(to_opt), input[1], output[1])
            os.system(cmdline)

            if PY2:
                source[0] = open(output[1]).read().decode('utf-8')
            else:
                source[0] = open(output[1]).read()

            source[0] = post_process(source[0])
            print(source[0])

        finally:
            os.unlink(input[1])
            os.unlink(output[1])

    def setup(self, app):
        app.add_config_value('markdown_title', None, 'html')

        app.connect('source-read', self.on_source_read)


def setup(app):
    md = MarkdownProcessor()
    md.setup(app)


REPLACE_CODE_TYPES = [
    "math", "note", "todo", "mermaid"
]


def post_process(docs):
    new_docs = []
    code_re = re.compile(r".. code::\s+?(.*)")

    g = (x for x in docs.splitlines())
    for doc in g:
        group = code_re.match(doc)
        if group:
            code_type = group.group(1).strip()

            if code_type in REPLACE_CODE_TYPES:
                doc = ".. {}::".format(code_type)
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
