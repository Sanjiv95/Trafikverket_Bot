# Trafikverket_Bot
## Telegram setup
Look at https://medium.com/analytics-vidhya/how-i-used-a-bot-to-successfully-book-a-vaccination-slot-in-2-days-89e7ce274234
Update the bot token & chat ID in the script once you have setup your telegram app.

## First create a python venv and install the following packages
python3 -m venv <<"venv_name">>
## Activate virtual env
. .<<"venv_name">>/bin/activate
## Install required packages
pip3 install selenium
pip3 install requests
## Selenium requires firefox drivers which can be installed using:
sudo apt-get install firefox-geckodriver
## Finally run the script
python3 bot.py
  
