# src/pycodemark/console.py
import argparse
import sys
import logging
from .config import load_config
from .analyzer import analyze_file
from .renderer import print_report, print_json_report, print_sarif_report
from .smart_reviewer import smart_review

# Logger setup
logger = logging.getLogger("pycodemark")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    """
    Entry point for PyCodemark CLI.

    Supports two commands:
      - review: static code analysis
      - smart-review: AI-powered code review

    Handles output formatting (terminal, JSON, SARIF) and sets proper exit codes.
    """
    parser = argparse.ArgumentParser(
        prog="pycodemark", description="pycodemark – a reflective code review tool for Python."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Static code review
    review_parser = subparsers.add_parser("review", help="Analyze code using static rules and print report")
    review_parser.add_argument("path", help="Path to Python file or directory")
    review_parser.add_argument(
        "--format",
        choices=["terminal", "json", "sarif"],
        default="terminal",
        help="Output format (terminal, json, sarif)",
    )

    # AI-powered smart review
    smart_parser = subparsers.add_parser("smart-review", help="Analyze code using AI-powered review")
    smart_parser.add_argument("path", help="Path to Python file or directory")
    smart_parser.add_argument(
        "--format",
        choices=["terminal", "json", "sarif"],
        default="terminal",
        help="Output format (terminal, json, sarif)",
    )

    args = parser.parse_args()
    config = load_config()

    try:
        if args.command == "review":
            results = analyze_file(args.path, config)
            # Ensure results are dicts
            mapped_results = [
                {
                    "file": r.get("file") if isinstance(r, dict) else r[0],
                    "line": r.get("line") if isinstance(r, dict) else r[1],
                    "code": r.get("code") if isinstance(r, dict) else r[2],
                    "message": r.get("message") if isinstance(r, dict) else r[3],
                }
                for r in results
            ]

        elif args.command == "smart-review":
            results = smart_review(args.path, config)
            mapped_results = results  # already dicts with file/line/code/message

        # Generate table tuples for Rich renderer
        table_report = [(f"{i['file']}:{i['line']} – {i['code']}", i["message"]) for i in mapped_results]

        # Output
        if args.format == "terminal":
            print_report(table_report)
        elif args.format == "json":
            print_json_report(table_report)
        elif args.format == "sarif":
            print_sarif_report(table_report)

        # Exit code: 0 if no issues, 1 if any issues found
        logger.info("Found %d issue(s).", len(mapped_results))
        sys.exit(0 if not mapped_results else 1)

    except Exception:
        logger.exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()
