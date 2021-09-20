import telebot

bot = telebot.TeleBot("1960307734:AAEdFALBTV93kkVKpzquzf273ineNfU_0jo")

import mysql.connector

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 passwd="",
 database="restaurant_system"
)

def getAllFoodTypes():
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT * FROM food_types"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

def getAllRestaurants():
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT * FROM restaurants"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result

def getFoodsByRestaurantId(id):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.food_type_id, ft.name as foodType, r.name as restaurantName " \
    "FROM foods f " \
    "LEFT OUTER JOIN food_types ft ON ft.id = f.food_type_id " \
    "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
    "WHERE f.restaurant_id = "+str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result


def getFoodByFoodType(id):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.foodtype_id, ft.name as foodType, r.name as restaurantName " \
          "FROM foods f " \
          "LEFT OUTER JOIN food_types ft ON ft.id = f.foodtype_id " \
          "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
          "WHERE f.foodtype_id = " + str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result

def getFood(id):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.foodtype_id, ft.name as foodType, r.name as restaurantName " \
    "FROM foods f " \
    "LEFT OUTER JOIN food_types ft ON ft.id = f.foodtype_id " \
    "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
    "WHERE f.id = "+str(id)

    mycursor.execute(sql)
    result = mycursor.fetchone()

    return result


menu = "main"


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global menu

    if message.text.lower() == "/start":
        text = ""
        text = text + "*************************\n"
        text = text + "Добро пожаловать в сервис заказа еды\n"
        text = text + "*************************\n"
        text = text + "Выберите опцию поиска: \n"
        text = text + "1 - Поиск по типу еды\n"
        text = text + "2 - Поиск по ресторану\n"

        bot.send_message(message.chat.id, text)
        menu = "main"

    else:

        if menu == "main":
            if message.text.lower() == "1":
                allFoodTypes = getAllFoodTypes()
                text = "*************************\n"
                for food in allFoodTypes:
                    text = text + str(food[0]) + ") " + food[1] + "\n"
                menu = "choose_by_food_type"
                bot.send_message(message.chat.id, text)

            elif message.text.lower() == "2":
                allRestaurants = getAllRestaurants()
                text = "*************************\n"
                for rest in allRestaurants:
                    text = text + str(rest[0]) + ") " + rest[1] + "\n"
                menu = "choose_by_restaurant"
                bot.send_message(message.chat.id, text)

        elif menu == "choose_by_food_type":

            menu = "choose_food"
            id = message.text.lower()
            foods = getFoodByFoodType(id)
            text = "*************************\n"
            for food in foods:
                text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + food[7] + "\n"

            bot.send_message(message.chat.id, text)

        elif menu == "choose_by_restaurant":

            menu = "choose_food"

            id = message.text.lower()
            foods = getFoodsByRestaurantId(id)
            text = "*************************\n"
            for food in foods:
                text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + food[6] + "\n"

            bot.send_message(message.chat.id, text)

        elif menu == "choose_food":

            id = message.text.lower()
            food = getFood(id)

            text = "Вы заказали " + food[1] + " за " + str(food[2]) + " KZT\n"
            text = text + "Состав: [" + food[3] + "] \n"
            text = text + "К оплате: " + str(food[2]) + " KZT\n"
            text = text + "Спасибо за покупку\n"
            bot.send_message(message.chat.id, text)

bot.polling(none_stop=True, interval=0)
