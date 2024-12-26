import os
from flask import Flask, request
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = context.bot.username  # Get the bot's username
    message = update.message

    # Check if the message contains the bot's username or if it's a reply to the bot's previous message
    if bot_username in message.text or (message.reply_to_message and message.reply_to_message.from_user.username == bot_username):
        # Extract the message text
        user_message = message.text
        reply_message = message.reply_to_message.text if message.reply_to_message else ""

        # Prepare input for the GPT model
        full_context = f"Önceki mesaj : {reply_message}\nSonraki mesaj: {user_message}"

        # Generate response using GPT
        response = gpt(full_context)

        # Send the bot's response
        await message.reply_text(response)

def gpt(message: str):
    client = OpenAI()
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Do not format your answers using markdown. Just give plain text. Türkçe olarak cevap ver.",
                },
                {
                    "type": "text",
                    "text": f"{message}",
                },
            ],
        }],
    )
    return response.choices[0].message.content

# Telegram bot setup
token = os.environ.get('TOKEN')
application = Application.builder().token(token).build()
application.add_handler(MessageHandler(filters.ALL, callback))
application.run_polling(allowed_updates=Update.ALL_TYPES)

app = Flask(__name__)
app.run(host="0.0.0.0", port=8080)