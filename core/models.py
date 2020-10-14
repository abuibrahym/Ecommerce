from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'),
)
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)
QUANTITY_CHOICES = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    additional_information = models.TextField()
    img = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    def product_detail_url(self):
        return reverse('core:product', kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={'pk': self.pk})

    def get_add_to_favorites_url(self):
        return reverse('core:add-to-favorites', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # total_items_in_cart = models.IntegerField(default=0)
    # total_amount = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.quantity} {self.item.title}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    total_items_in_cart = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    countries = CountryField(multiple=False)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class FavoriteItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title
