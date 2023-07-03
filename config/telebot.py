import telebot
from telebot import types

TOKEN = '6012488137:AAGCe_QaKWw_1qYNqwbhKLV5z96GfgjIuXI'

categories = {
    'Мужская одежда': [
        {'item': 'Футболка', 'price': 10, 'colors': ['черный', 'белый', 'синий'], 'sizes': ['S', 'M', 'L']},
        {'item': 'Рубашка', 'price': 20, 'colors': ['синий', 'красный'], 'sizes': ['M', 'L', 'XL']},
        {'item': 'Джинсы', 'price': 30, 'colors': ['серый', 'черный'], 'sizes': ['L', 'XL']}
    ],
    'Женская одежда': [
        {'item': 'Платье', 'price': 40, 'colors': ['красный', 'черный', 'синий'], 'sizes': ['S', 'M', 'L']},
        {'item': 'Блузка', 'price': 25, 'colors': ['белый', 'голубой'], 'sizes': ['M', 'L']},
        {'item': 'Юбка', 'price': 35, 'colors': ['синий', 'коричневый'], 'sizes': ['S', 'L']}
    ],
    'Детская одежда': [
        {'item': 'Комбинезон', 'price': 15, 'colors': ['розовый', 'голубой'], 'sizes': ['S', 'M']},
        {'item': 'Куртка', 'price': 30, 'colors': ['синий', 'красный'], 'sizes': ['M', 'L']},
        {'item': 'Штаны', 'price': 20, 'colors': ['зеленый', 'серый'], 'sizes': ['S', 'L']}
    ]
}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        markup.add(category)
    bot.send_message(message.chat.id, 'Добро пожаловать в наш магазин одежды!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in categories.keys())
def select_category(message):
    category = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in categories[category]:
        markup.add(item['item'])
    bot.send_message(message.chat.id, f'Выберите товар из категории "{category}"', reply_markup=markup)


@bot.message_handler(func=lambda message: any(
    message.text == item['item'] for item in [item for sublist in categories.values() for item in sublist]))
def select_item(message):
    item_name = message.text
    for category in categories.values():
        for item in category:
            if item['item'] == item_name:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for color in item['colors']:
                    markup.add(color)
                bot.send_message(message.chat.id, f'Выберите цвет для товара "{item_name}"', reply_markup=markup)
                bot.register_next_step_handler(message, select_color, item)
                break


def select_color(message, item):
    color = message.text
    item['selected_color'] = color

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in item['sizes']:
        markup.add(size)
    bot.send_message(message.chat.id, 'Выберите размер', reply_markup=markup)
    bot.register_next_step_handler(message, select_size, item)


def select_size(message, item):
    size = message.text
    item['selected_size'] = size

    reply = f'Вы выбрали товар:\n\nНазвание: {item["item"]}\nЦена: {item["price"]} $\nЦвет: {item["selected_color"]}\nРазмер: {item["selected_size"]}\n\n' \
            f'Спасибо за заказ! Для подтверждения отправьте /confirm'
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['confirm'])
def confirm_order(message):
    order_summary = 'Ваш заказ:\n\n'
    for category in categories.values():
        for item in category:
            if 'selected_color' in item and 'selected_size' in item:
                order_summary += f'Название: {item["item"]}\nЦена: {item["price"]} $\nЦвет: {item["selected_color"]}\n' \
                                 f'Размер: {item["selected_size"]}\n\n'
    if order_summary == 'Ваш заказ:\n\n':
        order_summary = 'Вы еще не выбрали товары для заказа.'
    bot.send_message(message.chat.id, order_summary)


bot.polling(none_stop=True, interval=0)
