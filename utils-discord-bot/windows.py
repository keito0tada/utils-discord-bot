from .window import Window
import discord

class Windows:
    def __init__(self, defaultWindow: Window) -> None:
        self.defautlWindow = defaultWindow
        self.message: discord.Message = None

    async def run(self, interaction: discord.Interaction):
        self.message = await self.defautlWindow.response_send(interaction=interaction)

    async def destroy(self):
        if self.message is not None:
            await self.message.destroy()


class Pages(Windows):
    class PageNumberModal(discord.ui.Modal, title="ページ番号"):
        page_input = discord.ui.TextInput(label="ページ番号")

        def __init__(self, pages: "Pages"):
            super().__init__()
            self.pages = pages

        async def on_submit(self, interaction: discord.Interaction) -> None:
            await self.pages.move_on_page_number(
                page_number=int(self.page_input.value), interaction=interaction
            )

    class NextButton(discord.ui.Button):
        def __init__(self, pages: "Pages", disabled: bool = False):
            super().__init__(label=">>", disabled=disabled)
            self.pages = pages

        async def callback(self, interaction: discord.Interaction) -> None:
            await self.pages.move_to_side(next=True, interaction=interaction)

    class PrevButton(discord.ui.Button):
        def __init__(self, pages: "Pages", disabled: bool = False):
            super().__init__(label="<<", disabled=disabled)
            self.pages = pages

        async def callback(self, interaction: discord.Interaction) -> None:
            await self.pages.move_to_side(next=False, interaction=interaction)

    class PageButton(discord.ui.Button):
        def __init__(self, pages: "Pages", index: int):
            super().__init__(label="{0}/{1}".format(index, pages.length()))
            self.pages = pages

        async def callback(self, interaction: discord.Interaction) -> None:
            await interaction.response.send_modal(
                Pages.PageNumberModal(pages=self.pages)
            )

    def __init__(self, windows: list[Window], defaultIndex: int = 0) -> None:
        if len(windows) <= 0:
            raise ValueError
        self.index = defaultIndex
        self.windows = windows
        for index in range(self.length()):
            if self.windows[index].view is None:
                self.windows[index] = self.windows[index].copy(view=discord.ui.View())
            window = self.windows[index]
            if len(window.view.children) >= 23:
                raise ValueError
            window.view.add_item(Pages.PrevButton(pages=self, disabled=index <= 0))
            window.view.add_item(Pages.PageButton(pages=self, index=index + 1))
            window.view.add_item(
                Pages.NextButton(pages=self, disabled=self.length() - 1 <= index)
            )
        super().__init__(defaultWindow=windows[defaultIndex])

    def length(self):
        return len(self.windows)

    async def move_on_page_number(
        self, page_number: int, interaction: discord.Interaction
    ):
        page_number -= 1
        if page_number < 0 or self.length() <= page_number:
            raise IndexError
        self.index = page_number
        await self.windows[page_number].response_edit(interaction=interaction)

    async def move_to_side(self, next: bool, interaction: discord.Interaction):
        if next:
            if self.index + 1 < self.length():
                await self.windows[self.index + 1].response_edit(
                    interaction=interaction
                )
                self.index += 1
            else:
                raise IndexError
        else:
            if 0 <= self.index - 1:
                await self.windows[self.index - 1].response_edit(
                    interaction=interaction
                )
                self.index -= 1
            else:
                raise IndexError