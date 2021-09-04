from dal import autocomplete
from django import forms
from recipe.models import Ingredient

class IngredientForm(forms.ModelForm):
    ing = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete', attrs={"data-placeholder": "My Ingredients"}),
        label = ''
    )
    class Meta:
        model = Ingredient
        fields = []