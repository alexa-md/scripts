"""
    getLinksByLetter.py
"""


import pickle
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article


junkContent = ['e-newsletter', 'Mayo Clinic', 'Symptoms',
               'Before school', 'School age', 'Teens and adults',
               'When to see a doctor', 'Causes', 'Risk factors',
               'Complications']


def findAllDiseases():
    '''
    Searches for all disease URLs

    :return: set() of all URLs of diseases
    '''
    start = 'A'
    links = set()

    for i in range(26):
        suffix = chr(ord(start) + i)

        resp  = urllib.request.urlopen("http://www.mayoclinic.org/diseases-conditions/index?letter=" + suffix)
        soup = BeautifulSoup(resp, "lxml")

        for link in soup.find_all('a', href=True):
            if 'diseases-conditions' in str(link['href']) \
                    and 'letter=' not in str(link['href']) \
                    and 'http://www.mayoclinic.org/diseases-conditions' not in str(link['href']) \
                    and str(link['href']) != '/diseases-conditions':
                links.add('http://mayoclinic.org' + str(link['href']))

    return links


def findTitle(soup):
    '''
    Searches for the article title from meta tags

    :return: str
    '''

    for meta in soup.find_all('meta'):
        try:
            name = meta['name']

            if name == 'Subject':
                return meta['content']
        except:
            continue
    return None


def findSymptoms(url):
    '''
    Finds core article and returns it as a list of sentences

    :return: list of the symptom sentences
    '''
    article = Article(url=url.strip(' '), language='en')
    article.download()
    article.parse()

    unfiltered = article.text.replace('\n\n', ' ').split('.')
    filtered = []

    for a in unfiltered:
        junk = False

        for b in junkContent:
            if b in a:
                junk = True

        if a and not junk:
            filtered.append(a)

    return filtered


def findAllSymptoms():
    '''
    Goes through all disease URLs getting symptoms related to each disease,
    dumps them to a pickle file, and returns a list of dicts mapping each
    disease to its list of symptoms

    :return: list of dict of title and list of symptoms
    '''

    data = []

    for url in findAllDiseases():
        try:
            resp = urllib.request.urlopen(url)
            soup = BeautifulSoup(resp, "lxml")

            for link in soup.find_all('a', href=True):
                if 'diseases-conditions' in str(link['href']) \
                    and 'symptoms' in str(link['href']) \
                    and 'basics' in str(link['href']):

                    l = 'http://mayoclinic.org' + link['href']
                    print(l)
                    title = findTitle(soup)
                    symptoms = findSymptoms(l)
                    print({'title': title,
                           'symptoms': symptoms})
                    data.append({'title': title,
                                 'symptoms': symptoms})
                    break
        except:
            continue

    saveData = open('pickle/saveData2.pickle', 'wb')
    pickle.dump(data, saveData)
    saveData.close()

    return data
