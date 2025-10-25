"""PyCodemark Console Entrypoint.

Provides CLI commands for:
- Static code review (--format: terminal, json, sarif)
- AI-powered smart review using GPT
- Unit test generation for untested functions

Each feature is modular and logs results using a centralized logger.
"""

import argparse
import sys
from .config import load_config
from .analyzer import analyze_file
from .renderer import print_report, print_json_report, print_sarif_report
from .smart_reviewer import smart_review
from .fixer import auto_fix
from .logger import logger

# --------------------------------------------------------------------------------
# Logger setup (fallback if no handlers in centralized logger)
# --------------------------------------------------------------------------------
if not logger.handlers:
    import logging

    logger = logging.getLogger("pycodemark")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# --------------------------------------------------------------------------------
# Main CLI Entrypoint
# --------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        prog="pycodemark",
        description="PyCodemark – a reflective code review tool for Python.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --------------------------------------------------------------------------------
    # Static Code Review
    # --------------------------------------------------------------------------------
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

    # --------------------------------------------------------------------------------
    # AI-Powered Smart Review
    # --------------------------------------------------------------------------------
    smart_parser = subparsers.add_parser("smart-review", help="Analyze code using AI-powered review")
    smart_parser.add_argument("path", help="Path to Python file or directory")
    smart_parser.add_argument(
        "--format",
        choices=["terminal", "json", "sarif"],
        default="terminal",
        help="Output format (terminal, json, sarif)",
    )

    # --------------------------------------------------------------------------------
    # Unit Test Generation
    # --------------------------------------------------------------------------------
    test_parser = subparsers.add_parser("gen-tests", help="Generate unit tests for untested functions")
    test_parser.add_argument("path", help="Path to scan for Python files")
    test_parser.add_argument(
        "--ai",
        action="store_true",
        help="Use GPT-5 for realistic test generation",
    )
    test_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing test files instead of appending",
    )
    test_parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private functions (those starting with _)",
    )
    test_parser.add_argument(
        "--output",
        default="tests",
        help="Output directory for generated test files (default: tests)",
    )

    args = parser.parse_args()
    config = load_config()

    try:
        issues = []

        # --------------------------------------------------------------------------------
        # Static Review
        # --------------------------------------------------------------------------------
        if args.command == "review":
            issues = analyze_file(args.path, config)
            if getattr(args, "fix", False):
                issues = auto_fix(args.path, config)

        # --------------------------------------------------------------------------------
        # Smart AI Review
        # --------------------------------------------------------------------------------
        elif args.command == "smart-review":
            issues = smart_review(args.path, config)

        # --------------------------------------------------------------------------------
        # Unit Test Generation
        # --------------------------------------------------------------------------------
        elif args.command == "gen-tests":
            from .test_generator import generate_tests

            generate_tests(
                path=args.path,
                overwrite=getattr(args, "overwrite", False),
                output_dir=getattr(args, "output", "tests"),
                use_ai=getattr(args, "ai", False),
            )

            logger.info("✅ Unit test generation completed successfully.")
            sys.exit(0)

        # --------------------------------------------------------------------------------
        # Output and Exit
        # --------------------------------------------------------------------------------
        for issue in issues:
            issue.setdefault("level", "warning")

        if hasattr(args, "format"):
            if args.format == "terminal":
                print_report(issues)
            elif args.format == "json":
                print_json_report(issues)
            elif args.format == "sarif":
                print_sarif_report(issues)

        logger.info("Found %d issue(s).", len(issues))
        sys.exit(0 if not issues else 1)

    except Exception:
        logger.exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()
