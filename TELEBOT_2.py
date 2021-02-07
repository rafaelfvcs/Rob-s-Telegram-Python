# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:57:05 2021

@author: rafaelfvcs

Canal YouTube - Analistas Quant - https://bit.ly/CanalYouTube-Analistas-Quant

CURSO COMPLETO ROBÔ TELEGRAM UDEMY - 

https://www.udemy.com/course/como-criar-robos-no-telegram-com-python/?referralCode=3DD249FE96053E98CE8F 

"""

import telebot
import ast
import time
from telebot import types
import requests 

TOKEN ='2590109764:AAGpNDyZ14nBsiD7hRFF1rFZcM4bGSxFXic'

bot = telebot.TeleBot(TOKEN)

stringList = {"Chave1": "Valor1", "Cahve2": "Valor2", "Chave3": "Valor3","Chave4":"Valor4"}


def makeKeyboard(cep_n):
    markup = types.InlineKeyboardMarkup()
    print("Passou - "+cep_n)
    
    if len(cep_n) == 8:
        print("vai coletar cep")
        url_base = f'https://viacep.com.br/ws/{cep_n}/json/'
        r = requests.get(url_base).json()
        
    for key, value in stringList.items():
        if value != "": 
            markup.add(types.InlineKeyboardButton(text=value,
                                                  callback_data="['value', '" + value + "', '" + key + "']"))

    return markup



@bot.message_handler(commands=['cep'])
def handle_command_adminwindow(message):
    msg = message.text
    cep_n = msg.split(" ")[1]
       
    bot.send_message(chat_id=message.chat.id,
                     text="Aqui estão as informações para seu CEP:",
                     reply_markup=makeKeyboard(cep_n),
                     parse_mode='HTML')
    return cep_n
    
   
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    
    if (call.data.startswith("['value'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="Este valor de " + valueFromCallBack + " representa o " + keyFromCallBack)
    
    
    
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)
