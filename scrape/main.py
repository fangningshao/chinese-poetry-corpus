# coding: utf-8
import sys
import os
import re
from bs4 import BeautifulSoup
import urllib2


def fetch(url):
    return urllib2.urlopen(url).read()


def soup(url):
    return BeautifulSoup(fetch(url), 'html.parser')


def find_text(s, cls, tag='div'):
    """Find text or return None"""
    r = s.find(tag, cls)
    if r:
        return r.text
    else:
        return None


def mkdir(path):
    if not os.path.exists(path):
        print 'Making directory:', path
        os.makedirs(path)


ROOT_PAGE = 'http://sou-yun.com/'
DATA_FOLDER = './data/'


def get_dynasties():
    # Fetch main page
    MAIN_PAGE = 'http://sou-yun.com/PoemIndex.aspx'
    main_soup = BeautifulSoup(fetch(MAIN_PAGE), 'html.parser')

    # Find all dynasties
    dynasties = main_soup.find_all('a', 'list')

    dynasty_name_urls = []
    for a in dynasties:
        url = ROOT_PAGE + a.get('href')
        name = a.text
        print 'Get dynasty:', name.encode('utf8')
        dynasty_name_urls.append((name, url))

    return dynasty_name_urls


def save_dynasties(dynasties):
    f = open(DATA_FOLDER + 'dynasty.tsv', 'w')
    for d in dynasties:
        f.write('\t'.join(d).encode('utf8') + '\n')

    f.close()



def get_authors(dynasty):
    dynasty_name, url = dynasty
    print dynasty_name, url

    dynasty_soup = soup(url)

    d = dynasty_soup.find('div', 'list1')
    authors = d.find_all('a')
    author_name_urls = []

    for a in authors:
        name = a.text
        url = ROOT_PAGE + a.get('href')
        author_name_urls.append((name, url))
        print name, url

    return author_name_urls


def save_authors(dynasty, authors):
    # e.g. save into data/清/authors.tsv
    folder = DATA_FOLDER + '%s/' % dynasty
    mkdir(folder)
    print 'Saving authors in dynasty', dynasty
    f = open(folder + 'authors.tsv', 'w')
    for d in authors:
        f.write('\t'.join(d).encode('utf8') + '\n')

    f.close()

def get_poems(author):
    dynasty_name, url = dynasty


def save_poems(poems):
    pass

# p1 = soup(dynasty_name_urls[0][1])


# d = p1.find('div', 'list1')
# authors = d.find_all('a')
# author_name_urls = []
# for a in authors:
#     author_name_urls.append((a.text, ROOT_PAGE + a.get('href')))

# author_name_urls


# test_author_name, url = author_name_urls[1]
# print test_author_name, url
# test_author_soup = soup(url)


# def get_all_poems_for_author(author_soup):
#     poem_soup = author_soup.find('div', 'poem')
#     divs = poem_soup.find_all('div')
#     for d in divs:
#         if d.get('id', '').startswith('item_'):  # is a poem
#             p_title = find_text(d, 'title')
#             p_title = re.sub('显示自动注释', '', p_title).strip()
# #             print 'POEM TITLE:', p_title
#             p_content = find_text(d, 'content')
# #             print 'CONTENT:', p_content
#             yield p_title, p_content


# print test_author_name
# for t, c in get_all_poems_for_author(test_author_soup):
#     pass


# for name, url in author_name_urls:
#     s = soup(url)
#     for t, c in get_all_poems_for_author(s):
#         print (name, t)


# ####################

if __name__ == '__main__':
    mkdir(DATA_FOLDER)
    print 'Data will be saved into:', DATA_FOLDER
    dynasty_name_urls = get_dynasties()
    save_dynasties(dynasty_name_urls)

    for dynasty in dynasty_name_urls:
        authors = get_authors(dynasty)
        save_authors(dynasty[0], authors)

        for a in authors:
            poems = get_poems(a)
            save_poems(poems)
