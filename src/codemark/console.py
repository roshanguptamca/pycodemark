import argparse
from .config import load_config
from .analyzer import analyze_file
from .reporter import generate_report
from .renderer import print_report, print_json_report, print_sarif_report

def main():
    """
    Codemark CLI with subcommands for reviewing code.
    """
    parser = argparse.ArgumentParser(
        prog="codemark",
        description="Codemark – a reflective code review tool for Python."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Review command
    review_parser = subparsers.add_parser("review", help="Analyze code and print report")
    review_parser.add_argument("path", help="Path to Python file or directory")
    review_parser.add_argument("--format", choices=["terminal", "json", "sarif"], default="terminal")

    args = parser.parse_args()
    config = load_config()
    results = analyze_file(args.path, config)
    report = generate_report(results)

    # Render output based on chosen format
    if args.command == "review":
        if args.format == "terminal":
            print_report(report)
        elif args.format == "json":
            print_json_report(report)
        elif args.format == "sarif":
            print_sarif_report(report)
