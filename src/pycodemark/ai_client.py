"""Centralized OpenAI client for PyCodemark."""

import os
import logging
from openai import OpenAI

logger = logging.getLogger("pycodemark")

client: OpenAI | None = None

try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("⚠️ OPENAI_API_KEY not set. AI features will be disabled.")
    else:
        client = OpenAI(api_key=api_key)
except Exception as e:
    logger.error("❌ Failed to initialize OpenAI client: %s", e)
    client = None
