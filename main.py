from pyrogram import Client, filters
from config import API_ID, API_HASH
app = Client("my_account", api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrogram!")


if __name__ == '__main__':
    app.run()


