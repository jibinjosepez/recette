from recipe.recipe import get_matching_recipe
from django.shortcuts import render
from dal import autocomplete
from recipe.forms import IngredientForm
from recipe.models import Ingredient
from django.shortcuts import render
from django.views import View

class IngredientSearchView(View):
    form_class = IngredientForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = request.POST
        ingredients = list(post.getlist('ing'))
        form = self.form_class(initial = { "ing" :  ingredients})
        recipes = get_matching_recipe(ingredients)
        return render(request, self.template_name, context={'form': form, "recipes": recipes})

class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Ingredient.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

    def get_result_label(self, item):
        return item.name

    def get_selected_result_label(self, item):
        return item.name
