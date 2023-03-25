from discord import Message, Embed, Color, ui, Interaction, File, ButtonStyle
from discord.ext import commands
from datetime import datetime
from io import StringIO

from scripts.utils import listener_auth, append_attachments
from scripts.views.CreateButton import CreateButton

class Messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        if listener_auth(message=message):
            return
    
        embed = Embed(
            description=f'Message ID : {message.id}',
            color=Color.red(),
            timestamp=datetime.now()
        )
    
        embed.set_author(name=message.author, icon_url=message.author.avatar.url)
        embed.add_field(name='Channel', value=f'<#{message.channel.id}>', inline=False)

        list = append_attachments(target=message, list=[])

        if len(message.content) > 0:
            content = message.content

            if len(content) > 1024:
                content = '埋め込みの文字数上限に達したため、下のボタンから削除されたメッセージの内容をファイルに出力できます。'

            embed.add_field(name='Content', value=f'{content}', inline=False)

        if not len(list) == 0:
            embed.add_field(name='Attachments', value='\n'.join(list), inline=False)

        if len(message.content) > 1024:
            views = ui.View(timeout=None)

            async def callback(interaction: Interaction):
                with StringIO(message.content) as txtFile:
                    await interaction.response.send_message(file=File(txtFile, 'content.txt'), ephemeral=True)

            views.add_item(CreateButton(style=ButtonStyle.primary, label='Export', emoji='📜', disabled=False, callback=callback))

            await self.client.get_channel(1087364865003364422).send(embeds=[embed], view=views)
        else:
            await self.client.get_channel(1087364865003364422).send(embeds=[embed])

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if listener_auth(message=after):
            return
        
        if before.content == after.content:
            return
        
        embed = Embed(
            color=Color.red(),
            timestamp=datetime.now()
        )

        embed.set_author(name=after.author, icon_url=after.author.avatar.url)
        embed.add_field(name='Channel', value=f'<#{after.channel.id}>', inline=False)

        before_list = append_attachments(target=before, list=[])
        after_list = append_attachments(target=after, list=[])

        if len(before.content) > 0:
            before_content = before.content

            if len(before_content) > 1024:
                before_content = '埋め込みの文字数上限に達したため、下のボタンから削除されたメッセージの内容をファイルに出力できます。'

            embed.add_field(name='BeforeContent', value=f'{before_content}', inline=False)

        if len(after.content) > 0:
            after_content = after.content

            if len(after_content) > 1024:
                after_content = '埋め込みの文字数上限に達したため、下のボタンから削除されたメッセージの内容をファイルに出力できます。'

            embed.add_field(name='AfterContent', value=f'{after_content}', inline=False)

        if not len(before_list) == 0:
            embed.add_field(name='BeforeAttachments', value='\n'.join(before_list), inline=False)

        if not len(after_list) == 0:
            embed.add_field(name='AfterAttachments', value='\n'.join(after_list), inline=False)

        async def before_callback(interaction: Interaction):
            with StringIO(before.content) as txtFile:
                await interaction.response.send_message(file=File(txtFile, 'before_content.txt'), ephemeral=True)

        async def after_callback(interaction: Interaction):
            with StringIO(after.content) as txtFile:
                await interaction.response.send_message(file=File(txtFile, 'after_content.txt'), ephemeral=True)

        if len(before.content) > 1024 or len(after.content) > 1024:
            views = ui.View()

            if len(before.content) > 1024 and len(after.content) > 1024:
                views.add_item(CreateButton(style=ButtonStyle.primary, label='BeforeExport', emoji='📜', disabled=False, callback=before_callback))
                views.add_item(CreateButton(style=ButtonStyle.primary, label='AfterExport', emoji='📜', disabled=False, callback=after_callback))

                await self.client.get_channel(1087364865003364422).send(embeds=[embed], view=views)
            elif len(before.content) > 1024:
                views.add_item(CreateButton(style=ButtonStyle.primary, label='BeforeExport', emoji='📜', disabled=False, callback=before_callback))

                await self.client.get_channel(1087364865003364422).send(embeds=[embed], view=views)
            elif len(after.content) > 1024:
                views.add_item(CreateButton(style=ButtonStyle.primary, label='AfterExport', emoji='📜', disabled=False, callback=after_callback))

                await self.client.get_channel(1087364865003364422).send(embeds=[embed], view=views)   
        else:
            await self.client.get_channel(1087364865003364422).send(embeds=[embed])

def setup(client: commands.Bot):
    client.add_cog(Messages(client=client))
