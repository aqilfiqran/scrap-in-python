from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import sys
import requests
import argparse

# scrapping url method


def scrap(data):
    soup = BeautifulSoup(requests.get(data[0]).text, 'html.parser')
    title = soup.select_one('.read__title').get_text()
    credit = soup.select_one('.read__credit')
    editor = credit.findAll('a')[1].get_text()
    data[1].write(f'{editor}:{title}\n')


# argument documentary
arg = argparse.ArgumentParser()
arg.add_argument("directory", help="path output file all")
option = arg.add_mutually_exclusive_group()
option.add_argument("-p", "--page-limit",
                    help="limit file by total of rows", type=int)
option.add_argument("-d", "--day-limit",
                    help="limit file by days backward", type=int)
args = vars(arg.parse_args())

# dinamic link
indexlink = "https://indeks.kompas.com/?site=all&date="

# get time of today
date = datetime.today()

# number of day and limit
day, day_limit = 1, args['day_limit'] if args['day_limit'] != None else None

# number of page and limit
page, page_limit = 0, args['page_limit'] if args['page_limit'] != None else None

path = Path()/args['directory']
with open(path, 'w') as file:
    # looping to get dynamic link by time
    while True:
        link = f'{indexlink}{date.strftime("%Y-%m-%d")}'
        # looping to get all detail link
        while True:
            print(f'Getting url from : {link}')
            soup = BeautifulSoup(requests.get(
                link).text.encode('utf-8'), 'html.parser')
            print("Url found      : ", len(soup.select('.article__title')))
            for url in soup.select('.article__title'):
                urls = url.find('a')['href']
                try:
                    # clean url and put on directory file
                    scrap([urls, file])
                    page += 1
                except (AttributeError, IndexError):
                    pass
                if page == page_limit:
                    sys.exit(f'Program reach maximum {page_limit} page')
            else:
                if(soup.find('a', {'rel': 'next'})):
                    link = soup.find('a', {'rel': 'next'})['href']
                    continue
                else:
                    break
        if day == day_limit:
            sys.exit(f'Program reach maximum {day_limit} day')

        date += timedelta(days=-1)
        day += 1
