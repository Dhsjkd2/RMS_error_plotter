from __future__ import annotations

import ast
import math
from typing import Callable, Any, Dict

_SUPPORTED_FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
    "floor": math.floor,
    "ceil": math.ceil,
}

_SUPPORTED_CONSTS = {
    "pi": math.pi,
    "e": math.e,
}

_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
}

def compile_expr(expr: str) -> Callable[[dict[str, float]], float]:
    tree = ast.parse(expr, mode="eval")

    for node in ast.walk(tree):
        ...

    def f(vars: dict[str, float]) -> float:

        return float()

    return f