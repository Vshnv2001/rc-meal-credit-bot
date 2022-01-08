import os
import telebot
from replit import db
from credits import return_message

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, "Hello, this is the Meal Credit Bot :)\nUse /help to see the full list of commands")

@bot.message_handler(commands=['breakfast'])
def input_bf(message):
	credit_value = message.text
	value = credit_value.replace("/breakfast", "") 
	if value.strip().isnumeric():
		return_value = return_message(True, int(value))
		bot.send_message(message.chat.id, return_value)
	else:
		bot.send_message(message.chat.id, "Please input an integer without any symbols!")


@bot.message_handler(commands=['dinner'])
def input_din(message):
	credit_value = message.text
	value = credit_value.replace("/dinner", "")
	if value.strip().isnumeric():
		return_value = return_message(False, int(value))
		bot.send_message(message.chat.id, return_value)
	else:
		bot.send_message(message.chat.id, "Please input an integer without any symbols!")

@bot.message_handler(commands=['sell'])
def sell(message):
	text_value = message.text
	selling_price = text_value.replace("/sell", "")
	try:
		selling_price = float(selling_price)
		username = message.from_user.username
		duplicate = False
		for key in db.keys():
			if key == username:
				duplicate = True
				db[f"{username}"] = selling_price
				break
		if not duplicate:
			db[f"{username}"] = selling_price
		bot.send_message(message.chat.id, "Alright, now your username will appear to interested buyers!")
	except:
		bot.send_message(message.chat.id, "Please only input numbers without any symbols!")

@bot.message_handler(commands=['buy']) 
def buy(message):
	text_value = message.text
	string_value = text_value.replace("/buy", "") 
	try:
		buying_price = float(string_value)
		lst = []
		for key in db.keys():
			selling_price = db[f"{key}"]
			if float(selling_price) <= buying_price:
				lst.append([key, selling_price])
		print(lst)
		if len(lst) == 0:
			bot.send_message(message.chat.id, "Sorry, there are no users that have selling price lower than or equal to your bid")
		else:
			bot.send_message(message.chat.id, f"Alright, these are the possible sellers")
			for value in lst:
				bot.send_message(message.chat.id, f"seller's username: {value[0]}, price: {value[1]}")
	except:
		bot.send_message(message.chat.id, "Please input only numbers without any symbols!")

@bot.message_handler(commands=['delete'])
def delete(message):
	username = message.from_user.username
	try:
		del db[f"{username}"]
		bot.send_message(message.chat.id, "Your username is deleted from our database!\n use /sell to start selling again")
	except: 
		bot.send_message(message.chat.id, "Your username is deleted from our database!\n use /sell to start selling again")

@bot.message_handler(commands=['help'])
def help(message):
	breakfast = "/breakfast [input your remaining credits] (to check your usage of credits)\n"
	dinner = "\n/dinner [your remaining credits] (check your usage of credits)\n"
	sell = "\n/sell [selling price (do not enter any $ symbol)] (to sell your credits, and by using this command, you consent to giving your telegram username to potential buyers)\n"
	sell_note = "(To change sell price, just type /sell [your new price])\n"
	buy = "\n/buy [lowest price you are willing to buy at] (shows you any buyers with selling price lower than your buying price, if any\n"
	delete = "\n/delete (to retract your sell request)"
	bot.send_message(message.chat.id, breakfast + dinner + sell + sell_note + buy + delete)


bot.polling()