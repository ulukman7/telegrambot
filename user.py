import json

import cv2
import pytesseract
import numpy as np
import requests
import telebot
from telebot import types
import sqlite3
import re
import uuid
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
bot = telebot.TeleBot("6339660614:AAHOAnVWlNrIs8JLSn8cGc_TAzRMCAKMju4")

cheks_button = types.InlineKeyboardButton(text="Cheklarim", callback_data="get_cheks")
keyboard = types.InlineKeyboardMarkup()
keyboard.add(cheks_button)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ваше Имя:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_name = message.text
    bot.send_message(message.chat.id, "Ваше Фамилия:")
    bot.register_next_step_handler(message, get_lastname, user_name)

def get_lastname(message, user_name):
  user_lastname = message.text

  bot.send_message(message.chat.id, "Ваш номер телефона в международном формате (+996*********):")
  bot.register_next_step_handler(message, get_phone, user_name, user_lastname)

def get_phone(message, user_name, user_lastname):
  user_phone = message.text
  if not re.match("\+\d{3}\d{8}", user_phone):
    bot.send_message(message.chat.id, "Номер не в международном формате")
    return
  # Ma'lumotlarni saqlash
  add_user(user_name, user_lastname, user_phone, message.chat.id)
  bot.send_message(message.chat.id, "✅ Вы успешно зарегистрированы!")
  bot.send_message(message.chat.id, "📃 Отправьте фото чека")
def add_user(name, lastname, phone, chat_id):

  conn = sqlite3.connect('database.db')
  c = conn.cursor()

  # Foydalanuvchi mavjudligini tekshirish
  c.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
  data = c.fetchone()
  if data is None:
    # Foydalanuvchi yo'q, qo'shamiz
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                phone TEXT)''')
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
              (name, lastname, phone, chat_id))
  else:
    # Foydalanuvchi bor, xabardor qilamiz
    bot.send_message(chat_id, "Вы уже зарегистрированы")

  conn.commit()
  conn.close()

# @bot.message_handler(content_types=['photo'])
# def handle_photo(message):
#   file_id = message.photo[-1].file_id
#   img_id = str(uuid.uuid4())
#   save_receipt(img_id, file_id, message.chat.id)
#
#   bot.send_message(message.chat.id, "✅ Чек успешно получен!")
@bot.message_handler(content_types=['photo'])
def handle_receipt(message):

  file_id = message.photo[-1].file_id
  file_path = bot.get_file(file_id).file_path
  # Rasmni yuklab olamiz
  file_bytes = bot.download_file(file_path)
  # Rasmdagi matnni o'qish
  receipt_text = read_receipt(file_bytes)

  # Kerakli qiymatlarni ajratib olamiz
  # date = parse_receipt(receipt_text)
  print(receipt_text)
  # Tekshiradi
  # if valid_date(date) and valid_total(total):
  #    bot.send_message(message.chat.id, "Чек принят!")
  #    save_to_db(message.chat.id, date, total)
  # else:
  #    bot.send_message(message.chat.id, "Неверные данные чека")


def read_receipt(file_bytes):
  url = "https://ocr.asprise.com/api/v1/receipt"
  image = file_bytes

  api_key = "TEST"

  response = requests.post(url,
                           data={"api_key": api_key},
                           files={"file": open(image, "rb")})

  data = json.loads(response.text)
  print(data)
  receipt = data["receipts"][0]

  print("Chek ma'lumotlari:")
  print("- Sana:", receipt["date"])
  print("- Vaqt:", receipt["time"])
  print("- Xaridlar soni:", len(receipt["items"]))

  total_amount = 0
  for item in receipt["items"]:
      print(f"- {item['description']} - {item['amount']}")
      total_amount += float(item["amount"])

  print(f"Jami summa: {total_amount}")
# def parse_receipt(text):
#
#   # Sana uchun regex
#   date_regex = r"(\d{2}\.\d{2}\.\d{4})"
#   date = re.search(date_regex, text).group(1)
#
#   # Jami uchun regex
#   total_regex = r"Итого\s+(\d+\s+\S+)"
#   total = re.search(total_regex, text).group(1)
#
#   return date, total


def save_receipt(img_id, file_id, chat_id):

  conn = sqlite3.connect('database.db')

  conn.execute('''CREATE TABLE IF NOT EXISTS receipts
             (id text, file_id text, chat_id text)''')

  conn.execute("INSERT INTO receipts VALUES (?, ?, ?)",
            (img_id, file_id, chat_id))

  conn.commit()
  conn.close()
def get_user_cheks(chat_id):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT * FROM receipts WHERE chat_id=?", (chat_id,))
  cheks = c.fetchall()

  return cheks

@bot.message_handler(commands=['chek'])
def get_cheks(msg):

  chat_id = msg.chat.id
  cheks = get_user_cheks(chat_id)

  for chek in cheks:
    file_id = chek[1]
    bot.send_photo(chat_id, file_id)


bot.polling()
