import abc
import enum
import zoneinfo
from typing import Optional, List, Union, NamedTuple

import discord
import psycopg2
from discord.ext import commands, tasks

from . import commandparser

ZONE_TOKYO = zoneinfo.ZoneInfo('Asia/Tokyo')


class DuplicatedSendError(Exception):
    pass


class Popups:
    def __init__(self, modal_patterns: List[Optional[discord.ui.Modal]]):
        self.modal_patterns = modal_patterns
        self.modal = modal_patterns[0]

    def set_pattern(self, index: int):
        self.modal = self.modal_patterns[index]

    async def response_send(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.modal)


class IWindow(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def destroy(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check_index(self, index: enum.IntEnum):
        raise NotImplementedError

    @abc.abstractmethod
    def get_embed_dict(self, index: enum.IntEnum) -> Optional[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_embeds_dicts(self, index: enum.IntEnum) -> Optional[list]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_view_items(self, index: enum.IntEnum) -> Optional[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, sender: discord.abc.Messageable, index: enum.IntEnum) -> 'IWindow':
        raise NotImplementedError

    @abc.abstractmethod
    async def reply(self, message: discord.Message, index: enum.IntEnum) -> 'IWindow':
        raise NotImplementedError

    @abc.abstractmethod
    async def response_send(self, interaction: discord.Interaction, index: enum.IntEnum) -> 'IWindow':
        raise NotImplementedError

    @abc.abstractmethod
    async def edit(self, message: discord.Message, index: enum.IntEnum) -> 'IWindow':
        raise NotImplementedError

    @abc.abstractmethod
    async def response_edit(self, interaction: discord.Interaction, index: enum.IntEnum) -> 'IWindow':
        raise NotImplementedError


class Window(IWindow):
    def __init__(self, content: Optional[str] = None, embed_dict: Optional[dict] = None,
                 embeds_dicts: Optional[dict] = None, view_items: Optional[list[discord.ui.Item]] = None,
                 emojis: Optional[list[str]] = None):
        self.message: Optional[discord.Message] = None
        self.content = content
        self.embed_dict = embed_dict
        self._embed: Optional[discord.Embed] = None
        self.embeds_dicts = embeds_dicts
        self._embeds: Optional[list[discord.Embed]] = None
        self.view_items = view_items
        self._view: Optional[discord.ui.View()] = None
        self.emojis = emojis

    def is_sent(self) -> bool:
        return self.message is not None

    def check_index(self, index: enum.IntEnum):
        if index != 0:
            raise IndexError

    def destroy(self):
        self._view().stop()

    def get_embed_dict(self, index: enum.IntEnum):
        self.check_index(index=index)
        return self.embed_dict

    def get_embeds_dicts(self, index: enum.IntEnum):
        self.check_index(index=index)
        return self.embeds_dicts

    def get_view_items(self, index: enum.IntEnum):
        self.check_index(index=index)
        return self.view_items

    def _prepare_message(self):
        if self.embed_dict is None:
            self._embed = None
        else:
            self._embed = discord.Embed.from_dict(self.embed_dict)
        if self.embeds_dicts is None:
            self._embeds = None
        else:
            self._embeds = [discord.Embed.from_dict(embed) for embed in self.embeds_dicts]
        if self.view_items is None:
            self._view = None
        else:
            self._view = discord.ui.View()
            for item in self.view_items:
                self._view.add_item(item=item)

    async def send(self, sender: discord.abc.Messageable, index: enum.IntEnum) -> 'IWindow':
        if self.is_sent():
            raise DuplicatedSendError
        self._prepare_message()
        if self.content is None:
            if self._embed is None:
                if self._embeds is None:
                    raise ValueError
                else:
                    if self._view is None:
                        self.message = await sender.send(embeds=self._embeds)
                    else:
                        self.message = await sender.send(embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await sender.send(embed=self._embed)
                    else:
                        self.message = await sender.send(embed=self._embed, view=self._view)
                else:
                    raise ValueError
        else:
            if self._embed is None:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await sender.send(content=self.content)
                    else:
                        self.message = await sender.send(content=self.content, view=self._view)
                else:
                    if self._view is None:
                        self.message = await sender.send(content=self.content, embeds=self._embeds)
                    else:
                        self.message = await sender.send(content=self.content, embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await sender.send(content=self.content, embed=self._embed)
                    else:
                        self.message = await sender.send(content=self.content, embed=self._embed, view=self._view)
                else:
                    raise ValueError
        if self.emojis is not None:
            for emoji in self.emojis:
                await self.message.add_reaction(emoji)
        return self

    async def reply(self, message: discord.Message, index: enum.IntEnum) -> 'IWindow':
        if self.is_sent():
            raise DuplicatedSendError
        self._prepare_message()
        if self.content is None:
            if self._embed is None:
                if self._embeds is None:
                    raise ValueError
                else:
                    if self._view is None:
                        self.message = await message.reply(embeds=self._embeds)
                    else:
                        self.message = await message.reply(embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await message.reply(embed=self._embed)
                    else:
                        self.message = await message.reply(embed=self._embed, view=self._view)
                else:
                    raise ValueError
        else:
            if self._embed is None:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await message.reply(content=self.content)
                    else:
                        self.message = await message.reply(content=self.content, view=self._view)
                else:
                    if self._view is None:
                        self.message = await message.reply(content=self.content, embeds=self._embeds)
                    else:
                        self.message = await message.reply(content=self.content, embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await message.reply(content=self.content, embed=self._embed)
                    else:
                        self.message = await message.reply(content=self.content, embed=self._embed, view=self._view)
                else:
                    raise ValueError
        if self.emojis is not None:
            for emoji in self.emojis:
                await self.message.add_reaction(emoji)
        return self

    async def response_send(self, interaction: discord.Interaction, index: enum.IntEnum) -> 'IWindow':
        if self.is_sent():
            raise DuplicatedSendError
        self._prepare_message()
        if self.content is None:
            if self._embed is None:
                if self._embeds is None:
                    raise ValueError
                else:
                    if self._view is None:
                        self.message = await interaction.response.send_message(embeds=self._embeds)
                    else:
                        self.message = await interaction.response.send_message(embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await interaction.response.send_message(embed=self._embed)
                    else:
                        self.message = await interaction.response.send_message(embed=self._embed, view=self._view)
                else:
                    raise ValueError
        else:
            if self._embed is None:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await interaction.response.send_message(content=self.content)
                    else:
                        self.message = await interaction.response.send_message(content=self.content, view=self._view)
                else:
                    if self._view is None:
                        self.message = await interaction.response.send_message(content=self.content, embeds=self._embeds)
                    else:
                        self.message = await interaction.response.send_message(content=self.content, embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await interaction.response.send_message(content=self.content, embed=self._embed)
                    else:
                        self.message = await interaction.response.send_message(content=self.content, embed=self._embed, view=self._view)
                else:
                    raise ValueError
        if self.emojis is not None:
            for emoji in self.emojis:
                await self.message.add_reaction(emoji)
        return self

    async def edit(self, message: discord.Message, index: enum.IntEnum) -> 'IWindow':
        self._prepare_message()
        if self.content is None:
            if self._embed is None:
                if self._embeds is None:
                    raise ValueError
                else:
                    if self._view is None:
                        self.message = await message.edit(embeds=self._embeds)
                    else:
                        self.message = await message.edit(embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await message.edit(embed=self._embed)
                    else:
                        self.message = await message.edit(embed=self._embed, view=self._view)
                else:
                    raise ValueError
        else:
            if self._embed is None:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await message.edit(content=self.content)
                    else:
                        self.message = await message.edit(content=self.content, view=self._view)
                else:
                    if self._view is None:
                        self.message = await message.edit(content=self.content, embeds=self._embeds)
                    else:
                        self.message = await message.edit(content=self.content, embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await message.edit(content=self.content, embed=self._embed)
                    else:
                        self.message = await message.edit(content=self.content, embed=self._embed, view=self._view)
                else:
                    raise ValueError
        if self.emojis is not None:
            for emoji in self.emojis:
                await self.message.add_reaction(emoji)
        return self

    async def response_edit(self, interaction: discord.Interaction, index: enum.IntEnum) -> 'IWindow':
        self._prepare_message()
        if self.content is None:
            if self._embed is None:
                if self._embeds is None:
                    raise ValueError
                else:
                    if self._view is None:
                        self.message = await interaction.response.edit_message(embeds=self._embeds)
                    else:
                        self.message = await interaction.response.edit_message(embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await interaction.response.edit_message(embed=self._embed)
                    else:
                        self.message = await interaction.response.edit_message(embed=self._embed, view=self._view)
                else:
                    raise ValueError
        else:
            if self._embed is None:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await interaction.response.edit_message(content=self.content)
                    else:
                        self.message = await interaction.response.edit_message(content=self.content, view=self._view)
                else:
                    if self._view is None:
                        self.message = await interaction.response.edit_message(content=self.content, embeds=self._embeds)
                    else:
                        self.message = await interaction.response.edit_message(content=self.content, embeds=self._embeds, view=self._view)
            else:
                if self._embeds is None:
                    if self._view is None:
                        self.message = await interaction.response.edit_message(content=self.content, embed=self._embed)
                    else:
                        self.message = await interaction.response.edit_message(content=self.content, embed=self._embed, view=self._view)
                else:
                    raise ValueError
        if self.emojis is not None:
            for emoji in self.emojis:
                await self.message.add_reaction(emoji)
        return self


class Windows(IWindow):
    def __init__(self, windows: tuple[IWindow, ...]):
        self.windows = windows
        self.index: Optional[enum.IntEnum] = None

    def destroy(self):
        self.windows[self.index].desctroy()

    def check_index(self, index: enum.IntEnum):
        if index < 0 or len(self.windows) <= index:
            raise IndexError

    def get_embed_dict(self, index: enum.IntEnum) -> Optional[dict]:
        self.check_index(index=index)
        return self.windows[index].get_embed_dict(index=0)

    def get_embeds_dicts(self, index: enum.IntEnum) -> Optional[list]:
        self.check_index(index=index)
        return self.windows[index].get_embeds_dicts(index=0)

    def get_view_items(self, index: enum.IntEnum) -> Optional[dict]:
        self.check_index(index=index)
        return self.windows[index].get_view_items(index=0)

    async def send(self, sender: discord.abc.Messageable, index: enum.IntEnum) -> 'IWindow':
        win = await self.windows[index].send(sender=sender, index=0)
        if isinstance(win, Window):
            self.index = index
            return self
        elif isinstance(win, Windows):
            self.windows[self.index].destroy()
            self.index = index
            return win
        else:
            raise TypeError

    async def reply(self, message: discord.Message, index: enum.IntEnum) -> 'IWindow':
        win = await self.windows[index].reply(message=message, index=0)
        if isinstance(win, Window):
            return self
        elif isinstance(win, Windows):
            self.windows[self.index].destroy()
            self.index = index
            return win
        else:
            raise TypeError

    async def response_send(self, interaction: discord.Interaction, index: enum.IntEnum) -> 'IWindow':
        self.index = index
        win = await self.windows[index].response_send(interaction=interaction, index=0)
        if isinstance(win, Window):
            return self
        elif isinstance(win, Windows):
            self.windows[self.index].destroy()
            self.index = index
            return win
        else:
            raise TypeError

    async def edit(self, message: discord.Message, index: enum.IntEnum) -> 'IWindow':
        self.index = index
        win = await self.windows[index].edit(message=message, index=0)
        if isinstance(win, Window):
            return self
        elif isinstance(win, Windows):
            return win
        else:
            raise TypeError

    async def response_edit(self, interaction: discord.Interaction, index: enum.IntEnum) -> 'IWindow':
        self.index = index
        win = await self.windows[index].response_edit(interaction=interaction, index=0)
        if isinstance(win, Window):
            return self
        elif isinstance(win, Windows):
            return win
        else:
            raise TypeError


class Runner:
    def __init__(self, channel: discord.TextChannel, timeout: float = 3.0):
        self.channel = channel
        self.timeout = timeout

    async def run(self, interaction: discord.Interaction):
        pass

    async def destroy(self):
        pass

    async def timeout_check(self, minutes: float) -> bool:
        self.timeout -= minutes
        if self.timeout <= 0:
            await self.destroy()
            return True
        else:
            return False


class GroupCog(commands.GroupCog):
    def __init__(self, bot: discord.ext.commands.Bot, allow_duplicated: bool):
        super().__init__()
        self.bot = bot
        self.allow_duplicated = allow_duplicated


class Command(commands.Cog):
    MINUTES = 3.0

    def __init__(self, bot: discord.ext.commands.Bot, allow_duplicated=False):
        self.bot = bot
        self.allow_duplicated = allow_duplicated
        self.parser = commandparser.CommandParser()
        self.runners: List[Runner] = []

    @tasks.loop(minutes=MINUTES)
    async def timeout_check(self):
        self.runners = [runner for runner in self.runners if await runner.timeout_check(minutes=Command.MINUTES)]
