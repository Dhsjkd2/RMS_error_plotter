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
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in _SUPPORTED_FUNCS:
                raise ValueError(f"Unsupported function: {ast.dump(node)}")
        if isinstance(node, ast.Name):
            pass
    code = compile(tree, filename="<expr>", mode="eval")

    def f(vars: dict[str, float]) -> float:
        scope: Dict[str, Any] = {}
        scope.update(_SUPPORTED_FUNCS)
        scope.update(_SUPPORTED_CONSTS)
        scope.update(vars)
        return float(eval(code, {"__builtins__": {}}, scope))
    return f