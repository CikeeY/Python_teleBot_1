import json
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup as BS


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

bot = telebot.TeleBot('6086228035:AAFDeqPzXntsvxNbTf0O3Kflu_sO7gsaXp0')
#bot = telebot.TeleBot('6425255039:AAFDI3b_merGpbBJK041gHWpBD1CT30WiA0')

urlWeb = 'https://habrahabr.ru'
urlUSD = 'https://www.banki.ru/products/currency/usd/'
urlMTSS = 'https://www.dohod.ru/ik/analytics/dividend/mtss'
urlSBER = 'https://www.dohod.ru/ik/analytics/dividend/sber'
urlGAZP = 'https://www.dohod.ru/ik/analytics/dividend/gazp'


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("☁️ Погода")
    button2 = types.KeyboardButton("💼 Рынок")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, text="Здравствуй, {0.first_name}!\nКонтакт моего разработчика:\nhttps://t.me/Pussyeater_228".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    
    if(message.text == "☁️ Погода"):
        res = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid=9054e8c15a48f4a3b751f6e2b88fc907&units=metric')
        data = json.loads(res.text)
        if data["weather"][0]["main"] == 'Clouds':
            sign = '☁️'
        elif data["weather"][0]["main"] == 'Rain':
            sign = '🌧'
        elif data["weather"][0]["main"] == 'Clear':
            sign = '☀️'

        bot.send_message(message.chat.id, f'Москва:\n{data["main"]["temp"]}°\n{sign} {data["weather"][0]["main"]}')
    
    elif message.text == "💼 Рынок":
        try:
            page1 = requests.get(urlUSD, headers=headers)
            soup = BS(page1.text, 'lxml')
            cours = soup.find("div", {"class" : "Text__sc-j452t5-0 bCCQWi"}).text
            bot.send_message(message.chat.id, f'Курс доллара: {cours}')
            
            page1 = requests.get(urlMTSS, headers=headers)
            soup = BS(page1.text, 'lxml')
            cours = soup.find("td", {"class" : "greendark"}).text
            bot.send_message(message.chat.id, f'Дивиденды МТС: {cours}')
            
            page1 = requests.get(urlSBER, headers=headers)
            soup = BS(page1.text, 'lxml')
            cours = soup.find("td", {"class" : "greendark"}).text
            bot.send_message(message.chat.id, f'Дивиденды Сбер: {cours}')
            
            page1 = requests.get(urlGAZP, headers=headers)
            soup = BS(page1.text, 'lxml')
            cours = soup.find("td", {"class" : "greendark"}).text
            bot.send_message(message.chat.id, f'Дивиденды Газпром: {cours}')
        except Exception as err:
            print(err)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

bot.polling(none_stop=True)