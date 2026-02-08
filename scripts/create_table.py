import argparse
import json
import os

from email import parser
import re

def average(values):
    return sum(values) / len(values) if values else None

def print_float(value: float|None) -> str:
    return f"{value / 1000.0:.1f}" if value is not None else "-"

def print_memory(value: float|None) -> str:
    return f"{value:.1f}" if value is not None else "-"

def human_sort(text: str) -> list:
    """
    Sort key function for sorting strings in human-friendly order.
    Splits text into alternating strings and integers for natural sorting.
    """
    parts = []
    for part in re.split(r'(\d+)', text):
        if part.isdigit():
            parts.append(int(part))
        else:
            parts.append(part)
    return parts

def read_results(directory: str) -> dict[str, dict[str, dict[str, float]]]:
    results = {}

    # Open all the JSON files in the directory and yield their contents
    for file in os.listdir(directory):
        if file.endswith(".json"):
            with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
                for line in f:
                    result = json.loads(line)

                    rewriter = result["rewriter"]
                    experiment = result["experiment"]
                    # Remove the .dataspec and .rec suffix
                    experiment = os.path.splitext(experiment)[0]

                    if experiment not in results:
                        results[experiment] = {}

                    if rewriter not in results[experiment]:
                        results[experiment][rewriter] = {}
                    
                    results[experiment][rewriter]["time"] = average(result.get("timings", []))
                    results[experiment][rewriter]["memory"] = average(result.get("memory_usage", []))

    return results

def create_table(json_path: str) -> None:
    results = read_results(json_path)
    # Generate a latex table from the results
    print("\\documentclass{standalone}")
    print("\\usepackage{booktabs}")

    print("\\begin{document}")

    print("\\begin{tabular}{lrrrrrrrr}")
    print("\\toprule")
    print("Experiment & \\multicolumn{2}{c}{Jitty} & \\multicolumn{2}{c}{Jittyc} & \\multicolumn{2}{c}{Innermost} & \\multicolumn{2}{c}{Sabre} \\\\")
    print("& Time (s) & Mem (MB) & Time (s) & Mem (MB) & Time (s) & Mem (MB) & Time (s) & Mem (MB) \\\\")

    print("\\midrule")

    # Sort the experiments by name
    for experiment, data in sorted(results.items()):
        jitty_time = print_float(data.get("jitty", {}).get("time", None))
        jitty_mem = print_memory(data.get("jitty", {}).get("memory", None))
        jittyc_time = print_float(data.get("jittyc", {}).get("time", None))
        jittyc_mem = print_memory(data.get("jittyc", {}).get("memory", None))
        innermost_time = print_float(data.get("innermost", {}).get("time", None))
        innermost_mem = print_memory(data.get("innermost", {}).get("memory", None))
        sabre_time = print_float(data.get("sabre", {}).get("time", None))
        sabre_mem = print_memory(data.get("sabre", {}).get("memory", None))

        print(f"{experiment} & {jitty_time} & {jitty_mem} & {jittyc_time} & {jittyc_mem} & {innermost_time} & {innermost_mem} & {sabre_time} & {sabre_mem} \\\\")

    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{document}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="run.py")
    parser.add_argument("input", help="Input JSON directory")

    args = parser.parse_args()

    create_table(args.input)
