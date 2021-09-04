#!/usr/local/bin/python

import re
import json
from util import *

def main():    
    recipies = parse_recipe(read_file(FILE_NAME['RECIPIES'])) 
    write_dict_to_file(FILE_NAME['DIFFICULTIES'], get_unique_difficulty_with_count(recipies))
    write_dict_to_file(FILE_NAME['BUDGET'], get_unique_budget_with_count(recipies))
    write_dict_to_file(FILE_NAME['TAGS'], get_unique_tags_with_count(recipies))
    ingr_from_recipie = get_unique_ingredients_from_recipie(recipies)
    write_dict_to_file(FILE_NAME['INGREDIENTS'], ingr_from_recipie)
    write_dict_to_file(FILE_NAME['QUANTITY_UNIT'], get_unique_quantity_unit(recipies))
    ingr_from_marm = sorted(get_ingredients_from_marmiton(FILE_NAME['MARMITON_INGR']).keys(), key=lambda x: len(x.split()), reverse=True)
    map, missing = get_ingr_map_from_recipie_to_maram(ingr_from_marm, ingr_from_recipie)
    write_dict_to_file(FILE_NAME['INGR_MAP_RECIPIE_TO_MARMITON'],map)
    write_dict_to_file(FILE_NAME['MISSING_INGREDIENTS'],missing)

def get_ingr_map_from_recipie_to_maram(ingr_from_marm, ingr_from_recipie):
    map = {}
    missing_dict = {}
    marm_set = set(ingr_from_marm)
    for rec in ingr_from_recipie.keys():
        if rec in marm_set: 
            map[rec] = rec
        else:
            for ingr in ingr_from_marm:
                if ingr in rec:
                    map[rec] = ingr
                    break
        if not rec in map:
            map[rec] = rec
            if rec in missing_dict.keys():
                missing_dict[rec] += 1
            else:
                missing_dict[rec] = 1
    return (map, missing_dict)

def get_unique_difficulty_with_count(recipe):
    difficulties = {}
    for item in recipe:
        key = item.get('difficulty', None)
        if key in difficulties.keys():
            difficulties[key] += 1
        else:
            difficulties[key] = 1
    return difficulties
    
def get_unique_tags_with_count(recipe):
    tags_dict = {}
    for item in recipe:
        tags = item.get('tags', None)
        for tag in tags: 
            if tag in tags_dict.keys():
                tags_dict[tag] += 1
            else:
                tags_dict[tag] = 1
    return tags_dict

def get_unique_budget_with_count(recipe):
    budget = {}
    for item in recipe:
        key = item.get('budget', None)
        if key in budget.keys():
            budget[key] += 1
        else:
            budget[key] = 1
    return budget

def get_unique_ingredients_from_recipie(recipe):
    ingredient_dict = {}
    for item in recipe:
        ingredients = item.get('ingredients', None)
        for ingredient in ingredients: 
            ing = convert_ingredient(ingredient)
            if ing in ingredient_dict.keys():
                ingredient_dict[ing] += 1
            else:
                ingredient_dict[ing] = 1
    return ingredient_dict
    # return dict(sorted(ingredient_dict.items(), key=lambda item: item[1]))

def get_unique_quantity_unit(recipe):
    qnt_units = {}
    for item in recipe:
        ingredients = item.get('ingredients', None)
        for ingredient in ingredients: 
            ing = parse_ingredient_unit(ingredient)
            if ing in qnt_units.keys():
                qnt_units[ing] += 1
            else:
                qnt_units[ing] = 1
    return qnt_units

def parse_ingredient_unit(ing):
    if ing[0].isdigit() and len(ing.split(' ')) > 1 :
        return re.sub("[^a-zA-Z]+", '', ing.split(' ', 1)[0])
    return None

main()
