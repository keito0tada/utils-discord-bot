import discord
from discord.ext import commands, tasks

from commandparser import commandparser
from runner import Runner
from typing import List

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