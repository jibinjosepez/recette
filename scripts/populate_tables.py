#!/usr/local/bin/python
import sys
path = '/home/jibinjosepez/work/pennylane/recette'
sys.path.append(path)

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'recette.settings'

import django
django.setup()

from django.db import transaction
import re
from util import *
from recipe.models import *

def main():
    ingr_from_marm = get_ingredients_from_marmiton(FILE_NAME['MARMITON_INGR'])
    insert_ingredient(ingr_from_marm)
    recipes = parse_recipe(read_file(FILE_NAME['RECIPIES'])) 
    ingr_marm_ingr_map = parse_ingredient_file(read_file(FILE_NAME['INGR_MAP_RECIPIE_TO_MARMITON'])) 
    insert_recipe(recipes, ingr_marm_ingr_map)

def insert_ingredient(ingr_from_marm):
    for key, val in ingr_from_marm.items():
        ing = Ingredient(name = key, img = val)
        ing.save()

def insert_recipe(recipes, recp_marm_ingr_map):
    for rec in recipes:
        try: 
            with transaction.atomic():
                rec_dao = Recipe() 
                if rec['rate']:
                    rec_dao.rate = rec['rate']
                if rec['author_tip']:
                    rec_dao.author_tip = rec['author_tip']
                rec_dao.author = rec['author']
                if rec['image']:
                    rec_dao.image = rec['image']
                if rec['budget']:
                    rec_dao.budget = rec['budget']
                rec_dao.name = rec['name']
                if rec['nb_comments']:
                    rec_dao.nb_comments = rec['nb_comments']
                if rec['prep_time']:
                    rec_dao.prep_time_seconds = convert_to_seconds(rec['prep_time'])
                if rec['people_quantity']:
                    rec_dao.people_quantity = rec['people_quantity']
                if rec['cook_time']:
                    rec_dao.cook_time_seconds = convert_to_seconds(rec['cook_time'])
                if rec['total_time']:
                    rec_dao.total_time_seconds = convert_to_seconds(rec['total_time'])
                rec_dao.save()
                save_ingredients(rec_dao, rec['ingredients'], recp_marm_ingr_map)
                save_tags(rec_dao, rec['tags'])
                save_raw_data(rec_dao, rec)
        except Exception as e:
            print ("Recipe",  rec['name'], e)
            

def save_raw_data(id, rec):
    raw = RecipeRawData(recipe = id, raw_data = json.dumps(rec))
    raw.save()

def save_tags(id, tags):
    for tag in tags:
        tag_dao = Tag(recipe = id, tag = tag)
        tag_dao.save()

def save_ingredients(id, ingredients, recp_marm_ingr_map):
    for ing in ingredients:
        ing_dao = RecipeIngredient()
        ing_dao.recipe = id
        ing_dao.description = ing
        ing_dao.quantiy = get_quanitiy(ing)
        ing_dao.quantiy_unit = get_quanitiy_unit(ing)
        ingredient = get_ingredient_id(ing, recp_marm_ingr_map)
        if ingredient :
            ing_dao.ingredient = ingredient
        ing_dao.save()

def get_ingredient_id(ing, recp_marm_ingr_map):
    ing_without_unit = convert_ingredient(ing)
    ingredient =  recp_marm_ingr_map[ing_without_unit]
    try:
        ing = Ingredient.objects.get(name = ingredient)
    except Ingredient.DoesNotExist:
        print(ingredient, ing_without_unit, ing)
        return None
    return ing

def get_quanitiy(ing):
    if ing[0].isdigit() and len(ing.split(' ')) > 1 :
        return re.sub("[a-zA-Z]+", '', ing.split(' ', 1)[0])
    return None

def get_quanitiy_unit(ing):
    if ing[0].isdigit() and len(ing.split(' ')) > 1 :
        return re.sub("[^a-zA-Z]+", '', ing.split(' ', 1)[0])
    return None

def convert_to_seconds(string):
    if string.endswith("h"):
        hours = int(re.search(r'\d+', string).group())
        return hours*60*60
    elif string.endswith("m"):
        minutes = int(re.search(r'\d+',string).group())
        return minutes*60
    elif string.endswith("s"):
        seconds = int(re.search(r'\d+',string).group())
        return seconds
    elif string.isdigit():
        return int(string)
    else:
        return 0
main()