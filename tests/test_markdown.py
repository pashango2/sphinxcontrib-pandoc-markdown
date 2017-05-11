# -*- coding: utf-8 -*-
from sphinxcontrib.pandoc_markdown import post_process


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

    print(post_process(text))
    assert post_process(text) == ans