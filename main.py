# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import pandas as pd

# essayer voir plus
# Prendre le titre de la maison

url_nordouest = 'https://www.leboncoin.fr/recherche/?category=9&locations=Monsols_69860__46.22131_4.51854_10000_50000&immo_sell_type=old&real_estate_type=1,5&price=50000-125000&square=130-max&rooms=6-max'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
offres = list()
offres_valides = []
offres_premium = []
offres_valides_url = []
offres_valides_title = []
offres_valides_prix = []
offres_premium_url = []
offres_premium_title = []
offres_premium_prix = []

for i in range(1, 6):
    if (i == 1):
        url_base = url_nordouest
    else:
        url_base = url_nordouest+"&page="+str(i)
    r = requests.get(url_base, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    for link in soup.find_all("a", {"class": "clearfix trackable"}):
        offres.append(link.get('href'))
    for offre in offres:

        url_pages = "https://www.leboncoin.fr" + offre
        r = requests.get(url_pages, headers=headers)
        secondarySoup = BeautifulSoup(r.content, "html.parser")
        description = secondarySoup.find("span", {"class": "_1fFkI"}).string
        titre = secondarySoup.find(
            "h1", {"class": "_1VBjc _3c6yv _3eNLO _2QVPN _3zIi4 _2-a8M _1JYGK _35DXM"})
        titre = titre.string
        prix = str(secondarySoup.find(
            "span", {"class": "_3Ce01 _3gP8T _25LNb _35DXM"}).text)
        description_str = str(description).lower()

        if (re.search("travaux|oeuvres|r.novation.|r.nover", description_str)):
            if (re.search("(pas|aucun|quelques|peu)\s(de|un|)?\s?(travaux|oeuvres|r.novation.)", description_str)):
                if (re.search("puit.|grange|ferme", description_str)):
                    offres_premium.append(description_str)
                    offres_premium_url.append(url_pages)
                    offres_premium_title.append(titre)
                    offres_premium_prix.append(prix)

                else:
                    offres_valides.append(description_str)
                    offres_valides_url.append(url_pages)
                    offres_valides_title.append(titre)
                    offres_valides_prix.append(prix)
        else:
            if (re.search("puit.|grange|ferme", description_str)):
                offres_premium.append(description_str)
                offres_premium_url.append(url_pages)
                offres_premium_title.append(titre)
                offres_premium_prix.append(prix)
            else:
                offres_valides.append(description_str)
                offres_valides_url.append(url_pages)
                offres_valides_title.append(titre)
                offres_valides_prix.append(prix)

data = {'Titre': offres_premium_title, 'Prix': offres_premium_prix,
        'Description': offres_premium, 'Lien': offres_premium_url}
df_product = pd.DataFrame(data)
df_product.to_csv('maisons_premium.csv')

data = {'Titre': offres_valides_title, 'Prix': offres_valides_prix,
        'Description': offres_valides, 'Lien': offres_valides_url}
df_product = pd.DataFrame(data)
df_product.to_csv('maisons_valides.csv')
