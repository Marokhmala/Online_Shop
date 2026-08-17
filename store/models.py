from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    short_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    subcategory = models.ForeignKey(   #temporarily
    Subcategory,
    on_delete=models.CASCADE,
    related_name='products',
    null=True,
    blank=True
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )   
    # subcategory = models.ForeignKey(
    #     Subcategory,
    #     on_delete=models.CASCADE,
    #     related_name='products'
    # )
    # brand = models.ForeignKey(
    #     Brand,
    #     on_delete=models.CASCADE,
    #     related_name='products'
    # )

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    text = models.TextField()

    def __str__(self):
        return f'{self.reviewer_name} - {self.product.name}'
