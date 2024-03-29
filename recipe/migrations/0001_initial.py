# Generated by Django 3.2.7 on 2021-09-04 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('img', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.FloatField(null=True)),
                ('author_tip', models.CharField(max_length=200, null=True)),
                ('budget', models.CharField(max_length=200)),
                ('prep_time_seconds', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('author', models.CharField(max_length=200)),
                ('difficulty', models.CharField(choices=[('F', 'facile'), ('TF', 'très facile'), ('NM', 'Niveau moyen'), ('DF', 'difficile')], max_length=2)),
                ('people_quantity', models.IntegerField(null=True)),
                ('cook_time_seconds', models.IntegerField(null=True)),
                ('total_time_seconds', models.IntegerField(null=True)),
                ('image', models.TextField(null=True)),
                ('nb_comments', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeRawData',
            fields=[
                ('recipe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='recipe.recipe')),
                ('raw_data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=200)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantiy', models.TextField(null=True)),
                ('quantiy_unit', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=200)),
                ('ingredient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['name'], name='recipe_reci_name_6b613c_idx'),
        ),
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='recipe_ingr_name_0ead22_idx'),
        ),
    ]
