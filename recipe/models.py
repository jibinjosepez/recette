from django.db import models

class Recipe(models.Model):
    class Difficulty(models.TextChoices):
        FACILE = 'F', ('facile')
        TRES_FACILE = 'TF', ('très facile')
        NIVEAU_MOYEN = 'NM', ('Niveau moyen')
        DIFFICILE = 'DF', ('difficile')

    class Budget(models.TextChoices):
        BON_MARCHE = 'BM', ('bon marché')
        COUT_MOYEN = 'CM', ('Coût moyen')
        ASSEZ_CHER = 'AC', ('assez cher')

    id = models.AutoField(primary_key=True)
    rate = models.FloatField(null= True) 
    author_tip = models.CharField(max_length=200, null= True)
    budget = models.CharField(max_length=200)
    prep_time_seconds = models.IntegerField(default=0) 
    name = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=200)
    difficulty = models.CharField(
        max_length=2,
        choices=Difficulty.choices,
    )
    people_quantity = models.IntegerField(null= True) 
    cook_time_seconds = models.IntegerField(null= True) 
    total_time_seconds = models.IntegerField(null= True) 
    image = models.TextField(null= True) 
    nb_comments = models.IntegerField(null= True)
    class Meta:
        indexes = [models.Index(fields=['name' ])]

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    img = models.CharField(max_length=200)
    class Meta:
        indexes = [models.Index(fields=['name', ])]
    def __str__(self) :
        return self.name

class RecipeIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True)
    quantiy =  models.TextField(null=True)
    quantiy_unit = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)

class RecipeRawData(models.Model):
    recipe= models.OneToOneField(
        Recipe,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    raw_data = models.TextField()

