# jungtypes
Translate MBTI 4-letter-codes to psychological functional stacks.

Python module to translate 4-letter-codes of the Myers-Briggs and
simular personality type indicators based on Jungian psychology into
corresponding Jungian psychological functional stacks.

This module was primarly written to understand this correspondence
so most likely no more development will go into it. Furthermore it
is designed to understand the translation process - a much easier
implementation would be purely data-driven as a dictionary that maps
each type to the functional stack.

For a description of the algorithms used see:
http://www.typeinmind.com/4-letter-code/

## Usage
You can run the module directly:

```bash
$ python -m jungtypes INTJ TiNe
INTJ -> NiTeFiSe
TiNe -> INTP
```

For library use please see the code documentation.
