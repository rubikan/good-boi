from dataclasses import dataclass
from typing import List
import json
import os


@dataclass
class GuildAndChannel:
    guildId: str
    channelId: str


@dataclass
class DiscordConfig:
    token: str
    announceGuilds: List[GuildAndChannel]


@dataclass
class OpenAIConfig:
    baseUrl: str
    apiKey: str
    model: str
    chatPrompt: str


@dataclass
class ReplicateConfig:
    token: str


@dataclass
class GoodBoiConfig:
    discord: DiscordConfig
    replicate: ReplicateConfig
    openai: OpenAIConfig


def load_config(location="data/config.json") -> GoodBoiConfig:
    with open(location, "r") as f:
        config_dict = json.load(f)
        # the replicate API wants the API token as an environment variable
        config = GoodBoiConfig(**config_dict)
        os.environ["REPLICATE_API_TOKEN"] = config.replicate.token
        return config
