import requests
from bs4 import BeautifulSoup as bs
import scraperwiki
from datetime import datetime
import grequests

start_url = 'http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0'

asins=[]
def scrape(response, **kwargs):
        listing_soup = bs(response.text, 'lxml')
        asin_nums = listing_soup.find_all('div', 'zg_itemImageImmersion')
        for asin_num in asin_nums:
            asin = ''
            try:
                asin = asin_num.a['href'].split('dp/')[-1].strip()
            except:
                pass
            print asin
            today_date = str(datetime.now())
            scraperwiki.sqlite.save(unique_keys=['Date'], data={'ASIN': asin, 'Date': today_date})


def parse(url):
    page = requests.get(url)
    soup = bs(page.text, 'lxml')
    if url == start_url:
        async_list = []
        for i in xrange(1, 6):
            print (url+'?&pg={}'.format(i))
            rs = (grequests.get(url+'?&pg={}'.format(i), hooks = {'response' : scrape}))
            async_list.append(rs)
        grequests.map(async_list)


    active_sel = soup.find('span', 'zg_selected').find_next()
    if active_sel.name == 'ul':
        links_list = active_sel.find_all('li')
        for link_list in links_list:
            link = link_list.find('a')['href'].encode('utf-8')
            async_list = []
            for i in xrange(1, 6):
                print (link+'?&pg={}'.format(i))
                rs = (grequests.get(link+'?&pg={}'.format(i), hooks = {'response' : scrape}))
                async_list.append(rs)

            grequests.map(async_list)
            parse(link)


if __name__ == '__main__':

    parse(start_url)
