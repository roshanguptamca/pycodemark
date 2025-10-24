import json
from rich.console import Console
from rich.panel import Panel

console = Console()

def print_report(report):
    """Print report to terminal with rich panels."""
    if not report:
        console.print("[green]✓ No issues found. Your code looks good![/green]")
        return
    for summary, suggestion in report:
        console.print(Panel(f"[bold]{summary}[/bold]\n[salmon1]{suggestion}[/salmon1]", border_style="blue"))

def print_json_report(report):
    """Print report as JSON."""
    json_report = [{"summary": s, "suggestion": sug} for s, sug in report]
    print(json.dumps(json_report, indent=2))

def print_sarif_report(report):
    """
    Print report in SARIF format (static analysis format for CI integration)
    """
    sarif = {
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "Codemark", "informationUri": "https://github.com/your/codemark"}},
            "results": [{
                "ruleId": s.split("–")[1].strip(" []") if "–" in s else "UNKNOWN",
                "message": {"text": f"{s} {sug}"},
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": s.split(':')[0]},
                                                    "region": {"startLine": int(s.split(':')[1])}}}]
            } for s, sug in report]
        }]
    }
    print(json.dumps(sarif, indent=2))
