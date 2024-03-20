from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests

TOKEN: final = 'BOT_TOKEN'
BOT_USERNAME: final = '@meteomaster_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to Meteo Master! \n Type /weather <city> to get the current weather of a city.')

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        city = context.args[0].strip('<>').lower()  
        weather_data = get_weather(city)
        if weather_data:
            await update.message.reply_text(weather_data)
        else:
            await update.message.reply_text('Weather data not found for the specified city or '
                                             'the city name format is incorrect.')
    except IndexError:
        await update.message.reply_text('Please provide a city name.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Welcome to Meteo Master! Here are the available commands:\n"
        "/start - Start the bot and get welcome message\n"
        "/weather <city> - Get the current weather of a city\n"
        "/help - Display this help message\n"
        "/about - About Me!"
    )
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "Meteo Master 1.0\n"
        "This bot provides current weather information for cities around the world.\n"
        f"Created by Rudransh Das\n"
        "Check out my portfolio:(https://rudransh.rf.gd)"
    )
    await update.message.reply_text(about_text)

def get_weather(city: str) -> str:
    api_key = 'API KEY'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    data = response.json()
    if response.status_code == 200:
        weather_info = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'].capitalize(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return (f"Weather in {weather_info['city']}:\n"
                f"🌡️ Temperature: {weather_info['temperature']}°C\n"
                f"🌤️ Description: {weather_info['description']}\n"
                f"💧 Humidity: {weather_info['humidity']}%\n"
                f"🌬️ Wind Speed: {weather_info['wind_speed']} m/s")
    else:
        return ''

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('weather', weather_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about_command))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
