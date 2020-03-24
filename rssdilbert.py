import os
from datetime import date
import configparser
import requests
from bs4 import BeautifulSoup as bs
from slackclient import SlackClient

#slack_channel = "CEKB88A1Y"
slack_channel = "GDQ7JPD8U"

BASE_URL = "https://dilbert.com/strip/"
NEWEST_COMIC = date.today()

def get_today():
    """
    Returns today's date
    """
    today = date.today()
    return today

def get_comic_strip_url(start_date):
    """
    Outputs the comic strip date url in the https://dilbert.com/YYYY-MM-DD format
    """
    full_url = []
    full_url.append(BASE_URL+str(start_date))
    return full_url

def get_image_comic_url(session, response):
    """
    Fetches the comic strip image source url based on the strip url
    """
    soup = bs(response.text, 'lxml')
    for div in soup.find_all('div', class_="img-comic-container"):
        for a in div.find_all('a', class_="img-comic-link"):
            for img in a.find_all('img', src=True):
                return "https:" + img['src']

def download_dilbert(s, u):
    """
    Downloads and saves the comic strip
    """
    with open("comicfile.jpg", "wb") as file:
        response = s.get(u)
        file.write(response.content)

def post_to_slack(slack_client, comic):
    slack_client.api_call("chat.postMessage", channel=slack_channel, text='Test', as_user = True)

def download_engine(fcsd): #fcsd = first comic strip date

    """
    Based on the strip url, fetches the comic image source and downloads it
    """

    url_list = get_comic_strip_url(fcsd)

    for url in url_list:
        session = requests.Session()
        response = session.get(url)
        download_url = get_image_comic_url(session, response)
#        download_dilbert(session, download_url)
    return download_url

def load_config(config_file, config_section):
#    dir_path = os.path.dirname(os.path.relpath('config.ini'))
    dir_path = os.path.dirname(os.path.realpath(__file__))
#    dir_path = os.path.abspath('.')
    if os.path.isfile(dir_path + '/' + config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        slack_token = config.get(config_section, 'token')
    else:
        slack_token = os.environ['token']
    return slack_token

def main():
    config_file = 'config.ini'
    config_section = 'dev'
    slack_token = load_config(config_file, config_section)
    slack_client = SlackClient(slack_token)    
    comic = download_engine(get_today())
    post_to_slack(slack_client,comic)

if __name__ == '__main__':
    main()

