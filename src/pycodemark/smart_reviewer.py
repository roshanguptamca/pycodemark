"""Module description."""

import os
import json
import logging
from openai import OpenAI
from openai._exceptions import OpenAIError, RateLimitError, APIError
from .config import load_config
from .analyzer import get_python_files, read_file  # Ensure read_file exists in analyzer.py

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def smart_review(path: str, config: dict = None) -> list[dict]:
    """
    Perform AI-powered code review using GPT-5 on Python files.
    Returns:
        List[dict]: Each dict contains 'file', 'line', 'code', 'message', 'level'
    """
    if config is None:
        config = load_config()

    issues = []
    checks = config.get("checks", {})

    # Skip AI review if disabled
    if not checks.get("ai_review", True):
        return issues

    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Collect Python files
    python_files = get_python_files(path)
    if not python_files:
        msg = f"No Python files found at path: {path}"
        logger.warning(msg)
        return [{"file": path, "line": 0, "code": "InvalidPath", "message": msg, "level": "warning"}]

    # Analyze each file
    for file_path in python_files:
        logger.info("Running AI-powered smart review on %s", file_path)
        code = read_file(file_path)
        model = os.environ.get("CODEMARK_MODEL", config.get("model", "gpt-5"))

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional Python code reviewer. "
                            "Check the code for style issues, clarity, missing docstrings, "
                            "type hints, potential bugs, and best practices. "
                            "Return a list of issues in JSON format with keys: "
                            "'file', 'line', 'code', 'message'."
                        ),
                    },
                    {"role": "user", "content": code},
                ],
                temperature=0,
            )

            ai_output = response.choices[0].message.content
            try:
                parsed_issues = json.loads(ai_output)
                for issue in parsed_issues:
                    # Respect config checks
                    if issue["code"].lower() in checks and not checks[issue["code"].lower()]:
                        continue
                    # Assign level for reporting
                    issue["level"] = "warning" if issue["code"] in ["LineLength", "MissingDocstring"] else "error"
                    issue["file"] = file_path
                    issues.append(issue)
            except json.JSONDecodeError:
                logger.warning("AI returned invalid JSON for %s", file_path)
                issues.append(
                    {"file": file_path, "line": 0, "code": "AIReview", "message": ai_output, "level": "error"}
                )

        except RateLimitError as e:
            logger.error("RateLimitError for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "RateLimitError", "message": str(e), "level": "error"})
        except APIError as e:
            logger.error("APIError for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "APIError", "message": str(e), "level": "error"})
        except OpenAIError as e:
            logger.error("OpenAIError for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "OpenAIError", "message": str(e), "level": "error"})
        except Exception as e:
            logger.error("Unknown error for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "UnknownError", "message": str(e), "level": "error"})

    if issues:
        logger.warning("Found %d issue(s) from AI review.", len(issues))
    return issues
