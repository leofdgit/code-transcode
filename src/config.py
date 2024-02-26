import os
from typing import Literal
from pydantic import BaseModel


class AIConfig(BaseModel):
    provider: Literal["open_ai"]
    model: str
    api_key: str


def load_required(name: str) -> str:
    if not (value := os.getenv(name)):
        raise Exception(f"No value for {name}")
    return value


def load_config() -> AIConfig:
    return AIConfig(
        provider=load_required("AI_PROVIDER"),
        model=load_required("AI_MODEL"),
        api_key=load_required("AI_API_KEY"),
    )
