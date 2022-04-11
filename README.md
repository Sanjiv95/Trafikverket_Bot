# Trafikverket_Bot

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
  
