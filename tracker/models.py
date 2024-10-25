from django.db import models
from halal_bites import Food, Resto, Forum

class Tracker(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Resto, on_delete=models.CASCADE)
    rating = models.ForeignKey(Forum, on_delete=models.CASCADE)
    order_at = models.DateTimeField() 

    def __str__(self):
        return f"{self.food.name} at {self.restaurant.name} - Rated {self.rating.score}"
