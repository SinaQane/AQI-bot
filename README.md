# AQI-bot
A Telegram bot for getting your city and its regions' AQI directly from http://aqicn.org

It’s using the website’s official API, you can get your private Token from http://aqicn.org/api/

Bot can be used in pv (for getting city and all it's regions' AQI), or in inline mode (for just city's AQI)

It's good to know about the condition of our city's air and, maybe in the future, act better on it.

## Setup
First install requirements
```python
pip install -r requirements.txt
```
For running the code just Use the token as command arg in terminal
```python
python3 AQIbot.py botToken APIToken
```

## Usage
You can test my bot at: https://t.me/AirNow_bot

Use it as inline bot in private chats or groups by calling ID of bot:
```python
@AirNow_bot Example City
```
