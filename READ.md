 
Project : Get recipe for given ingradients. 
Description :   
    Suggest possible dishes based ingredients available with the client

Source of data :
    1. The recipes.json file contain approximately 9500 recipes, scraped from the website www.marmiton.org.
    Download it with this command if the above link doesn't work:
    wget https://d1sf7nqdl8wqk.cloudfront.net/recipes.json.gz && gzip -dc recipes.json.gz > recipes.json
    Each line contains a JSON-formatted entry, scraped with python-marmiton. The entry format is described in the package README.


