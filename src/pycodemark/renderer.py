import json
from rich.console import Console
from rich.panel import Panel

console = Console()


def print_report(report):
    """Print report to terminal with rich panels."""
    if not report:
        console.print("[green]✓ No issues found. Your code looks good![/green]")
        return

    for issue in report:
        if isinstance(issue, dict):
            file = issue.get("file", "unknown")
            line = issue.get("line", 0)
            code = issue.get("code", "")
            message = issue.get("message", "")
            panel_content = f"[bold]{file}:{line} – {code}[/bold]\n[salmon1]{message}[/salmon1]"
        else:
            summary, suggestion = issue
            panel_content = f"[bold]{summary}[/bold]\n[salmon1]{suggestion}[/salmon1]"

        console.print(Panel(panel_content, border_style="blue"))


def print_json_report(report):
    """Print report as JSON."""
    json_report = []
    for issue in report:
        if isinstance(issue, dict):
            json_report.append(issue)
        else:
            summary, suggestion = issue
            json_report.append({"summary": summary, "suggestion": suggestion})
    print(json.dumps(json_report, indent=2))


def print_sarif_report(report):
    """Print report in SARIF format for CI integration."""
    sarif_results = []
    for issue in report:
        if isinstance(issue, dict):
            file = issue.get("file", "unknown")
            line = issue.get("line", 0)
            code = issue.get("code", "UNKNOWN")
            message = issue.get("message", "")
        else:
            file_line, code = issue[0].split(" – ") if " – " in issue[0] else ("unknown", "UNKNOWN")
            file = file_line.split(":")[0]
            line = int(file_line.split(":")[1]) if ":" in file_line else 0
            message = issue[1]

        sarif_results.append(
            {
                "ruleId": code,
                "message": {"text": message},
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": file}, "region": {"startLine": line}}}],
            }
        )

    sarif = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "Codemark", "informationUri": "https://github.com/your/codemark"}},
                "results": sarif_results,
            }
        ],
    }

    print(json.dumps(sarif, indent=2))
