from typing import Optional, Union, NamedTuple

import discord
from .base import Runner


class Button(discord.ui.Button):
    def __init__(
        self,
        runner: Runner,
        style: discord.ButtonStyle = None,
        label: Optional[str] = None,
        disabled=False,
        custom_id: Optional[str] = None,
        url: Optional[str] = None,
        emoji: Optional[Union[discord.PartialEmoji, discord.Emoji, str]] = None,
        row: Optional[int] = None,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        self.runner = runner


class View(discord.ui.View):
    def __init__(self, runner: Runner):
        super().__init__(timeout=None)
        self.runner = runner

    async def on_timeout(self) -> None:
        await self.runner.destroy()


class Emoji(NamedTuple):
    discord: str
    text: str
    url: str
