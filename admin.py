
import sqlite3
import random
import re
from datetime import datetime
from telebot import TeleBot
from telebot import  types
bot = TeleBot("6582575861:AAHK19MQ8_PIkZjLIETzBizj3i0QS36eT7Q")


@bot.message_handler(commands=['start'])
def start(message):
    list_btn = types.KeyboardButton("/list_products")
    auction_product_btn = types.KeyboardButton("/selected_auction_product")
    create_btn = types.KeyboardButton("/create_auction")
    add_product_btn = types.KeyboardButton("/add_product")
    delete_btn = types.KeyboardButton("/delete_product")
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(list_btn, auction_product_btn, create_btn,add_product_btn,delete_btn)
    bot.send_message(message.chat.id, "Здравствуйте!", reply_markup=buttons)



# Mahsulot qo'shish
@bot.message_handler(commands=['add_product'])
def add_product(message):
   # Mahsulot qo'shish funktsiyasi
    bot.send_message(message.chat.id, "Enter product name:")
    bot.register_next_step_handler(message, add_product_name)



def add_product_name(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  name = message.text

  cursor.execute("INSERT INTO products VALUES (?, ?)", (None, name))

  data = cursor.fetchone()

  if data is None:
    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT);""")
    cursor.execute("INSERT INTO products (name) VALUES (?)", (name,))
    bot.send_message(message.chat.id, "🎉 Товар успешно добавлен!")
  conn.commit()
  conn.close()

@bot.message_handler(commands=['/delete_product'])
def dlt_product(message):
   # Mahsulot qo'shish funktsiyasi
    bot.send_message(message.chat.id, "Enter product name:")
    bot.register_next_step_handler(message, delete_product_by_id)
def delete_product_by_id(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS auction_products (
    id INTEGER PRIMARY KEY,
    name TEXT
  )
""")
  product_id = message.text

  cursor.execute("DELETE FROM products WHERE name=?", (product_id,))
  conn.commit()
  conn.close()
  bot.send_message(message.chat.id, "Product deleted successfully")

# Mahsulotlar ro'yxati
@bot.message_handler(commands=['select_auction_product'])
def get_products(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auction_products")
    products = cursor.fetchall()

    if len(products) == 0:
        bot.send_message(message.chat.id, "There are no products yet")
        return

    text = "Registered products:\n"
    for product in products:
        text += f"{product[0]}. {product[1]}\n"

    bot.send_message(message.chat.id, text)
    conn.commit()
    conn.close()

# Auktsion uchun mahsulot tanlash
@bot.message_handler(commands=['list_products'])
def select_auction_product(message):
    # Avval mahsulotlar ro'yxatini ko'rsatamiz

    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
  CREATE TABLE IF NOT EXISTS auction_products (
    id INTEGER PRIMARY KEY,
    product_id INTEGER
  )
""")
    cursor.execute("SELECT * FROM products")
    product_list = cursor.fetchall()
    auction_names = ["%s. %s" % (a[0], a[1]) for a in product_list]
    auctions_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    auctions_keyboard.add(*auction_names)

    bot.send_message(message.chat.id, "Choose auction:", reply_markup=auctions_keyboard)
selected_product = None
@bot.message_handler(regexp='(\d+).')
def add_delete_product(message):
  global selected_product
  selected_product = message
  product_id = message.text.split('.')[0]
# Knopkalar
  add_btn = types.KeyboardButton("/add_auction")
  delete_btn = types.KeyboardButton("/dlt_product_of_auc")
  dltprod_btn = types.KeyboardButton("/delete_product")
  back = types.KeyboardButton("/start")

    # Knopkalar paneli
  buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
  buttons.add(add_btn, delete_btn,dltprod_btn,back)

    # Knopkalarni jo'natish
  bot.send_message(message.chat.id, "выбирай", reply_markup=buttons)

# Mahsulotni auktsionga qo'shish
@bot.message_handler(commands=["add_auction"])
def add_product_to_auction(message):
  product_id = selected_product.text.split('.')[1].strip()
  print(product_id)
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS auction_products (
    id INTEGER PRIMARY KEY,
    product_id
  )
""")
  cursor.execute("SELECT * FROM products WHERE name=?", (product_id,))
  product = cursor.fetchone()

  if product:
    cursor.execute("INSERT INTO auction_products (product_id) VALUES (?)", (product_id,))
    conn.commit()
    bot.reply_to(message, "Товар успешно добавлен")
  else:
    bot.reply_to(message, "Такой товар не найден")

  conn.close()

# Mahsulotni auktsiondan olib tashlash
@bot.message_handler(commands=['dlt_product_of_auc'])
def delete_product_from_auction(message):
  product_id = selected_product.text.split('.')[1].strip()

  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()

  cursor.execute("DELETE FROM auction_products WHERE product_id=?", (product_id,))
  conn.commit()

  bot.reply_to(message, "Продукт успешно удален")

  conn.close()

# акция
@bot.message_handler(commands=['create_auction'])
def create_auction(message):
    bot.send_message(message.chat.id, "Enter auction name:")
    bot.register_next_step_handler(message, auction_name_step)

def auction_name_step(message):
    name = message.text
    # Оставшиеся шаги...
    bot.send_message(message.chat.id, "Enter start date (DD.MM.YYYY):")
    bot.register_next_step_handler(message, auction_start_date_step, name)

def auction_start_date_step(message, name):
    start_date = message.text
    #...
    bot.send_message(message.chat.id, "Enter end date (DD.MM.YYYY):")
    bot.register_next_step_handler(message, auction_end_date_step, name, start_date)

def auction_end_date_step(message, name, start_date):
   end_date = message.text
   #...
   bot.send_message(message.chat.id, "Enter minimum amount:")
   bot.register_next_step_handler(message, auction_min_amount_step, name, start_date, end_date)

def auction_min_amount_step(message, name, start_date, end_date):

    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS auctions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    start_date TEXT,
    end_date TEXT,
    min_amount INTEGER
);
""")
    min_amount = message.text

# Мы сохраняем данные аукциона
    cursor.execute("INSERT INTO auctions VALUES (?, ?, ?, ?, ?)",
                   (None, name, start_date, end_date, min_amount))

    bot.send_message(message.chat.id, "Auction created successfully!")

    conn.commit()
    conn.close()
# Список участников
@bot.message_handler(commands=['auction_participants'])
def auction_participants(message):
# Сначала показываем список аукционов
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    receipt_id INTEGER,
    auction_id INTEGER
);
""")
    cursor.execute("SELECT * FROM auctions")
    auctions = cursor.fetchall()

    auction_names = ["%s. %s" % (a[0], a[1]) for a in auctions]
    auctions_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    auctions_keyboard.add(*auction_names)

    bot.send_message(message.chat.id, "Choose auction:", reply_markup=auctions_keyboard)

    # bot.register_next_step_handler(message, show_participants)

# def show_participants(message, auction_id):
#
#   # выборка участников по аукциону
#   cursor.execute("SELECT * FROM participants WHERE auction_id=?", (auction_id,))
#
#   # вывод данных
#   for participant in cursor.fetchall():
#     bot.send_message(chat_id, f"{participant[1]} {participant[2]} {participant[3]}")
#
# def select_winner(auction_id):
#
#   # получение списка участников
#   participants = get_participants(auction_id)
#
#   # рандомный выбор
#   winner = random.choice(participants)
#
#   # отправка сообщения
#   bot.send_message(chat_id, f"Победитель: {winner['name']} {winner['phone']}")

# G'olibni tanlash
# @bot.message_handler(commands=['select_winner'])
# def select_winner(auction_id):
#   winner_index = random.randint(0, len(participants)-1)
#   winner = participants[winner_index]
#   bot.send_message(chat_id, f"Winner: {winner.name} ({winner.phone})")
bot.polling()

