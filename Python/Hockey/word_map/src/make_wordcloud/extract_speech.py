from bs4 import BeautifulSoup
import requests
import lxml
import csv
import time

# Sample with an html file on the disk
# with open('src/make_wordcloud/simple.html') as html_file:
#     soup = BeautifulSoup(html_file, 'lxml')

# print(soup.prettify())
# match = soup.title.text
# match2 = soup.div
# match3 = soup.find('div', class_='footer')  # class = python keyword
# match4 = soup.find('h1', id='site_title')

# # print(match, '\n', match2, match3, match4)

# # artmat = soup.find('div', class_='article') #single
# for artmat in soup.find_all('div', class_='article'):
#     headline = artmat.h2.a.text
#     summary = artmat.p.text

#     print(artmat, headline, summary)

source = requests.get('http://coreyms.com').text

soup = BeautifulSoup(source, 'lxml')

csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headers', 'summary', 'video_link'])

for article in soup.find_all('article'):
    headline = article.h2.a.text
    summary = article.find('div', class_='entry-content').p.text

    try:
        # grab the URL from the iFrame for the embedded youtube video
        vid_src = article.find('iframe', class_='youtube-player')['src']

        # gives us where the ID is located - left of the ? and then split again on the ?
        vid_id = vid_src.split('/')[4].split('?')[0]
        youtube_link = f'https://youtube.com/watch?v={vid_id}'
    except Exception as e:
        youtube_link = None

    csv_writer.writerow([headline, summary, youtube_link])
    print(headline, '\n', summary, '\n', vid_src, '\n', youtube_link, '\n')
    time.sleep(5)

csv_file.close()

# # print(article.prettify(), '\n', headline, '\n', summary, '\n', vid_src)
# print(vid_src, '\n', vid_id)


# print(youtube_link)
