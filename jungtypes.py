# -*- coding: utf-8 -*-

"""Translate MBTI 4-letter-codes to psychological functional stacks.

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
"""

import sys
import itertools

# All functions and if they are rational and judging
FUNCTIONDESC = {
    'F' : ('feeling', 'J'),
    'T' : ('thinking', 'J'),
    'N' : ('intuition', 'P'),
    'S' : ('sensing', 'P'),
}

# the other stuff...
LETTERDESC = {
    'E' : 'extroverted',
    'I' : 'introverted',
    'J' : 'judging',
    'P' : 'perceiving',
}

ALLTYPES = ["".join(t) for t in itertools.product(
    ('E', 'I'), ('N', 'S'), ('F', 'T'), ('J', 'P'))]
ALLFUNCTIONS = ["".join(s) for s in itertools.product(
    ('F', 'N', 'S', 'T'), ('e', 'i'))]

def type2stack(typestr, fullstack=False):
    """Translate type to functional stack as str

    Args:
        typestr (str): 4-letter-code personality type indicator
        fullstack (bool): Return the full stack instead of only the
                          dominant and supporting functions

    Returns:
        str

    Raises:
        TypeError if typestr is no str
        ValueError if typestr is no valid 4-letter-code

    Usage:
        >>> type2stack('ENFP')
        'NeFi'
        >>> type2stack('ENFP', fullstack=True)
        'NeFiTeSi'
        >>> type2stack('ENFJ', fullstack=True)
        'FeNiSeTi'
        >>> type2stack('INFJ', fullstack=True)
        'NiFeTiSe'
        >>> type2stack('INFP', fullstack=True)
        'FiNeSiTe'
        >>> type2stack('INSP')
        Traceback (most recent call last):
            ...
        ValueError: first argument must be valid 4-letter-code
    """
    # checking input
    if not isinstance(typestr, str):
        raise TypeError("first argument must be string")
    typestr = typestr.upper()
    if typestr not in ALLTYPES:
        raise ValueError("first argument must be valid 4-letter-code")

    # applying the alternating rule (eiei, ieie)
    if typestr[0] == 'E':
        align = 'eiei'
    else:
        align = 'ieie'

    # applying the JPPJ / PJJP rule
    if typestr[0] + typestr[3] in ['EJ', 'IP']:
        funcs = 'JPPJ'
    else:
        funcs = 'PJJP'

    # second place in the 4-letter-code is the first perceiving
    # function, 3rd place is the first judging function
    if typestr[1] == 'N':
        pfuncs = 'NS'
    else:
        pfuncs = 'SN'

    if typestr[2] == 'F':
        jfuncs = 'FT'
    else:
        jfuncs = 'TF'

    for i in range(2):
        funcs = funcs.replace('P', pfuncs[i], 1)
        funcs = funcs.replace('J', jfuncs[i], 1)

    stack = "".join([funcs[i] + align[i] for i in range(4)])

    if fullstack:
        return stack
    else:
        return stack[0:4]

# being lazy here...
ALLFULLSTACKS = [type2stack(t, fullstack=True) for t in ALLTYPES]

def stack2type(stackstr):
    """Translate functional stack to type as str

    Args:
        stackstr (str): Functinal stack as str (4 or 8 letters)

    Returns:
        str

    Raises:
        TypeError if stackstr is no str
        ValueError if stackstr is no functional stack

    Usage:
        >>> stack2type('NeFi')
        'ENFP'
        >>> stack2type('NeFiTeSi')
        'ENFP'
        >>> stack2type('TeNi')
        'ENTJ'
        >>> stack2type('TiNe')
        'INTP'
        >>> stack2type('NeFe')
        Traceback (most recent call last):
            ...
        ValueError: argument must be valid functional stack
    """
    # checking input
    if not isinstance(stackstr, str):
        raise TypeError("first argument must be string")

    stackstr = stackstr.upper()
    slen = len(stackstr)
    if slen not in [4, 8]:
        raise ValueError("argument must be valid functional stack")
    elif stackstr not in [s[0:slen].upper() for s in ALLFULLSTACKS]:
        raise ValueError("argument must be valid functional stack")

    align = stackstr[1]

    if stackstr[stackstr.find('E')-1] in ['N', 'S']:
        extrfunctype = 'P'
    else:
        extrfunctype = 'J'

    if align + extrfunctype in ['EP', 'IJ']:
        typestr = align + stackstr[0] + stackstr[2] + extrfunctype
    else:
        typestr = align + stackstr[2] + stackstr[0] + extrfunctype

    return typestr

if __name__ == '__main__':
    # This is terrible inefficient code, but I assume, that you're
    # most likely not traslating more than say... 16 types.

    for arg in sys.argv[1:]:
        res = "[invalid]"

        try:
            res = type2stack(arg, fullstack=True)
        except (TypeError, ValueError):
            pass

        try:
            res = stack2type(arg)
        except (TypeError, ValueError):
            pass

        print("%s -> %s" % (arg, res))
