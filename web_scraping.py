import re
from bs4 import BeautifulSoup
import requests
import dateutil.parser


def get_movie_dict(link):
    base_url = 'https://www.imdb.com'
    url = base_url + link
    soup = create_soup(url)

    headers = ['title', 'country', 'runtime_minutes', 'budget', 'global_gross',
               'mpaa_rating', 'japan_release_date', 'usa_release_date', 'genres',
               'imdb_user_rating', 'imdb_user_rating_count', 'oscar_wins',
               'non_oscar_wins', 'metascore']

    title = get_title(soup)
    country = get_country(soup)
    runtime = get_runtime(soup)
    budget = get_budget(soup)
    global_gross = get_global_gross(soup)
    mpaa_rating = get_mpaa_rating(soup)

    if country == 'Japan | USA':
        japan_release_date = None
        usa_release_date = get_usa_release_date(soup)
    elif country == 'Japan':
        release_info_url = url + 'releaseinfo'
        release_info_soup = create_soup(release_info_url)
        japan_release_date = get_japan_release_date(release_info_soup)
        usa_release_date = None
    elif country == 'USA':
        usa_release_date = get_usa_release_date(soup)
        japan_release_date = None
    else:
        japan_release_date = None
        usa_release_date = None

    genres = get_genres(soup)
    imdb_user_rating = get_user_rating(soup)
    imdb_user_rating_count = get_user_rating_count(soup)
    oscar_wins = get_oscar_wins(soup)
    non_oscar_wins = get_non_oscar_wins(soup)
    metascore = get_metascore(soup)

    movie_dict = dict(
        zip(headers, [title, country, runtime, budget, global_gross,
                      mpaa_rating, japan_release_date,
                      usa_release_date, genres, imdb_user_rating,
                      imdb_user_rating_count, oscar_wins,
                      non_oscar_wins, metascore]))

    return movie_dict


def get_search_urls(base_url, next_url):
    search_urls = [base_url, next_url]
    num_titles = get_num_titles(base_url)

    for i in range(num_titles//100-1):
        search_urls.append(
            next_url.replace('101', str(201+100*i)))
    return search_urls


def get_num_titles(base_url):
    soup = create_soup(base_url)
    mini_header = soup.find('div', class_='desc').findNext().text.split()
    num_titles = int(
        mini_header[mini_header.index('titles.')-1].replace(',', ''))
    return num_titles


def create_soup(url):
    response_text = requests.get(url).text
    soup = BeautifulSoup(response_text, 'html5lib')
    return soup


def create_soups(urls):
    soups = []
    for url in urls:
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text, 'html5lib')
        soups.append(soup)
    return soups


def get_title_urls(soups):
    titles_urls = []
    for soup in soups:
        title_spans = soup.find(
            'div', class_='lister-list').find_all('span', class_='lister-item-header')
        for element in title_spans:
            titles_urls.append(element.find('a').get('href'))
    return titles_urls


def get_title(soup):
    if soup.find('h1'):
        raw_text = soup.find('h1').text.strip()
        return clean_title(raw_text)
    return None


def get_country(soup):
    for element in soup.find_all('h4'):
        if 'Country:' in element:
            raw_text = element.findParent().text.strip()
            if ('Japan' in raw_text) and ('USA' in raw_text):
                return 'Japan | USA'
            elif 'Japan' in raw_text:
                return 'Japan'
            elif 'USA' in raw_text:
                return 'USA'
    return None


def get_runtime(soup):
    if soup.find('time'):
        raw_runtime = soup.find('time').text.strip()
        return runtime_to_minutes(raw_runtime)
    return None


def get_budget(soup):
    if soup.find(text='Budget:'):
        raw_text = soup.find(
            text='Budget:').findParent().findParent().text.strip()
        budget = clean_budget(raw_text)
        if 'JPY' in budget:
            return yen_to_int(budget)
        return dollars_to_int(budget)
    return None


def get_global_gross(soup):
    for element in soup.find_all('h4'):
        if 'Cumulative Worldwide Gross:' in element:
            raw_text = element.findParent().text.strip()
            raw_text = raw_text.replace('Cumulative Worldwide Gross: ', '')
            raw_text = remove_commas(raw_text)
            return dollars_to_int(raw_text)
    return None


def get_mpaa_rating(soup):
    ratings = ['G', 'PG', 'PG-13', 'R', 'TV-PG', 'TV-MA']
    if soup.find('div', class_='subtext'):
        rating = soup.find('div', class_='subtext').text.strip().split()[0]
        if rating in ratings:
            return rating
    return None


def get_japan_release_date(soup):
    if soup.find(href='/calendar/?region=jp'):
        raw_text = soup.find(href='/calendar/?region=jp').findNext().text
        return to_datetime(raw_text)
    return None


def get_usa_release_date(soup):
    if soup.find(title='See more release dates'):
        raw_text = soup.find(
            title='See more release dates').text.strip().replace(' (USA)', '')
        return to_datetime(raw_text)
    return None


def get_genres(soup):
    if soup.find(text='Genres:'):
        raw_text = soup.find(
            text='Genres:').findParent().findParent().text.strip()
        return clean_genres(raw_text)
    return None


def get_user_rating(soup):
    if soup.find('span', itemprop='ratingValue'):
        return float(soup.find('span', itemprop='ratingValue').text)
    return None


def get_user_rating_count(soup):
    if soup.find(itemprop='ratingCount'):
        raw_text = soup.find(itemprop='ratingCount').text
        return int(remove_commas(raw_text))
    return None


def get_oscar_wins(soup):
    if soup.find('span', class_='awards-blurb'):
        if 'Won' in soup.find('span', class_='awards-blurb').text:
            raw_text = soup.find('span', class_='awards-blurb').text.strip()
            for s in raw_text.split():
                if s.isdigit():
                    return int(s)
    return None


def get_non_oscar_wins(soup):
    if soup.find('span', class_='awards-blurb'):
        if ('Oscar' in soup.find('span', class_='awards-blurb').text) and \
                (soup.find('span', class_='awards-blurb').findNextSibling()):
            raw_text = soup.find(
                'span', class_='awards-blurb').findNextSibling().text.strip()
            if 'win' in raw_text:
                for s in raw_text.split():
                    if s.isdigit():
                        return int(s)
        raw_text = soup.find('span', class_='awards-blurb').text.strip()
        if 'win' in raw_text:
            for s in raw_text.split():
                if s.isdigit():
                    return int(s)
    return None


def get_metascore(soup):
    if soup.find('div', class_='metacriticScore'):
        return int(soup.find('div', class_='metacriticScore').text.strip())
    return None


def clean_title(string):
    return re.sub('\\xa0.+', '', string)


def clean_budget(string):
    string = string.replace('Budget:', '')
    string = remove_commas(string)
    return re.sub('\\n.+', '', string)


def remove_commas(string):
    return string.replace(',', '')


def clean_genres(string):
    string = string.replace('Genres:', '')
    string = re.sub('\\n ', '', string)
    return re.sub('\\xa0\|', ', ', string)


def runtime_to_minutes(raw_runtime):
    raw_runtime = raw_runtime.replace('h', '').replace('min', '')
    runtime = raw_runtime.split()
    minutes = int(runtime[0])*60 + int(runtime[1])
    return minutes


def to_datetime(datestring):
    return dateutil.parser.parse(datestring)


def dollars_to_int(dollars_string):
    dollars_string = dollars_string.replace('$', '')
    return int(dollars_string)


def yen_to_int(yen_string):
    yen_conversion = 106.9
    yen_string = yen_string.replace('JPY', '')
    return round(int(yen_string) / yen_conversion)
