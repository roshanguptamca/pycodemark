"""Module description."""

import argparse
import sys
import logging
from .config import load_config
from .analyzer import analyze_file
from .renderer import print_report, print_json_report, print_sarif_report
from .smart_reviewer import smart_review
from .fixer import auto_fix

# Logger setup
logger = logging.getLogger("pycodemark")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    parser = argparse.ArgumentParser(
        prog="pycodemark", description="PyCodemark – a reflective code review tool for Python."
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
    review_parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix fixable issues (e.g., line length, insert template docstrings)",
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
        issues = []

        if args.command == "review":
            issues = analyze_file(args.path, config)
            if getattr(args, "fix", False):
                issues = auto_fix(args.path, config)

        elif args.command == "smart-review":
            issues = smart_review(args.path, config)

        # Ensure every issue has a level
        for issue in issues:
            issue.setdefault("level", "warning")

        # Output
        if args.format == "terminal":
            print_report(issues)
        elif args.format == "json":
            print_json_report(issues)
        elif args.format == "sarif":
            print_sarif_report(issues)

        # Exit code: 0 if no issues, 1 if any issues found
        logger.info("Found %d issue(s).", len(issues))
        sys.exit(0 if not issues else 1)

    except Exception:
        logger.exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()
