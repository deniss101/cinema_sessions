import requests
import json
import sqlite3
from bs4 import BeautifulSoup as Bs
from datetime import date, datetime

SET_DATE = date.today()
LOCATION = 'msk'

con = sqlite3.connect('cinema_sessions.db', check_same_thread=False)


def get_cinema_sessions():
    cur = con.cursor()
    cur.execute("DROP TABLE if exists sessions")
    cur.execute("CREATE TABLE if not exists sessions (id, title, cinema, address, subway, time, price)")
    id_list, title_list = [],[]
    site_url = f'https://kudago.com/{LOCATION}/kino/schedule-cinema/'
    html_data = Bs(requests.get(site_url).text, 'lxml')
    ids = html_data.find_all(class_='post post-rect')
    for id in ids:
        film_id = id.get('data-ping-item-id')
        id_list.append(film_id)
    films = html_data.find_all(class_='post-title-link')
    for film in films:
        film_name = film.get('title')
        title_list.append(film_name)
    title_start = 0
    for movie_id in id_list:
        title_start +=1
        film_url = f'https://kudago.com/widgets/movie-showings/?date={SET_DATE}&movie_id={movie_id}&group_by=place&location={LOCATION}'
        json_file = requests.get(film_url).text
        json_data = json.loads(json_file)['places']
        for i in range(len(json_data)):
            title = json_data[i]['title'].capitalize()
            address = json_data[i]['address']
            subway = json_data[i]['subway']
            for show in json_data[i]['showings']:
                time = datetime.fromtimestamp(show['time']).strftime('%H:%M')
                price = show['price']
                print(movie_id, title_list[title_start], title, address, subway, time, price)
                cur.execute("INSERT INTO sessions (id, title, cinema, address, subway, time, price) VALUES(?, ?, ?, ?, ?, ?, ?)",
                            (movie_id, title_list[title_start], title, address, subway, time, price))
    con.commit()
    cur.close()


def read_data_from_base():
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    films = cur.execute("SELECT DISTINCT title FROM sessions ").fetchall()
    cur.close()
    text = "Сеансы:"
    for film in films:
        text += '\n' + film
    return text

get_cinema_sessions()