import json
import re

FILE_LOCATION = '../data'
FILE_NAME = {
    "RECIPIES" : 'recipes.json',
    "DIFFICULTIES" : 'difficulties.txt',
    "TAGS" : 'tags.txt',
    "BUDGET" : 'budget.txt',
    "INGREDIENTS" : 'ingredients_from_recipie.txt',
    "QUANTITY_UNIT": 'quanity_unit.txt',
    "MARMITON_INGR" : 'marmiton_ingredients.txt',
    "INGR_MAP_RECIPIE_TO_MARMITON" : 'ingredient_map.txt',
    "MISSING_INGREDIENTS" : 'missing_ingredient_marmiton.txt'

}

def read_file(file_name):
    text_file = open(get_file_path(file_name), "r")
    lines = text_file.readlines()
    text_file.close
    return lines

def parse_recipe (lines):
    recipies = []
    for item in lines:
        recipies.append(json.loads(item.lower()))
    return recipies

def convert_ingredient(ing):
    if ing[0].isdigit() and len(ing.split(' ')) > 1 :
        ing = ing.split(' ', 1)[1]
    removeOptions =  ing.split("(")[0]
    removeBeginingDeOrA = removeOptions.lstrip("de ").lstrip("à ")
    removeSpecialCharacter = re.sub('®', '', removeBeginingDeOrA)
    return removeSpecialCharacter

def parse_ingredient_file (lines):
    ingr = {}
    for item in lines:
        ingr[item.split(" : ")[0]] = item.split(" : ")[1].strip()
    return ingr
def get_file_path(file_name):
    return FILE_LOCATION + '/' + file_name

def get_ingredients_from_marmiton(file_name) :
    text_file = open(get_file_path(file_name), "r")
    lines = text_file.readlines()
    text_file.close
    ingrs = {}
    for line in lines:
        ingrs[line.split(" : ")[0]] = line.split(" : ")[1].strip() 
    return ingrs

def write_dict_to_file(file_name, dict):
    filehandler = open(get_file_path(file_name), 'w')
    for key, value in dict.items(): 
        filehandler.write('%s : %s\n' % (key, value))
    filehandler.close()
    print(F"{file_name}  written") 
