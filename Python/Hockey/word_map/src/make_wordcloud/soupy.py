from bs4 import BeautifulSoup
import requests
import lxml
import csv
import time
import json

# *********** RULES FOR WEBSCRAPPING **************
# look to robots.txt file to see if it is allowed or not

# get_text() - research options - used ' ' as a separator for words that are stripped out with <br> or similar and


def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_data(title):
    with open(title, encoding='utf-8') as f:
        return json.load(f)


def get_content_from_li(row_data):
    if row_data.find('li'):
        return [li.get_text(' ', strip=True).replace('\xa0', ' ') for li in row_data.find_all('li')]
    else:
        return row_data.get_text(' ', strip=True).replace('\xa0', ' ')

# def get_source(url, filename):
#     source = requests.get(url)
#     soup = BeautifulSoup(source.content, 'lxml')
#     soup_file = open('data/raw/' + filename, 'w')
#     soup_file.write(str(soup))
#     soup_file.close()


def get_info_box(url):
    source = requests.get(url)
    soup = BeautifulSoup(source.content, 'lxml')

    info_box = soup.find('table', class_='infobox vevent')
    info_rows = info_box.find_all('tr')

    movie_info = {}

    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['Title'] = row.find('th').get_text(
                ' ', strip=True).replace('\xa0', ' ')
        elif index == 1:
            continue    # picture of poster
        else:
            content_key = row.find(
                class_='infobox-label').get_text(' ', strip=True).replace('\xa0', ' ')
            content_data = get_content_from_li(row.find(class_='infobox-data'))
            # content_data = row.find(class_='infobox-data').get_text()

            movie_info[content_key] = content_data
    return movie_info


# get_source('https://en.wikipedia.org/wiki/Toy_Story_3')
# get_source(
#     'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films', 'souplist.html')


# source = requests.get('https://en.wikipedia.org/wiki/Toy_Story_3').text

# soup = BeautifulSoup(source.content, 'lxml')

# with open('data/raw/soup.html') as html_file:
#     soup = BeautifulSoup(html_file, 'lxml')

with open('data/raw/souplist.html') as html_file:
    souplist = BeautifulSoup(html_file, 'lxml')

# using the i class because the title and href is in the i attribute in the td
# however - there were items that had italics in the co-production companies on the right which were NOT film names
# put the italics as part of an a tag and that solves that part of things
movies = souplist.select('.wikitable.sortable i a')
base_path = 'https://en.wikipedia.org'

movie_info_list = []
for index, movie in enumerate(movies):
    time.sleep(3)
    if index == 5:
        break

    try:
        relative_path = movie['href']
        full_path = base_path + relative_path
        title = movie['title']
        print(full_path)

        movie_info_list.append(get_info_box(full_path))
    except Exception as e:
        print(movie.get_text())
        print(e)

    # print(relative_path, '\n', title, '\n')

save_data('output/disney_data.json', movie_info_list)

print(movie_info_list)


# <td><i><a href="/wiki/Academy_Award_Review_of_Walt_Disney_Cartoons" title="Academy Award Review of Walt Disney Cartoons">Academy Award Review of Walt Disney Cartoons</a></i>

# ***** WORKING ******
# stuff2 = open('data/raw/stuff2.txt', 'w')
# stuff2.write(str(movies))
# stuff2.close()

# movie_info = {}

# info_box = soup.find('table', class_='infobox vevent')
# info_rows = info_box.find_all('tr')

# for index, row in enumerate(info_rows):
#     if index == 0:
#         movie_info['Title'] = row.find('th').get_text(
#             ' ', strip=True).replace('\xa0', ' ')
#     elif index == 1:
#         continue    # picture of poster
#     else:
#         content_key = row.find(
#             class_='infobox-label').get_text(' ', strip=True).replace('\xa0', ' ')
#         content_data = get_content_from_li(row.find(class_='infobox-data'))
#         # content_data = row.find(class_='infobox-data').get_text()

#         movie_info[content_key] = content_data
# ***** END WORKING ******


# print(movie_info)
