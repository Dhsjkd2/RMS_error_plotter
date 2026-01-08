import argparse
import csv
from pathlib import Path
from core import rms_sweep
from expr import compile_expr

def write_csv(path: Path, xcol: str, ycols: str, data: any, fieldnames: list[str]) -> None:
    with path.open(path, "w", newline="") as f:
        writer = csv.writer(f, fieldnames=fieldnames)
        # write header
        writer.writeheader()
        # write data
        writer.writerows(data)
        

def read_csv(path: Path, xcol: str, ycol: str, delimiter: str) -> tuple[list[float], list[float]]:
    with path.open(path, "r", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        x_values: list[float] = []
        y_values: list[float] = []
        for row in reader:
            x_values.append(float(row[xcol]))
            y_values.append(float(row[ycol]))
    return x_values, y_values

def init_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="RMS error plotter",
        description="Simple program that plots the RMS error between your input expression and data points",
    )
    p.add_argument("csv", type=Path, required=True, help="Input the CSV file containing your data points")
    p.add_argument("--expr", required=True, help="Input the expression to evaluate")
    # CSV parameters
    p.add_argument("--xname", help="Input the variable that will be treated as the x-variable in your equation")
    p.add_argument("--xcol", default="t", help="Input the name of the column containing x values")
    p.add_argument("--ycol", default="V", help="Input the name of the column containing y values")
    p.add_argument("--delimeter", default=",", help="Input the delimiter used in your CSV file. Default is ','")
    # Sweeping parameters
    p.add_argument("--sweep", required=True, help="Input the variable to sweep over")
    p.add_argument("--min", type=int, required=True, help="Input the minimum value for the sweep")
    p.add_argument("--max", type=int, required=True, help="Input the maximum value for the sweep")
    p.add_argument("--steps", type=int, default=100, help="Input the number of steps to use in the sweep. Default is 100")
    # Output parameters
    p.add_argument("--out", type=Path, help="Input the path to save the output plot. If not given, a default path will be used.")
    return p

def main() -> int:
    parser = init_parser()
    argv = parser.parse_args()

    # Input validation
    
    for arg in argv.values:
        ...
    
    # Run the Sweep
    expression = compile_expr()

    rms_values = rms_sweep()

    # Write to output

    if "out" not in argv:
        # Write to default file path
        ...
    else:
        # Write to given file path
        ...

    return 0