from enum import Enum

from .ai_client import AIClient
from .eval import CompareResult


class ProgrammingLanguage(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"


class Transcoder:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client

    async def __call__(
        self,
        input_code: str,
        input_language: ProgrammingLanguage,
        output_language: ProgrammingLanguage,
    ) -> str:
        return await self.ai_client(_system_prompt(input_language, output_language), input_code)

    async def iterate(
        self,
        input_language: ProgrammingLanguage,
        input_code: str,
        output_language: ProgrammingLanguage,
        output_code: str,
        discrependies: list[CompareResult],
    ) -> str:
        return await self.ai_client(
            _system_prompt_iterate(input_language, input_code, output_language, output_code),
            "\n".join(d.model_dump_json() for d in discrependies),
        )


def _system_prompt(input_language: ProgrammingLanguage, output_language: ProgrammingLanguage):
    return f"""
    You will receive a code snippet in language {input_language.name}. Rewrite the code in
    language {output_language.name}. The code snippet will contain a top-level function called
    `main`: your code must also define a top-level function called `main`.
    """


def _system_prompt_iterate(
    input_language: ProgrammingLanguage,
    input_code: str,
    output_language: ProgrammingLanguage,
    output_code: str,
):
    return f"""
    [no prose]
    [only {output_language}]
    An attempt was made to convert some code from {input_language.name} to {output_language.name} but 
    some errors were made. The base code is \n\n{input_code}\n\n and the new code is \n\n{output_code}\n\n.
    I'll send you the test cases for which the base code's output did not match the new code's output.
    Consider these discrepencies and response with EXACTLY a code snippet with an amended solution in language {output_language.name}.
    """
