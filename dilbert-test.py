#!/usr/bin/python3.6

"""
A simple comic strip scraper for dilbert.com
"""

import os
import subprocess

import time
import sys

import colorama
from colorama import Fore

from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from dateutil.relativedelta import relativedelta


LOGO = """
     _        _             _ _ _ _               _   
    | |      (_)           | (_) | |             | |  
 ___| |_ _ __ _ _ __     __| |_| | |__   ___ _ __| |_ 
/ __| __| '__| | '_ \   / _` | | | '_ \ / _ \ '__| __|
\__ \ |_| |  | | |_) | | (_| | | | |_) |  __/ |  | |_ 
|___/\__|_|  |_| .__/   \__,_|_|_|_.__/ \___|_|   \__|
               | |                                    
               |_|                 version: 0.2 | 2019

"""

DEFAULT_DIR_NAME = "my_dilberts"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)

BASE_URL = "https://dilbert.com/strip/"

FIRST_COMIC = date(1989, 4, 16)  # The earliest diblert comic strip published
NEWEST_COMIC = date.today()


def clear_screen():
    """
    Clears terminal screen
    """
    if os.name in ('nt', 'dos'):
        subprocess.call('cls')
    elif os.name in ('linux', 'osx', 'posix'):
        subprocess.call('clear')
    else:
        print("\n" * 120)


def show_logo():
    """
    Displays the ascii logo
    """
    clear_screen()
    colorama.init(autoreset=True)
    print("\nA simple comic strip scraper for dilbert.com")
    print(Fore.RED + LOGO)
    print("author: baduker | repo: github.com/baduker/strip_dilbert\n")


def show_main_menu():
    """
    Main download menu
    """
    print("Choose a menu item to download:\n")
    print("1. Today's comic strip: {}".format(get_today()))
    print("2. This week's strips:  {} - {}".format(get_this_week()[0], get_this_week()[1]))
    print("3. Last week's strips:  {} - {}".format(get_last_week()[0], get_last_week()[1]))
    print("4. This month's strips: {} - {}".format(get_this_month()[0], get_this_month()[1]))
    print("5. Last month's strips: {} - {}".format(get_last_month()[0], get_last_month()[1]))
    print("6. Custom date ragne:")
    print("-"*20)
    print("0. Type 0 to Exit.\n")


def get_main_menu_item():
    """
    Takes and checks the main menu selection input
    """
    while True:
        try:
            main_menu_item = int(input("Type your selection here: "))
        except ValueError:
            print("\nError: expected a number! Try again.\n")
            continue
        if main_menu_item < 0:
            print("\nSorry, that didn't work! Try again.\n")
            continue
        elif main_menu_item > 6:
            print("\nNo such menu item! Try again.\n")
            continue
        elif main_menu_item == 0:
            sys.exit()
        else:
            break
    return main_menu_item


def handle_main_menu(menu_item):
    """
    Handles the main menu and invokes the download engine
    """
    if menu_item == 1:
        download_engine(get_today(), get_today())
    elif menu_item == 2:
        download_engine(get_this_week()[0], get_this_week()[1])
    elif menu_item == 3:
        download_engine(get_last_week()[0], get_last_week()[1])
    elif menu_item == 4:
        download_engine(get_this_month()[0], get_this_month()[1])
    elif menu_item == 5:
        download_engine(get_last_month()[0], get_last_month()[1])
    elif menu_item == 6:
        clear_screen()
        today = date.today()
        print("\nNOTE! Since {}, there has been {} (as of {}) dilberts published.".format(FIRST_COMIC.strftime('%d/%b/%Y'), get_number_of_dilberts_till_now(), today.strftime('%d/%b/%Y')))
        print("So, if you want to download all of them bear in mind that it might take a while.\n")
        print("1. Downlaod all dilberts ({})!".format(get_number_of_dilberts_till_now()))
        print("2. Enter a custom date range.")
        print("-"*20)
        print("0. Type 0 to Exit.\n")

        minor_item = get_minor_menu_item()
        handle_minor_menu(minor_item)


def get_minor_menu_item():
    """
    Takes and checks the minor menu selection input
    """
    while True:
        try:
            minor_menu_item = int(input("Type your selection here: "))
        except ValueError:
            print("\nError: expected a number! Try again.\n")
            continue
        if minor_menu_item < 0:
            print("\nSorry, that didn't work! Try again.\n")
            continue
        elif minor_menu_item > 2:
            print("\nNo such menu item! Try again.\n")
            continue
        elif minor_menu_item == 0:
            sys.exit()
        else:
            break
    return minor_menu_item


def handle_minor_menu(menu_item):
    """
    Handles the minor menu and invokes the custom date range download engine
    """
    if menu_item == 1:
        download_engine(FIRST_COMIC, NEWEST_COMIC)
    elif menu_item == 2:
        first_strip_date = get_comic_strip_start_date()
        last_strip_date = get_comic_strip_end_date()
        download_engine(first_strip_date, last_strip_date)


def get_today():
    """
    Returns today's date
    """
    today = date.today()
    return today


def get_this_week():
    """
    Returns dates for current week
    """
    today = date.today()
    week_start = today - timedelta(days = today.weekday())
    delta = (today - week_start).days
    week_end = week_start + timedelta(days= delta)
    return week_start, week_end


def get_last_week():
    """
    Returns last week's date range
    """
    today = date.today()
    last_week_start = today - timedelta(days = today.weekday(), weeks = 1)
    last_week_end = last_week_start + timedelta(days=6)
    return last_week_start, last_week_end


def get_this_month():
    """
    Returns dates for current month
    """
    today = date.today()
    if today.day > 25:
        today += timedelta(7)
    first_day_of_this_month = today.replace(day=1)
    return first_day_of_this_month, today


def get_last_month():
    """
    Returns last month's date range
    """
    today = date.today()
    today_but_a_month_ago = today - relativedelta(months = 1)
    first_day_of_previous_month = date(today_but_a_month_ago.year, today_but_a_month_ago.month, 1)
    last_day_of_the_previous_month = date(today.year, today.month, 1) - relativedelta(days = 1)
    return first_day_of_previous_month, last_day_of_the_previous_month          


def get_number_of_dilberts_till_now():
    """
    Counts all the comic strips published since April 16th, 1989
    """
    today = date.today()
    delta = (today - FIRST_COMIC).days + 1
    return delta


def get_comic_strip_start_date():
    """
    Asks for initial comic strip date for custom date range
    """
    print("Type a dilbert comic start date in YYYY/MM/DD format:")
    while True:
        start_year, start_month, start_day = map(int, input(">> ").split("/"))
        start_date = date(start_year, start_month, start_day)
        if start_date < FIRST_COMIC:
            print("The oldest comic is from 1989/04/16. Try again.")
            continue
        elif start_date > date.today():
            print("You can't download anything from the future yet. Try again.")
            continue
        else:
            break
    return start_date


def get_comic_strip_end_date():
    """
    Asks for final comic strip date for custom date range
    """
    print("Type a dilbert comic end date in YYYY/MM/DD format:")
    while True:
        end_year, end_month, end_day = map(int, input(">> ").split("/"))
        end_date = date(end_year, end_month, end_day)
        if end_date < FIRST_COMIC:
            print("The oldest comic is from 1989/04/16. Try again.")
            continue
        elif end_date > date.today():
            print("You can't download anything from the future yet. Try again.")
            continue
        else:
            break
    return end_date


def get_comic_strip_url(start_date, end_date):
    """
    Outputs the comic strip date url in the https://dilbert.com/YYYY-MM-DD format
    """
    full_url = []
    delta = end_date - start_date
    for day in range(delta.days + 1):
        full_url.append(BASE_URL+str(start_date + timedelta(day)))
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
    filne_name = u.split('/')[-1]
    with open(os.path.join(COMICS_DIRECTORY, filne_name), "wb") as file:
        response = s.get(u)
        file.write(response.content)


def download_engine(fcsd, lcsd): #fcsd = first comic strip date & lcsd = last comis strip date

    """
    Based on the strip url, fetches the comic image source and downloads it
    """
    start = time.time()

    url_list = get_comic_strip_url(fcsd, lcsd)

    os.mkdir(DEFAULT_DIR_NAME)

    for url in url_list:
        session = requests.Session()
        response = session.get(url)
        download_url = get_image_comic_url(session, response)

        pbar = tqdm(range(len(url_list)))

        for i in pbar:
            pbar.set_description("Fetching {}".format(url[8:]))
            download_dilbert(session, download_url)

    end = time.time()

    print("{} dilbert comics downloaded in {:.2f} seconds!".format(len(url_list), end - start))


def main():
    """
    Encapsulates and executes all methods in the main function
    """
    show_logo()
    show_main_menu()
    the_main_menu_item = get_main_menu_item()
    handle_main_menu(the_main_menu_item)


if __name__ == '__main__':
    main()
    