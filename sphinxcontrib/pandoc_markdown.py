# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import re
from tempfile import mkstemp
from six import PY2
import codecs
from docutils.parsers.rst import Parser

__version__ = "1.6"

REPLACE_CODE_TYPES = {
    "math": "math",
    "note": "note",
    "warning": "warning",
    "todo": "todo",
    "todolist": "todolist",
    "seealso": "seealso",
    "pull-quote": "pull-quote",
    "highlights": "highlights",
    "epigraph": "epigraph",

    "mermaid": "mermaid",
    "viz": "graphviz",
    "graph": "graph",
    "digraph": "digraph",
}


EXTENSION_DIRECTIVE_DICT = {
    '.mermaid': 'mermaid',
    '.plantuml': 'uml',
    '.puml': 'uml',
    '.wavedrom': 'wavedrom',
    '.viz': 'graphviz',
    '.dot': 'graphviz',
}


EXTENSION_LANGUAGE_DICT = {
    '.sh': 'shell',
    '.bash': 'shell',
    '.c': 'c',
    '.cpp': 'cpp',
    '.coffee': 'coffee',
    '.coffeescript': 'coffee',
    '.coffee-script': 'coffee',
    '.cs': 'cs',
    '.csharp': 'cs',
    '.css': 'css',
    '.scss': 'css.scss',
    '.sass': 'sass',
    '.erlang': 'erl',
    '.go': 'go',
    '.html': 'text.html.basic',
    '.java': 'java',
    '.js': 'js',
    '.javascript': 'js',
    '.json': 'json',
    '.less': 'less',
    '.mustache': 'text.html.mustache',
    '.objc': 'objc',
    '.objectivec': 'objc',
    '.objective-c': 'objc',
    '.php': 'text.html.php',
    '.py': 'python',
    '.pyw': 'python',
    '.python': 'python',
    '.rb': 'ruby',
    '.ruby': 'ruby',
    '.text': 'text.plain',
    '.toml': 'toml',
    '.xml': 'xml',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.yaml_table': 'yaml',
    '.erd': 'erd',
    '.node': 'js',
    '.markdown': 'markdown',
    '.md': "markdown"
}

IMPORT_RE = re.compile(r'^@import\s*"(.*?)"')
MARKDOWN_ENCODE = "utf-8"


def csv_to_table(csv_path):
    return """
```eval_rst
.. csv-table::
    :file: {}
    :header-rows: 1

```
    """.format(csv_path)


def import_raw(data_type, path):
    return """
```eval_rst
.. raw:: {}
    :file: {}
```
    """.format(data_type, path)


def import_directive(directive, path):
    return """
```eval_rst
.. {}:: {}
```
    """.format(directive, path)


def import_code_block(code_type, path):
    return """
```eval_rst
.. literalinclude:: {}
    :language: {}
```
    """.format(path, code_type)


# noinspection PyUnresolvedReferences
def pre_process(lines):
    new_lines = []
    for line in lines:
        if line.startswith("@import"):
            g = IMPORT_RE.match(line)
            if g and g.group(1):
                path = g.group(1)
                _, ext = os.path.splitext(path)
                ext = ext.lower()

                if ext in (".png", ".jpg", ".jpeg", ".apng", ".svg", ".bmp", ".gif"):
                    new_lines.append("![]({})".format(path))
                    continue
                elif ext == ".csv":
                    new_lines.append(csv_to_table(path))
                    continue
                elif ext in (".html", ".css"):
                    new_lines.append(import_raw(ext[1:], path))
                    continue
                elif ext in ('.md', '.mmark', '.markdown'):
                    try:
                        new_lines.append(codecs.open(path, "r", MARKDOWN_ENCODE).read())
                        continue
                    except:
                        pass
                elif ext in EXTENSION_DIRECTIVE_DICT:
                    new_lines.append(import_directive(EXTENSION_DIRECTIVE_DICT[ext], path))
                    continue
                else:
                    language = EXTENSION_LANGUAGE_DICT.get(ext, "text")
                    # code block
                    new_lines.append(import_code_block(language, path))
                    continue

        new_lines.append(line)

    return new_lines


# noinspection PyUnresolvedReferences
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
                        space = None

                        while True:
                            doc = g.next() if PY2 else g.__next__()
                            reg = re.match("^(\s*).*", doc)
                            if reg and space is None:
                                space = reg.group(1)
                            else:
                                if reg.group(1) == "" and doc.strip() != "":
                                    new_docs.append(doc)
                                    break

                            doc = re.sub("^{}".format(space), "", doc)
                            new_docs.append(doc)
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

    @staticmethod
    def convert(input_string):
        pre_code = []
        _input_string = []
        for line in input_string.splitlines():
            if line.startswith(".. |"):
                pre_code.append(line)
            else:
                _input_string.append(line)

        # pre process
        _input_string = pre_process(_input_string)

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
                " ".join(MarkdownParser.PANDOC_OPT),
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

        return output_string

    # noinspection PyUnresolvedReferences
    def parse(self, input_string, document):
        output_string = self.convert(input_string)

        if output_string:
            Parser.parse(self, output_string, document)
