import argparse
import csv
from pathlib import Path
from core import rms_sweep
from expr import compile_expr

def write_csv(path: Path = "", xcol: str | None = None, ycols: str | None = None, data: any = None, fieldnames: list[str] | None = None) -> None:
    if not fieldnames:
        raise ValueError("fieldnames must be a non-empty list")

    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        

def read_csv(path: Path, xcol: str, ycol: str, delimiter: str) -> tuple[list[float], list[float]]:
    with path.open("r", newline="") as f:
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
    if not argv.csv.exists():
        raise FileNotFoundError(f"CSV file not found: {argv.csv}")
    
    if argv.steps <= 0:
        raise ValueError("Steps must be a positive integer")
    
    if argv.sweep_min >= argv.sweep_max:
        raise ValueError("Sweep min must be less than sweep max")
    
    output_path = argv.out if argv.out else Path("results") / "sweep.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    x, y = read_csv(path=argv.csv, xcol=argv.xcol, ycol=argv.ycol, delimiter=argv.delimeter)

    # Run the Sweep
    expression = compile_expr(argv.expr)

    increment = (argv.max - argv.min) / argv.steps
    vals = [argv.sweep_min + i * increment for i in range(argv.steps + 1)]

    rms_values = rms_sweep(expr=expression, x=x, y=y, sweep_name=argv.sweep, sweep_min=vals[0], sweep_max=vals[-1], steps=argv.steps, xname=argv.xname if argv.xname else "x")

    # Write to output
    rows = []

    for i, rms in enumerate(rms_values):
        rows.append({argv.sweep: vals[i], "RMS_Error": rms})

    write_csv(path=output_path, data=rows, fieldnames=[argv.sweep, "RMS_Error"])

    return 0