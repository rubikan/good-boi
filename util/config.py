from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import List
import os


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GuildAndChannel:
    guild_id: str
    channel_id: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DiscordConfig:
    token: str
    announce_guilds: List[GuildAndChannel]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class OpenAIConfig:
    base_url: str
    api_key: str
    model: str
    chat_prompt: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReplicateConfig:
    token: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GoodBoiConfig:
    discord: DiscordConfig
    replicate: ReplicateConfig
    openai: OpenAIConfig


def load_config(location="data/config.json") -> GoodBoiConfig:
    with open(location, "r") as f:
        text = f.read()
        config = GoodBoiConfig.from_json(text)
        # the replicate API wants the API token as an environment variable
        os.environ["REPLICATE_API_TOKEN"] = config.replicate.token
        return config
