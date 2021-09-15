from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField("название", max_length=50)
    address = models.CharField(
        "адрес",
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        "контактный телефон",
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "рестораны"

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = RestaurantMenuItem.objects.filter(
            availability=True
        ).values_list("product")
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField("название", max_length=50)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("название", max_length=50)
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="категория",
        related_name="products",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        "цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField("картинка")
    special_status = models.BooleanField(
        "спец.предложение",
        default=False,
        db_index=True,
    )
    description = models.TextField(
        "описание",
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="menu_items",
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="продукт",
    )
    availability = models.BooleanField(
        "в продаже", default=True, db_index=True
    )

    class Meta:
        verbose_name = "пункт меню ресторана"
        verbose_name_plural = "пункты меню ресторана"
        unique_together = [["restaurant", "product"]]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

class OrderQuerySet(models.QuerySet):
    def get_price(self):
        return self.orderedproduct_set.annotate(price=F("product__id")*F("quantity")).aggegate(Sum("price"))

class Order(models.Model):
    objects = OrderQuerySet.as_manager()

    status_choices = [
        (True, "Обработано"),
        (False, "Необработано"),        
    ]
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    phonenumber = PhoneNumberField(max_length=32)
    address = models.CharField(max_length=100)
    is_processed = models.BooleanField(choices=status_choices, default=False)
    comment = models.TextField(default="", blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    called_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Order - {self.phonenumber}"
    
    def get_price(self):
        result = self.orderedproduct_set.annotate(price=F("product__price")*F("quantity")).aggregate(Sum("price"))
        if result["price__sum"] is None:
            return 0
        return result["price__sum"]
    
class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="order_position"
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    product_price = models.DecimalField(
        "цена товара",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    total_price = models.DecimalField(
        "общая цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        verbose_name = "позиция"
        verbose_name_plural = "позиции"

    def __str__(self):
        return f"OrderPosition {self.id}"
