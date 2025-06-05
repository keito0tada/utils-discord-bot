import abc
import discord
from typing import Optional, Union, Sequence, Any

class UnSetType:
    pass

UnSet = UnSetType()

class IWindow(metaclass=abc.ABCMeta):
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


class Window(IWindow):
    def __init__(
        self,
        content: Optional[str] = None,
        tts: bool = False,
        embed: Optional[discord.Embed] = None,
        embeds: Optional[list[discord.Embed]] = None,
        file: Optional[discord.File] = None,
        files: Optional[list[discord.File]] = None,
        stickers: Optional[
            Sequence[Union[discord.GuildSticker, discord.StickerItem]]
        ] = None,
        delete_after: Optional[float] = None,
        nonce: Optional[int] = None,
        allowed_mentions: Optional[discord.AllowedMentions] = None,
        reference: Union[
            discord.Message, discord.MessageReference, discord.PartialMessage, None
        ] = None,
        mention_author: Optional[bool] = None,
        view: Optional[discord.ui.View] = None,
        suppress_embeds: bool = False,
        silent: bool = False,
        ephemeral: bool = False,
        emojis: Optional[
            list[Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]]
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
        self.args_messageable_send: dict[str, Any] = {
            "tts": tts,
            "suppress_embeds": suppress_embeds,
            "silent": silent,
        }
        self.args_messageable_edit: dict[str, Any] = {
            "suppress": suppress_embeds,
        }
        self.args_interaction_send: dict[str, Any] = {
            "tts": tts,
            "ephemeral": ephemeral,
            "suppress_embeds": suppress_embeds,
            "silent": silent,
        }
        self.args_interaction_edit: dict[str, Any] = {}
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
        content: Union[str, UnSetType] = UnSet,
        tts: Union[bool, UnSetType] = UnSet,
        embed: Union[discord.Embed, UnSetType] = UnSet,
        embeds: Union[list[discord.Embed], UnSetType] = UnSet,
        file: Union[discord.File, UnSetType] = UnSet,
        files: Union[list[discord.File], UnSetType] = UnSet,
        stickers: Union[
            Sequence[Union[discord.GuildSticker, discord.StickerItem]], UnSetType
        ] = UnSet,
        delete_after: Union[float, UnSetType] = UnSet,
        nonce: Union[int, UnSetType] = UnSet,
        allowed_mentions: Union[discord.AllowedMentions, UnSetType] = UnSet,
        reference: Union[
            discord.Message, discord.MessageReference, discord.PartialMessage, UnSetType
        ] = UnSet,
        mention_author: Union[bool, UnSetType] = UnSet,
        view: Union[discord.ui.View, UnSetType] = UnSet,
        suppress_embeds: Union[bool, UnSetType] = UnSet,
        silent: Union[bool, UnSetType] = UnSet,
        ephemeral: Union[bool, UnSetType] = UnSet,
        emojis: Union[
            list[Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]],
            UnSetType,
        ] = UnSet,
    ) -> "Window":
        return Window(
            content=self.content if content is UnSet else content,
            tts=self.tts if tts is UnSet else tts,
            embed=self.embed if embed is UnSet else embed,
            embeds=self.embeds if embeds is UnSet else embeds,
            file=self.file if file is UnSet else file,
            files=self.files if files is UnSet else files,
            stickers=self.stickers if stickers is UnSet else stickers,
            delete_after=self.delete_after if delete_after is UnSet else delete_after,
            nonce=self.nonce if nonce is UnSet else nonce,
            allowed_mentions=self.allowed_mentions
            if allowed_mentions is UnSet
            else allowed_mentions,
            reference=self.reference if reference is UnSet else reference,
            mention_author=self.mention_author
            if mention_author is UnSet
            else mention_author,
            view=self.view if view is UnSet else view,
            suppress_embeds=self.suppress_embeds
            if suppress_embeds is UnSet
            else suppress_embeds,
            silent=self.silent if silent is UnSet else silent,
            ephemeral=self.ephemeral if ephemeral is UnSet else ephemeral,
            emojis=self.emojis if emojis is UnSet else emojis,
        )

    async def send(self, sender: discord.abc.Messageable) -> discord.Message:
        message: discord.Message = await sender.send(**self.args_messageable_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def reply(self, message: discord.Message) -> discord.Message:
        new_message: discord.Message = await message.reply(**self.args_messageable_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await new_message.add_reaction(emoji=emoji)
        return new_message

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
            **self.args_interaction_edit
        )
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message