# import telegram
# import requests
# import logging
# import json
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
# from telegram import InlineQueryResultArticle , ParseMode , InputTextMessageContent
# from telegram.utils.helpers import escape_markdown
# from urllib.request import urlopen
# from uuid import uuid4
# import urllib.request
# import sys
#
#
# # Get your private API key here: https://aqicn.org/api/
# # Use the token as command arg in terminal, Example: python3 AQIbot.py botToken APIToken
#
# botToken = sys.argv[1]
# APIToken = sys.argv[2]
#
#
# bot = telegram.Bot(token=botToken)
#
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# 					level=logging.INFO)
#
# logger = logging.getLogger(__name__)
#
#
# pagein = {}
# def start(update, context):
# 	pagein[update.Message.Chat.ID] = 0
# 	update.message.reply_text("Hello, for getting the Air Quality Index of your city, just send me the city's name, for more info press /info, to get started press /help")
#
#
# def help(update, context):
# 	update.message.reply_text("For getting the AQI of your city just type its name, for learning more about AQI number range and its meanings press /aqiranges, for getting a list of all regions in your city, press /regions, for further info visit: \n https://github.com/SinaQane/AQI-bot")
#
#
# def info(update, context):
# 	update.message.reply_text("The AQI is an index for reporting daily air quality. It tells you how clean or polluted your air is, and what associated health effects might be a concern for you. The AQI focuses on health effects you may experience within a few hours or days after breathing polluted air. By knowing it, we can prevent likely harms to our health, reduce usage of personal vehicles and work together to make our city a healthier place.")
#
#
# def aqiranges(update, context):
# 	update.message.reply_text('Every category corresponds to a different level of health concern. The six levels of health concern and what they mean are: \n \n' + 'Good: AQI is 0 to 50. Air quality is considered satisfactory, and air pollution poses little or no risk. \n \n' + 'Moderate: AQI is 51 to 100. Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people. For example, people who are unusually sensitive to ozone may experience respiratory symptoms. \n \n' + 'Unhealthy for Sensitive Groups: AQI is 101 to 150. Although general public is not likely to be affected at this AQI range, people with lung disease, older adults and children are at a greater risk from exposure to ozone, whereas persons with heart and lung disease, older adults and children are at greater risk from the presence of particles in the air. \n \n' + 'Unhealthy: AQI is 151 to 200. Everyone may begin to experience some adverse health effects, and members of the sensitive groups may experience more serious effects. \n \n' + 'Very Unhealthy: AQI is 201 to 300. This would trigger a health alert signifying that everyone may experience more serious health effects. \n \n' + 'Hazardous: AQI greater than 300. This would trigger a health warnings of emergency conditions. The entire population is more likely to be affected.')
#
#
# def aqilevelcheck (aqinumber):
# 	if aqinumber in range (0,51):
# 		return ("Good")
# 	elif aqinumber in range (51,101):
# 		return ("Moderate")
# 	elif aqinumber in range (101,151):
# 		return ("Unhealthy for sensitive groups")
# 	elif aqinumber in range (151,201):
# 		return ("Unhealthy")
# 	elif aqinumber in range (201,301):
# 		return ("Very Unhealthy")
# 	elif aqinumber in range (301,501):
# 		return ("Hazardous")
# 	else:
# 		return ("Out of range")
#
#
# def airnowcity (city):
# 	request = requests.get('https://api.waqi.info/feed/'+city+'/?token='+APIToken)
# 	reqdictype = json.loads(request.text)
# 	datatag = reqdictype.get('data')
# 	aqicity = datatag.get('aqi')
# 	return (aqicity)
#
#
# def airnowregions (city):
# 	request = requests.get('https://api.waqi.info/search/?token='+APIToken+'&keyword='+city)
# 	res = json.loads(request.text)
# 	resdic = res.get('data')
# 	stations =[]
#
# 	for i in range (0,len(resdic)):
# 		stations.append (resdic[i].get('station'))
# 		if resdic[i].get('aqi') == '-':
# 			stations.append ("No Data Available")
# 		else:
# 			stations.append (resdic[i].get('aqi'))
#
# 	stations2=[]
# 	for i in range (0 , len(stations),2):
# 		stations2.append (stations[i].get('name'))
# 		stations2.append (stations[i+1])
#
# 	finalstr = ""
# 	for i in range (0 , len(stations),2):
# 		finalstr = finalstr + stations2[i] +" :" + stations2[i+1] +"\n"
# 	return("For" + city + "regions, we have results below: \n" + finalstr)
#
#
# def regions(update, context):
# 	ChatID = update.Message.Chat.ID
# 	pagein[ChatID] = 1
# 	update.message.reply_text("Enter a city to get its regions' AQI in a list.")
#
#
# def aircheck (update, context):
# 	ChatID = update.Message.Chat.ID
# 	global cityforcheck
# 	global aqinow
# 	global airlevelnow
#
# 	if pagein[ChatID] == 0:
# 		cityforcheck = update.message.text
# 		aqinow = airnowcity (cityforcheck)
# 		airlevelnow = aqilevelcheck(aqinow)
# 		message = cityforcheck + " Air Quality Index is " + str(aqinow) + " And It's " + airlevelnow + "."
# 		img = open("img" + airlevelnow + ".JPG","rb")
# 		update.message.reply_photo(photo=img,caption=message)
#
# 	elif pagein[ChatID] == 1:
# 		cityforcheck = update.message.text
# 		regionslist = airnowregions(cityforcheck)
# 		update.message.reply_text(regionslist)
# 	pagein[ChatID] = 0
#
#
# def inlinequery(update, context):
# 	global cityforcheck
# 	global aqinow
# 	global airlevelnow
# 	query = update.inline_query.query
# 	aircheck (query)
# 	des = cityforcheck + " air quality index is " + str(aqinow)
# 	airlevelinlink = airlevelnow.replace(" ", "%20")
# 	results =[ InlineQueryResultArticle(
# 		id=uuid4(),
# 		title=cityforcheck,
# 		description=des,
# 		input_message_content=InputTextMessageContent(
# 			message_text = cityforcheck + " air quality index is " + str(aqinow) + " And it's " + airlevelnow + "."))
# 			]
#
#
# 	update.inline_query.answer(results)
#
#
# def error(update, context):
# 	logger.warning('Update "%s" caused error "%s"', update, context.error)
#
#
# def main():
#
# 	updater = Updater(botToken, use_context=True)
#
# 	dp = updater.dispatcher
#
# 	dp.add_handler(CommandHandler("start", start))
# 	dp.add_handler(CommandHandler("help", help))
# 	dp.add_handler(CommandHandler("info", info))
# 	dp.add_handler(CommandHandler("aqiranges", aqiranges))
# 	dp.add_handler(CommandHandler("regions", regions))
# 	dp.add_handler(MessageHandler(Filters.text, aircheck))
# 	dp.add_handler(InlineQueryHandler(inlinequery))
#
# 	dp.add_error_handler(error)
#
# 	updater.start_polling()
#
# 	updater.idle()
#
# if __name__ == '__main__':
# 	main()




import telegram
import requests
import logging
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle , ParseMode , InputTextMessageContent
from telegram.utils.helpers import escape_markdown
from urllib.request import urlopen
from uuid import uuid4
import urllib.request
import sys

# Get your private API key here: https://aqicn.org/api/
# Use the token as command arg in terminal, Example: python3 AQIbot.py botToken siteToken

botToken = sys.argv[1]
APIToken = sys.argv[2]

bot = telegram.Bot(token=botToken)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
	update.message.reply_text("Hello, for getting the Air Quality Index of your city, just send me the city's name, for more info press /help")

def help(update, context):
	update.message.reply_text("The AQI is an index for reporting daily air quality. It tells you how clean or polluted your air is, and what associated health effects might be a concern for you. The AQI focuses on health effects you may experience within a few hours or days after breathing polluted air. EPA calculates the AQI for five major air pollutants regulated by the Clean Air Act: ground-level ozone, particle pollution (also known as particulate matter), carbon monoxide, sulfur dioxide, and nitrogen dioxide. For each of these pollutants, EPA has established national air quality standards to protect public health .Ground-level ozone and airborne particles are the two pollutants that pose the greatest threat to human health in this country.")

def aqiranges(update, context):
	update.message.reply_text('Every category corresponds to a different level of health concern. The six levels of health concern and what they mean are: \n' + 'Good: AQI is 0 to 50. Air quality is considered satisfactory, and air pollution poses little or no risk. \n' + 'Moderate: AQI is 51 to 100. Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people. For example, people who are unusually sensitive to ozone may experience respiratory symptoms. \n' + 'Unhealthy for Sensitive Groups: AQI is 101 to 150. Although general public is not likely to be affected at this AQI range, people with lung disease, older adults and children are at a greater risk from exposure to ozone, whereas persons with heart and lung disease, older adults and children are at greater risk from the presence of particles in the air. \n' + 'Unhealthy: AQI is 151 to 200. Everyone may begin to experience some adverse health effects, and members of the sensitive groups may experience more serious effects. \n' + 'Very Unhealthy: AQI is 201 to 300. This would trigger a health alert signifying that everyone may experience more serious health effects. \n' + 'Hazardous: AQI greater than 300. This would trigger a health warnings of emergency conditions. The entire population is more likely to be affected.')

def aqilevelcheck (aqinumber):
	if aqinumber in range (0,51):
		return ("Good")
	elif aqinumber in range (51,101):
		return ("Moderate")
	elif aqinumber in range (101,151):
		return ("Unhealthy for sensitive groups")
	elif aqinumber in range (151,201):
		return ("Unhealthy")
	elif aqinumber in range (201,301):
		return ("Very Unhealthy")
	elif aqinumber in range (301,501):
		return ("Hazardous")
	else:
		return ("There seems to be an error or the Air Quality Index is out of our range.")

def airnowcity (city):
	request = requests.get('https://api.waqi.info/feed/'+city+'/?token='+APIToken)
	reqdictype = json.loads(request.text)
	datatag = reqdictype.get('data')
	aqicity = datatag.get('aqi')
	return (aqicity)

def airnowregions (city):
	request = requests.get('https://api.waqi.info/search/?token='+APIToken+'&keyword='+city)
	res = json.loads(request.text)
	resdic = res.get('data')
	stations =[]
	for i in range (0,len(resdic)):
    		stations.append (resdic[i].get('station'))
    		if resdic[i].get('aqi') == '-':
        		stations.append ("No Data Available")
    		else:
       			stations.append (resdic[i].get('aqi'))

	stations2=[]
	for i in range (0 , len(stations),2):
    		stations2.append (stations[i].get('name'))
    		stations2.append (stations[i+1])

	finalstr = ""
	for i in range (0 , len(stations),2):
    		finalstr = finalstr + stations2[i] +" :" + stations2[i+1] +"\n"
	return("For" + city + "regions, we have results below: \n" + finalstr)

def aircheck (update, context):
	cityforcheck = update.message.text
	aqinow = airnowcity (cityforcheck)
	airlevelnow = aqilevelcheck(aqinow)
	message = cityforcheck + " Air Quality Index is " + str(aqinow) + " And It's " + airlevelnow
	img = open("img/" + airlevelnow + ".JPG","rb")
	update.message.reply_photo(photo=img,caption=message)
	stations = airnowregions(cityforcheck)
	print(stations)

def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def inlinequery(update, context):
	query = update.inline_query.query
	aqinow = airnowcity(query)
	airlevelnow = aqilevelcheck(aqinow)
	print(query)
	results =[
		InlineQueryResultArticle(
			id=uuid4(),
			title=query,
			description=airlevelnow,
			input_message_content=InputTextMessageContent(
				message_text= "Air quality index of " + query + " is " + str(aqinow) + " and It's " + airlevelnow))
			]

	update.inline_query.answer(results)


def main():

	updater = Updater(botToken, use_context=True)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("aqiranges", aqiranges))
	dp.add_handler(MessageHandler(Filters.text, aircheck))
	dp.add_handler(InlineQueryHandler(inlinequery))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()

if __name__ == '__main__':
	main()
