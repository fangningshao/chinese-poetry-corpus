# coding: utf-8
import sys
import os
import re
from bs4 import BeautifulSoup
import urllib2
import multiprocessing as mp


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
        # print 'Get dynasty:', name.encode('utf8')
        dynasty_name_urls.append((name, url))

    return dynasty_name_urls


def save_dynasties(dynasties):
    f = open(DATA_FOLDER + 'dynasty.tsv', 'w')
    for d in dynasties:
        f.write('\t'.join(d).encode('utf8') + '\n')

    f.close()


def get_authors(dynasty):
    dynasty_name, url = dynasty
    print 'Getting authors for dynasty', dynasty_name, url

    dynasty_soup = soup(url)

    d = dynasty_soup.find('div', 'list1')
    authors = d.find_all('a')
    author_name_urls = []

    for a in authors:
        name = a.text
        url = ROOT_PAGE + a.get('href')
        author_name_urls.append((name, url))
        # print name, url

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
    author_name, url = author
    print 'Getting poems for author', author_name, url
    author_soup = soup(url)
    poem_soup = author_soup.find('div', 'poem')
    divs = poem_soup.find_all('div')
    all_poems = []
    for d in divs:
        if d.get('id', '').startswith('item_'):  # is a poem
            p_title = find_text(d, 'title')
            # strip out bad characters after name
            p_title = re.sub('显示自动注释'.decode('utf8'), '', p_title).strip()

            # don't include tabs and newlines
            p_content = find_text(d, 'content').replace(
                '\t', ' ').replace('\n', '')

            all_poems.append((p_title, p_content))

            print 'POEM TITLE:', p_title
            # print 'CONTENT:', p_content

    return all_poems


def save_poems(dynasty, author, poems):
    folder = DATA_FOLDER + '%s/poems/' % dynasty
    mkdir(folder)
    print 'Saving poems for author', author
    f = open(folder + '%s.tsv' % author, 'w')
    for d in poems:
        f.write('\t'.join(d).encode('utf8') + '\n')

    f.close()


def process_author_poems(dynasty, authors, i):
    print('%s: Process %d has %d authors' % (dynasty, i, len(authors)))
    for author in authors:
        poems = get_poems(author)
        save_poems(dynasty, author[0], poems)


def mp_process_all_authors(dynasty, authors):
    processes = []
    num_processes = 8
    chunk_size = len(authors) / num_processes + 1
    for i in range(num_processes):
        authors_chunk = authors[i * chunk_size: (i + 1) * chunk_size]
        p = mp.Process(target=process_author_poems,
                       args=(dynasty, authors_chunk, i))
        p.start()
        processes.append(p)

    # wait until all finished
    for p in processes:
        p.join()


# ####################

if __name__ == '__main__':
    mkdir(DATA_FOLDER)
    print 'Data will be saved into:', DATA_FOLDER
    dynasty_name_urls = get_dynasties()
    save_dynasties(dynasty_name_urls)

    for dynasty in dynasty_name_urls:
        authors = get_authors(dynasty)
        save_authors(dynasty[0], authors)

        # for a in authors:
        #     poems = get_poems(a)
        #     save_poems(dynasty[0], a[0], poems)

        mp_process_all_authors(dynasty[0], authors)
