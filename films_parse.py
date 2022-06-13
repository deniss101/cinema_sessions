import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime

film_list, link_list, cinema_list, sessions_list, = [], [], [], []


def get_data_from_url(url):
    request = requests.get(url)
    html_content = BS(request.content, 'lxml')
    return html_content


def get_film_list():
    url = "https://kudago.com/msk/kino/schedule-cinema/"
    html_data = get_data_from_url(url)
    films = html_data.find_all(class_='post-title-link')
    print(films)
    for film in films:
        film_name = film.get('title')
        film_link = film.get('href')
        film_list.append(film_name)
        link_list.append(film_link)


def get_cinema_and_time():
    for url in link_list:
        html_data = get_data_from_url(url)
        sessions = html_data.find_all(class_='schedule-showing-row')
        print(sessions)
        '''for session in sessions:
            cinemas = session.get('href')
            cinema_list.append(cinemas)
            print(cinema_list)'''

get_film_list()
get_cinema_and_time()