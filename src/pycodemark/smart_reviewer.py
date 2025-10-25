# src/pycodemark/smart_reviewer.py
import os
import json
import logging
from openai import OpenAI
from openai._exceptions import OpenAIError, RateLimitError, APIError

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def read_file(file_path: str) -> str:
    """Reads a Python file and returns its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def smart_review(path: str, config: dict = None) -> list[dict]:
    """
    Perform AI-powered code review using GPT-5 on a Python file or directory.

    Returns:
        List[dict]: Each dict contains 'file', 'line', 'code', 'message'
    """
    if config is None:
        config = {}

    issues = []

    # Only initialize OpenAI client here
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        msg = "OPENAI_API_KEY not set. Skipping AI-powered review."
        logger.warning(msg)
        return [{"file": path, "line": 0, "code": "MissingAPIKey", "message": msg}]

    client = OpenAI(api_key=api_key)

    # Collect Python files
    python_files = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    python_files.append(os.path.join(root, f))
    elif path.endswith(".py"):
        python_files.append(path)
    else:
        msg = f"Path {path} is not a Python file or directory."
        logger.error(msg)
        return [{"file": path, "line": 0, "code": "InvalidPath", "message": msg}]

    # Analyze each file
    for file_path in python_files:
        logger.info("Running AI-powered smart review on %s", file_path)
        code = read_file(file_path)
        model = os.environ.get("CODEMARK_MODEL", "gpt-5")

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional Python code reviewer. "
                            "Check the code for style issues, clarity, missing docstrings, "
                            "potential bugs, and best practices. Return a list of issues in JSON format."
                        ),
                    },
                    {"role": "user", "content": code},
                ],
                temperature=0,
            )

            ai_output = response.choices[0].message.content
            logger.debug("AI output: %s", ai_output)

            try:
                parsed_issues = json.loads(ai_output)
                for issue in parsed_issues:
                    if all(k in issue for k in ("file", "line", "code", "message")):
                        issues.append(issue)
                    else:
                        issues.append({"file": file_path, "line": 0, "code": "AIReview", "message": ai_output})
            except json.JSONDecodeError:
                logger.warning("AI returned invalid JSON for %s", file_path)
                issues.append({"file": file_path, "line": 0, "code": "AIReview", "message": ai_output})

        except RateLimitError as e:
            logger.error("RateLimitError for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "RateLimitError", "message": str(e)})
        except APIError as e:
            logger.error("APIError for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "APIError", "message": str(e)})
        except OpenAIError as e:
            logger.error("OpenAIError for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "OpenAIError", "message": str(e)})
        except Exception as e:
            logger.error("Unknown error for %s: %s", file_path, e)
            issues.append({"file": file_path, "line": 0, "code": "UnknownError", "message": str(e)})

    if issues:
        logger.warning("Found %d issue(s).", len(issues))
    return issues
