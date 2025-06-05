import abc
import discord

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