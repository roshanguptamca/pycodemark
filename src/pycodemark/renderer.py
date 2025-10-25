"""Module description: Colorized issue renderer for PyCodemark."""

from rich.console import Console
from rich.table import Table
from rich.text import Text
import json

console = Console()


def print_report(issues: list[dict]):
    """
    Print a table of issues with colored levels.
    Each issue dict must contain: file, line, code, message, level.
    AI/OpenAI errors are highlighted in magenta, warnings in yellow, others in cyan.
    """
    if not issues:
        console.print("[bold green]✅ No issues found![/bold green]")
        return

    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("Location", style="bold", no_wrap=True)
    table.add_column("Message", style="bold")
    table.add_column("Level", style="bold")

    for issue in issues:
        file = issue.get("file", "<unknown>")
        line = issue.get("line", 0)
        code = issue.get("code", "")
        message = issue.get("message", "")
        level = issue.get("level", "warning")

        loc = f"{file}:{line} – {code}"

        # Color logic
        level_lower = level.lower()
        if level_lower == "error" and code.lower().startswith("openai"):
            level_text = Text(level.upper(), style="bold magenta")
        elif level_lower == "error":
            level_text = Text(level.upper(), style="bold red")
        elif level_lower == "warning":
            level_text = Text(level.upper(), style="yellow")
        else:
            level_text = Text(level.upper(), style="cyan")

        # Message coloring for AI errors
        if code.lower().startswith("openai"):
            message_text = Text(message, style="magenta")
        elif level_lower == "warning":
            message_text = Text(message, style="yellow")
        else:
            message_text = Text(message)

        table.add_row(loc, message_text, level_text)

    console.print(table)


def print_json_report(issues: list[dict]):
    """
    Pretty-print issues as JSON using rich.
    """
    console.print_json(json.dumps(issues, indent=2))


def print_sarif_report(issues: list[dict]):
    """
    Generate SARIF-compatible JSON report.
    """
    sarif_output = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "PyCodemark"}},
                "results": [
                    {
                        "ruleId": issue.get("code", ""),
                        "message": {"text": issue.get("message", "")},
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {"uri": issue.get("file", "")},
                                    "region": {"startLine": issue.get("line", 0)},
                                }
                            }
                        ],
                    }
                    for issue in issues
                ],
            }
        ],
    }
    console.print_json(json.dumps(sarif_output, indent=2))
