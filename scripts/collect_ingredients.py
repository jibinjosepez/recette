#!/usr/local/bin/python
# change above line to point to local
# python executable

import requests
from bs4 import BeautifulSoup
from requests.models import iter_slices

BASE_URL = "https://www.marmiton.org/recettes/index/ingredient"
FILE_LOCATION = "../data/marmiton_ingredients.txt"

def create_ingrediant_list_from_marmiton():
    items = scrape_ingredient_From_marimton()
    add_hardcoded_data(items) #Maintian a file or db for this
    write_to_file(items)

def scrape_ingredient_From_marimton(): 
    '''
        Scrape  marmiton.org and get list of of ingredients
        marmiton uses first letter of ingredient and page number as url to display ingredients
        Keep incrementing the letters and page id till the apge is empty
    '''

    items = {}
    ch = 97
    while ch <= 124:
        i = 1
        while True:
            url = BASE_URL + "/" + chr(ch) + "/" + str(i)
            new_items = scrape(url)
            if len(new_items):
                items.update(new_items)
            else:
                break
            i += 1
        ch += 1
    return items

def add_hardcoded_data(items):
    '''
        Some of the basi ingredinets mimatching fromt the recipe and the ingredient from marmiton
        It is based on my nalaysis. This heled to bring down the mismatch by 90%
    '''
    items['épinard'] =  'https://assets.afcdn.com/recipe/20170607/67594_w200h200cx350cy350.jpgs'
    items['orade']  =   'https://assets.afcdn.com/recipe/20170621/69025_w200h200cxt0cyt0cxb700cyb700.jpg'
    items['fève']   =   'https://assets.afcdn.com/recipe/20170607/67507_w200h200cx350cy350.jpg'
    items['légume'] =   'https://assets.afcdn.com/recipe/20170607/67398_w200h200cx350cy350.jpg'
    items['inde']   =   'https://assets.afcdn.com/recipe/20170607/67734_w200h200cx350cy350.jpg'
    items['cerise'] =   'https://assets.afcdn.com/recipe/20170607/67491_w200h200cx350cy350.jpgs'
    items['pistache'] = 'https://assets.afcdn.com/recipe/20170607/67716_w200h200cx350cy350.jpg'
    items['cornichon'] = 'https://assets.afcdn.com/recipe/20170607/67340_w200h200cx350cy350.jpg'
    items['chavroux'] =  'https://assets.afcdn.com/recipe/20100101/ingredient_default_w200h200c1.jpg'
    items['ndives'] =  'https://assets.afcdn.com/recipe/20170607/67408_w200h200cx350cy350.jpg'
    items['ndive'] =  'https://assets.afcdn.com/recipe/20170607/67408_w200h200cx350cy350.jpg'
    items['chavroux'] =  'https://assets.afcdn.com/recipe/20100101/ingredient_default_w200h200c1.jpg'
    items['aurade'] =  'https://assets.afcdn.com/recipe/20180213/77535_w200h200cx2350cy2350cxt0cyt0cxb4700cyb4700.jpg'
    items['aurades'] =  'https://assets.afcdn.com/recipe/20180213/77535_w200h200cx2350cy2350cxt0cyt0cxb4700cyb4700.jpg'
    items['stragon'] =  'https://assets.afcdn.com/recipe/20170607/67546_w200h200cx350cy350.jpg'
    items['tagliatelle'] =  'https://assets.afcdn.com/recipe/20170621/69175_w200h200cxt0cyt0cxb700cyb700.jpg'
    items['crevette'] =  'https://assets.afcdn.com/recipe/20170607/67700_w200h200cx2736cy1824.jpg'
    items['scargots'] =  'https://assets.afcdn.com/recipe/20170607/67655_w200h200cx350cy350.jpg'
    items['morille'] =  'https://assets.afcdn.com/recipe/20170607/67705_w200h200cx350cy350.jpg'

def valid_url(url):
    response = requests.get(url)
    return response.status_code == 200

def scrape(url):
    print(url)
    items = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("div", class_="index-item-card")
    for result in results:
        ingr = result.find("div", class_="index-item-card-name").text.strip().lower()
        if "(" in ingr:
            items[ingr.split("(")[0]] = (
                result.find("img", class_="").attrs["src"].strip()
            )
            items[ingr.split("(")[1].replace(")", "")] = (
                result.find("img", class_="").attrs["src"].strip()
            )
        else:
            items[ingr] = result.find("img", class_="").attrs["src"].strip()
    return items

def write_to_file(data):
    filehandler = open(FILE_LOCATION, "w")
    for key, value in data.items():
        filehandler.write("%s : %s\n" % (key, value))
    filehandler.close()

create_ingrediant_list_from_marmiton()
