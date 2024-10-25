from django.db import models

class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(default='https://cdn1-production-images-kly.akamaized.net/jGwFeeZ3t6lUfdkz-S9BeFU6NnA=/469x625/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3463633/original/053964600_1621840903-bolu_pandan_panggang.jpg')  # Provide a default value
    promo = models.CharField(max_length=255)