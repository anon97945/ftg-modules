from .. import loader
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest


def register(cb):
    cb(OwnershipsMod())
    
class OwnershipsMod(loader.Module):
    """Zeigt Besitztümer an."""
    strings = {'name': 'Ownerships'}
    
    async def owncmd(self, message):
        """Der Befehl .own listet den Besitz offener Chats / Kanäle auf. """
        await message.edit('<b>Bearbeite...</b>')
        result = await message.client(GetAdminedPublicChannelsRequest())
        msg = ""
        count = 0
        for obj in result.chats:
            count += 1
            msg += f'\n• <a href="tg://resolve?domain={obj.username}">{obj.title}</a> <b>|</b> <code>{obj.id}</code>'
        await message.edit(f'<b>Meine Kanäle/Gruppen: {count}</b>\n {msg}')
