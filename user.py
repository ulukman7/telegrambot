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
def handle_photo(message):

  file_id = message.photo[-1].file_id
  img_id = str(uuid.uuid4())

  file_info = bot.get_file(file_id)
  downloaded_file = bot.download_file(file_info.file_path)
  img = Image.open(BytesIO(downloaded_file))


  try:
    decoded_objs = decode(img)
    for obj in decoded_objs:
      print(obj.data.decode('utf-8'))
      if "tax.salyk.kg/tax-web-control/client/api/v1/" in obj.data.decode('utf-8'):

        save_receipt(img_id, file_id, message.chat.id)

        bot.send_message(message.chat.id, "✅ чек получено")
        return

  except:
    bot.send_message(message.chat.id, "❌ чек отклонено")

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
