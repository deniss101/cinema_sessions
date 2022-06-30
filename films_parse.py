import requests
import json
import sqlite3
from bs4 import BeautifulSoup as Bs
from datetime import date, datetime

set_date = date.today()
title_list, id_list = [], []
con = sqlite3.connect('cinema_sessions.db')
cur = con.cursor()

def get_data_from_url(url):
    request = requests.get(url)
    return request


def sql_operations(query):
    con = sqlite3.connect('cinema_sessions.db')
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()


def get_film_list(location='msk'):
    url = f'https://kudago.com/{location}/kino/schedule-cinema/'
    html_data = Bs(get_data_from_url(url).text, 'lxml')
    ids = html_data.find_all(class_='post post-rect')
    for i in ids:
        film_id = i.get('data-ping-item-id')
        id_list.append(film_id)
    films = html_data.find_all(class_='post-title-link')
    for film in films:
        film_name = film.get('title')
        title_list.append(film_name)
    for i in range(len(id_list)):
        print(title_list[i+1])          #title_list[i+1], to remove with useless film with id=1
        cur.execute("INSERT INTO tab (title) VALUES(?)", (str(1)))
        get_sessions_price(id_list[i])



def get_sessions_price(movie_id, location='msk'):
    url = f'https://kudago.com/widgets/movie-showings/?date={set_date}&movie_id={movie_id}&group_by=place&location={location}'
    json_file = get_data_from_url(url).text
    json_data = json.loads(json_file)['places']
    for i in range(len(json_data)):
        title = json_data[i]['title'].capitalize()
        address = json_data[i]['address']
        subway = json_data[i]['subway']
        print(title, address, subway)
        for show in json_data[i]['showings']:
            print(datetime.fromtimestamp(show['time']).strftime('%H:%M'), "Цена:", show['price'], '\n')
            time = datetime.fromtimestamp(show['time']).strftime('%H:%M')
            price = show['price']
            cur.execute("INSERT INTO tab (cinema, address, subway, time, price) VALUES(?, ?, ?, ?, ?)", (title, address, subway, time, price))


get_film_list()
con.commit()
cur.close()
con.close()

