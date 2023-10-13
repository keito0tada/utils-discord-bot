import abc
import enum
import zoneinfo
from typing import Optional, List, Union, NamedTuple, Sequence, Callable, Any

import discord
from discord.ext import commands, tasks

from . import commandparser

ZONE_TOKYO = zoneinfo.ZoneInfo("Asia/Tokyo")


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


class IWindow2(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def send(self, sender: discord.abc.Messageable) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def reply(self, message: discord.Message) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def response_send(self, interaction: discord.Interaction) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def edit(self, message: discord.Message) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def response_edit(self, interaction: discord.Interaction) -> discord.Message:
        raise NotImplementedError


class Window(IWindow2):
    def __init__(
        self,
        content: str = None,
        tts: bool = False,
        embed: discord.Embed = None,
        embeds: list[discord.Embed] = None,
        file: discord.File = None,
        files: list[discord.File] = None,
        stickers: Sequence[Union[discord.GuildSticker, discord.StickerItem]] = None,
        delete_after: float = None,
        nonce: int = None,
        allowed_mentions: discord.AllowedMentions = None,
        reference: Union[
            discord.Message, discord.MessageReference, discord.PartialMessage
        ] = None,
        mention_author: bool = None,
        view: discord.ui.View = None,
        suppress_embeds: bool = False,
        silent: bool = False,
        ephemeral: bool = False,
        emojis: list[
            Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]
        ] = None,
    ) -> None:
        self.content = content
        self.tts = tts
        self.embed = embed
        self.embeds = embeds
        self.file = file
        self.files = files
        self.stickers = stickers
        self.delete_after = delete_after
        self.nonce = nonce
        self.allowed_mentions = allowed_mentions
        self.reference = reference
        self.mention_author = mention_author
        self.view = view
        self.suppress_embeds = suppress_embeds
        self.silent = silent
        self.emojis = emojis
        self.ephemeral = ephemeral
        self.args_messageable_send = {
            "tts": tts,
            "suppress_embeds": suppress_embeds,
            "silent": silent,
        }
        self.args_messageable_edit = {
            "suppress": suppress_embeds,
        }
        self.args_interaction_send = {
            "tts": tts,
            "ephemeral": ephemeral,
            "suppress_embeds": suppress_embeds,
            "silent": silent,
        }
        self.args_interaction_edit = {}
        if content is not None:
            self.args_messageable_send["content"] = content
            self.args_messageable_edit["content"] = content
            self.args_interaction_send["content"] = content
            self.args_interaction_edit["content"] = content
        if embed is not None:
            self.args_messageable_send["embed"] = embed
            self.args_messageable_edit["embed"] = embed
            self.args_interaction_send["embed"] = embed
            self.args_interaction_edit["embed"] = embed
        if embeds is not None:
            self.args_messageable_send["embeds"] = embeds
            self.args_messageable_edit["embeds"] = embeds
            self.args_interaction_send["embeds"] = embeds
            self.args_interaction_edit["embeds"] = embeds
        if file is not None:
            self.args_messageable_send["file"] = file
            self.args_messageable_edit["attachments"] = [file]
            self.args_interaction_send["file"] = file
            self.args_interaction_edit["attachments"] = [file]
        if files is not None:
            self.args_messageable_send["files"] = files
            self.args_messageable_edit["attachments"] = files
            self.args_interaction_send["files"] = files
            self.args_interaction_edit["attachments"] = files
        if stickers is not None:
            self.args_messageable_send["stickers"] = stickers
        if delete_after is not None:
            self.args_messageable_send["delete_after"] = delete_after
            self.args_messageable_edit["delete_after"] = delete_after
            self.args_interaction_send["delete_after"]
            self.args_interaction_edit["delete_after"] = delete_after
        if nonce is not None:
            self.args_messageable_send["nonce"] = nonce
        if allowed_mentions is not None:
            self.args_messageable_send["allowed_mentions"] = allowed_mentions
            self.args_messageable_edit["allowed_mentions"] = allowed_mentions
            self.args_interaction_send["allowed_mentions"] = allowed_mentions
            self.args_interaction_edit["allowed_mentions"] = allowed_mentions
        if reference is not None:
            self.args_messageable_send["reference"] = reference
        if mention_author is not None:
            self.args_messageable_send["mention_author"] = mention_author
        if view is not None:
            self.args_messageable_send["view"] = view
            self.args_messageable_edit["view"] = view
            self.args_interaction_send["view"] = view
            self.args_interaction_edit["view"] = view

    def copy(
        self,
        content: str = None,
        tts: bool = False,
        embed: discord.Embed = None,
        embeds: list[discord.Embed] = None,
        file: discord.File = None,
        files: list[discord.File] = None,
        stickers: Sequence[Union[discord.GuildSticker, discord.StickerItem]] = None,
        delete_after: float = None,
        nonce: int = None,
        allowed_mentions: discord.AllowedMentions = None,
        reference: Union[
            discord.Message, discord.MessageReference, discord.PartialMessage
        ] = None,
        mention_author: bool = None,
        view: discord.ui.View = None,
        suppress_embeds: bool = False,
        silent: bool = False,
        ephemeral: bool = False,
        emojis: list[
            Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]
        ] = None,
    ) -> "Window":
        return Window(
            content=content,
            tts=tts,
            embed=embed,
            embeds=embeds,
            file=file,
            files=files,
            stickers=stickers,
            delete_after=delete_after,
            nonce=nonce,
            allowed_mentions=allowed_mentions,
            reference=reference,
            mention_author=mention_author,
            view=view,
            suppress_embeds=suppress_embeds,
            silent=silent,
            ephemeral=ephemeral,
            emojis=emojis,
        )

    async def send(self, sender: discord.abc.Messageable) -> discord.Message:
        message: discord.Message = await sender.send(**self.args_messageable_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def reply(self, message: discord.Message) -> discord.Message:
        message: discord.Message = await message.reply(**self.args_messageable_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def response_send(self, interaction: discord.Interaction) -> discord.Message:
        message = await interaction.response.send_message(**self.args_interaction_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def edit(self, message: discord.Message) -> discord.Message:
        message: discord.Message = await message.edit(**self.args_messageable_edit)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def response_edit(self, interaction: discord.Interaction) -> discord.Message:
        message: discord.Message = await interaction.response.edit_message(
            **self.args_messageable_send
        )
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message


class Windows:
    def __init__(self, defaultWindow) -> None:
        self.defautlWindow = defaultWindow
        self.message: discord.Message = None

    async def run(self, interaction: discord.Interaction):
        self.message = await self.defautlWindow.response_send(interaction=interaction)

    async def destroy(self):
        if self.message is not None:
            await self.message.destroy()


class Pages(Windows):
    def __init__(self, windows: list[Callable[[], Window]]) -> None:
        if len(windows) <= 0:
            raise ValueError
        super().__init__(defaultWindow=windows[0]())


class IRunner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def run(self, interaction: discord.Interaction):
        raise NotImplementedError

    @abc.abstractmethod
    async def destroy(self):
        raise NotImplementedError


class Runner(IRunner):
    def __init__(self, channel: discord.TextChannel, timeout: float = None):
        self.channel = channel
        self.timeout = timeout

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
        self.runners = [
            runner
            for runner in self.runners
            if await runner.timeout_check(minutes=Command.MINUTES)
        ]
