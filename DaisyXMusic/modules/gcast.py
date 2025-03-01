
from pyrogram import Client, filters
from pyrogram.types import Message
from DaisyXMusic.leejieun import get_arg
from DaisyXMusic.sql.chat_sql import load_chats_list, remove_chat_from_db
from DaisyXMusic.services.callsmusic.callsmusic import client as USER
from DaisyXMusic.helpers.filters import other_filters, other_filters2
from DaisyXMusic.helpers.decorators import authorized_users_only, errors
from io import BytesIO


@Client.on_message(filters.command("gcast"))
@authorized_users_only
async def broadcast(client: Client, message: Message):
    to_send = get_arg(message)
    success = 0
    failed = 0
    for chat in load_chats_list():
        try:
            await client.send_message(
                str(chat), 
                to_send
            )
            success += 1
        except:
            failed += 1
            pass
    await message.reply(
        f"Message sent to {success} chat(s). {failed} chat(s) failed recieve message"
    )


@Client.on_message(filters.command("chatlist"))
async def chatlist(client, message):
    chats = []
    all_chats = load_chats_list()
    for i in all_chats:
        if str(i).startswith("-"):
            chats.append(i)
    chatfile = "Daftar chat.\n0. ID grup | Jumlah anggota | tautan undangan\n"
    P = 1
    for chat in chats:
        try:
            link = await client.export_chat_invite_link(int(chat))
        except:
            link = "Null"
        try:
            members = await client.get_chat_members_count(int(chat))
        except:
            members = "Null"
        try:
            chatfile += "{}. {} | {} | {}\n".format(P, chat, members, link)
            P = P + 1
        except:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        await message.reply_document(document=output, disable_notification=True)
