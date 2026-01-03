from math import exp, sqrt
from typing import Callable, Sequence

def rms_error(expr: Callable[[dict[str, float]], float], x: Sequence[float], y: Sequence[float], xname: str = "x") -> float:
    if(len(x) != len(y) or len(x) == 0):
        raise ValueError("Input x and y sequences must have the same length and must be non-zero in length")
    N = len(y) # Set the N for the RMS equation to the length of the dataset given
    ssr = 0.0

    for xi, yi in zip(x, y):
       scope = {xname: float(xi)}
       prediction = expr(scope)
       error = yi - prediction
       ssr += error ** 2 

    rms = sqrt(ssr / N)
    return rms

def rms_sweep(*, expr, x, y, sweep_name, sweep_min, sweep_max, steps, xname="x") -> list[float]:
    increment = (sweep_max - sweep_min) / steps
    results: list[float] = []

    for i in range(steps + 1):
        sweep_value = sweep_min + i * increment
        def model(scope: dict[str, float]) -> float:
            return expr(scope)
        results.append(rms_error(model, x=x, y=y, xname=xname))

    return results