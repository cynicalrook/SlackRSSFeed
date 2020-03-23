import os
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup as bs


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

def download_engine(fcsd): #fcsd = first comic strip date

    """
    Based on the strip url, fetches the comic image source and downloads it
    """

    url_list = get_comic_strip_url(fcsd)

    for url in url_list:
        session = requests.Session()
        response = session.get(url)
        download_url = get_image_comic_url(session, response)
        download_dilbert(session, download_url)


def main():
    download_engine(get_today())


if __name__ == '__main__':
    main()

