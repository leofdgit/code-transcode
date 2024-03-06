from typing import Union

from openai import AsyncOpenAI

from .ai_client import AIClient
from .config import AIConfig


class OpenAIClient(AsyncOpenAI, AIClient):
    def __init__(self, config: AIConfig, *args, **kwargs):
        AIClient.__init__(self, config)
        AsyncOpenAI.__init__(self, *args, api_key=config.api_key, **kwargs)

    async def __call__(self, system_prompt: Union[str, None], user_prompt: str) -> str:
        print(f"Calling OpenAIClient with system_prompt={system_prompt}\n\nuser_prompt={user_prompt}")
        response = await self.chat.completions.create(
            max_tokens=1000,  # TODO: change this arbitrary value
            model=self.config.model,
            messages=(
                [{"role": "user", "content": user_prompt}]
                if system_prompt is None
                else [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {"role": "user", "content": user_prompt},
                ]
            ),
        )

        if (content := response.choices[0].message.content) is None:
            raise Exception("Received no content.")
        return content
