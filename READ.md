 
Project : Get recipe for given ingradients. 
Description :   
    Suggest possible dishes based ingredients available with the client

Source of data :
    1. The recipes.json file contain approximately 9500 recipes, scraped from the website www.marmiton. org.Download it with this command if the above link doesn't work:
    wget https://d1sf7nqdl8wqk.cloudfront.net/recipes.json.gz && gzip -dc recipes.json.gz > recipes.json
    Each line contains a JSON-formatted entry, scraped with python-marmiton. The entry format is described in the package README.   

    2. Super list of ingredients was scrapped from https://www.marmiton.org/recettes/index/ingredient. 
    scripts/collect_ingredients.py has the code for the same. There were mismatches between ingredients present in the recipe list and ingredients scrapped from marmiton, I have manually fixed 80% of mismatches. For around 100 ingredients in the recipies couldn't be classsified to any available recipie.

Analysis of data: 
    scripts/recipe_analyzer.py has set of analysis tools which I used to desigh tables. Most of this scripts populated some insightful data in the folder data.


Tables:  [Detailed structure and indexes can be found in recipe/models.py]
    Recipe : 
        Contais high lever information of Recipies.
    
    Ingredients: 
        Contains Ingredient data scrapped from the marmiton. This is not same as the ingredients provided in the Recipe. Ingredients provided in  recipie.json has ingredients with quantity and other description

    RecipieIngredient:
        This table contains info about recipie and ingredients, this also contains ingredient_info provided in the recipe.json

    Tag : 
        Contains tag and recipe mapping, not used in this app.

    Recipe.json and scrapped ingredient data from marmiton are stored in DB via scripts/populate_tables.py, 

    User Search data is not collected as of now. It is a nice to have.
    

Applications :
    This is a single page application developed in Django. Django's MVC framework is used to design the application. I have used default sqlite to run the app.


Optimizations: 


How To Deploy :
    

