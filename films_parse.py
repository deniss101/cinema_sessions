import requests
from bs4 import BeautifulSoup as BS
from datetime import date, datetime, timezone

film_list, link_list = [], []


def get_data_from_url(url):
    request = requests.get(url)
    return request


def get_film_list():
    url = "https://kudago.com/msk/kino/schedule-cinema/"
    html_data = BS(get_data_from_url(url).content, 'lxml')
    films = html_data.find_all(class_='post-title-link')
    for film in films:
        film_name = film.get('title')
        film_link = film.get('href')
        film_list.append(film_name)
        link_list.append(film_link)
        print(film_name +' '+ film_link)


def get_sessions_price():
    today = date.today()
    movie_id = 5335
    location = 'msk'
    url = f'https://kudago.com/widgets/movie-showings/?date={today}&movie_id={movie_id}&group_by=place&location={location}'
    json_file = get_data_from_url(url)
    json_data = [*json_file.json()['places']]
    for i in range(len(json_data)):
        title = json_data[i]['title'].capitalize()
        address = json_data[i]['address']
        subway = json_data[i]['subway']
        times_prices_extract = json_data[i]['showings']
        times_prices = (times_prices_extract[0])
        time = (datetime.fromtimestamp(times_prices['time']).strftime('%H:%M'))
        price = (times_prices['price'])
        print(f'{title} \nАдрес: {address} \nМетро: {subway}\nСеансы: {time}\nЦена: {price}\n')


get_film_list()
get_sessions_price()