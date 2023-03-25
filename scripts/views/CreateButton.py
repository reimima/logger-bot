from discord import ui, ButtonStyle, Interaction

class CreateButton(ui.Button):
    def __init__(self, style: ButtonStyle, label: str, emoji: str, disabled: bool, callback):
        super().__init__(style=style, label=label, emoji=emoji, disabled=disabled)

        self.button_callback = callback

    async def callback(self, interaction: Interaction):
        await self.button_callback(interaction=interaction)
