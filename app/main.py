import telebot
import time
import requests
import sys


def avg_course(currency_data):
    return (currency_data['buy'] + currency_data['sell']) / 2

def parse_avg_courses():
    url = 'https://bank.bcs.ru/get_courses_update_pack/74'

    response = requests.get(url)
    if not response.status_code == 200:
        return {'error': response.status_code}

    data = response.json()['online_courses']
    eur = data['EUR']
    usd = data['USD']
    return {'eur': avg_course(eur), 'usd': avg_course(usd)}

BOT_TOKEN = 'token'
LEXA_TELEGRAM_ID = 365951234
bot = telebot.TeleBot(BOT_TOKEN)

def render_message():
    courses = parse_avg_courses()
    if courses['error']:
        return f"Ошибка: {courses['error']}"

    return f"Евро {courses['eur']}, доллар {courses['usd']}"

def send_message():
    try:
        message = render_message()
        bot.send_message(LEXA_TELEGRAM_ID, message)
    except Exception as e:
        bot.send_message(LEXA_TELEGRAM_ID, f"Error sending message: {e}")

def main():
    while True:
        send_message()
        time.sleep(60)

if __name__ == "__main__":
    main()
