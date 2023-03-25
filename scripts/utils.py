from discord import Message

def append_attachments(target: Message, list: list) -> list:
    if len(target.attachments) > 0:
        for x in target.attachments:
            list.append(x.url)

    return list

def listener_auth(message: Message) -> bool:
    if message.author.bot or message.guild is None:
            return True
        
    return False
