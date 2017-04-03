"""
    getSymptomsByLetter.py
"""


import pickle
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article


def findAllSymptomLinks():
    '''
    Finds all symptom links in a MayoClinic article

    :return: set of all URLs of diseases
    '''
    start = 'A'
    links = set()

    for i in range(26):
        suffix = chr(ord(start) + i)

        resp = urllib.request.urlopen(
            "http://www.mayoclinic.org/symptoms/index?letter=" + suffix)
        soup = BeautifulSoup(resp, "lxml")

        for link in soup.find_all('a', href=True):
            if 'symptoms' in str(link['href']) \
                    and 'index' not in str(link['href']) \
                    and str(link['href']) != '/symptoms' \
                    and str(link['href']) != 'http://www.mayoclinic.org/symptoms':

                links.add('http://mayoclinic.org' + str(link['href']))

    return links


def findTitle(url):
    '''
    Searches for the article title from meta tags

    :return: str
    '''
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, "lxml")

    for meta in soup.find_all('meta'):
        try:
            name = meta['name']

            if name == 'Subject':
                return meta['content']
        except:
            continue
    return None


def findAllSymptoms():
    '''
    Finds the names of all the diseases, dumps them into a pickle file and
    returns the list of all symptoms

    :return: list of symptoms
    '''

    data = []

    for url in findAllSymptomLinks():
        try:
            title = findTitle(url)
            data.append(title)
        except:
            continue

    saveData = open('pickle/saveSymptomData.pickle', 'wb')
    pickle.dump(data, saveData)
    saveData.close()

    return data
