from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
import os


@dataclass_json
@dataclass
class GuildAndChannel:
    guildId: str
    channelId: str


@dataclass_json
@dataclass
class DiscordConfig:
    token: str
    announceGuilds: List[GuildAndChannel]


@dataclass_json
@dataclass
class OpenAIConfig:
    baseUrl: str
    apiKey: str
    model: str
    chatPrompt: str


@dataclass_json
@dataclass
class ReplicateConfig:
    token: str


@dataclass_json
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
