import requests
import json
from bs4 import BeautifulSoup as Bs
from datetime import date, datetime

TODAY = date.today()
title_list, link_list, id_list = [], [], []


def get_data_from_url(url):
    request = requests.get(url)
    return request


def get_film_list(location='msk'):
    url = f'https://kudago.com/{location}/kino/schedule-cinema/'
    html_data = Bs(get_data_from_url(url).text, 'lxml')
    ids_extend = html_data.find_all(class_='post post-rect post-editors-choice')
    for i in ids_extend:
        film_id_ex = i.get('data-ping-item-id')
        id_list.append(film_id_ex)
    ids = html_data.find_all(class_='post post-rect')
    for i in ids:
        film_id = i.get('data-ping-item-id')
        id_list.append(film_id)
    films = html_data.find_all(class_='post-title-link')
    for film in films:
        film_name = film.get('title')
        film_link = film.get('href')
        title_list.append(film_name)
        link_list.append(film_link)


def get_sessions_price(movie_id=5364, date=TODAY, location='msk'):
    url = f'https://kudago.com/widgets/movie-showings/?date={date}&movie_id={movie_id}&group_by=place&location={location}'
    json_file = get_data_from_url(url).text
    json_data = json.loads(json_file)['places']
    for i in range(len(json_data)):
        title = json_data[i]['title'].capitalize()
        address = json_data[i]['address']
        subway = json_data[i]['subway']
        print(title, address, subway)
        for show in json_data[i]['showings']:
            print(datetime.fromtimestamp(show['time']).strftime('%H:%M'), "Цена:", show['price'])
        print()


get_film_list()
get_sessions_price()

