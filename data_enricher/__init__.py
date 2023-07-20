"""
The data_enricher package.

This package contains the DataEnricherLLM application. The application is designed to gather data from the web and enrich prompts for better responses from Language Learning Models (LLMs). The main purpose of this package is to offer an alternative to browser extensions for enriching LLM prompts and to provide a way to improve LLM responses without concern for response time.

Modules:
    enricher: Contains the Enricher class responsible for gathering data and enriching prompts.
    llm_api: wraps calls to OpenAI API
"""

from enricher import Enricher
from llm_api import LLM_API