import abc
from typing import Union

from .config import AIConfig


class AIClient(abc.ABC):
    def __init__(self, config: AIConfig):
        self.config = config

    @abc.abstractmethod
    async def __call__(self, system_prompt: Union[str, None], user_prompt: str) -> str:
        pass
