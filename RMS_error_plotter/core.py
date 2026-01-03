from math import exp, sqrt
from typing import Callable

def rms_error(expr: Callable[[dict[str, float]], float], x: Sequence[float], y: Sequence[float], xname: str = "x") -> float:
    if(len(x) != len(y) or len(x) == 0):
        raise ValueError("Input x and y sequences must have the same length and must be non-zero in length")
    N = len(y) # Set the N for the RMS equation to the length of the dataset given
    SSR = 0.0

    for xi, yi in zip(x, y):
       scope = {xname: float(xi)}
       prediction = expr(scope)
       error = yi - prediction
       SSR += error ** 2 

    rms = sqrt(SSR / N)
    return rms

