#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import constants 
import requests
TOKEN="YOUR-BOT-TOKEN"
bot = telebot.TeleBot(TOKEN)
user_step={}

def listener(messages):
    for m in messages:
        if m.chat.id in user_step:
            replies_listener(m)
bot.set_update_listener(listener) #We tell the bot to use the listener that we have created

def replies_listener(m):
    cid=m.chat.id
    waiting=user_step[cid]
    if(waiting==constants.WAITING_LOCATION_SUNSET):
        if(m.content_type == "location"):
            latitude=m.location.latitude
            longitude=m.location.longitude
            bot.send_message( cid, "Location received: \nLatitud: "+str(latitude)+"\nLongitud: "+str(longitude)+"\nGetting data...")
            request = 'http://api.sunrise-sunset.org/json?lat='+str(latitude)+'&lng='+str(longitude)
            r = requests.get(request).json()
            if(r['status']=='OK'):
                sunset=r['results']['sunset']
                bot.send_message( cid, "Sunset time is: *"+sunset+"*\nAll times are in UTC and summer time adjustments are not included in the returned data.\n_Data from http://sunrise-sunset.org_",parse_mode='Markdown')
            else:
                bot.send_message( cid, "ERROR. Please, try again")
        else:
            bot.send_message( cid, "Location not received. Request cancelled")
        del user_step[cid]
    if(waiting==constants.WAITING_LOCATION_SUNRISE):
        if(m.content_type == "location"):
            latitude=m.location.latitude
            longitude=m.location.longitude
            bot.send_message( cid, "Location received: \nLatitud: "+str(latitude)+"\nLongitud: "+str(longitude)+"\nGetting data...")
            request = 'http://api.sunrise-sunset.org/json?lat='+str(latitude)+'&lng='+str(longitude)
            r = requests.get(request).json()
            if(r['status']=='OK'):
                sunrise=r['results']['sunrise']
                bot.send_message( cid, "Sunrise time is: *"+sunrise+"*\nAll times are in UTC and summer time adjustments are not included in the returned data.\n_Data from http://sunrise-sunset.org_",parse_mode='Markdown')
            else:
                bot.send_message( cid, "ERROR. Please, try again")
        else:
            bot.send_message( cid, "Location not received. Request cancelled")
        del user_step[cid]
    if(waiting==constants.WAITING_LOCATION_DAY_LENGTH):
        if(m.content_type == "location"):
            latitude=m.location.latitude
            longitude=m.location.longitude
            bot.send_message( cid, "Location received: \nLatitud: "+str(latitude)+"\nLongitud: "+str(longitude)+"\nGetting data...")
            request = 'http://api.sunrise-sunset.org/json?lat='+str(latitude)+'&lng='+str(longitude)
            r = requests.get(request).json()
            if(r['status']=='OK'):
                day=r['results']['day_length']
                bot.send_message( cid, "Day length is: *"+day+"*\nAll times are in UTC and summer time adjustments are not included in the returned data.\n_Data from http://sunrise-sunset.org_",parse_mode='Markdown')
            else:
                bot.send_message( cid, "ERROR. Please, try again")
        else:
            bot.send_message( cid, "Location not received. Request cancelled")
        del user_step[cid]
    if(waiting==constants.WAITING_LOCATION_ALL):
        if(m.content_type == "location"):
            latitude=m.location.latitude
            longitude=m.location.longitude
            bot.send_message( cid, "Location received: \nLatitud: "+str(latitude)+"\nLongitud: "+str(longitude)+"\nGetting data...")
            request = 'http://api.sunrise-sunset.org/json?lat='+str(latitude)+'&lng='+str(longitude)
            r = requests.get(request).json()
            if(r['status']=='OK'):
                day=r['results']['day_length']
                sunset=r['results']['sunset']
                sunrise=r['results']['sunrise']
                bot.send_message( cid, "Sunset time is *"+sunset+"*\nSunrise time is *"+sunrise+"*\nDay length is: *"+day+"*\nAll times are in UTC and summer time adjustments are not included in the returned data.\n_Data from http://sunrise-sunset.org_",parse_mode='Markdown')
            else:
                bot.send_message( cid, "ERROR. Please, try again")
        else:
            bot.send_message( cid, "Location not received. Request cancelled")
        del user_step[cid]
        
######################################## COMMANDS ################################################################

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_message( cid, "Welcome to Sunrise & Sunset bot. With this bot you will be able to obtain sunset and sunrise times for a given location. Use the command /help to explore the different actions")
    

@bot.message_handler(commands=['help'])
def command_help(m): 
    cid = m.chat.id 
    bot.send_message( cid, "These are the possible comands:\n/sunset: Obtain sunset time for a given location\n/sunrise: Obtain sunrise time for a given location\n/day_length: Obtain the day length\n/all: Obtain all the previous information at the same time")

@bot.message_handler(commands=['sunrise'])
def command_sunrise(m): 
    cid = m.chat.id 
    bot.send_message( cid, "Please: send me your location: ")
    user_step[cid]=constants.WAITING_LOCATION_SUNRISE 
    
@bot.message_handler(commands=['sunset'])
def command_sunset(m): 
    cid = m.chat.id 
    bot.send_message( cid, "Please: send me your location: ")
    user_step[cid]=constants.WAITING_LOCATION_SUNSET 

@bot.message_handler(commands=['day_length'])
def command_daylength(m): 
    cid = m.chat.id 
    bot.send_message( cid, "Please: send me your location: ")
    user_step[cid]=constants.WAITING_LOCATION_DAY_LENGTH
    
@bot.message_handler(commands=['all'])
def command_all(m): 
    cid = m.chat.id 
    bot.send_message( cid, "Please: send me your location: ")
    user_step[cid]=constants.WAITING_LOCATION_ALL
  
################################################################################################################       
bot.polling(none_stop=True)
while True: #Infinite loop
    pass
    
