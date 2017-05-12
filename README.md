sphinxcontrib-pandoc-markdown
=============================

It is an extension that you can use Markdown with Sphinx.


## Install

```
pip install sphinxcontrib-pandoc-markdown
```

## Requirement

[pandoc](http://pandoc.org/)


## Usage

Write the following in sphinx's `conf.py`.

```python
from sphinxcontrib.pandoc_markdown import MarkdownParser

source_suffix = [source_suffix, '.md']
source_parsers = {
   '.md': MarkdownParser,
}
```

## Future

### eval_rst
Can embed reStructuredText.

````
``` eval_rst
* This is a bulleted list.
* It has two items, the second
  item uses two lines.
```
````

### math

Inline math.
```
Since Pythagoras, we know that $a^2 + b^2 = c^2$.
```

Code block.

````
``` math
(a + b)^2 = a^2 + 2ab + b^2
(a - b)^2 = a^2 - 2ab + b^2
```
````

And write the following in sphinx's `conf.py`.

```python
extensions += ['sphinx.ext.mathjax']
```

### note, warning, todo

````
```note
This is note.
```

```warning
This is warning.
```

```todo
This is todo.
```
````

And write the following in sphinx's `conf.py`.

```python
extensions += ['sphinx.ext.todo']

...

todo_include_todos=True
```

### mermaid

````
```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
````

Requirement [sphinxcontrib-mermaid](https://github.com/mgaitan/sphinxcontrib-mermaid).

### plantuml, puml

````
```plantuml
Alice -> Bob: Hi!
Alice <- Bob: How are you?
```

```puml
Alice -> Bob: Hi!
Alice <- Bob: How are you?
```
````

### viz
````
```viz
digraph G {
  A -> B;
  B -> C;
}
```
````
### wavedrom

````
```wavedrom
{ signal: [
  { name: "pclk", wave: 'p.......' },
  { name: "Pclk", wave: 'P.......' },
  { name: "nclk", wave: 'n.......' },
  { name: "Nclk", wave: 'N.......' },
  {},
  { name: 'clk0', wave: 'phnlPHNL' },
  { name: 'clk1', wave: 'xhlhLHl.' },
  { name: 'clk2', wave: 'hpHplnLn' },
  { name: 'clk3', wave: 'nhNhplPl' },
  { name: 'clk4', wave: 'xlh.L.Hx' },
]}
```
````
