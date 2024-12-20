# Generated by Django 5.1.1 on 2024-10-25 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0002_alter_food_image'),
        ('rating', '0002_alter_rating_rating'),
        ('resto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_at', models.DateTimeField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rating.rating')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resto.resto')),
            ],
        ),
    ]
