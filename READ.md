 
Project : Get recipe for given ingradients. 
Description :   
    Suggest possible dishes based ingredients available with the client

Source of data :
    
    1. The recipes.json file contain approximately 9500 recipes, scraped from the website www.marmiton. org.Download it with this command if the above link doesn't work:
    wget https://d1sf7nqdl8wqk.cloudfront.net/recipes.json.gz && gzip -dc recipes.json.gz > recipes.json
    Each line contains a JSON-formatted entry, scraped with python-marmiton. The entry format is described in the package README.   

    2. Super list of ingredients was scrapped from https://www.marmiton.org/recettes/index/ingredient. 
    scripts/collect_ingredients.py has the code for the same. There were mismatches between ingredients present in the recipe list and ingredients scrapped from marmiton, I have    manually fixed 80% of mismatches. For around 100 ingredients in the recipies couldn't be classsified to any available recipie.


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

Challanges: 
   
    Biggest challange was recipie,json doesn't contain proper ingredeints. So matching them is pretty hard. Also had to provide a super list  of ingredients to the custmer to select from. I solved it by scrapping the data from marmiton. 

    Second challenge was to design  table structure for fast retrivel. I came up with a hybrid approach where I use both db and application code to match ingredients. Detailed comment and logic can be found in recipe/reipe.py
    
Optimizations: 
    
    For now I applied couple of optimization techniques like cahcing some static data and also added some filtering on queries. 


How To Deploy :
    
    Application is deployed in heroku.
    I have used this doc to deply app in heroku : https://medium.com/geekculture/how-to-deploy-a-django-app-on-heroku-4d696b458272
    Keep debug == True and don't use postgres. 
