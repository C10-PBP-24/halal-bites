# Generated by Django 5.1.2 on 2024-10-25 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.URLField(default='https://cdn1-production-images-kly.akamaized.net/jGwFeeZ3t6lUfdkz-S9BeFU6NnA=/469x625/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3463633/original/053964600_1621840903-bolu_pandan_panggang.jpg')),
                ('promo', models.CharField(max_length=255)),
            ],
        ),
    ]
