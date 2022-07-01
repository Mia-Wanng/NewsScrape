import requests
from bs4 import BeautifulSoup
import pprint

# set how many pages you want to scrape
n = 8

# set main page
res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
All_Links = soup.select('.titlelink')
All_Subtexts = soup.select('.subtext')
# add page 2-n 's info
for i in range(2, n):
    res = requests.get(f'https://news.ycombinator.com/news?p={i}')
    soup = BeautifulSoup(res.text, 'html.parser')
    All_Links += soup.select('.titlelink') 
    All_Subtexts += soup.select('.subtext')

#sort based on votes rank
def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
  hn = []
  for idx, item in enumerate(links):
    title = item.getText()
    href = item.get('href', None)
    vote = subtext[idx].select('.score')
    if len(vote):
      points = int(vote[0].getText().replace(' points', ''))
      if points > 99:
        hn.append({'title': title, 'link': href, 'votes': points})
  return sort_stories_by_votes(hn)
 
pprint.pprint(create_custom_hn(All_Links, All_Subtexts))
