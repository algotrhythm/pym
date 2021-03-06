"""Parse source text to an AST"""

import os
import ast
from functools import singledispatch
from typing import Callable

from pysyte.types.methods import Method
from pysyte.types.paths import StrPath
from pysyte.types.paths import FilePath
from pysyte.types.paths import NonePath
from pysyte.types.paths import makepath


def parse_path(source: str, path: str):
    path_name = path if path else "<None>"
    return ast.parse(source, path_name) if source else None


@singledispatch
def parse(arg):
    """In the face of ambiguity, refuse the temptation to guess."""
    # breakpoint()
    raise NotImplementedError


@parse.register(type(None))
def _(arg):
    """GIGO"""
    return None


@parse.register(str)
def _(arg):
    """Parse the arg's source code

    If the arg is a path, or file-like, read source from there
    Else use the arg as source
    """
    source, path = arg, None
    try:
        try:
            source, path = arg.read(), arg.name
        except AttributeError:
            p = FilePath(arg)
            if p:
                return parse(p)
    except (FileNotFoundError, IOError):
        pass
    return parse_path(source, path)


@parse.register(Callable)
def _(arg):
    p = makepath(arg)
    assert p
    astree = parse(p)
    assert astree


@parse.register(Method)
def _(arg):
    return parse(arg.method)


@parse.register(type(os))
def _(arg):
    return parse(makepath(arg))


@parse.register(NonePath)
def _(arg):
    return parse(None)


@parse.register(StrPath)
def _(arg):
    return parse_path(arg.text(), arg)
