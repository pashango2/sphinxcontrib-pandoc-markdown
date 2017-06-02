# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, ".")
from sphinxcontrib.pandoc_markdown import post_process
from sphinxcontrib.pandoc_markdown import MarkdownParser


def test_postprocess():
    text = """
.. code:: todo
    this is todo.
    """.strip()

    ans = """
.. todo::
    this is todo.
    """.strip()

    assert post_process(text) == ans

    text = """
.. code:: todo
    th"""

    ans = """
.. todo::
    th"""

    assert post_process(text) == ans

    text = """
.. code:: python
    python
    """.strip()

    ans = """
.. code:: python
    python
    """.strip()

    assert post_process(text) == ans

    text = """
.. code:: eval_rst

    this is rst.
    """.strip()

    ans = """
this is rst.
    """.strip()

    assert post_process(text) == ans


def test_import():
    markdown = """
@import "thunder.png"
    """.strip()

    ans = """
.. figure:: thunder.png
   :alt:
    """.strip()

    output_string = MarkdownParser.convert(markdown)
    assert output_string.strip() == ans

    markdown = """
@import "test.csv"
    """.strip()

    ans = """
.. csv-table::
    :file: test.csv
    :header-rows: 1
    """.strip()

    output_string = MarkdownParser.convert(markdown)
    assert output_string.strip() == ans

    markdown = '@import "test.mermaid"'
    ans = ".. mermaid:: test.mermaid"
    assert MarkdownParser.convert(markdown).strip() == ans

    markdown = '@import "test.plantuml"'
    ans = ".. uml:: test.plantuml"
    assert MarkdownParser.convert(markdown).strip() == ans

    markdown = '@import "test.puml"'
    ans = ".. uml:: test.puml"
    assert MarkdownParser.convert(markdown).strip() == ans

    markdown = '@import "import.wavedrom"'
    ans = ".. wavedrom::"
    assert MarkdownParser.convert(markdown).strip() == ans

    markdown = '@import "test.viz"'
    ans = ".. graphviz:: test.viz"
    assert MarkdownParser.convert(markdown).strip() == ans

    markdown = '@import "test.dot"'
    ans = ".. graphviz:: test.dot"
    assert MarkdownParser.convert(markdown).strip() == ans

    markdown = '@import "test.py"'
    ans = """
.. literalinclude:: test.py
    :language: python
    """.strip()
    assert MarkdownParser.convert(markdown).strip() == ans

    markdown = '@import "import.md"'
    ans = "this is import markdown"
    assert MarkdownParser.convert(markdown).strip() == ans


def test_list():
    markdown = """
```eval_rst
*A
*B

  *B-1
  *B-2
*C
```
    """.strip()

    ans = """
*A
*B

    *B-1
    *B-2
*C
    """.strip()

    assert MarkdownParser.convert(markdown).strip() == ans


def test_code_and_quote():
    markdown = """
```python
import os
```

> test
    """.strip()

    ans = """
.. code:: python

    import os

    test
    """.strip()

    assert MarkdownParser.convert(markdown).strip() == ans


def test_bullet_list():
    # Note:
    # https://github.com/jgm/pandoc/issues/137
    # https://github.com/jgm/pandoc/issues/3511
    markdown = """
- A
  - A-1
  - A-2
- B
  - B-1
  - B-2
    """.strip()

    ans = """
-  A

   -  A-1
   -  A-2

-  B

   -  B-1
   -  B-2
    """.strip()

    assert MarkdownParser.convert(markdown).strip() == ans


def test_softbreak():
    markdown = "one  \ntwo"
    assert MarkdownParser.convert(markdown).strip() == '| one\n| two'

    markdown = """
one
two

# title
    """.strip()
    assert MarkdownParser.convert(markdown).strip() == '| one\n| two'


def test_auto_ref():
    markdown = "correct link: [node](test/node_api.md)"
    result = "correct link: :doc:`node <test/node_api>`"
    assert result == MarkdownParser.convert(markdown).strip()

    markdown = "correct link: [node](http://xxx.com/node_api.md)"
    result = "correct link: `node <http://xxx.com/node_api.md>`__"
    assert result == MarkdownParser.convert(markdown).strip()
