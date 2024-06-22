from pyrogram import Client, filters
from config import API_ID, API_HASH
from modules import misc
app = Client("my_account", api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.command(["help"]), filters.me)
async def my_handler(client, message):
    await message.edit("Pyrogram")


if __name__ == '__main__':
    app.run()


