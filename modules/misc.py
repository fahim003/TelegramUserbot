from pyrogram import Client, filters
from client import app
import time

@app.on_message(filters.command(["help"]), filters.me)
async def my_handler(client, message):
    await message.edit("Pyrogram")

@app.on_message(filters.command("id"), filters.me)
async def get_user_id(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        await message.edit(f"The user ID of the replied message is: {user_id}")
    elif message.command and len(message.command) > 1:
        username = message.command[1]
        user = client.get_users(username)
        await message.edit(f"The user ID of @{username} is: {user.id}")
    else:
        await message.edit("Please reply to a message or provide a username.")

@app.on_message(filters.command("time") & filters.reply, filters.me)
async def edit_to_current_time(client, message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.reply_to_message.edit(f"Current time is: {current_time}")


@app.on_message(filters.command("ping"), filters.me)
async def ping(client, message):
    start_time = time.time()
    response = await message.edit("Pong!")
    end_time = time.time()

    ping_time = (end_time - start_time) * 1000  # Convert to milliseconds
    await response.edit(f"Pong! 🏓\nPing: {ping_time:.2f} ms")


@app.on_message(filters.command("clear"), filters.me)
async def clear_chat(client, message):
    if len(message.command) < 2:
        await message.reply("Please specify the number of messages to delete.")
        return

    try:
        num_messages = int(message.command[1])
    except ValueError:
        await message.reply("Please provide a valid number of messages to delete.")
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    # Get the last num_messages
    messages_to_delete = []
    async for msg in client.get_chat_history(chat_id, limit=num_messages):
        messages_to_delete.append(msg)

    if message.chat.type == "private":
        # In private chat, delete only bot's messages
        own_message_ids = [msg.message_id for msg in messages_to_delete if msg.from_user.id == user_id]
        if own_message_ids:
            await client.delete_messages(chat_id, own_message_ids)
            await message.reply(f"Deleted {len(own_message_ids)} of my own messages.")
        else:
            await message.reply("No messages to delete.")
    else:
        # In group chat, check if the bot is an admin
        try:
            bot_member = await client.get_chat_member(chat_id, 'me')
            is_admin = bot_member.status in ["administrator", "creator"]
        except ValueError:
            is_admin = False

        if is_admin:
            # Bot is admin, delete all specified messages
            message_ids = [msg.message_id for msg in messages_to_delete]
            await client.delete_messages(chat_id, message_ids)
            await message.reply(f"Deleted {len(message_ids)} messages.")
        else:
            # Bot is not admin, delete only its own messages
            own_message_ids = [msg.message_id for msg in messages_to_delete if msg.from_user.id == user_id]
            if own_message_ids:
                await client.delete_messages(chat_id, own_message_ids)
                await message.reply(f"Deleted {len(own_message_ids)} of my own messages.")
            else:
                await message.reply("No messages to delete.")