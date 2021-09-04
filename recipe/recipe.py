from recipe.models import Ingredient, RecipeIngredient, RecipeRawData
import json
from django.db.models import Count
from django.core.cache import cache

PERMITTED_PERCENTAGE_OF_MATCHING_ITEM=50
MAX_OUTPUT = 10
REIPIE_WITH_LESS_THAN_2_INGREDIENT = 'recipie_ing_less_than_2'
MINIMUM_INGREDIENT_VALUE = 3

def get_matching_recipe (ingredients):
    
    """ 
        Finds matching recipe for given list of ingredients. 
        intput: list of ingredient_id
        output: List of recipe wich has minimum  matching ingredients, sorted by match and then by user rating.

        Description : 
            Steps:
            1. Get all the recipies with atleast 3 ingredient match to the input. I selected 3 because only very few recipie has ingredients less than 3
            2. Get all recipes with less than 3 ingredients merge it with recipie list. This is cached. 
                we have only 10 recipe with less than 2 items needed. If this grows  the performance will be impacted
            3. Get Recipie with ingredients fromt the table. (this can be cached)
            4. Go through the ingredients of given recipie and find the percentage of map with user inpout
                if it is > PERMITTED_PERCENTAGE_OF_MATCHING_ITEM add to final list
            5. sort recipie with the % match and rating
            6.Prepare final output
        TODO : 
            1. Optimize the queries : We can cache all the recipie and ingredients.
            2. Cache most commenely used ingredients and don't match them. [EG: it is normal to assume everyone has salt]
    """

    #Step 1
    recipe_ids = get_recipe_matching_with_minimum_matching_ingradients(ingredients)
    #Step 2
    recipe_ids.extend(get_recipiewith_less_than_x_ingredient(MINIMUM_INGREDIENT_VALUE))

    if len(recipe_ids) == 0 :
        return []
    #Step 3
    recipe_dict = get_recipe_with_ingredient(recipe_ids)
    #Step 4
    recipie_matched = match_input_ingredient_and_recipie_ingredient(ingredients, recipe_dict)
    #Step 5
    selected_items = sorted(recipie_matched.keys(), key=lambda key: (1 - recipie_matched[key]['missing_percent'], recipe_dict[key][0].recipe.rate if recipe_dict[key][0].recipe.rate else 0))
    #Step 6

    output = serialize_recipe(selected_items, recipe_dict, recipie_matched)  
    print (output)

    return output

def get_recipe_matching_with_minimum_matching_ingradients(ingredients):
    return list(RecipeIngredient.objects.filter(ingredient_id__in=ingredients).values_list("recipe_id", flat=True).annotate(count=Count('recipe_id')).filter(count__gt=3))


def get_recipiewith_less_than_x_ingredient(x):
    if  cache.get(REIPIE_WITH_LESS_THAN_2_INGREDIENT) :
        return cache.get(REIPIE_WITH_LESS_THAN_2_INGREDIENT)
    else:
        queryset = list(RecipeIngredient.objects.filter().values_list('recipe_id', flat=True).annotate(count=Count('recipe_id')).filter(count__lte=x))
        cache.set(REIPIE_WITH_LESS_THAN_2_INGREDIENT, queryset)
        return queryset

def get_recipe_with_ingredient(recipe_ids):
    recipe_dict = {}
    for obj in  RecipeIngredient.objects.filter(recipe_id__in=list(recipe_ids)):
        recipe_dict.setdefault(obj.recipe.id, []).append(obj)
    return recipe_dict

def match_input_ingredient_and_recipie_ingredient(ingredients, recipes):
    ing_set = set(list(map(int, ingredients)))
    recipie_matched = {}
    for key, value in recipes.items():
        # Skip recipes which has far more ingredients than provided ingredients.
        if len(ingredients)/len(value)  <  PERMITTED_PERCENTAGE_OF_MATCHING_ITEM/100:
            continue

        missing_ing =  0
        for rec_ing in value:
            rec_ing.missing = False
            if rec_ing.ingredient:
                if not rec_ing.ingredient.id in ing_set: 
                    missing_ing += 1
                    rec_ing.missing = True
                #return if  missing ingredients are more than allowed
                if missing_ing /len(value) > 1 -  PERMITTED_PERCENTAGE_OF_MATCHING_ITEM/100:
                    break

        if (len(value) - missing_ing)/len(value) > PERMITTED_PERCENTAGE_OF_MATCHING_ITEM/100: 
            recipie_matched[key] = {
                'missing_count' : missing_ing,
                'missing_percent' : len(value) - missing_ing/len(value)
            }
    return recipie_matched
    

def serialize_recipe(selected_items, recipe_dict, recipie_matched):
    output = []
    for item in selected_items:
        recipe = {
            'id' : recipe_dict[item][0].recipe.id,
            'rate' : recipe_dict[item][0].recipe.rate,
            'name' : recipe_dict[item][0].recipe.name,
            'people_quantity' : recipe_dict[item][0].recipe.people_quantity,
            'image' : recipe_dict[item][0].recipe.image,
            'missing_count' : recipie_matched[item]['missing_count']
        }
        if not recipe['image']:
            recipe['image'] = 'https://assets.afcdn.com/recipe/20100101/ingredient_default_w200h200c1.jpg'
        recipe['ingredients'] = []
        for rec_ing in recipe_dict[item]:
            image = 'https://assets.afcdn.com/recipe/20100101/ingredient_default_w200h200c1.jpg'
            ing_id = 0
            if rec_ing.ingredient: 
                image = rec_ing.ingredient.img
                ing_id = rec_ing.ingredient.id
            recipe['ingredients'].append({"ingredient" : rec_ing.description, "missing" : rec_ing.missing , 'ing_id' : ing_id, 'id' : rec_ing.id, 'img' : image})
        output.append(recipe)
    return output
