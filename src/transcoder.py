from enum import Enum

from .ai_client import AIClient


class InputLanguage(str, Enum):
    PYTHON = "python"


class OutputLanguage(str, Enum):
    JAVASCRIPT = "javascript"


class Transcoder:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client

    async def __call__(
        self,
        input_code: str,
        input_language: InputLanguage,
        output_language: OutputLanguage,
    ) -> str:
        return await self.ai_client(
            _system_prompt(input_language, output_language), input_code
        )


def _system_prompt(input_language: InputLanguage, output_language: OutputLanguage):
    return f"""
    You will receive a code snippet in language {input_language.name}. Rewrite the code in
    language {output_language.name}. The code snippet will contain a top-level function called
    `main`: your code must also define a top-level function called `main`.
    """
